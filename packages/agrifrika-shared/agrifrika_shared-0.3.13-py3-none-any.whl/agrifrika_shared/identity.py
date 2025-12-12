"""
Identity helpers shared across Agrifrika services.
"""

from typing import Optional, Dict, Any, List
from agrifrika_shared.utils.logger import get_logger
from botocore.exceptions import ClientError
from agrifrika_shared.aws import get_cognito_client
import os
import secrets
import string


logger = get_logger(__name__)

_REGION = os.environ.get('REGION', 'us-east-1')
_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
_DEFAULT_COUNTRY_CODE = os.environ.get('DEFAULT_COUNTRY_CODE', '+237')


def _get_cognito_client():
    return get_cognito_client(region_name=_REGION)


def generate_temporary_password(length: int = 12) -> str:
    """
    Generate a secure temporary password that satisfies Cognito requirements.
    """
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]

    all_chars = lowercase + uppercase + digits + special
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


def create_cognito_user(
    *,
    username: str,
    email: str,
    temp_password: str,
    phone: Optional[str] = None,
    user_pool_id: Optional[str] = None,
    user_type: Optional[str] = None,
    given_name: Optional[str] = None,
    family_name: Optional[str] = None,
    additional_attributes: Optional[Dict[str, str]] = None,
    lookup_existing: bool = True,
    default_country_code: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Create (or update) a Cognito user with a temporary password.
    """
    pool_id = user_pool_id or _USER_POOL_ID
    if not pool_id:
        raise ValueError("COGNITO_USER_POOL_ID is not configured")

    client = _get_cognito_client()
    normalized_phone = _normalize_phone_number(
        phone,
        default_country_code or _DEFAULT_COUNTRY_CODE
    )

    resolved_given_name = given_name or email.split('@')[0]
    user_attributes = [
        {'Name': 'email', 'Value': email},
        {'Name': 'email_verified', 'Value': 'true'},
        {'Name': 'given_name', 'Value': resolved_given_name},
    ]

    if family_name:
        user_attributes.append({'Name': 'family_name', 'Value': family_name})

    if normalized_phone:
        user_attributes.append({'Name': 'phone_number', 'Value': normalized_phone})

    if user_type:
        user_attributes.append({'Name': 'custom:user_type', 'Value': user_type})

    if additional_attributes:
        for attr_name, attr_value in additional_attributes.items():
            normalized_name = attr_name if attr_name.startswith('custom:') else attr_name
            user_attributes.append({'Name': normalized_name, 'Value': attr_value})

    try:
        response = client.admin_create_user(
            UserPoolId=pool_id,
            Username=username,
            UserAttributes=user_attributes,
            TemporaryPassword=temp_password,
            ForceAliasCreation=False,
            MessageAction='SUPPRESS',
            DesiredDeliveryMediums=['EMAIL']
        )
        return response['User']

    except ClientError as error:
        error_code = error.response['Error']['Code']

        if error_code == 'UsernameExistsException' and lookup_existing:
            return _handle_existing_user(
                client=client,
                pool_id=pool_id,
                email=email,
                temp_password=temp_password,
                given_name=resolved_given_name,
                family_name=family_name,
                user_attributes=user_attributes
            )

        logger.error(
            "cognito_user_creation_failed",
            error_code=error_code,
            error=str(error)
        )
        return None

    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "unexpected_cognito_error",
            error=str(exc),
            exc_info=True
        )
        return None


def _handle_existing_user(
    *,
    client,
    pool_id: str,
    email: str,
    temp_password: str,
    given_name: str,
    family_name: Optional[str],
    user_attributes: Optional[List[Dict[str, str]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Update an existing Cognito user (matched by alias email) with the latest attributes.
    """
    try:
        existing_user = client.admin_get_user(
            UserPoolId=pool_id,
            Username=email
        )

        update_attributes = [
            {'Name': 'given_name', 'Value': given_name},
        ]

        if family_name:
            update_attributes.append({'Name': 'family_name', 'Value': family_name})

        if user_attributes:
            for attr in user_attributes:
                if attr['Name'] not in {'email', 'email_verified', 'given_name', 'family_name'}:
                    update_attributes.append(attr)

        client.admin_update_user_attributes(
            UserPoolId=pool_id,
            Username=email,
            UserAttributes=update_attributes
        )

        client.admin_set_user_password(
            UserPoolId=pool_id,
            Username=email,
            Password=temp_password,
            Permanent=False
        )

        return {
            'Username': existing_user['Username'],
            'UserStatus': 'FORCE_CHANGE_PASSWORD'
        }

    except client.exceptions.UserNotFoundException:
        logger.warning("username_exists_different_email", username=email)
        return None

    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "error_updating_existing_cognito_user",
            error=str(exc),
            exc_info=True
        )
        return None


def _normalize_phone_number(phone: Optional[str], default_country_code: str) -> Optional[str]:
    """Simple helper to normalize phone numbers into E.164 format."""
    if not phone:
        return None

    cleaned = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')
    if cleaned.startswith('+'):
        return cleaned

    digits = ''.join(ch for ch in cleaned if ch.isdigit())
    return f"{default_country_code}{digits}" if digits else None
