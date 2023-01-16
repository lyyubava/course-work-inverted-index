import re
import os 
from threading import Thread
from queue import Queue


def preprocess_document_text(text):
    """Preprocess document before """
    text_lower = text.lower()
    #remove everything that doesn't match letters&&whitespaces&&newlines
    cleaned_text = re.sub(r"[^a-z\s]+", "", text_lower)
    # substitute multiple whitespaces with single one
    formatted_text = re.sub(r"(\s+)", " ", cleaned_text)
    return formatted_text.split()


class InvertedIndex():

    def __init__(self, storage):
        self.preprocessor = preprocess_document_text
        self.storage = storage
        self.index = {}
    
    def update(self, index):
        for word in index:
            if word in self.index:
                self.index[word].append(index[word][0])
                continue
            
            self.index[word] = index[word]

    def preprocess_word(self, word):
        return self.preprocessor(word)[0]
    
    def build_index_from_file(self, file):
        temp_index = {}
        with open(file, "r") as f:
            text = f.read()
            data = self.preprocessor(text)
            for word in data:
                if word in temp_index:
                    temp_index[word][0]["frequency"] += 1
                else: 
                    temp_index[word] = [{"frequency": 1, "docID": file}]
        return temp_index

    def search(self, word):
        word_to_search = self.preprocess_word(word)
        if not word_to_search in self.index:
            return []
        return self.index[word_to_search]

    def worker(self, q):
        while not q.empty():
            self.update(q.get())

    def create_index_parallel(self, num_workers):
        queue = Queue()

        for file in self.storage.storage:
            queue.put(self.build_index_from_file(file))
        threads = [None] * num_workers

        for i in range(num_workers):
            threads[i] = Thread(target=self.worker,args=(queue,))
            threads[i].start()

        for i in range(num_workers):
            threads[i].join()


