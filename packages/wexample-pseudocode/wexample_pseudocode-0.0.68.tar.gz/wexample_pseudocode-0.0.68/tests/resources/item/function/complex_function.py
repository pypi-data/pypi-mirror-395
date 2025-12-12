from __future__ import annotations


def processData(
    data: list, config: list = [], callback: typing.Callable | None = None
) -> list:
    """Process an array of data with optional configuration.

    :param data: The data to process
    :param config: Optional configuration parameters
    :param callback: Optional callback for custom processing
    """
