"""FastAPI dependencies for Cognito authentication."""
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from .cognito_auth import CognitoAuth

bearer_scheme = HTTPBearer(auto_error=True)

# Global instance (initialized once at startup)
_cognito_auth: Optional[CognitoAuth] = None


def get_cognito_auth() -> CognitoAuth:
    """Get or initialize global CognitoAuth instance.

    Returns:
        CognitoAuth instance configured from environment variables.
    """
    global _cognito_auth
    if _cognito_auth is None:
        _cognito_auth = CognitoAuth()
    return _cognito_auth


def get_token_from_request(request: Request) -> str:
    """Extract JWT token from request.

    Checks (in order):
    1. Authorization header (Bearer token)
    2. Cookie (cognito_token)

    Args:
        request: FastAPI Request object

    Returns:
        JWT token string

    Raises:
        HTTPException: If no token found
    """
    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")

    # Check cookies
    token = request.cookies.get("cognito_token")
    if token:
        return token

    raise HTTPException(
        status_code=401,
        detail="Not authenticated - no token provided"
    )


def get_cognito_user_swagger(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    cognito: CognitoAuth = Depends(get_cognito_auth)
) -> Dict[str, Any]:
    """FastAPI dependency for Swagger UI authentication.

    This dependency uses HTTPBearer which integrates with Swagger UI's
    "Authorize" button for testing authenticated endpoints.

    Args:
        credentials: HTTP Bearer credentials from Swagger
        cognito: CognitoAuth instance

    Returns:
        Dict containing user information

    Raises:
        HTTPException: If token is invalid or expired

    Example:
        >>> @router.get('/protected')
        ... async def protected_route(user: Dict = Depends(get_cognito_user_swagger)):
        ...     return {"email": user["email"]}
    """
    token = credentials.credentials
    try:
        return cognito.validate_token(token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")


def get_cognito_user(
    token: str = Depends(get_token_from_request),
    cognito: CognitoAuth = Depends(get_cognito_auth)
) -> Dict[str, Any]:
    """FastAPI dependency to get authenticated user from JWT token.

    This dependency extracts tokens from both Authorization header
    and cookies, making it suitable for both API and web clients.

    Args:
        token: JWT token from request
        cognito: CognitoAuth instance

    Returns:
        Dict containing user information

    Raises:
        HTTPException: If token is invalid or expired

    Example:
        >>> @router.get('/me')
        ... async def get_me(user: Dict = Depends(get_cognito_user)):
        ...     return {"email": user["email"], "name": user["name"]}
    """
    try:
        user = cognito.validate_token(token)
        return user
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired token: {e}"
        )


def require_groups(*required_groups: str):
    """Create a dependency that requires user to be in specific groups.

    Args:
        *required_groups: Group names the user must belong to (at least one)

    Returns:
        FastAPI Depends object

    Example:
        >>> @router.post('/admin/action')
        ... async def admin_action(
        ...     user: Dict = Depends(require_groups("SuperAdmin", "AdminGroup"))
        ... ):
        ...     return {"message": "Admin action performed"}
    """
    def check_groups(user: Dict = Depends(get_cognito_user)) -> Dict:
        user_groups = set(user.get("cognito:groups", []))
        required = set(required_groups)

        if not user_groups.intersection(required):
            raise HTTPException(
                status_code=403,
                detail=f"User must be in one of these groups: {', '.join(required_groups)}"
            )

        return user

    return Depends(check_groups)
