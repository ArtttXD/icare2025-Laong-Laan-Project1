import pandas as pd
import csv

def clean_data(file_path, output_name):
    print(f"--- Processing {file_path} ---")
    
    # TRICK 1: Detect the Delimiter (Comma or Semicolon?)
    # We peek at the first valid line to see what character is used more
    try:
        with open(file_path, 'r', encoding='latin1') as f:
            sample = f.read(2048) # Read the first bit of the file
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter
            print(f"Detected delimiter: '{delimiter}'")
    except:
        delimiter = ',' # Default fallback
        print("Could not detect delimiter, defaulting to ','")

    # TRICK 2: Load Data & Handle "Junk" Rows
    # We try loading it. If the header looks wrong (too few columns), we skip a row and try again.
    df = None
    for skip in range(5): # Try skipping 0, 1, 2, 3, 4 rows
        try:
            temp_df = pd.read_csv(file_path, sep=delimiter, skiprows=skip, encoding='latin1', on_bad_lines='skip')
            # Sanity Check: If we have at least 2 columns, it's probably right
            if len(temp_df.columns) > 1:
                df = temp_df
                print(f"Successfully loaded by skipping {skip} rows.")
                break
        except:
            continue
            
    if df is None:
        print("CRITICAL ERROR: Could not read the file format.")
        return

    # --- FROM HERE BELOW IS YOUR ORIGINAL CLEANING LOGIC ---

    # 2. Standardize Headers
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')
    
    # 3. Remove Duplicates
    df = df.drop_duplicates()

    # 4. Standardize Text (Title Case)
    for col in df.select_dtypes(include=['object']).columns:
        if 'date' not in col:
            df[col] = df[col].str.strip().str.title()

    # 5. Fix Numbers (Remove commas like "1,000")
    # This is important for your specific file which has population numbers
    for col in df.columns:
        # Check if column looks numeric but is stored as object/string
        if df[col].dtype == 'object':
             # Try converting to numbers to see if it works
             # We replace commas first
             clean_col = df[col].astype(str).str.replace(',', '', regex=False)
             # If it converts cleanly, we keep it
             df[col] = pd.to_numeric(clean_col, errors='ignore')

    # 6. Export
    df.to_csv(output_name, index=False)
    print(f"Done! Saved to {output_name}")

# --- RUN IT ---
# Make sure to include the file extension!
clean_data('1A6DPAG0.csv', 'cleaned_population.csv')