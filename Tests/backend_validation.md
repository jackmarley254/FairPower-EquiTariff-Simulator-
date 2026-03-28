# Backend Validation Tests

FairPower: EquiTariff API
Version: 1.0.0
OAS: 3.1
OpenAPI: /openapi.json
Description: Backend simulator for equitable tariff design.

## System

### GET /health — Health Check

Request:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'
```

Response (example):
```
HTTP/1.1 200 OK
{
  "status": "active",
  "message": "FairPower API is running"
}
```

Headers:
- content-type: application/json

---

## Tariff Simulator

### POST /calculate-tariff — Calculate Tariff

Request body (application/json):

```
{
  "household": {
    "household_id": "HH001",
    "consumption_kwh": 120,
    "income_proxy": 25000,
    "hh_size": 4,
    "county": "Kiambu",
    "county_poverty_idx": 0.42,
    "appliance_index": 3,
    "appliance_ownership": 2,
    "urban_rural": 1
  },
  "proposed_config": {
    "rates": {
      "A": {"energy_rate": 5.0, "fixed_charge": 100},
      "B": {"energy_rate": 7.0, "fixed_charge": 150},
      "C": {"energy_rate": 10.0, "fixed_charge": 200},
      "D": {"energy_rate": 12.0, "fixed_charge": 250}
    }
  }
}
```

Example curl:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/calculate-tariff' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '<body-above>'
```

Example response (200):
```
{
  "segment_label": "C",
  "baseline_bill": {
    "energy_charge": 2516.4,
    "fixed_charge": 150,
    "fec": 372,
    "forex": 144.73,
    "vat": 485.3,
    "rep": 125.82,
    "epra_levy": 4.8,
    "warma_levy": 3.6,
    "total_bill": 3802.65
  },
  "proposed_bill": {
    "energy_charge": 1200,
    "fixed_charge": 200,
    "fec": 372,
    "forex": 144.73,
    "vat": 274.68,
    "rep": 60,
    "epra_levy": 4.8,
    "warma_levy": 3.6,
    "total_bill": 2259.81
  },
  "baseline_energy_burden_pct": 15.21,
  "proposed_energy_burden_pct": 9.04,
  "exceeds_10pct_threshold": false
}
```

Possible responses: 200 (Successful Response), 422 (Validation Error).

---

### POST /simulate-scenario — Simulate Scenario

Request body (application/json):

```
{
  "households": [
    {
      "household_id": "HH001",
      "consumption_kwh": 30,
      "income_proxy": 8000,
      "hh_size": 3,
      "county": "Nakuru",
      "county_poverty_idx": 0.55,
      "appliance_index": 1,
      "appliance_ownership": 1,
      "urban_rural": 0
    },
    {
      "household_id": "HH002",
      "consumption_kwh": 90,
      "income_proxy": 15000,
      "hh_size": 5,
      "county": "Kiambu",
      "county_poverty_idx": 0.42,
      "appliance_index": 2,
      "appliance_ownership": 2,
      "urban_rural": 1
    },
    {
      "household_id": "HH003",
      "consumption_kwh": 250,
      "income_proxy": 40000,
      "hh_size": 6,
      "county": "Nairobi",
      "county_poverty_idx": 0.25,
      "appliance_index": 4,
      "appliance_ownership": 4,
      "urban_rural": 1
    }
  ],
  "proposed_config": {
    "rates": {
      "A": {"energy_rate": 5.0, "fixed_charge": 100},
      "B": {"energy_rate": 7.0, "fixed_charge": 150},
      "C": {"energy_rate": 10.0, "fixed_charge": 200},
      "D": {"energy_rate": 12.0, "fixed_charge": 250}
    }
  },
  "cost_to_serve_per_kwh": 6.5
}
```

Example response (200):
```
{
  "total_baseline_revenue": 10736.15,
  "total_proposed_revenue": 6415.47,
  "total_cost_to_serve": 2405,
  "revenue_reconciliation_ratio": 2.6676,
  "is_sustainable": true,
  "segment_metrics": {
    "A": {"household_count": 0, "total_revenue": 0, "avg_proposed_bill": 0},
    "B": {"household_count": 2, "total_revenue": 1924.21, "avg_proposed_bill": 962.11},
    "C": {"household_count": 1, "total_revenue": 4491.26, "avg_proposed_bill": 4491.26},
    "D": {"household_count": 0, "total_revenue": 0, "avg_proposed_bill": 0}
  }
}
```

Possible responses: 200 (Successful Response), 422 (Validation Error).

---

## Insights

### GET /segments — Get Segments

Example response (200):
```
{
  "A": {"name": "Vulnerable", "description": "Rural, high poverty index, highly sensitive to price changes.", "typical_consumption": "0 - 40 kWh", "appliance_profile": "Few appliances (e.g., lighting, radio)."},
  "B": {"name": "Lower-Middle", "description": "Urban moderate, growing consumption needs.", "typical_consumption": "41 - 100 kWh", "appliance_profile": "Basic appliances (e.g., TV, small fridge)."},
  "C": {"name": "Upper-Middle", "description": "Suburban, comfortable income levels.", "typical_consumption": "101 - 300 kWh", "appliance_profile": "Multiple appliances (e.g., washing machine, microwave)."},
  "D": {"name": "High Income", "description": "Urban elite, low price elasticity.", "typical_consumption": "300+ kWh", "appliance_profile": "All standard appliances, potentially AC/water heaters."}
}
```

### GET /metrics/affordability — Get Affordability Metrics

Example response (200):
```
{
  "national_poverty_rate": 39.8,
  "baseline_energy_burden_avg": 14.5,
  "target_burden_threshold": 10,
  "gini_coefficient_estimate": 0.45
}
```

---

## Recorded Test Runs

These are the actual requests and server responses captured while testing the running backend (timestamps from server headers).

### GET /health — Recorded Run

Request (curl):
```
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'
```

Request URL: http://127.0.0.1:8000/health

Server response: 200 OK

Response body:
```
{
  "status": "active",
  "message": "FairPower API is running"
}
```

Response headers:
```
content-length: 56
content-type: application/json
date: Sat,28 Mar 2026 10:35:23 GMT
server: uvicorn
```

### POST /calculate-tariff — Recorded Run

Request (curl):
```
curl -X 'POST' \
  'http://127.0.0.1:8000/calculate-tariff' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "household": {
    "household_id": "HH001",
    "consumption_kwh": 120,
    "income_proxy": 25000,
    "hh_size": 4,
    "county": "Kiambu",
    "county_poverty_idx": 0.42,
    "appliance_index": 3,
    "appliance_ownership": 2,
    "urban_rural": 1
  },
  "proposed_config": {
    "rates": {
      "A": {"energy_rate": 5.0, "fixed_charge": 100},
      "B": {"energy_rate": 7.0, "fixed_charge": 150},
      "C": {"energy_rate": 10.0, "fixed_charge": 200},
      "D": {"energy_rate": 12.0, "fixed_charge": 250}
    }
  }
}'
```

Request URL: http://127.0.0.1:8000/calculate-tariff

Server response: 200 OK

Response body:
```
{
  "segment_label": "C",
  "baseline_bill": {
    "energy_charge": 2516.4,
    "fixed_charge": 150,
    "fec": 372,
    "forex": 144.73,
    "vat": 485.3,
    "rep": 125.82,
    "epra_levy": 4.8,
    "warma_levy": 3.6,
    "total_bill": 3802.65
  },
  "proposed_bill": {
    "energy_charge": 1200,
    "fixed_charge": 200,
    "fec": 372,
    "forex": 144.73,
    "vat": 274.68,
    "rep": 60,
    "epra_levy": 4.8,
    "warma_levy": 3.6,
    "total_bill": 2259.81
  },
  "baseline_energy_burden_pct": 15.21,
  "proposed_energy_burden_pct": 9.04,
  "exceeds_10pct_threshold": false
}
```

Response headers:
```
content-length: 457
content-type: application/json
date: Sat,28 Mar 2026 10:25:57 GMT
server: uvicorn
```

### POST /simulate-scenario — Recorded Run

Request (curl):
```
curl -X 'POST' \
  'http://127.0.0.1:8000/simulate-scenario' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "households": [
    {
      "household_id": "HH001",
      "consumption_kwh": 30,
      "income_proxy": 8000,
      "hh_size": 3,
      "county": "Nakuru",
      "county_poverty_idx": 0.55,
      "appliance_index": 1,
      "appliance_ownership": 1,
      "urban_rural": 0
    },
    {
      "household_id": "HH002",
      "consumption_kwh": 90,
      "income_proxy": 15000,
      "hh_size": 5,
      "county": "Kiambu",
      "county_poverty_idx": 0.42,
      "appliance_index": 2,
      "appliance_ownership": 2,
      "urban_rural": 1
    },
    {
      "household_id": "HH003",
      "consumption_kwh": 250,
      "income_proxy": 40000,
      "hh_size": 6,
      "county": "Nairobi",
      "county_poverty_idx": 0.25,
      "appliance_index": 4,
      "appliance_ownership": 4,
      "urban_rural": 1
    }
  ],
  "proposed_config": {
    "rates": {
      "A": {"energy_rate": 5.0, "fixed_charge": 100},
      "B": {"energy_rate": 7.0, "fixed_charge": 150},
      "C": {"energy_rate": 10.0, "fixed_charge": 200},
      "D": {"energy_rate": 12.0, "fixed_charge": 250}
    }
  },
  "cost_to_serve_per_kwh": 6.5
}'
```

Request URL: http://127.0.0.1:8000/simulate-scenario

Server response: 200 OK

Response body:
```
{
  "total_baseline_revenue": 10736.15,
  "total_proposed_revenue": 6415.47,
  "total_cost_to_serve": 2405,
  "revenue_reconciliation_ratio": 2.6676,
  "is_sustainable": true,
  "segment_metrics": {
    "A": {"household_count": 0, "total_revenue": 0, "avg_proposed_bill": 0},
    "B": {"household_count": 2, "total_revenue": 1924.21, "avg_proposed_bill": 962.11},
    "C": {"household_count": 1, "total_revenue": 4491.26, "avg_proposed_bill": 4491.26},
    "D": {"household_count": 0, "total_revenue": 0, "avg_proposed_bill": 0}
  }
}
```

Response headers:
```
content-length: 472
content-type: application/json
date: Sat,28 Mar 2026 10:30:14 GMT
server: uvicorn
```

### GET /segments — Recorded Run

Request (curl):
```
curl -X 'GET' \
  'http://127.0.0.1:8000/segments' \
  -H 'accept: application/json'
```

Request URL: http://127.0.0.1:8000/segments

Server response: 200 OK

Response body:
```
{
  "A": {"name": "Vulnerable", "description": "Rural, high poverty index, highly sensitive to price changes.", "typical_consumption": "0 - 40 kWh", "appliance_profile": "Few appliances (e.g., lighting, radio)."},
  "B": {"name": "Lower-Middle", "description": "Urban moderate, growing consumption needs.", "typical_consumption": "41 - 100 kWh", "appliance_profile": "Basic appliances (e.g., TV, small fridge)."},
  "C": {"name": "Upper-Middle", "description": "Suburban, comfortable income levels.", "typical_consumption": "101 - 300 kWh", "appliance_profile": "Multiple appliances (e.g., washing machine, microwave)."},
  "D": {"name": "High Income", "description": "Urban elite, low price elasticity.", "typical_consumption": "300+ kWh", "appliance_profile": "All standard appliances, potentially AC/water heaters."}
}
```

Response headers:
```
content-length: 776
content-type: application/json
date: Sat,28 Mar 2026 10:35:45 GMT
server: uvicorn
```

### GET /metrics/affordability — Recorded Run

Request (curl):
```
curl -X 'GET' \
  'http://127.0.0.1:8000/metrics/affordability' \
  -H 'accept: application/json'
```

Request URL: http://127.0.0.1:8000/metrics/affordability

Server response: 200 OK

Response body:
```
{
  "national_poverty_rate": 39.8,
  "baseline_energy_burden_avg": 14.5,
  "target_burden_threshold": 10,
  "gini_coefficient_estimate": 0.45
}
```

Response headers:
```
content-length: 128
content-type: application/json
date: Sat,28 Mar 2026 10:36:06 GMT
server: uvicorn
```

---

## Notes
- Schemas: `AffordabilityMetricsResponse`, `BillBreakdown`, `CalculateTariffRequest`, `CalculateTariffResponse`, `SimulationScenarioRequest`, `SimulationScenarioResponse`, etc.
- Validate payloads produce 422 responses for invalid inputs.
