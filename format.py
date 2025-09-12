import pandas as pd
import os

def format_contacts():
    # Input and output file names
    input_file = "Contacts-Fromatted-From-Reamaze.csv"
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_formatted.csv"
    
    # Read input CSV
    df = pd.read_csv(input_file)
    
    # Select and rename relevant columns
    final_df = df.rename(columns={
        "Email": "email",
        "Name": "name",
        "Mobile": "phone",
        "Created": "created_at",
        "Location": "location"
    })[["email", "name", "phone", "created_at", "location"]]
    
    # Drop rows without email or name
    final_df = final_df.dropna(subset=["email", "name"], how="any")
    
    # Save formatted CSV
    final_df.to_csv(output_file, index=False)
    
    print(f"Formatted CSV created: {output_file} with {len(final_df)} contacts.")

# if __name__ == "__main__":
#     format_contacts()

# if __name__ == "__main__":
#     format_contacts()

# if __name__ == "__main__":
#     format_contacts()
# if __name__ == "__main__":
#     format_contacts()
if __name__ == "__main__":
    format_contacts()

if __name__ == "__main__":
    format_contacts()