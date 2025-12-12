import pytest
from atlas_consortia_commons import url


@pytest.mark.parametrize(
    "base,path,params,expected",
    [
        ("https://example.com", None, None, "https://example.com"),
        ("example.com", None, None, "https://example.com"),
        ("https://example.com", ["a", "b"], None, "https://example.com/a/b"),
        ("https://example.com", "a/b", None, "https://example.com/a/b"),
        ("https://example.com/base", "c", None, "https://example.com/base/c"),
        ("https://example.com/", None, {"q": "x"}, "https://example.com/?q=x"),
        ("https://example.com/", "a/b", {"q": "x"}, "https://example.com/a/b?q=x"),
        ("https://example.com/", ["a", "b"], {"q": "x"}, "https://example.com/a/b?q=x"),
        ("https://example.com/?a=1", None, None, "https://example.com/?a=1"),
    ],
)
def test_create_url_parametrized(base, path, params, expected):
    assert url.create_url(base, path, params) == expected
