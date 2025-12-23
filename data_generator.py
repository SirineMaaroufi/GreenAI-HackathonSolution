# data_generator.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class CampusDataGenerator:
    def __init__(self, start_date, days=1):
        self.start_date = start_date
        self.days = days
        self.timesteps = int(days * 24 * 4)  # 15-min intervals
        
    def generate_dataset(self):
        """Generate 24h+ of synthetic campus data"""
        
        timestamps = [self.start_date + timedelta(minutes=15*i) 
                     for i in range(self.timesteps)]
        
        data = []
        for i, ts in enumerate(timestamps):
            hour = ts.hour + ts.minute / 60
            
            # Solar generation (sine wave, peak at noon)
            solar = self._generate_solar(hour)
            
            # Occupancy (low at night, high during day)
            occupancy = self._generate_occupancy(ts)
            
            # Outdoor temperature (sine wave, peak at 3pm)
            outdoor_temp = self._generate_temperature(hour)
            
            # Electricity price (high during peak hours)
            price = self._generate_price(hour)
            
            # Grid carbon intensity (varies by time)
            carbon_intensity = self._generate_carbon_intensity(hour)
            
            data.append({
                'timestamp': ts,
                'solar_forecast': solar,
                'occupancy_forecast': occupancy,
                'outdoor_temp': outdoor_temp,
                'electricity_price': price,
                'grid_carbon_intensity': carbon_intensity
            })
        
        return pd.DataFrame(data)
    
    def _generate_solar(self, hour):
        """Solar generation pattern (kW)"""
        if 6 <= hour <= 18:
            # Peak at noon (hour 12)
            return 150 * np.sin(np.pi * (hour - 6) / 12) * np.random.uniform(0.8, 1.0)
        return 0
    
    def _generate_occupancy(self, timestamp):
        """Occupancy pattern (number of people)"""
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        
        # Weekend vs weekday
        if day_of_week >= 5:  # Weekend
            return np.random.randint(5, 20)
        
        # Weekday patterns
        if 8 <= hour <= 17:  # Class hours
            return np.random.randint(50, 100)
        elif 17 < hour <= 22:  # Evening study
            return np.random.randint(20, 50)
        else:  # Night/early morning
            return np.random.randint(0, 10)
    
    def _generate_temperature(self, hour):
        """Outdoor temperature (°C)"""
        # Daily variation: min at 6am, max at 3pm
        base_temp = 18
        variation = 8 * np.sin(np.pi * (hour - 6) / 12)
        return base_temp + variation + np.random.uniform(-1, 1)
    
    def _generate_price(self, hour):
        """Electricity price ($/kWh)"""
        # Peak pricing: 9-11am and 5-8pm
        if (9 <= hour <= 11) or (17 <= hour <= 20):
            return np.random.uniform(0.25, 0.35)  # Peak
        elif 0 <= hour <= 6:
            return np.random.uniform(0.08, 0.12)  # Off-peak
        else:
            return np.random.uniform(0.15, 0.20)  # Mid-peak
    
    def _generate_carbon_intensity(self, hour):
        """Grid carbon intensity (gCO2/kWh)"""
        # Higher in evening (less solar on grid)
        if 17 <= hour <= 21:
            return np.random.uniform(600, 800)
        elif 10 <= hour <= 15:
            return np.random.uniform(300, 450)
        else:
            return np.random.uniform(450, 600)