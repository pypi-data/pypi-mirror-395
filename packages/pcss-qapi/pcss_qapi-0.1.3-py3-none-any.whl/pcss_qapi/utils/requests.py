"""Requests utils"""
from requests import Response


def raise_for_common(response: Response, default_raises_generic: bool = True) -> bool:
    """
    Common boilerplate for handling api response codes

    Args:
        response (Response): api response
        default_raises_generic (bool, optional): Whether to raise a generic error for unmatched codes. Defaults to True.

    Raises:
        RuntimeError: one of specified errors

    Returns:
        bool: Whether the response status was 200
    """
    if response.ok:
        return True

    match response.status_code:
        case 401:
            raise RuntimeError("Unauthorized. Use AuthorizationService.login() first.")
        case 403:
            raise RuntimeError("Your account is not authorized to use the api at this moment.")
        case _:
            if default_raises_generic:
                raise RuntimeError(f"Error reaching server ({response.status_code}).")

    return False
