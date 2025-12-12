"""Router1 - Example API routes."""

from fastapi import APIRouter  # , Security
# from fastapi.security import APIKeyHeader

from endpoints.router1 import example_endpoint

router = APIRouter(prefix="/router1", tags=["router1"])

# Uncomment to enable API key authentication
# api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@router.get("/example")
async def get_example() -> dict:
    """
    Get example data.

    Returns:
        dict: Example response
    """
    return await example_endpoint.get_example_data()


@router.post("/items")
async def create_item(item_data: dict) -> dict:
    """
    Create a new item.

    Args:
        item_data: Item data to create

    Returns:
        dict: Created item
    """
    return await example_endpoint.create_example_item(item_data)


# Example with API key security (commented out)
# @router.get("/secure")
# async def secure_endpoint(api_key: str = Security(api_key_header)):
#     """
#     Secure endpoint requiring API key.
#
#     Args:
#         api_key: API key from header
#
#     Returns:
#         dict: Secure data
#     """
#     if api_key != "your-secret-key":
#         raise HTTPException(status_code=403, detail="Invalid API key")
#     return {"message": "Access granted", "secure_data": "sensitive information"}
