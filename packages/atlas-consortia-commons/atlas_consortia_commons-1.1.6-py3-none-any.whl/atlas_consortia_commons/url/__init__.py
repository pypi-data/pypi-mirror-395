from typing import Any, Iterable, Mapping, Optional, Union
from urllib.parse import quote, urlencode, urlsplit, urlunsplit


def create_url(
    base: str,
    path: Optional[Union[Iterable[str], str]] = None,
    query: Optional[Mapping[str, Any]] = None,
) -> str:
    """Create a URL by joining base, optional path, and optional query parameters.

    Parameters
    ----------
    base : str
        The base URL.
    path : Optional[Union[Iterable[str], str]]
        An optional path to append to the base URL. Can be a string or an iterable of path segments.
    query : Optional[Mapping[str, Any]]
        An optional dictionary of query parameters to append to the URL.

    Returns
    -------
    str
        The constructed URL.

    Notes
    -----
    - If the base URL does not include a scheme, "https://" is prepended.
    - If `path` is a string, it is treated as a raw string to append
    - If `path` is an iterable, each segment is URL-encoded and joined with slashes.
    - If `query` is provided, it is URL-encoded and appended to the URL

    Examples
    --------
    >>> create_url("example.com", path="a/b", query={"q": "test"})
    'https://example.com/a/b?q=test'
    >>> create_url("https://example.com/base/", path=["subdir", "file.html"])
    'https://example.com/base/subdir/file.html'
    >>> create_url("example.com", query={"key": "value"})
    'https://example.com/?key=value'
    """
    parts = urlsplit(base)
    if not parts.scheme:
        base = "https://" + base
        parts = urlsplit(base)

    base_path = parts.path or ""
    base_is_root = base_path == "/"
    base_segments = [
        s for s in (base_path.strip("/").split("/") if base_path and not base_is_root else []) if s
    ]

    # Build new path
    if path is None:
        new_path = base_path or ""
    elif isinstance(path, str):
        raw = path.strip("/")
        encoded_base = "/".join(quote(seg, safe="") for seg in base_segments)
        if encoded_base:
            prefix = "/" + encoded_base
        else:
            prefix = "/" if base_is_root else ""

        if raw:
            encoded_add = quote(raw, safe="/")
            if prefix.endswith("/"):
                new_path = prefix + encoded_add
            elif prefix:
                new_path = prefix + "/" + encoded_add
            else:
                new_path = "/" + encoded_add
        else:
            new_path = prefix or ("/" if base_is_root else "")
    else:
        add_segments = [s for s in (path or []) if s is not None and s != ""]
        # allow '/' inside provided segments
        encoded = [quote(seg, safe="/") for seg in base_segments + add_segments]
        new_path = ("/" + "/".join(encoded)) if encoded else ("/" if base_is_root else "")

    if query is not None:
        q = urlencode(query, doseq=True)
    else:
        q = parts.query

    return urlunsplit((parts.scheme, parts.netloc, new_path, q, parts.fragment))
