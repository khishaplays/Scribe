
import httpx


GITHUB_API_URL = "https://api.github.com"


class GitHubService:
    """Handle communication with the GitHub API."""

    def __init__(self):
        self.client = httpx.Client(
            base_url=GITHUB_API_URL,
            timeout=15.0,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "scribe-cli",
            },
        )

    def get_user(self, username: str):
        """Retrieve a public GitHub profile."""
        response = self.client.get(f"/users/{username}")
        response.raise_for_status()
        return response.json()

    def get_repositories(self, username: str):
        """Retrieve public repositories for a GitHub user."""
        repositories = []

        for page in range(1, 11):
            response = self.client.get(
                f"/users/{username}/repos",
                params={
                    "per_page": 100,
                    "page": page,
                    "sort": "updated",
                },
            )
            response.raise_for_status()

            page_results = response.json()
            repositories.extend(page_results)

            if len(page_results) < 100:
                break

        return repositories

    def close(self):
        """Close the HTTP connection."""
        self.client.close()
