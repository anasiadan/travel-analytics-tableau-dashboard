"""
Travel Data Cleaning Pipeline
Processes raw travel data for Tableau dashboard analysis
"""

import pandas as pd
from cleaning_functions import clean_data

def main():
    # File paths
    input_file = 'Travel details dataset.csv'
    output_file = 'Cleaned travel data.csv'
    
    try:
        # Load and clean data
        df = pd.read_csv(input_file)
        
        # Clean data
        df_clean = clean_data(df)
        
        # Save results
        df_clean.to_csv(output_file, index=False)
        print(f"💾 Saved {len(df_clean)} cleaned records to {output_file}")
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"   Original records: {len(df)}")
        print(f"   Cleaned records: {len(df_clean)}")
        print(f"   Unique destinations: {df_clean['Country'].nunique()}")
        print(f"   Date range: {df_clean['Travel_Month'].nunique()} months")
        print(f"   Average cost: ${df_clean['Total_Cost'].mean():.0f}")
        
    except FileNotFoundError:
        print(f" Error: {input_file} not found")
    except Exception as e:
        print(f" Error: {str(e)}")

if __name__ == "__main__":
    main()