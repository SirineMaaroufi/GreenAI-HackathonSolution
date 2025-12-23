# generate_zone_data.py
"""
Standalone script to generate and save zone forecast data
Run this once to create the dataset, then use it multiple times
"""
from zone_data_generator import ZoneDataGenerator
from datetime import datetime
import sys

def generate_data(days=1, filename='zone_forecast_data.csv'):
    """Generate zone forecast data and save to CSV"""
    
    print("="*70)
    print("📊 ZONE FORECAST DATA GENERATOR")
    print("="*70)
    
    # Get parameters
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except:
            print(f"⚠️  Invalid days parameter, using default: {days}")
    
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    
    print(f"\n⚙️  Configuration:")
    print(f"   Duration: {days} day(s)")
    print(f"   Output file: {filename}")
    print(f"   Timesteps: {days * 24 * 4} (15-min intervals)")
    
    # Generate data
    start_date = datetime(2024, 3, 15, 8, 0)  # Friday 8 AM
    generator = ZoneDataGenerator(start_date, days=days)
    
    print(f"\n🔧 Generating data starting from {start_date.strftime('%Y-%m-%d %H:%M')}...")
    data = generator.save_to_csv(filename)
    
    # Show summary
    print(f"\n📈 Data Summary:")
    print(f"   Total records: {len(data)}")
    print(f"   Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
    print(f"   Columns: {len(data.columns)}")
    
    # Show sample
    print(f"\n📋 Sample data (first row):")
    print(f"   Time: {data.iloc[0]['timestamp']}")
    print(f"   Solar: {data.iloc[0]['solar_forecast']:.1f} kW")
    print(f"   Price: ${data.iloc[0]['electricity_price']:.3f}/kWh")
    print(f"   Outdoor temp: {data.iloc[0]['outdoor_temp']:.1f}°C")
    
    # Zone occupancies
    zone_cols = [col for col in data.columns if 'occupancy' in col]
    print(f"\n🏫 Zone occupancy columns ({len(zone_cols)}):")
    for col in zone_cols:
        zone_name = col.replace('_occupancy', '').replace('_', ' ').title()
        avg_occ = data[col].mean()
        max_occ = data[col].max()
        print(f"   {zone_name}: avg={avg_occ:.0f}, max={max_occ}")
    
    print(f"\n" + "="*70)
    print(f"✅ SUCCESS!")
    print(f"="*70)
    print(f"\n📁 Data saved to: {filename}")
    print(f"\n🚀 Next steps:")
    print(f"   1. Run simulation: python main_multizone.py")
    print(f"   2. Simulation will automatically use {filename}")
    print(f"   3. Regenerate data anytime: python generate_zone_data.py [days]")
    
    print(f"\n💡 Tips:")
    print(f"   - Generate 7 days: python generate_zone_data.py 7")
    print(f"   - Custom filename: python generate_zone_data.py 1 my_data.csv")
    print(f"   - Larger datasets take longer but provide more patterns")

if __name__ == "__main__":
    generate_data()
