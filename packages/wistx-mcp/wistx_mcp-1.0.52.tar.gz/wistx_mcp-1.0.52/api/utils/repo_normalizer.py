"""Repository URL normalization utilities."""


def normalize_repo_url(url: str) -> str:
    """Normalize GitHub URLs for comparison.
    
    Examples:
        https://github.com/owner/repo.git -> https://github.com/owner/repo
        http://github.com/owner/repo -> https://github.com/owner/repo
        owner/repo -> https://github.com/owner/repo
    
    Args:
        url: Repository URL to normalize
        
    Returns:
        Normalized URL string
    """
    if not url:
        return ""
    
    url = url.strip().rstrip("/").replace(".git", "")
    
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    
    return url.lower()

