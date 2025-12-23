# main_multizone.py
import time
from agents.anomaly import SherlockAgent
from agents.solar import SolarProphetAgent
from agents.grid import GridOracleAgent
from agents.load import ComfortGuardianAgent
from agents.corrdinator import OrchestratorAgent
from building_zones import MultiZoneUniversity
from zone_data_generator import ZoneDataGenerator
from utils.hist_tracker import HistoricalTracker
from datetime import datetime
import pandas as pd

def run_multizone_simulation():
    """Run multi-zone simulation with per-zone agent decisions"""
    
    print("="*70)
    print("🏫 MULTI-ZONE UNIVERSITY ENERGY MANAGEMENT SYSTEM")
    print("="*70)
    
    # Initialize multi-zone campus
    campus = MultiZoneUniversity()
    zone_ids = campus.get_zone_ids()
    
    print(f"\n📍 Monitoring {len(zone_ids)} zones:")
    for zone_id in zone_ids:
        zone = campus.get_zone(zone_id)
        print(f"   - {zone.zone_name} ({zone.floor_area}m², capacity: {zone.occupancy_capacity})")
    
    # Initialize agents (one set per zone)
    print(f"\n🚀 Initializing {len(zone_ids)} AI Agent Teams...")
    zone_agents = {}
    for zone_id in zone_ids:
        zone_agents[zone_id] = {
            'sherlock': SherlockAgent(),
            'solar': SolarProphetAgent(),
            'grid': GridOracleAgent(),
            'comfort': ComfortGuardianAgent(),
            'orchestrator': OrchestratorAgent()
        }
    
    # Initialize tracking
    zone_trackers = {zone_id: HistoricalTracker() for zone_id in zone_ids}
    alerts = []
    
    # Generate or load forecast data
    print("\n📊 Loading forecast data...")
    forecast_data = ZoneDataGenerator.load_from_csv('zone_forecast_data.csv')
    
    if forecast_data is None:
        print("   Generating new forecast data...")
        generator = ZoneDataGenerator(datetime(2024, 3, 15, 8, 0), days=1)
        forecast_data = generator.save_to_csv('zone_forecast_data.csv')
    else:
        print(f"   Using cached data: {len(forecast_data)} timesteps")
    
    results = []
    
    # Simulate every hour
    for idx in range(0, len(forecast_data), 4):
        row = forecast_data.iloc[idx]
        current_time = row['timestamp']
        
        print(f"\n{'='*70}")
        print(f"🕐 Time: {current_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*70}")
        print(f"☀️  Solar: {row['solar_forecast']:.0f} kW | 💰 Price: ${row['electricity_price']:.3f}/kWh")
        
        # Process each zone independently
        zone_decisions = {}
        zone_hvac_powers = {}
        zone_occupancies = {}
        
        for zone_id in zone_ids:
            zone = campus.get_zone(zone_id)
            occupancy = int(row[f'{zone_id}_occupancy'])
            zone_occupancies[zone_id] = occupancy
            
            print(f"\n📍 {zone.zone_name}")
            
            # Get zone state
            zone_state = {
                'indoor_temp': float(zone.indoor_temp),
                'outdoor_temp': float(row['outdoor_temp']),
                'hvac_setpoint': float(zone.hvac_setpoint),
                'occupancy': int(occupancy),
                'solar_generation': 0,  # Will be allocated later
                'total_consumption': float(zone.base_load),
                'grid_used': 0,
                'hvac_power': 0
            }
            
            # Get historical baseline
            historical_avg = zone_trackers[zone_id].get_hourly_average(current_time.hour)
            
            # STEP 1: Anomaly Detection
            print(f"   🔍 Sherlock analyzing...")
            anomaly_report = zone_agents[zone_id]['sherlock'].analyze(
                current_time, zone_state, historical_avg
            )
            
            if anomaly_report.get('anomaly_detected', False):
                severity = anomaly_report.get('severity', 'unknown')
                print(f"   ⚠️  ANOMALY: {severity.upper()} - {anomaly_report.get('description', '')[:60]}")
                
                alerts.append({
                    'timestamp': current_time,
                    'zone_id': zone_id,
                    'zone_name': zone.zone_name,
                    'severity': severity,
                    'description': anomaly_report.get('description', ''),
                    'recommended_action': anomaly_report.get('recommended_action', '')
                })
                
                if anomaly_report.get('block_optimization', False):
                    print(f"   🚫 Safe mode - using defaults")
                    zone_decisions[zone_id] = {
                        'decision': 'Safe mode',
                        'hvac_setpoint': 22,
                        'anomaly_detected': True
                    }
                    zone_hvac_powers[zone_id] = 50
                    continue
            else:
                print(f"   ✅ No anomalies")
            
            # STEP 2: Agent Optimization
            print(f"   🤖 Agents optimizing...")
            
            # Future forecasts (simplified - proportional allocation)
            future_solar = [float(x) for x in forecast_data.iloc[idx:idx+16]['solar_forecast'].tolist()]
            future_prices = [{'time': f"+{i*15}min", 'price': float(p)} 
                            for i, p in enumerate(forecast_data.iloc[idx:idx+16]['electricity_price'].tolist())]
            future_carbon = [{'time': f"+{i*15}min", 'carbon_intensity': float(c)}
                            for i, c in enumerate(forecast_data.iloc[idx:idx+16]['grid_carbon_intensity'].tolist())]
            
            # Run agents
            solar_rec = zone_agents[zone_id]['solar'].analyze(current_time, future_solar, zone_state)
            time.sleep(0.3)
            
            grid_rec = zone_agents[zone_id]['grid'].analyze(current_time, future_prices, future_carbon, zone_state)
            if 'error' in grid_rec:
                grid_rec = {'recommendation': 'Maintain', 'priority': 'low'}
            time.sleep(0.3)
            
            comfort_rec = zone_agents[zone_id]['comfort'].analyze(current_time, zone_state, {})
            if 'error' in comfort_rec:
                comfort_rec = {'comfort_status': 'acceptable', 'constraints': {'min_temp': 20, 'max_temp': 24}}
            time.sleep(0.3)
            
            # Orchestrator decision
            decision = zone_agents[zone_id]['orchestrator'].coordinate(
                current_time,
                zone_state,
                {
                    'solar_prophet': solar_rec,
                    'grid_oracle': grid_rec,
                    'comfort_guardian': comfort_rec
                }
            )
            
            print(f"   ✅ Setpoint: {decision.get('hvac_setpoint', 22):.1f}°C | Current: {zone.indoor_temp:.1f}°C")
            
            zone_decisions[zone_id] = decision
            zone.hvac_setpoint = decision.get('hvac_setpoint', 22)
            
            # Calculate HVAC power needed
            temp_error = zone.hvac_setpoint - zone.indoor_temp
            hvac_power = max(-zone.hvac_capacity, min(zone.hvac_capacity, temp_error * 50))
            zone_hvac_powers[zone_id] = hvac_power
        
        # Simulate campus for this hour
        print(f"\n⚙️  Simulating campus...")
        for sub_idx in range(idx, min(idx+4, len(forecast_data))):
            sub_row = forecast_data.iloc[sub_idx]
            
            # Get sub-step occupancies
            sub_occupancies = {zone_id: int(sub_row[f'{zone_id}_occupancy']) 
                              for zone_id in zone_ids}
            
            # Simulate all zones
            sim_result = campus.simulate_step(
                zone_hvac_powers,
                sub_occupancies,
                float(sub_row['solar_forecast']),
                float(sub_row['outdoor_temp'])
            )
            
            # Store results
            for zone_id, zone_result in sim_result['zones'].items():
                result_row = {
                    'timestamp': sub_row['timestamp'],
                    'zone_id': zone_id,
                    'zone_name': campus.get_zone(zone_id).zone_name,
                    **zone_result,
                    'price': float(sub_row['electricity_price']),
                    'decision': zone_decisions[zone_id].get('decision', 'N/A'),
                    'anomaly_detected': zone_decisions[zone_id].get('anomaly_detected', False)
                }
                results.append(result_row)
                
                # Update tracker
                zone_trackers[zone_id].add_datapoint(sub_row['timestamp'], zone_result)
        
        # Print campus summary
        summary = sim_result['campus_summary']
        print(f"\n📊 Campus Summary:")
        print(f"   Total Consumption: {summary['total_consumption']:.1f} kW")
        print(f"   Solar Used: {summary['total_solar_used']:.1f} kW | Grid: {summary['total_grid_used']:.1f} kW")
    
    # Save results
    print(f"\n{'='*70}")
    print("💾 Saving results...")
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('multizone_results.csv', index=False)
    print(f"   ✅ Zone results: multizone_results.csv ({len(results)} records)")
    
    # Zone summary statistics
    zone_summary = results_df.groupby('zone_name').agg({
        'total_consumption': 'sum',
        'grid_used': 'sum',
        'solar_used': 'sum',
        'anomaly_detected': 'sum'
    }).round(2)
    zone_summary.to_csv('zone_summary.csv')
    print(f"   ✅ Zone summary: zone_summary.csv")
    
    # Save alerts
    if alerts:
        alerts_df = pd.DataFrame(alerts)
        alerts_df.to_csv('zone_alerts.csv', index=False)
        print(f"   ✅ Alerts: zone_alerts.csv ({len(alerts)} alerts)")
        
        print(f"\n🚨 ALERT SUMMARY:")
        for alert in alerts[:10]:  # Show first 10
            print(f"   [{alert['zone_name']}] {alert['timestamp'].strftime('%H:%M')} - "
                  f"{alert['severity'].upper()}: {alert['description'][:60]}")
    
    # Calculate costs
    total_cost = (results_df['grid_used'] * results_df['price']).sum() * 0.25
    total_energy = results_df['total_consumption'].sum() * 0.25
    
    print(f"\n{'='*70}")
    print(f"📊 SIMULATION COMPLETE")
    print(f"{'='*70}")
    print(f"💰 Total Cost: ${total_cost:.2f}")
    print(f"⚡ Total Energy: {total_energy:.2f} kWh")
    print(f"⚠️  Total Anomalies: {len(alerts)}")
    print(f"📁 Results saved to multizone_results.csv and zone_summary.csv")

if __name__ == "__main__":
    run_multizone_simulation()
