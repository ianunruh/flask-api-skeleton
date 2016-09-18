from backend.registry import Registry

from .facebook import FacebookProvider
from .github import GitHubProvider
from .google import GoogleProvider

social_provider_registry = Registry()
social_provider_registry.register(FacebookProvider, GitHubProvider, GoogleProvider)
