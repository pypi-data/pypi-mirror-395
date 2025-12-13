import os
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Literal, Sequence, TypeAlias, cast

import polars as pl
from typing_extensions import TypeAliasType

if TYPE_CHECKING:
    Hierarchy: TypeAlias = "list[str] | Mapping[str, Hierarchy]"
else:
    Hierarchy = TypeAliasType("Hierarchy", list[str] | Mapping[str, "Hierarchy"])


def check_unique_hierarchy(v: Mapping[str, Hierarchy]) -> Mapping[str, Hierarchy]:
    """Check that all hierarchies have unique codes.

    Parameters
    ----------
    v : Mapping[str, Hierarchy]
        The mapping of hierarchy names to hierarchies.

    Returns
    -------
    Mapping[str, Hierarchy]
        The validated mapping.

    Raises
    ------
    ValueError
        If any hierarchy contains duplicate codes.
    """
    errors = []
    for hierarchy_name, hierarchy in v.items():
        flat_hierarchy = flatten(hierarchy)
        dupes = [item for item, count in Counter(flat_hierarchy).items() if count > 1]

        if dupes:
            errors.append(
                f"There are duplicate elements in hierarchy {hierarchy_name}: "
                f"{', '.join(dupes)}"
            )
    if errors:
        raise ValueError(os.linesep.join(errors))
    else:
        return v


def check_all_codes_have_labels(
    hierarchies: Mapping[str, Hierarchy],
    labels: Mapping[str, Mapping[str, str]],
) -> list[str]:
    """Check that all hierarchy codes have corresponding labels.

    Parameters
    ----------
    hierarchies : Mapping[str, Hierarchy]
        The mapping of hierarchy names to hierarchies.
    labels : Mapping[str, Mapping[str, str]]
        The mapping of hierarchy names to label mappings.

    Returns
    -------
    list[str]
        List of error messages for any missing or extra labels.
    """
    errors = []

    # check that keys align
    if missing_labels := set(hierarchies) - set(labels):
        errors.append(
            f"The following hierarchies do not have labels: {', '.join(missing_labels)}"
        )
    if extra_labels := set(labels) - set(hierarchies):
        errors.append(
            f"The following label keys do not have hierarchies: {', '.join(extra_labels)}"
        )

    missing_codes = defaultdict(list)
    extra_codes = defaultdict(list)
    for hierarchy_name, hierarchy in hierarchies.items():
        if hierarchy_name not in labels:
            continue
        all_codes = set(flatten(hierarchy))
        all_label_codes = set(labels[hierarchy_name].keys())
        missing_codes[hierarchy_name].extend(list(all_codes - all_label_codes))
        extra_codes[hierarchy_name].extend(list(all_label_codes - all_codes))

    for hierarchy_name, codes in missing_codes.items():
        if codes:
            missing_str = ", ".join(codes)
            errors.append(
                f"Hierarchies {hierarchy_name} has missing mappings: {missing_str}",
            )

    for hierarchy_name, codes in extra_codes.items():
        if codes:
            xtr_str = ", ".join(codes)
            errors.append(
                f"Hierarchies {hierarchy_name} has superfluous mappings: {xtr_str}",
            )

    return errors


def flatten(hierarchy: Hierarchy, only_leaves: bool = False) -> list[str]:
    """Flatten a hierarchical structure into a list of codes.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchical structure to flatten.
    only_leaves : bool, default=False
        If True, only include leaf nodes (codes at the deepest level).

    Returns
    -------
    list[str]
        A flat list of all codes in the hierarchy.
    """
    if isinstance(hierarchy, list):
        return hierarchy
    else:
        items = []
        for k, v in hierarchy.items():
            if not only_leaves:
                items.append(k)
            items.extend(flatten(v, only_leaves=only_leaves))
        return items


def validate_hierarchy_schema(
    available_schemas: Iterable[str],
    hierarchy_schema: str,
) -> None:
    """Validate that a hierarchy schema exists in the available schemas.

    Parameters
    ----------
    available_schemas : Iterable[str]
        The list of available schema names.
    hierarchy_schema : str
        The schema name to validate.

    Raises
    ------
    ValueError
        If the schema does not exist in the available schemas.
    """
    if hierarchy_schema not in available_schemas:
        raise ValueError(
            f"Schema {hierarchy_schema} does not exist. "
            f"Only {', '.join(available_schemas)} exist. "
        )


def map_hierarchy(
    hierarchy: Hierarchy,
    fn: Callable[[str], str],
) -> Hierarchy:
    """Apply a function to all codes in a hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchical structure to map over.
    fn : Callable[[str], str]
        The function to apply to each code.

    Returns
    -------
    Hierarchy
        A new hierarchy with the function applied to all codes.
    """
    if isinstance(hierarchy, list):
        return [fn(e) for e in hierarchy]
    else:
        return {fn(k): map_hierarchy(v, fn) for k, v in hierarchy.items()}


def filter_leaves(
    hierarchy: Hierarchy,
    fn: Callable[[str], bool],
) -> Hierarchy:
    """Filter leaves in a hierarchy based on a predicate function.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchical structure to filter.
    fn : Callable[[str], bool]
        The predicate function to apply to each leaf code.

    Returns
    -------
    Hierarchy
        A new hierarchy with only the leaves that pass the predicate.
    """
    if isinstance(hierarchy, list):
        return [e for e in hierarchy if fn(e)]
    else:
        return {
            k: survivors
            for k, v in hierarchy.items()
            if (survivors := filter_leaves(v, fn))
        }


def find_in_hierarchy(hierarchy: Hierarchy, needle: str) -> Hierarchy | None:
    """Find a needle in a hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to search in.
    needle : str
        The needle to search for.

    Returns
    -------
    Hierarchy | None
        The sub-hierarchy that contains the needle, or None if the needle is not found.
    """
    if isinstance(hierarchy, list):
        if needle in hierarchy:
            return [needle]
    else:
        for k, v in hierarchy.items():
            if k == needle:
                return {k: v}
            else:
                if match := find_in_hierarchy(v, needle):
                    return match
    return None


def find_in_hierarchy_depth(
    hierarchy: Hierarchy, needle: str, *, depth: int = 0
) -> int:
    """Find the depth of a needle in a hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to search in.
    needle : str
        The needle to search for.
    depth : int, default=0
        The current depth in the hierarchy.

    Returns
    -------
    int
        The depth of the hierarchy that contains the needle, or -1 if the needle is not
        found.
    """
    if isinstance(hierarchy, list):
        if needle in hierarchy:
            return depth + 1
    else:
        for k, v in hierarchy.items():
            if k == needle:
                return depth + 1
            else:
                if (match := find_in_hierarchy_depth(v, needle, depth=depth + 1)) > -1:
                    return match
    return -1


def trim_to_depth(hierarchy: Hierarchy, depth: int) -> Hierarchy:
    """Trim a hierarchy to a given depth.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to trim.
    depth : int
        The depth to trim the hierarchy to.

    Returns
    -------
    Hierarchy
        The trimmed hierarchy.

    Raises
    ------
    AssertionError
        If the depth is less than 0.
    """
    if depth < 0:
        raise AssertionError(f"Depth must be >= 0., {depth}")
    if depth == 1:
        return list(hierarchy.keys()) if isinstance(hierarchy, dict) else hierarchy
    elif isinstance(hierarchy, list):
        return hierarchy
    else:
        return {k: trim_to_depth(v, depth - 1) for k, v in hierarchy.items()}


def filter_labels_to_hierarchy(
    hierarchy: Hierarchy,
    labels: Mapping[str, str],
) -> Mapping[str, str]:
    """Filter the labels to only include those present in the hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to filter the labels for.
    labels : Mapping[str, str]
        The labels to filter.

    Returns
    -------
    Mapping[str, str]
        The filtered labels.
    """
    return {k: v for k, v in labels.items() if k in flatten(hierarchy)}


def get_depth(hierarchy: Hierarchy) -> int:
    """Get the depth of a hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to get the depth of.

    Returns
    -------
    int
        The depth of the hierarchy.
    """
    if isinstance(hierarchy, list):
        return 1
    else:
        return max(get_depth(v) for v in hierarchy.values()) + 1


def hierarchy_to_df(
    hierarchy: Hierarchy, hierarchies_labels: Mapping[str, str]
) -> pl.DataFrame:
    """Convert a hierarchy to a DataFrame.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to convert to a DataFrame.
    hierarchies_labels : Mapping[str, str]
        The labels to use for the hierarchy.

    Returns
    -------
    pl.DataFrame
        The DataFrame representation of the hierarchy. The columns are:
        - level: The level of the hierarchy.
        - code: The code of the hierarchy.
        - label: The label of the hierarchy.
        - parent_code: The parent code of the hierarchy.
    """
    rows = []

    def recurse(node: Hierarchy, level: int, parent_code: str | None) -> None:
        if isinstance(node, list):
            # If we hit a list, each element is a leaf code
            for leaf in node:
                rows.append({"code": leaf, "level": level, "parent_code": parent_code})
        else:
            for key, subtree in node.items():
                # Add the current key (an intermediate node)
                rows.append({"code": key, "level": level, "parent_code": parent_code})
                # Recurse into its value
                recurse(subtree, level + 1, key)

    recurse(hierarchy, level=0, parent_code=None)

    return (
        pl.DataFrame(rows)
        .select(
            pl.col("level").cast(pl.Int32),
            "code",
            pl.col("code").replace_strict(hierarchies_labels).alias("label"),
            pl.col("parent_code").cast(pl.String),
        )
        .sort("level", maintain_order=True)
    )


def hierarchy_df_to_wide(
    hierarchy: Hierarchy, hierarchies_labels: Mapping[str, str]
) -> pl.DataFrame:
    """Convert a hierarchy to a wide DataFrame.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to convert to a wide DataFrame.
    hierarchies_labels : Mapping[str, str]
        The labels to use for the hierarchy.

    Returns
    -------
    pl.DataFrame
        The wide DataFrame representation of the hierarchy. The columns are:
        - level_1: The code of the root level.
        - level_1_label: The label of the root level.
        - level_2: The code of the second level.
        - level_2_label: The label of the second level.
        - ...
        - level_n: The code of the n-th level.
        - level_n_label: The label of the n-th level.
    """
    df = hierarchy_to_df(hierarchy, hierarchies_labels)

    df_wide = df.filter(pl.col("level") == 0).select(
        pl.col("code").alias("level_1"), pl.col("label").alias("level_1_label")
    )
    for lvl in range(cast(int, df.get_column("level").max())):
        df_wide = (
            df_wide.join(
                df.filter(pl.col("level") == lvl + 1),
                left_on=f"level_{lvl + 1}",
                right_on="parent_code",
                how="left",
            )
            .drop("level")
            .rename({"code": f"level_{lvl + 2}", "label": f"level_{lvl + 2}_label"})
        )
    return df_wide


def _filter_leaves_by_labels_or_codes(  # noqa: C901
    hierarchy: Hierarchy,
    include: Sequence[str] | Literal["All"],
    exclude: Sequence[str],
    labels: Mapping[str, str],
) -> list[str]:
    leaf_include = []
    if isinstance(include, str) and include == "All":
        leaf_include = flatten(hierarchy, only_leaves=True)
    else:
        for i in include:
            v = find_in_hierarchy(hierarchy, i)
            if v is None:
                # must be a label then
                codes = [k for k, v in labels.items() if v == i]
                if not codes:
                    raise AssertionError(
                        f"{i} is unknown which at this stage should've been verified"
                    )

                # find the highest level in the hierarchy for possible codes
                depths = {
                    find_in_hierarchy_depth(hierarchy, code): code for code in codes
                }
                if len(depths) != len(codes):
                    raise AssertionError(
                        f"Include {include}: {codes} - {depths}"
                        "illegal, all codes must be represented"
                    )
                v = find_in_hierarchy(
                    hierarchy,
                    depths[min(depths.keys())],  # type: ignore
                )

            if isinstance(v, list):
                leaf_include.extend(v)
            else:
                if not isinstance(v, Mapping):
                    raise AssertionError()
                leaf_include.extend(
                    flatten(v, only_leaves=True),
                )

    leaf_exclude = []
    for e in exclude:
        v = find_in_hierarchy(hierarchy, e)
        if v is None:
            # must be a label then
            codes = [k for k, v in labels.items() if v == e]
            if not codes:
                raise AssertionError(
                    f"{e} is unknown which at this stage should've been verified"
                )

            # find the lowest level in the hierarchy for possible codes
            depths = {find_in_hierarchy_depth(hierarchy, code): code for code in codes}
            v = find_in_hierarchy(
                hierarchy,
                depths[max(depths.keys())],  # type: ignore
            )

        if isinstance(v, list):
            leaf_exclude.extend(v)
        else:
            if not isinstance(v, Mapping):
                raise AssertionError()
            leaf_exclude.extend(flatten(v, only_leaves=True))

    return list(set(leaf_include) - set(leaf_exclude))


def effective_hierarchy(
    hierarchy: Hierarchy,
    include: Sequence[str] | Literal["All"],
    exclude: Sequence[str],
    labels: Mapping[str, str],
) -> Hierarchy:
    """Return the hierarchy based on the include and exclude filters.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to filter the leaves for.
    include : Sequence[str] | Literal["All"]
        The include to filter the leaves for.
    exclude : Sequence[str]
        The exclude to filter the leaves for. Applied after the include.
    labels : Mapping[str, str]
        The label of each code in the hierarchy.

    Returns
    -------
    Hierarchy
        The hierarchy that is included and not excluded.
    """
    effective_codes = _filter_leaves_by_labels_or_codes(
        hierarchy, include, exclude, labels
    )
    return filter_leaves(hierarchy, lambda x: x in effective_codes)


def effective_leaves(
    hierarchy: Hierarchy,
    include: Sequence[str] | Literal["All"],
    exclude: Sequence[str],
    labels: Mapping[str, str],
    depth: int | None = None,
) -> list[str]:
    """Return the leaves based on the include and exclude filters.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to filter the leaves for.
    include : Sequence[str] | Literal["All"]
        The include to filter the leaves for.
    exclude : Sequence[str]
        The exclude to filter the leaves for. Applied after the include.
    labels : Mapping[str, str]
        The label of each code in the hierarchy.
    depth : int | None, default=None
        The depth to trim the hierarchy to. If None, the hierarchy is not trimmed. If
        not, only leaves at the given depth are returned.

    Returns
    -------
    list[str]
        The leaves of the hierarchy that are included and not excluded.
    """
    hierarchy = effective_hierarchy(hierarchy, include, exclude, labels)
    if depth is not None:
        hierarchy = trim_to_depth(hierarchy, depth)
    return flatten(hierarchy, only_leaves=True)


def _maybe_get(
    mapping: Mapping[str, str], key: str, *, prefix: str | None = None
) -> str:
    if prefix is None:
        prefix_out = ""
    else:
        prefix_out = prefix if key.startswith(prefix) else ""
    if prefix_out:
        key = key[1:]  # strip the prefix
    return prefix_out + mapping.get(key, key)


def codes_to_labels(
    hierarchy: Hierarchy,
    labels: Mapping[str, str],
    *,
    prefix: str | None = None,
) -> Hierarchy:
    """Return the hierarchy with all codes replaced by their labels.

    If a code is not in the labels, it is left unchanged.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to replace the codes with labels for.
    labels : Mapping[str, str]
        The label of each code in the hierarchy.
    prefix : str | None, default=None
        The prefix that is used for the label, that has to survive the replacement.

    Returns
    -------
    Hierarchy
        The hierarchy with all codes replaced by their labels.
    """
    return map_hierarchy(hierarchy, lambda x: _maybe_get(labels, x, prefix=prefix))


def labels_to_codes(
    hierarchy: Hierarchy,
    labels: Mapping[str, str],
    *,
    prefix: str | None = None,
) -> Hierarchy:
    """Return the hierarchy with all labels replaced by their codes.

    If a label is not in the labels, it is left unchanged.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to replace the labels with codes for.
    labels : Mapping[str, str]
        The label of each code in the hierarchy.
    prefix : str | None, default=None
        The prefix that is used for the label, that has to survive the replacement.

    Returns
    -------
    Hierarchy
        The hierarchy with all labels replaced by their codes.
    """
    rev_labels = {v: k for k, v in labels.items()}  # reverse the labels
    return map_hierarchy(hierarchy, lambda x: _maybe_get(rev_labels, x, prefix=prefix))


def process_excludes(
    hierarchy: Hierarchy,
    reference_hierarchy: Hierarchy,
    subset: str | None = None,
) -> Hierarchy:
    """Process the excludes (prefixed with ~) for a hierarchy.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to process the excludes for.
    reference_hierarchy : Hierarchy
        The reference hierarchy to use for the excludes.
    subset : str | None, default=None
        The subset to process the excludes for. If None, the entire hierarchy is used.

    Returns
    -------
    Hierarchy
        The hierarchy with the excludes processed and replaced by their complement.

    Raises
    ------
    ValueError
        If the subset has an invalid format or is not found in the reference hierarchy.
    """
    if subset is None:
        subhierarchy = reference_hierarchy
    else:
        if subset.startswith("~"):
            raise ValueError(f"~ prefix only allowed on leaves, {subset} is not a leaf")
        maybe_subhierarchy = find_in_hierarchy(reference_hierarchy, subset)
        if maybe_subhierarchy is None:
            raise ValueError(f"subset {subset} not found in reference hierarchy")
        else:
            subhierarchy = maybe_subhierarchy

    if isinstance(hierarchy, list):
        exclude = [leaf[1:] for leaf in hierarchy if leaf.startswith("~")]
        include = [leaf for leaf in hierarchy if not leaf.startswith("~")] or "All"
        return flatten(
            effective_hierarchy(subhierarchy, include, exclude, {}), only_leaves=True
        )
    else:
        return {
            k: process_excludes(v, reference_hierarchy, k) for k, v in hierarchy.items()
        }


def validate_hierarchy_filters(
    hierarchy: Hierarchy,
    include: Sequence[str] | Literal["All"],
    exclude: Sequence[str],
    labels: Mapping[str, str],
) -> None:
    """Validate the hierarchy filters.

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to validate the filters for.
    include : Sequence[str] | Literal["All"]
        The include to validate.
    exclude : Sequence[str]
        The exclude to validate.
    labels : Mapping[str, str]
        The labels to validate.

    Raises
    ------
    ValueError
        If the include or exclude are unknown.
    """
    flat_hierarchy = flatten(hierarchy)
    label_values = set(labels.values())

    unknown = []
    if include != "All":
        unknown.extend(
            [i for i in include if i not in flat_hierarchy and i not in label_values],
        )

    unknown.extend(
        [e for e in exclude if e not in flat_hierarchy and e not in label_values],
    )

    if len(unknown) > 0:
        raise ValueError(f"there are unknown items: {', '.join(unknown)}")

    effective_includes = _filter_leaves_by_labels_or_codes(
        hierarchy, include, exclude, labels
    )
    if len(effective_includes) == 0:
        raise ValueError(
            "the include and exclude statements lead to an empty set.",
        )


def assert_no_empty_branches(hierarchy: Hierarchy, branch_name: str = "root") -> None:
    """Assert that the hierarchy is not empty or has empty branches.

    If at any point in the tree (including at the root) a branch is either an empty list
    of dict, the hierarchy has empty branches. For example, the following hierarchies
    all have empty branches:
    - []
    - {}
    - {"a": {}, "b": ["c"]}
    - {"a": {"b": []}}

    Parameters
    ----------
    hierarchy : Hierarchy
        The hierarchy to validate.
    branch_name : str, default="root"
        The name of the branch to validate.

    Raises
    ------
    ValueError
        If the hierarchy is empty.
    """
    if not hierarchy:
        raise ValueError(f"Hierarchy at branch {branch_name} cannot be empty")
    if isinstance(hierarchy, dict):
        for k, v in hierarchy.items():
            assert_no_empty_branches(v, k)
