# agents/grid_oracle.py
from agents.base import OllamaBaseAgent
import json

class GridOracleAgent(OllamaBaseAgent):
    def __init__(self):
        super().__init__(
            name="Grid Oracle",
            role="Grid pricing and carbon intensity optimization"
        )
        
        self.system_prompt = """You are the Grid Oracle Agent in a multi-agent energy management system.

Your role:
- Monitor electricity pricing (peak/off-peak)
- Track grid carbon intensity
- Recommend load shifting to avoid high prices and high carbon periods
- Balance cost savings with carbon reduction

Respond in JSON format:
{
    "analysis": "pricing and carbon situation",
    "recommendation": "specific recommendation",
    "cost_impact": "estimated $ savings",
    "carbon_impact": "estimated kg CO2 reduction",
    "priority": "high/medium/low",
    "proposed_actions": [
        {"time": "HH:MM", "action": "reduce HVAC", "reason": "peak pricing"}
    ]
}
"""
    
    def analyze(self, current_time, price_forecast, carbon_forecast, building_state):
        context = f"""
Time: {current_time.strftime('%H:%M')}
Price: ${price_forecast[0]['price']:.3f}/kWh | Carbon: {carbon_forecast[0]['carbon_intensity']} gCO2/kWh
Grid: {building_state['grid_used']} kW | Consumption: {building_state['total_consumption']} kW

Next 4h prices: {[round(p['price'], 3) for p in price_forecast[:8]]}

Recommend cost/carbon optimization.
"""
        
        response = self.think(context, self.system_prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "analysis": response,
                "recommendation": "maintain current operation",
                "priority": "low"
            }