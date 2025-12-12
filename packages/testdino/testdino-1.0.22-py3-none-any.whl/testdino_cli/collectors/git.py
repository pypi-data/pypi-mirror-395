"""Git metadata collector

Uses GitPython for git operations with environment variable fallbacks for CI/CD
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from urllib.parse import quote, urlparse

import httpx
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from testdino_cli.utils.verbose import is_verbose_mode
from testdino_cli.version import VERSION

# HTTP timeout for GitHub API requests (15 seconds)
GITHUB_API_TIMEOUT = 15.0

PRStatus = Literal[
    "", "open", "draft", "ready_for_review", "changes_requested", "approved", "merged", "closed"
]


@dataclass
class CommitInfo:
    """Commit information"""

    hash: str
    message: str
    author: str
    author_id: Optional[str] = None
    email: str = ""
    timestamp: str = ""


@dataclass
class RepositoryInfo:
    """Repository information"""

    name: str
    url: str


@dataclass
class PullRequestInfo:
    """Pull request information"""

    id: str = ""
    title: str = ""
    url: str = ""
    status: PRStatus = ""


@dataclass
class GitMetadata:
    """Git metadata structure matching server schema"""

    branch: str
    commit: CommitInfo
    repository: RepositoryInfo
    pr: PullRequestInfo = field(default_factory=PullRequestInfo)


class GitCollector:
    """Collector for Git metadata"""

    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        try:
            self.repo = Repo(self.repo_path)
        except InvalidGitRepositoryError:
            self.repo = None

    async def get_metadata(self) -> GitMetadata:
        """Gather Git metadata: branch, latest commit, and remote repository info"""
        # Try to get metadata from git commands first
        git_metadata = await self._get_git_command_metadata()

        # Get environment variable metadata as fallback
        env_metadata = await self._get_environment_metadata()

        # Determine if we should prioritize environment variables
        is_gitlab_ci = os.getenv("GITLAB_CI") == "true"
        is_circle_ci = os.getenv("CIRCLECI") == "true"
        is_azure_devops = os.getenv("TF_BUILD") == "True" or bool(os.getenv("AZURE_HTTP_USER_AGENT"))
        is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
        should_prioritize_env = is_gitlab_ci or is_circle_ci or is_azure_devops or is_github_actions

        # Build commit object
        commit_author_id = (
            env_metadata.get("authorId") or git_metadata.get("commit", {}).get("author_id")
            if should_prioritize_env
            else git_metadata.get("commit", {}).get("author_id") or env_metadata.get("authorId")
        )

        commit_data = CommitInfo(
            hash=(
                env_metadata.get("commitHash") or git_metadata.get("commit", {}).get("hash") or "unknown"
                if should_prioritize_env
                else git_metadata.get("commit", {}).get("hash") or env_metadata.get("commitHash") or "unknown"
            ),
            message=(
                env_metadata.get("commitMessage") or git_metadata.get("commit", {}).get("message") or ""
                if should_prioritize_env
                else git_metadata.get("commit", {}).get("message") or env_metadata.get("commitMessage") or ""
            ),
            author=(
                env_metadata.get("author") or git_metadata.get("commit", {}).get("author") or ""
                if should_prioritize_env
                else git_metadata.get("commit", {}).get("author") or env_metadata.get("author") or ""
            ),
            email=(
                env_metadata.get("email") or git_metadata.get("commit", {}).get("email") or ""
                if should_prioritize_env
                else git_metadata.get("commit", {}).get("email") or env_metadata.get("email") or ""
            ),
            timestamp=git_metadata.get("commit", {}).get("timestamp") or datetime.now().isoformat(),
            author_id=commit_author_id,
        )

        metadata = GitMetadata(
            branch=(
                env_metadata.get("branch") or git_metadata.get("branch") or "unknown"
                if should_prioritize_env
                else git_metadata.get("branch") or env_metadata.get("branch") or "unknown"
            ),
            commit=commit_data,
            repository=RepositoryInfo(
                name=git_metadata.get("repository", {}).get("name") or env_metadata.get("repoName") or "unknown",
                url=(
                    env_metadata.get("repoUrl") or git_metadata.get("repository", {}).get("url") or ""
                    if should_prioritize_env
                    else git_metadata.get("repository", {}).get("url") or env_metadata.get("repoUrl") or ""
                ),
            ),
            pr=PullRequestInfo(
                id=git_metadata.get("pr", {}).get("id") or env_metadata.get("prId") or "",
                title=git_metadata.get("pr", {}).get("title") or env_metadata.get("prTitle") or "",
                url=git_metadata.get("pr", {}).get("url") or env_metadata.get("prUrl") or "",
                status=self._normalize_status(
                    git_metadata.get("pr", {}).get("status") or env_metadata.get("prStatus") or ""
                ),
            ),
        )

        if is_verbose_mode():
            print(f"🔍 Git metadata: {metadata.branch}")

        return metadata

    def _normalize_status(self, status: str) -> PRStatus:
        """Normalize PR status to match server enum"""
        normalized = status.lower()
        valid_statuses: list[PRStatus] = [
            "open",
            "draft",
            "ready_for_review",
            "changes_requested",
            "approved",
            "merged",
            "closed",
        ]
        return normalized if normalized in valid_statuses else ""  # type: ignore

    async def _get_git_command_metadata(self) -> dict:
        """Attempt to gather metadata using git commands"""
        metadata: dict = {"pr": {}}

        if not self.repo:
            return metadata

        # Get branch
        try:
            metadata["branch"] = self.repo.active_branch.name
        except Exception:
            pass

        # Get latest commit
        try:
            commit = self.repo.head.commit
            metadata["commit"] = {
                "hash": commit.hexsha,
                "message": commit.message.strip(),
                "author": commit.author.name,
                "email": commit.author.email,
                "timestamp": datetime.fromtimestamp(commit.committed_date).isoformat(),
            }
        except Exception:
            pass

        # Get remote repository
        try:
            origin = self.repo.remote("origin")
            url = next((u for u in origin.urls), "")
            metadata["repository"] = {
                "url": url,
                "name": self._extract_repo_name_from_url(url),
            }
        except Exception:
            pass

        return metadata

    async def _get_environment_metadata(self) -> dict:
        """Extract git metadata from environment variables (CI/CD contexts)"""
        env = os.environ
        env_info: dict = {}

        # GitHub Actions
        if env.get("GITHUB_ACTIONS") == "true":
            # For Pull Requests, prioritize GITHUB_HEAD_REF
            if env.get("GITHUB_EVENT_NAME") == "pull_request" and env.get("GITHUB_HEAD_REF"):
                env_info["branch"] = env.get("GITHUB_HEAD_REF")
            else:
                extracted_branch = self._extract_branch_from_ref(env.get("GITHUB_REF"))
                if extracted_branch:
                    env_info["branch"] = extracted_branch

            # Try to get PR data from GitHub event file
            if env.get("GITHUB_EVENT_NAME") == "pull_request" and env.get("GITHUB_EVENT_PATH"):
                try:
                    event_path = Path(env["GITHUB_EVENT_PATH"])
                    event_data = json.loads(event_path.read_text())
                    pull_request = event_data.get("pull_request")

                    if pull_request:
                        if pull_request.get("head", {}).get("sha"):
                            env_info["commitHash"] = pull_request["head"]["sha"]
                        if pull_request.get("title"):
                            env_info["prTitle"] = pull_request["title"]

                        # Determine PR status
                        state = pull_request.get("state")
                        draft = pull_request.get("draft")
                        merged = pull_request.get("merged")

                        if draft:
                            env_info["prStatus"] = "draft"
                        elif merged:
                            env_info["prStatus"] = "merged"
                        elif state == "open":
                            env_info["prStatus"] = "open"
                        elif state == "closed":
                            env_info["prStatus"] = "closed"

                        # Extract commit details using git
                        if pull_request.get("head", {}).get("sha"):
                            await self._extract_commit_from_sha(pull_request["head"]["sha"], env_info)

                except Exception:
                    pass

            if not env_info.get("commitHash") and env.get("GITHUB_SHA"):
                env_info["commitHash"] = env["GITHUB_SHA"]

            if env.get("GITHUB_REPOSITORY"):
                env_info["repoName"] = env["GITHUB_REPOSITORY"]
                env_info["repoUrl"] = f"https://github.com/{env['GITHUB_REPOSITORY']}"

            # For non-PR events, try to fetch author info from GitHub API
            if env.get("GITHUB_EVENT_NAME") != "pull_request":
                # [Priority 1 - Non-PR] Try to get commit info from Branch Commit API (most accurate)
                if env.get("GITHUB_REPOSITORY") and env_info.get("branch"):
                    branch_commit_info = await self._fetch_github_branch_commit(
                        env["GITHUB_REPOSITORY"], env_info["branch"]
                    )
                    if branch_commit_info:
                        # Use commit message from API if not already set
                        if branch_commit_info.get("message") and not env_info.get("commitMessage"):
                            env_info["commitMessage"] = branch_commit_info["message"]
                        # Use email from API if not already set
                        if branch_commit_info.get("email") and not env_info.get("email"):
                            env_info["email"] = branch_commit_info["email"]
                        # Always use GitHub username from Branch Commit API (highest priority)
                        if branch_commit_info.get("author"):
                            env_info["author"] = branch_commit_info["author"]
                        # Save GitHub user ID for deduplication (highest priority)
                        if branch_commit_info.get("authorId"):
                            env_info["authorId"] = branch_commit_info["authorId"]

                # [Priority 2 - Non-PR] Fallback to GitHub Users API if Branch Commit API didn't provide login
                if env.get("GITHUB_ACTOR") and not env_info.get("author"):
                    user_info = await self._fetch_github_user_info(env["GITHUB_ACTOR"])
                    if user_info:
                        # Use GitHub username from Users API (fallback)
                        if user_info.get("login"):
                            env_info["author"] = user_info["login"]
                        # Save GitHub user ID for deduplication (fallback)
                        if user_info.get("id") and not env_info.get("authorId"):
                            env_info["authorId"] = user_info["id"]

            # Extract PR info
            if env.get("GITHUB_EVENT_NAME") == "pull_request" and env.get("GITHUB_REF"):
                pr_match = re.search(r"refs/pull/(\d+)/", env["GITHUB_REF"])
                if pr_match:
                    env_info["prId"] = pr_match.group(1)
                    if env.get("GITHUB_REPOSITORY"):
                        env_info["prUrl"] = f"https://github.com/{env['GITHUB_REPOSITORY']}/pull/{pr_match.group(1)}"

                # Try to get PR details from GitHub API for PRs
                if env.get("GITHUB_REPOSITORY") and env_info.get("prId"):
                    pr_details = await self._fetch_github_pull_request_details(
                        env["GITHUB_REPOSITORY"], env_info["prId"]
                    )
                    if pr_details:
                        if pr_details.get("title") and not env_info.get("prTitle"):
                            env_info["prTitle"] = pr_details["title"]
                        if pr_details.get("status") and not env_info.get("prStatus"):
                            env_info["prStatus"] = pr_details["status"]

                # Try to enhance with GitHub API data for PRs (for GitHub user ID)
                if (
                    env.get("GITHUB_REPOSITORY")
                    and env.get("GITHUB_HEAD_REF")
                    and not env_info.get("authorId")
                ):
                    branch_commit_info = await self._fetch_github_branch_commit(
                        env["GITHUB_REPOSITORY"], env["GITHUB_HEAD_REF"]
                    )
                    if branch_commit_info:
                        # Only use API data to fill in missing fields (don't override git data)
                        if not env_info.get("commitMessage") and branch_commit_info.get("message"):
                            env_info["commitMessage"] = branch_commit_info["message"]
                        if not env_info.get("email") and branch_commit_info.get("email"):
                            env_info["email"] = branch_commit_info["email"]
                        if not env_info.get("commitHash") and branch_commit_info.get("sha"):
                            env_info["commitHash"] = branch_commit_info["sha"]
                        # GitHub user ID is valuable for deduplication
                        if branch_commit_info.get("authorId"):
                            env_info["authorId"] = branch_commit_info["authorId"]
                        # Only use GitHub username if git data is not available
                        if not env_info.get("author") and branch_commit_info.get("author"):
                            env_info["author"] = branch_commit_info["author"]

        # GitLab CI
        elif env.get("GITLAB_CI") == "true":
            # Branch name - prefer CI_COMMIT_BRANCH over CI_COMMIT_REF_NAME for accuracy
            if env.get("CI_COMMIT_BRANCH"):
                env_info["branch"] = env["CI_COMMIT_BRANCH"]
            elif env.get("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"):
                # For merge requests, use the source branch
                env_info["branch"] = env["CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"]
            elif env.get("CI_COMMIT_REF_NAME"):
                env_info["branch"] = env["CI_COMMIT_REF_NAME"]

            if env.get("CI_COMMIT_SHA"):
                env_info["commitHash"] = env["CI_COMMIT_SHA"]
            if env.get("CI_COMMIT_MESSAGE"):
                env_info["commitMessage"] = env["CI_COMMIT_MESSAGE"]
            if env.get("CI_COMMIT_AUTHOR"):
                env_info["author"] = env["CI_COMMIT_AUTHOR"]
            if env.get("CI_COMMIT_AUTHOR_EMAIL"):
                env_info["email"] = env["CI_COMMIT_AUTHOR_EMAIL"]
            if env.get("CI_PROJECT_PATH"):
                env_info["repoName"] = env["CI_PROJECT_PATH"]

            # Clean the repository URL to remove CI token
            if env.get("CI_REPOSITORY_URL"):
                env_info["repoUrl"] = self._clean_gitlab_url(env["CI_REPOSITORY_URL"])
            elif env.get("CI_PROJECT_URL"):
                env_info["repoUrl"] = env["CI_PROJECT_URL"]

            # Merge Request info
            if env.get("CI_MERGE_REQUEST_IID"):
                env_info["prId"] = env["CI_MERGE_REQUEST_IID"]
                if env.get("CI_MERGE_REQUEST_TITLE"):
                    env_info["prTitle"] = env["CI_MERGE_REQUEST_TITLE"]
                if env.get("CI_PROJECT_URL"):
                    env_info["prUrl"] = f"{env['CI_PROJECT_URL']}/-/merge_requests/{env['CI_MERGE_REQUEST_IID']}"

        # Azure DevOps
        elif env.get("TF_BUILD") == "True" or env.get("AZURE_HTTP_USER_AGENT"):
            # Branch handling - prioritize PR source branch for pull requests
            if env.get("BUILD_REASON") == "PullRequest" and env.get("SYSTEM_PULLREQUEST_SOURCEBRANCH"):
                # For PRs, use the source branch
                branch = env["SYSTEM_PULLREQUEST_SOURCEBRANCH"]
                env_info["branch"] = branch.replace("refs/heads/", "") if branch.startswith("refs/heads/") else branch
            elif env.get("BUILD_SOURCEBRANCH"):
                branch = env["BUILD_SOURCEBRANCH"]
                env_info["branch"] = branch.replace("refs/heads/", "") if branch.startswith("refs/heads/") else branch
            elif env.get("BUILD_SOURCEBRANCHNAME"):
                env_info["branch"] = env["BUILD_SOURCEBRANCHNAME"]

            # Commit info
            if env.get("BUILD_SOURCEVERSION"):
                env_info["commitHash"] = env["BUILD_SOURCEVERSION"]
            if env.get("BUILD_SOURCEVERSIONMESSAGE"):
                env_info["commitMessage"] = env["BUILD_SOURCEVERSIONMESSAGE"]

            # Author info
            if env.get("BUILD_REQUESTEDFOR"):
                env_info["author"] = env["BUILD_REQUESTEDFOR"]
            if env.get("BUILD_REQUESTEDFOREMAIL"):
                env_info["email"] = env["BUILD_REQUESTEDFOREMAIL"]

            # Repository info with URL cleaning
            if env.get("BUILD_REPOSITORY_NAME"):
                env_info["repoName"] = env["BUILD_REPOSITORY_NAME"]

            if env.get("BUILD_REPOSITORY_URI"):
                env_info["repoUrl"] = self._clean_azure_devops_url(env["BUILD_REPOSITORY_URI"])
                # Extract clean repo name if not already set
                if not env_info.get("repoName"):
                    env_info["repoName"] = self._extract_repo_name_from_url(env_info["repoUrl"])

            # PR info
            if env.get("SYSTEM_PULLREQUEST_PULLREQUESTID"):
                env_info["prId"] = env["SYSTEM_PULLREQUEST_PULLREQUESTID"]
                if env.get("SYSTEM_PULLREQUEST_PULLREQUESTTITLE"):
                    env_info["prTitle"] = env["SYSTEM_PULLREQUEST_PULLREQUESTTITLE"]
                if env.get("SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI"):
                    env_info["prUrl"] = f"{env['SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI']}/pullrequest/{env['SYSTEM_PULLREQUEST_PULLREQUESTID']}"

        # CircleCI
        elif env.get("CIRCLECI") == "true":
            if env.get("CIRCLE_BRANCH"):
                env_info["branch"] = env["CIRCLE_BRANCH"]
            if env.get("CIRCLE_SHA1"):
                env_info["commitHash"] = env["CIRCLE_SHA1"]

            # CircleCI commit message and author info
            if env.get("CIRCLE_USERNAME"):
                env_info["author"] = env["CIRCLE_USERNAME"]
            # Note: CircleCI doesn't provide commit message directly, will fall back to git commands

            # Repository info - construct clean URLs
            if env.get("CIRCLE_PROJECT_USERNAME") and env.get("CIRCLE_PROJECT_REPONAME"):
                env_info["repoName"] = f"{env['CIRCLE_PROJECT_USERNAME']}/{env['CIRCLE_PROJECT_REPONAME']}"
                # Construct clean HTTPS URL
                if env.get("CIRCLE_REPOSITORY_URL"):
                    env_info["repoUrl"] = self._clean_circleci_url(env["CIRCLE_REPOSITORY_URL"])
                else:
                    # Default to GitHub if no repository URL provided
                    env_info["repoUrl"] = f"https://github.com/{env['CIRCLE_PROJECT_USERNAME']}/{env['CIRCLE_PROJECT_REPONAME']}"
            elif env.get("CIRCLE_REPOSITORY_URL"):
                # Clean up the repository URL (remove SSH format, credentials, etc.)
                env_info["repoUrl"] = self._clean_circleci_url(env["CIRCLE_REPOSITORY_URL"])
                env_info["repoName"] = self._extract_repo_name_from_url(env_info["repoUrl"])

            # PR info - enhanced handling
            if env.get("CIRCLE_PULL_REQUEST") or env.get("CIRCLE_PR_NUMBER"):
                # Extract PR number from URL if not directly available
                if env.get("CIRCLE_PR_NUMBER"):
                    env_info["prId"] = env["CIRCLE_PR_NUMBER"]
                elif env.get("CIRCLE_PULL_REQUEST"):
                    # Extract PR number from URL like: https://github.com/owner/repo/pull/123
                    pr_match = re.search(r"/pull/(\d+)$", env["CIRCLE_PULL_REQUEST"])
                    if pr_match:
                        env_info["prId"] = pr_match.group(1)

                if env.get("CIRCLE_PULL_REQUEST"):
                    env_info["prUrl"] = env["CIRCLE_PULL_REQUEST"]

                # Determine PR status based on available info
                if env.get("CIRCLE_TAG"):
                    # If there's a tag, it might be a release PR that was merged
                    env_info["prStatus"] = ""
                elif env.get("CIRCLE_PULL_REQUEST"):
                    env_info["prStatus"] = "open"  # Assume open if we have PR info

        # Jenkins
        elif env.get("JENKINS_URL"):
            git_branch = env.get("BRANCH_NAME") or env.get("GIT_BRANCH")
            if git_branch:
                env_info["branch"] = git_branch.replace("origin/", "")
            if env.get("GIT_COMMIT"):
                env_info["commitHash"] = env["GIT_COMMIT"]
            if env.get("GIT_AUTHOR_NAME"):
                env_info["author"] = env["GIT_AUTHOR_NAME"]
            if env.get("GIT_AUTHOR_EMAIL"):
                env_info["email"] = env["GIT_AUTHOR_EMAIL"]
            if env.get("GIT_URL"):
                env_info["repoUrl"] = env["GIT_URL"]
                env_info["repoName"] = self._extract_repo_name_from_url(env["GIT_URL"])

        return env_info

    async def _extract_commit_from_sha(self, sha: str, env_info: dict) -> None:
        """Extract commit details from SHA using git show"""
        if not self.repo:
            return

        try:
            commit = self.repo.commit(sha)
            if commit.message and not env_info.get("commitMessage"):
                env_info["commitMessage"] = commit.message.strip()
            if commit.author.name and not env_info.get("author"):
                env_info["author"] = commit.author.name
            if commit.author.email and not env_info.get("email"):
                env_info["email"] = commit.author.email
        except Exception:
            pass

    def _extract_branch_from_ref(self, ref: Optional[str]) -> Optional[str]:
        """Extract branch name from git ref"""
        if not ref:
            return None
        if ref.startswith("refs/heads/"):
            return ref.replace("refs/heads/", "")
        if ref.startswith("refs/tags/"):
            return ref.replace("refs/tags/", "")
        return ref

    def _extract_repo_name_from_url(self, url: str) -> str:
        """Extract repository name from URL
        Special handling for Azure DevOps: https://dev.azure.com/org/project/_git/repo -> project/repo
        """
        if not url:
            return ""

        try:
            # First clean GitLab URLs that might contain CI tokens
            clean_url = url
            if "gitlab-ci-token" in url:
                clean_url = self._clean_gitlab_url(url)

            # Remove .git suffix
            clean_url = clean_url.replace(".git", "")

            # Special handling for Azure DevOps URLs
            if "dev.azure.com" in clean_url or "visualstudio.com" in clean_url:
                # Azure DevOps format: https://dev.azure.com/org/project/_git/repo
                azure_match = re.search(r"/([^/]+)/_git/([^/]+)$", clean_url)
                if azure_match:
                    from urllib.parse import unquote
                    project = unquote(azure_match.group(1))
                    repo = unquote(azure_match.group(2))
                    return f"{project}/{repo}"

            # Default: Extract the last two parts of the path
            parts = clean_url.rstrip("/").split("/")
            if len(parts) >= 2:
                try:
                    from urllib.parse import unquote
                    return unquote("/".join(parts[-2:]))
                except Exception:
                    return "/".join(parts[-2:])

            return clean_url
        except Exception:
            return url

    def _clean_gitlab_url(self, url: str) -> str:
        """Clean GitLab repository URL by removing CI token
        Converts: https://gitlab-ci-token:xxxxx@gitlab.com/user/repo.git
        To: https://gitlab.com/user/repo.git
        """
        try:
            parsed = urlparse(url)
            # Remove credentials by rebuilding URL without them
            clean_url = f"{parsed.scheme}://{parsed.hostname}"
            if parsed.port:
                clean_url += f":{parsed.port}"
            clean_url += parsed.path
            if parsed.query:
                clean_url += f"?{parsed.query}"
            return clean_url
        except Exception:
            # Fallback: regex-based cleaning
            return re.sub(r"gitlab-ci-token:[^@]+@", "", url)

    def _clean_circleci_url(self, url: str) -> str:
        """Clean CircleCI repository URL by removing SSH format and converting to HTTPS
        Converts: git@github.com:user/repo.git -> https://github.com/user/repo
        """
        if not url:
            return ""

        try:
            # Handle SSH format: git@github.com:user/repo.git
            if url.startswith("git@"):
                ssh_match = re.match(r"git@([^:]+):([^/]+)/(.+?)(?:\.git)?$", url)
                if ssh_match:
                    host, user, repo = ssh_match.groups()
                    return f"https://{host}/{user}/{repo}"

            # Handle HTTPS URLs - clean credentials
            parsed = urlparse(url)
            clean_url = f"{parsed.scheme}://{parsed.hostname}"
            if parsed.port:
                clean_url += f":{parsed.port}"

            # Remove .git suffix if present
            path = parsed.path
            if path.endswith(".git"):
                path = path[:-4]
            clean_url += path

            return clean_url
        except Exception:
            # Fallback: basic cleaning
            try:
                return (
                    re.sub(r"^git@([^:]+):", r"https://\1/", url)
                    .replace(".git", "")
                    .rstrip("/")
                )
            except Exception:
                return url

    def _clean_azure_devops_url(self, url: str) -> str:
        """Clean Azure DevOps repository URL by removing credentials
        Converts: https://user@dev.azure.com/org/Project/_git/Repo
        To: https://dev.azure.com/org/Project/_git/Repo
        """
        if not url:
            return ""

        try:
            parsed = urlparse(url)
            # Remove credentials by rebuilding URL without them
            clean_url = f"{parsed.scheme}://{parsed.hostname}"
            if parsed.port:
                clean_url += f":{parsed.port}"
            clean_url += parsed.path
            if parsed.query:
                clean_url += f"?{parsed.query}"
            return clean_url
        except Exception:
            # Fallback: remove credentials only
            try:
                return re.sub(r"//[^@]+@", "//", url)
            except Exception:
                return url

    async def _fetch_github_user_info(self, username: str) -> Optional[dict]:
        """Fetch GitHub user info using the public Users API
        This works for both public and private repos since it only queries user data
        """
        try:
            url = f"https://api.github.com/users/{username}"

            if is_verbose_mode() or os.getenv("LOG_LEVEL") == "debug":
                print(f"🔍 Fetching user info from GitHub API: {url}")

            async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
                response = await client.get(
                    url,
                    headers={
                        "Accept": "application/vnd.github.v3+json",
                        "User-Agent": f"testdino/{VERSION}",
                    },
                )

                if response.is_success:
                    data = response.json()
                    result = {}
                    if data.get("login"):
                        result["login"] = data["login"]
                    if data.get("id"):
                        result["id"] = str(data["id"])
                    return result if result else None
                return None
        except Exception:
            return None

    async def _fetch_github_branch_commit(
        self, repository: str, branch: str
    ) -> Optional[dict]:
        """Fetch the HEAD commit information from a specific branch
        This avoids merge commit messages in PR scenarios
        """
        try:
            url = f"https://api.github.com/repos/{repository}/commits/{branch}"

            if os.getenv("LOG_LEVEL") == "debug":
                print(f"🔍 Fetching branch HEAD commit from GitHub API: {url}")

            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"testdino/{VERSION}",
            }
            # If GITHUB_TOKEN is available, use it for higher rate limits
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"

            async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
                response = await client.get(url, headers=headers)

                if response.is_success:
                    data = response.json()
                    sha = data.get("sha")
                    message = data.get("commit", {}).get("message")
                    email = data.get("commit", {}).get("author", {}).get("email")
                    author_login = data.get("author", {}).get("login") if data.get("author") else None
                    author_id = str(data["author"]["id"]) if data.get("author", {}).get("id") else None

                    if sha and message:
                        result = {
                            "sha": sha,
                            "message": message,
                            "email": email or "",
                        }
                        if author_login:
                            result["author"] = author_login
                        if author_id:
                            result["authorId"] = author_id
                        return result
                return None
        except Exception as error:
            if os.getenv("LOG_LEVEL") == "debug":
                print(f"❌ Error fetching GitHub branch commit: {error}")
            return None

    async def _fetch_github_pull_request_details(
        self, repository: str, pr_id: str
    ) -> Optional[dict]:
        """Fetch pull request details from GitHub API to get PR title and status"""
        try:
            url = f"https://api.github.com/repos/{repository}/pulls/{pr_id}"

            if os.getenv("LOG_LEVEL") == "debug":
                print(f"🔍 Fetching PR details from GitHub API: {url}")

            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"testdino/{VERSION}",
            }
            # If GITHUB_TOKEN is available, use it for higher rate limits
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"

            async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
                response = await client.get(url, headers=headers)

                if response.is_success:
                    data = response.json()
                    title = data.get("title")
                    state = data.get("state")
                    draft = data.get("draft")

                    # Determine PR status
                    status = ""
                    if draft:
                        status = "draft"
                    elif state == "open":
                        status = "open"
                    elif state == "closed":
                        status = "closed"
                    elif state == "merged":
                        status = "merged"

                    if os.getenv("LOG_LEVEL") == "debug":
                        print(f"✅ Successfully fetched PR details - Title: {title}, Status: {status}")

                    if title:
                        return {"title": title, "status": status}
                return None
        except Exception as error:
            if os.getenv("LOG_LEVEL") == "debug":
                print(f"❌ Error fetching GitHub PR details: {error}")
            return None
