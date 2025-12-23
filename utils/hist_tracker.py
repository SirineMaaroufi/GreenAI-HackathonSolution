# utils/historical_tracker.py
import pandas as pd
import numpy as np

class HistoricalTracker:
    def __init__(self):
        self.history = []
        
    def add_datapoint(self, timestamp, building_state):
        """Add a data point to history"""
        self.history.append({
            'timestamp': timestamp,
            'consumption': building_state['total_consumption'],
            'occupancy': building_state['occupancy'],
            'indoor_temp': building_state['indoor_temp'],
            'hvac_power': building_state['hvac_power'],
            'solar_used': building_state.get('solar_used', building_state.get('solar_generation', 0))
        })
        
        # Keep only last 96 records (24 hours at 15-min intervals)
        if len(self.history) > 96:
            self.history = self.history[-96:]
    
    def get_hourly_average(self, current_hour):
        """Get average values for the same hour from history"""
        
        if len(self.history) < 4:
            # Not enough history, return current as baseline
            return {
                'avg_consumption': 50,
                'avg_occupancy': 50,
                'avg_hvac_power': 50
            }
        
        df = pd.DataFrame(self.history)
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        # Filter to same hour
        same_hour = df[df['hour'] == current_hour]
        
        if len(same_hour) == 0:
            same_hour = df  # Fallback to all data
        
        return {
            'avg_consumption': float(same_hour['consumption'].mean()),
            'avg_occupancy': float(same_hour['occupancy'].mean()),
            'avg_hvac_power': float(same_hour['hvac_power'].mean())
        }