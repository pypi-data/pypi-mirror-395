"""
Module `catenary`

Provides classes and utilities to model overhead conductors as catenaries 
for mechanical analysis, sag-tension calculations, and load evaluation.

Classes:
    CatenaryState: Represents the mechanical state of a conductor (temperature, tension, weight).
    CatenaryApparentLoad: Represents the apparent load due to wind and vertical loads, 
        including resultant magnitude and swing angle.
    CatenaryModel: Encapsulates the catenary equations and change-of-state calculations 
        for a conductor.

Functions:
    (Uses `find_root` from .utils for numerical root-finding in change-of-state calculations.)

Notes:
    - Swing angle is the angle between the resultant conductor load vector and vertical.
    - Tension and weight are expressed in daN and daN/m respectively.
"""


import math
from dataclasses import dataclass

from .utils import find_root
from .conductor import Conductor


@dataclass
class CatenaryState:
    """Represents the mechanical state of a conductor catenary.

    Attributes:
        temp (float): Conductor temperature in degrees Celsius.
        tense (float): Horizontal tension in the conductor (daN).
        weight (float): Effective weight per unit length (daN/m), including any ice or additional loads.
    """

    temp: float
    tense: float
    weight: float


@dataclass
class CatenaryApparentLoad:
    """Represents the apparent (combined) load due to wind, ice and weight.

    Attributes:
        wind_load: Horizontal load component from wind (daN/m).
        effective_load: Vertical load component (bare + ice) (daN/m).
    """
    wind_load: float
    effective_load: float

    @property
    def resultant(self):
        """Returns the magnitude of resultant load vector."""
        return math.sqrt(self.wind_load ** 2 + self.effective_load **2)

    @property
    def swing_angle(self):
        """Returns the swing angle in radians.

        Swing angle is the angle formed between the conductor’s resultant load
        vector and the vertical direction.
        """
        return math.atan2(self.wind_load, self.effective_load)

    def __str__(self):
        """Return a readable string representation of the load."""
        return f"CatenaryApparentLoad(wind_load={self.wind_load}, effective_load={self.effective_load}) daN/m"

    
class CatenaryModel:
    """Represents a conductor as a catenary to understand its mechanical properties."""

    def __init__(self, conductor: Conductor) -> None:
        """Initialize the catenary model for a specific conductor.

        Args:
            conductor: The conductor object containing material and geometric properties.
        """
        self.conductor = conductor

    def cos(self, state0: CatenaryState, temp1: float, weight1: float, span: float) -> CatenaryState:
        """Perform a change of state (COS) for a catenary.

        Computes the new tension of the conductor when moving from an initial
        state to a new temperature and weight over a given span. This implements
        the standard catenary change-of-state equations used in sag-tension
        analysis.

        Args:
            state0: Initial catenary state (temperature, tension, and weight).
            temp1: Target temperature of the conductor (°C).
            weight1: Target conductor weight (daN/m), including ice if present.
            span: Span length between supports (m).

        Returns:
            CatenaryState: New state of the conductor at the target temperature
            and weight, including the recalculated horizontal tension.
        """

        def coseq(tense1: float) -> float:
            """Catenary equation for root finding: returns residual for a given horizontal tension."""

            temperature_factor = self.conductor.thermal_exp_factor * (temp1 - state0.temp)
            strength_factor = (tense1 - state0.tense) / (self.conductor.total_area * self.conductor.elastic_modulus)
            arc_length1_factor = (state0.tense / state0.weight) * math.sinh(span * state0.weight / (2 * state0.tense))
            arc_length2_factor = (tense1 / weight1) * math.sinh(span * weight1 / (2 * tense1))

            return temperature_factor + strength_factor - arc_length2_factor / arc_length1_factor + 1

        def cos_prime(tense1: float) -> float:
            """Derivative of the catenary residual function with respect to horizontal tension."""

            arc_length_state1 = (state0.tense / state0.weight) * math.sinh(span * state0.weight / (2 * state0.tense))
            span_times_weight2 = span * weight1
            return 1 / (self.conductor.total_area * self.conductor.elastic_modulus) + (1 / (weight1 * arc_length_state1)) * ((span_times_weight2 / (2 * tense1)) * math.cosh(span_times_weight2 / (2 * tense1)) - math.sinh(span_times_weight2 / (2 * tense1)))

        tense1 = find_root(coseq, cos_prime, state0.tense)
        return CatenaryState(temp=temp1, weight=weight1, tense=tense1)

    # TODO
    #def sag(self, tense, weight, suspan: SuspensionSpan):
    def sag(self):
        raise NotImplementedError("Not implemented yet")
        a = tense / weight
        suspan.start = - (suspan.length / 2 - a * suspan.inclination / suspan.length)
        assert suspan.start is not None
        suspan.end = suspan.length + suspan.start
        assert suspan.end is not None

        suspan.sag = a * math.cosh((suspan.start + suspan.end) / (2 * a)) * (math.cosh(suspan.length / (2 * a)) - 1)
        return suspan.sag


