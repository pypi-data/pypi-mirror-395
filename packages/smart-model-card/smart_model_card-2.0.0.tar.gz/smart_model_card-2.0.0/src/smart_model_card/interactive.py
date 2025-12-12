"""
Interactive CLI for guided model card creation

Author: Ankur Lohachab
Department of Advanced Computing Sciences, Maastricht University
"""

import sys
import re
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from smart_model_card import ModelCard, ModelDetails, IntendedUse
from smart_model_card.sections import (
    DataFactors, FeaturesOutputs, PerformanceValidation,
    Methodology, AdditionalInfo, SourceDataset, InputFeature,
    OutputFeature, ValidationDataset, PerformanceMetric
)
from smart_model_card.exporters import HTMLExporter, JSONExporter


# ============================================================================
# Input Validation Functions
# ============================================================================

def validate_date(date_str: str) -> bool:
    """Validate date in YYYY-MM-DD format"""
    if not date_str:
        return True  # Allow empty for optional fields

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return True  # Allow empty for optional fields

    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_numeric_range(value: float, min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
    """Validate numeric value is within range"""
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True


# ============================================================================
# Prompt Functions
# ============================================================================

def prompt_input(prompt: str, required: bool = True, default: Optional[str] = None, validator=None, validator_msg: str = "Invalid input format") -> str:
    """Prompt user for input with optional default and validation"""
    if default:
        prompt = f"{prompt} [{default}]"

    while True:
        value = input(f"  {prompt}: ").strip()

        if not value and default:
            return default

        if not value and not required:
            return ""

        if not value and required:
            print("  ⚠ This field is required. Please provide a value.")
            continue

        # Apply validator if provided
        if validator and not validator(value):
            print(f"  ⚠ {validator_msg}")
            continue

        return value


def prompt_choice(prompt: str, choices: List[str]) -> str:
    """Prompt user to select from choices with retry limit"""
    print(f"\n  {prompt}")
    for i, choice in enumerate(choices, 1):
        print(f"    {i}. {choice}")

    max_retries = 5
    retries = 0

    while retries < max_retries:
        selection = input("  Select number: ").strip()
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
            else:
                print(f"  ⚠ Please enter a number between 1 and {len(choices)}.")
        except ValueError:
            print(f"  ⚠ Please enter a valid number (1-{len(choices)}).")

        retries += 1
        if retries < max_retries:
            print(f"  (Attempt {retries + 1}/{max_retries})")

    print(f"  ⚠ Too many invalid attempts. Using default: {choices[0]}")
    return choices[0]


def prompt_yes_no(prompt: str, default: bool = False) -> bool:
    """Prompt yes/no question"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"  {prompt} [{default_str}]: ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']


def prompt_float(prompt: str, required: bool = True, min_val: Optional[float] = None, max_val: Optional[float] = None) -> Optional[float]:
    """Prompt for float value with optional range validation"""
    while True:
        value = input(f"  {prompt}: ").strip()

        if not value and not required:
            return None

        if not value and required:
            print("  ⚠ This field is required.")
            continue

        try:
            num = float(value)
            if not validate_numeric_range(num, min_val, max_val):
                range_msg = ""
                if min_val is not None and max_val is not None:
                    range_msg = f"between {min_val} and {max_val}"
                elif min_val is not None:
                    range_msg = f"greater than or equal to {min_val}"
                elif max_val is not None:
                    range_msg = f"less than or equal to {max_val}"
                print(f"  ⚠ Value must be {range_msg}.")
                continue
            return num
        except ValueError:
            print("  ⚠ Please enter a valid number.")


def prompt_int(prompt: str, required: bool = True, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Optional[int]:
    """Prompt for integer value with optional range validation"""
    while True:
        value = input(f"  {prompt}: ").strip()

        if not value and not required:
            return None

        if not value and required:
            print("  ⚠ This field is required.")
            continue

        try:
            num = int(value)
            if not validate_numeric_range(num, min_val, max_val):
                range_msg = ""
                if min_val is not None and max_val is not None:
                    range_msg = f"between {min_val} and {max_val}"
                elif min_val is not None:
                    range_msg = f"greater than or equal to {min_val}"
                elif max_val is not None:
                    range_msg = f"less than or equal to {max_val}"
                print(f"  ⚠ Value must be {range_msg}.")
                continue
            return num
        except ValueError:
            print("  ⚠ Please enter a valid integer.")


# ============================================================================
# OMOP Integration
# ============================================================================

def prompt_omop_integration() -> Optional[Dict[str, Any]]:
    """Prompt for OMOP data integration with improved workflow"""
    print("\n" + "-"*60)
    print("OMOP CDM Integration (Optional)")
    print("-"*60)
    print("You can integrate OMOP Common Data Model cohort data.")
    print("This requires smart-omop package and OHDSI WebAPI access.")

    if not prompt_yes_no("Would you like to add OMOP data?", default=False):
        return None

    try:
        from smart_model_card.integrations import OMOPIntegration
        from smart_omop import CohortBuilder

        print("\n  Choose integration method:")
        print("    1. Fetch existing cohort from OHDSI WebAPI")
        print("    2. Create new cohort from scratch")
        print("    3. Use locally saved cohort data")

        max_retries = 5
        retries = 0
        choice_idx = -1

        while retries < max_retries:
            selection = input("  Select number: ").strip()
            try:
                choice_idx = int(selection) - 1
                if 0 <= choice_idx < 3:
                    break
                print(f"  Please enter a number between 1 and 3")
                retries += 1
            except ValueError:
                print(f"  Please enter a valid number")
                retries += 1

        if retries >= max_retries or choice_idx == -1:
            print("  Too many invalid attempts. Skipping OMOP integration.")
            return None

        # Option 1: Fetch existing cohort
        if choice_idx == 0:
            return _fetch_existing_cohort()

        # Option 2: Create new cohort
        elif choice_idx == 1:
            return _create_new_cohort()

        # Option 3: Use local data
        else:
            print("\n  For local OMOP data, you can manually add it after creation.")
            print("  Skipping OMOP integration for now.")
            return None

    except ImportError:
        print("\n  ⚠ OMOP integration requires 'smart-omop' package.")
        print("  Install it with: pip install smart-omop")
        print("  Skipping OMOP integration.")
        return None
    except Exception as e:
        print(f"\n  ⚠ Unexpected error: {e}")
        print("  Skipping OMOP integration.")
        return None


def _fetch_existing_cohort() -> Optional[Dict[str, Any]]:
    """Fetch existing cohort from WebAPI"""
    from smart_model_card.integrations import OMOPIntegration
    from smart_omop import OMOPClient

    # Retry loop for WebAPI URL
    max_url_retries = 3
    sources = None
    selected_source = None
    cohort_id = None
    include_heracles = True
    webapi_url = None

    for url_attempt in range(max_url_retries):
        webapi_url = prompt_input("\n  OHDSI WebAPI URL (e.g., https://your-atlas.org/WebAPI)", required=True)

        print("\n  Connecting to OHDSI WebAPI...")

        try:
            # First, fetch available sources
            with OMOPClient(webapi_url) as client:
                print("  Fetching available CDM sources...")
                sources = client.get_sources()

                if not sources:
                    print("  ⚠ No CDM sources found on this WebAPI.")
                    print("  Please check your WebAPI URL or contact your administrator.")

                    if url_attempt < max_url_retries - 1:
                        if prompt_yes_no("\n  Retry with different URL?", default=True):
                            continue
                        else:
                            return None
                    else:
                        return None

                print(f"\n  Available CDM sources ({len(sources)}):")
                for i, source in enumerate(sources, 1):
                    source_key = source.get('sourceKey', 'Unknown')
                    source_name = source.get('sourceName', 'Unknown')
                    print(f"    {i}. {source_key} - {source_name}")

                # Let user select source
                max_retries = 5
                retries = 0
                selected_source = None

                while retries < max_retries:
                    selection = input(f"\n  Select source number (1-{len(sources)}): ").strip()
                    try:
                        source_idx = int(selection) - 1
                        if 0 <= source_idx < len(sources):
                            selected_source = sources[source_idx]
                            break
                        print(f"  Please enter a number between 1 and {len(sources)}")
                        retries += 1
                    except ValueError:
                        print(f"  Please enter a valid number")
                        retries += 1

                if retries >= max_retries or not selected_source:
                    print("  Too many invalid attempts. Skipping OMOP integration.")
                    return None

                source_key = selected_source['sourceKey']
                print(f"\n  Selected source: {source_key}")

                # Ask for cohort ID
                cohort_id = prompt_int("\n  Cohort ID", required=True, min_val=1)

                # Ask about Heracles reports
                include_heracles = prompt_yes_no("\n  Include Heracles characterization reports?", default=True)

                # Successfully connected - break out of retry loop
                break

        except Exception as e:
            print(f"\n  ⚠ Error connecting to WebAPI: {e}")
            print("  Please check your WebAPI URL and network connection.")

            if url_attempt < max_url_retries - 1:
                if prompt_yes_no("\n  Retry with different URL?", default=True):
                    continue
                else:
                    return None
            else:
                print("  Maximum connection attempts reached.")
                return None

    # If we couldn't connect after all retries
    if not sources or not selected_source or cohort_id is None or webapi_url is None:
        return None

    # Fetch cohort data
    try:
        print("\n  Fetching cohort data...")

        with OMOPIntegration(webapi_url=webapi_url, source_key=source_key) as integration:
            cohort_data = integration.get_cohort_with_reports(
                cohort_id=cohort_id,
                include_heracles=include_heracles
            )

        print(f"\n  ✓ Successfully fetched cohort: {cohort_data.get('name', 'Unknown')}")
        return cohort_data

    except Exception as e:
        print(f"\n  ⚠ Error fetching cohort: {e}")

        # Provide helpful suggestions
        if "does not exist" in str(e).lower():
            print(f"\n  Cohort ID {cohort_id} was not found.")
            print(f"  Suggestions:")
            print(f"    - Check the cohort ID in ATLAS web interface")
            print(f"    - Use smart-omop CLI to list available cohorts")
        elif "heracles" in str(e).lower():
            print(f"\n  Heracles reports may not be available for this cohort.")
            print(f"  You can:")
            print(f"    - Run Heracles analysis first using smart-omop CLI")
            print(f"    - Retry without Heracles reports")

        return None


def _create_new_cohort() -> Optional[Dict[str, Any]]:
    """Create new cohort from scratch"""
    from smart_model_card.integrations import OMOPIntegration
    from smart_omop import OMOPClient, CohortBuilder

    print("\n  Creating new cohort from scratch")

    # Retry loop for WebAPI URL
    max_url_retries = 3
    sources = None
    selected_source = None
    webapi_url = None

    for url_attempt in range(max_url_retries):
        webapi_url = prompt_input("\n  OHDSI WebAPI URL (e.g., https://your-atlas.org/WebAPI)", required=True)

        print("\n  Connecting to OHDSI WebAPI...")

        try:
            # Fetch available sources
            with OMOPClient(webapi_url) as client:
                print("  Fetching available CDM sources...")
                sources = client.get_sources()

                if not sources:
                    print("  ⚠ No CDM sources found on this WebAPI.")

                    if url_attempt < max_url_retries - 1:
                        if prompt_yes_no("\n  Retry with different URL?", default=True):
                            continue
                        else:
                            return None
                    else:
                        return None

                print(f"\n  Available CDM sources ({len(sources)}):")
                for i, source in enumerate(sources, 1):
                    source_key = source.get('sourceKey', 'Unknown')
                    source_name = source.get('sourceName', 'Unknown')
                    print(f"    {i}. {source_key} - {source_name}")

                # Let user select source
                max_retries = 5
                retries = 0
                selected_source = None

                while retries < max_retries:
                    selection = input(f"\n  Select source number (1-{len(sources)}): ").strip()
                    try:
                        source_idx = int(selection) - 1
                        if 0 <= source_idx < len(sources):
                            selected_source = sources[source_idx]
                            break
                        print(f"  Please enter a number between 1 and {len(sources)}")
                        retries += 1
                    except ValueError:
                        print(f"  Please enter a valid number")
                        retries += 1

                if retries >= max_retries or not selected_source:
                    print("  Too many invalid attempts. Skipping OMOP integration.")
                    return None

                source_key = selected_source['sourceKey']
                print(f"\n  Selected source: {source_key}")

                # Successfully connected - break out of retry loop
                break

        except Exception as e:
            print(f"\n  ⚠ Error connecting to WebAPI: {e}")
            print("  Please check your WebAPI URL and network connection.")

            if url_attempt < max_url_retries - 1:
                if prompt_yes_no("\n  Retry with different URL?", default=True):
                    continue
                else:
                    return None
            else:
                print("  Maximum connection attempts reached.")
                return None

    # If we couldn't connect after all retries
    if not sources or not selected_source or webapi_url is None:
        return None

    # Gather cohort definition details
    print("\n  Define your cohort:")
    cohort_name = prompt_input("  Cohort name", required=True)
    cohort_description = prompt_input("  Description", required=False)

    print("\n  Inclusion criteria:")
    concept_ids_str = prompt_input("  Concept IDs (comma-separated, e.g., 255573)", required=True)
    concept_ids = [int(x.strip()) for x in concept_ids_str.split(",") if x.strip().isdigit()]

    if not concept_ids:
        print("  ⚠ No valid concept IDs provided. Cannot create cohort.")
        return None

    min_age = prompt_input("  Minimum age (leave empty for no limit)", required=False)
    max_age = prompt_input("  Maximum age (leave empty for no limit)", required=False)

    gender = prompt_input("  Gender filter (M/F/leave empty for all)", required=False)

    print("\n  Creating cohort definition...")

    try:
        from smart_omop import Gender

        with OMOPClient(webapi_url) as client:
            # Build cohort using CohortBuilder
            builder = CohortBuilder(cohort_name)

            if cohort_description:
                builder.description = cohort_description

            # Add condition criteria (all concept IDs at once)
            builder.with_condition("Conditions", concept_ids)

            # Add age filter
            min_age_int = int(min_age) if min_age and min_age.isdigit() else None
            max_age_int = int(max_age) if max_age and max_age.isdigit() else None

            if min_age_int is not None or max_age_int is not None:
                builder.with_age_range(min_age=min_age_int, max_age=max_age_int)

            # Add gender filter
            if gender and gender.upper() in ['M', 'F']:
                gender_enum = Gender.MALE if gender.upper() == 'M' else Gender.FEMALE
                builder.with_gender(gender_enum)

            # Create cohort
            cohort_def = builder.build()
            created_cohort = client.create_cohort(cohort_def.to_dict())
            cohort_id = created_cohort.get('id')

            print(f"  ✓ Cohort created with ID: {cohort_id}")

            # Ask if user wants to generate it now
            if prompt_yes_no("\n  Generate cohort on database now?", default=True):
                print("  Generating cohort...")
                client.generate_cohort(cohort_id, source_key)
                print("  ✓ Cohort generation started (may take a few minutes)")

                # Wait a bit and try to get results
                import time
                time.sleep(5)

                try:
                    # Try to fetch cohort data
                    include_heracles = prompt_yes_no("\n  Include Heracles characterization reports?", default=False)

                    if include_heracles:
                        print("  Note: Heracles reports may not be available immediately.")
                        print("  You may need to run Heracles analysis separately.")

                    with OMOPIntegration(webapi_url=webapi_url, source_key=source_key) as integration:
                        cohort_data = integration.get_cohort_with_reports(
                            cohort_id=cohort_id,
                            include_heracles=include_heracles
                        )

                    print(f"\n  ✓ Successfully fetched cohort: {cohort_data.get('name', 'Unknown')}")
                    return cohort_data

                except Exception as e:
                    print(f"\n  ⚠ Cohort created but couldn't fetch results yet: {e}")
                    print(f"  The cohort may still be generating.")
                    print(f"  You can retry later with cohort ID: {cohort_id}")
                    return None

            else:
                print(f"\n  Cohort created but not generated.")
                print(f"  To generate later, use:")
                print(f"    smart-omop --base-url {webapi_url} generate --cohort-id {cohort_id} --source-key {source_key}")
                return None

    except Exception as e:
        print(f"\n  ⚠ Error creating cohort: {e}")
        import traceback
        traceback.print_exc()
        return None


def section_model_details() -> ModelDetails:
    """Guided input for Section 1: Model Details"""
    print("\n" + "="*60)
    print("SECTION 1: Model Details")
    print("="*60)

    return ModelDetails(
        model_name=prompt_input("Model Name (e.g., COPD-Risk-Predictor-v2)", required=True),
        version=prompt_input("Version", default="1.0.0"),
        developer_organization=prompt_input("Developer/Organization (e.g., University Hospital Research Lab)", required=True),
        release_date=prompt_input(
            "Release Date (YYYY-MM-DD)",
            required=False,
            validator=validate_date,
            validator_msg="Please enter a valid date in YYYY-MM-DD format (e.g., 2025-01-15)"
        ),
        description=prompt_input("Description (e.g., Predicts 5-year diabetes risk using EHR data)", required=True),
        intended_purpose=prompt_choice(
            "Intended Purpose",
            ["decision_support", "screening", "diagnosis", "prognosis", "other"]
        ),
        algorithms_used=prompt_input("Algorithm(s) Used (e.g., XGBoost Classifier, Random Forest)", required=True),
        licensing=prompt_input("License", default="MIT"),
        support_contact=prompt_input(
            "Support Contact (email)",
            required=True,
            validator=validate_email,
            validator_msg="Please enter a valid email address (e.g., user@example.com)"
        )
    )


def section_intended_use() -> IntendedUse:
    """Guided input for Section 2: Intended Use"""
    print("\n" + "="*60)
    print("SECTION 2: Intended Use and Clinical Context")
    print("="*60)

    return IntendedUse(
        primary_intended_users=prompt_input("Primary Intended Users (e.g., Cardiologists, Primary care physicians)", required=True),
        clinical_indications=prompt_input("Clinical Indications (e.g., Risk stratification for heart failure patients)", required=True),
        patient_target_group=prompt_input("Patient Target Group (e.g., Adults aged 40-75 with hypertension)", required=True),
        intended_use_environment=prompt_choice(
            "Intended Use Environment",
            ["hospital_inpatient", "hospital_outpatient", "clinic", "home", "mobile", "other"]
        ),
        contraindications=prompt_input("Contraindications", required=False),
        out_of_scope_applications=prompt_input("Out of Scope Applications", required=False),
        warnings=prompt_input("Warnings", required=False)
    )


def section_data_factors() -> DataFactors:
    """Guided input for Section 3: Data & Factors"""
    print("\n" + "="*60)
    print("SECTION 3: Data & Factors")
    print("="*60)

    # OMOP Integration
    omop_data = prompt_omop_integration()

    # If OMOP data was successfully fetched, use the pre-built DataFactors
    if omop_data and 'data_factors' in omop_data:
        print("\n  ✓ Using OMOP-generated DataFactors")
        print(f"  ✓ Source Dataset: {omop_data['name']}")
        print(f"  ✓ Detailed Reports: {'Included' if omop_data.get('reports') else 'Not available'}")

        # Ask if user wants to add additional datasets
        if prompt_yes_no("\n  Add additional non-OMOP datasets?", default=False):
            print("\n  Adding supplementary datasets...")
            omop_df = omop_data['data_factors']

            while True:
                print(f"\n  Dataset {len(omop_df.source_datasets) + 1}:")
                name = prompt_input("  Dataset Name (e.g., Hospital A - EHR Database)", required=True)
                origin = prompt_input("  Origin/Source (e.g., Academic medical center, 2020-2024)", required=True)
                size = prompt_int("  Size (number of records)", required=True, min_val=1)
                period = prompt_input("  Collection Period (e.g., 2020-01-01 to 2024-12-31)", required=True)
                pop_char = prompt_input("  Population Characteristics (e.g., Urban population, 65% male, mean age 62)", required=True)

                omop_df.source_datasets.append(SourceDataset(name, origin, size, period, pop_char))

                if not prompt_yes_no("\n  Add another dataset?", default=False):
                    break

        return omop_data['data_factors']

    # No OMOP data - proceed with manual entry
    print("\n  Manual data entry (no OMOP integration)")

    # Source datasets
    datasets = []
    print("\nAdd source datasets:")

    while True:
        print(f"\n  Dataset {len(datasets) + 1}:")
        name = prompt_input("  Dataset Name (e.g., Hospital A - EHR Database)", required=True)
        origin = prompt_input("  Origin/Source (e.g., Academic medical center, 2020-2024)", required=True)
        size = prompt_int("  Size (number of records)", required=True, min_val=1)
        period = prompt_input("  Collection Period (e.g., 2020-01-01 to 2024-12-31)", required=True)
        pop_char = prompt_input("  Population Characteristics (e.g., Urban population, 65% male, mean age 62)", required=True)

        datasets.append(SourceDataset(name, origin, size, period, pop_char))

        if not prompt_yes_no("\nAdd another dataset?", default=False):
            break

    return DataFactors(
        source_datasets=datasets,
        data_distribution_summary=prompt_input("Data Distribution Summary (e.g., 10000 patients, balanced age/gender, 30% positive cases)", required=True),
        data_representativeness=prompt_input("Data Representativeness (e.g., Representative of urban academic hospital population)", required=True),
        data_governance=prompt_input("Data Governance (e.g., IRB-approved, HIPAA-compliant, de-identified per Safe Harbor)", required=True),
        omop_detailed_reports=None
    )


def section_features_outputs() -> FeaturesOutputs:
    """Guided input for Section 4: Features & Outputs"""
    print("\n" + "="*60)
    print("SECTION 4: Features & Outputs")
    print("="*60)

    # Input features
    input_features = []
    print("\nAdd input features:")

    while True:
        print(f"\n  Feature {len(input_features) + 1}:")
        name = prompt_input("  Dataset Name (e.g., Hospital A - EHR Database)", required=True)
        data_type = prompt_choice("  Data Type", ["numeric", "categorical", "binary", "text", "image"])
        required = prompt_yes_no("  Required?", default=True)
        domain = prompt_input("  Clinical Domain (e.g., Demographics, Labs, Vitals, Medications)", required=True)

        input_features.append(InputFeature(name, data_type, required, domain))

        if not prompt_yes_no("\nAdd another input feature?", default=True):
            break

    # Output features
    output_features = []
    print("\nAdd output features:")

    while True:
        print(f"\n  Output {len(output_features) + 1}:")
        name = prompt_input("  Dataset Name (e.g., Hospital A - EHR Database)", required=True)
        output_type = prompt_choice("  Type", ["probability", "classification", "regression", "ranking"])

        output_features.append(OutputFeature(name, output_type))

        if not prompt_yes_no("\nAdd another output?", default=False):
            break

    return FeaturesOutputs(
        input_features=input_features,
        output_features=output_features,
        feature_type_distribution=prompt_input("Feature Type Distribution", required=False),
        uncertainty_quantification=prompt_input("Uncertainty Quantification", required=False),
        output_interpretability=prompt_input("Output Interpretability", required=False)
    )


def section_performance() -> PerformanceValidation:
    """Guided input for Section 5: Performance & Validation"""
    print("\n" + "="*60)
    print("SECTION 5: Performance & Validation")
    print("="*60)

    # Validation datasets
    val_datasets = []
    print("\nAdd validation datasets:")

    while True:
        print(f"\n  Dataset {len(val_datasets) + 1}:")
        name = prompt_input("  Dataset Name (e.g., Hospital A - EHR Database)", required=True)
        institution = prompt_input("  Source Institution (e.g., Same hospital, External validation site)", required=True)
        pop = prompt_input("  Population Characteristics (e.g., Urban population, 65% male, mean age 62)", required=True)
        val_type = prompt_choice("  Validation Type", ["internal", "external", "cross_validation"])

        val_datasets.append(ValidationDataset(name, institution, pop, val_type))

        if not prompt_yes_no("\nAdd another validation dataset?", default=False):
            break

    # Metrics
    metrics = []
    print("\nAdd performance metrics:")

    while True:
        print(f"\n  Metric {len(metrics) + 1}:")
        metric_name = prompt_input("  Metric Name (e.g., AUC-ROC, Sensitivity)", required=True)
        value = prompt_float("  Value (typically 0.0-1.0)", required=True, min_val=0.0, max_val=1.0)
        status = prompt_choice("  Validation Status", ["Claimed", "Validated", "External"])
        subgroup = prompt_input("  Subgroup (optional)", required=False)

        metrics.append(PerformanceMetric(metric_name, value, status, subgroup if subgroup else None))

        if not prompt_yes_no("\nAdd another metric?", default=True):
            break

    return PerformanceValidation(
        validation_datasets=val_datasets,
        claimed_metrics=[m for m in metrics if m.validation_status == "Claimed"],
        validated_metrics=[m for m in metrics if m.validation_status != "Claimed"],
        calibration_analysis=prompt_input("Calibration Analysis", required=False),
        fairness_assessment=prompt_input("Fairness Assessment", required=False),
        metric_validation_status=prompt_input("Overall Validation Status", required=False)
    )


def section_methodology() -> Methodology:
    """Guided input for Section 6: Methodology & Explainability"""
    print("\n" + "="*60)
    print("SECTION 6: Methodology & Explainability")
    print("="*60)

    return Methodology(
        model_development_workflow=prompt_input("Development Workflow (e.g., Data extraction → Feature engineering → Model training → Validation)", required=True),
        training_procedure=prompt_input("Training Procedure (e.g., 5-fold cross-validation, hyperparameter tuning with grid search)", required=True),
        data_preprocessing=prompt_input("Data Preprocessing (e.g., Missing value imputation, normalization, outlier removal)", required=True),
        synthetic_data_usage=prompt_input("Synthetic Data Usage (if any)", required=False),
        explainable_ai_method=prompt_input("Explainability Method (if any)", required=False),
        global_vs_local_interpretability=prompt_input("Global vs Local Interpretability", required=False)
    )


def section_additional_info() -> AdditionalInfo:
    """Guided input for Section 7: Additional Information"""
    print("\n" + "="*60)
    print("SECTION 7: Additional Information")
    print("="*60)

    return AdditionalInfo(
        benefit_risk_summary=prompt_input("Benefit-Risk Summary (e.g., Improves early detection with minimal false positives)", required=True),
        ethical_considerations=prompt_input("Ethical Considerations (e.g., Monitored for demographic bias, transparent decision-making)", required=True),
        caveats_limitations=prompt_input("Caveats & Limitations (e.g., Not validated in pediatric populations, limited to specific conditions)", required=True),
        recommendations_for_safe_use=prompt_input("Recommendations for Safe Use (e.g., Use as screening tool, not for diagnosis; require clinical validation)", required=True),
        post_market_surveillance_plan=prompt_input("Post-Market Surveillance Plan", required=False),
        explainability_recommendations=prompt_input("Explainability Recommendations", required=False)
    )


def interactive_create_model_card() -> ModelCard:
    """Interactive workflow to create a model card"""
    print("\n" + "*"*60)
    print("SMART Model Card - Interactive Creation")
    print("*"*60)
    print("\nThis wizard will guide you through creating a model card.")
    print("You can skip optional fields by pressing Enter.\n")

    card = ModelCard()

    # Section 1
    card.set_model_details(section_model_details())

    # Section 2
    card.set_intended_use(section_intended_use())

    # Section 3
    card.set_data_factors(section_data_factors())

    # Section 4
    card.set_features_outputs(section_features_outputs())

    # Section 5
    card.set_performance_validation(section_performance())

    # Section 6
    card.set_methodology(section_methodology())

    # Section 7
    card.set_additional_info(section_additional_info())

    print("\n" + "="*60)
    print("Model Card Creation Complete!")
    print("="*60)

    return card


def run_interactive_wizard():
    """Run the full interactive wizard with export - for use by CLI"""
    card = interactive_create_model_card()

    # Export
    print("\n" + "="*60)
    print("Exporting Model Card")
    print("="*60)

    output_dir = prompt_input("Output directory", default="output")
    output_base = prompt_input("Output filename (without extension)", default="model_card")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    formats = []
    if prompt_yes_no("Export HTML?", default=True):
        formats.append("html")
    if prompt_yes_no("Export JSON?", default=True):
        formats.append("json")

    exported_files = []
    for fmt in formats:
        output_path = os.path.join(output_dir, f"{output_base}.{fmt}")
        if fmt == "html":
            HTMLExporter.export(card, output_path)
        elif fmt == "json":
            JSONExporter.export(card, output_path)

        abs_path = os.path.abspath(output_path)
        exported_files.append((fmt, abs_path))
        print(f"  ✓ Exported {fmt.upper()}: {abs_path}")

    print("\n" + "="*60)
    print("✓ Model Card Creation Complete!")
    print("="*60)

    # Show file locations
    print("\nYour model card has been saved to:")
    for fmt, path in exported_files:
        print(f"  • {fmt.upper()}: {path}")

    # Viewing suggestions
    html_files = [path for fmt, path in exported_files if fmt == "html"]
    if html_files:
        print("\n" + "-"*60)
        print("To view your model card:")
        print("-"*60)
        for html_path in html_files:
            print(f"\n  Open in browser:")
            print(f"    open {html_path}")
            print(f"\n  Or use this command:")
            print(f"    python -m webbrowser {html_path}")

    json_files = [path for fmt, path in exported_files if fmt == "json"]
    if json_files:
        print("\n  View JSON:")
        for json_path in json_files:
            print(f"    cat {json_path}")

    print()
    return exported_files


def main():
    """Main entry point for standalone execution"""
    try:
        run_interactive_wizard()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
