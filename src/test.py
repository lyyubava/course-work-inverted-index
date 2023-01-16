from inverted_index_parallel_another_try import InvertedIndex as ii_parallel
from inverted_index_serial import InvertedIndex as ii_serial

from storage import Storage

storage = Storage(16, "test/neg", "test/pos", "train/neg", "train/pos", "train/unsup")

inverted_index_serial = ii_serial(storage)
inverted_index_parallel = ii_parallel(storage)

inverted_index_serial.create_index_serial()
inverted_index_parallel.create_index_parallel(5)


def test_parallel_and_serial_executions():
    assert len(inverted_index_serial.search("Leonardo")) == len(inverted_index_parallel.search("Leonardo"))

def test_parallel_and_serial_executions_compare_word_entry():
    result_serial = inverted_index_serial.search("movie")
    result_parallel = inverted_index_parallel.search("movie")
    for entry in result_serial:
        assert entry in result_parallel


def test_parallel_and_serial_executions_compare_len_indexes():
    assert len(inverted_index_parallel.index) == len(inverted_index_serial.index)



