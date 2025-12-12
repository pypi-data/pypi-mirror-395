# -------------------------------------------------------------------------
# UNIT CLASS
# -------------------------------------------------------------------------
from __future__ import (
    annotations,
)  # Allows using 'Unit' as a type hint inside the class
from typing import Union, List, Tuple

METRIC_PREFIXES = {
    "Y": 1e24,
    "Z": 1e21,
    "E": 1e18,
    "P": 1e15,
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "h": 1e2,
    "da": 1e1,
    "": 1,
    "d": 1e-1,
    "c": 1e-2,
    "m": 1e-3,
    "mi": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
    "z": 1e-21,
    "y": 1e-24,
}

# Set of known base units used to distinguish between prefix 'm' (milli) and base unit 'm' (meter)
KNOWN_BASE_UNITS = {
    "m",
    "g",
    "s",
    "A",
    "K",
    "mol",
    "cd",
    "N",
    "Pa",
    "J",
    "W",
    "V",
    "Hz",
    "C",
    "F",
    "Ohm",
    "S",
    "Wb",
    "T",
    "H",
}


class Unit:
    """
    A class to represent physical units and perform dimensional analysis and arithmetic operations.

    It handles metric prefixes (e.g., k, M, m) and allows for addition/subtraction of
    quantities with different compatible prefixes (e.g., adding kN to N).
    """

    def __init__(
        self, value: float, prefix: str, unitTop: str, unitBottom: str
    ) -> None:
        """
        Initialize a Unit object.

        Args:
            value (float): The numerical value of the unit.
            prefix (str): The metric prefix string (e.g., "k", "M", "m", "").
            unitTop (str): The string representing the numerator units (e.g., "N*m").
            unitBottom (str): The string representing the denominator units (e.g., "s").
        """
        self.prefix: str = prefix
        self.value: float = value
        self.unitTop: str = unitTop
        self.unitBottom: str = unitBottom

    @property
    def true_value(self) -> float:
        """
        float: The absolute value converted to base units (e.g., 10 kN -> 10000).
        """
        multiplier = METRIC_PREFIXES.get(self.prefix, 1)
        return self.value * multiplier

    def convert_to(self, new_prefix: str) -> Unit:
        """
        Converts the current unit to a specific metric prefix.

        Args:
            new_prefix (str): The target prefix (e.g., "k", "M").

        Returns:
            Unit: The instance itself (for chaining), with updated value and prefix.

        Raises:
            ValueError: If the provided prefix is not valid.
        """
        if new_prefix not in METRIC_PREFIXES:
            raise ValueError(f"Invalid prefix: '{new_prefix}'")
        new_multiplier = METRIC_PREFIXES[new_prefix]
        self.value = self.true_value / new_multiplier
        self.prefix = new_prefix
        return self

    def auto_scale(self) -> Unit:
        """
        Automatically adjusts the metric prefix to standard engineering notation.

        The method selects a prefix (T, G, M, k, m, u, n) such that the numerical
        value falls within the readable range of 0.1 to 1000. It avoids non-standard
        prefixes like 'c' (centi), 'd' (deci), or 'da' (deca).

        Returns:
            Unit: The instance itself with the optimized prefix.
        """
        base_val = abs(self.true_value)
        if base_val == 0:
            return self.convert_to("")

        eng_prefixes = ["T", "G", "M", "k", "", "m", "u", "n"]
        best_prefix = ""

        for prefix in eng_prefixes:
            multiplier = METRIC_PREFIXES[prefix]
            test_val = base_val / multiplier
            # We accept range 0.1 - 1000.
            if 0.1 <= test_val < 1000:
                best_prefix = prefix
                break

        return self.convert_to(best_prefix)

    def __repr__(self) -> str:
        """Returns the string representation of the unit (e.g., '10.5 k[N]')."""
        top = self.unitTop.strip("*")
        bot = self.unitBottom.strip("*")
        unit_str = f"[{top}]" if not bot else f"[{top} / {bot}]"
        prefix_display = self.prefix + " " if self.prefix else ""
        if not self.prefix:
            prefix_display = ""

        return f"{self.value:.4g} {prefix_display}{unit_str}"

    def _get_parts(self, s: str) -> List[str]:
        """Splits a unit string by '*' delimiter."""
        return [x for x in s.split("*") if x]

    def _simplify_units(
        self, top_list: List[str], bot_list: List[str]
    ) -> Tuple[str, str]:
        """Cancels out matching units from numerator and denominator lists."""
        for item in top_list[:]:
            if item in bot_list:
                top_list.remove(item)
                bot_list.remove(item)
        return "*".join(top_list), "*".join(bot_list)

    # --- UNIT PARSING HELPERS ---

    def _parse_component(self, part: str) -> Tuple[float, str]:
        """
        Parses a single unit component into its multiplier and base unit.

        Example: 'kN' -> (1000.0, 'N')

        Args:
            part (str): The unit string component.

        Returns:
            tuple: (multiplier, base_unit_string)
        """
        if part in KNOWN_BASE_UNITS:
            return 1.0, part

        # Check if it starts with a known prefix
        for p, mult in METRIC_PREFIXES.items():
            if p and part.startswith(p):
                base = part[len(p) :]
                if base in KNOWN_BASE_UNITS:
                    return mult, base
        return 1.0, part

    def _analyze_unit_string(self, unit_str: str) -> Tuple[float, str]:
        """
        Analyzes a full unit string to determine total multiplier and canonical form.

        This handles complex units like 'kN*cm'.

        Returns:
            tuple: (total_multiplier, canonical_base_string)
        """
        parts = self._get_parts(unit_str)
        total_mult = 1.0
        canonical_parts = []
        for p in parts:
            m, base = self._parse_component(p)
            total_mult *= m
            canonical_parts.append(base)
        # Sort to ensure N*m is treated equal to m*N
        return total_mult, "*".join(sorted(canonical_parts))

    # --- OPERATOR OVERLOADS ---

    def __add__(self, other: Union[Unit, int, float]) -> Unit:
        """
        Adds two Unit objects, handling prefix conversion automatically.

        Example: 1 kN + 500 N = 1.5 kN
        """
        if isinstance(other, Unit):
            # Analyze units (e.g. kN -> 1000, N)
            s_top_mult, s_top_can = self._analyze_unit_string(self.unitTop)
            s_bot_mult, s_bot_can = self._analyze_unit_string(self.unitBottom)

            o_top_mult, o_top_can = other._analyze_unit_string(other.unitTop)
            o_bot_mult, o_bot_can = other._analyze_unit_string(other.unitBottom)

            # Check dimensional consistency (normalized to base units)
            if s_top_can != o_top_can or s_bot_can != o_bot_can:
                raise TypeError(f"Cannot add different dimensions: {self} + {other}")

            # Calculate scaling factors relative to base units
            s_factor = s_top_mult / s_bot_mult
            o_factor = o_top_mult / o_bot_mult

            # Normalize both values to base units
            val_self_norm = self.true_value * s_factor
            val_other_norm = other.true_value * o_factor

            total_norm = val_self_norm + val_other_norm

            # Convert result back to 'self' units
            final_value = total_norm / s_factor

            # Return result in units of the first operand (self)
            return Unit(final_value, "", self.unitTop, self.unitBottom)

        return NotImplemented

    def __sub__(self, other: Union[Unit, int, float]) -> Unit:
        """
        Subtracts two Unit objects, handling prefix conversion automatically.
        """
        if isinstance(other, Unit):
            s_top_mult, s_top_can = self._analyze_unit_string(self.unitTop)
            s_bot_mult, s_bot_can = self._analyze_unit_string(self.unitBottom)
            o_top_mult, o_top_can = other._analyze_unit_string(other.unitTop)
            o_bot_mult, o_bot_can = other._analyze_unit_string(other.unitBottom)

            if s_top_can != o_top_can or s_bot_can != o_bot_can:
                raise TypeError(
                    f"Cannot subtract different dimensions: {self} - {other}"
                )

            s_factor = s_top_mult / s_bot_mult
            o_factor = o_top_mult / o_bot_mult

            val_self_norm = self.true_value * s_factor
            val_other_norm = other.true_value * o_factor

            total_norm = val_self_norm - val_other_norm
            final_value = total_norm / s_factor

            return Unit(final_value, "", self.unitTop, self.unitBottom)
        return NotImplemented

    def __mul__(self, other: Union[Unit, int, float]) -> Unit:
        """
        Multiplies Unit by another Unit or scalar.

        Returns:
            Unit: A new Unit object with combined dimensions and calculated value.
        """
        if isinstance(other, Unit):
            s_top = self._get_parts(self.unitTop)
            s_bot = self._get_parts(self.unitBottom)
            o_top = other._get_parts(other.unitTop)
            o_bot = other._get_parts(other.unitBottom)
            new_top = s_top + o_top
            new_bot = s_bot + o_bot
            final_top, final_bot = self._simplify_units(new_top, new_bot)
            return Unit(self.true_value * other.true_value, "", final_top, final_bot)
        elif isinstance(other, (int, float)):
            return Unit(self.value * other, self.prefix, self.unitTop, self.unitBottom)
        return NotImplemented

    def __truediv__(self, other: Union[Unit, int, float]) -> Unit:
        """
        Divides Unit by another Unit or scalar.

        Returns:
            Unit: A new Unit object with simplified dimensions.
        """
        if isinstance(other, Unit):
            s_top = self._get_parts(self.unitTop)
            s_bot = self._get_parts(self.unitBottom)
            o_top = other._get_parts(other.unitTop)
            o_bot = other._get_parts(other.unitBottom)
            new_top = s_top + o_bot
            new_bot = s_bot + o_top
            final_top, final_bot = self._simplify_units(new_top, new_bot)
            return Unit(self.true_value / other.true_value, "", final_top, final_bot)
        elif isinstance(other, (int, float)):
            return Unit(self.value / other, self.prefix, self.unitTop, self.unitBottom)
        return NotImplemented

    def __pow__(self, power: Union[int, float]) -> Unit:
        """Raises the unit's value to a power (mostly for dimensionless scaling)."""
        if isinstance(power, (int, float)):
            return Unit(self.true_value**power, "", self.unitTop, self.unitBottom)
        return NotImplemented

    def __lt__(self, other: Unit) -> bool:
        if isinstance(other, Unit):
            return self.true_value < other.true_value
        return NotImplemented
