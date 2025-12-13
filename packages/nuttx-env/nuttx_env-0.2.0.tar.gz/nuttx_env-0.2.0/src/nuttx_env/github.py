"""
Utils for work with github
"""
from __future__ import annotations

from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Generator

import requests


GITHUB_URL_BASE = "https://api.github.com"


# --- Models ---

@dataclass
class GitHubTag:
    """
    Not all fields
    """
    name: str


# --- Methods ---

def gh_parse_url(repo_url: str) -> tuple[str, str]:
    """
    Parse GitHub repository URL and extract owner and repo name

    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)

    Returns:
        Tuple of (owner, repo_name)

    Raises:
        ValueError: If URL is not a valid GitHub repository URL
    """
    parsed = urlparse(repo_url)

    if parsed.netloc not in ['github.com', 'www.github.com']:
        raise ValueError("URL must be a GitHub repository")

    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repository URL format")

    owner = path_parts[0]
    repo_name = path_parts[1]

    return owner, repo_name


def get_github_tags(owner: str, repo: str) -> list[GitHubTag]:
    """
    Fetch all tags from a GitHub repository

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        List of tag information dictionaries

    Raises:
        requests.RequestException: If API request fails
    """
    url = f"{GITHUB_URL_BASE}/repos/{owner}/{repo}/tags"

    # TODO: Don't get all, add pages
    response = requests.get(url)
    response.raise_for_status()

    result = []
    for item in response.json():
        result.append(GitHubTag(name=item["name"]))

    return result


def gh_download_repo(
    repo_url: str,
    tag: str
) -> Generator[tuple[int, int, bytes], None, None]:
    """
    Download GitHub repository archive by tag as zip with progress tracking

    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        tag: repository tag

    Yields:
        Tuple of (downloaded_bytes, total_bytes, chunk_data)
        for progress tracking

    Raises:
        ValueError: If URL is not a valid GitHub repository URL
        requests.RequestException: If download fails
    """
    owner, repo_name = gh_parse_url(repo_url)

    # GitHub archive URL format:
    # https://github.com/owner/repo/archive/refs/tags/tag.zip
    archive_url = (
        f"https://github.com/{owner}/{repo_name}/archive/refs/tags/{tag}.zip"
    )

    # Stream the download to track progress
    response = requests.get(archive_url, stream=True)
    response.raise_for_status()

    # Get total size from headers
    total_size = int(response.headers.get('Content-Length', 0))
    downloaded = 0

    # Yield progress and data chunks
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive chunks
            downloaded += len(chunk)
            yield downloaded, total_size, chunk
