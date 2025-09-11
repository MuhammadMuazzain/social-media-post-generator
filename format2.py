import pandas as pd
import os

def format_contacts_for_tidio():
    # Input and output file names
    input_file = "Contacts-Fromatted-From-Reamaze.csv"
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_tidio_ready.csv"
    
    # Read input CSV
    df = pd.read_csv(input_file)
    
    # Rename existing columns to match Tidio requirements
    df = df.rename(columns={
        "Name": "Name",
        "Email": "Email",
        "Mobile": "Phone",
        "Created": "Created at",
        "Location": "Location"
    })
    
    # Create all required Tidio columns, fill with existing or default values
    tidio_df = pd.DataFrame()
    tidio_df["ID"] = ""  # leave blank (Tidio can auto-generate)
    tidio_df["Name"] = df.get("Name", "")
    tidio_df["Email"] = df.get("Email", "")
    tidio_df["Email consent"] = "subscribed"  # default to subscribed
    tidio_df["Created at"] = df.get("Created at", "")
    tidio_df["Conversation rating"] = ""  # no data available
    tidio_df["Browser language"] = ""  # no data available

    # Split Location into City & Country if possible
    if "Location" in df and df["Location"].notna().any():
        tidio_df["City"] = df["Location"].apply(lambda x: str(x).split(",")[0] if pd.notna(x) else "")
        tidio_df["Country"] = df["Location"].apply(lambda x: str(x).split(",")[-1].strip() if pd.notna(x) and "," in str(x) else "")
    else:
        tidio_df["City"] = ""
        tidio_df["Country"] = ""

    tidio_df["Phone"] = df.get("Phone", "")
    tidio_df["Tags"] = ""  # can add custom tags later in Tidio
    
    # Drop rows without Email (Tidio requires email to identify contacts)
    tidio_df = tidio_df.dropna(subset=["Email"], how="any")
    
    # Save final CSV ready for Tidio
    tidio_df.to_csv(output_file, index=False)
    
    print(f"Tidio-ready CSV created: {output_file} with {len(tidio_df)} contacts.")

if __name__ == "__main__":
    format_contacts_for_tidio()
