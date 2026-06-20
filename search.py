from algorithms import rank_repositories
from errors import EmptyResponseError, handle
from github_client import fetch_topics, search_repositories


def _enrich(repos: list[dict]) -> list[dict]:
    total = len(repos)
    for i, repo in enumerate(repos, 1):
        owner = repo["owner"]["login"]
        name = repo["name"]
        print(f"  Loading topics [{i}/{total}] {owner}/{name}")
        repo["topics"] = fetch_topics(owner, name)
    return repos


def find_similar(query: str, top_n: int = 5, per_page: int = 50) -> list[dict]:
    try:
        print(f"Searching GitHub for '{query}'...")
        repos = search_repositories(query, per_page=per_page)
        if not repos:
            raise EmptyResponseError(f"No results for query: '{query}'")
        print(f"Found {len(repos)} repositories (top 50 by stars). Enriching with topics...")
        enriched = _enrich(repos)
        print("Computing TF-IDF and cosine similarity...")
        ranked = rank_repositories(query, enriched)
        return [repo for _, repo in ranked[:top_n]]
    except EmptyResponseError as e:
        handle(e, "find_similar")
        return []
    except Exception as e:
        handle(e, "find_similar")
        raise