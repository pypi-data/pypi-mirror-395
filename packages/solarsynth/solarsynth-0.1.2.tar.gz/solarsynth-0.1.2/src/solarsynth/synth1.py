import numpy as np
import pandas as pd

def generate_multiple_columns(num_rows=50, output_filename="generated_data.csv"):
    """
    Generates up to five columns of continuous data with optional correlations,
    saves them to a CSV file, and returns the dataframe.
    """
    num_cols = int(input("How many columns would you like to generate? (1–5): "))
    if not (1 <= num_cols <= 5):
        print("Please choose between 1 and 5 columns.")
        return
    
    data = {}
    col_names = []

    for i in range(num_cols):
        print(f"\n--- Column {i+1} ---")
        col_name = input(f"Enter column {i+1} name: ").strip()
        col_names.append(col_name)

        # Ask if it must be correlated
        if i > 0:
            correlate = input(f"Should '{col_name}' be correlated with any previous column? (yes/no): ").strip().lower()
        else:
            correlate = "no"

        # Ask for range
        min_val = float(input(f"Enter minimum value for '{col_name}': "))
        max_val = float(input(f"Enter maximum value for '{col_name}': "))

        # Generate data
        if correlate == "yes":
            print(f"Available previous columns: {col_names[:-1]}")
            other_col = input("Enter the column to correlate with: ").strip()

            if other_col not in data:
                print(f"Column '{other_col}' not found — generating random data instead.")
                data[col_name] = np.random.uniform(min_val, max_val, num_rows)
                continue

            base = np.array(data[other_col])
            noise = np.random.normal(0, (max_val - min_val) * 0.05, num_rows)  # small random variation
            correlated_values = np.interp(base, (base.min(), base.max()), (min_val, max_val)) + noise
            data[col_name] = correlated_values
        else:
            data[col_name] = np.random.uniform(min_val, max_val, num_rows)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_filename, index=False)
    print(f"\n✅ Data generated and saved as '{output_filename}' successfully!")
    print(df.head())

    return df