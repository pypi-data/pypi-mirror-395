from math import isinf

class ParaxialMagnification:
    def __init__(self, value: float):
        self.value = float(value)

    @classmethod
    def positive_infinity(cls):
        return cls(float('inf'))

    @classmethod
    def negative_infinity(cls):
        return cls(float('-inf'))

    @classmethod
    def from_float(cls, value: float) -> 'ParaxialMagnification':
        return cls(value)

    def is_infinite(self):
        return isinf(self.value)

    def is_negative(self):
        return self.value < 0

    def is_positive(self):
        return self.value > 0

    def __str__(self):
        if isinf(self.value):
            return "+∞" if self.value > 0 else "−∞"
        return f"{self.value:.2f}"

    def __repr__(self):
        return f"Magnification({self.value})"

    def __float__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, ParaxialMagnification):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == float(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ParaxialMagnification):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < float(other)
        return NotImplemented
