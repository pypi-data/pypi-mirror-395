from good_common.types.web import URL


def test_double_question_mark_key_is_normalized_and_tracking_removed():
    # Raw URL with double question marks produces a key that begins with '?' (e.g., '?intcmp')
    raw = (
        "https://foxnews.com/politics/us-turns-finland-close-arctic-icebreaker-gap-"
        "russia-china-expand-polar-presence??intcmp=tw_pols"
    )
    u = URL(raw)
    c = u.canonical
    # Ensure tracking parameter is not present in canonicalized query
    assert "intcmp" not in c.query
    # The canonical URL should not contain the encoded tuple artifacts like %28%27tw_pols%27%2C%29
    assert "%28%27tw_pols%27%2C%29" not in str(c)


def test_update_preserves_multi_value_query_without_tuple_stringification():
    # Start with a URL that has two values for the same key
    u = URL("https://example.com/path?a=1&a=2")
    # Force an update that rebuilds the URL using query derived from dict-of-tuples
    v = u.update(path="/new")
    # Both a=1 and a=2 should remain present, not stringified as a tuple
    s = str(v)
    assert "a=1" in s and "a=2" in s
    assert "%28%27" not in s  # no tuple stringification artifacts
