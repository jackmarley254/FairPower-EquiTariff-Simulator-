from pydantic import BaseModel, Field
from typing import Dict, Literal, List

# --- BASE DATA MODELS ---
class HouseholdFeatures(BaseModel):
    household_id: str = Field(..., description="Unique identifier [cite: 198]")
    consumption_kwh: float = Field(..., ge=0, description="Monthly consumption in kWh [cite: 198]")
    hh_size: int = Field(..., gt=0, description="Number of persons in household [cite: 198]")
    county: str = Field(..., description="County of residence [cite: 198]")
    urban_rural: int = Field(..., ge=0, le=1, description="1 = urban, 0 = rural [cite: 198]")
    county_poverty_idx: float = Field(..., ge=0, le=100, description="Percentage below poverty line in county [cite: 198]")
    income_proxy: float = Field(..., gt=0, description="Estimated monthly income [cite: 198]")
    appliance_ownership: int = Field(..., ge=0, le=10, description="Count of major appliances [cite: 198]")

class SegmentRates(BaseModel):
    energy_rate: float = Field(..., ge=0, description="Energy charge in KES/kWh [cite: 203]")
    fixed_charge: float = Field(..., ge=0, description="Fixed charge in KES [cite: 203]")

class ProposedTariffConfig(BaseModel):
    rates: Dict[Literal["A", "B", "C", "D"], SegmentRates] = Field(
        ..., description="Proposed rates for segments A-D [cite: 203]"
    )

# --- SINGLE CALCULATION (Issues #1 & #2) ---
class CalculateTariffRequest(BaseModel):
    household: HouseholdFeatures
    proposed_config: ProposedTariffConfig

class BillBreakdown(BaseModel):
    energy_charge: float
    fixed_charge: float
    fec: float
    forex: float
    vat: float
    rep: float
    epra_levy: float
    warma_levy: float
    total_bill: float

class CalculateTariffResponse(BaseModel):
    segment_label: Literal["A", "B", "C", "D"]
    baseline_bill: BillBreakdown
    proposed_bill: BillBreakdown
    baseline_energy_burden_pct: float
    proposed_energy_burden_pct: float
    exceeds_10pct_threshold: bool

# --- BATCH SIMULATION (Issue #3: Revenue Reconciliation) ---
class SimulationScenarioRequest(BaseModel):
    households: List[HouseholdFeatures] = Field(..., description="Batch of households")
    proposed_config: ProposedTariffConfig
    cost_to_serve_per_kwh: float = Field(15.00, description="Estimated utility cost to serve 1 kWh")

class SegmentMetrics(BaseModel):
    household_count: int
    total_revenue: float
    avg_proposed_bill: float

class SimulationScenarioResponse(BaseModel):
    total_baseline_revenue: float
    total_proposed_revenue: float
    total_cost_to_serve: float
    revenue_reconciliation_ratio: float = Field(..., description="Total Revenue / Total Cost ")
    is_sustainable: bool = Field(..., description="True if ratio is >= 1.0 ")
    segment_metrics: Dict[Literal["A", "B", "C", "D"], SegmentMetrics]