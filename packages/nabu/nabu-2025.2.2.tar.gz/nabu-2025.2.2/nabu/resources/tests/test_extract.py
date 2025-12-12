from nabu.utils import list_match_queries


def test_list_match_queries():

    # entry0000 .... entry0099
    avail = ["entry%04d" % i for i in range(100)]
    assert list_match_queries(avail, "entry0000") == ["entry0000"]
    assert list_match_queries(avail, ["entry0001"]) == ["entry0001"]
    assert list_match_queries(avail, ["entry000?"]) == ["entry%04d" % i for i in range(10)]
    assert list_match_queries(avail, ["entry*"]) == avail
