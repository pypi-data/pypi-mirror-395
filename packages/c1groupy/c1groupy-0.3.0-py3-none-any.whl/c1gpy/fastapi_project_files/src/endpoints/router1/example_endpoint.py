"""Example endpoint for router1."""


async def get_example_data() -> dict:
    """
    Example async endpoint function.

    Returns:
        dict: Example data
    """
    return {"message": "Hello from router1", "status": "success"}


async def create_example_item(item_data: dict) -> dict:
    """
    Example async POST endpoint function.

    Args:
        item_data: Data for the new item

    Returns:
        dict: Created item with ID
    """
    return {"id": 1, "data": item_data, "status": "created"}
