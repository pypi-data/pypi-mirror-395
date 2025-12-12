"""Router2 - Example API routes."""

from fastapi import APIRouter  # , Security
# from fastapi.security import APIKeyHeader

from endpoints.router2 import example_endpoint

router = APIRouter(prefix="/router2", tags=["router2"])

# Uncomment to enable API key authentication
# api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@router.get("/status")
async def get_status() -> dict:
    """
    Get service status.

    Returns:
        dict: Status information
    """
    return await example_endpoint.get_status()


@router.post("/process")
async def process_data(data: dict) -> dict:
    """
    Process input data.

    Args:
        data: Data to process

    Returns:
        dict: Processing result
    """
    return await example_endpoint.process_data(data)
