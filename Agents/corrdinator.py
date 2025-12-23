# agents/orchestrator.py
from agents.base import OllamaBaseAgent
import json

class OrchestratorAgent(OllamaBaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            role="Coordinate all agents and make final decisions"
        )
        
        self.system_prompt = """You are the Orchestrator Agent coordinating a multi-agent energy management system.

Your role:
- Receive recommendations from PV Generation Agent, Cost Efficiency Agent, and Comfort Agent
- Resolve conflicts between agents
- Make final decisions on HVAC setpoints and actions
- Prioritize: 1) Comfort constraints (hard limits), 2) Cost/carbon optimization, 3) Solar/PV utilization

Respond in JSON format:
{
    "decision": "final action to take",
    "hvac_setpoint": 21.5,
    "hvac_power": 100,
    "reasoning": "why this decision balances all factors",
    "trade_offs": "what was sacrificed",
    "agent_consensus": "high/medium/low",
    "alerts": ["any alerts for facility managers"]
}

IMPORTANT: You MUST include a numeric "hvac_setpoint" field (between 20-24°C). Do not default to 22.0.
"""
    
    def coordinate(self, current_time, building_state, agent_recommendations):
        context = f"""
Time: {current_time.strftime('%H:%M')}
Temp: {building_state['indoor_temp']:.1f}°C (setpoint: {building_state['hvac_setpoint']}°C)
Occupancy: {building_state['occupancy']} | Solar: {building_state['solar_generation']:.0f} kW

Agent Recommendations:
- PV Generation: {agent_recommendations.get('pv_generation', {}).get('recommendation', 'N/A')}
- Cost Efficiency: {agent_recommendations.get('cost_efficiency', {}).get('recommendation', 'N/A')}
- Comfort: {agent_recommendations.get('comfort', {}).get('comfort_status', 'N/A')}

Decide HVAC setpoint (20-24°C range). You MUST vary the setpoint based on the situation. Do NOT always choose 22.0°C.
"""
        
        response = self.think(context, self.system_prompt)
        
        # Debug output - print raw LLM response
        print(f"         🔍 RAW LLM RESPONSE: {response[:200]}...")
        
        try:
            decision = json.loads(response)
            # Ensure required fields
            if 'hvac_setpoint' not in decision:
                print(f"         ⚠️ WARNING: No hvac_setpoint in response, using fallback")
                decision['hvac_setpoint'] = building_state.get('hvac_setpoint', 22)
            if 'hvac_power' not in decision:
                decision['hvac_power'] = 100
            return decision
        except Exception as e:
            print(f"         ❌ JSON PARSE ERROR: {e}")
            print(f"         Response was: {response}")
            # Safe fallback
            return {
                "decision": "maintain current operation",
                "hvac_setpoint": building_state.get('hvac_setpoint', 22),
                "hvac_power": 100,
                "reasoning": f"Fallback due to parsing error: {e}"
            }