from typing import Dict, Literal
from backend.schemas import HouseholdFeatures

class MLService:
    @staticmethod
    def mock_predict_segment(features: HouseholdFeatures) -> Literal["A", "B", "C", "D"]:
        """Placeholder for Joel's clustering model (Issue #1 requirement)."""
        if features.consumption_kwh <= 40 and features.county_poverty_idx > 40:
            return "A"
        elif features.consumption_kwh <= 100:
            return "B"
        elif features.consumption_kwh <= 300:
            return "C"
        return "D"

class TariffLogicEngine:
    # ISSUE #5: REGULATORY LOCKING (March 2026 Rates) 
    FEC_RATE = 3.10          
    FOREX_RATE = 1.2061      
    VAT_RATE = 0.16          
    REP_RATE = 0.05          
    EPRA_RATE = 0.04         
    WARMA_RATE = 0.03        

    @classmethod
    def _calculate_pass_through_charges(cls, consumption_kwh: float, energy_charge: float) -> Dict[str, float]:
        fec = consumption_kwh * cls.FEC_RATE
        forex = consumption_kwh * cls.FOREX_RATE
        vat = cls.VAT_RATE * (energy_charge + fec + forex)
        rep = cls.REP_RATE * energy_charge
        epra = consumption_kwh * cls.EPRA_RATE
        warma = consumption_kwh * cls.WARMA_RATE

        return {
            "fec": round(fec, 2), "forex": round(forex, 2), "vat": round(vat, 2),
            "rep": round(rep, 2), "epra_levy": round(epra, 2), "warma_levy": round(warma, 2)
        }

    # ISSUE #2: TARIFF LOGIC IMPLEMENTATION (Baseline) [cite: 200, 201]
    @classmethod
    def calculate_baseline_bill(cls, consumption_kwh: float) -> Dict[str, float]:
        if consumption_kwh <= 30:
            energy_rate, fixed_charge = 12.22, 0.00
        elif consumption_kwh <= 100:
            energy_rate, fixed_charge = 16.30, 150.00
        else:
            energy_rate, fixed_charge = 20.97, 150.00

        energy_charge = consumption_kwh * energy_rate
        pass_throughs = cls._calculate_pass_through_charges(consumption_kwh, energy_charge)
        total_bill = energy_charge + fixed_charge + sum(pass_throughs.values())

        return {
            "energy_charge": round(energy_charge, 2), "fixed_charge": round(fixed_charge, 2),
            **pass_throughs, "total_bill": round(total_bill, 2)
        }

    # ISSUE #2: TARIFF LOGIC IMPLEMENTATION (Proposed) [cite: 203]
    @classmethod
    def calculate_proposed_bill(cls, consumption_kwh: float, segment: str, energy_rate: float, fixed_charge: float) -> Dict[str, float]:
        # ISSUE #2: Segment A defaults to 0 fixed charge [cite: 204]
        if segment == "A":
            fixed_charge = 0.00  

        energy_charge = consumption_kwh * energy_rate
        pass_throughs = cls._calculate_pass_through_charges(consumption_kwh, energy_charge)
        total_bill = energy_charge + fixed_charge + sum(pass_throughs.values())

        return {
            "energy_charge": round(energy_charge, 2), "fixed_charge": round(fixed_charge, 2),
            **pass_throughs, "total_bill": round(total_bill, 2)
        }