"""
PIC permission policy.

Currently identical to upstream "generic".
"""
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from rucio.common.types import InternalAccount
    from sqlalchemy.orm import Session


def has_permission(issuer: "InternalAccount", action: str, kwargs: dict[str, Any], *, session: "Optional[Session]" = None) -> Union[bool, None]:
    """
    Checks if an account has the specified permission to
    execute an action with parameters.

    :param issuer: Account identifier which issues the command..
    :param action:  The action(API call) called by the account.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    # always returning None means to use the default permission policy for any action
    return None
