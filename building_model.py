# building_model.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class UniversityBuilding:
    def __init__(self):
        # Building parameters
        self.floor_area = 5000  # square meters
        self.thermal_mass = 500  # kWh/°C (how much energy to change temp)
        self.base_load = 50  # kW (lights, computers, etc.)
        self.hvac_capacity = 200  # kW max cooling/heating
        self.solar_capacity = 150  # kW peak
        
        # State variables
        self.indoor_temp = 22  # °C
        self.hvac_setpoint = 22
        self.outdoor_temp = 20
        
    def simulate_step(self, hvac_power, solar_generation, occupancy, outdoor_temp, dt=0.25):
        """Simulate one time step (dt in hours)"""
        
        # Update outdoor temperature
        self.outdoor_temp = outdoor_temp
        
        # Calculate occupancy heat gain (people generate heat)
        occupancy_heat = occupancy * 0.1  # kW per person
        
        # Calculate base electrical load based on occupancy
        base_consumption = self.base_load * (0.3 + 0.7 * occupancy / 100)
        
        # HVAC heat transfer
        temp_diff = self.indoor_temp - self.outdoor_temp
        heat_loss = temp_diff * 0.5  # kW lost to outside
        
        # Temperature change from HVAC
        hvac_effect = hvac_power / self.thermal_mass
        
        # Temperature change from heat loss and gains
        natural_change = (heat_loss + occupancy_heat) / self.thermal_mass
        
        # Update indoor temperature
        self.indoor_temp += (hvac_effect - natural_change) * dt
        
        # Total building consumption
        total_consumption = base_consumption + abs(hvac_power)
        
        # Grid vs solar split
        solar_used = min(solar_generation, total_consumption)
        grid_used = max(0, total_consumption - solar_generation)
        solar_excess = max(0, solar_generation - total_consumption)
        
        return {
            'timestamp': datetime.now(),
            'indoor_temp': self.indoor_temp,
            'hvac_power': hvac_power,
            'base_load': base_consumption,
            'total_consumption': total_consumption,
            'solar_generation': solar_generation,
            'solar_used': solar_used,
            'grid_used': grid_used,
            'solar_excess': solar_excess,
            'occupancy': occupancy,
            'outdoor_temp': outdoor_temp
        }