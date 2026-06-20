# GitHub Repository Finder

A terminal tool that takes a short description from the user and finds the most relevant GitHub repositories using **TF-IDF** and **Cosine Similarity** algorithms. No third-party dependencies — pure Python standard library only.

---

## How It Works

1. You enter a short description (2–3 words)
2. You choose how many repositories to analyze
3. The tool fetches the top N repositories from GitHub by stars
4. Each repository is enriched with its topics
5. TF-IDF vectors are computed for your query and every repository
6. Cosine Similarity ranks them by relevance
7. The 5 most similar repositories are displayed with links

---

## Algorithms

**TF-IDF (Term Frequency – Inverse Document Frequency)**
Weighs words by how important they are. Common words like "the" get low weight. Rare domain-specific words like "neural" get high weight.

**Cosine Similarity**
Converts each text into a numeric vector and measures the angle between the query vector and each repository vector. The smaller the angle — the more similar the meaning.

---

## Project Structure

```
github_finder/
├── main.py           — terminal interface
├── search.py         — search orchestration
├── github_client.py  — GitHub API requests
├── algorithms.py     — TF-IDF + Cosine Similarity
├── errors.py         — error handling + logging to search.log
└── requirements.txt  — no dependencies required
```

---

## Getting Started

**Requirements:** Python 3.10+

```bash
git clone https://github.com/your-username/github-finder
cd github-finder
python main.py
```

---

## GitHub Token (recommended)

Without a token: **60 requests/hour**
With a free token: **5000 requests/hour**

```bash
export GITHUB_TOKEN=your_token_here
python main.py
```

Get your token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (no scopes needed)

---

## Example

```
Search: machine learning visualization
How many repos to analyze? (default 50): 30
Searching GitHub for 'machine learning visualization'...
Found 30 repositories (top 30 by stars). Enriching with topics...
  Loading topics [1/30] tensorflow/tensorflow
  ...
Computing TF-IDF and cosine similarity...
Ranking by similarity...

1. matplotlib/matplotlib (19000 stars)
   matplotlib: plotting with Python
   https://github.com/matplotlib/matplotlib

2. streamlit/streamlit (32000 stars)
   Streamlit — A faster way to build and share data apps
   https://github.com/streamlit/streamlit
...
```

---

## Logging

All errors are silently logged to `search.log` in the project directory. The terminal stays clean.

---

<div align="center">

If you found this repository useful, please consider giving it a ⭐

Made with ❤️

</div>