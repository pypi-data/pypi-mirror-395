# Synthetic Data Generator

A powerful Python package for generating realistic synthetic data for testing, development, and demonstrations. Built with a modular architecture and professional packaging standards.

## Overview

Synthetic Data Generator provides a comprehensive toolkit for creating fake but realistic datasets across multiple domains including e-commerce, healthcare, finance, IoT, education, and more. The package is designed with modularity, testability, and ease of use in mind.

## Features

- **10 Pre-built Templates** covering diverse domains
- **Modular Architecture** with clean separation of concerns
- **CLI Interface** for quick data generation
- **Python API** for programmatic usage
- **Data Profiling** capabilities for analyzing generated datasets
- **Multiple Export Formats** (CSV, JSON)
- **Reproducible Results** with seed support
- **Extensible Design** for custom templates

## Installation

### 📦 Install from PyPI (Recommended)

The easiest way to install `synthetic-data-maker`:

```bash
pip install synthetic-data-maker
```

To upgrade to the latest version:

```bash
pip install synthetic-data-maker --upgrade 
```

### 🧪 Verify Installation

Check the installed version:

```bash
pip show structured-data-generator
```

### 🐍 Install in Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install package
pip install synthetic-data-maker
```

### 📁 Install from Source (For Development)

```bash
# Clone or navigate to the project directory
cd structured_data_generator

# Install in development mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

### 🧰 Uninstalling

To remove the package:

```bash
pip uninstall synthetic-data-maker
```

### ✅ Requirements

- ✔ Python 3.8+
- ✔ pip installed
- ✔ Internet connection (only for installation)

## Quick Start

### ⚙️ Available CLI Commands

After installation, two CLI commands become available globally:

#### ➤ 1. Generate Dataset

```bash
generate-dataset
```

This launches an interactive CLI that guides you through:
1. Select a template (e.g., User, E-commerce, Healthcare)
2. Choose subcategories (specific data fields)
3. Specify number of rows
4. Optionally set a seed for reproducibility
5. Preview and export data as CSV or JSON

#### ➤ 2. Profile Dataset

```bash
profile-dataset data/generated/output.csv
```

Analyze any CSV or JSON dataset to get comprehensive statistics.

### 📁 Basic Usage Examples

**Generate a dataset:**
```bash
generate-dataset
```

**Profile an existing dataset:**
```bash
profile-dataset output.csv
```

### Using the CLI (Development Mode)

If you installed from source, you can also run:

```bash
python scripts/generate_dataset.py
python scripts/profile_dataset.py data.csv
```

### Using as a Python Module

```python
from structured_data_generator.core.generators import (
    USER_TEMPLATE, 
    ECOM_TEMPLATE,
    generate_from_template
)

# Generate 100 user profiles
data = generate_from_template(
    USER_TEMPLATE,
    ["Personal Info", "Address", "Account Info"],
    count=100,
    seed=42
)

# Save to CSV
from structured_data_generator.io.csv_handler import save_to_csv
save_to_csv(data, "users.csv")

# Save to JSON
from structured_data_generator.io.json_handler import save_to_json
save_to_json(data, "users.json")
```

## Available Templates

### 1. USER_TEMPLATE
Generate user profiles and account information.

**Subcategories:**
- Personal Info: Name, username, email, phone, gender, date of birth
- Address: Street, city, state, country, pincode
- Account Info: Creation date, last login, account status
- Preferences: Language, currency, marketing opt-in
- Device Info: Device type, OS, browser

**Use Cases:** User databases, authentication systems, customer profiles

### 2. ECOM_TEMPLATE
Generate e-commerce transaction data.

**Subcategories:**
- Order Info: Order ID, transaction date, status, total amount
- Customer Info: User ID, name, email, phone
- Product Info: Product ID, name, category, quantity, price
- Payment Info: Payment method, status, transaction ID
- Shipping Info: Address, shipping partner, shipping status
- Device Info: Device type, OS, browser

**Use Cases:** E-commerce platforms, order management systems, payment testing

### 3. FINANCIAL_TEMPLATE
Generate banking and financial transaction data.

**Subcategories:**
- Account Info: Account ID, type, bank name, IFSC code
- Transaction Info: Transaction ID, date, type, amount, status
- Customer Info: Customer ID, name, email, PAN, Aadhaar
- Card Info: Card type, network, last 4 digits
- Loan Info: Loan ID, type, amount, interest rate, EMI
- Device Info: Device type, OS, browser

**Use Cases:** Banking applications, financial dashboards, transaction analytics

### 4. HEALTHCARE_TEMPLATE
Generate medical records and patient data.

**Subcategories:**
- Patient Info: Patient ID, name, age, gender, blood group, risk score
- Medical Record: Record ID, diagnosis, symptoms, severity
- Doctor Info: Doctor ID, name, specialization, hospital
- Appointment Info: Appointment ID, date, status, consultation type
- Prescription Info: Prescription ID, medicine, dosage, duration
- Billing Info: Invoice ID, consultation fee, medicine charges, total bill
- Device Info: Device type, OS, browser

**Use Cases:** Hospital management systems, telemedicine apps, medical records

### 5. IOT_SENSOR_TEMPLATE
Generate IoT sensor readings and device data.

**Subcategories:**
- Device Info: Device ID, type, firmware version, manufacturer
- Location Data: Latitude, longitude, altitude, zone
- Sensor Readings: Temperature, humidity, air quality, CO2, motion
- Network Data: Signal strength, connection type, IP address
- Battery Power: Battery level, health, charging status
- Timestamp Info: Timestamp, last maintenance

**Use Cases:** IoT dashboards, sensor data analysis, smart home testing

### 6. NLP_TEXT_TEMPLATE
Generate text data for NLP applications.

**Subcategories:**
- Basic Text: Sentences, paragraphs, words, keywords
- Document Metadata: Title, author, published year, document type
- NLP Annotations: Language, sentiment, emotion, toxicity, reading level
- Synthetic NER Data: Person names, locations, organizations
- Text Stats: Word count, character count, average word length
- Timestamp Info: Created at, updated at

**Use Cases:** NLP model testing, text analysis, chatbot training

### 7. WEB_ANALYTICS_TEMPLATE
Generate website analytics and user behavior data.

**Subcategories:**
- Session Info: Session ID, user ID, duration, engagement score
- Page Metrics: URL, time on page, scroll depth, interactions, CTR
- Traffic Source: Source, medium, campaign, keyword
- Device Info: Device type, browser, OS, screen resolution
- Geo Data: IP address, country, city, timezone
- Performance: Page load time, DNS lookup, TTFB, JS errors

**Use Cases:** Analytics dashboards, website performance testing, traffic analysis

### 8. IMAGE_METADATA_TEMPLATE
Generate image metadata and EXIF data.

**Subcategories:**
- Basic Info: Image ID, filename, format, file size, color mode
- Dimensions: Width, height, aspect ratio, DPI
- Camera EXIF: Camera make/model, lens, focal length, aperture, ISO
- Geolocation: Latitude, longitude, country, city
- Tags Labels: Primary label, secondary labels, confidence score
- Color Stats: Dominant color, brightness, contrast
- Timestamp Info: Created at, uploaded at, last modified

**Use Cases:** Image databases, photo library apps, image analysis

### 9. EDU_STUDENT_TEMPLATE
Generate student academic records.

**Subcategories:**
- Student Profile: Student ID, name, age, gender, grade level
- Academic Scores: Math, science, English, social science, computer scores
- Attendance: Total classes, classes attended, attendance percentage
- Behavior Activity: Disciplinary actions, participation, sports score
- Performance Metrics: Study hours, homework completion, participation score
- Timestamp Info: Record created, last updated

**Use Cases:** School management systems, student performance dashboards

### 10. PRODUCT_CATALOG_TEMPLATE
Generate product catalog data.

**Subcategories:**
- Basic Info: Product ID, name, category, brand, description
- Variants: Color, size, material, model number
- Pricing: Price, discount, final price, currency
- Inventory: Stock status, quantity, warehouse location, restock date
- Ratings Reviews: Average rating, total reviews, review text
- Timestamps: Released at, last updated

**Use Cases:** E-commerce catalogs, product databases, inventory management

## Project Structure

```
structured_data_generator/
├── README.md                          # This file
├── pyproject.toml                     # Modern Python packaging
├── requirements.txt                   # Dependencies
├── LICENSE                            # MIT License
│
├── structured_data_generator/         # Main package
│   ├── __init__.py
│   │
│   ├── core/                          # Core generation logic
│   │   ├── __init__.py
│   │   ├── generators.py              # All templates and generation engine
│   │   ├── constraints.py             # Data constraints and validation
│   │   └── utils.py                   # Helper functions, seed management
│   │
│   ├── io/                            # Input/output handling
│   │   ├── __init__.py
│   │   ├── csv_handler.py             # CSV operations
│   │   └── json_handler.py            # JSON operations
│   │
│   ├── profiling/                     # Data profiling
│   │   ├── __init__.py
│   │   └── profiler.py                # Dataset profiling and statistics
│   │
│   └── config/                        # Configuration
│       ├── __init__.py
│       └── default_config.py          # Default settings
│
├── scripts/                           # CLI scripts
│   ├── __init__.py
│   ├── generate_dataset.py            # Main CLI for data generation
│   └── profile_dataset.py             # CLI for profiling datasets
│
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_generators.py
│   ├── test_constraints.py
│   ├── test_io.py
│   └── test_profiler.py
│
└── examples/                          # Example notebooks
    ├── numeric_example.ipynb
    ├── categorical_example.ipynb
    └── timeseries_example.ipynb
```

## Usage Examples

### Example 1: Generate User Profiles

```python
from structured_data_generator.core.generators import USER_TEMPLATE, generate_from_template
from structured_data_generator.io.csv_handler import save_to_csv

# Generate 50 user profiles
users = generate_from_template(
    USER_TEMPLATE,
    ["Personal Info", "Address", "Account Info"],
    count=50,
    seed=123
)

# Save to CSV
save_to_csv(users, "user_profiles.csv")
```

### Example 2: Generate E-commerce Orders

```python
from structured_data_generator.core.generators import ECOM_TEMPLATE, generate_from_template
from structured_data_generator.io.json_handler import save_to_json

# Generate 100 orders
orders = generate_from_template(
    ECOM_TEMPLATE,
    ["Order Info", "Customer Info", "Product Info", "Payment Info"],
    count=100,
    seed=42
)

# Save to JSON
save_to_json(orders, "orders.json")
```

### Example 3: Generate Healthcare Data

```python
from structured_data_generator.core.generators import HEALTHCARE_TEMPLATE, generate_from_template

# Generate 200 patient records
patients = generate_from_template(
    HEALTHCARE_TEMPLATE,
    ["Patient Info", "Medical Record", "Doctor Info"],
    count=200
)

# Display first few rows
print(patients.head())
```

### Example 4: Profile a Dataset

```python
from structured_data_generator.profiling.profiler import generate_profile, print_profile
import pandas as pd

# Load a dataset
df = pd.read_csv("users.csv")

# Generate and print profile
profile = generate_profile(df)
print_profile(profile)
```

Or use the CLI:

```bash
python scripts/profile_dataset.py users.csv
```

## Advanced Usage

### Custom Configuration

Edit `structured_data_generator/config/default_config.py` to customize:

```python
DEFAULT_CONFIG = {
    'locale': 'en_US',           # Faker locale
    'default_rows': 100,         # Default number of rows
    'default_seed': None,        # Default seed
    'csv_index': False,          # Include index in CSV
    'json_orient': 'records',    # JSON orientation
    'json_indent': 4,            # JSON indentation
}
```

### Creating Custom Templates

Add your own template to `structured_data_generator/core/generators.py`:

```python
CUSTOM_TEMPLATE = {
    "template_name": "my_custom_template",
    "subcategories": {
        "Basic Info": {
            "ID": lambda: str(uuid.uuid4()),
            "Name": lambda: fake.name(),
            "Custom Field": lambda: random.choice(["A", "B", "C"])
        }
    }
}
```

### Using Constraints

```python
from structured_data_generator.core.constraints import enforce_range, ensure_uniqueness

# Enforce value range
value = enforce_range(150, min_val=0, max_val=100)  # Returns 100

# Ensure uniqueness
unique_list = ensure_uniqueness([1, 2, 2, 3, 3, 4])  # Returns [1, 2, 3, 4]
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_generators

# Run with verbose output
python -m unittest discover tests -v
```

## Data Profiling

Profile any generated dataset to get comprehensive statistics:

```bash
python scripts/profile_dataset.py data.csv
```

Output includes:
- Dataset shape (rows × columns)
- Memory usage
- Column names and data types
- Missing values
- Numeric statistics (mean, std, min, max, quartiles)

## Configuration

The package uses sensible defaults but can be customized:

- **Locale**: Change Faker locale for region-specific data
- **Default rows**: Set default number of rows to generate
- **Seed behavior**: Control randomness and reproducibility
- **Export settings**: Customize CSV and JSON output formats

## Dependencies

- **pandas** (>=1.3.0): Data manipulation and analysis
- **faker** (>=8.0.0): Realistic fake data generation
- **numpy**: Numerical operations (installed with pandas)

## Best Practices

1. **Use seeds for reproducibility**: When testing, always use a seed to get consistent results
2. **Start small**: Generate 10-100 rows first to verify the output
3. **Select only needed subcategories**: Don't generate unnecessary fields
4. **Profile your data**: Use the profiler to understand your generated datasets
5. **Batch large datasets**: For millions of rows, generate in batches

## Performance

Generation speed depends on:
- Number of rows
- Number of fields
- Complexity of field generators

Typical performance:
- 100 rows: ~1-2 seconds
- 1,000 rows: ~5-10 seconds
- 10,000 rows: ~30-60 seconds

## Limitations

- All data is synthetic and fake - not suitable for production use with real users
- Some field combinations may not be perfectly realistic
- Large datasets (millions of rows) may require significant memory

## Contributing

To add new templates or features:

1. Add template to `structured_data_generator/core/generators.py`
2. Export in `structured_data_generator/core/__init__.py`
3. Add tests in `tests/test_generators.py`
4. Update this README

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- Check the examples in the `examples/` directory
- Review test files in `tests/` for usage patterns
- Refer to `STRUCTURE_README.md` for detailed architecture information

## Version

Current Version: 0.3.1

## Acknowledgments

Built with:
- [Faker](https://faker.readthedocs.io/) for realistic fake data generation
- [Pandas](https://pandas.pydata.org/) for data manipulation
- Python's standard library for core functionality
