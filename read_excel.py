import os
import pandas as pd


folder_path = os.path.join("Data", "Raw Data")


excel_file = os.path.join(folder_path, "EP_data_SFU.xlsx")
sheets = pd.read_excel(excel_file, sheet_name=None)

# Loop through each sheet and save it as a CSV file
for sheet_name, df in sheets.items():
    csv_file = os.path.join(folder_path, f"{sheet_name}.csv")  
    df.to_csv(csv_file, index=False)
    print(f"Saved {sheet_name} as {csv_file}")
