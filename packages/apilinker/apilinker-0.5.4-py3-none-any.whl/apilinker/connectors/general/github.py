"""
GitHub API connector for code repository research and analysis.

Provides access to GitHub's REST API for repository data, contribution
analysis, and software development research.
"""

from typing import Any, Dict, List, Optional
from apilinker.core.connector import ApiConnector


class GitHubConnector(ApiConnector):
    """
    Connector for GitHub API.

    Provides access to repository data, user profiles, commits, issues,
    and other GitHub resources for software engineering research.

    Example usage:
        connector = GitHubConnector(token="github_token")
        repos = connector.search_repositories("machine learning")
        user_info = connector.get_user_info("octocat")
        commits = connector.get_repository_commits("owner/repo")
    """

    def __init__(self, token: Optional[str] = None, **kwargs):
        """
        Initialize GitHub connector.

        Args:
            token: GitHub personal access token (recommended for higher rate limits)
            **kwargs: Additional connector arguments
        """
        # GitHub API base URL
        base_url = "https://api.github.com"

        # Set up headers
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ApiLinker/0.5.4",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        # Define GitHub endpoints
        endpoints = {
            "search_repositories": {
                "path": "/search/repositories",
                "method": "GET",
                "params": {},
            },
            "search_users": {"path": "/search/users", "method": "GET", "params": {}},
            "search_code": {"path": "/search/code", "method": "GET", "params": {}},
            "search_issues": {"path": "/search/issues", "method": "GET", "params": {}},
            "get_repository": {
                "path": "/repos/{owner}/{repo}",
                "method": "GET",
                "params": {},
            },
            "get_user": {"path": "/users/{username}", "method": "GET", "params": {}},
            "get_user_repos": {
                "path": "/users/{username}/repos",
                "method": "GET",
                "params": {},
            },
            "get_repository_commits": {
                "path": "/repos/{owner}/{repo}/commits",
                "method": "GET",
                "params": {},
            },
            "get_repository_issues": {
                "path": "/repos/{owner}/{repo}/issues",
                "method": "GET",
                "params": {},
            },
            "get_repository_contributors": {
                "path": "/repos/{owner}/{repo}/contributors",
                "method": "GET",
                "params": {},
            },
            "get_repository_languages": {
                "path": "/repos/{owner}/{repo}/languages",
                "method": "GET",
                "params": {},
            },
            "get_repository_stats": {
                "path": "/repos/{owner}/{repo}/stats/participation",
                "method": "GET",
                "params": {},
            },
        }

        super().__init__(
            connector_type="github",
            base_url=base_url,
            auth_config=None,  # Auth handled via headers
            endpoints=endpoints,
            default_headers=headers,
            **kwargs,
        )

        self.token = token

    def search_repositories(
        self,
        query: str,
        sort: str = "best-match",
        order: str = "desc",
        per_page: int = 30,
        language: Optional[str] = None,
        created_after: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for repositories.

        Args:
            query: Search query
            sort: Sort criteria ("stars", "forks", "help-wanted-issues", "updated", "best-match")
            order: Sort order ("asc" or "desc")
            per_page: Results per page (max 100)
            language: Filter by programming language
            created_after: Filter by creation date (YYYY-MM-DD)

        Returns:
            Dictionary containing repository search results
        """
        params = {"q": query, "sort": sort, "order": order, "per_page": per_page}

        # Add filters to query
        query_filters = []
        if language:
            query_filters.append(f"language:{language}")
        if created_after:
            query_filters.append(f"created:>{created_after}")

        if query_filters:
            params["q"] = f"{query} {' '.join(query_filters)}"

        return self.fetch_data("search_repositories", params)

    def search_users(
        self,
        query: str,
        sort: str = "best-match",
        order: str = "desc",
        per_page: int = 30,
    ) -> Dict[str, Any]:
        """
        Search for users.

        Args:
            query: Search query (username, name, email)
            sort: Sort criteria ("followers", "repositories", "joined", "best-match")
            order: Sort order ("asc" or "desc")
            per_page: Results per page (max 100)

        Returns:
            Dictionary containing user search results
        """
        params = {"q": query, "sort": sort, "order": order, "per_page": per_page}

        return self.fetch_data("search_users", params)

    def search_code(
        self,
        query: str,
        sort: str = "best-match",
        order: str = "desc",
        per_page: int = 30,
        language: Optional[str] = None,
        repository: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for code.

        Args:
            query: Search query
            sort: Sort criteria ("indexed", "best-match")
            order: Sort order ("asc" or "desc")
            per_page: Results per page (max 100)
            language: Filter by programming language
            repository: Filter by repository (owner/repo)

        Returns:
            Dictionary containing code search results
        """
        params = {"q": query, "sort": sort, "order": order, "per_page": per_page}

        # Add filters to query
        query_filters = []
        if language:
            query_filters.append(f"language:{language}")
        if repository:
            query_filters.append(f"repo:{repository}")

        if query_filters:
            params["q"] = f"{query} {' '.join(query_filters)}"

        return self.fetch_data("search_code", params)

    def get_repository_info(
        self,
        owner: str,
        repo: str,
        include_contributors: bool = True,
        include_languages: bool = True,
        include_recent_commits: bool = True,
    ) -> Dict[str, Any]:
        """
        Get comprehensive repository information.

        Args:
            owner: Repository owner
            repo: Repository name
            include_contributors: Whether to include contributor data
            include_languages: Whether to include language statistics
            include_recent_commits: Whether to include recent commit activity

        Returns:
            Dictionary containing comprehensive repository data
        """
        # Get basic repository info
        repo_path = self.endpoints["get_repository"].path.format(owner=owner, repo=repo)

        response = self.client.request(
            method="GET", url=repo_path, headers=self.default_headers
        )
        response.raise_for_status()
        repo_data = response.json()

        # Add additional data if requested
        if include_contributors:
            try:
                contributors = self.get_repository_contributors(owner, repo)
                repo_data["contributors_data"] = contributors[
                    :10
                ]  # Top 10 contributors
            except Exception:
                repo_data["contributors_data"] = {
                    "note": "Contributors data not available"
                }

        if include_languages:
            try:
                languages = self.get_repository_languages(owner, repo)
                repo_data["languages_data"] = languages
            except Exception:
                repo_data["languages_data"] = {"note": "Languages data not available"}

        if include_recent_commits:
            try:
                commits = self.get_repository_commits(owner, repo, per_page=10)
                repo_data["recent_commits"] = commits[:10]
            except Exception:
                repo_data["recent_commits"] = {
                    "note": "Recent commits data not available"
                }

        return repo_data

    def get_user_info(
        self, username: str, include_repositories: bool = True, max_repos: int = 20
    ) -> Dict[str, Any]:
        """
        Get user information and repositories.

        Args:
            username: GitHub username
            include_repositories: Whether to include user's repositories
            max_repos: Maximum number of repositories to include

        Returns:
            Dictionary containing user information
        """
        user_path = self.endpoints["get_user"].path.format(username=username)

        response = self.client.request(
            method="GET", url=user_path, headers=self.default_headers
        )
        response.raise_for_status()
        user_data = response.json()

        if include_repositories:
            try:
                repos = self.get_user_repositories(username, per_page=max_repos)
                user_data["repositories_data"] = repos
            except Exception:
                user_data["repositories_data"] = {
                    "note": "Repositories data not available"
                }

        return user_data

    def get_user_repositories(
        self,
        username: str,
        type: str = "owner",
        sort: str = "updated",
        per_page: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Get user's repositories.

        Args:
            username: GitHub username
            type: Repository type ("all", "owner", "member")
            sort: Sort order ("created", "updated", "pushed", "full_name")
            per_page: Results per page

        Returns:
            List of repository dictionaries
        """
        params = {"type": type, "sort": sort, "per_page": per_page}

        repos_path = self.endpoints["get_user_repos"].path.format(username=username)

        response = self.client.request(
            method="GET", url=repos_path, params=params, headers=self.default_headers
        )
        response.raise_for_status()
        return response.json()

    def get_repository_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        per_page: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Get repository commits.

        Args:
            owner: Repository owner
            repo: Repository name
            since: Only commits after this date (ISO 8601)
            until: Only commits before this date (ISO 8601)
            per_page: Results per page

        Returns:
            List of commit dictionaries
        """
        params = {"per_page": per_page}
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        commits_path = self.endpoints["get_repository_commits"].path.format(
            owner=owner, repo=repo
        )

        response = self.client.request(
            method="GET", url=commits_path, params=params, headers=self.default_headers
        )
        response.raise_for_status()
        return response.json()

    def get_repository_contributors(
        self, owner: str, repo: str, per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get repository contributors.

        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Results per page

        Returns:
            List of contributor dictionaries
        """
        params = {"per_page": per_page}

        contributors_path = self.endpoints["get_repository_contributors"].path.format(
            owner=owner, repo=repo
        )

        response = self.client.request(
            method="GET",
            url=contributors_path,
            params=params,
            headers=self.default_headers,
        )
        response.raise_for_status()
        return response.json()

    def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get repository programming languages.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary mapping languages to bytes of code
        """
        languages_path = self.endpoints["get_repository_languages"].path.format(
            owner=owner, repo=repo
        )

        response = self.client.request(
            method="GET", url=languages_path, headers=self.default_headers
        )
        response.raise_for_status()
        return response.json()

    def analyze_repository_activity(
        self,
        owner: str,
        repo: str,
        analyze_contributors: bool = True,
        analyze_commits: bool = True,
        analyze_issues: bool = True,
    ) -> Dict[str, Any]:
        """
        Analyze repository activity patterns.

        Args:
            owner: Repository owner
            repo: Repository name
            analyze_contributors: Whether to analyze contributor patterns
            analyze_commits: Whether to analyze commit patterns
            analyze_issues: Whether to analyze issue patterns

        Returns:
            Dictionary containing activity analysis
        """
        analysis = {
            "repository": f"{owner}/{repo}",
            "analysis_timestamp": None,
            "activity_summary": {},
        }

        from datetime import datetime

        analysis["analysis_timestamp"] = datetime.now().isoformat()

        # Get basic repository info
        repo_info = self.get_repository_info(
            owner, repo, include_contributors=analyze_contributors
        )
        analysis["repository_info"] = {
            "stars": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "open_issues": repo_info.get("open_issues_count", 0),
            "watchers": repo_info.get("watchers_count", 0),
            "created_at": repo_info.get("created_at"),
            "updated_at": repo_info.get("updated_at"),
        }

        if analyze_contributors and "contributors_data" in repo_info:
            contributors = repo_info["contributors_data"]
            analysis["contributor_analysis"] = {
                "total_contributors": len(contributors),
                "top_contributor": contributors[0] if contributors else None,
                "contribution_distribution": self._analyze_contribution_distribution(
                    contributors
                ),
            }

        if analyze_commits:
            try:
                recent_commits = self.get_repository_commits(owner, repo, per_page=100)
                analysis["commit_analysis"] = self._analyze_commit_patterns(
                    recent_commits
                )
            except Exception:
                analysis["commit_analysis"] = {"note": "Commit analysis not available"}

        if analyze_issues:
            try:
                issues = self.get_repository_issues(
                    owner, repo, state="all", per_page=100
                )
                analysis["issue_analysis"] = self._analyze_issue_patterns(issues)
            except Exception:
                analysis["issue_analysis"] = {"note": "Issue analysis not available"}

        return analysis

    def get_repository_issues(
        self, owner: str, repo: str, state: str = "open", per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get repository issues.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state ("open", "closed", "all")
            per_page: Results per page

        Returns:
            List of issue dictionaries
        """
        params = {"state": state, "per_page": per_page}

        issues_path = self.endpoints["get_repository_issues"].path.format(
            owner=owner, repo=repo
        )

        response = self.client.request(
            method="GET", url=issues_path, params=params, headers=self.default_headers
        )
        response.raise_for_status()
        return response.json()

    def research_technology_adoption(
        self,
        technology_keywords: List[str],
        min_stars: int = 100,
        max_results: int = 100,
    ) -> Dict[str, Any]:
        """
        Research technology adoption patterns on GitHub.

        Args:
            technology_keywords: List of technology keywords to search
            min_stars: Minimum stars for repositories
            max_results: Maximum results per technology

        Returns:
            Dictionary containing technology adoption analysis
        """
        adoption_data = {
            "technologies": {},
            "overall_trends": {},
            "top_repositories": [],
        }

        for tech in technology_keywords:
            # Search for repositories using this technology
            repos = self.search_repositories(
                query=f"{tech} stars:>={min_stars}",
                sort="stars",
                order="desc",
                per_page=max_results,
            )

            if "items" in repos:
                repo_items = repos["items"]

                # Analyze adoption metrics
                total_stars = sum(
                    repo.get("stargazers_count", 0) for repo in repo_items
                )
                total_forks = sum(repo.get("forks_count", 0) for repo in repo_items)

                # Language distribution
                languages = {}
                for repo in repo_items:
                    lang = repo.get("language")
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1

                adoption_data["technologies"][tech] = {
                    "repository_count": len(repo_items),
                    "total_stars": total_stars,
                    "total_forks": total_forks,
                    "avg_stars": total_stars / len(repo_items) if repo_items else 0,
                    "language_distribution": sorted(
                        languages.items(), key=lambda x: x[1], reverse=True
                    )[:5],
                    "top_repositories": repo_items[:5],
                }

                # Add to overall top repositories
                adoption_data["top_repositories"].extend(repo_items[:3])

        # Sort overall top repositories by stars
        adoption_data["top_repositories"].sort(
            key=lambda x: x.get("stargazers_count", 0), reverse=True
        )
        adoption_data["top_repositories"] = adoption_data["top_repositories"][:10]

        return adoption_data

    def _analyze_contribution_distribution(
        self, contributors: List[Dict]
    ) -> Dict[str, Any]:
        """Analyze contribution distribution among contributors."""
        if not contributors:
            return {"distribution": "No contributors"}

        contributions = [c.get("contributions", 0) for c in contributors]
        total_contributions = sum(contributions)

        if total_contributions == 0:
            return {"distribution": "No contributions data"}

        # Calculate concentration (what % of contributions come from top contributors)
        top_contributor_pct = (
            (contributions[0] / total_contributions * 100) if contributions else 0
        )
        top_3_pct = (
            (sum(contributions[:3]) / total_contributions * 100)
            if len(contributions) >= 3
            else 100
        )

        return {
            "total_contributions": total_contributions,
            "top_contributor_percentage": round(top_contributor_pct, 1),
            "top_3_percentage": round(top_3_pct, 1),
            "distribution_type": (
                "concentrated" if top_contributor_pct > 50 else "distributed"
            ),
        }

    def _analyze_commit_patterns(self, commits: List[Dict]) -> Dict[str, Any]:
        """Analyze commit patterns."""
        if not commits:
            return {"pattern": "No commits to analyze"}

        from datetime import datetime
        from collections import Counter

        # Extract commit dates
        commit_dates = []
        authors = []

        for commit in commits:
            try:
                commit_date = commit.get("commit", {}).get("author", {}).get("date")
                if commit_date:
                    dt = datetime.fromisoformat(commit_date.replace("Z", "+00:00"))
                    commit_dates.append(dt)

                author = commit.get("commit", {}).get("author", {}).get("name")
                if author:
                    authors.append(author)
            except Exception:
                continue

        if not commit_dates:
            return {"pattern": "No valid commit dates"}

        # Analyze patterns
        author_counts = Counter(authors)

        # Calculate commit frequency
        if len(commit_dates) > 1:
            date_range = (max(commit_dates) - min(commit_dates)).days
            commits_per_day = len(commit_dates) / max(date_range, 1)
        else:
            commits_per_day = 0

        return {
            "total_commits_analyzed": len(commits),
            "unique_authors": len(author_counts),
            "commits_per_day": round(commits_per_day, 2),
            "most_active_author": (
                author_counts.most_common(1)[0] if author_counts else None
            ),
            "date_range_days": date_range if len(commit_dates) > 1 else 0,
        }

    def _analyze_issue_patterns(self, issues: List[Dict]) -> Dict[str, Any]:
        """Analyze issue patterns."""
        if not issues:
            return {"pattern": "No issues to analyze"}

        open_issues = [i for i in issues if i.get("state") == "open"]
        closed_issues = [i for i in issues if i.get("state") == "closed"]

        # Calculate labels
        labels = []
        for issue in issues:
            issue_labels = issue.get("labels", [])
            for label in issue_labels:
                if isinstance(label, dict):
                    labels.append(label.get("name", ""))

        from collections import Counter

        label_counts = Counter(labels)

        return {
            "total_issues": len(issues),
            "open_issues": len(open_issues),
            "closed_issues": len(closed_issues),
            "open_rate": (
                round(len(open_issues) / len(issues) * 100, 1) if issues else 0
            ),
            "common_labels": label_counts.most_common(5),
        }
