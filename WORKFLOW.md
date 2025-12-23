# Multi-Zone System Workflow

## 📋 Data Flow and Usage

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: GENERATE FORECAST DATA (One Time)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  python generate_zone_data.py [days]                   │
│                                                         │
│  Creates: zone_forecast_data.csv                       │
│  ├─ timestamp                                          │
│  ├─ solar_forecast                                     │
│  ├─ outdoor_temp                                       │
│  ├─ electricity_price                                  │
│  ├─ grid_carbon_intensity                              │
│  ├─ engineering_occupancy                              │
│  ├─ library_occupancy                                  │
│  ├─ admin_occupancy                                    │
│  ├─ science_floor1_occupancy                           │
│  ├─ science_floor2_occupancy                           │
│  ├─ cafeteria_occupancy                                │
│  ├─ dorms_east_occupancy                               │
│  └─ dorms_west_occupancy                               │
│                                                         │
│  💡 Reusable: Generate once, use many times            │
│     Regenerate when you want different scenarios       │
│                                                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2: RUN SIMULATION (Uses Cached Data)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  python main_multizone.py                              │
│                                                         │
│  1. Loads: zone_forecast_data.csv                      │
│     (or generates if not found)                        │
│                                                         │
│  2. For each zone (8 total):                           │
│     ├─ Initialize AI agents                            │
│     ├─ Sherlock: Detect anomalies                      │
│     ├─ Solar Prophet: Solar optimization               │
│     ├─ Grid Oracle: Price/carbon optimization          │
│     ├─ Comfort Guardian: Temperature control           │
│     └─ Orchestrator: Final decision                    │
│                                                         │
│  3. Simulate building physics                          │
│     ├─ HVAC operation                                  │
│     ├─ Temperature dynamics                            │
│     └─ Energy consumption                              │
│                                                         │
│  Creates:                                              │
│  ├─ multizone_results.csv (all timesteps, all zones)  │
│  ├─ zone_summary.csv (aggregated by zone)             │
│  └─ zone_alerts.csv (anomalies detected)              │
│                                                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3: VISUALIZE & ANALYZE (Optional)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  python visualize_zones.py                             │
│                                                         │
│  Loads: multizone_results.csv, zone_summary.csv       │
│                                                         │
│  Creates: multizone_dashboard.png                      │
│  ├─ Energy consumption by zone                         │
│  ├─ Hourly patterns                                    │
│  ├─ Solar vs grid usage                                │
│  ├─ Temperature control                                │
│  ├─ Anomaly locations                                  │
│  └─ Cost breakdown                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Typical Usage Patterns

### Pattern 1: First Time Setup
```bash
# Generate data
python generate_zone_data.py

# Run simulation (uses generated data)
python main_multizone.py

# Visualize
python visualize_zones.py
```

### Pattern 2: Testing Different Scenarios
```bash
# Scenario A: Normal day (weekday)
python generate_zone_data.py 1 weekday_data.csv
python main_multizone.py  # Edit to use weekday_data.csv

# Scenario B: Week with weekend
python generate_zone_data.py 7 week_data.csv
python main_multizone.py  # Edit to use week_data.csv
```

### Pattern 3: Multiple Runs with Same Data
```bash
# Generate once
python generate_zone_data.py

# Run multiple times with same data
python main_multizone.py  # Run 1
python main_multizone.py  # Run 2 (uses cached data)
python main_multizone.py  # Run 3 (uses cached data)

# Compare different agent configurations
```

## 📊 Data Reusability Benefits

✅ **Faster Development**
- Generate data once, test agents multiple times
- No waiting for data regeneration each run

✅ **Consistent Testing**
- Same forecast data = reproducible results
- Compare agent performance fairly

✅ **Scenario Library**
- Save different scenarios:
  - `heatwave_data.csv` (high temps)
  - `winter_data.csv` (low temps)
  - `weekend_data.csv` (low occupancy)
  - `exam_week_data.csv` (high library usage)

✅ **Debugging**
- Use same data to debug agent behavior
- Isolate simulation issues from data issues

## 💾 File Size Estimates

| Duration | Timesteps | File Size | Generation Time |
|----------|-----------|-----------|-----------------|
| 1 day    | 96        | ~15 KB    | <1 second       |
| 3 days   | 288       | ~45 KB    | ~2 seconds      |
| 7 days   | 672       | ~100 KB   | ~5 seconds      |
| 30 days  | 2,880     | ~450 KB   | ~20 seconds     |

## 🔧 Advanced: Custom Data Generation

Edit `generate_zone_data.py` to customize:

```python
# Different start date
start_date = datetime(2024, 12, 15, 8, 0)  # Winter break

# Longer duration
generator = ZoneDataGenerator(start_date, days=30)

# Custom parameters in zone_data_generator.py
# - Occupancy patterns
# - Peak hours
# - Weekend factors
```

## 🚀 Quick Commands Reference

```bash
# Basic workflow
python generate_zone_data.py        # Step 1: Generate data
python main_multizone.py            # Step 2: Run simulation
python visualize_zones.py           # Step 3: Visualize

# Generate longer datasets
python generate_zone_data.py 7      # 7 days
python generate_zone_data.py 30     # 30 days

# Test setup
python test_multizone_setup.py      # Validate everything works

# Compare approaches
python compare_systems.py           # See single vs multi-zone
```
