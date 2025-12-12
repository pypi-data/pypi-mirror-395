"""Compute mean and variance."""

import math
import typing

from attrs import define


@define
class RunningMeanVar:
    """Compute mean and variance."""

    num_values: int = 0
    M1: float = 0.0
    M2: float = 0.0

    def push(self, x: float) -> None:
        """Add a value.

        Examples:
        >>> rmv = RunningMeanVar()
        >>> rmv.push(2.0)
        >>> rmv.push(3.0)
        >>> rmv.mean()
        2.5
        """
        self.num_values += 1
        delta = x - self.M1
        self.M1 += delta / self.num_values
        self.M2 += delta * (x - self.M1)

    def push_iter(self, values: typing.Iterable[float]) -> None:
        """Add values from an Iterable."""
        for value in values:
            self.push(value)

    def mean(self) -> float:
        """Compute mean."""
        return self.M1

    def variance(self) -> float:
        """Compute the sample variance."""
        return self.M2 / (self.num_values - 1) if self.num_values > 1 else 0.0

    def standard_deviation(self) -> float:
        """Compute the sample standard deviation."""
        return math.sqrt(self.variance())

    def __add__(self, other: "RunningMeanVar") -> "RunningMeanVar":
        """Combine 2 RunningMeanVar instances."""
        combined = RunningMeanVar()
        combined.num_values = self.num_values + other.num_values

        if combined.num_values == 0:
            return combined

        delta = other.M1 - self.M1
        delta2 = delta * delta

        combined.M1 = (
            self.M1 * self.num_values + other.M1 * other.num_values
        ) / combined.num_values
        combined.M2 = (
            self.M2
            + other.M2
            + delta2 * self.num_values * other.num_values / combined.num_values
        )

        return combined


@define
class RunningStats(RunningMeanVar):
    """Compute mean, variance, skewness and kurtosis."""

    M3: float = 0.0
    M4: float = 0.0

    def push(self, x: float) -> None:
        """Add a value."""
        n_1 = self.num_values
        self.num_values += 1
        delta = x - self.M1
        delta_n = delta / self.num_values
        delta_n2 = delta_n * delta_n
        term1 = delta * delta_n * n_1
        self.M1 += delta_n
        self.M4 += (
            term1 * delta_n2 * (self.num_values * self.num_values - 3 * self.num_values + 3)
            + 6 * delta_n2 * self.M2
            - 4 * delta_n * self.M3
        )
        self.M2 += term1

    def __add__(self, other: "RunningStats") -> "RunningStats":  # type: ignore
        """Combine 2 RunningMeanVar instances."""
        combined = RunningStats()
        combined.num_values = self.num_values + other.num_values

        if combined.num_values == 0:
            return combined

        delta = other.M1 - self.M1
        delta2 = delta * delta
        delta3 = delta * delta2
        delta4 = delta2 * delta2

        combined.M1 = (
            self.M1 * self.num_values + other.M1 * other.num_values
        ) / combined.num_values

        combined.M2 = (
            self.M2
            + other.M2
            + delta2 * self.num_values * other.num_values / combined.num_values
        )

        combined.M3 = (
            self.M3
            + other.M3
            + delta3
            * self.num_values
            * other.num_values
            * (self.num_values - other.num_values)
            / (combined.num_values * combined.num_values)
        )
        combined.M3 += (
            3.0
            * delta
            * (self.num_values * other.M2 - other.num_values * self.M2)
            / combined.num_values
        )

        combined.M4 = (
            self.M4
            + other.M4
            + delta4
            * self.num_values
            * other.num_values
            * (
                self.num_values * self.num_values
                - self.num_values * other.num_values
                + other.num_values * other.num_values
            )
            / (combined.num_values * combined.num_values * combined.num_values)
        )
        combined.M4 += (
            6.0
            * delta2
            * (
                self.num_values * self.num_values * other.M2
                + other.num_values * other.num_values * self.M2
            )
            / (combined.num_values * combined.num_values)
            + 4.0
            * delta
            * (self.num_values * other.M3 - other.num_values * self.M3)
            / combined.num_values
        )

        return combined
