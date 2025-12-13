"""
Audit Trail Logging Module

Provides async functions for logging audit trails and system errors to MongoDB.
"""

import json
import sys
from typing import Optional

from inception_audittrail_logger.format_data import (
    format_audittrail_data,
    format_sys_error_data,
)
from inception_audittrail_logger.audittrail_mongo import insert_document


async def log_audittrail(
    data: dict,
    user: dict,
    correlation_id: str,
    user_agent_str: str,
    ip_address: str,
) -> Optional[bool]:
    """
    Asynchronously format and log audit trail data to MongoDB.

    Args:
        data: The audit trail data to log.
        user: User information associated with the action.
        correlation_id: Unique identifier for request tracing.
        user_agent_str: User agent string from the request.
        ip_address: IP address of the client.

    Returns:
        Result of the insert operation, or None if an error occurred.
    """
    try:
        formatted_data = await format_audittrail_data(
            data, user, correlation_id, user_agent_str, ip_address
        )
        return await insert_document(formatted_data)
    except Exception as e:
        print(f"[ERROR] Unable to log audit trail: {e}", file=sys.stderr)
        return None


async def log_sys_error(
    data: dict,
    user: dict,
    correlation_id: str,
    user_agent_str: str,
    ip_address: str,
) -> Optional[bool]:
    """
    Asynchronously format and log system error data to MongoDB.

    Args:
        data: The error data to log.
        user: User information associated with the error.
        correlation_id: Unique identifier for request tracing.
        user_agent_str: User agent string from the request.
        ip_address: IP address of the client.

    Returns:
        Result of the insert operation, or None if an error occurred.
    """
    try:
        formatted_data = await format_sys_error_data(
            data, user, correlation_id, user_agent_str, ip_address
        )
        return await insert_document(formatted_data)
    except Exception as e:
        print(f"[ERROR] System error logging failed: {e}", file=sys.stderr)
        return None


def get_changed_fields(old_data: dict, new_data: dict) -> str:
    """
    Compare two dictionaries and return JSON string of changed fields.

    Args:
        old_data: The original data dictionary.
        new_data: The updated data dictionary.

    Returns:
        JSON string containing list of changed fields with old and new values.
    """
    changed_fields = [
        {
            "field": key,
            "old_value": old_data.get(key),
            "new_value": value,
        }
        for key, value in new_data.items()
        if old_data.get(key) != value
    ]
    return json.dumps(changed_fields, indent=4)
