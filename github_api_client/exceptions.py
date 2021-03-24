class GitHubClientError(Exception):
    """Base exception class for errors thrown by the GitHub API Client"""
    pass


class UnsupportedResponseStatus(GitHubClientError):
    """Received unexpected status code"""
    pass
