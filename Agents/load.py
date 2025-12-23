# agents/comfort_guardian.py
from agents.base import OllamaBaseAgent
import json

class ComfortGuardianAgent(OllamaBaseAgent):
    def __init__(self):
        super().__init__(
            name="Comfort Guardian",
            role="Occupant comfort and building environment management"
        )
        
        self.system_prompt = """You are the Comfort Guardian Agent in a multi-agent energy management system.

Your role:
- Ensure occupant comfort (temperature within acceptable range)
- Consider occupancy levels and schedules
- Set comfort boundaries that other agents must respect
- Balance comfort with energy efficiency

Temperature comfort ranges:
- Occupied: 20-24°C (stricter)
- Low occupancy: 18-26°C (more flexible)
- Unoccupied: 16-28°C (very flexible)

Respond in JSON format:
{
    "analysis": "current comfort situation",
    "comfort_status": "comfortable/acceptable/uncomfortable",
    "constraints": {
        "min_temp": 20,
        "max_temp": 24,
        "flexibility": "low/medium/high"
    },
    "recommendation": "any comfort-related actions needed",
    "veto_reasons": ["list any proposed actions that violate comfort"]
}
"""
    
    def analyze(self, current_time, building_state, proposed_actions):
        context = f"""
Time: {current_time.strftime('%H:%M')}
Indoor: {building_state['indoor_temp']:.1f}°C | Outdoor: {building_state['outdoor_temp']:.1f}°C
Occupancy: {building_state['occupancy']} people | HVAC: {building_state['hvac_power']} kW

Evaluate comfort status. Range: 20-24°C (occupied), 18-26°C (unoccupied).
"""
        
        response = self.think(context, self.system_prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "comfort_status": "acceptable",
                "constraints": {"min_temp": 20, "max_temp": 24, "flexibility": "medium"}
            }