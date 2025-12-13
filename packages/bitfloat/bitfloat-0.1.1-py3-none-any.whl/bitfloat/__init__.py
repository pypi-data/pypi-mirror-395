__version__ = "0.1.1"


class BitFloat:
    """
    A class representing a floating-point number following IEEE 754 standard.
    Supports arbitrary exponent and mantissa bitwidths, including denormal numbers.
    """

    def __init__(
        self,
        sign: int = 0,
        exponent: int = 0,
        mantissa: int = 0,
        exponent_bits: int = 8,
        mantissa_bits: int = 23,
    ):
        """
        Initialize a BitFloat number.

        Args:
            sign: Sign bit (0 for positive, 1 for negative)
            exponent: Exponent bits value (unsigned integer)
            mantissa: Mantissa bits value (unsigned integer)
            exponent_bits: Number of bits for exponent (default: 8 for float32)
            mantissa_bits: Number of bits for mantissa (default: 23 for float32)
        """
        self.sign = sign & 1
        self.exponent_bits = exponent_bits
        self.mantissa_bits = mantissa_bits

        # Clamp exponent and mantissa to their bit ranges
        self.exponent = exponent & ((1 << exponent_bits) - 1)
        self.mantissa = mantissa & ((1 << mantissa_bits) - 1)

    def to_float(self) -> float:
        """
        Convert the Float representation to a Python float value.
        Handles normal, denormal, zero, infinity, and NaN according to IEEE 754.
        """
        # Calculate bias for the exponent
        bias = (1 << (self.exponent_bits - 1)) - 1

        # Check for special cases
        max_exponent = (1 << self.exponent_bits) - 1

        # Zero
        if self.exponent == 0 and self.mantissa == 0:
            return -0.0 if self.sign else 0.0

        # Infinity
        if self.exponent == max_exponent and self.mantissa == 0:
            return float("-inf") if self.sign else float("inf")

        # NaN
        if self.exponent == max_exponent and self.mantissa != 0:
            return float("nan")

        # Denormal (subnormal) numbers
        if self.exponent == 0:
            # Denormal: (-1)^sign × 2^(1-bias) × 0.mantissa
            mantissa_value = self.mantissa / (1 << self.mantissa_bits)
            value = mantissa_value * (2 ** (1 - bias))
        else:
            # Normal numbers: (-1)^sign × 2^(exponent-bias) × 1.mantissa
            mantissa_value = 1.0 + self.mantissa / (1 << self.mantissa_bits)
            value = mantissa_value * (2 ** (self.exponent - bias))

        return -value if self.sign else value

    @classmethod
    def from_float(
        cls, value: float, exponent_bits: int = None, mantissa_bits: int = None
    ) -> "BitFloat":
        """
        Create a BitFloat from a Python float value.

        Args:
            value: The float value to convert
            exponent_bits: Number of bits for exponent (uses class default if None)
            mantissa_bits: Number of bits for mantissa (uses class default if None)

        Returns:
            Float instance representing the value
        """
        import math

        # For subclasses, use their default bit widths if not specified
        if exponent_bits is None or mantissa_bits is None:
            # Create a temporary instance to get default values
            temp = cls()
            if exponent_bits is None:
                exponent_bits = temp.exponent_bits
            if mantissa_bits is None:
                mantissa_bits = temp.mantissa_bits

        # Extract sign
        sign = 1 if value < 0 else 0
        value = abs(value)

        bias = (1 << (exponent_bits - 1)) - 1
        max_exponent = (1 << exponent_bits) - 1

        # Handle special cases
        if value == 0.0:
            return cls(sign, 0, 0, exponent_bits, mantissa_bits)

        if math.isinf(value):
            return cls(sign, max_exponent, 0, exponent_bits, mantissa_bits)

        if math.isnan(value):
            return cls(0, max_exponent, 1, exponent_bits, mantissa_bits)

        # Get exponent and mantissa
        # frexp returns mantissa in [0.5, 1.0) and exponent
        mantissa_float, exp = math.frexp(value)
        mantissa_float *= 2  # Scale to [1.0, 2.0)
        exp -= 1

        # Check if the number should be denormal
        min_exp = 1 - bias
        if exp < min_exp:
            # Denormal number
            # Adjust mantissa for denormal representation
            mantissa_float *= 2 ** (exp - min_exp)
            exponent = 0
            mantissa = int(mantissa_float * (1 << mantissa_bits))
        else:
            # Normal number
            exponent = exp + bias
            # Remove implicit leading 1
            mantissa_float -= 1.0
            mantissa = int(mantissa_float * (1 << mantissa_bits) + 0.5)

            # Handle rounding overflow
            if mantissa >= (1 << mantissa_bits):
                mantissa = 0
                exponent += 1

            # Check for overflow to infinity
            if exponent >= max_exponent:
                exponent = max_exponent
                mantissa = 0

        # For subclasses, only pass sign, exponent, mantissa
        if cls != BitFloat:
            return cls(sign, exponent, mantissa)
        else:
            return cls(sign, exponent, mantissa, exponent_bits, mantissa_bits)

    def to_int(self) -> int:
        """
        Convert the BitFloat representation to its integer bit pattern.
        """
        return (
            (self.sign << (self.exponent_bits + self.mantissa_bits))
            | (self.exponent << self.mantissa_bits)
            | self.mantissa
        )

    @classmethod
    def from_int(
        cls, value: int, exponent_bits: int = None, mantissa_bits: int = None
    ) -> "BitFloat":
        """
        Create a BitFloat from its integer bit pattern.

        Args:
            value: The integer bit pattern
            exponent_bits: Number of bits for exponent (uses class default if None)
            mantissa_bits: Number of bits for mantissa (uses class default if None)
        Returns:
            BitFloat instance representing the value
        """
        # For subclasses, use their default bit widths if not specified
        if exponent_bits is None or mantissa_bits is None:
            # Create a temporary instance to get default values
            temp = cls()
            if exponent_bits is None:
                exponent_bits = temp.exponent_bits
            if mantissa_bits is None:
                mantissa_bits = temp.mantissa_bits

        sign = (value >> (exponent_bits + mantissa_bits)) & 0x1
        exponent = (value >> mantissa_bits) & ((1 << exponent_bits) - 1)
        mantissa = value & ((1 << mantissa_bits) - 1)

        # For subclasses, only pass sign, exponent, mantissa
        if cls != BitFloat:
            return cls(sign, exponent, mantissa)
        else:
            return cls(sign, exponent, mantissa, exponent_bits, mantissa_bits)

    def __repr__(self) -> str:
        """
        String representation showing both bit pattern and float value.
        """
        # Format bit patterns
        sign_str = f"{self.sign:1b}"
        exp_str = f"{self.exponent:0{self.exponent_bits}b}"
        mant_str = f"{self.mantissa:0{self.mantissa_bits}b}"

        # Calculate the actual float value
        float_value = self.to_float()

        # Determine the type of number
        max_exponent = (1 << self.exponent_bits) - 1
        if self.exponent == 0 and self.mantissa == 0:
            num_type = "zero"
        elif self.exponent == max_exponent and self.mantissa == 0:
            num_type = "inf"
        elif self.exponent == max_exponent and self.mantissa != 0:
            num_type = "nan"
        elif self.exponent == 0:
            num_type = "denormal"
        else:
            num_type = "normal"

        return (
            f"float(e{self.exponent_bits}m{self.mantissa_bits}): "
            f"{sign_str}|{exp_str}|{mant_str} = {hex(self.to_int())} = {float_value} ({num_type})"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def _make_instance(self, sign: int, exponent: int, mantissa: int) -> "BitFloat":
        """
        Helper method to create an instance of the same class.
        Handles both Float and subclass constructors correctly.
        """
        if self.__class__ != BitFloat:
            return self.__class__(sign, exponent, mantissa)
        else:
            return self.__class__(
                sign, exponent, mantissa, self.exponent_bits, self.mantissa_bits
            )

    def __add__(self, other: "BitFloat") -> "BitFloat":
        """
        Add two BitFloat numbers according to IEEE 754 standard.
        Handles all special cases: NaN, infinity, zero, normal, and denormal numbers.
        """
        import math

        # Ensure both operands have the same format
        if (
            self.exponent_bits != other.exponent_bits
            or self.mantissa_bits != other.mantissa_bits
        ):
            raise ValueError(
                "Cannot add Float numbers with different formats. "
                f"self: e{self.exponent_bits}m{self.mantissa_bits}, "
                f"other: e{other.exponent_bits}m{other.mantissa_bits}"
            )

        max_exponent = (1 << self.exponent_bits) - 1
        bias = (1 << (self.exponent_bits - 1)) - 1

        # Check for NaN
        if (self.exponent == max_exponent and self.mantissa != 0) or (
            other.exponent == max_exponent and other.mantissa != 0
        ):
            # NaN + anything = NaN
            return self._make_instance(0, max_exponent, 1)

        # Check for infinity
        self_is_inf = self.exponent == max_exponent and self.mantissa == 0
        other_is_inf = other.exponent == max_exponent and other.mantissa == 0

        if self_is_inf and other_is_inf:
            # inf + inf = inf (same sign) or NaN (opposite signs)
            if self.sign == other.sign:
                return self.__class__(
                    self.sign, max_exponent, 0, self.exponent_bits, self.mantissa_bits
                )
            else:
                # inf + (-inf) = NaN
                return self._make_instance(0, max_exponent, 1)

        if self_is_inf:
            return self._make_instance(self.sign, max_exponent, 0)

        if other_is_inf:
            return self._make_instance(other.sign, max_exponent, 0)

        # Check for zero
        self_is_zero = self.exponent == 0 and self.mantissa == 0
        other_is_zero = other.exponent == 0 and other.mantissa == 0

        if self_is_zero and other_is_zero:
            # +0 + +0 = +0, -0 + -0 = -0, +0 + -0 = +0 (default)
            result_sign = self.sign if self.sign == other.sign else 0
            return self._make_instance(result_sign, 0, 0)

        if self_is_zero:
            return self._make_instance(other.sign, other.exponent, other.mantissa)

        if other_is_zero:
            return self._make_instance(self.sign, self.exponent, self.mantissa)

        # Extract actual exponents and mantissas
        # For denormal numbers: exponent = 1 - bias, mantissa has no implicit 1
        # For normal numbers: exponent = exp - bias, mantissa has implicit 1
        if self.exponent == 0:  # Denormal
            self_exp = 1 - bias
            self_mant = self.mantissa
        else:  # Normal
            self_exp = self.exponent - bias
            self_mant = self.mantissa | (1 << self.mantissa_bits)

        if other.exponent == 0:  # Denormal
            other_exp = 1 - bias
            other_mant = other.mantissa
        else:  # Normal
            other_exp = other.exponent - bias
            other_mant = other.mantissa | (1 << self.mantissa_bits)

        # Align exponents
        exp_diff = self_exp - other_exp
        if exp_diff > 0:
            # self has larger exponent
            result_exp = self_exp
            # Shift other's mantissa right
            if exp_diff < self.mantissa_bits + 10:  # Keep some precision
                other_mant = other_mant >> exp_diff
            else:
                other_mant = 0
        elif exp_diff < 0:
            # other has larger exponent
            result_exp = other_exp
            # Shift self's mantissa right
            if -exp_diff < self.mantissa_bits + 10:
                self_mant = self_mant >> (-exp_diff)
            else:
                self_mant = 0
        else:
            result_exp = self_exp

        # Perform addition or subtraction based on signs
        if self.sign == other.sign:
            # Same sign: add magnitudes
            result_mant = self_mant + other_mant
            result_sign = self.sign
        else:
            # Different signs: subtract magnitudes
            if self_mant >= other_mant:
                result_mant = self_mant - other_mant
                result_sign = self.sign
            else:
                result_mant = other_mant - self_mant
                result_sign = other.sign

        # Handle zero result
        if result_mant == 0:
            return self._make_instance(0, 0, 0)

        # Normalize the result
        # Find the position of the leading 1 bit
        mantissa_mask = (1 << self.mantissa_bits) - 1
        implicit_bit = 1 << self.mantissa_bits

        # Normalize: shift until we have 1.xxxxx format
        while result_mant >= (implicit_bit << 1):
            # Too large, shift right
            result_mant >>= 1
            result_exp += 1

        while result_mant < implicit_bit and result_exp > (1 - bias):
            # Too small, shift left
            result_mant <<= 1
            result_exp -= 1

        # Check for denormal result
        if result_exp <= (1 - bias):
            # Result is denormal
            # Shift mantissa to denormal position
            shift = (1 - bias) - result_exp
            if shift < self.mantissa_bits + 10:
                result_mant >>= shift
            else:
                result_mant = 0

            if result_mant == 0:
                return self._make_instance(result_sign, 0, 0)

            return self._make_instance(result_sign, 0, result_mant & mantissa_mask)

        # Remove implicit bit for normal numbers
        result_mant &= mantissa_mask

        # Convert exponent back to biased form
        result_exp_biased = result_exp + bias

        # Check for overflow to infinity
        if result_exp_biased >= max_exponent:
            return self._make_instance(result_sign, max_exponent, 0)

        # Check for underflow to zero
        if result_exp_biased <= 0:
            return self._make_instance(result_sign, 0, 0)

        return self._make_instance(result_sign, result_exp_biased, result_mant)

    def __mul__(self, other: "BitFloat") -> "BitFloat":
        """
        Multiply two BitFloat numbers according to IEEE 754 standard.
        Handles all special cases: NaN, infinity, zero, normal, and denormal numbers.
        """
        import math

        # Ensure both operands have the same format
        if (
            self.exponent_bits != other.exponent_bits
            or self.mantissa_bits != other.mantissa_bits
        ):
            raise ValueError(
                "Cannot multiply Float numbers with different formats. "
                f"self: e{self.exponent_bits}m{self.mantissa_bits}, "
                f"other: e{other.exponent_bits}m{other.mantissa_bits}"
            )

        max_exponent = (1 << self.exponent_bits) - 1
        bias = (1 << (self.exponent_bits - 1)) - 1

        # Result sign: XOR of signs
        result_sign = self.sign ^ other.sign

        # Check for NaN
        if (self.exponent == max_exponent and self.mantissa != 0) or (
            other.exponent == max_exponent and other.mantissa != 0
        ):
            # NaN * anything = NaN
            return self._make_instance(0, max_exponent, 1)

        # Check for infinity
        self_is_inf = self.exponent == max_exponent and self.mantissa == 0
        other_is_inf = other.exponent == max_exponent and other.mantissa == 0
        self_is_zero = self.exponent == 0 and self.mantissa == 0
        other_is_zero = other.exponent == 0 and other.mantissa == 0

        # inf * 0 = NaN, 0 * inf = NaN
        if (self_is_inf and other_is_zero) or (self_is_zero and other_is_inf):
            return self._make_instance(0, max_exponent, 1)

        # inf * anything (non-zero) = inf
        if self_is_inf or other_is_inf:
            return self._make_instance(result_sign, max_exponent, 0)

        # 0 * anything = 0
        if self_is_zero or other_is_zero:
            return self._make_instance(result_sign, 0, 0)

        # Extract actual exponents and mantissas
        if self.exponent == 0:  # Denormal
            self_exp = 1 - bias
            self_mant = self.mantissa
        else:  # Normal
            self_exp = self.exponent - bias
            self_mant = self.mantissa | (1 << self.mantissa_bits)

        if other.exponent == 0:  # Denormal
            other_exp = 1 - bias
            other_mant = other.mantissa
        else:  # Normal
            other_exp = other.exponent - bias
            other_mant = other.mantissa | (1 << self.mantissa_bits)

        # Multiply mantissas
        # Both mantissas are in format: (1 or 0).fraction with mantissa_bits precision
        result_mant = self_mant * other_mant

        # Add exponents
        result_exp = self_exp + other_exp

        # The multiplication of two mantissas gives us a result with 2*mantissa_bits precision
        # We need to shift it back to mantissa_bits precision
        # If both have implicit 1: (1.xxx) * (1.yyy) = 1.zzz to 3.zzz (2 to 4 in integer form)
        result_mant >>= self.mantissa_bits

        # Normalize the result
        mantissa_mask = (1 << self.mantissa_bits) - 1
        implicit_bit = 1 << self.mantissa_bits

        # Normalize: shift until we have 1.xxxxx format
        while result_mant >= (implicit_bit << 1):
            result_mant >>= 1
            result_exp += 1

        while (
            result_mant > 0 and result_mant < implicit_bit and result_exp > (1 - bias)
        ):
            result_mant <<= 1
            result_exp -= 1

        # Handle zero result
        if result_mant == 0:
            return self._make_instance(result_sign, 0, 0)

        # Check for denormal result
        if result_exp <= (1 - bias):
            # Result is denormal
            shift = (1 - bias) - result_exp
            if shift < self.mantissa_bits + 10:
                result_mant >>= shift
            else:
                result_mant = 0

            if result_mant == 0:
                return self._make_instance(result_sign, 0, 0)

            return self._make_instance(result_sign, 0, result_mant & mantissa_mask)

        # Remove implicit bit for normal numbers
        result_mant &= mantissa_mask

        # Convert exponent back to biased form
        result_exp_biased = result_exp + bias

        # Check for overflow to infinity
        if result_exp_biased >= max_exponent:
            return self._make_instance(result_sign, max_exponent, 0)

        # Check for underflow to zero
        if result_exp_biased <= 0:
            return self._make_instance(result_sign, 0, 0)

        return self._make_instance(result_sign, result_exp_biased, result_mant)

    def __sub__(self, other: "BitFloat") -> "BitFloat":
        """
        Subtract two BitFloat numbers according to IEEE 754 standard.
        Implements a - b by computing a + (-b).
        """
        # Create a negated version of other by flipping its sign bit
        negated_other = self._make_instance(
            other.sign ^ 1, other.exponent, other.mantissa
        )
        # Reuse addition logic
        return self.__add__(negated_other)

    def __truediv__(self, other: "BitFloat") -> "BitFloat":
        """
        Divide two BitFloat numbers according to IEEE 754 standard.
        Handles all special cases: NaN, infinity, zero, normal, and denormal numbers.
        """
        import math

        # Ensure both operands have the same format
        if (
            self.exponent_bits != other.exponent_bits
            or self.mantissa_bits != other.mantissa_bits
        ):
            raise ValueError(
                "Cannot divide Float numbers with different formats. "
                f"self: e{self.exponent_bits}m{self.mantissa_bits}, "
                f"other: e{other.exponent_bits}m{other.mantissa_bits}"
            )

        max_exponent = (1 << self.exponent_bits) - 1
        bias = (1 << (self.exponent_bits - 1)) - 1

        # Result sign: XOR of signs
        result_sign = self.sign ^ other.sign

        # Check for NaN
        if (self.exponent == max_exponent and self.mantissa != 0) or (
            other.exponent == max_exponent and other.mantissa != 0
        ):
            # NaN / anything = NaN, anything / NaN = NaN
            return self._make_instance(0, max_exponent, 1)

        # Check for infinity and zero
        self_is_inf = self.exponent == max_exponent and self.mantissa == 0
        other_is_inf = other.exponent == max_exponent and other.mantissa == 0
        self_is_zero = self.exponent == 0 and self.mantissa == 0
        other_is_zero = other.exponent == 0 and other.mantissa == 0

        # inf / inf = NaN, 0 / 0 = NaN
        if (self_is_inf and other_is_inf) or (self_is_zero and other_is_zero):
            return self._make_instance(0, max_exponent, 1)

        # inf / anything (non-inf) = inf
        if self_is_inf:
            return self._make_instance(result_sign, max_exponent, 0)

        # anything / inf = 0
        if other_is_inf:
            return self._make_instance(result_sign, 0, 0)

        # 0 / anything (non-zero) = 0
        if self_is_zero:
            return self._make_instance(result_sign, 0, 0)

        # anything / 0 = inf
        if other_is_zero:
            return self._make_instance(result_sign, max_exponent, 0)

        # Extract actual exponents and mantissas
        if self.exponent == 0:  # Denormal
            self_exp = 1 - bias
            self_mant = self.mantissa
        else:  # Normal
            self_exp = self.exponent - bias
            self_mant = self.mantissa | (1 << self.mantissa_bits)

        if other.exponent == 0:  # Denormal
            other_exp = 1 - bias
            other_mant = other.mantissa
        else:  # Normal
            other_exp = other.exponent - bias
            other_mant = other.mantissa | (1 << self.mantissa_bits)

        # Subtract exponents
        result_exp = self_exp - other_exp

        # Divide mantissas
        # We need to shift the dividend left to maintain precision
        # Shift by mantissa_bits to get enough precision for the division
        self_mant_shifted = self_mant << self.mantissa_bits
        result_mant = self_mant_shifted // other_mant

        # Normalize the result
        mantissa_mask = (1 << self.mantissa_bits) - 1
        implicit_bit = 1 << self.mantissa_bits

        # Normalize: shift until we have 1.xxxxx format
        while result_mant >= (implicit_bit << 1):
            result_mant >>= 1
            result_exp += 1

        while (
            result_mant > 0 and result_mant < implicit_bit and result_exp > (1 - bias)
        ):
            result_mant <<= 1
            result_exp -= 1

        # Handle zero result
        if result_mant == 0:
            return self._make_instance(result_sign, 0, 0)

        # Check for denormal result
        if result_exp <= (1 - bias):
            # Result is denormal
            shift = (1 - bias) - result_exp
            if shift < self.mantissa_bits + 10:
                result_mant >>= shift
            else:
                result_mant = 0

            if result_mant == 0:
                return self._make_instance(result_sign, 0, 0)

            return self._make_instance(result_sign, 0, result_mant & mantissa_mask)

        # Remove implicit bit for normal numbers
        result_mant &= mantissa_mask

        # Convert exponent back to biased form
        result_exp_biased = result_exp + bias

        # Check for overflow to infinity
        if result_exp_biased >= max_exponent:
            return self._make_instance(result_sign, max_exponent, 0)

        # Check for underflow to zero
        if result_exp_biased <= 0:
            return self._make_instance(result_sign, 0, 0)

        return self._make_instance(result_sign, result_exp_biased, result_mant)


class F64(BitFloat):
    """
    A subclass of BitFloat representing standard 64-bit float (float64).
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=11, mantissa_bits=52)


class F32(BitFloat):
    """
    A subclass of BitFloat representing standard 32-bit float (float32).
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=8, mantissa_bits=23)


class F16(BitFloat):
    """
    A subclass of BitFloat representing standard 16-bit float (float16).
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=5, mantissa_bits=10)


class BF16(BitFloat):
    """
    A subclass of BitFloat representing bfloat16 float.
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=8, mantissa_bits=7)


class F8E4M3(BitFloat):
    """
    A subclass of BitFloat representing 8-bit float with 4 exponent bits and 3 mantissa bits.
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=4, mantissa_bits=3)


class F8E5M2(BitFloat):
    """
    A subclass of BitFloat representing 8-bit float with 5 exponent bits and 2 mantissa bits.
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=5, mantissa_bits=2)


class F4E2M1(BitFloat):
    """
    A subclass of BitFloat representing 4-bit float with 2 exponent bits and 1 mantissa bit.
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=2, mantissa_bits=1)


class BF24(BitFloat):
    """
    A subclass of BitFloat representing a custom 24-bit float with 8 exponent bits and 15 mantissa bits.
    """

    def __init__(self, sign: int = 0, exponent: int = 0, mantissa: int = 0):
        super().__init__(sign, exponent, mantissa, exponent_bits=8, mantissa_bits=15)
