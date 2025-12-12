# SMART Model Card

A Python library for generating standardized AI/ML model documentation cards with OMOP Common Data Model integration for healthcare applications.

## Overview

SMART Model Card provides tools for creating structured model documentation following healthcare AI/ML best practices. The library includes:

- Interactive CLI wizard with validation
- OMOP CDM integration via OHDSI WebAPI
- Multiple export formats (HTML, JSON, Markdown)
- Automated visualization generation
- Provenance tracking with cryptographic hashing

Healthcare AI/ML models require rigorous documentation for regulatory compliance, clinical validation, deployment safety, reproducibility, and transparency. This library automates the documentation process while maintaining flexibility for diverse use cases.

## Installation

### From PyPI

```bash
pip install smart-model-card
```

### From Source

```bash
git clone https://github.com/ankurlohachab/smart-model-card.git
cd smart-model-card
pip install -e .
```

### Optional Dependencies

OMOP integration support:
```bash
pip install smart-model-card[omop]
```

Visualization support:
```bash
pip install smart-model-card[viz]
```

Development tools:
```bash
pip install smart-model-card[dev]
```

All dependencies:
```bash
pip install smart-model-card[all]
```

### Requirements

- Python >= 3.8
- requests >= 2.25.0
- smart-omop >= 0.1.0 (optional, for OMOP integration)
- matplotlib >= 3.3.0 (optional, for visualizations)

## Quick Start

### Interactive Wizard

Create a model card using the interactive CLI:

```bash
smart-model-card interactive
```

The wizard provides:
- Step-by-step prompts for all 7 sections
- Input validation (dates: YYYY-MM-DD, emails, numeric ranges)
- OMOP data integration option
- Default values for common fields

Example session:
```
SECTION 1: Model Details
  Model Name: COPD-Risk-Predictor
  Version [1.0.0]: 1.0.0
  Release Date (YYYY-MM-DD): 2025-01-15
  Support Contact (email): researcher@hospital.org

✓ Model Card Creation Complete!

Your model card has been saved to:
  • HTML: /path/to/output/model_card.html
  • JSON: /path/to/output/model_card.json

To view your model card:
  open /path/to/output/model_card.html
```

### Programmatic Usage

Basic example:

```python
from smart_model_card import ModelCard, ModelDetails, IntendedUse
from smart_model_card.sections import DataFactors, SourceDataset
from smart_model_card.exporters import HTMLExporter

# Create model card
card = ModelCard()

# Section 1: Model Details
card.set_model_details(ModelDetails(
    model_name="Diabetes-Risk-Model",
    version="2.1.0",
    developer_organization="University Hospital Research Lab",
    release_date="2025-01-15",
    description="Predicts 5-year diabetes risk using EHR data",
    intended_purpose="decision_support",
    algorithms_used="XGBoost Classifier",
    licensing="MIT",
    support_contact="ai-team@hospital.org"
))

# Section 2: Intended Use
card.set_intended_use(IntendedUse(
    primary_intended_users="Primary care physicians",
    clinical_indications="Patients aged 40-75 with pre-diabetes indicators",
    patient_target_group="Adults with BMI > 25 and family history of diabetes",
    intended_use_environment="hospital_outpatient"
))

# Section 3: Data Factors
card.set_data_factors(DataFactors(
    source_datasets=[
        SourceDataset(
            name="Hospital EHR Database",
            origin="Academic Medical Center",
            size=15000,
            collection_period="2018-2023",
            population_characteristics="Adult patients, 45% female, mean age 62"
        )
    ],
    data_distribution_summary="Balanced dataset with 30% positive cases",
    data_representativeness="Representative of urban academic hospital population",
    data_governance="IRB-approved, HIPAA-compliant data access"
))

# Export to HTML
HTMLExporter.export(card, "output/diabetes_model_card.html")
```

## Features

### Validation

The interactive wizard validates:

| Input Type | Validation Rule |
|-----------|-----------------|
| Dates | YYYY-MM-DD format (e.g., 2025-01-15) |
| Emails | Standard email format (user@example.com) |
| Metrics | Numeric range 0.0-1.0 |
| Dataset Sizes | Integer >= 0 |
| Retry Limit | Maximum 5 attempts per field |

### OMOP CDM Support

Integrate observational health data:

- Cohort extraction from OHDSI ATLAS
- Heracles report parsing for demographic characterizations
- Athena API integration for concept enrichment
- Automatic demographic table generation
- Age/gender/race distribution visualizations

### Export Formats

**HTML:**
- Interactive collapsible sections
- Searchable tables
- Pagination support
- Embedded visualizations
- Multi-dataset dropdown switching
- Print-friendly styling
- Interactive tooltips for field descriptions

**JSON:**
- Structured schema
- Machine-readable format
- Version control friendly
- API-compatible

**Markdown:**
- Plain text format
- Git diff friendly
- Easy manual editing

### Structure

All model cards include 7 sections:

1. **Model Details**: Name, version, developer, release date, algorithms, licensing, contact
2. **Intended Use**: Target users, clinical indications, patient population, environment, warnings
3. **Data & Factors**: Source datasets, distribution, representativeness, governance
4. **Features & Outputs**: Input features, output types, uncertainty quantification
5. **Performance & Validation**: Validation datasets, metrics, calibration, fairness
6. **Methodology**: Development workflow, training procedure, preprocessing, explainability
7. **Additional Information**: Benefits, risks, ethics, limitations, recommendations

## CLI Reference

### Interactive Mode

```bash
smart-model-card interactive
```

Launch interactive wizard for model card creation.

### Validation

```bash
smart-model-card validate model_card.json
```

Validate existing model card against schema.

### Export

```bash
# Export to HTML
smart-model-card export model_card.json --format html -o output.html

# Export to JSON
smart-model-card export model_card.json --format json -o output.json

# Export to Markdown
smart-model-card export model_card.json --format markdown -o output.md
```

### Scaffold Generation

```bash
smart-model-card create --model-name "MyModel" -o scaffold.json
```

Generate template model card with placeholder values.

### Provenance

```bash
# Compute hash
smart-model-card hash --card model_card.json

# Compare versions
smart-model-card diff old_card.json new_card.json
```

### Fairness Analysis

```bash
smart-model-card fairness-check model_card.json
```

Analyze fairness metrics and demographic performance.

## Python API

### Core Classes

#### ModelCard

Main container for model card sections.

```python
from smart_model_card import ModelCard

card = ModelCard()
card.set_model_details(details)
card.set_intended_use(use)
card.set_data_factors(data)
card.set_features_outputs(features)
card.set_performance_validation(perf)
card.set_methodology(method)
card.set_additional_info(info)

# Serialize
card_dict = card.to_dict()
```

#### ModelDetails

Section 1: Model information.

```python
from smart_model_card import ModelDetails

details = ModelDetails(
    model_name="MyModel",              # Required
    version="1.0.0",                   # Required
    developer_organization="Org Name", # Required
    release_date="2025-01-15",        # Optional (YYYY-MM-DD)
    description="Model description",   # Required
    intended_purpose="decision_support", # Required
    algorithms_used="Algorithm name",  # Required
    licensing="MIT",                   # Optional
    support_contact="email@org.com"   # Required (validated)
)
```

Purpose options: `decision_support`, `screening`, `diagnosis`, `prognosis`, `other`

#### IntendedUse

Section 2: Clinical context.

```python
from smart_model_card import IntendedUse

use = IntendedUse(
    primary_intended_users="Clinicians",
    clinical_indications="Use cases",
    patient_target_group="Patient population",
    intended_use_environment="hospital_outpatient",
    contraindications="When not to use",           # Optional
    out_of_scope_applications="Out of scope",      # Optional
    warnings="Important warnings"                  # Optional
)
```

Environment options: `hospital_inpatient`, `hospital_outpatient`, `clinic`, `home`, `mobile`, `other`

### Exporters

```python
from smart_model_card.exporters import HTMLExporter, JSONExporter, MarkdownExporter

# Export to different formats
HTMLExporter.export(card, "output/card.html")
JSONExporter.export(card, "output/card.json")
MarkdownExporter.export(card, "output/card.md")
```

## OMOP Integration

### Interactive Wizard

When creating a model card interactively, the wizard prompts for OMOP integration in Section 3:

```
Would you like to add OMOP data? [y/N]: y

Choose integration method:
  1. Fetch existing cohort from OHDSI WebAPI
  2. Create new cohort from scratch
  3. Use locally saved cohort data

Select number: 1

OHDSI WebAPI URL: https://atlas.yourorg.org/WebAPI

Available CDM sources (2):
  1. KAGGLECOPD - Kaggle COPD Dataset
  2. SYNPUF1K - Synthetic Data

Select source number (1-2): 1

Cohort ID: 168

Include Heracles characterization reports? [Y/n]: y

✓ Successfully fetched cohort: COPD Patients 2023
✓ Cohort has 95 persons (status: COMPLETE)
```

The system includes:
- **Automatic source discovery**: Lists available CDM sources from WebAPI
- **URL retry logic**: Up to 3 attempts if connection fails
- **Cohort creation**: Build new cohorts interactively from scratch
- **Person count validation**: Verifies cohort generation status

### Programmatic Integration

```python
from smart_model_card.integrations import OMOPIntegration

# Connect to OHDSI WebAPI
with OMOPIntegration(
    webapi_url="https://atlas.yourorg.org/WebAPI",
    source_key="YOUR_CDM_SOURCE"
) as omop:
    # Fetch cohort with reports
    cohort_data = omop.get_cohort_with_reports(
        cohort_id=168,
        include_heracles=True
    )

# The cohort_data includes:
# - Cohort definition
# - Person count
# - Demographics (age, gender, race)
# - Condition distributions
# - Drug exposures
# - Procedure counts
# - Pre-built DataFactors section

# Add to model card
card.set_data_factors(cohort_data['data_factors'])
```

### Available Reports

When Heracles characterization is included:

- **Person**: Age distribution, gender distribution, race/ethnicity
- **Dashboard**: Overview statistics
- **Conditions**: Diagnosis distributions
- **Drugs**: Medication exposures
- **Procedures**: Procedure utilization

## Examples

The `examples/` directory contains working demonstrations:

### Basic Usage

```bash
python examples/quickstart.py
```

Creates minimal model card with required fields.

### OMOP Integration

```bash
python examples/demo_smart_omop_integration.py
```

Demonstrates OMOP cohort fetching and demographic visualization generation.

### Multi-Dataset

```bash
python examples/demo_multi_dataset.py
```

Documents models trained on multiple datasets with different characteristics.

### Complete Workflow

```bash
python examples/demo_complete_workflow.py
```

End-to-end example including OMOP integration and multiple export formats.

## Testing

### Run Tests

```bash
pytest tests/ -v
```

### Coverage Report

```bash
pytest tests/ --cov=smart_model_card --cov-report=html
```

### Test Suite

- **Model Card Validation** (8 tests): Schema compliance, required fields
- **Provenance Tracking** (3 tests): Hash computation, version comparison
- **CAC Integration** (1 test): Code suggestion functionality
- **Standardization** (4 tests): Section structure, consistency checks

Total: 16 tests

### Specific Tests

```bash
# Standardization tests only
pytest tests/test_standardization.py -v

# Model card tests only
pytest tests/test_model_card.py -v
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/ankurlohachab/smart-model-card.git
cd smart-model-card

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/
```

### Code Style

This project follows PEP 8:

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/
```

### Building

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check distribution
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest tests/`)
6. Commit changes (`git commit -m 'Add my feature'`)
7. Push to branch (`git push origin feature/my-feature`)
8. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file.

## Citation

If you use this library in research or projects, please cite:

```bibtex
@software{smart_model_card,
  title={SMART Model Card: Standardized Model Documentation for Healthcare AI},
  author={Lohachab, Ankur},
  organization={Department of Advanced Computing Sciences, Maastricht University},
  year={2025},
  url={https://github.com/ankurlohachab/smart-model-card}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/ankurlohachab/smart-model-card/issues)
- **Examples**: See `examples/` directory
- **Email**: ankur.lohachab@maastrichtuniversity.nl

## Author

`Ankur Lohachab`,
Department of Advanced Computing Sciences,
Maastricht University
