#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Matching of topic selectors. """
from __future__ import annotations

import re
from typing import Iterable, Optional, Set, Union, Hashable

from typing_extensions import Protocol, runtime_checkable

from diffusion.internal.exceptions import DiffusionError


@runtime_checkable
class Selector(Protocol, Hashable):
    """ Generic protocol for all selectors. """

    def match(self, topic_path: str) -> bool:
        """Compares a topic path against the selector.

        Args:
            topic_path: The topic path to match against the selector.

        Returns:
            `True` if the path matches the selector; `False` otherwise.
        """
        ...  # pragma: no cover

    @property
    def raw(self) -> str:
        """ The original, unoptimised value of the selector. """
        ...  # pragma: no cover


class TopicSelectorError(DiffusionError):
    """ Error related to selector matching. """


def get_selector(selector: str) -> Selector:
    """ Instantiate a selector based on the given textual value. """
    selector_class = {
        SplitPathPatternSelector.PATH_PREFIX: SplitPathPatternSelector,
        FullPathPatternSelector.PATH_PREFIX: FullPathPatternSelector,
        SelectorSet.PATH_PREFIX: SelectorSet,
    }.get(selector[0], PathSelector)
    return selector_class(selector)


class PathSelector(Selector):
    """Basic topic selector, matching the topic path exactly.

    Args:
        selector: The topic selector text.
    """

    PATH_PREFIX = ">"
    SEPARATOR = "/"
    ILLEGAL_PREFIXES = "$&<"

    def __init__(self, selector: str):
        self._raw = selector
        self._selector = self._prepare(selector)

    def match(self, topic_path: str) -> bool:
        """Compares a topic path against the selector.

        Args:
            topic_path: The topic path to match against the selector.

        Returns:
            `True` if the path matches the selector; `False` otherwise.
        """
        return self._selector == topic_path

    def _prepare(self, selector: str) -> str:
        if any(map(selector.startswith, self.ILLEGAL_PREFIXES)):
            raise TopicSelectorError
        if selector.startswith(self.PATH_PREFIX):
            selector = selector[1:]
        return selector.strip(self.SEPARATOR)

    @property
    def raw(self) -> str:
        """ The original, unoptimised value of the selector. """
        return self._raw

    def __str__(self) -> str:
        return self.raw

    def __repr__(self) -> str:
        return f"<{type(self).__name__} selector={self.raw}>"

    def __hash__(self) -> int:
        return hash(self.raw)

    def __eq__(self, other) -> bool:
        return str(other) == self.raw


class PatternSelector(PathSelector):
    """ Common functionality of pattern selectors. """

    EXCLUSIVE_DESCENDANT_QUALIFIER = "/"
    INCLUSIVE_DESCENDANT_QUALIFIER = "//"

    def __init__(self, selector: str):
        if not selector.startswith(self.PATH_PREFIX):
            raise TopicSelectorError(f"{type(self)} must begin with '{self.PATH_PREFIX}")
        self._match_descendants: Optional[bool] = None
        super().__init__(selector)


class FullPathPatternSelector(PatternSelector):
    """Selector containing a regular expression matching the entire path.

    A full-path pattern topic selector returns topics for which the
    regular expression matches the full topic path.

    Args:
        selector: The topic selector text.
    """

    PATH_PREFIX = "*"

    def __init__(self, selector: str):
        super().__init__(selector)
        self._pattern = re.compile(self._selector)

    def _prepare(self, selector: str) -> str:
        if selector.endswith(self.INCLUSIVE_DESCENDANT_QUALIFIER):
            selector = f"{selector[:-len(self.INCLUSIVE_DESCENDANT_QUALIFIER)]}/?.*"
        elif selector.endswith(self.EXCLUSIVE_DESCENDANT_QUALIFIER):
            selector = f"{selector[:-len(self.EXCLUSIVE_DESCENDANT_QUALIFIER)]}/.*"
        return super()._prepare(selector)

    def match(self, topic_path: str) -> bool:
        """Compares a topic path against the selector.

        Args:
            topic_path: The topic path to match against the selector.

        Returns:
            `True` if the path matches the selector; `False` otherwise.
        """
        return self._pattern.fullmatch(topic_path) is not None


class SplitPathPatternSelector(PatternSelector):
    """Selector containing split-path regular expression pattern.

    A split-path pattern expression contains a list of regular
    expressions separated by the / character. Each regular expression
    describes a part of the topic path. The selector returns topics for
    which each regular expression matches the part of the topic path at
    the corresponding level.

    Args:
        selector: The topic selector text.
    """

    PATH_PREFIX = "?"

    def __init__(self, selector: str):
        self._match_descendants_inclusive = None
        if selector.endswith(self.INCLUSIVE_DESCENDANT_QUALIFIER):
            self._match_descendants_inclusive = True
        elif selector.endswith(self.EXCLUSIVE_DESCENDANT_QUALIFIER):
            self._match_descendants_inclusive = False
        super().__init__(selector)
        self._patterns = [re.compile(sel) for sel in self._selector.split(self.SEPARATOR)]

    def match(self, topic_path: str) -> bool:
        """Compares a topic path against the selector.

        Args:
            topic_path: The topic path to match against the selector.

        Returns:
            `True` if the path matches the selector; `False` otherwise.
        """
        path_parts = topic_path.split(self.SEPARATOR)
        parts_count = len(path_parts)
        patterns_count = len(self._patterns)
        return (
            not any(
                (
                    self._match_descendants_inclusive is True and parts_count < patterns_count,
                    self._match_descendants_inclusive is False
                    and parts_count <= patterns_count,
                    self._match_descendants_inclusive is None and parts_count != patterns_count,
                )
            )
            and all(
                pattern.fullmatch(part) for pattern, part in zip(self._patterns, path_parts)
            )
        )


class SelectorSet(Set[Selector], Selector):
    """A set of multiple path or pattern selectors.

    A selector set returns topics that match any of the selectors. Its
    textual form is a list of selectors separated by the separator `////`.

    Args:
        selectors: Either the full list of selectors (separated by `////`)
                   or an iterable of individual selectors.
    """

    PATH_PREFIX = "#"
    PATHS_SEPARATOR = "////"

    def __init__(self, selectors: Union[str, Iterable[str]]):
        if isinstance(selectors, str):
            if not selectors.startswith(self.PATH_PREFIX):
                raise TopicSelectorError(
                    f"{type(self).__name__} must begin with '{self.PATH_PREFIX}"
                )
            selectors = set(selectors[1:].split(self.PATHS_SEPARATOR))
        super().__init__(map(get_selector, selectors))
        self._raw = f"{self.PATH_PREFIX}{self.PATHS_SEPARATOR.join(sorted(map(str, self)))}"

    def match(self, topic_path: str) -> bool:
        """Compares a topic path against the selector.

        Args:
            topic_path: The topic path to match against the selector.

        Returns:
            `True` if the path matches the selector; `False` otherwise.
        """
        return any(sel.match(topic_path) for sel in self)

    @classmethod
    def any_of(cls, *args: str) -> SelectorSet:
        """ Helper method that accepts selectors as individual arguments to create a set. """
        return SelectorSet(args)

    @property
    def raw(self) -> str:
        """ The original, unoptimised value of the selector. """
        return self._raw

    def __str__(self):
        return self.raw

    def __repr__(self):
        return f"""SelectorSet({{'{"', '".join(sorted(map(str, self)))}'}})"""

    def __hash__(self):
        return hash(self.raw)
