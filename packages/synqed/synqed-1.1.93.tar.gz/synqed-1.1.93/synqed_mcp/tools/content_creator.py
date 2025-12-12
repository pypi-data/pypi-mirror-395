"""
content creator tool for generating content via a2a.

provides mcp tool endpoint for generating content
by sending tasks to a content creator agent.
"""

import logging
from typing import Dict, Any, Optional

from synqed import AgentId
from synqed_mcp.a2a.client import A2AClient

logger = logging.getLogger(__name__)


async def generate_content(
    a2a_client: A2AClient,
    prompt: str,
    tone: Optional[str] = "professional",
    format: Optional[str] = "markdown",
    max_length: Optional[int] = 1000
) -> Dict[str, Any]:
    """
    generate content via a2a.
    
    sends a content generation task to the content creator agent
    and returns the generated content.
    
    args:
        a2a_client: a2a client for sending tasks
        prompt: content generation prompt/instructions
        tone: desired tone (e.g., "professional", "casual", "technical", "creative")
        format: output format (e.g., "markdown", "html", "plain")
        max_length: maximum content length in characters
        
    returns:
        dictionary containing:
        - content: generated content text
        - prompt: original prompt
        - tone: applied tone
        - format: output format
        - word_count: approximate word count
        
    example:
        ```python
        result = await generate_content(
            client,
            prompt="Write a blog post about the future of AI",
            tone="informative",
            format="markdown",
            max_length=2000
        )
        print(result['content'])
        ```
    """
    logger.info(f"generating content: prompt='{prompt[:50]}...', tone={tone}")
    
    # resolve content creator agent
    agent = AgentId.from_email_like("content_creator@tools")
    
    # prepare task payload
    payload = {
        "prompt": prompt,
        "tone": tone,
        "format": format,
        "max_length": max_length,
        "temperature": 0.7,  # default creativity setting
    }
    
    try:
        # send task via a2a
        response = await a2a_client.send_task(
            agent=agent,
            task_type="generate_content",
            payload=payload
        )
        
        logger.info(f"content generated: {response.get('status')}")
        
        # parse response
        content = response.get("content", "")
        word_count = len(content.split()) if content else 0
        
        return {
            "content": content,
            "prompt": prompt,
            "tone": tone,
            "format": format,
            "word_count": word_count,
            "status": response.get("status", "success")
        }
        
    except Exception as e:
        logger.error(f"failed to generate content: {e}")
        return {
            "content": "",
            "prompt": prompt,
            "tone": tone,
            "format": format,
            "word_count": 0,
            "status": "error",
            "error": str(e)
        }


# tool schema for mcp registration
TOOL_SCHEMA = {
    "name": "content_creator_generate",
    "description": (
        "Generate content based on a prompt. "
        "Supports various tones and output formats. "
        "Returns generated content with metadata."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Content generation prompt/instructions"
            },
            "tone": {
                "type": "string",
                "description": "Desired tone (e.g., 'professional', 'casual', 'technical', 'creative')",
                "default": "professional"
            },
            "format": {
                "type": "string",
                "description": "Output format (e.g., 'markdown', 'html', 'plain')",
                "default": "markdown"
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum content length in characters",
                "default": 1000
            }
        },
        "required": ["prompt"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Generated content text"
            },
            "prompt": {
                "type": "string",
                "description": "Original prompt"
            },
            "tone": {
                "type": "string",
                "description": "Applied tone"
            },
            "format": {
                "type": "string",
                "description": "Output format"
            },
            "word_count": {
                "type": "integer",
                "description": "Approximate word count"
            },
            "status": {
                "type": "string",
                "description": "Generation status"
            }
        }
    }
}

