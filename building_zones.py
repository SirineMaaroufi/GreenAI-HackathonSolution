# building_zones.py
import numpy as np
from datetime import datetime

class BuildingZone:
    """Represents a single building/floor/bloc with independent HVAC control"""
    
    def __init__(self, zone_id, zone_name, floor_area, occupancy_capacity):
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.floor_area = floor_area  # square meters
        self.occupancy_capacity = occupancy_capacity  # max people
        
        # Thermal parameters (scaled by area)
        self.thermal_mass = floor_area * 0.1  # kWh/°C
        self.base_load = floor_area * 0.01  # kW (lights, computers)
        self.hvac_capacity = floor_area * 0.04  # kW max cooling/heating
        
        # State variables
        self.indoor_temp = 22  # °C
        self.hvac_setpoint = 22
        self.outdoor_temp = 20
        
    def simulate_step(self, hvac_power, solar_allocated, occupancy, outdoor_temp, dt=0.25):
        """Simulate one time step (dt in hours)"""
        
        self.outdoor_temp = outdoor_temp
        
        # Occupancy heat gain
        occupancy_heat = occupancy * 0.1  # kW per person
        
        # Base electrical load (scales with occupancy)
        occupancy_factor = occupancy / max(self.occupancy_capacity, 1)
        base_consumption = self.base_load * (0.3 + 0.7 * occupancy_factor)
        
        # HVAC heat transfer
        temp_diff = self.indoor_temp - self.outdoor_temp
        heat_loss = temp_diff * (self.floor_area / 10000)  # kW lost to outside
        
        # Temperature changes
        hvac_effect = hvac_power / self.thermal_mass
        natural_change = (heat_loss + occupancy_heat) / self.thermal_mass
        
        # Update indoor temperature
        self.indoor_temp += (hvac_effect - natural_change) * dt
        
        # Total consumption
        total_consumption = base_consumption + abs(hvac_power)
        
        # Solar allocation
        solar_used = min(solar_allocated, total_consumption)
        grid_used = max(0, total_consumption - solar_allocated)
        
        return {
            'zone_id': self.zone_id,
            'zone_name': self.zone_name,
            'indoor_temp': self.indoor_temp,
            'hvac_power': hvac_power,
            'base_load': base_consumption,
            'total_consumption': total_consumption,
            'solar_used': solar_used,
            'grid_used': grid_used,
            'occupancy': occupancy,
            'outdoor_temp': outdoor_temp
        }


class MultiZoneUniversity:
    """University campus with multiple independently controlled zones"""
    
    def __init__(self):
        # Define realistic university zones
        self.zones = {
            'engineering': BuildingZone('engineering', 'Engineering Building', 3000, 150),
            'library': BuildingZone('library', 'Main Library', 2500, 200),
            'admin': BuildingZone('admin', 'Administration', 2000, 80),
            'science_floor1': BuildingZone('science_floor1', 'Science Building - Floor 1', 1500, 100),
            'science_floor2': BuildingZone('science_floor2', 'Science Building - Floor 2', 1500, 100),
            'cafeteria': BuildingZone('cafeteria', 'Student Cafeteria', 1000, 250),
            'dorms_east': BuildingZone('dorms_east', 'Dormitories East Wing', 2000, 120),
            'dorms_west': BuildingZone('dorms_west', 'Dormitories West Wing', 2000, 120),
        }
        
        # Total solar capacity (shared across campus)
        self.total_solar_capacity = 300  # kW peak
        
    def get_zone_ids(self):
        return list(self.zones.keys())
    
    def get_zone(self, zone_id):
        return self.zones.get(zone_id)
    
    def allocate_solar(self, total_solar_generation, zone_consumptions):
        """Allocate solar generation proportionally to zone consumption"""
        total_consumption = sum(zone_consumptions.values())
        
        if total_consumption == 0:
            return {zone_id: 0 for zone_id in zone_consumptions.keys()}
        
        allocations = {}
        for zone_id, consumption in zone_consumptions.items():
            proportion = consumption / total_consumption
            allocations[zone_id] = total_solar_generation * proportion
        
        return allocations
    
    def simulate_step(self, zone_hvac_powers, zone_occupancies, solar_generation, outdoor_temp, dt=0.25):
        """Simulate all zones for one timestep"""
        
        # First pass: calculate consumptions
        zone_consumptions = {}
        for zone_id, zone in self.zones.items():
            hvac_power = zone_hvac_powers.get(zone_id, 0)
            occupancy = zone_occupancies.get(zone_id, 0)
            
            # Quick consumption estimate
            occupancy_factor = occupancy / max(zone.occupancy_capacity, 1)
            base = zone.base_load * (0.3 + 0.7 * occupancy_factor)
            zone_consumptions[zone_id] = base + abs(hvac_power)
        
        # Allocate solar
        solar_allocations = self.allocate_solar(solar_generation, zone_consumptions)
        
        # Second pass: simulate with solar allocations
        results = {}
        for zone_id, zone in self.zones.items():
            hvac_power = zone_hvac_powers.get(zone_id, 0)
            occupancy = zone_occupancies.get(zone_id, 0)
            solar_allocated = solar_allocations.get(zone_id, 0)
            
            result = zone.simulate_step(hvac_power, solar_allocated, occupancy, outdoor_temp, dt)
            results[zone_id] = result
        
        # Campus-wide summary
        total_consumption = sum(r['total_consumption'] for r in results.values())
        total_solar_used = sum(r['solar_used'] for r in results.values())
        total_grid_used = sum(r['grid_used'] for r in results.values())
        solar_excess = max(0, solar_generation - total_consumption)
        
        return {
            'zones': results,
            'campus_summary': {
                'total_consumption': total_consumption,
                'total_solar_used': total_solar_used,
                'total_grid_used': total_grid_used,
                'solar_generation': solar_generation,
                'solar_excess': solar_excess
            }
        }
