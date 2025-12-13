"""
RAFAEL Framework Version Information
"""

__version__ = "1.1.0"
__version_info__ = (1, 1, 0)

# Release information
__release_date__ = "2025-12-07"
__release_name__ = "Adaptive Evolution"

# Build information
__build__ = "stable"
__status__ = "Production"

# Feature flags for this version
FEATURES = {
    "chaos_testing": True,
    "adaptive_genome": True,
    "resilience_vault": True,
    "guardian_layer": True,
    "real_time_dashboard": True,
    "api_endpoints": True,
    "ssl_secured": True,
    "bilingual_support": True,
}

# Version history
VERSION_HISTORY = {
    "1.1.0": {
        "date": "2025-12-07",
        "changes": [
            "Fixed chaos testing in demo page",
            "Fixed API vault/patterns endpoint",
            "Added comprehensive testing suite (19/19 passing)",
            "Updated README with live URLs and badges",
            "Added social media content strategy",
            "Improved error handling in dashboard",
            "Enhanced security with SSL on all domains",
            "Added bilingual support (EN/ID)",
        ],
        "breaking_changes": [],
        "deprecations": [],
    },
    "1.0.0": {
        "date": "2025-12-06",
        "changes": [
            "Initial production release",
            "Core RAFAEL engine with ARG",
            "Chaos Forge for attack simulation",
            "Resilience Vault for pattern storage",
            "Guardian Layer for compliance",
            "Web dashboard for monitoring",
            "REST API for integration",
            "Interactive demo page",
        ],
        "breaking_changes": [],
        "deprecations": [],
    },
}

def get_version():
    """Get the current version string"""
    return __version__

def get_version_info():
    """Get the version as a tuple"""
    return __version_info__

def get_release_info():
    """Get full release information"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "release_date": __release_date__,
        "release_name": __release_name__,
        "build": __build__,
        "status": __status__,
        "features": FEATURES,
    }
