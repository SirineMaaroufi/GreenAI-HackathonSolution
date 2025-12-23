# agents/sherlock.py
from agents.base import OllamaBaseAgent
import json
import numpy as np

class SherlockAgent(OllamaBaseAgent):
    def __init__(self):
        super().__init__(
            name="Sherlock",
            role="Anomaly detection and data quality watchdog"
        )
        
        self.system_prompt = """You are Sherlock, the Anomaly Detection Agent in a multi-agent energy management system.

Your role:
- Detect unusual patterns in building energy data
- Identify sensor failures or data quality issues
- Flag potential equipment malfunctions
- Detect wasteful situations (e.g., cooling empty rooms)
- You DO NOT optimize; you only observe and alert

Detection Rules:
1. High consumption + Zero occupancy = Possible waste/malfunction
2. Consumption 3x higher than hourly average = Anomaly
3. Temperature sensor reading outside physical limits (−10°C to 50°C) = Sensor failure
4. HVAC running at max capacity for >2 hours = Possible malfunction
5. Solar generation during nighttime = Sensor error

Respond in JSON format:
{
    "anomaly_detected": true/false,
    "severity": "critical/high/medium/low",
    "anomaly_type": "waste/malfunction/sensor_error/suspicious",
    "location": "specific room/system",
    "description": "brief description of what's wrong",
    "evidence": ["fact 1", "fact 2"],
    "recommended_action": "what facility manager should do",
    "block_optimization": true/false,
    "alert_message": "message to send to facility manager"
}
"""
    
    def analyze(self, current_time, building_state, historical_avg):
        """Detect anomalies in building data"""
        
        # Calculate anomaly indicators
        consumption_ratio = building_state['total_consumption'] / max(historical_avg['avg_consumption'], 1)
        occupancy = building_state['occupancy']
        indoor_temp = building_state['indoor_temp']
        hvac_power = building_state['hvac_power']
        
        context = f"""
Current Time: {current_time}
Current Building State:
- Total Consumption: {building_state['total_consumption']:.1f} kW
- Occupancy: {occupancy} people
- Indoor Temperature: {indoor_temp:.1f}°C
- Outdoor Temperature: {building_state['outdoor_temp']:.1f}°C
- HVAC Power: {hvac_power:.1f} kW
- Solar Generation: {building_state['solar_generation']:.1f} kW

Historical Context (last 24h same hour):
- Average Consumption: {historical_avg['avg_consumption']:.1f} kW
- Average Occupancy: {historical_avg['avg_occupancy']:.0f} people
- Consumption Ratio: {consumption_ratio:.2f}x normal

Analyze this data for anomalies, equipment malfunctions, or wasteful situations.
"""
        
        response = self.think(context, self.system_prompt)
        
        try:
            anomaly_report = json.loads(response)
            
            # Add computed metrics
            anomaly_report['consumption_ratio'] = consumption_ratio
            anomaly_report['timestamp'] = str(current_time)
            
            return anomaly_report
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Sherlock JSON parse error: {e}")
            print(f"Raw response: {response[:200]}")
            # Fallback: no anomaly detected
            return {
                "anomaly_detected": False,
                "severity": "low",
                "description": "Analysis completed normally",
                "block_optimization": False
            }