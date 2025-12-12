"""
zoom tool for creating meetings via a2a.

provides mcp tool endpoint for creating zoom meetings
by sending tasks to a zoom agent.
"""

import logging
from typing import Dict, Any, Optional

from synqed import AgentId
from synqed_mcp.a2a.client import A2AClient

logger = logging.getLogger(__name__)


async def create_meeting(
    a2a_client: A2AClient,
    topic: str,
    start_time: str,
    duration: Optional[int] = 60,
    agenda: Optional[str] = None
) -> Dict[str, Any]:
    """
    create a zoom meeting via a2a.
    
    sends a meeting creation task to the zoom agent and returns
    the meeting details including join url.
    
    args:
        a2a_client: a2a client for sending tasks
        topic: meeting topic/title
        start_time: meeting start time in iso 8601 format (e.g., "2025-11-23T10:00:00Z")
        duration: meeting duration in minutes (default: 60)
        agenda: optional meeting agenda/description
        
    returns:
        dictionary containing:
        - join_url: zoom meeting join url
        - meeting_id: unique meeting identifier
        - password: meeting password (if applicable)
        - start_time: scheduled start time
        - topic: meeting topic
        
    example:
        ```python
        meeting = await create_meeting(
            client,
            topic="Product Roadmap Review",
            start_time="2025-11-25T14:00:00Z",
            duration=90,
            agenda="Discuss Q1 2026 features"
        )
        print(f"Join URL: {meeting['join_url']}")
        ```
    """
    logger.info(f"creating zoom meeting: {topic} at {start_time}")
    
    # resolve zoom agent
    agent = AgentId.from_email_like("zoom@tools")
    
    # prepare task payload
    payload = {
        "topic": topic,
        "start_time": start_time,
        "duration": duration,
        "type": 2,  # scheduled meeting
        "settings": {
            "join_before_host": True,
            "mute_upon_entry": False,
            "waiting_room": False
        }
    }
    
    if agenda:
        payload["agenda"] = agenda
    
    try:
        # send task via a2a
        response = await a2a_client.send_task(
            agent=agent,
            task_type="create_meeting",
            payload=payload
        )
        
        logger.info(f"zoom meeting created: {response.get('status')}")
        
        # parse response
        # in real implementation, this would parse actual zoom api response
        return {
            "join_url": response.get("join_url", "https://zoom.us/j/mock-meeting-id"),
            "meeting_id": response.get("meeting_id", "mock-123456789"),
            "password": response.get("password", ""),
            "start_time": start_time,
            "topic": topic,
            "duration": duration,
            "status": response.get("status", "success")
        }
        
    except Exception as e:
        logger.error(f"failed to create zoom meeting: {e}")
        return {
            "join_url": "",
            "meeting_id": "",
            "password": "",
            "start_time": start_time,
            "topic": topic,
            "status": "error",
            "error": str(e)
        }


# tool schema for mcp registration
TOOL_SCHEMA = {
    "name": "zoom_create_meeting",
    "description": (
        "Create a scheduled Zoom meeting. "
        "Returns meeting details including join URL, meeting ID, and password."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Meeting topic/title"
            },
            "start_time": {
                "type": "string",
                "description": "Meeting start time in ISO 8601 format (e.g., '2025-11-23T10:00:00Z')"
            },
            "duration": {
                "type": "integer",
                "description": "Meeting duration in minutes (default: 60)",
                "default": 60
            },
            "agenda": {
                "type": "string",
                "description": "Optional meeting agenda/description"
            }
        },
        "required": ["topic", "start_time"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "join_url": {
                "type": "string",
                "description": "Zoom meeting join URL"
            },
            "meeting_id": {
                "type": "string",
                "description": "Unique meeting identifier"
            },
            "password": {
                "type": "string",
                "description": "Meeting password (if applicable)"
            },
            "start_time": {
                "type": "string",
                "description": "Scheduled start time"
            },
            "topic": {
                "type": "string",
                "description": "Meeting topic"
            },
            "status": {
                "type": "string",
                "description": "Creation status"
            }
        }
    }
}

