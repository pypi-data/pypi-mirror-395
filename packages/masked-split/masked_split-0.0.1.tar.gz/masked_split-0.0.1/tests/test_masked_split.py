from masked_split.masked_split import get_delim_locations, filter_out_nodes, get_mask_locations, masked_split
import test_masked_split_data as cases

def test_delim_locations():
    for x, y, z in cases.get_delim_locations:
        assert get_delim_locations(x, y) == z

def test_filter_out_nodes():
    for x, y, z in cases.filter_out_nodes:
        assert filter_out_nodes(x, y) == z

def test_get_mask_locations():
    for x, y, z in cases.get_mask_locations:
        assert get_mask_locations(x, y) == z

def test_masked_split():
    for s, m, d, i, p, debug, z in cases.masked_split:
        assert masked_split(s, m, d, i, p, debug) == z
