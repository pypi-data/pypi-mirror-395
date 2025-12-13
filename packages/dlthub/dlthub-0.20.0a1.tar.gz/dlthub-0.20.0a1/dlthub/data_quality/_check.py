from __future__ import annotations

import abc
from collections.abc import Mapping, Sequence
from typing import Any

import dlt
from dlt.common.utils import simple_repr, without_none
from sqlglot import exp as sge

from dlthub.data_quality._checks_runner import row_level_checks


class _BaseCheck(abc.ABC):
    @property
    @abc.abstractmethod
    def name(cls) -> str:
        """Name of the check"""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Description of the check"""

    @property
    @abc.abstractmethod
    def parameters(self) -> Sequence[str]:
        """Parameters used by the check"""

    @property
    @abc.abstractmethod
    def qualified_name(self) -> str:
        """Name that uniquely identifies a check.

        This typically involves namespacing `{check_name}.{param1_value}.{param2_value}`,
        and can include some check parameters.
        """


# TODO we need to version built-in checks to allow schema migration mechanism
class LazyCheck(_BaseCheck):
    @abc.abstractmethod
    def __init__(self, **kwargs: Any):
        """Initialize the check with the given arguments"""
        self._arguments = without_none(kwargs)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        return self.__doc__.format(**self.arguments)

    @property
    def parameters(self) -> Sequence[str]:
        return tuple(
            [k for k in self.__init__.__annotations__.keys() if k != "return"]  # type: ignore[misc]
        )

    @property
    def arguments(self) -> Mapping[str, Any]:
        return self._arguments

    # TODO probably better to implement `qualified_name` per class and use a test to ensure
    # a naming convention
    @property
    def qualified_name(self) -> str:
        # TODO use dlt name normalization logic used in the `dlt.Schema`
        qualified = self.name
        for key in sorted(self.parameters):
            argument = self.arguments[key]
            # use `column` value as prefix instead of suffix
            if key == "column":
                qualified = argument + f"__{qualified}"
                continue

            if not isinstance(argument, str) and isinstance(argument, Sequence):
                argument = "_".join(argument)

            qualified += f"__{argument}"

        return qualified

    @property
    @abc.abstractmethod
    def expr(self) -> sge.Expression:
        """SQL, SQLGlot, or Ibis expression underlying the check"""

    # NOTE this works for row-level checks
    def run(self, table_rel: dlt.Relation) -> dlt.Relation:
        """Create a `dlt.Relation` from the `check.expr`. This is useful
        for executing a single check during development.

        This is a convenience method over the internal `row_level_checks()`
        """
        return row_level_checks(table_rel, checks=[self])

    def __repr__(self) -> str:
        return simple_repr(
            self.name, **{k: v for k, v in self.arguments.items() if k != "true_is_success"}
        )

    def __eq__(self, other: Any) -> bool:
        return bool(
            self.expr == getattr(other, "expr", None)
            and self.qualified_name == getattr(other, "qualified_name", None)
            and self.name == getattr(other, "name", None)
        )
