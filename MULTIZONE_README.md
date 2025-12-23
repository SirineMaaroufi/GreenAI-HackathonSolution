# Multi-Zone University Energy Management System

## 🏫 Overview

This system simulates a realistic university campus with **8 independent zones**, each with its own:
- Energy metering and consumption tracking
- HVAC control system
- AI agent team for optimization
- Anomaly detection specific to that zone

## 🗺️ Campus Zones

| Zone | Description | Area | Capacity | Usage Pattern |
|------|-------------|------|----------|---------------|
| **Engineering Building** | Classrooms & labs | 3000m² | 150 people | High daytime usage (8am-6pm) |
| **Main Library** | Study & research | 2500m² | 200 people | Extended hours (9am-10pm) |
| **Administration** | Offices | 2000m² | 80 people | Business hours only (8am-5pm) |
| **Science Floor 1** | Labs & classrooms | 1500m² | 100 people | Daytime with equipment loads |
| **Science Floor 2** | Labs & classrooms | 1500m² | 100 people | Daytime with equipment loads |
| **Student Cafeteria** | Dining | 1000m² | 250 people | Meal peaks (7-9am, 12-2pm, 6-7pm) |
| **Dormitories East** | Student housing | 2000m² | 120 people | High nighttime occupancy |
| **Dormitories West** | Student housing | 2000m² | 120 people | High nighttime occupancy |

## 🚀 Quick Start

### 1. Generate Forecast Data (First Time)

```bash
python generate_zone_data.py
```

This creates `zone_forecast_data.csv` with realistic zone-specific data for 24 hours.

**Options:**
- Generate 7 days: `python generate_zone_data.py 7`
- Custom filename: `python generate_zone_data.py 1 my_data.csv`

### 2. Run Multi-Zone Simulation

```bash
python main_multizone.py
```

This will:
- Automatically use cached data from `zone_forecast_data.csv` (if exists)
- Or generate new data and save it (if not found)
- Simulate all 8 zones for the entire dataset
- Run independent AI agent teams for each zone
- Detect zone-specific anomalies
- Generate detailed results files

### 3. Visualize Results

```bash
python visualize_zones.py
```

Creates a comprehensive dashboard showing:
- Energy consumption by zone
- Hourly patterns for each zone
- Solar vs grid usage
- Temperature control effectiveness
- Anomaly locations
- Cost breakdown by zone

## 📊 Output Files

After running the simulation:

1. **zone_forecast_data.csv** - Generated forecast data (cached for reuse)
   - Columns: timestamp, solar_forecast, outdoor_temp, electricity_price, carbon_intensity
   - Plus: occupancy columns for each zone (engineering_occupancy, library_occupancy, etc.)
   
2. **multizone_results.csv** - Detailed timestep data for all zones
   - Columns: timestamp, zone_id, zone_name, consumption, temperature, etc.
   
3. **zone_summary.csv** - Aggregated statistics per zone
   - Total consumption, solar/grid split, anomaly count
   
3. **zone_alerts.csv** - All anomalies detected
   - Timestamp, zone name, severity, description, recommended action
   
4. **multizone_dashboard.png** - Visual dashboard (after running visualize_zones.py)

## 🎯 Key Features

### Zone-Specific Optimization
- Each zone has its own AI agent team
- Decisions tailored to zone occupancy and usage patterns
- Independent HVAC setpoints per zone

### Intelligent Solar Allocation
- Campus-wide solar generation (300 kW peak)
- Proportionally distributed to zones based on demand
- Optimizes self-consumption

### Precise Anomaly Detection
- Sherlock identifies **which specific zone** has issues
- Zone-specific baselines for better accuracy
- Examples:
  - "Engineering Building: High consumption with low occupancy"
  - "Library: Temperature sensor malfunction"
  - "Cafeteria: Wasteful cooling during closed hours"

### Realistic Usage Patterns
- **Academic buildings**: High 8am-6pm, low evenings/weekends
- **Library**: Extended hours, moderate weekend usage
- **Cafeteria**: Meal-time peaks
- **Dormitories**: Inverse pattern - high at night, low during day
- **Admin**: Strict business hours

## 🔧 Architecture

```
building_zones.py          - Zone and multi-zone campus classes
zone_data_generator.py     - Realistic per-zone data generation
main_multizone.py          - Main simulation loop
visualize_zones.py         - Analysis and visualization
agents/                    - AI agents (anomaly, solar, grid, comfort, orchestrator)
utils/                     - Historical tracking utilities
```

## 📈 Example Use Cases

### 1. Identify Problem Zones
```
ALERT: Engineering Building - HIGH severity
- Consumption 2.5x normal for 10:00 AM
- Only 15 occupants but HVAC at max capacity
- Recommended: Check HVAC system for malfunction
```

### 2. Optimize Solar Usage
```
12:00 PM - High solar generation (280 kW)
- Library: Pre-cooling to 20°C (surplus available)
- Engineering: Standard cooling (peak class time)
- Dorms: Minimal HVAC (empty during day)
```

### 3. Cost Optimization by Zone
```
Most Expensive Zones:
1. Engineering Building: $45.23 (24h)
2. Main Library: $38.91
3. Science Floor 1: $32.15

Recommendation: Focus optimization efforts on top 3 zones
```

## 🆚 Comparison to Original

| Feature | Original | Multi-Zone |
|---------|----------|------------|
| Granularity | Single building | 8 independent zones |
| Agent teams | 1 set | 8 sets (one per zone) |
| Anomaly detection | Campus-wide | Zone-specific |
| Data realism | Generic | Zone-specific patterns |
| Action precision | Campus HVAC | Per-zone HVAC |

## 🔬 Extending the System

### Add a New Zone

Edit `building_zones.py`:

```python
'new_zone': BuildingZone('new_zone', 'New Building Name', 2000, 100)
```

Edit `zone_data_generator.py`:

```python
'new_zone': {'peak_hours': (9, 17), 'evening_activity': 0.2, 'weekend_factor': 0.1}
```

### Modify Zone Behavior

Each zone has independent:
- `floor_area` - Affects thermal mass and base load
- `occupancy_capacity` - Max occupants
- `hvac_capacity` - Max heating/cooling power
- Usage profile in `zone_data_generator.py`

## 💡 Tips

1. **Run for longer periods** - Change `days=1` to `days=7` in main_multizone.py
2. **Focus on specific zones** - Filter results by `zone_id` in the CSV
3. **Compare zones** - Use zone_summary.csv for quick comparison
4. **Monitor anomalies** - zone_alerts.csv shows exactly where problems occur

## 📝 Notes

- Simulation runs hourly (can adjust by changing step size in main_multizone.py)
- Solar allocation is proportional to zone demand
- Each zone maintains independent temperature control
- Historical tracking per zone enables better anomaly detection

---

**Ready to simulate?** Run `python main_multizone.py` 🚀
