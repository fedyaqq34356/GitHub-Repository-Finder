import sys

from errors import NetworkError, RateLimitError, handle
from search import find_similar


def display(repos: list[dict]) -> None:
    if not repos:
        print("No repositories found.")
        return

    for i, repo in enumerate(repos, 1):
        full_name = repo.get("full_name", "unknown")
        desc = repo.get("description") or "No description"
        url = repo.get("html_url", "")
        stars = repo.get("stargazers_count", 0)
        print(f"\n{i}. {full_name} ({stars} stars)")
        print(f"   {desc[:120]}")
        print(f"   {url}")


def main() -> None:
    while True:
        try:
            query = input("\nSearch: ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        if not query:
            continue

        try:
            limit = input("How many repos to analyze? (default 50): ").strip()
            limit = int(limit) if limit.isdigit() else 50
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        try:
            print(f"Fetching top {limit} repositories from GitHub...")
            results = find_similar(query, top_n=5, per_page=limit)
            print("Ranking by similarity...")
            display(results)
        except RateLimitError:
            print("Rate limit exceeded. Set GITHUB_TOKEN and retry.")
        except NetworkError as e:
            handle(e, "main")
            print("Network error. Check your connection.")
        except Exception as e:
            handle(e, "main")
            print("Unexpected error. See search.log for details.")

        try:
            again = input("\nSearch again? (y/n): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        if again != "y":
            break


if __name__ == "__main__":
    main()