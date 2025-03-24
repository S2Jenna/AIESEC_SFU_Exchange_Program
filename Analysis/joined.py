import pandas as pd
import os

def joined_data_1324():
    # Load datasets
    sfu_1324 = pd.read_csv(os.path.join("Data", "SFU 2013 - 2024.csv"))
    ubc_1324 = pd.read_csv(os.path.join("Data", "UBC 2013 - 2024.csv"))

    sfu_1324_tojoin = sfu_1324[['Backgrounds','Signed up', 'Applied', 'Accepted', 'Approved', 'Realized', 'Finished', 'Completed', 'Gender', 'GPA', 'Funding', 'SFU Campus']]

    # Merge datasets
    frames = [ubc_1324, sfu_1324_tojoin]
    sfu_ubc_1324 = pd.concat(frames)

    # Renaming
    sfu_ubc_1324["SFU Campus"] = sfu_ubc_1324["SFU Campus"].fillna("UBC")
    sfu_ubc_1324.rename(columns={'SFU Campus': 'Campus'}, inplace=True)
    sfu_ubc_1324["Campus"] = sfu_ubc_1324["Campus"].replace({
    "Vancouver": "SFU Vancouver",
    "Burnaby": "SFU Burnaby",
    "Surrey": "SFU Surrey"
})

    return sfu_ubc_1324

def joined_data_24():
    # Load datasets
    sfu_24 = pd.read_csv(os.path.join("Data", "SFU 2024 Data.csv"))
    ubc_24 = pd.read_csv(os.path.join("Data", "UBC.csv"))

    sfu_24_tojoin = sfu_24[['Backgrounds','Signed up', 'Applied', 'Accepted', 'Approved', 'Realized', 'Finished', 'Completed', 'Gender']]
    sfu_24_tojoin["Campus"] = "SFU"

    ubc_24["Campus"] = "UBC"

    # Merge datasets
    frames = [ubc_24, sfu_24_tojoin]
    sfu_ubc_24 = pd.concat(frames)

    return sfu_ubc_24

    

def main():
    result_df = joined_data_1324()
    output_file = os.path.join("Data", "SFU_UBC_1324_Merged.csv")
    result_df.to_csv(output_file, index=False)

    res_df = joined_data_24()
    output = os.path.join("Data", "SFU_UBC_24_Merged.csv")
    res_df.to_csv(output, index=False)

    print(f"Dataset saved to {output_file}")
    print(f"Dataset saved to {output}")

    

if __name__ == '__main__':
    main()

