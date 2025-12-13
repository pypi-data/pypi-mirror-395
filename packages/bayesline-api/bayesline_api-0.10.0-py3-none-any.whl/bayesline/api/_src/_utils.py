import inspect
import re
import sys
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=type)

# ---------------- helpers ----------------


def _short_type(ann: Any) -> str:
    if ann is None:
        return "None"
    s = getattr(ann, "__name__", None) or str(ann)
    s = s.replace("typing.", "")
    return re.sub(r"(?<!\w)[\w\.]*\.", "", s)  # strip module prefixes


def _param_names(func: Callable[..., Any]) -> list[str]:
    sig = inspect.signature(func)
    return [p.name for p in sig.parameters.values() if p.name not in {"self", "cls"}]


def _find_numpy_block(
    doc: str, title: str
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    pat = re.compile(rf"(^\s*{re.escape(title)}\s*\n^\s*-+\s*\n)", re.MULTILINE)
    m = pat.search(doc)
    if not m:
        return None
    body_start = m.end(1)
    body_m = re.compile(r"(?=^\s*\n^\S)|\Z", re.MULTILINE).search(doc, body_start)
    body_end = body_m.start() if body_m else len(doc)
    return (m.span(1), (body_start, body_end))


def _split_type_and_tail(r: str) -> tuple[str, str]:
    # split 'TYPE[, tail...]' at first comma not inside (), [], {}.
    depth = 0
    for i, ch in enumerate(r):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            return r[:i].strip(), r[i:]  # keep comma in tail
    return r.strip(), ""


def _replace_idents_to_async(type_text: str, dst_ann_str: str) -> str:
    # replace only identifiers X with AsyncX if AsyncX appears in dst_ann_str.
    # - preserves generics/Literal contents and anything not explicitly mapped.
    # - only replaces CamelCase-like identifiers (starts with uppercase letter).

    def repl(m: re.Match) -> str:
        ident = m.group(0)
        if not ident[0].isupper():
            return ident
        cand = f"Async{ident}"
        return cand if re.search(rf"\b{re.escape(cand)}\b", dst_ann_str) else ident

    # Replace dotted names token-by-token (only the trailing identifier will match)
    return re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", repl, type_text)


def _rewrite_params_types_numpy(body: str, dst_ann_str_by_name: dict[str, str]) -> str:
    out = []
    for line in body.splitlines():
        m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*:\s*(.+)$", line)
        if not m:
            out.append(line)
            continue
        indent, name, right = m.groups()
        if name not in dst_ann_str_by_name:
            out.append(line)
            continue
        type_token, tail = _split_type_and_tail(right.lstrip())
        # Only tweak identifiers inside the existing type token
        new_type = _replace_idents_to_async(type_token, dst_ann_str_by_name[name])
        out.append(f"{indent}{name} : {new_type}{tail}")
    return "\n".join(out)


def _rewrite_returns_type_numpy(body: str, dst_ret_str: str) -> str:
    lines = body.splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if s and not set(s) <= {"-"}:
            indent = line[: len(line) - len(line.lstrip())]
            keep_colon = ":" if s.endswith(":") else ""
            new_type = _replace_idents_to_async(s.rstrip(":"), dst_ret_str)
            lines[i] = f"{indent}{new_type}{keep_colon}"
            break
    return "\n".join(lines)


def _adapt_doc_numpy(
    src_doc: str, src_func: Callable[..., Any], dst_func: Callable[..., Any]
) -> str:
    new_doc = src_doc

    # If param names match, adapt only the identifiers inside the existing type text
    if _param_names(src_func) == _param_names(dst_func):
        dst_sig = inspect.signature(dst_func)
        dst_ann_str_by_name = {
            n: _short_type(dst_func.__annotations__.get(n, None))
            for n in dst_sig.parameters
            if n not in {"self", "cls"}
        }
        blk = _find_numpy_block(new_doc, "Parameters")
        if blk:
            (_, _), (bs, be) = blk
            new_doc = (
                new_doc[:bs]
                + _rewrite_params_types_numpy(new_doc[bs:be], dst_ann_str_by_name)
                + new_doc[be:]
            )

    # Returns: conservatively replace identifiers only
    dst_ret_str = _short_type(dst_func.__annotations__.get("return"))
    blk = _find_numpy_block(new_doc, "Returns")
    if blk and dst_ret_str:
        (_, _), (bs, be) = blk
        new_doc = (
            new_doc[:bs]
            + _rewrite_returns_type_numpy(new_doc[bs:be], dst_ret_str)
            + new_doc[be:]
        )

    return new_doc


# ---------------- main decorator ----------------


def docstrings_from_sync(cls: T) -> T:  # noqa: C901
    """For an async twin class (e.g., AsyncFoo), copy/adjust NumPy docstrings from Foo.

    - Copy class docstring if AsyncFoo lacks one.
    - For each method *and property* in AsyncFoo:
        * If it lacks a docstring, copy Foo counterpart's docstring.
        * Adapt only identifier tokens (X -> AsyncX) inside 'Parameters'/'Returns' types.
          Do not expand generics or Literal values.
        * For properties, set docstring on both the property object and its fget.

    Parameters
    ----------
    cls : T
        The async twin class to copy docstrings into.

    Returns
    -------
    T
        The async twin class with copied docstrings.
    """
    name = cls.__name__
    sync_name = name[5:] if name.startswith("Async") else name.replace("Async", "", 1)
    mod = sys.modules.get(cls.__module__)
    sync_cls = getattr(mod, sync_name, None) if mod else None
    if not isinstance(sync_cls, type):
        return cls

    # Class docstring
    if not cls.__doc__ and getattr(sync_cls, "__doc__", None):
        cls.__doc__ = sync_cls.__doc__

    for attr, dst in list(cls.__dict__.items()):
        if attr.startswith("_"):
            continue

        # properties
        if isinstance(dst, property):
            src_prop = getattr(sync_cls, attr, None)
            if not isinstance(src_prop, property):
                continue
            src_doc = src_prop.__doc__
            if not src_doc:
                continue
            dst_fget = dst.fget
            src_fget = src_prop.fget
            if not (dst_fget and src_fget):
                continue
            new_doc = _adapt_doc_numpy(src_doc, src_fget, dst_fget)
            dst_fget.__doc__ = new_doc
            setattr(cls, attr, property(dst.fget, dst.fset, dst.fdel, doc=new_doc))
            continue

        # functions (sync or async)
        if inspect.isfunction(dst):
            src = getattr(sync_cls, attr, None)
            if not (src and inspect.isfunction(src)):
                continue
            if getattr(dst, "__doc__", None):
                continue
            src_doc = getattr(src, "__doc__", None)
            if not src_doc:
                continue
            new_doc = _adapt_doc_numpy(src_doc, src, dst)
            try:
                dst.__doc__ = new_doc
            except Exception:
                dst.__func__.__doc__ = new_doc  # type: ignore[attr-defined]

    return cls
