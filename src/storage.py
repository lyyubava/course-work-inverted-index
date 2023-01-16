import os

class Storage():
    def __init__(self, V, *args):
        self.dirs = args
        self.V = V
    
    @property
    def storage(self):
        storage = []
        for dir in self.dirs:
            
            N = len(os.listdir(dir))
            lower_index = N*(self.V-1) // 50
            upper_index = N*(self.V) // 50
            ordered = sorted(os.listdir(dir), key=lambda filename: int(filename.split("_")[0]))
            sliced_files = ordered[lower_index:upper_index]
            sliced_files_pathes = [os.path.join(dir, file) for file in sliced_files]
            storage += sliced_files_pathes

        return storage
    