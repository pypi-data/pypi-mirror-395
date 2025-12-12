"""
Module `mech`

Provides mechanical analysis tools for overhead conductors, including:

- Zone-based conductor properties (altitude-dependent ice loads)
- Every-Day Stress (EDS) and Cold-Hour Stress (CHS) calculation
- Apparent load computation under wind and ice
- Ruling span calculation
- Hypothesis-based sag-tension analysis

Classes:
    MechAnalysisZone: Altitude-based mechanical analysis zone.
    MechAnalysis: Performs mechanical analysis of a conductor for a given zone.
    MechAnalysisHypothesis: Represents a single scenario for analysis.
    SagTensionAnalyzer: Generates sag-tension tables and finds controlling hypotheses.

Notes:
    - Tensions are in daN, weights in daN/m.
    - The controlling hypothesis is the one whose calculated tension does not exceed allowable limits in any scenario.
"""


import math
from dataclasses import dataclass
from enum import Enum

from .conductor import Conductor
from .catenary import CatenaryModel, CatenaryState, CatenaryApparentLoad


class MechAnalysisZone(Enum):
    """Mechanical analysis zone based on altitude."""

    A = (0, "Below 500 m")
    B = (1, "Between 500 and 1000 m")
    C = (2, "Above 1000 m")

    def __init__(self, _, description):
        """Initializes the zone with a description.

        Args:
            description: Human-readable description of the zone.
        """
        self.description = description

class MechAnalysis:
    """Performs mechanical analysis of a conductor for a given zone."""

    def __init__(self, conductor: Conductor, zone: MechAnalysisZone):
        """Initializes the mechanical analysis.

        Args:
            conductor: Conductor object with material and geometric properties.
            zone: Mechanical analysis zone (altitude-dependent).
        """

        self.conductor = conductor
        self.cat = CatenaryModel(conductor)
        self.zone = zone
    
    @property
    def ice_weight(self) -> float:
        """Returns ice load per unit length (daN/m) based on the zone.

        Raises:
            ValueError: If ice is undefined for the zone.
        """

        if self.zone == MechAnalysisZone.A:
            raise ValueError("Ice weight is undefined for zone A (no ice per the norm)")
        if self.zone == MechAnalysisZone.B:
            return 0.18 * math.sqrt(self.conductor.overall_diameter)
        return 0.36 * math.sqrt(self.conductor.overall_diameter)

    def eds(self, with_dampers: bool = False) -> CatenaryState:
        """Computes Every-Day Stress (EDS) conditions for the conductor.

        Args:
            with_dampers: If True, includes the effect of dampers.

        Returns:
            CatenaryState: Conductor state with temperature, tension, and weight.
        """

        max_tense = 0.15 * self.conductor.rated_strength
        if with_dampers: max_tense = 0.22 * self.conductor.rated_strength

        return CatenaryState(temp=15, tense=max_tense, weight=self.conductor.unit_weight)

    def chs(self, temp: float, rts_factor: float) -> CatenaryState:
        """Computes Cold-Hour Stress (CHS) conditions for the conductor.

        Args:
            temp: Conductor temperature (°C).
            rts_factor: Fraction of conductor rated strength to use.

        Returns:
            CatenaryState: Conductor state at the given temperature and tension.
        """

        return CatenaryState(temp, tense = rts_factor * self.conductor.rated_strength, weight=self.conductor.unit_weight)

    def overload(self, wind_speed: float = 0., with_ice: bool = False):
        """Calculates apparent load due to wind and/or ice.

        Args:
            wind_speed: Wind speed in km/h.
            with_ice: Whether ice is present.

        Returns:
            CatenaryApparentLoad: Combined wind and vertical load on the conductor.
        """

        wind_velocity_factor = (wind_speed / 120) ** 2  # this is in daN/m^2

        conductor_diameter = self.conductor.overall_diameter * 1e-3  # We need this in meters, not millimeters.

        total_diameter = conductor_diameter
        if with_ice:
            total_diameter = math.sqrt((4 * self.ice_weight / (750 * math.pi)) + conductor_diameter ** 2)

        wind_pressure = 60 * wind_velocity_factor
        if total_diameter > 16 * 1e-3:
            wind_pressure = 50 * wind_velocity_factor

        wind_load = wind_pressure * total_diameter
        effective_load = self.conductor.unit_weight  # we're converting from kN/m in daN/m
        if with_ice:
            effective_load += self.ice_weight

        return CatenaryApparentLoad(wind_load, effective_load)

    def overload_factor(self, apparent_load: CatenaryApparentLoad) -> float:
        """Returns the ratio of resultant load to the conductor's weight.

        Args:
            apparent_load: Apparent load including wind and ice.

        Returns:
            float: Overload factor (dimensionless).
        """

        return apparent_load.resultant / self.conductor.unit_weight

    def ruling_span(self, spans: list[float | int]) -> float:
        """Computes the ruling span for a set of spans.

        Args:
            spans: List of span lengths (m).

        Returns:
            float: Ruling span (m), weighted by cube of individual spans.
        """
        
        return math.sqrt(sum(pow(span, 3) for span in spans) / sum(spans))


@dataclass
class MechAnalysisHypothesis:
    """Represents a single hypothesis (scenario) for mechanical analysis."""

    temp: float
    rts_factor: float
    zone: MechAnalysisZone | None = None
    wind_speed: float = 0.
    with_ice: bool = False
    name: str | None = None


class SagTensionAnalyzer:
    """Generates sag-tension tables and finds controlling mechanical states."""

    def __init__(self, mech: MechAnalysis, hypotheses: list[MechAnalysisHypothesis]) -> None:
        """Initialize the sag-tension analyzer.

        Args:
            mech: Mechanical analysis object for the conductor.
            hypotheses: List of scenarios to evaluate.
        """
        self.mech = mech
        self.hypotheses = hypotheses

    def find_controlling_state(self, span: float | int) -> MechAnalysisHypothesis | None:
        """Find the hypothesis that controls the conductor tension for a span.

        Iteratively checks all hypotheses and returns the first one that does
        not violate allowable tension in any scenario.

        Args:
            span: Span length between supports (m).

        Returns:
            MechAnalysisHypothesis or None: Controlling hypothesis, if found.
        """

        sorted_hypos = sorted(self.hypotheses, key=lambda h: h.temp)
        for i, base_hypo in enumerate(sorted_hypos):

            base_overload = self.mech.overload(wind_speed=base_hypo.wind_speed, with_ice=base_hypo.with_ice)
            base_case = CatenaryState(temp=base_hypo.temp, weight=base_overload.resultant, tense=self.mech.conductor.rated_strength * base_hypo.rts_factor)

            violation_found = False
            for j, hypo in enumerate(sorted_hypos):
                if j == i:
                    continue
                overload = self.mech.overload(wind_speed=hypo.wind_speed, with_ice=hypo.with_ice)
                state1 = self.mech.cat.cos(state0=base_case, temp1=hypo.temp, weight1=overload.resultant, span=span)

                allowed_tense = hypo.rts_factor * self.mech.conductor.rated_strength
                if state1.tense >= allowed_tense:
                    violation_found = True
                    break
                
            if not violation_found:
                return base_hypo

        return None

    def tbl(self, spans: list[float] | list[int]):
        """Generate a sag-tension table for a list of spans.

        Args:
            spans: List of spans to compute (m).

        Returns:
            list[dict]: Each dict contains the span and a list of resulting tensions
            for each hypothesis.
        """
        tbl = []

        for span in spans:
            controller = self.find_controlling_state(span)
            if not controller:
                return None

            base_overload = self.mech.overload(wind_speed=controller.wind_speed, with_ice=controller.with_ice)
            base_state = CatenaryState(temp=controller.temp, weight=base_overload.resultant, tense=self.mech.conductor.rated_strength * controller.rts_factor)

            row = {"span": span, "results": []}

            for hypo in self.hypotheses:
                load = self.mech.overload(wind_speed=hypo.wind_speed, with_ice=hypo.with_ice)
                state1 = self.mech.cat.cos(state0=base_state, temp1=hypo.temp, weight1=load.resultant, span=span)

                row["results"].append(state1.tense)

            tbl.append(row)

        return tbl

