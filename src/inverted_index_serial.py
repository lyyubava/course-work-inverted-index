import re

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

    @staticmethod
    def merge_indexes(index, other_index):
        result_index = {}
        if len(index) == 0 and len(other_index) == 0:
            return result_index
        
        if len(index) == 0 or len(other_index) == 0:
            return index if len(index) > 0 else other_index
        
        result_index = index if len(index) > len(other_index) else other_index
        iterable_index = other_index if result_index == index else index

        for word in iterable_index:

            if word in result_index:
                result_index[word].append(iterable_index[word][0])
                continue
            
            result_index[word] = iterable_index[word]
        return result_index
        
    def create_index_serial(self):
        for file in self.storage.storage:
            self.index = self.merge_indexes(self.index, self.build_index_from_file(file))

    def search(self, word):
        word_to_search = self.preprocess_word(word)
        if not word_to_search in self.index:
            return []
        return self.index[word_to_search]
    


