# zone_data_generator.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class ZoneDataGenerator:
    """Generates realistic zone-specific occupancy and consumption patterns"""
    
    def __init__(self, start_date, days=1):
        self.start_date = start_date
        self.days = days
        self.timesteps = int(days * 24 * 4)  # 15-min intervals
        
        # Zone-specific profiles
        self.zone_profiles = {
            'engineering': {'peak_hours': (8, 18), 'evening_activity': 0.3, 'weekend_factor': 0.2},
            'library': {'peak_hours': (9, 22), 'evening_activity': 0.6, 'weekend_factor': 0.4},
            'admin': {'peak_hours': (8, 17), 'evening_activity': 0.1, 'weekend_factor': 0.05},
            'science_floor1': {'peak_hours': (8, 18), 'evening_activity': 0.2, 'weekend_factor': 0.15},
            'science_floor2': {'peak_hours': (8, 18), 'evening_activity': 0.2, 'weekend_factor': 0.15},
            'cafeteria': {'peak_hours': (11, 14), 'evening_activity': 0.4, 'weekend_factor': 0.5},
            'dorms_east': {'peak_hours': (18, 23), 'evening_activity': 0.8, 'weekend_factor': 0.9},
            'dorms_west': {'peak_hours': (18, 23), 'evening_activity': 0.8, 'weekend_factor': 0.9},
        }
        
    def generate_dataset(self):
        """Generate zone-specific data for entire campus"""
        
        timestamps = [self.start_date + timedelta(minutes=15*i) 
                     for i in range(self.timesteps)]
        
        data = []
        for i, ts in enumerate(timestamps):
            hour = ts.hour + ts.minute / 60
            
            # Campus-wide data
            solar = self._generate_solar(hour)
            outdoor_temp = self._generate_temperature(hour)
            price = self._generate_price(hour)
            carbon_intensity = self._generate_carbon_intensity(hour)
            
            # Zone-specific occupancy
            zone_occupancies = {}
            for zone_id, profile in self.zone_profiles.items():
                zone_occupancies[zone_id] = self._generate_zone_occupancy(ts, zone_id, profile)
            
            data.append({
                'timestamp': ts,
                'solar_forecast': solar,
                'outdoor_temp': outdoor_temp,
                'electricity_price': price,
                'grid_carbon_intensity': carbon_intensity,
                **{f'{zone_id}_occupancy': occ for zone_id, occ in zone_occupancies.items()}
            })
        
        return pd.DataFrame(data)
    
    def save_to_csv(self, filename='zone_forecast_data.csv'):
        """Generate and save dataset to CSV file"""
        print(f"📊 Generating zone forecast data...")
        data = self.generate_dataset()
        data.to_csv(filename, index=False)
        print(f"✅ Saved {len(data)} timesteps to {filename}")
        return data
    
    @staticmethod
    def load_from_csv(filename='zone_forecast_data.csv'):
        """Load previously generated dataset from CSV"""
        try:
            data = pd.read_csv(filename)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            print(f"✅ Loaded {len(data)} timesteps from {filename}")
            return data
        except FileNotFoundError:
            print(f"❌ File {filename} not found. Generate new data with save_to_csv()")
            return None
    
    def _generate_zone_occupancy(self, timestamp, zone_id, profile):
        """Generate realistic occupancy for specific zone"""
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        
        # Get zone capacity
        capacities = {
            'engineering': 150, 'library': 200, 'admin': 80,
            'science_floor1': 100, 'science_floor2': 100,
            'cafeteria': 250, 'dorms_east': 120, 'dorms_west': 120
        }
        capacity = capacities.get(zone_id, 100)
        
        # Weekend factor
        is_weekend = day_of_week >= 5
        weekend_mult = profile['weekend_factor'] if is_weekend else 1.0
        
        # Time-based occupancy
        peak_start, peak_end = profile['peak_hours']
        
        if peak_start <= hour <= peak_end:
            # Peak hours
            base_occupancy = np.random.uniform(0.5, 0.8) * capacity
        elif peak_end < hour <= 22:
            # Evening
            base_occupancy = profile['evening_activity'] * capacity * np.random.uniform(0.3, 0.7)
        else:
            # Night/early morning
            base_occupancy = np.random.uniform(0, 0.1) * capacity
        
        # Special case for cafeteria - meal peaks
        if zone_id == 'cafeteria':
            if 7 <= hour <= 9:  # Breakfast
                base_occupancy = capacity * np.random.uniform(0.3, 0.5)
            elif 11.5 <= hour <= 13.5:  # Lunch peak
                base_occupancy = capacity * np.random.uniform(0.7, 0.95)
            elif 17.5 <= hour <= 19:  # Dinner
                base_occupancy = capacity * np.random.uniform(0.5, 0.7)
            elif 19 < hour or hour < 7:
                base_occupancy = capacity * np.random.uniform(0, 0.05)
        
        # Dorms have inverse pattern - more people at night
        if 'dorm' in zone_id:
            if 0 <= hour <= 7 or hour >= 22:  # Sleep hours
                base_occupancy = capacity * np.random.uniform(0.7, 0.95)
            elif 8 <= hour <= 17:  # Class hours - mostly empty
                base_occupancy = capacity * np.random.uniform(0.1, 0.3)
            else:  # Evening - people returning
                base_occupancy = capacity * np.random.uniform(0.4, 0.7)
        
        final_occupancy = int(base_occupancy * weekend_mult)
        return max(0, final_occupancy)
    
    def _generate_solar(self, hour):
        """Solar generation pattern (kW)"""
        if 6 <= hour <= 18:
            return 300 * np.sin(np.pi * (hour - 6) / 12) * np.random.uniform(0.8, 1.0)
        return 0
    
    def _generate_temperature(self, hour):
        """Outdoor temperature (°C)"""
        base_temp = 18
        variation = 8 * np.sin(np.pi * (hour - 6) / 12)
        return base_temp + variation + np.random.uniform(-1, 1)
    
    def _generate_price(self, hour):
        """Electricity price ($/kWh)"""
        if (9 <= hour <= 11) or (17 <= hour <= 20):
            return np.random.uniform(0.25, 0.35)  # Peak
        elif 0 <= hour <= 6:
            return np.random.uniform(0.08, 0.12)  # Off-peak
        else:
            return np.random.uniform(0.15, 0.20)  # Mid-peak
    
    def _generate_carbon_intensity(self, hour):
        """Grid carbon intensity (gCO2/kWh)"""
        if 17 <= hour <= 21:
            return np.random.uniform(600, 800)
        elif 10 <= hour <= 15:
            return np.random.uniform(300, 450)
        else:
            return np.random.uniform(450, 600)
