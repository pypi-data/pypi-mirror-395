"""Filterable object list."""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from inspect import isclass
from typing import Literal

from click import Argument, Context, UsageError
from click.shell_completion import CompletionItem

from cmem_cmemc.completion import finalize_completion, get_completion_args
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.title_helper import TitleHelper


class Filter(ABC):
    """Base class for object list filters"""

    name: str
    description: str

    @abstractmethod
    def is_filtered(self, object_: dict, value: str) -> bool:
        """Return True if the object is filtered (stays in list)."""

    def filter_list(self, objects: list[dict], value: str) -> list[dict]:
        """Filter a given dictionary list"""
        return [o for o in objects if self.is_filtered(object_=o, value=value)]

    @abstractmethod
    def complete_values(self, objects: list[dict], incomplete: str) -> list[CompletionItem]:
        """Provide completion items for filter values"""


def compare_str_equality(ctx: Filter, object_value: str, filter_value: str) -> bool:  # noqa: ARG001
    """Return True if object_value and filter_value are equal"""
    return object_value == filter_value


def compare_int_lower_than(ctx: Filter, object_value: str, filter_value: str) -> bool:
    """Return True if object_value lower than filter_value"""
    try:
        filter_value_int = int(filter_value)
    except ValueError as error:
        raise UsageError(
            f"Invalid filter value '{filter_value}' - need in an integer for filter '{ctx.name}'."
        ) from error
    return int(object_value) < filter_value_int


def compare_int_greater_than(ctx: Filter, object_value: str, filter_value: str) -> bool:
    """Return True if object_value greater than filter_value"""
    try:
        filter_value_int = int(filter_value)
    except ValueError as error:
        raise UsageError(
            f"Invalid filter value '{filter_value}' - need in an integer for filter '{ctx.name}'."
        ) from error
    return int(object_value) > filter_value_int


def compare_regex(ctx: Filter, object_value: str, filter_value: str) -> bool:
    """Return True if object_value matches the regex in filter_value"""
    try:
        pattern = re.compile(filter_value)
    except re.error as error:
        raise UsageError(
            f"Invalid filter value '{filter_value}' - "
            f"need a valid regular expression for filter '{ctx.name}'."
        ) from error
    return bool(re.search(pattern, object_value))


def transform_none(ctx: Filter, value: str) -> str:  # noqa: ARG001
    """Transform: do nothing"""
    return value


def transform_lower(ctx: Filter, value: str) -> str:  # noqa: ARG001
    """Transform: to lower case"""
    return value.lower()


class DirectValuePropertyFilter(Filter):
    """Class to create a filter based on direct properties of an object.

    Missing keys AND Null values are treated as no match (no addition to the completion)
    OR match (completion addition) with the default value if default value is set.
    """

    name: str
    description: str
    property_key: str
    default_value: str | None
    compare: Callable[[Filter, str, str], bool]
    transform: Callable[[Filter, str], str]
    completion_method: Literal["values", "none", "fixed"]
    fixed_completion: list[CompletionItem]
    fixed_completion_only: bool
    title_helper: TitleHelper | None

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        description: str,
        property_key: str,
        default_value: str | None = None,
        compare: Callable[[Filter, str, str], bool] = compare_str_equality,
        transform: Callable[[Filter, str], str] = transform_none,
        completion_method: Literal["values", "none", "fixed"] = "values",
        fixed_completion: list[CompletionItem] | None = None,
        fixed_completion_only: bool = False,
        title_helper: TitleHelper | None = None,
    ):
        """Create the new filter

        name:
            The name of the filter (used as identifier)
        description:
            The description of the filter (used in filter name completion)
        property_key:
            The key of the property which is compared and completed
        default_value:
            Default value which is used in case of missing or NULL values
        compare:
            Overwrite the default string equality comparison function
        transform:
            Overwrite the default value transformation function
        completion_method:
            Overwrite the default completion value provisioning 'values'
        fixed_completion:
            A fixed list of CompletionItem objects used for value completion.
            Initialization with fixed_completion will set completion_method="fixed"
        fixed_completion_only:
            Raise an UsageError if a value is not from fixed completion.
        title_helper:
            (Optional) TitleHelper instance which will be used to provide
            resource titles as descriptions of completions candidates
        """
        self.name = name
        self.description = description
        self.property_key = property_key
        self.default_value = default_value
        self.compare = compare
        self.transform = transform
        self.completion_method = completion_method
        if fixed_completion is not None:
            self.fixed_completion = fixed_completion
            self.completion_method = "fixed"
        else:
            self.fixed_completion = []
        self.fixed_completion_only = fixed_completion_only
        self.title_helper = title_helper

    def is_filtered(self, object_: dict, value: str) -> bool:
        """Return True if the object is filtered (stays in list).

        False in case of missing key, or key is None
        True in case string(key) is value
        """
        filter_value = self.transform(self, value)
        fixed_values = [_.value for _ in self.fixed_completion]
        if self.fixed_completion_only and filter_value not in fixed_values:
            raise UsageError(
                f"'{filter_value}' is not a correct filter value for filter '{self.name}'. "
                f"Use one of {', '.join(fixed_values)}."
            )
        if self.property_key not in object_ or object_[self.property_key] is None:
            if self.default_value is None:
                return False
            return bool(self.compare(self, self.default_value, filter_value))
        object_value = self.transform(self, str(object_[self.property_key]))
        return bool(self.compare(self, object_value, filter_value))

    def complete_values(self, objects: list[dict], incomplete: str) -> list[CompletionItem]:
        """Provide completion items for filter values"""
        if self.completion_method == "none":
            return []
        if self.completion_method == "fixed":
            return self.fixed_completion
        if self.completion_method == "values":
            candidates: list = []
            for _ in objects:
                if self.property_key not in _ or _[self.property_key] is None:
                    if self.default_value is None:
                        # without actual values and no defaults, we can not complete something
                        continue
                    # without actual values but at least a default value
                    candidate = self.transform(self, str(self.default_value))
                else:
                    # a normal candidate value
                    candidate = self.transform(self, str(_[self.property_key]))
                candidates.append(candidate)
            if self.title_helper:
                self.title_helper.get(list(set(candidates)))
                candidates = [(str(_), self.title_helper.get(_)) for _ in candidates]
            return finalize_completion(
                candidates=candidates,
                incomplete=incomplete,
            )
        raise NotImplementedError(f"Completion method {self.completion_method} not implemented.")


class DirectListPropertyFilter(Filter):
    """Class to create filter based on direct list properties of an object

    False in case of missing key, key is None, or value is not in list
    True in case value is in the list
    """

    name: str
    description: str
    property_key: str
    title_helper: TitleHelper | None

    def __init__(
        self,
        name: str,
        description: str,
        property_key: str,
        title_helper: TitleHelper | None = None,
    ):
        """Create the new filter

        name:
            The name of the filter (used as identifier)
        description:
            The description of the filter (used in filter name completion)
        property_key:
            The key of the property which is compared and completed
        title_helper:
            (Optional) TitleHelper instance which will be used to provide
            resource titles as descriptions of completions candidates
        """
        self.name = name
        self.description = description
        self.property_key = property_key
        self.title_helper = title_helper

    def is_filtered(self, object_: dict, value: str) -> bool:
        """Return True if the object is filtered (stays in list)."""
        if self.property_key not in object_:
            return False  # key is not in object
        if object_[self.property_key] is None:
            return False  # key value is None
        if not isinstance(object_[self.property_key], list):
            return False  # key value is not a list
        return value in [str(_) for _ in object_[self.property_key]]

    def complete_values(self, objects: list[dict], incomplete: str) -> list[CompletionItem]:
        """Provide completion items for filter values"""
        candidates: list = []
        for object_ in objects:
            if self.property_key not in object_:
                continue  # key is not in object
            if object_[self.property_key] is None:
                continue  # key value is None
            if not isinstance(object_[self.property_key], list):
                continue  # key value is not a list
            candidates.extend([str(_) for _ in object_[self.property_key]])
        if self.title_helper:
            self.title_helper.get(list(set(candidates)))
            candidates = [(_, self.title_helper.get(_)) for _ in candidates]
        return finalize_completion(candidates=candidates, incomplete=incomplete)


class ObjectList:
    """Filterable object list"""

    name: str
    filters: dict[str, Filter]
    get_objects: Callable[[Context], list[dict]]

    def __init__(
        self,
        get_objects: Callable[[Context], list[dict]],
        filters: list[Filter | type[Filter]] | None = None,
        name: str = "list",
    ) -> None:
        self.get_objects = get_objects
        self.filters = {}
        self.name = name
        if filters:
            for _ in filters:
                self.add_filter(_)

    def add_filter(self, filter_: Filter | type[Filter]) -> None:
        """Add a filter to the object list"""
        added_filter = filter_() if isclass(filter_) else filter_
        if not isinstance(added_filter, Filter):
            raise TypeError("'filter_' parameter must be an instance OR a subclass of Filter")
        if added_filter.name in self.filters:
            raise UsageError(f"Filter {added_filter.name} already exists")
        self.filters[added_filter.name] = added_filter

    def remove_filter(self, filter_name: str) -> None:
        """Remove a filter from the object list"""
        self.filters.pop(filter_name)

    def purge_filters(self) -> None:
        """Remove all filters from the object list"""
        self.filters = {}

    def get_filter_help_text(self) -> str:
        """Get help text for the filter option."""
        return (
            f"Filter {self.name} by one of the following filter names and a "
            f"corresponding value: {', '.join(self.filters.keys())}."
        )

    def get_filter_names(self) -> list[str]:
        """Get names of all filters added to the object list"""
        return list(self.filters.keys())

    def get_filter(self, name: str) -> Filter:
        """Get filter by name"""
        try:
            return self.filters[name]
        except KeyError as error:
            filter_name_list = ", ".join(self.get_filter_names())
            raise UsageError(f"Invalid filter name - use one of {filter_name_list}") from error

    def apply_filters(
        self,
        ctx: Context,
        filter_: tuple[tuple[str, str]] | list[tuple[str, str]] | None = None,
        objects: list[dict] | None = None,
    ) -> list[dict]:
        """Filter a given object list"""
        filtered = list(self.get_objects(ctx)) if objects is None else list(objects)
        if not filter_:
            return filtered
        for filter_name, filter_value in filter_:
            the_filter = self.get_filter(filter_name)
            filtered = the_filter.filter_list(value=filter_value, objects=filtered)
        return filtered

    def complete_values(
        self,
        ctx: Context,
        param: Argument,  # noqa: ARG002
        incomplete: str,
    ) -> list[CompletionItem]:
        """Complete names and values for the filter collection"""
        previous_filter = ctx.params.get("filter_")  # tuple of (name, value) pairs or NONE
        previous_filter = previous_filter if previous_filter is not None else []
        previous_filter_names = [_[0] for _ in previous_filter]
        args = get_completion_args(incomplete)
        last_argument = args[len(args) - 1]

        if last_argument == "--filter":
            # complete filter names and descriptions
            candidates = [
                (name, self.get_filter(name).description)
                for name in self.get_filter_names()
                if name not in previous_filter_names  # do not show already used filters
            ]
            return finalize_completion(
                candidates=candidates,
                incomplete=incomplete,
            )

        ApplicationContext.set_connection_from_params(ctx.find_root().params)
        # This will filter the object list with name/values filter from the command line,
        # up to the current filter which values are completed
        objects = self.apply_filters(ctx=ctx, filter_=previous_filter)
        # provide completion for the values of the current filter
        return self.get_filter(last_argument).complete_values(
            objects=objects, incomplete=incomplete
        )
