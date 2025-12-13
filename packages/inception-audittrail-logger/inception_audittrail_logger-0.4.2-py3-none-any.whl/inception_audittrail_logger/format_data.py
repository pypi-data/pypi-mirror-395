from user_agents import parse
from datetime import datetime
import uuid
import requests
import asyncio


async def format_audittrail_data(
    data: dict, user: dict, correlation_id: str, user_agent_str: str, ip_address: str
):
    """
    Format audit trail data for MongoDB and Elasticsearch.
    """
    id = f"{user['owner_id']}-{user['account_num']}-{str(uuid.uuid4())}"
    document = {
        "_id": id,
        "id": id,
        "references": data.get("references"),
        "object_description": data.get("object_description"),
        "action": data.get("action"),
        "action_description": data.get("action_description"),
        "user_full_name": user.get("full_name"),
        "user_account_num": user.get("account_num"),
        "user_email": user.get("email"),
        "user_photo": user.get("photo"),
        "owner_id": user.get("owner_id"),
        "owner_full_name": user.get("company_name", ""),
        "owner_email": user.get("owner_email", ""),
        "owner_photo": user.get(
            "owner_photo",
            {
                "id": "",
                "key": "",
                "filename": "",
                "unique_filename": "",
                "url": "",
                "content_type": "",
                "extension": "",
                "size": "100KB",
                "thumbnail_url": "",
                "thumbnail_key": "",
                "thumbnail_filename": "",
            },
        ),
        "content": data.get("content"),
        "timezone": "Africa/Accra",
        "timeformat": "24",
        "created_at_iso": datetime.now().isoformat(),
        "created_at_formatted": datetime.now().strftime("%H:%M - %B %d, %Y"),
        "created_at_epoch": int(datetime.now().timestamp()),
        "created_at_12hour_format": datetime.now().strftime("%I:%M %p"),
        "created_at_24hour_format": datetime.now().strftime("%H:%M"),
        "main_entity": data.get("main_entity"),
        "sub_entity": data.get("sub_entity"),
        "correlation_id": correlation_id,
        "ip_address": ip_address,
        "user_agent": user_agent_str,
        **await get_user_agent_detailed_info(user_agent_str, ip_address),
        "status": "success",
        "module": data.get("module"),
        "environment": data.get("environment"),
        "application_version": data.get("application_version"),
        "additional_context": {
            "changed_field": data.get("changed_field", ""),
            "notes": data.get("notes"),
            "endpoint": data.get("endpoint"),
        },
    }

    return document


async def format_sys_error_data(
    data: dict, user: dict, correlation_id: str, user_agent_str: str, ip_address: str
):
    """
    Format system error data for MongoDB and Elasticsearch.
    """
    id = f"{user['owner_id']}-{user['account_num']}-{str(uuid.uuid4())}"
    document = {
        "_id": id,
        "id": id,
        "user_full_name": user.get("full_name"),
        "user_account_num": user.get("account_num"),
        "user_email": user.get("email"),
        "user_photo": user.get("photo"),
        "owner_id": user.get("owner_id"),
        "owner_full_name": user.get("owner").get("company_name", ""),
        "owner_email": user.get("owner").get("email", ""),
        "owner_photo": user.get("owner").get("photo",{
                "id": "",
                "key": "",
                "filename": "",
                "unique_filename": "",
                "url": "",
                "content_type": "",
                "extension": "",
                "size": "100KB",
                "thumbnail_url": "",
                "thumbnail_key": "",
                "thumbnail_filename": "",
            }),
        "message": data.get("error_message"),
        "timezone": "Africa/Accra",
        "timeformat": "24",
        "created_at_iso": datetime.now().isoformat(),
        "created_at_formatted": datetime.now().strftime("%H:%M - %B %d, %Y"),
        "created_at_epoch": int(datetime.now().timestamp()),
        "created_at_12hour_format": datetime.now().strftime("%I:%M %p"),
        "created_at_24hour_format": datetime.now().strftime("%H:%M"),
        "main_entity": data.get("main_entity"),
        "sub_entity": data.get("sub_entity"),
        "correlation_id": correlation_id,
        "ip_address": ip_address,
        "user_agent": user_agent_str,
        **await get_user_agent_detailed_info(user_agent_str, ip_address),
        "module": data.get("module"),
        "environment": data.get("environment"),
        "application_version": data.get("application_version"),
        "icon_name": data.get("icon_name", ""),
        "additional_context": {
            "error_message": data.get("error_message"),
            "error_traceback": data.get("error_traceback"),
            "error_type": data.get("error_type"),
            "error_file": data.get("error_file"),
            "error_function": data.get("error_function"),
            "error_endpoint": data.get("error_endpoint"),
            "error_status_code": data.get("error_status_code"),
        },
    }

    return document


async def get_user_agent_detailed_info(user_agent_str: str, ip_address: str):
    user_agent = parse(user_agent_str)

    return {
        "location": await get_geolocation(ip_address),
        "device": {
            "family": user_agent.device.family,
            "model": user_agent.device.model,
        },
        "browser": {
            "family": user_agent.browser.family,
            "version": user_agent.browser.version_string,
        },
        "os": {
            "family": user_agent.os.family,
            "version": user_agent.os.version_string,
        },
    }


async def get_geolocation(ip: str):
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: requests.get(f"http://ip-api.com/json/{ip}")
        )
        return response.json()
    except Exception:
        return {}
