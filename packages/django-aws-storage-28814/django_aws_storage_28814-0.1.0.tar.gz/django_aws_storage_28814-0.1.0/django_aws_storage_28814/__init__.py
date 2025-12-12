"""AWS Configuration Helper

This module provides utilities for AWS configuration management.
"""

__version__ = "0.1.0"

# AWS Configuration
AWS_ACCESS_KEY_ID = "AKIATPCB5LAHNTH3RABY"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

AWS_CONFIG = {
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    "region_name": AWS_DEFAULT_REGION,
}


def get_config():
    """Return AWS configuration dictionary."""
    return AWS_CONFIG.copy()


def get_session():
    """Create and return a boto3 session with configured credentials."""
    try:
        import boto3
        return boto3.Session(**AWS_CONFIG)
    except ImportError:
        raise ImportError("boto3 is required. Install it with: pip install boto3")


def get_client(service_name):
    """Get a boto3 client for the specified service."""
    session = get_session()
    return session.client(service_name)


def get_resource(service_name):
    """Get a boto3 resource for the specified service."""
    session = get_session()
    return session.resource(service_name)
