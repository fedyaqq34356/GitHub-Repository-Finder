import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def compute_tf(tokens: list[str]) -> dict[str, float]:
    count = Counter(tokens)
    total = max(len(tokens), 1)
    return {word: freq / total for word, freq in count.items()}


def compute_idf(documents: list[list[str]]) -> dict[str, float]:
    n = len(documents)
    df: dict[str, int] = {}
    for doc in documents:
        for word in set(doc):
            df[word] = df.get(word, 0) + 1
    return {word: math.log((n + 1) / (freq + 1)) + 1 for word, freq in df.items()}


def tfidf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    tf = compute_tf(tokens)
    return {word: tf[word] * idf.get(word, 0.0) for word in tf}


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[w] * vec_b[w] for w in common)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / (mag_a * mag_b)


def _repo_tokens(repo: dict) -> list[str]:
    name = repo.get("name", "")
    desc = repo.get("description") or ""
    topics = " ".join(repo.get("topics", []))
    language = repo.get("language") or ""
    return tokenize(f"{name} {desc} {topics} {language}")


def rank_repositories(query: str, repos: list[dict]) -> list[tuple[float, dict]]:
    query_tokens = tokenize(query)
    repo_token_lists = [_repo_tokens(r) for r in repos]

    all_docs = [query_tokens] + repo_token_lists
    idf = compute_idf(all_docs)

    query_vec = tfidf_vector(query_tokens, idf)

    scored: list[tuple[float, dict]] = []
    for tokens, repo in zip(repo_token_lists, repos):
        repo_vec = tfidf_vector(tokens, idf)
        score = cosine_similarity(query_vec, repo_vec)
        scored.append((score, repo))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored