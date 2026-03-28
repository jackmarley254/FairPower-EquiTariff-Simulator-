from fastapi import FastAPI, HTTPException
from typing import Literal

from backend.schemas import (
    CalculateTariffRequest, CalculateTariffResponse, 
    SimulationScenarioRequest, SimulationScenarioResponse, SegmentMetrics,
    SegmentDefinition, AffordabilityMetricsResponse
)
from backend.services import TariffLogicEngine, MLService

app = FastAPI(
    title="FairPower: EquiTariff API",
    description="Backend simulator for equitable tariff design.",
    version="1.0.0"
)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "active", "message": "FairPower API is running"}

@app.post("/calculate-tariff", response_model=CalculateTariffResponse, tags=["Tariff Simulator"])
async def calculate_tariff(request: CalculateTariffRequest):
    household = request.household
    proposed_config = request.proposed_config

    segment_label = MLService.mock_predict_segment(household)

    baseline_bill = TariffLogicEngine.calculate_baseline_bill(household.consumption_kwh)
    baseline_burden = (baseline_bill["total_bill"] / household.income_proxy) * 100

    try:
        segment_rates = proposed_config.rates[segment_label]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Missing rates for segment {segment_label}")

    proposed_bill = TariffLogicEngine.calculate_proposed_bill(
        consumption_kwh=household.consumption_kwh,
        segment=segment_label,
        energy_rate=segment_rates.energy_rate,
        fixed_charge=segment_rates.fixed_charge
    )
    proposed_burden = (proposed_bill["total_bill"] / household.income_proxy) * 100

    return CalculateTariffResponse(
        segment_label=segment_label,
        baseline_bill=baseline_bill,
        proposed_bill=proposed_bill,
        baseline_energy_burden_pct=round(baseline_burden, 2),
        proposed_energy_burden_pct=round(proposed_burden, 2),
        exceeds_10pct_threshold=proposed_burden > 10.0
    )

@app.post("/simulate-scenario", response_model=SimulationScenarioResponse, tags=["Tariff Simulator"])
async def simulate_scenario(request: SimulationScenarioRequest):
    """ISSUE #3: Revenue Reconciliation Batch Processing """
    total_baseline_revenue = 0.0
    total_proposed_revenue = 0.0
    total_kwh_consumed = 0.0
    
    # Initialize tracking metrics for segments
    seg_data = {
        "A": {"count": 0, "rev": 0.0}, "B": {"count": 0, "rev": 0.0},
        "C": {"count": 0, "rev": 0.0}, "D": {"count": 0, "rev": 0.0}
    }

    for household in request.households:
        total_kwh_consumed += household.consumption_kwh
        segment_label = MLService.mock_predict_segment(household)
        
        # Baseline
        baseline_bill = TariffLogicEngine.calculate_baseline_bill(household.consumption_kwh)
        total_baseline_revenue += baseline_bill["total_bill"]

        # Proposed
        rates = request.proposed_config.rates.get(segment_label)
        if not rates:
            continue
        
        proposed_bill = TariffLogicEngine.calculate_proposed_bill(
            consumption_kwh=household.consumption_kwh,
            segment=segment_label,
            energy_rate=rates.energy_rate,
            fixed_charge=rates.fixed_charge
        )
        total_proposed_revenue += proposed_bill["total_bill"]
        
        # Track Segment Data
        seg_data[segment_label]["count"] += 1
        seg_data[segment_label]["rev"] += proposed_bill["total_bill"]

    total_cost_to_serve = total_kwh_consumed * request.cost_to_serve_per_kwh
    ratio = total_proposed_revenue / total_cost_to_serve if total_cost_to_serve > 0 else 0

    metrics = {
        seg: SegmentMetrics(
            household_count=data["count"],
            total_revenue=round(data["rev"], 2),
            avg_proposed_bill=round(data["rev"] / data["count"], 2) if data["count"] > 0 else 0.0
        ) for seg, data in seg_data.items()
    }

    return SimulationScenarioResponse(
        total_baseline_revenue=round(total_baseline_revenue, 2),
        total_proposed_revenue=round(total_proposed_revenue, 2),
        total_cost_to_serve=round(total_cost_to_serve, 2),
        revenue_reconciliation_ratio=round(ratio, 4),
        is_sustainable=ratio >= 1.0,  # Sustainability threshold 
        segment_metrics=metrics
    )

@app.get("/segments", response_model=Dict[str, SegmentDefinition], tags=["Insights"])
async def get_segments():
    """Returns the definitions and profiles of the 4 household segments [cite: 153-157]."""
    return {
        "A": SegmentDefinition(
            name="Vulnerable",
            description="Rural, high poverty index, highly sensitive to price changes.",
            typical_consumption="0 - 40 kWh",
            appliance_profile="Few appliances (e.g., lighting, radio)."
        ),
        "B": SegmentDefinition(
            name="Lower-Middle",
            description="Urban moderate, growing consumption needs.",
            typical_consumption="41 - 100 kWh",
            appliance_profile="Basic appliances (e.g., TV, small fridge)."
        ),
        "C": SegmentDefinition(
            name="Upper-Middle",
            description="Suburban, comfortable income levels.",
            typical_consumption="101 - 300 kWh",
            appliance_profile="Multiple appliances (e.g., washing machine, microwave)."
        ),
        "D": SegmentDefinition(
            name="High Income",
            description="Urban elite, low price elasticity.",
            typical_consumption="300+ kWh",
            appliance_profile="All standard appliances, potentially AC/water heaters."
        )
    }

@app.get("/metrics/affordability", response_model=AffordabilityMetricsResponse, tags=["Insights"])
async def get_affordability_metrics():
    """
    Returns baseline affordability metrics for the dashboard's initial load.
    In production, this would calculate aggregates from the master dataset.
    """
    return AffordabilityMetricsResponse(
        national_poverty_rate=39.8,       # From KCHS 2022 Data [cite: 86-87]
        baseline_energy_burden_avg=14.5,  # Mock starting value > 10% threshold
        target_burden_threshold=10.0,
        gini_coefficient_estimate=0.45    # Mock starting inequality metric
    )