# test_multizone_setup.py
"""
Quick test to verify multi-zone system is working
Runs a SHORT simulation (1 hour only) to validate setup
"""
from building_zones import MultiZoneUniversity
from zone_data_generator import ZoneDataGenerator
from datetime import datetime

def test_setup():
    print("🧪 Testing Multi-Zone System Setup...")
    print("="*60)
    
    # Test 1: Campus initialization
    print("\n1️⃣  Testing campus initialization...")
    try:
        campus = MultiZoneUniversity()
        zone_ids = campus.get_zone_ids()
        print(f"   ✅ Campus created with {len(zone_ids)} zones")
        for zone_id in zone_ids:
            zone = campus.get_zone(zone_id)
            print(f"      • {zone.zone_name}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 2: Data generation
    print("\n2️⃣  Testing zone data generation...")
    try:
        generator = ZoneDataGenerator(datetime(2024, 3, 15, 8, 0), days=0.1)  # Just 2.4 hours
        data = generator.generate_dataset()
        print(f"   ✅ Generated {len(data)} timesteps")
        print(f"      Columns: {list(data.columns[:5])}...")
        
        # Verify zone occupancy columns
        zone_columns = [col for col in data.columns if 'occupancy' in col]
        print(f"   ✅ Found {len(zone_columns)} zone occupancy columns")
        
        # Test save/load
        print("\n   Testing CSV save/load...")
        test_file = 'test_zone_data.csv'
        data.to_csv(test_file, index=False)
        loaded_data = ZoneDataGenerator.load_from_csv(test_file)
        if loaded_data is not None and len(loaded_data) == len(data):
            print(f"   ✅ CSV save/load working")
            import os
            os.remove(test_file)  # Cleanup
        else:
            print(f"   ⚠️  CSV save/load may have issues")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 3: Simulation step
    print("\n3️⃣  Testing simulation step...")
    try:
        row = data.iloc[0]
        
        # Setup zone parameters
        zone_hvac_powers = {zone_id: 50 for zone_id in zone_ids}
        zone_occupancies = {zone_id: int(row[f'{zone_id}_occupancy']) for zone_id in zone_ids}
        
        # Run simulation
        result = campus.simulate_step(
            zone_hvac_powers,
            zone_occupancies,
            float(row['solar_forecast']),
            float(row['outdoor_temp'])
        )
        
        print(f"   ✅ Simulation successful")
        print(f"      Total consumption: {result['campus_summary']['total_consumption']:.1f} kW")
        print(f"      Zones simulated: {len(result['zones'])}")
        
        # Show sample zone
        sample_zone = list(result['zones'].keys())[0]
        sample_data = result['zones'][sample_zone]
        print(f"\n      Sample zone ({sample_zone}):")
        print(f"         Consumption: {sample_data['total_consumption']:.1f} kW")
        print(f"         Indoor temp: {sample_data['indoor_temp']:.1f}°C")
        print(f"         Occupancy: {sample_data['occupancy']} people")
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Agent imports
    print("\n4️⃣  Testing agent imports...")
    try:
        from agents.anomaly import SherlockAgent
        from agents.solar import SolarProphetAgent
        from agents.grid import GridOracleAgent
        from agents.load import ComfortGuardianAgent
        from agents.corrdinator import OrchestratorAgent
        
        print(f"   ✅ All agents imported successfully")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 5: Quick agent test (no Ollama call)
    print("\n5️⃣  Testing agent initialization...")
    try:
        sherlock = SherlockAgent()
        solar = SolarProphetAgent()
        grid = GridOracleAgent()
        comfort = ComfortGuardianAgent()
        orchestrator = OrchestratorAgent()
        print(f"   ✅ All agents initialized")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print("\n✅ Multi-zone system is ready to run")
    print("\n🚀 Next steps:")
    print("   1. Run full simulation:  python main_multizone.py")
    print("   2. Visualize results:    python visualize_zones.py")
    print("   3. Compare approaches:   python compare_systems.py")
    print("\n💡 Note: Full simulation will take 30-40 minutes")
    print("   (8 zones × 5 agents × 24 hours = lots of Ollama calls)")
    
    return True

if __name__ == "__main__":
    success = test_setup()
    if not success:
        print("\n❌ Setup test failed. Please fix errors above.")
        exit(1)
