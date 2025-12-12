from __future__ import annotations


class Calculator:
    """A class that performs basic arithmetic operations."""

    lastResult: int = 0  # Stores the result of the last operation performed.

    def add(self, a: int, b: int) -> int:
        """Calculate the sum of two ints.

        :param a: The first operand.
        :param b: The second operand.
        :return: The sum of the two numbers.
        """
