import pandas as pd
import os
import re

def clean_date(date_value):
    """Convert 2023-09-15T19:02:02.856+05:00 → 2023-09-15"""
    if pd.isna(date_value):
        return ""
    return str(date_value).split("T")[0]

def clean_name(name_value):
    """Remove special unicode characters (leave only readable text)"""
    if pd.isna(name_value):
        return ""
    return re.sub(r'[^\x00-\x7F]+', '', str(name_value)).strip()

def clean_email(email_value):
    """Remove dummy/test emails like dummy+X@yourdomain.com"""
    if pd.isna(email_value):
        return ""
    email = str(email_value).strip()
    if email.startswith("dummy+"):
        return ""
    return email

def clean_phone(phone_value):
    """Return phone only if valid digits exist, else empty"""
    if pd.isna(phone_value):
        return ""
    phone = re.sub(r'\D', '', str(phone_value))
    return phone if len(phone) >= 7 else ""  # Keep only valid numbers

def clean_location(location_value):
    """Remove empty commas and whitespace from location"""
    if pd.isna(location_value):
        return ""
    location = str(location_value).strip().strip(",")
    return location if location else ""

def format_contacts():
    # Input and output file names
    input_file = "Contacts-Fromatted-From-Reamaze.csv"
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_formatted.csv"
    
    # Read input CSV
    df = pd.read_csv(input_file)
    
    # Rename and select only needed columns
    final_df = df.rename(columns={
        "Email": "email",
        "Name": "name",
        "Mobile": "phone",
        "Created": "created_at",
        "Location": "location"
    })[["email", "name", "phone", "created_at", "location"]]
    
    # Clean each column
    final_df["email"] = final_df["email"].apply(clean_email)
    final_df["name"] = final_df["name"].apply(clean_name)
    final_df["phone"] = final_df["phone"].apply(clean_phone)
    final_df["created_at"] = final_df["created_at"].apply(clean_date)
    final_df["location"] = final_df["location"].apply(clean_location)
    
    # Drop rows with no email or name (mandatory for Tidio)
    final_df = final_df[(final_df["email"] != "") & (final_df["name"] != "")]
    
    # Save formatted CSV
    final_df.to_csv(output_file, index=False)
    print(f"Formatted CSV created: {output_file} with {len(final_df)} valid contacts.")

if __name__ == "__main__":
    format_contacts()
