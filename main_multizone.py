# main_multizone.py
"""
AI Agent Analysis on Pre-Simulated Building Data
Runs agents on selected time points to analyze and optimize
"""
import time
import pandas as pd
from agents.anomaly import SherlockAgent as AnomalyDetector
from agents.solar import SolarProphetAgent as PVGenerationAgent
from agents.grid import GridOracleAgent as CostEfficiencyAgent
from agents.load import ComfortGuardianAgent as ComfortAgent
from agents.corrdinator import OrchestratorAgent
from building_zones import MultiZoneUniversity
from utils.hist_tracker import HistoricalTracker

def select_analysis_timepoints(data, num_points=5):
    """
    Select representative time points across the day for analysis
    Default: Morning, Mid-morning, Noon, Afternoon, Evening
    """
    # Group by date and hour
    data['date'] = pd.to_datetime(data['timestamp']).dt.date
    data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
    
    # Select specific hours: 8am, 10am, 12pm, 3pm, 6pm
    target_hours = [8, 10, 12, 15, 18]
    
    # Get first occurrence of each target hour for each zone
    timepoints = []
    for target_hour in target_hours:
        matches = data[data['hour'] == target_hour]
        if len(matches) > 0:
            # Get timestamp from first day
            first_match = matches.iloc[0]['timestamp']
            timepoints.append({
                'timestamp': first_match,
                'hour': target_hour,
                'label': f"{target_hour:02d}:00"
            })
    
    return timepoints

def analyze_timepoint(timestamp, simulation_data, campus, zone_agents, zone_trackers, active_zone_ids):
    """
    Run AI agent analysis for a specific timepoint
    """
    # Get data for this timestamp (all zones)
    timepoint_data = simulation_data[simulation_data['timestamp'] == timestamp]
    
    if len(timepoint_data) == 0:
        print(f"   ⚠️  No data found for {timestamp}")
        return None
    
    # Use only the active zones (for testing)
    zone_ids = active_zone_ids
    recommendations = {}
    alerts = []
    
    print(f"\n{'='*70}")
    print(f"🕐 Analyzing: {timestamp.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")
    
    # Get campus-wide context
    sample_row = timepoint_data.iloc[0]
    print(f"☀️  Solar: {sample_row['solar_forecast']:.0f} kW | "
          f"💰 Price: ${sample_row['electricity_price']:.3f}/kWh | "
          f"🌡️  Outdoor: {sample_row['outdoor_temp']:.1f}°C")
    
    # Analyze each zone
    for zone_id in zone_ids:
        zone = campus.get_zone(zone_id)
        zone_data = timepoint_data[timepoint_data['zone_id'] == zone_id].iloc[0]
        
        print(f"\n📍 {zone.zone_name}")
        print(f"   Indoor: {zone_data['indoor_temp']:.1f}°C | "
              f"Setpoint: {zone_data['hvac_setpoint']:.1f}°C | "
              f"Occupancy: {int(zone_data['occupancy'])}")
        print(f"   Consumption: {zone_data['total_consumption']:.1f} kW | "
              f"Grid: {zone_data['grid_used']:.1f} kW")
        
        # Build zone state
        zone_state = {
            'indoor_temp': float(zone_data['indoor_temp']),
            'outdoor_temp': float(zone_data['outdoor_temp']),
            'hvac_setpoint': float(zone_data['hvac_setpoint']),
            'occupancy': int(zone_data['occupancy']),
            'solar_generation': float(zone_data['solar_used']),
            'total_consumption': float(zone_data['total_consumption']),
            'grid_used': float(zone_data['grid_used']),
            'hvac_power': float(zone_data['hvac_power'])
        }
        
        # Get historical baseline
        hour = pd.to_datetime(timestamp).hour
        historical_avg = zone_trackers[zone_id].get_hourly_average(hour)
        
        # === ANOMALY DETECTION ===
        print(f"   🔍 Anomaly Detector analyzing...")
        anomaly_report = zone_agents[zone_id]['anomaly'].analyze(
            timestamp, zone_state, historical_avg
        )
        
        if anomaly_report.get('anomaly_detected', False):
            severity = anomaly_report.get('severity', 'unknown')
            print(f"   ⚠️  ANOMALY: {severity.upper()}")
            print(f"      {anomaly_report.get('description', '')[:70]}")
            
            alerts.append({
                'timestamp': timestamp,
                'zone_id': zone_id,
                'zone_name': zone.zone_name,
                'severity': severity,
                'description': anomaly_report.get('description', ''),
                'recommended_action': anomaly_report.get('recommended_action', '')
            })
        else:
            print(f"   ✅ No anomalies")
        
        # === OPTIMIZATION RECOMMENDATIONS ===
        print(f"   🤖 Getting agent recommendations...")
        
        # Get future data (next 4 hours from simulation)
        future_data = simulation_data[
            (simulation_data['timestamp'] > timestamp) & 
            (simulation_data['zone_id'] == zone_id)
        ].head(16)  # Next 4 hours
        
        if len(future_data) > 0:
            future_solar = future_data['solar_forecast'].tolist()
            future_prices = [{'time': f"+{i*15}min", 'price': float(p)} 
                            for i, p in enumerate(future_data['electricity_price'].tolist())]
            future_carbon = [{'time': f"+{i*15}min", 'carbon_intensity': float(c)}
                            for i, c in enumerate(future_data['grid_carbon_intensity'].tolist())]
        else:
            future_solar = [0] * 16
            future_prices = [{'time': f"+{i*15}min", 'price': 0.15} for i in range(16)]
            future_carbon = [{'time': f"+{i*15}min", 'carbon_intensity': 500} for i in range(16)]
        
        # Run agents
        print(f"      🤖 Calling PV Generation Agent LLM...")
        solar_rec = zone_agents[zone_id]['pv'].analyze(timestamp, future_solar, zone_state)
        print(f"         ✅ PV Generation: {solar_rec.get('recommendation', 'N/A')}")
        time.sleep(0.3)
        
        print(f"      🤖 Calling Cost Efficiency Agent LLM...")
        cost_rec = zone_agents[zone_id]['cost'].analyze(timestamp, future_prices, future_carbon, zone_state)
        if 'error' in cost_rec:
            cost_rec = {'recommendation': 'Maintain operation', 'priority': 'low'}
        print(f"         ✅ Cost Efficiency: {cost_rec.get('recommendation', 'N/A')}")
        time.sleep(0.3)
        
        print(f"      🤖 Calling Comfort Agent LLM...")
        comfort_rec = zone_agents[zone_id]['comfort'].analyze(timestamp, zone_state, {})
        if 'error' in comfort_rec:
            comfort_rec = {'comfort_status': 'acceptable', 'constraints': {'min_temp': 20, 'max_temp': 24}}
        print(f"         ✅ Comfort Agent: {comfort_rec.get('comfort_status', 'N/A')}")
        time.sleep(0.3)
        
        # Orchestrator decision
        print(f"      🤖 Calling Orchestrator LLM...")
        decision = zone_agents[zone_id]['orchestrator'].coordinate(
            timestamp,
            zone_state,
            {
                'pv_generation': solar_rec,
                'cost_efficiency': cost_rec,
                'comfort': comfort_rec
            }
        )
        print(f"         ✅ Orchestrator decision: Setpoint {decision.get('hvac_setpoint', 22):.1f}°C")
        print(f"         🔍 DEBUG - Full decision: {decision}")
        
        print(f"\n   📝 FINAL RECOMMENDATION: Setpoint {decision.get('hvac_setpoint', 22):.1f}°C")
        print(f"      Reasoning: {decision.get('reasoning', 'N/A')}")
        
        recommendations[zone_id] = {
            'current_setpoint': float(zone_data['hvac_setpoint']),
            'recommended_setpoint': decision.get('hvac_setpoint', 22),
            'decision': decision.get('decision', 'N/A'),
            'reasoning': decision.get('reasoning', 'N/A'),
            'pv_rec': solar_rec.get('recommendation', 'N/A'),
            'cost_rec': cost_rec.get('recommendation', 'N/A'),
            'comfort_status': comfort_rec.get('comfort_status', 'N/A')
        }
    
    return {
        'timestamp': timestamp,
        'recommendations': recommendations,
        'alerts': alerts
    }

def run_multizone_analysis():
    """
    Analyze pre-simulated building data with AI agents
    """
    print("="*70)
    print("🤖 MULTI-ZONE AI AGENT ANALYSIS")
    print("="*70)
    
    # Load pre-simulated building data
    print("\n📂 Loading pre-simulated building data...")
    try:
        simulation_data = pd.read_csv('building_simulation_data.csv')
        simulation_data['timestamp'] = pd.to_datetime(simulation_data['timestamp'])
        print(f"   ✅ Loaded {len(simulation_data)} records")
        print(f"   Date range: {simulation_data['timestamp'].min()} to {simulation_data['timestamp'].max()}")
    except FileNotFoundError:
        print("   ❌ Error: building_simulation_data.csv not found!")
        print("   Run: python simulate_building_data.py")
        return
    
    # Initialize campus and agents
    campus = MultiZoneUniversity()
    all_zone_ids = campus.get_zone_ids()
    
    # FOR TESTING: Use only 2 zones
    zone_ids = ['engineering', 'library']  # Test with just 2 zones
    print(f"\n🧪 TEST MODE: Running on {len(zone_ids)} zones only: {zone_ids}")
    print(f"   (Full campus has {len(all_zone_ids)} zones)")
    
    print(f"\n🚀 Initializing AI agents for {len(zone_ids)} zones...")
    zone_agents = {}
    for zone_id in zone_ids:
        zone_agents[zone_id] = {
            'anomaly': AnomalyDetector(),
            'pv': PVGenerationAgent(),
            'cost': CostEfficiencyAgent(),
            'comfort': ComfortAgent(),
            'orchestrator': OrchestratorAgent()
        }
    print("   ✅ Agents initialized")
    
    # Build historical context from simulation data
    print(f"\n📚 Building historical context...")
    zone_trackers = {zone_id: HistoricalTracker() for zone_id in zone_ids}
    
    for zone_id in zone_ids:
        zone_data = simulation_data[simulation_data['zone_id'] == zone_id]
        for _, row in zone_data.iterrows():
            state = {
                'total_consumption': row['total_consumption'],
                'occupancy': row['occupancy'],
                'indoor_temp': row['indoor_temp'],
                'hvac_power': row['hvac_power'],
                'solar_used': row['solar_used']
            }
            zone_trackers[zone_id].add_datapoint(row['timestamp'], state)
    print("   ✅ Historical baselines ready")
    
    # Select analysis timepoints
    print(f"\n⏰ Selecting analysis timepoints...")
    timepoints = select_analysis_timepoints(simulation_data, num_points=5)
    print(f"   Selected {len(timepoints)} timepoints:")
    for tp in timepoints:
        print(f"      • {tp['label']} - {tp['timestamp']}")
    
    # Run analysis on selected timepoints
    all_recommendations = []
    all_alerts = []
    
    for tp in timepoints:
        result = analyze_timepoint(
            tp['timestamp'],
            simulation_data,
            campus,
            zone_agents,
            zone_trackers,
            zone_ids  # Pass the active zone_ids
        )
        
        if result:
            all_recommendations.append(result)
            all_alerts.extend(result['alerts'])
    
    # Save analysis results
    print(f"\n{'='*70}")
    print("💾 Saving analysis results...")
    
    # Save recommendations
    rec_records = []
    for result in all_recommendations:
        for zone_id, rec in result['recommendations'].items():
            rec_records.append({
                'timestamp': result['timestamp'],
                'zone_id': zone_id,
                **rec
            })
    
    rec_df = pd.DataFrame(rec_records)
    rec_df.to_csv('agent_recommendations.csv', index=False)
    print(f"   ✅ Recommendations: agent_recommendations.csv")
    
    # Save alerts
    if all_alerts:
        alerts_df = pd.DataFrame(all_alerts)
        alerts_df.to_csv('zone_alerts.csv', index=False)
        print(f"   ✅ Alerts: zone_alerts.csv ({len(all_alerts)} alerts)")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 ANALYSIS SUMMARY")
    print(f"{'='*70}")
    print(f"Timepoints analyzed: {len(timepoints)}")
    print(f"Zones analyzed: {len(zone_ids)}")
    print(f"Total recommendations: {len(rec_records)}")
    print(f"Anomalies detected: {len(all_alerts)}")
    
    if all_alerts:
        print(f"\n🚨 ALERTS BY ZONE:")
        alerts_by_zone = pd.DataFrame(all_alerts).groupby('zone_name').size()
        for zone_name, count in alerts_by_zone.sort_values(ascending=False).items():
            print(f"   {zone_name}: {count}")
    
    print(f"\n✅ Analysis complete!")

if __name__ == "__main__":
    run_multizone_analysis()
