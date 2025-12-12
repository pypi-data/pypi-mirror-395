"""
salesforce tool for querying leads via a2a.

provides mcp tool endpoint for querying salesforce data
by sending tasks to a salesforce agent.
"""

import logging
from typing import Dict, Any, List

from synqed import AgentId
from synqed_mcp.a2a.client import A2AClient

logger = logging.getLogger(__name__)


async def query_leads(
    a2a_client: A2AClient,
    query: str
) -> Dict[str, Any]:
    """
    query salesforce leads via a2a.
    
    sends a query task to the salesforce agent and returns
    the results as a structured response.
    
    args:
        a2a_client: a2a client for sending tasks
        query: soql query string (e.g., "SELECT Id, Name FROM Lead WHERE Status='New'")
        
    returns:
        dictionary containing:
        - results: array of lead records
        - count: number of results
        - query: original query
        
    example:
        ```python
        results = await query_leads(
            client,
            "SELECT Id, Name, Email FROM Lead LIMIT 10"
        )
        print(f"Found {results['count']} leads")
        ```
    """
    logger.info(f"querying salesforce leads: {query[:100]}...")
    
    # resolve salesforce agent
    agent = AgentId.from_email_like("salesforce@tools")
    
    # prepare task payload
    payload = {
        "query": query,
        "format": "json"
    }
    
    try:
        # send task via a2a
        response = await a2a_client.send_task(
            agent=agent,
            task_type="query_leads",
            payload=payload
        )
        
        logger.info(f"received response from salesforce agent: {response.get('status')}")
        
        # parse response
        # in real implementation, this would parse actual salesforce response
        return {
            "results": response.get("data", []),
            "count": len(response.get("data", [])),
            "query": query,
            "status": response.get("status", "success")
        }
        
    except Exception as e:
        logger.error(f"failed to query salesforce: {e}")
        return {
            "results": [],
            "count": 0,
            "query": query,
            "status": "error",
            "error": str(e)
        }


# tool schema for mcp registration
TOOL_SCHEMA = {
    "name": "salesforce_query_leads",
    "description": (
        "Query Salesforce leads using SOQL. "
        "Returns lead records matching the query criteria. "
        "Use standard Salesforce Object Query Language (SOQL) syntax."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "SOQL query string (e.g., 'SELECT Id, Name FROM Lead WHERE Status=\"New\"')"
            }
        },
        "required": ["query"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "description": "Array of lead records"
            },
            "count": {
                "type": "integer",
                "description": "Number of results returned"
            },
            "query": {
                "type": "string",
                "description": "Original query"
            },
            "status": {
                "type": "string",
                "description": "Query execution status"
            }
        }
    }
}

