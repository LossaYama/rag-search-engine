import pickle
import os

from .keyword_search import tokenize_text
from .search_utils import load_movies, Movie


class InvertedIndex:
    def __init__(self) -> None:
        # dictionary mapping tokens (strings) to sets of document IDs (integers)
        self.index: dict[str, set[int]] = {}
        # dictionary mapping document IDs to their full document objects
        self.docmap: dict[int, Movie] = {}

    def __add_document(self, doc_id: int, text: str):
        text_tokens = tokenize_text(text)
        for token in text_tokens:
            if token in self.index.keys():
                self.index[token].add(doc_id)
            else:
                self.index[token] = {doc_id}

    def get_documents(self, term: str) -> list[int]:
        return sorted(list(self.index[term]))

    def build(self) -> None:
        movies = load_movies()
        for movie in movies:
            self.docmap[movie["id"]] = movie
            self.__add_document(movie["id"], f"{movie["title"]} {movie["description"]}")

    def save(self) -> None:
        if not os.path.exists("cache"):
            os.mkdir("cache")
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self) -> None:
        with open("cache/index.pkl", "rb") as f:
            self.index = pickle.load(f)
        with open("cache/docmap.pkl", "rb") as f:
            self.docmap = pickle.load(f)