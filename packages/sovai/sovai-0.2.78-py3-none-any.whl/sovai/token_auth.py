from typing import Optional
from sovai.api_config import ApiConfig, save_key
# Removed verify_token import from top level
from sovai.errors.sovai_errors import InvalidCredentialsError

# Valid version values
VALID_VERSIONS = ["p72", "sovai"]


def token_auth(token: str, version: Optional[str] = None):
    """
    Authenticates using a token, saves it, and verifies it.
    
    Args:
        token: API authentication token
        version: Optional version parameter for column exclusions (e.g., 'p72', 'sovai')
    
    Raises:
        InvalidCredentialsError: If token is invalid or expired
        ValueError: If version is provided but not in the list of valid versions
    """
    # Validate version if provided
    if version is not None and version not in VALID_VERSIONS:
        raise ValueError(
            f"Invalid version '{version}'. Must be one of: {', '.join(VALID_VERSIONS)}"
        )

    # Lazy load verify_token here, just before use
    from sovai.utils.client_side import verify_token

    ApiConfig.token = token
    ApiConfig.token_type = "Bearer"
    ApiConfig.version = version
    
    save_key() # Assumes save_key doesn't trigger heavy imports

    # Now call the imported function
    is_valid, user_id = verify_token(verbose=False) # Uses lazy-loaded verify_token

    if not is_valid:
        # print('invalid') # Keep commented or use logging
        raise InvalidCredentialsError("Invalid or expired token. Please authenticate.")

    # Optionally, you could return something useful, like the validity or user_id
    # print(f"Token verified successfully for user ID: {user_id}") # Or use logging
    # return is_valid, user_id
