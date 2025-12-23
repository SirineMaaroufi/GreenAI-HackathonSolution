# agents/solar_prophet_ollama.py
from agents.base import OllamaBaseAgent
import json

class SolarProphetAgent(OllamaBaseAgent):
    def __init__(self):
        super().__init__(
            name="Solar Prophet",
            role="Solar generation forecasting and optimization"
        )
        
        self.system_prompt = """Solar Prophet Agent: Analyze solar forecasts and recommend actions.

JSON format:
{
    "recommendation": "action to take",
    "confidence": 80
}
"""
    
    def analyze(self, current_time, solar_forecast, building_state):
        context = f"""
Time: {current_time.strftime('%H:%M')}
Solar now: {building_state['solar_generation']:.1f} kW
Consumption: {building_state['total_consumption']:.1f} kW
Next 4h forecast: {solar_forecast[:16]}

Recommend action to maximize solar usage.

Next 4 hours solar forecast (kW): {solar_forecast[:16]}

Building: {building_state['indoor_temp']:.1f}°C indoor, {building_state['occupancy']} people

What actions maximize solar utilization?
"""
        
        response = self.think(context, self.system_prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "analysis": "Normal operation",
                "recommendation": "maintain current operation",
                "confidence": 50
            }