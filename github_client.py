import json
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from errors import GitHubAPIError, NetworkError, RateLimitError, handle

BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN", "")


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 403:
            raise RateLimitError("Rate limit exceeded. Set GITHUB_TOKEN env variable.")
        if e.code == 422:
            raise GitHubAPIError(f"Invalid query: {url}")
        raise NetworkError(f"HTTP {e.code}: {e.reason}")
    except URLError as e:
        raise NetworkError(f"Connection failed: {e.reason}")


def search_repositories(query: str, per_page: int = 50) -> list[dict]:
    encoded = urllib.parse.quote(query)
    url = f"{BASE_URL}/search/repositories?q={encoded}&per_page={per_page}&sort=stars&order=desc"
    try:
        data = _get(url)
        return data.get("items", [])
    except (RateLimitError, NetworkError, GitHubAPIError) as e:
        handle(e, "search_repositories")
        raise


def fetch_topics(owner: str, repo: str) -> list[str]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/topics"
    try:
        data = _get(url)
        return data.get("names", [])
    except Exception as e:
        handle(e, f"fetch_topics:{owner}/{repo}")
        return []