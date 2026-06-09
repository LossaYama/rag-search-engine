import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        query_tokens = remove_stopword_tokens(tokenize_text(query))
        title_tokens = remove_stopword_tokens(tokenize_text(movie["title"]))
        if has_matching_token(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break
    return results

def has_matching_token(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False

def prep_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text
    
def tokenize_text(text: str) -> list[str]:
    text = prep_text(text)
    text_tokens = text.split(" ")
    tokens: list[str] = []
    for text_token in text_tokens:
        if text_token:
            tokens.append(text_token)
    return tokens

def prep_stopwords() -> list[str]:
    stopwords = load_stopwords()
    prep_stopwords: list[str] = []
    for word in stopwords:
        prep_stopwords.append(prep_text(word))
    return prep_stopwords

def remove_stopword_tokens(tokens: list[str]) -> list[str]:
    filter_list = prep_stopwords()
    filtered_tokens = []
    for token in tokens:
        if token not in filter_list:
            filtered_tokens.append(token)
    return filtered_tokens