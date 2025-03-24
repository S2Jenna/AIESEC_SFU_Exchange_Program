import pandas as pd
import os

def sfu_ubc_conversion():
    # Load the dataset
    df = pd.read_csv(os.path.join("Data", "SFU_UBC_1324_Merged.csv"))

    # Standardize "Campus" values
    df["Campus"] = df["Campus"].replace({
        "SFU Vancouver": "SFU",
        "SFU Burnaby": "SFU",
        "SFU Surrey": "SFU",
        "UBC": "UBC"
    })

    # Define steps in the process
    steps = ["Signed up", "Applied", "Accepted", "Approved", "Realized", "Finished", "Completed"]

    # Create an empty DataFrame to store conversion rates
    conversion_rates = []

    # Group by Campus (SFU & UBC)
    grouped_df = df.groupby("Campus")

    # Calculate conversion rates for each campus
    for campus, campus_df in grouped_df:
        campus_conversion = {"Campus": campus}

        for i in range(len(steps) - 1):  # Loop through each step except the last one
            step_current = steps[i]
            step_next = steps[i + 1]

            # Avoid division by zero
            campus_filtered = campus_df[campus_df[step_current] > 0]  # Consider only rows with at least 1 student

            if campus_filtered[step_current].sum() > 0:  # Ensure denominator is not zero
                campus_conversion[f"{step_current} → {step_next}"] = (
                    (campus_filtered[step_next].sum() / campus_filtered[step_current].sum()) * 100
                )
            else:
                campus_conversion[f"{step_current} → {step_next}"] = None  # Assign None if no data

        conversion_rates.append(campus_conversion)

    # Convert results to DataFrame and display
    conversion_df = pd.DataFrame(conversion_rates)
    return conversion_df

def sfu_1324_conversion():
    # Load the dataset
    df = pd.read_csv(os.path.join("Data", "SFU 2013 - 2024.csv"))

    steps = ["Signed up", "Applied", "Accepted", "Approved", "Realized", "Finished", "Completed"]

    conversion_rates = []

    grouped_df = df.groupby("Backgrounds")

    # Calculate conversion rates for each background
    for bg, bg_df in grouped_df:
        bg_conversion = {"Backgrounds": bg}

        # Compute conversion rates step by step
        for i in range(len(steps) - 1):
            step_current = steps[i]
            step_next = steps[i + 1]

            bg_filtered = bg_df[bg_df[step_current] > 0]  # Consider only rows with students in the current step

            if bg_filtered[step_current].sum() > 0:
                bg_conversion[f"{step_current} → {step_next}"] = (
                    (bg_filtered[step_next].sum() / bg_filtered[step_current].sum()) * 100
                )
            else:
                bg_conversion[f"{step_current} → {step_next}"] = None

        # Store conversion dictionary
        conversion_rates.append(bg_conversion)

    # Convert list of dictionaries to DataFrame
    bg_conversion_df = pd.DataFrame(conversion_rates)

    # Concatenate additional columns
    columns_to_add = ["Gender", "GPA", "Funding", "Length of Exchange", "Motivation", 
                      "Number of Destinations", "English Proficiency", "Prior International Experience", 
                      "SFU Campus", "Co-op Participation"]
    
    columns_to_add = [col for col in columns_to_add if col in df.columns]  # Ensure they exist

    # Group the additional columns by "Backgrounds" and take the first non-null value
    extra_data_df = df.groupby("Backgrounds")[columns_to_add].first().reset_index()

    # Merge conversion rates with additional columns
    bg_conversion_df = bg_conversion_df.merge(extra_data_df, on="Backgrounds", how="left")

    return bg_conversion_df


def main():
    sfu_ubc_res = sfu_ubc_conversion()
    output_file = os.path.join("Data", "SFU_UBC_Conversion_rate.csv")
    sfu_ubc_res.to_csv(output_file, index=False)

    sfu_res = sfu_1324_conversion()
    output= os.path.join("Data", "SFU_1324_Conversion_rate.csv")
    sfu_res.to_csv(output, index=False)

    print(f"Dataset saved to {output_file}")
    print(f"Dataset saved to {output}")

if __name__ == '__main__':
    main()
