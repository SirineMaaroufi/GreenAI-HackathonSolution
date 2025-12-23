# simulate_building_data.py
"""
Building Physics Simulation - Run Once
Simulates building energy consumption for a month without AI agents
Saves raw data for later agent analysis
"""
from building_zones import MultiZoneUniversity
from zone_data_generator import ZoneDataGenerator
from datetime import datetime
import pandas as pd
import sys

def simulate_building_physics(days=30, output_file='building_simulation_data.csv'):
    """
    Simulate building physics without AI agents
    Runs simple rule-based HVAC control
    """
    
    print("="*70)
    print("🏗️  BUILDING PHYSICS SIMULATION (No AI Agents)")
    print("="*70)
    
    # Configuration
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except:
            print(f"⚠️  Invalid days parameter, using default: {days}")
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"\n⚙️  Configuration:")
    print(f"   Duration: {days} days")
    print(f"   Simulation interval: Every hour")
    print(f"   Output: {output_file}")
    print(f"   Total hours: {days * 24}")
    
    # Initialize campus
    campus = MultiZoneUniversity()
    zone_ids = campus.get_zone_ids()
    
    print(f"\n🏫 Simulating {len(zone_ids)} zones:")
    for zone_id in zone_ids:
        zone = campus.get_zone(zone_id)
        print(f"   • {zone.zone_name}")
    
    # Load or generate forecast data
    print(f"\n📊 Loading forecast data...")
    forecast_data = ZoneDataGenerator.load_from_csv('zone_forecast_data.csv')
    
    if forecast_data is None or len(forecast_data) < days * 24 * 4:
        print(f"   Generating new {days}-day forecast...")
        generator = ZoneDataGenerator(datetime(2024, 3, 15, 8, 0), days=days)
        forecast_data = generator.save_to_csv('zone_forecast_data.csv')
    else:
        # Trim to requested days
        forecast_data = forecast_data.iloc[:days * 24 * 4]
    
    print(f"   ✅ Using {len(forecast_data)} timesteps")
    
    # Initialize zone setpoints (rule-based, no AI)
    zone_setpoints = {zone_id: 22.0 for zone_id in zone_ids}  # Default 22°C
    
    results = []
    
    print(f"\n🔄 Running simulation...")
    print(f"   Progress: ", end='', flush=True)
    
    # Simulate every hour (every 4th row = 4 * 15min)
    total_hours = len(forecast_data) // 4
    progress_interval = max(total_hours // 20, 1)
    
    for hour_idx, idx in enumerate(range(0, len(forecast_data), 4)):
        row = forecast_data.iloc[idx]
        current_time = row['timestamp']
        
        # Progress indicator
        if hour_idx % progress_interval == 0:
            print("█", end='', flush=True)
        
        # Rule-based HVAC control (no AI agents)
        # Adjust setpoint based on occupancy and time of day
        hour = current_time.hour
        
        for zone_id in zone_ids:
            zone = campus.get_zone(zone_id)
            occupancy = int(row[f'{zone_id}_occupancy'])
            
            # Simple occupancy-based setpoint
            if occupancy > zone.occupancy_capacity * 0.5:
                # High occupancy - strict comfort
                zone_setpoints[zone_id] = 22.0
            elif occupancy > zone.occupancy_capacity * 0.2:
                # Medium occupancy - moderate comfort
                zone_setpoints[zone_id] = 22.5
            else:
                # Low occupancy - relaxed comfort (save energy)
                zone_setpoints[zone_id] = 23.0
            
            # Night setback for non-residential zones
            if hour < 6 or hour > 22:
                if 'dorm' not in zone_id:
                    zone_setpoints[zone_id] = 24.0  # Less cooling at night
            
            zone.hvac_setpoint = zone_setpoints[zone_id]
        
        # Calculate HVAC power for each zone
        zone_hvac_powers = {}
        zone_occupancies = {}
        
        for zone_id in zone_ids:
            zone = campus.get_zone(zone_id)
            occupancy = int(row[f'{zone_id}_occupancy'])
            zone_occupancies[zone_id] = occupancy
            
            # Simple proportional controller
            temp_error = zone.hvac_setpoint - zone.indoor_temp
            hvac_power = max(-zone.hvac_capacity, min(zone.hvac_capacity, temp_error * 50))
            zone_hvac_powers[zone_id] = hvac_power
        
        # Simulate all 15-min timesteps in this hour
        for sub_idx in range(idx, min(idx + 4, len(forecast_data))):
            sub_row = forecast_data.iloc[sub_idx]
            
            sub_occupancies = {zone_id: int(sub_row[f'{zone_id}_occupancy']) 
                              for zone_id in zone_ids}
            
            # Run simulation
            sim_result = campus.simulate_step(
                zone_hvac_powers,
                sub_occupancies,
                float(sub_row['solar_forecast']),
                float(sub_row['outdoor_temp'])
            )
            
            # Store results for each zone
            for zone_id, zone_result in sim_result['zones'].items():
                result_row = {
                    'timestamp': sub_row['timestamp'],
                    'zone_id': zone_id,
                    'zone_name': campus.get_zone(zone_id).zone_name,
                    'hvac_setpoint': zone_setpoints[zone_id],
                    **zone_result,
                    'solar_forecast': float(sub_row['solar_forecast']),
                    'outdoor_temp': float(sub_row['outdoor_temp']),
                    'electricity_price': float(sub_row['electricity_price']),
                    'grid_carbon_intensity': float(sub_row['grid_carbon_intensity'])
                }
                results.append(result_row)
    
    print(" ✅")
    
    # Save results
    print(f"\n💾 Saving simulation data...")
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    
    # Calculate statistics
    total_energy = results_df.groupby('zone_id')['total_consumption'].sum() * 0.25  # kWh
    total_cost = (results_df['grid_used'] * results_df['electricity_price']).sum() * 0.25
    
    print(f"\n📊 SIMULATION SUMMARY")
    print(f"="*70)
    print(f"Duration: {days} days ({len(results_df)} records)")
    print(f"Total Energy: {total_energy.sum():.2f} kWh")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"\nEnergy by Zone:")
    for zone_id, energy in total_energy.sort_values(ascending=False).items():
        zone_name = campus.get_zone(zone_id).zone_name
        print(f"   {zone_name:.<40} {energy:>10.2f} kWh")
    
    print(f"\n✅ Simulation complete!")
    print(f"📁 Data saved to: {output_file}")
    print(f"\n🚀 Next step: Run agent analysis")
    print(f"   python main_multizone.py")

if __name__ == "__main__":
    simulate_building_physics()
