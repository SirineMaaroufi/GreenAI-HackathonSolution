# main_simulation_with_sherlock.py
from agents.anomaly import SherlockAgent
from agents.solar import SolarProphetAgent
from agents.grid import GridOracleAgent
from agents.load import ComfortGuardianAgent
from agents.corrdinator import OrchestratorAgent
from building_model import UniversityBuilding
from data_generator import CampusDataGenerator
from utils.hist_tracker import HistoricalTracker
from datetime import datetime
import pandas as pd
import time

def run_multi_agent_simulation():
    """Run simulation with Sherlock anomaly detection"""
    
    # Initialize agents
    print("🚀 Initializing AI Agents...")
    sherlock = SherlockAgent()
    solar_agent = SolarProphetAgent()
    grid_agent = GridOracleAgent()
    comfort_agent = ComfortGuardianAgent()
    orchestrator = OrchestratorAgent()
    
    # Initialize tracking
    historical_tracker = HistoricalTracker()
    alerts = []
    
    # Generate forecast data
    generator = CampusDataGenerator(datetime(2024, 3, 15, 8, 0), days=1)
    forecast_data = generator.generate_dataset()
    
    # Initialize building
    building = UniversityBuilding()
    
    results = []
    
    # Simulate every hour (to save computation time during hackathon)
    for idx in range(0, len(forecast_data), 4):  # Every hour
        row = forecast_data.iloc[idx]
        current_time = row['timestamp']
        
        print(f"\n{'='*60}")
        print(f"🕐 Time: {current_time.strftime('%H:%M')}")
        print(f"{'='*60}")
        
        # Get building state (convert numpy types to native Python types for JSON serialization)
        building_state = {
            'indoor_temp': float(building.indoor_temp),
            'outdoor_temp': float(row['outdoor_temp']),
            'hvac_setpoint': float(building.hvac_setpoint),
            'occupancy': int(row['occupancy_forecast']),
            'solar_generation': float(row['solar_forecast']),
            'total_consumption': float(50 + abs(building.hvac_capacity * 0.3)),  # Simplified
            'grid_used': float(0),
            'hvac_power': float(building.hvac_capacity * 0.3)
        }
        
        # Get historical baseline
        historical_avg = historical_tracker.get_hourly_average(current_time.hour)
        
        # === STEP 1: SHERLOCK ANALYZES DATA ===
        print("🔍 Sherlock analyzing for anomalies...")
        start_time = time.time()
        
        anomaly_report = sherlock.analyze(current_time, building_state, historical_avg)
        
        print(f"   ⏱️  Analysis time: {time.time() - start_time:.2f}s")
        
        if anomaly_report.get('anomaly_detected', False):
            severity = anomaly_report.get('severity', 'unknown')
            print(f"   ⚠️  ANOMALY DETECTED: {severity.upper()}")
            print(f"   📋 {anomaly_report.get('description', 'Unknown issue')}")
            
            # Store alert
            alerts.append({
                'timestamp': current_time,
                'severity': severity,
                'description': anomaly_report.get('description', ''),
                'action': anomaly_report.get('recommended_action', ''),
                'alert_message': anomaly_report.get('alert_message', '')
            })
            
            # Should we block optimization?
            if anomaly_report.get('block_optimization', False):
                print(f"   🚫 BLOCKING optimization - Manual intervention required")
                
                # Skip agent optimization, use safe defaults
                decision = {
                    "decision": "Safe mode - anomaly detected",
                    "hvac_setpoint": 22,
                    "hvac_power": 50,
                    "reasoning": f"Sherlock detected anomaly: {anomaly_report.get('description')}",
                    "anomaly_mode": True
                }
                
                # Still simulate the building
                building.hvac_setpoint = decision['hvac_setpoint']
                
                for sub_idx in range(idx, min(idx+4, len(forecast_data))):
                    sub_row = forecast_data.iloc[sub_idx]
                    
                    result = building.simulate_step(
                        hvac_power=decision['hvac_power'],
                        solar_generation=sub_row['solar_forecast'],
                        occupancy=sub_row['occupancy_forecast'],
                        outdoor_temp=sub_row['outdoor_temp']
                    )
                    
                    result['timestamp'] = sub_row['timestamp']
                    result['price'] = sub_row['electricity_price']
                    result['agent_decision'] = decision['decision']
                    result['agent_reasoning'] = decision['reasoning']
                    result['anomaly_detected'] = True
                    result['anomaly_severity'] = severity
                    
                    results.append(result)
                    historical_tracker.add_datapoint(sub_row['timestamp'], result)
                
                continue  # Skip to next hour
        
        else:
            print(f"   ✅ No anomalies detected")
        
        # === STEP 2: NORMAL AGENT OPTIMIZATION ===
        print("🤖 Agents optimizing...")
        
        # Get forecasts (convert numpy types to native Python types)
        future_solar = [float(x) for x in forecast_data.iloc[idx:idx+16]['solar_forecast'].tolist()]
        future_prices = [{'time': f"+{i*15}min", 'price': float(p)} 
                        for i, p in enumerate(forecast_data.iloc[idx:idx+16]['electricity_price'].tolist())]
        future_carbon = [{'time': f"+{i*15}min", 'carbon_intensity': float(c)}
                        for i, c in enumerate(forecast_data.iloc[idx:idx+16]['grid_carbon_intensity'].tolist())]
        
        # Run agents sequentially with delays (Ollama doesn't parallelize well)
        solar_rec = solar_agent.analyze(current_time, future_solar, building_state)
        print(f"   ☀️  Solar Prophet: {solar_rec.get('recommendation', 'N/A')[:50]}...")
        time.sleep(0.5)  # Small delay between agents
        
        grid_rec = grid_agent.analyze(current_time, future_prices, future_carbon, building_state)
        if 'error' in grid_rec:
            grid_rec = {'recommendation': 'Maintain current operation', 'priority': 'low'}
        print(f"   ⚡ Grid Oracle: {grid_rec.get('recommendation', 'N/A')[:50]}...")
        time.sleep(0.5)  # Small delay between agents
        
        comfort_rec = comfort_agent.analyze(current_time, building_state, {})
        if 'error' in comfort_rec:
            comfort_rec = {'comfort_status': 'acceptable', 'constraints': {'min_temp': 20, 'max_temp': 24}}
        print(f"   🏠 Comfort Guardian: {comfort_rec.get('comfort_status', 'N/A')}")
        time.sleep(0.5)  # Small delay before orchestrator
        
        # Orchestrator decides
        print("🎯 Orchestrator deciding...")
        decision = orchestrator.coordinate(
            current_time,
            building_state,
            {
                'solar_prophet': solar_rec,
                'grid_oracle': grid_rec,
                'comfort_guardian': comfort_rec,
                'sherlock': anomaly_report
            }
        )
        
        print(f"   ✅ Decision: {decision.get('decision', 'N/A')[:60]}...")
        print(f"   🌡️  HVAC Setpoint: {decision['hvac_setpoint']}°C")
        
        # Apply decision and simulate
        building.hvac_setpoint = decision['hvac_setpoint']
        
        for sub_idx in range(idx, min(idx+4, len(forecast_data))):
            sub_row = forecast_data.iloc[sub_idx]
            
            # Simple HVAC controller
            temp_error = building.hvac_setpoint - building.indoor_temp
            hvac_power = max(-building.hvac_capacity, min(building.hvac_capacity, temp_error * 50))
            
            result = building.simulate_step(
                hvac_power=hvac_power,
                solar_generation=sub_row['solar_forecast'],
                occupancy=sub_row['occupancy_forecast'],
                outdoor_temp=sub_row['outdoor_temp']
            )
            
            result['timestamp'] = sub_row['timestamp']
            result['price'] = sub_row['electricity_price']
            result['agent_decision'] = decision.get('decision', 'N/A')
            result['agent_reasoning'] = decision.get('reasoning', 'N/A')
            result['anomaly_detected'] = False
            
            results.append(result)
            historical_tracker.add_datapoint(sub_row['timestamp'], result)
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('simulation_results.csv', index=False)
    
    # Save alerts
    if alerts:
        alerts_df = pd.DataFrame(alerts)
        alerts_df.to_csv('alerts_log.csv', index=False)
        
        print(f"\n⚠️  {len(alerts)} ALERTS GENERATED:")
        for alert in alerts:
            print(f"   - {alert['timestamp'].strftime('%H:%M')}: {alert['description']}")
    
    # Summary
    total_cost = (results_df['grid_used'] * results_df['price']).sum() * 0.25
    anomaly_count = results_df['anomaly_detected'].sum()
    
    print(f"\n{'='*60}")
    print(f"📊 SIMULATION COMPLETE")
    print(f"{'='*60}")
    print(f"💰 Total Cost: ${total_cost:.2f}")
    print(f"⚠️  Anomalies Detected: {anomaly_count}")
    print(f"📁 Results saved to: simulation_results.csv")
    if alerts:
        print(f"🚨 Alerts saved to: alerts_log.csv")

if __name__ == "__main__":
    run_multi_agent_simulation()