"""Data quality dashboard widget functions for marimo notebooks.

This module provides reusable functions for creating data quality widgets
that can be imported into any marimo notebook.
"""

from typing import Any, List, Optional, Tuple

import dlt
import marimo as mo

from dlthub.data_quality.storage import (
    DLT_CHECKS_RESULTS_TABLE_NAME,
    DLT_DATA_QUALITY_SCHEMA_NAME,
    TABLE_NAME_COL,
    QUALIFIED_CHECK_NAME_COL,
    ROW_COUNT_COL,
    CHECK_SUCCESS_COUNT_COL,
    CHECK_SUCCESS_RATE_COL,
)


def get_checks_arrow_table(dlt_pipeline: dlt.Pipeline) -> Optional[Any]:
    """Get the data quality checks results as a PyArrow table.

    Args:
        dlt_pipeline: The dlt pipeline instance to get checks from.

    Returns:
        PyArrow table with check results, or None if checks table doesn't exist.
    """
    # Get the dataset from the pipeline
    checks_dataset = dlt.dataset(
        destination=dlt_pipeline.destination,
        dataset_name=dlt_pipeline.dataset_name,
        schema=DLT_DATA_QUALITY_SCHEMA_NAME,
    )

    dlt_checks_schema = checks_dataset.schema
    if dlt_checks_schema.is_new:
        return None

    table_name = dlt_checks_schema.naming.normalize_table_identifier(DLT_CHECKS_RESULTS_TABLE_NAME)
    # Check if checks table exists
    if table_name in dlt_checks_schema.tables:
        return checks_dataset.table(table_name).arrow()
    return None


def create_data_quality_controls(
    dlt_pipeline: Optional[dlt.Pipeline] = None,
) -> Tuple[
    Optional[mo.ui.checkbox],
    Optional[mo.ui.dropdown],
    Optional[mo.ui.slider],
    Optional[Any],
]:
    """Create filter controls for the data quality widget.

    This function creates UI controls for filtering data quality check results.
    Import and call this function from your marimo notebook to get the controls.

    Args:
        dlt_pipeline: The dlt pipeline instance

    Returns:
        Tuple of (show_only_failed_checkbox, table_dropdown, failure_rate_slider, checks_arrow)
        or (None, None, None, None) if not available

    Example:
        ```python
        from dlthub.data_quality._dashboard import create_data_quality_controls

        checkbox, dropdown, slider, checks_data = create_data_quality_controls(pipeline)
        ```
    """
    show_only_failed_checkbox, table_dropdown, failure_rate_slider, checks_arrow = (
        None,
        None,
        None,
        None,
    )
    import pyarrow.compute as pc

    if dlt_pipeline:
        checks_arrow = get_checks_arrow_table(dlt_pipeline)
        if checks_arrow is not None and checks_arrow.num_rows > 0:
            try:
                # Get unique table names from Arrow table
                table_names_list = pc.unique(checks_arrow.column(TABLE_NAME_COL)).to_pylist()
                table_names_sorted = sorted(table_names_list)

                show_only_failed_checkbox = mo.ui.checkbox(
                    value=False,
                    label="Show only failed checks",
                )

                table_dropdown = (
                    mo.ui.dropdown(
                        options=["All"] + table_names_sorted,
                        value="All",
                        label="Filter by Table",
                    )
                    if table_names_sorted
                    else None
                )

                failure_rate_slider = mo.ui.slider(
                    start=0,
                    stop=100,
                    step=1,
                    value=0,
                    label="Minimum Failure Rate (%)",
                )
            except Exception:
                pass

    return (show_only_failed_checkbox, table_dropdown, failure_rate_slider, checks_arrow)


def data_quality_widget(
    dlt_pipeline: Optional[dlt.Pipeline] = None,
    failure_rate_slider: Optional[mo.ui.slider] = None,
    failure_rate_filter_value: Optional[float] = None,
    show_only_failed_checkbox: Optional[mo.ui.checkbox] = None,
    show_only_failed_value: Optional[bool] = False,
    table_dropdown: Optional[mo.ui.dropdown] = None,
    table_name_filter_value: Optional[str] = None,
    checks_arrow: Optional[Any] = None,
) -> Any:
    """Create a data quality widget displaying check results.

    This function builds a marimo vstack with data quality check results,
    including filtering controls and a styled table.

    Args:
        dlt_pipeline: The dlt pipeline instance to get checks from
        failure_rate_slider: Optional slider control to display
        failure_rate_filter_value: Optional minimum failure rate to filter by
        show_only_failed_checkbox: Optional checkbox control to display
        show_only_failed_value: Boolean to show only failed checks
        table_dropdown: Optional dropdown control to display
        table_name_filter_value: Optional table name to filter by
        checks_arrow: Optional PyArrow table with check results

    Returns:
        mo.vstack with the widget UI, or None if checks are not available

    Example:
        ```python
        from dlthub.data_quality._dashboard import (
            create_data_quality_controls,
            data_quality_widget
        )

        # In cell 1: Create controls
        checkbox, dropdown, slider, checks_data = create_data_quality_controls(pipeline)

        # In cell 2: Display widget (access .value in separate cell for reactivity)
        widget = data_quality_widget(
            dlt_pipeline=pipeline,
            show_only_failed_checkbox=checkbox,
            show_only_failed_value=checkbox.value if checkbox else False,
            table_dropdown=dropdown,
            table_name_filter_value=dropdown.value if dropdown else None,
            failure_rate_slider=slider,
            failure_rate_filter_value=slider.value if slider else None,
            checks_arrow=checks_data,
        )
        widget
        ```
    """
    _result: List[Any] = []

    if not dlt_pipeline:
        _result.append(mo.md("**No pipeline selected.**"))
        return mo.vstack(_result) if _result else None

    try:
        if checks_arrow is None or checks_arrow.num_rows == 0:
            _result.append(
                mo.md("**No checks found:** Checks have not been executed yet for this dataset.")
            )
            return mo.vstack(_result) if _result else None

        # Convert to list of dictionaries using PyArrow
        records = checks_arrow.to_pylist()

        if not records:
            _result.append(mo.md("**No check results found:** Table exists but is empty."))
            return mo.vstack(_result) if _result else None

        # Split check_qualified_name into column and check_name
        # Format: column__check_name or check_name
        def split_check_name(qualified_name: str) -> Tuple[str, str]:
            parts = qualified_name.split("__", 1)
            if len(parts) == 2:
                return parts[0], parts[1]  # column, check_name
            return "", parts[0]  # no column, just check_name

        # Process records: add computed columns
        processed_records = []
        for record in records:
            qualified_name = record.get(QUALIFIED_CHECK_NAME_COL, "")
            column, check_name = split_check_name(qualified_name)

            row_count = record.get(ROW_COUNT_COL, 0)
            success_count = record.get(CHECK_SUCCESS_COUNT_COL, 0)

            # Add computed columns
            new_record = {
                **record,
                "column": column,
                "check_name": check_name,
                "is_failed": row_count > success_count,
                "failure_rate_pct": (
                    round((row_count - success_count) / row_count * 100, 4)
                    if row_count > 0
                    else 0.0
                ),
            }
            processed_records.append(new_record)

        # Apply filters using the provided values
        filtered_records = processed_records.copy()

        if table_name_filter_value and table_name_filter_value != "All":
            filtered_records = [
                r for r in filtered_records if r.get(TABLE_NAME_COL) == table_name_filter_value
            ]

        if failure_rate_filter_value is not None and failure_rate_filter_value > 0:
            filtered_records = [
                r
                for r in filtered_records
                if r.get("failure_rate_pct", 0) >= failure_rate_filter_value
            ]

        # Determine which checks to show based on filter
        failed_records = [r for r in filtered_records if r.get("is_failed", False)]
        total_failed = len(failed_records)
        total_checks = len(filtered_records)

        # Apply "show only failed" filter if enabled
        if show_only_failed_value:
            display_records = failed_records
            if len(display_records) == 0:
                _result.append(mo.md("**No failed checks match the current filters.**"))
                # Still show controls if provided
                controls_empty: List[Any] = []
                if show_only_failed_checkbox is not None:
                    controls_empty.append(show_only_failed_checkbox)
                if table_dropdown is not None:
                    controls_empty.append(table_dropdown)
                if failure_rate_slider is not None:
                    controls_empty.append(failure_rate_slider)
                if controls_empty:
                    _result.append(mo.hstack(controls_empty, justify="start", gap=2))
                return mo.vstack(_result) if _result else None
            else:
                _result.append(
                    mo.md(f"### ❌ Failed Checks Only ({total_failed} of {total_checks} total)")
                )
        else:
            # Show all checks by default
            display_records = filtered_records
            if total_failed == 0:
                _result.append(mo.md(f"### ✅ All Checks Passed ({total_checks} checks)"))
            else:
                _result.append(
                    mo.md(f"### All Checks ({total_failed} failed out of {total_checks} total)")
                )

        # Add filter controls if provided (for display only)
        controls_display: List[Any] = []
        if show_only_failed_checkbox is not None:
            controls_display.append(show_only_failed_checkbox)
        if table_dropdown is not None:
            controls_display.append(table_dropdown)
        if failure_rate_slider is not None:
            controls_display.append(failure_rate_slider)
        if controls_display:
            _result.append(mo.hstack(controls_display, justify="start", gap=2))

        # Prepare display columns with renamed keys
        column_mapping = {
            TABLE_NAME_COL: "Table",
            "column": "Column",
            "check_name": "Check",
            ROW_COUNT_COL: "Row Count",
            CHECK_SUCCESS_COUNT_COL: "Success Count",
            CHECK_SUCCESS_RATE_COL: "Success Rate",
            "failure_rate_pct": "Failure Rate %",
        }

        # Select and rename columns for display
        table_records = []
        for record in display_records:
            new_record = {
                column_mapping.get(key, key): record.get(key)
                for key in [
                    TABLE_NAME_COL,
                    "column",
                    "check_name",
                    ROW_COUNT_COL,
                    CHECK_SUCCESS_COUNT_COL,
                    CHECK_SUCCESS_RATE_COL,
                    "failure_rate_pct",
                ]
            }
            table_records.append(new_record)

        # Style function for failed checks - highlight Success Rate cell when < 1.0
        def style_failed_cells(row_id: str, column_name: str, value: Any) -> dict[str, Any]:
            """Style Success Rate cells with red background when < 1.0."""
            if column_name == "Success Rate" and value is not None:
                try:
                    if float(value) < 1.0:
                        return {"backgroundColor": "#ffebee", "color": "#c62828"}
                except (ValueError, TypeError):
                    pass
            return {}

        _result.append(
            mo.ui.table(
                table_records,
                style_cell=style_failed_cells,
            )
        )

        # Add summary statistics (using original records, not filtered)
        total_checks_all = len(processed_records)
        total_failed_all = sum(1 for r in processed_records if r.get("is_failed", False))
        if total_checks_all > 0:
            _result.append(
                mo.md(
                    f"**Summary:** {total_failed_all} failed out of "
                    f"{total_checks_all} total checks "
                    f"({total_failed_all / total_checks_all * 100:.1f}% failure rate)"
                )
            )

    except Exception as e:
        _result.append(
            mo.callout(
                mo.md(f"**Error loading checks:** {str(e)}"),
                kind="danger",
            )
        )

    return mo.vstack(_result) if _result else None
