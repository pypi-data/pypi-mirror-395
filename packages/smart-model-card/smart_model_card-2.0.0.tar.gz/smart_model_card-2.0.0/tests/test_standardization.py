"""
Tests for standardization - ensuring consistent structure across model cards
"""

import pytest
from smart_model_card import ModelCard, ModelDetails, IntendedUse
from smart_model_card.sections import DataFactors, SourceDataset
from smart_model_card.exporters import HTMLExporter
import re


def _create_complete_card(name="Test", with_omop=False):
    """Helper to create a card with all required sections"""
    from smart_model_card.sections import FeaturesOutputs, PerformanceValidation, Methodology, AdditionalInfo, InputFeature, OutputFeature, ValidationDataset, PerformanceMetric

    card = ModelCard()
    card.set_model_details(ModelDetails(
        model_name=name,
        version="1.0.0",
        developer_organization="Test",
        release_date="2025-01-01",
        description="Test",
        intended_purpose="decision_support",
        algorithms_used="Test",
        licensing="MIT",
        support_contact="test@example.com"
    ))

    card.set_intended_use(IntendedUse(
        primary_intended_users="Test",
        clinical_indications="Test",
        patient_target_group="Test",
        intended_use_environment="hospital_outpatient"
    ))

    omop_reports = {
        "person": {
            "age_distribution": [{"Age": 65, "Count": 10, "Year of Birth": 1960, "Percentage": "100%"}],
            "gender_distribution": [{"Gender": "MALE", "Count": 10, "Concept ID": 8507, "Percentage": "100%"}]
        }
    } if with_omop else None

    card.set_data_factors(DataFactors(
        source_datasets=[SourceDataset("Test", "Test", 100, "2025", "Test")],
        data_distribution_summary="Test",
        data_representativeness="Test",
        data_governance="Test",
        omop_detailed_reports=omop_reports
    ))

    card.set_features_outputs(FeaturesOutputs(
        input_features=[InputFeature("test", "numeric", True, "Test")],
        output_features=[OutputFeature("test", "probability")],
        feature_type_distribution="Test",
        uncertainty_quantification="Test",
        output_interpretability="Test"
    ))

    card.set_performance_validation(PerformanceValidation(
        validation_datasets=[ValidationDataset("Test", "Test", "Test", "internal")],
        claimed_metrics=[PerformanceMetric("AUC", 0.8, "Claimed")],
        validated_metrics=[PerformanceMetric("AUC", 0.8, "Validated")]
    ))

    card.set_methodology(Methodology(
        model_development_workflow="Test",
        training_procedure="Test",
        data_preprocessing="Test"
    ))

    card.set_additional_info(AdditionalInfo(
        benefit_risk_summary="Test",
        ethical_considerations="Test",
        caveats_limitations="Test",
        recommendations_for_safe_use="Test"
    ))

    return card


def test_detailed_reports_always_present_with_omop_data():
    """Test that Detailed Reports section appears when OMOP data exists"""
    card = _create_complete_card(with_omop=True)
    html = HTMLExporter._generate_html(card.to_dict(), "Test")

    # Check section appears
    assert "📊 Detailed Reports" in html
    assert "Demographics" in html
    assert "Detailed Tables" in html
    assert "Age Distribution" in html
    assert "Gender Distribution" in html


def test_detailed_reports_always_present_without_omop_data():
    """Test that Detailed Reports section appears even without OMOP data (with N/A)"""
    card = _create_complete_card(with_omop=False)
    html = HTMLExporter._generate_html(card.to_dict(), "Test")

    # Check section appears with N/A
    assert "📊 Detailed Reports" in html
    assert "Demographics" in html
    assert "N/A - No visualization data available" in html
    assert "Detailed Tables" in html
    assert "N/A - No age distribution data available" in html
    assert "N/A - No gender distribution data available" in html
    assert "N/A - No race/ethnicity distribution data available" in html


def test_section_structure_consistency():
    """Test that section structure is consistent across different model cards"""
    # Create two different model cards - one without OMOP, one with
    card1 = _create_complete_card(name="Model1", with_omop=False)
    card2 = _create_complete_card(name="Model2", with_omop=True)

    html1 = HTMLExporter._generate_html(card1.to_dict(), "Model1")
    html2 = HTMLExporter._generate_html(card2.to_dict(), "Model2")

    # Extract section headers from both
    section_pattern = r'<h3>(.*?)</h3>'
    headers1 = re.findall(section_pattern, html1)
    headers2 = re.findall(section_pattern, html2)

    # Both should have "Detailed Reports" header
    assert "📊 Detailed Reports" in headers1
    assert "📊 Detailed Reports" in headers2

    # Extract subsection headers
    subsection_pattern = r'<h4[^>]*>(.*?)</h4>'
    subsections1 = re.findall(subsection_pattern, html1)
    subsections2 = re.findall(subsection_pattern, html2)

    # Both should have same subsections
    assert "Demographics" in subsections1
    assert "Demographics" in subsections2
    assert "Detailed Tables" in subsections1
    assert "Detailed Tables" in subsections2


def test_na_styling_consistency():
    """Test that N/A messages have consistent styling"""
    card = _create_complete_card(with_omop=False)
    html = HTMLExporter._generate_html(card.to_dict(), "Test")

    # Check N/A messages have consistent styling
    na_pattern = r'<p style="color:var\(--muted\);font-style:italic">N/A - (.*?)</p>'
    na_messages = re.findall(na_pattern, html)

    # Should have at least 4 N/A messages (Demographics + 3 tables)
    assert len(na_messages) >= 4

    # Verify specific N/A messages exist
    assert any("visualization data available" in msg for msg in na_messages)
    assert any("age distribution data available" in msg for msg in na_messages)
    assert any("gender distribution data available" in msg for msg in na_messages)
    assert any("race/ethnicity distribution data available" in msg for msg in na_messages)
