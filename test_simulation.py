# test_simulation.py
# Run a simple HVAC baseline simulation and save clean results to Excel
# (with visible timestamps + auto-sized columns)

from building_model import UniversityBuilding
from data_generator import CampusDataGenerator
from datetime import datetime
import pandas as pd


def autosize_excel_columns(worksheet):
    """Auto-fit Excel column widths based on cell contents."""
    for col_cells in worksheet.columns:
        max_len = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            val = "" if cell.value is None else str(cell.value)
            if len(val) > max_len:
                max_len = len(val)
        worksheet.column_dimensions[col_letter].width = max(10, max_len + 2)


def main():
    # ===============================
    # 1) Generate forecast data
    # ===============================
    generator = CampusDataGenerator(
        start_date=datetime(2024, 3, 15, 0, 0),
        days=1
    )
    forecast_data = generator.generate_dataset()

    # Ensure timestamp column is datetime (so Excel recognizes it)
    if "timestamp" in forecast_data.columns:
        forecast_data["timestamp"] = pd.to_datetime(forecast_data["timestamp"])

    # ===============================
    # 2) Run simulation
    # ===============================
    building = UniversityBuilding()
    results = []

    for _, row in forecast_data.iterrows():
        # Simple baseline HVAC control
        hvac_power = 100 if row["outdoor_temp"] > 25 else 50

        result = building.simulate_step(
            hvac_power=hvac_power,
            solar_generation=row["solar_forecast"],
            occupancy=row["occupancy_forecast"],
            outdoor_temp=row["outdoor_temp"]
        )

        # Add metadata for analysis
        result["timestamp"] = row["timestamp"]
        result["electricity_price"] = row["electricity_price"]

        results.append(result)

    # ===============================
    # 3) Build results dataframe
    # ===============================
    results_df = pd.DataFrame(results)

    # Make sure timestamp is datetime (important for Excel display/format)
    if "timestamp" in results_df.columns:
        results_df["timestamp"] = pd.to_datetime(results_df["timestamp"])

    # ===============================
    # 4) Save to Excel (well delimited)
    # ===============================
    output_file = "simulation_results.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        results_df.to_excel(writer, sheet_name="SimulationResults", index=False)

        ws = writer.sheets["SimulationResults"]

        # Set a friendly format for the timestamp column (if present)
        # Find the column index of "timestamp"
        header = [cell.value for cell in ws[1]]
        if "timestamp" in header:
            ts_col_idx = header.index("timestamp") + 1  # 1-based indexing in Excel
            for cell in ws.iter_cols(min_col=ts_col_idx, max_col=ts_col_idx, min_row=2, values_only=False):
                for c in cell:
                    c.number_format = "YYYY-MM-DD HH:MM:SS"

        # Auto-size all columns so Excel won't show ########
        autosize_excel_columns(ws)

    # ===============================
    # 5) Print summary
    # ===============================
    print(results_df.head())

    if "grid_used" in results_df.columns and "electricity_price" in results_df.columns:
        total_cost = (results_df["grid_used"] * results_df["electricity_price"]).sum()
        print(f"Total cost: ${total_cost:.2f}")
    else:
        print("⚠️ Could not compute total cost (missing 'grid_used' or 'electricity_price').")

    print(f"\n✅ Results saved cleanly to Excel: {output_file}")


if __name__ == "__main__":
    main()