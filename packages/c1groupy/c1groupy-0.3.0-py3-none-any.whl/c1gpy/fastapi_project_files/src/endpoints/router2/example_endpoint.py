"""Example endpoint for router2."""


async def get_status() -> dict:
    """
    Example async endpoint function.

    Returns:
        dict: Status information
    """
    return {"status": "healthy", "service": "router2"}


async def process_data(data: dict) -> dict:
    """
    Example async data processing endpoint.

    Args:
        data: Input data to process

    Returns:
        dict: Processed result
    """
    return {"processed": True, "input": data, "result": "processed successfully"}
