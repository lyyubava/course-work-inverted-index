from inverted_index_parallel_another_try import InvertedIndex as ii_parallel
from inverted_index_serial import InvertedIndex as ii_serial
from storage import Storage

storage = Storage(16, "test/neg", "test/pos", "train/neg", "train/pos", "train/unsup")

from time import time

inverted_index_serial = ii_serial(storage)
inverted_index_parallel = ii_parallel(storage)

init_time = time()
inverted_index_serial.create_index_serial()
end_time = time()
print(f"Time of serial creation is {end_time - init_time}")


for i in range(1, 8):
    init_time = time()
    inverted_index_parallel.create_index_parallel(i)
    end_time = time()
    print(f"Time of parallel creation with {i} thread(s) is {end_time - init_time}")


