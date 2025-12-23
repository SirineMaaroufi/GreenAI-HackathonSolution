======================================================================
🤖 MULTI-ZONE AI AGENT ANALYSIS
======================================================================

📂 Loading pre-simulated building data...
   ✅ Loaded 23040 records
   Date range: 2024-03-15 08:00:00 to 2024-04-14 07:45:00

🧪 TEST MODE: Running on 2 zones only: ['engineering', 'library']
   (Full campus has 8 zones)

🚀 Initializing AI agents for 2 zones...
   ✅ Agents initialized

📚 Building historical context...
   ✅ Historical baselines ready

⏰ Selecting analysis timepoints...
   Selected 5 timepoints:
      • 08:00 - 2024-03-15 08:00:00
      • 10:00 - 2024-03-15 10:00:00
      • 12:00 - 2024-03-15 12:00:00
      • 15:00 - 2024-03-15 15:00:00
      • 18:00 - 2024-03-15 18:00:00

======================================================================
🕐 Analyzing: 2024-03-15 08:00
======================================================================
☀️  Solar: 127 kW | 💰 Price: $0.187/kWh | 🌡️  Outdoor: 22.9°C

📍 Engineering Building
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 110
   Consumption: 24.4 kW | Grid: 11.6 kW
      • 12:00 - 2024-03-15 12:00:00
      • 15:00 - 2024-03-15 15:00:00
      • 18:00 - 2024-03-15 18:00:00

======================================================================
🕐 Analyzing: 2024-03-15 08:00
======================================================================
☀️  Solar: 127 kW | 💰 Price: $0.187/kWh | 🌡️  Outdoor: 22.9°C

📍 Engineering Building
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 110
   Consumption: 24.4 kW | Grid: 11.6 kW

======================================================================
🕐 Analyzing: 2024-03-15 08:00
======================================================================
☀️  Solar: 127 kW | 💰 Price: $0.187/kWh | 🌡️  Outdoor: 22.9°C

📍 Engineering Building
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 110
   Consumption: 24.4 kW | Grid: 11.6 kW
☀️  Solar: 127 kW | 💰 Price: $0.187/kWh | 🌡️  Outdoor: 22.9°C

📍 Engineering Building
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 110
   Consumption: 24.4 kW | Grid: 11.6 kW
📍 Engineering Building
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 110
   Consumption: 24.4 kW | Grid: 11.6 kW
   Consumption: 24.4 kW | Grid: 11.6 kW
   🔍 Anomaly Detector analyzing...
   ✅ No anomalies
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Increase electricity usage for the next 4 hours to utilize as much solar power as possible.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: Shift non-essential loads to off-peak hours to reduce costs and carbon footprint.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: acceptable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Increase HVAC setpoint to 23.5°C for the next 4 hours to optimize solar power usage and cost efficiency",
    "hvac_setpoint": 23.5,
    "hvac_power": 100,
    "reasoning": "The dec...
         ✅ Orchestrator decision: Setpoint 23.5°C
         🔍 DEBUG - Full decision: {'decision': 'Increase HVAC setpoint to 23.5°C for the next 4 hours to optimize solar power usage and cost efficiency', 'hvac_setpoint': 23.5, 'hvac_power': 100, 'reasoning': 'The decision balances all factors by increasing the setpoint slightly to make use of available solar energy while also minimizing costs through reduced electricity consumption during off-peak hours.', 'trade_offs': 'Comfort may be compromised slightly as the temperature is raised. However, this adjustment is considered acceptable given the current occupancy and solar availability.', 'agent_consensus': 'high', 'alerts': ['Monitor comfort levels closely during the next 4 hours and consider adjusting setpoint if necessary']}

   📝 FINAL RECOMMENDATION: Setpoint 23.5°C
      Reasoning: The decision balances all factors by increasing the setpoint slightly to make use of available solar energy while also minimizing costs through reduced electricity consumption during off-peak hours.
======================================================================
🕐 Analyzing: 2024-03-15 08:00
======================================================================
☀️  Solar: 127 kW | 💰 Price: $0.187/kWh | 🌡️  Outdoor: 22.9°C
📍 Main Library
   Indoor: 22.0°C | Setpoint: 23.0°C | Occupancy: 7
   Consumption: 58.1 kW | Grid: 27.6 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      High HVAC consumption despite low occupancy.
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Adjust indoor temperature to reduce heating load and increase consumption of solar energy.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: To optimize cost, shift non-essential loads to off-peak hours (08:04 - 08:08) as the price will drop to $0.18/kWh during that time. 
         To reduce carbon footprint, consider shifting some loads to the period between 22:00 and 06:00 when the carbon intensity is lower.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: comfortable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Adjust indoor temperature to 21.5°C to reduce heating load and increase consumption of solar energy.",
    "hvac_setpoint": 21.5,
    "hvac_power": null,
    "reasoning": "The decis...
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Adjust indoor temperature to 21.5°C to reduce heating load and increase consumption of solar energy.', 'hvac_setpoint': 21.5, 'hvac_power': None,
          'reasoning': "The decision balances all factors by prioritizing comfort constraints 
         (Comfort: comfortable), cost optimization (shifting non-essential loads to off-peak hours as per Cost Efficiency Agent's recommendation), and solar/PV utilization (PV Generation Agent's recommendation).",
          'trade_offs': 'The trade-off is a slight decrease in comfort for a brief period. However, the temperature reduction will lead to increased PV energy consumption and cost savings.', 
          'agent_consensus': 'high', 
          'alerts': ['Facility managers should be aware of the temporary reduction in indoor temperature.']}

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: The decision balances all factors by prioritizing comfort constraints (Comfort: comfortable), cost optimization 
      (shifting non-essential loads to off-peak hours as per Cost Efficiency Agent's recommendation), and solar/PV utilization (PV Generation Agent's recommendation).

======================================================================
🕐 Analyzing: 2024-03-15 10:00
======================================================================
☀️  Solar: 247 kW | 💰 Price: $0.304/kWh | 🌡️  Outdoor: 24.3°C

📍 Engineering Building
   Indoor: 21.9°C | Setpoint: 22.0°C | Occupancy: 117
   Consumption: 28.3 kW | Grid: 0.0 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      High consumption detected that is 1.19 times the hourly average with n
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Continue operating as is, as the solar production forecast for the next 4 hours indicates an excess of power over consumption.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: Shift non-essential loads to off-peak hours to save cost and reduce carbon footprint.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: comfortable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Increase HVAC setpoint to 21.5°C",
    "hvac_setpoint": 21.5,
    "hvac_power": 95,
    "reasoning": "Given the comfortable occupancy level and excess solar production, we prioritiz...
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Increase HVAC setpoint to 21.5°C', 'hvac_setpoint': 21.5, 'hvac_power': 95, 'reasoning': 'Given the comfortable occupancy level and excess solar production, we prioritize comfort constraints (1), followed by cost/carbon optimization (2). However, considering the current temperature is slightly above the setpoint, a slight increase in setpoint allows for a reduction in HVAC power without compromising comfort. This reduces energy consumption while still utilizing the available solar power.', 'trade_offs': 'Sacrificed some energy savings by increasing the setpoint slightly', 'agent_consensus': 'high', 'alerts': ['Facility managers should be aware of the excess solar production and consider shifting non-essential loads to off-peak hours as recommended by the Cost Efficiency Agent']}

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: Given the comfortable occupancy level and excess solar production, we prioritize comfort constraints (1), followed by cost/carbon optimization (2). However, considering the current temperature is slightly above the setpoint, a slight increase in setpoint allows for a reduction in HVAC power without compromising comfort. This reduces energy consumption while still utilizing the available solar power.

======================================================================
🕐 Analyzing: 2024-03-15 10:00
======================================================================
☀️  Solar: 247 kW | 💰 Price: $0.304/kWh | 🌡️  Outdoor: 24.3°C

📍 Main Library
   Indoor: 22.1°C | Setpoint: 22.0°C | Occupancy: 125
   Consumption: 24.0 kW | Grid: 0.0 kW
   🔍 Anomaly Detector analyzing...
   ✅ No anomalies
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Continue operation as is, as the solar production for the next 4 hours exceeds the current consumption and building's electricity demand.  
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: To balance cost savings and carbon reduction, it is recommended to shift load during the next 4 hours by reducing HVAC consumption.      
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: comfortable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Reduce HVAC power consumption",
    "hvac_setpoint": 21.5,
    "hvac_power": 90,
    "reasoning": "To balance comfort constraints, cost/carbon optimization, and solar utilization, w...
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Reduce HVAC power consumption', 'hvac_setpoint': 21.5, 'hvac_power': 90, 'reasoning': "To balance comfort constraints, cost/carbon optimization, 
         and solar utilization, we are reducing the HVAC power consumption while keeping the temperature within a comfortable range to save energy costs and reduce carbon emissions. 
         
         The current solar production exceeds the building's electricity 
         demand for the next 4 hours.", 'trade_offs': 'Comfort might be slightly affected due to reduced HVAC power, but it remains within acceptable levels. Energy savings will occur due to lower consumption.',
          'agent_consensus': 'high', 'alerts': ['Alert: Reduced HVAC power consumption for cost and carbon optimization']} 

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: To balance comfort constraints, cost/carbon optimization, and solar utilization, 
      we are reducing the HVAC power
       consumption while keeping the temperature within a comfortable range to save energy costs and reduce carbon emissions.
       
        The current solar production exceeds the building's electricity demand for the next 4 hours.

======================================================================
🕐 Analyzing: 2024-03-15 12:00
======================================================================
☀️  Solar: 290 kW | 💰 Price: $0.175/kWh | 🌡️  Outdoor: 26.3°C

📍 Engineering Building
   Indoor: 21.9°C | Setpoint: 22.0°C | Occupancy: 87
   Consumption: 25.8 kW | Grid: 0.0 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      Higher consumption than usual with higher occupancy
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Reduce electricity consumption as much as possible for the next 4 hours to utilize the excess solar power generated.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: It is recommended to shift load during the next four hours to avoid high prices and high carbon periods.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: uncomfortable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Reduce HVAC setpoint to 20.5°C and shift some load during the next four hours to utilize excess solar power and reduce costs.",
    "hvac_setpoint": 20.5,
    "hvac_power": 80,
    ...
         ✅ Orchestrator decision: Setpoint 20.5°C
         🔍 DEBUG - Full decision: {'decision': 'Reduce HVAC setpoint to 20.5°C and shift some load during the next four hours to utilize excess solar power and reduce costs.', 'hvac_setpoint': 20.5, 'hvac_power': 80, 'reasoning': 'By reducing the HVAC setpoint slightly, we can save energy and utilize the excess solar power generated. Shifting some load during high-cost periods also helps in cost optimization.', 'trade_offs': 'Comfort might be compromised slightly for a short period, but it falls within acceptable comfort limits.', 'agent_consensus': 'medium', 'alerts': ['Alert: Slight temporary discomfort may occur to maintain energy savings and solar utilization. Consider adjusting clothing or using personal heaters if necessary.']}   

   📝 FINAL RECOMMENDATION: Setpoint 20.5°C
      Reasoning: By reducing the HVAC setpoint slightly, we can save energy and utilize the excess solar power generated. Shifting some load during high-cost periods also helps in cost optimization.

📍 Main Library
   Indoor: 22.0°C | Setpoint: 22.0°C | Occupancy: 133
   Consumption: 20.0 kW | Grid: 0.0 kW
   🔍 Anomaly Detector analyzing...
   ✅ No anomalies
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Reduce electricity consumption where possible to match the forecasted solar generation for the next 4 hours.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: To balance cost savings and carbon reduction, it's recommended to shift load during the next 4 hours by reducing HVAC consumption. This will help avoid high electricity prices and reduce carbon emissions.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: acceptable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Reduce HVAC consumption to match solar generation and shift load during the next 4 hours",
    "hvac_setpoint": 21.5,
    "hvac_power": 90,
    "reasoning": "By reducing HVAC setpoi...
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Reduce HVAC consumption to match solar generation and shift load during the next 4 hours', 'hvac_setpoint': 21.5, 'hvac_power': 90, 'reasoning': 'By reducing HVAC setpoint by 0.5°C and power consumption by 10%, we can balance comfort constraints, prioritize cost/carbon optimization, and maximize solar/PV utilization while maintaining acceptable comfort levels.', 'trade_offs': 'Comfort is maintained at an acceptable level with a slight decrease in temperature. Cost savings and carbon reduction are prioritized over maintaining the current temperature.', 'agent_consensus': 'high', 'alerts': ['Alert: Shift load during the next 4 hours to reduce HVAC consumption and maximize solar generation.']}

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: By reducing HVAC setpoint by 0.5°C and power consumption by 10%, we can balance comfort constraints, prioritize cost/carbon optimization, and maximize solar/PV utilization while maintaining acceptable comfort levels.

======================================================================
🕐 Analyzing: 2024-03-15 15:00
======================================================================
☀️  Solar: 173 kW | 💰 Price: $0.177/kWh | 🌡️  Outdoor: 24.2°C

📍 Engineering Building
   Indoor: 21.9°C | Setpoint: 22.0°C | Occupancy: 117
   Consumption: 31.6 kW | Grid: 3.3 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      High energy consumption (1.99x) detected during a period of increased 
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Adjust building's energy consumption to match the solar output over the next 4 hours.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: It is recommended to shift non-critical loads, particularly HVAC systems, to off-peak hours to avoid high costs and reduce carbon footprint.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: acceptable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Reduce HVAC setpoint to 21.5°C for the next 4 hours",
    "hvac_setpoint": 21.5,
    "hvac_power": 90,
    "reasoning": "By reducing the setpoint slightly, we balance comfort constr...  
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Reduce HVAC setpoint to 21.5°C for the next 4 hours', 'hvac_setpoint': 21.5, 'hvac_power': 90, 'reasoning': "By reducing the setpoint slightly, we balance comfort constraints (acceptable), cost/carbon optimization by adjusting building's energy consumption to match solar output and shifting non-critical loads to off-peak hours, and solar/PV utilization by prioritizing solar power over higher HVAC power demand.", 'trade_offs': 'Some occupants may experience slightly cooler temperatures, but overall comfort is acceptable. Energy costs are reduced due to load shifting and solar energy utilization.', 'agent_consensus': 'medium', 'alerts': ['Reminder: Consider adjusting clothing layers or using personal heaters if feeling uncomfortable']}

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: By reducing the setpoint slightly, we balance comfort constraints (acceptable), cost/carbon optimization by adjusting building's energy consumption to match solar output and shifting non-critical loads to off-peak hours, and solar/PV utilization by prioritizing solar power over higher HVAC power demand.

📍 Main Library
   Indoor: 21.9°C | Setpoint: 22.0°C | Occupancy: 137
   Consumption: 26.2 kW | Grid: 2.7 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: MEDIUM
      High consumption (1.44x higher than hourly average) with normal occupa
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Continue operation as is since current consumption (26.2 kW) is less than the predicted solar output for the next 4 hours.
      🤖 Calling Cost Efficiency Agent LLM...
   ⏳ Grid Oracle timeout, retrying in 1s... (attempt 1/4)
         ✅ Cost Efficiency: To balance cost savings and carbon reduction, it's recommended to shift load away from the next four hours (15:00 - 19:00) due to high pricing and high carbon periods. This could involve reducing HVAC usage or postponing non-essential tasks.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: comfortable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Reduce HVAC usage during peak hours to balance comfort constraints, cost/carbon optimization, and solar utilization.",
    "hvac_setpoint": 21.0,
    "hvac_power": 90,
    "reasonin...
         ✅ Orchestrator decision: Setpoint 21.0°C
         🔍 DEBUG - Full decision: {'decision': 'Reduce HVAC usage during peak hours to balance comfort constraints, cost/carbon optimization, and solar utilization.', 'hvac_setpoint': 21.0, 'hvac_power': 90, 'reasoning': "By reducing the setpoint slightly and adjusting the HVAC power, we can save energy costs during peak hours while still maintaining a comfortable environment for occupants. The PV Generation Agent's recommendation allows us to utilize solar power effectively, offsetting some of the reduced HVAC usage.", 'trade_offs': 'Some comfort may be sacrificed temporarily during the four high-cost/high-carbon hours, but overall comfort remains acceptable according to the Comfort Agent. The trade-off is a more energy-efficient operation during peak periods with potential cost savings.', 'agent_consensus': 'medium', 'alerts': ['Facility managers are advised to monitor HVAC usage and consider postponing non-essential tasks during the next four hours.']}

   📝 FINAL RECOMMENDATION: Setpoint 21.0°C
      Reasoning: By reducing the setpoint slightly and adjusting the HVAC power, we can save energy costs during peak hours while still maintaining a comfortable environment for occupants. The PV Generation Agent's recommendation allows us to utilize solar power effectively, offsetting some of the reduced HVAC usage.

======================================================================
🕐 Analyzing: 2024-03-15 18:00
======================================================================
☀️  Solar: 0 kW | 💰 Price: $0.273/kWh | 🌡️  Outdoor: 18.7°C

📍 Engineering Building
   Indoor: 21.8°C | Setpoint: 22.0°C | Occupancy: 100
   Consumption: 30.8 kW | Grid: 30.8 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      High energy consumption (2.35x) detected during non-peak occupancy hou
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Shift energy-intensive tasks (such as running air conditioning units) to earlier in the day when there is a higher probability of solar generation.
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: Shift non-critical loads to off-peak hours, specifically between 22:10 and 06:59 to avoid high prices and high carbon periods.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: acceptable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Increase HVAC setpoint to 21.5°C",
    "hvac_setpoint": 21.5,
    "hvac_power": 100,
    "reasoning": "To balance comfort constraints (Comfort Agent: acceptable), cost/carbon optimi...
         ✅ Orchestrator decision: Setpoint 21.5°C
         🔍 DEBUG - Full decision: {'decision': 'Increase HVAC setpoint to 21.5°C', 'hvac_setpoint': 21.5, 'hvac_power': 100, 'reasoning': "To balance comfort constraints (Comfort Agent: acceptable), cost/carbon optimization (Cost Efficiency Agent's recommendation to shift tasks to off-peak hours) and solar/PV utilization (PV Generation Agent's recommendation for higher solar generation during daytime), a slight increase in temperature is justified.", 'trade_offs': 'Comfort may be slightly compromised due to the increased temperature. However, this decision prioritizes cost efficiency and solar utilization over maintaining the setpoint at 22°C.', 'agent_consensus': 'medium', 'alerts': ['Alert: Consider adjusting individual comfort levels if needed to maintain comfort during slight temperature increase.']}

   📝 FINAL RECOMMENDATION: Setpoint 21.5°C
      Reasoning: To balance comfort constraints (Comfort Agent: acceptable), cost/carbon optimization (Cost Efficiency Agent's recommendation to shift tasks to off-peak hours) and solar/PV utilization (PV Generation Agent's recommendation for higher solar generation during daytime), a slight increase in temperature is justified.  

📍 Main Library
   Indoor: 21.8°C | Setpoint: 22.0°C | Occupancy: 111
   Consumption: 26.9 kW | Grid: 26.9 kW
   🔍 Anomaly Detector analyzing...
   ⚠️  ANOMALY: HIGH
      High energy consumption (2.21x higher than hourly average) observed at
   🤖 Getting agent recommendations...
      🤖 Calling PV Generation Agent LLM...
         ✅ PV Generation: Store excess consumption energy in batteries for later use
      🤖 Calling Cost Efficiency Agent LLM...
         ✅ Cost Efficiency: Shift load to off-peak hours to save costs and reduce carbon footprint.
      🤖 Calling Comfort Agent LLM...
         ✅ Comfort Agent: acceptable
      🤖 Calling Orchestrator LLM...
         🔍 RAW LLM RESPONSE: {
    "decision": "Lower HVAC setpoint to reduce costs and optimize solar utilization",
    "hvac_setpoint": 21.0,
    "hvac_power": 95,
    "reasoning": "Lowering the setpoint by 0.5 degrees reduces ...
         ✅ Orchestrator decision: Setpoint 21.0°C
         🔍 DEBUG - Full decision: {'decision': 'Lower HVAC setpoint to reduce costs and optimize solar utilization', 'hvac_setpoint': 21.0, 'hvac_power': 95, 'reasoning': 'Lowering the setpoint by 0.5 degrees reduces energy consumption slightly while also encouraging PV energy storage and load shifting for cost optimization and solar utilization', 'trade_offs': 'Comfort may be slightly compromised as temperature drops to 21.0°C, but it remains within acceptable limits', 'agent_consensus': 'medium', 'alerts': ['Consider adjusting personal comfort settings if necessary']}    

   📝 FINAL RECOMMENDATION: Setpoint 21.0°C
      Reasoning: Lowering the setpoint by 0.5 degrees reduces energy consumption slightly while also encouraging PV energy storage and load shifting for cost optimization and solar utilization

======================================================================
💾 Saving analysis results...
   ✅ Recommendations: agent_recommendations.csv
   ✅ Alerts: zone_alerts.csv (7 alerts)

======================================================================
   ✅ Alerts: zone_alerts.csv (7 alerts)

======================================================================

======================================================================
======================================================================
📊 ANALYSIS SUMMARY
======================================================================
======================================================================
Timepoints analyzed: 5
Zones analyzed: 2
Total recommendations: 10
Anomalies detected: 7

🚨 ALERTS BY ZONE:
======================================================================
Timepoints analyzed: 5
Zones analyzed: 2
Total recommendations: 10
Anomalies detected: 7
======================================================================
Timepoints analyzed: 5
Zones analyzed: 2
======================================================================
Timepoints analyzed: 5
Zones analyzed: 2
======================================================================
Timepoints analyzed: 5
Timepoints analyzed: 5
Zones analyzed: 2
Zones analyzed: 2
Total recommendations: 10
Anomalies detected: 7

🚨 ALERTS BY ZONE:
   Engineering Building: 4
   Main Library: 3