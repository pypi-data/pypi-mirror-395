import random
import pandas as pd
from faker import Faker
import uuid
import time
import os

# IMPORT YOUR TEMPLATES
from structured_data_generator.core.generators import (
    USER_TEMPLATE, ECOM_TEMPLATE, FINANCIAL_TEMPLATE, HEALTHCARE_TEMPLATE, 
    IOT_SENSOR_TEMPLATE, PRODUCT_CATALOG_TEMPLATE, NLP_TEXT_TEMPLATE, 
    WEB_ANALYTICS_TEMPLATE, IMAGE_METADATA_TEMPLATE, EDU_STUDENT_TEMPLATE,
    generate_from_template
)

# Add all templates here
TEMPLATES = {
    "USER TEMPLATE": USER_TEMPLATE,
    "ECOMMERCE TRANSACTION TEMPLATE": ECOM_TEMPLATE,
    "FINANCIAL BANKING TEMPLATE": FINANCIAL_TEMPLATE,
    "HEALTHCARE TEMPLATE": HEALTHCARE_TEMPLATE,
    "IOT SENSOR TEMPLATE": IOT_SENSOR_TEMPLATE,
    "NLP TEXT TEMPLATE": NLP_TEXT_TEMPLATE,
    "WEB ANALYTICS TEMPLATE": WEB_ANALYTICS_TEMPLATE,
    "IMAGE METADATA TEMPLATE": IMAGE_METADATA_TEMPLATE,
    "EDU STUDENT TEMPLATE": EDU_STUDENT_TEMPLATE,
    "PRODUCT CATALOG TEMPLATE": PRODUCT_CATALOG_TEMPLATE,
}

def main():
    print(""" 
-----------------------------
🔥 SYNTHETIC DATA GENERATOR 🔥
-----------------------------""")

    # Step 1: Template selection
    print("\nAvailable Templates:\n")
    for idx, tname in enumerate(TEMPLATES.keys(), start=1):
        print(f"{idx}. {tname}\n")

    template_choice = input("\nSelect a Template (number): ").strip()

    # Validate choice
    try:
        template_index = int(template_choice) - 1
        template_name = list(TEMPLATES.keys())[template_index]
    except (ValueError, IndexError):
        print("❌ Invalid template selection!")
        return
    
    template = TEMPLATES[template_name]

    # Step 2: Show subcategories
    print("\nAvailable Subcategories:")
    subcats = list(template["subcategories"].keys())
    for idx, sc in enumerate(subcats, start=1):
        print(f"{idx}. {sc}")

    selected_input = input("\nEnter Subcategories (comma-separated numbers): ").strip()

    try:
        selected_indices = [int(x) - 1 for x in selected_input.split(",")]
        selected_subcats = [subcats[i] for i in selected_indices]
    except Exception:
        print("❌ Invalid subcategory selection!")
        return
    
    # Step 3: Count
    try:
        count = int(input("\nEnter number of rows to generate: ").strip())
    except ValueError:
        print("❌ Invalid count!")
        return
    
    # Step 4: Seed (optional)
    seed_input = input("\nEnter Seed (press Enter to skip): ").strip()
    seed = int(seed_input) if seed_input else None

    # Step 5: Generate data
    print("\nGenerating Synthetic Data...")
    start = time.time()
    data = generate_from_template(template, selected_subcats, count, seed)
    end = time.time()
    
    df = pd.DataFrame(data)
    
    print(f"\n✅ DATA GENERATED SUCCESSFULLY!")
    print("==============================")
    print("           SUMMARY          \n")
    print(f"* Template: {template_name}")
    print(f"⏱ Time Taken: {end - start:.2f} seconds")
    print(f"* Rows Generated: {count}")
    print(f"* Columns Generated: {len(df.columns)}")
    print(f"* Seed: {seed_input}")
    print("==============================")
    
    # Step 6: Files export and data preview
    print("\nSelect what you want to do next:")
    print("1. Preview data (first 5 rows)")
    print("2. Save as CSV")
    print("3. Save as JSON")
    print("4. Exit\n")

    user_input = input("Enter options (comma-separated): ")
    choices = [c.strip() for c in user_input.split(",")]

    # Current working directory
    cwd = os.getcwd()

    if "1" in choices:
        print("\n---- DATA PREVIEW (top 5 rows) ----")
        print(f"{df.head().to_string(index=False)}\n")

    if "2" in choices:
        file_name_input = input("Enter CSV file name (e.g., mydata.csv or folder/mydata): ").strip()
        if not file_name_input.endswith(".csv"):
            file_name_input += ".csv"
        output_path = os.path.join(cwd, file_name_input)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✔ CSV saved at: {output_path}\n")

    if "3" in choices:
        file_name_input = input("Enter JSON file name (e.g., mydata.json or folder/mydata): ").strip()
        if not file_name_input.endswith(".json"):
            file_name_input += ".json"
        output_path = os.path.join(cwd, file_name_input)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_json(output_path, orient="records", indent=4)
        print(f"✔ JSON saved at: {output_path}\n")

    if "4" in choices:
        print("Exiting...\n")

    print("\nThank you for using Synthetic Data Generator!")


if __name__ == "__main__":
    main()