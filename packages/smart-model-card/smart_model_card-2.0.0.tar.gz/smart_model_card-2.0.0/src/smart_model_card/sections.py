"""
Model Card Section Definitions

Implements the 7 standard sections for medical AI model cards with all fields
from the standardized template.

Author: Ankur Lohachab
Department of Advanced Computing Sciences, Maastricht University
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import math
import re


def _validate_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _validate_date_iso(value: str, field_name: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except Exception as exc:
        raise ValueError(f"{field_name} must be in ISO format YYYY-MM-DD") from exc


def _normalize_enum(
    value: str,
    field_name: str,
    allowed: List[str],
    aliases: Optional[Dict[str, str]] = None
) -> str:
    if value is None:
        raise ValueError(f"{field_name} must be provided")

    aliases = aliases or {}

    def normalize_token(token: str) -> str:
        canonical = re.sub(r"[\s\-]+", "_", token.strip().lower())
        if not canonical:
            raise ValueError(f"{field_name} must not contain empty choices")
        if canonical in allowed:
            return canonical
        if canonical in aliases:
            return aliases[canonical]
        raise ValueError(f"{field_name} must be one of {allowed}")

    tokens = re.split(r"[;,]+", value) if re.search(r"[;,]", value) else [value]
    normalized_tokens = [normalize_token(tok) for tok in tokens if tok.strip()]
    return ", ".join(normalized_tokens)


def _validate_email_or_url(value: str, field_name: str) -> None:
    if value is None:
        raise ValueError(f"{field_name} must be provided")
    if "@" in value or value.startswith("http"):
        return
    raise ValueError(f"{field_name} must be an email or URL")


def _capture(errors: Optional[List[str]], section: str, field: str, func) -> None:
    """
    Run validation function and either raise or append errors.

    If errors list is provided, append formatted message instead of raising.
    """
    try:
        func()
    except ValueError as exc:
        if errors is None:
            raise
        errors.append(f"{section} -> {field}: {exc}")


PHI_KEYWORDS = [
    "patient name",
    "mrn",
    "medical record number",
    "ssn",
    "social security",
    "address",
    "phone",
    "email",
    "date of birth",
    "dob",
    "street",
    "zip",
    "postal",
    "contact",
    "guardian",
    "relative",
    "employer"
]


def _check_phi_leak(value, field_name: str, errors: Optional[List[str]]) -> None:
    """Check for PHI keywords in string or dict values"""
    if isinstance(value, dict):
        # Check all values in the dictionary
        for k, v in value.items():
            if isinstance(v, str):
                _check_phi_leak(v, f"{field_name}.{k}", errors)
        return

    if not isinstance(value, str):
        return

    lower = value.lower()
    for kw in PHI_KEYWORDS:
        if kw in lower:
            _capture(errors, "PHI Guard", field_name, lambda: (_ for _ in ()).throw(ValueError(f"Potential PHI keyword detected: {kw}")))


@dataclass
class Annotation:
    """Free-form notes/comments for interoperability and review."""
    author: str
    note: str
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "author": self.author,
            "note": self.note,
            "created_at": self.created_at
        }


@dataclass
class ModelDetails:
    """Section 1: Model Details"""
    model_name: str
    version: str
    developer_organization: str
    release_date: str
    description: str
    intended_purpose: str
    algorithms_used: str
    licensing: str
    support_contact: str

    gmdn_code: Optional[str] = None
    literature_references: Optional[List[str]] = None
    clinical_study_references: Optional[List[str]] = None
    logo_image: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Model Name": self.model_name,
            "Version": self.version,
            "Developer / Organization": self.developer_organization,
            "Release Date": self.release_date,
            "Description": self.description,
            "Intended Purpose": self.intended_purpose,
            "Algorithm(s) Used": self.algorithms_used,
            "GMDN Code": self.gmdn_code,
            "Licensing": self.licensing,
            "Support Contact": self.support_contact,
            "Literature References": self.literature_references or [],
            "Clinical Study References": self.clinical_study_references or [],
            "Logo / Image (optional)": self.logo_image
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Model Details"
        _capture(errors, section, "Model Name", lambda: _validate_non_empty(self.model_name, "Model Name"))
        _capture(errors, section, "Version", lambda: _validate_non_empty(self.version, "Version"))
        _capture(errors, section, "Developer / Organization", lambda: _validate_non_empty(self.developer_organization, "Developer / Organization"))
        _capture(errors, section, "Release Date", lambda: _validate_date_iso(self.release_date, "Release Date"))
        _capture(errors, section, "Description", lambda: _validate_non_empty(self.description, "Description"))
        allowed_purposes = [
            "diagnosis",
            "screening",
            "triage",
            "monitoring",
            "decision_support",
            "workflow_support",
            "other"
        ]
        purpose_aliases = {
            "clinical_decision_support": "decision_support",
            "cds": "decision_support",
            "workflow": "workflow_support"
        }
        _capture(
            errors,
            section,
            "Intended Purpose",
            lambda: setattr(
                self,
                "intended_purpose",
                _normalize_enum(self.intended_purpose, "Intended Purpose", allowed_purposes, purpose_aliases)
            )
        )
        _capture(errors, section, "Algorithm(s) Used", lambda: _validate_non_empty(self.algorithms_used, "Algorithm(s) Used"))
        _capture(errors, section, "Licensing", lambda: _validate_non_empty(self.licensing, "Licensing"))
        _capture(errors, section, "Support Contact", lambda: _validate_email_or_url(self.support_contact, "Support Contact"))


@dataclass
class IntendedUse:
    """Section 2: Intended Use and Clinical Context"""
    primary_intended_users: str
    clinical_indications: str
    patient_target_group: str
    intended_use_environment: str

    contraindications: Optional[str] = None
    out_of_scope_applications: Optional[str] = None
    warnings: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Primary Intended Users": self.primary_intended_users,
            "Clinical Indications": self.clinical_indications,
            "Patient target group": self.patient_target_group,
            "Contraindications": self.contraindications,
            "Intended Use Environment": self.intended_use_environment,
            "Out of Scope Applications": self.out_of_scope_applications,
            "Warnings": self.warnings
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Intended Use and Clinical Context"
        _capture(errors, section, "Primary Intended Users", lambda: _validate_non_empty(self.primary_intended_users, "Primary Intended Users"))
        _capture(errors, section, "Clinical Indications", lambda: _validate_non_empty(self.clinical_indications, "Clinical Indications"))
        _capture(errors, section, "Patient target group", lambda: _validate_non_empty(self.patient_target_group, "Patient target group"))
        _check_phi_leak(self.primary_intended_users, "Primary Intended Users", errors)
        _check_phi_leak(self.clinical_indications, "Clinical Indications", errors)
        _check_phi_leak(self.patient_target_group, "Patient target group", errors)
        if self.contraindications:
            _check_phi_leak(self.contraindications, "Contraindications", errors)
        if self.out_of_scope_applications:
            _check_phi_leak(self.out_of_scope_applications, "Out of Scope Applications", errors)
        if self.warnings:
            _check_phi_leak(self.warnings, "Warnings", errors)
        env_allowed = [
            "hospital_inpatient",
            "hospital_outpatient",
            "emergency",
            "telemedicine",
            "research",
            "home",
            "other"
        ]
        env_aliases = {
            "inpatient": "hospital_inpatient",
            "outpatient": "hospital_outpatient",
            "outpatient_clinic": "hospital_outpatient",
            "outpatient_clinics": "hospital_outpatient",
            "hospital_departments": "hospital_inpatient",
            "ed": "emergency",
            "telehealth": "telemedicine",
            "home_care": "home",
            "primary_care": "hospital_outpatient"
        }
        _capture(
            errors,
            section,
            "Intended Use Environment",
            lambda: setattr(
                self,
                "intended_use_environment",
                _normalize_enum(self.intended_use_environment, "Intended Use Environment", env_allowed, env_aliases)
            )
        )


@dataclass
class ConceptSet:
    """OMOP/SNOMED/LOINC concept set definition"""
    name: str
    vocabulary: str
    concept_ids: List[int]
    description: Optional[str] = None


@dataclass
class CohortCriteria:
    """Primary cohort inclusion/exclusion criteria"""
    inclusion_rules: List[str]
    exclusion_rules: List[str]
    observation_window: Optional[str] = None


@dataclass
class SourceDataset:
    """Source dataset metadata"""
    name: str
    origin: str
    size: int
    collection_period: str
    population_characteristics: str
    demographics: Optional[Dict[str, str]] = None  # Detailed demographics (age, gender, race, etc.)


@dataclass
class DataFactors:
    """Section 3: Data & Factors"""
    source_datasets: List[SourceDataset]
    data_distribution_summary: Union[str, Dict[str, str]]  # Can be string or dict for structured data
    data_representativeness: str
    data_governance: str
    deid_method: Optional[str] = None
    date_handling: Optional[str] = None
    cell_suppression: Optional[str] = None
    deid_report_uri: Optional[str] = None
    deid_report_hash: Optional[str] = None

    concept_sets: Optional[List[ConceptSet]] = None
    primary_cohort_criteria: Optional[CohortCriteria] = None
    omop_detailed_reports: Optional[Dict[str, Any]] = None  # Detailed OMOP reports for interactive display

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Concept Sets": [
                {
                    "name": cs.name,
                    "vocabulary": cs.vocabulary,
                    "concept_ids": cs.concept_ids,
                    "description": cs.description
                } for cs in (self.concept_sets or [])
            ],
            "Primary Cohort Criteria": {
                "inclusion_rules": self.primary_cohort_criteria.inclusion_rules if self.primary_cohort_criteria else [],
                "exclusion_rules": self.primary_cohort_criteria.exclusion_rules if self.primary_cohort_criteria else [],
                "observation_window": self.primary_cohort_criteria.observation_window if self.primary_cohort_criteria else None
            } if self.primary_cohort_criteria else None,
            "Source Datasets": [
                {
                    "name": ds.name,
                    "origin": ds.origin,
                    "size": ds.size,
                    "collection_period": ds.collection_period,
                    "population_characteristics": ds.population_characteristics,
                    "demographics": ds.demographics if ds.demographics else None
                } for ds in self.source_datasets
            ],
            "Data Distribution Summary": self.data_distribution_summary,
            "Data Representativeness": self.data_representativeness,
            "Data Governance": self.data_governance,
            "De-identification Method": self.deid_method,
            "Date Handling": self.date_handling,
            "Cell-size Suppression": self.cell_suppression,
            "De-id Report URI": self.deid_report_uri,
            "De-id Report Hash": self.deid_report_hash,
            "OMOP Detailed Reports": self.omop_detailed_reports  # For interactive display
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Data & Factors"
        _capture(
            errors,
            section,
            "Source Datasets",
            lambda: None if self.source_datasets else _validate_non_empty("", "Source Datasets")
        )
        for ds in self.source_datasets or []:
            _capture(
                errors,
                section,
                "Source Dataset size",
                lambda: None if (ds.size is not None and ds.size >= 0) else _validate_non_empty("", "Source Dataset size >= 0")
            )
        # Validate data_distribution_summary (can be str or dict)
        if isinstance(self.data_distribution_summary, dict):
            _capture(errors, section, "Data Distribution Summary", lambda: None if self.data_distribution_summary else _validate_non_empty("", "Data Distribution Summary"))
        else:
            _capture(errors, section, "Data Distribution Summary", lambda: _validate_non_empty(self.data_distribution_summary, "Data Distribution Summary"))

        _capture(errors, section, "Data Representativeness", lambda: _validate_non_empty(self.data_representativeness, "Data Representativeness"))
        _capture(errors, section, "Data Governance", lambda: _validate_non_empty(self.data_governance, "Data Governance"))

        if self.data_distribution_summary:
            _check_phi_leak(self.data_distribution_summary, "Data Distribution Summary", errors)
        if self.data_governance:
            _check_phi_leak(self.data_governance, "Data Governance", errors)
        if self.deid_method:
            _check_phi_leak(self.deid_method, "De-identification Method", errors)


@dataclass
class InputFeature:
    """Model input feature specification"""
    name: str
    data_type: str
    required: bool
    clinical_domain: str
    value_range: Optional[str] = None
    units: Optional[str] = None


@dataclass
class OutputFeature:
    """Model output specification"""
    name: str
    type: str
    units: Optional[str] = None
    value_range: Optional[str] = None
    classes: Optional[List[str]] = None


@dataclass
class FeaturesOutputs:
    """Section 4: Features & Outputs"""
    input_features: List[InputFeature]
    output_features: List[OutputFeature]
    feature_type_distribution: str
    uncertainty_quantification: str
    output_interpretability: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Input Features": [
                {
                    "name": f.name,
                    "data_type": f.data_type,
                    "required": f.required,
                    "clinical_domain": f.clinical_domain,
                    "value_range": f.value_range,
                    "units": f.units
                } for f in self.input_features
            ],
            "Output Features": [
                {
                    "name": f.name,
                    "type": f.type,
                    "units": f.units,
                    "value_range": f.value_range,
                    "classes": f.classes
                } for f in self.output_features
            ],
            "Feature Type Distribution": self.feature_type_distribution,
            "Uncertainty Quantification": self.uncertainty_quantification,
            "Output Interpretability": self.output_interpretability
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Features & Outputs"
        _capture(
            errors,
            section,
            "Input Features",
            lambda: None if self.input_features else _validate_non_empty("", "Input Features")
        )
        allowed_input_types = ["numeric", "categorical", "text", "image", "signal", "other"]
        input_aliases = {"numerical": "numeric"}
        for f in self.input_features or []:
            _capture(errors, section, "Input Feature name", lambda: _validate_non_empty(f.name, "Input Feature name"))
            _capture(
                errors,
                section,
                "Input Feature data_type",
                lambda: setattr(
                    f,
                    "data_type",
                    _normalize_enum(f.data_type, "Input Feature data_type", allowed_input_types, input_aliases)
                )
            )
        _capture(
            errors,
            section,
            "Output Features",
            lambda: None if self.output_features else _validate_non_empty("", "Output Features")
        )
        allowed_output_types = ["classification", "regression", "probability", "score", "segmentation", "text", "other"]
        output_aliases = {"class": "classification"}
        for f in self.output_features or []:
            _capture(errors, section, "Output Feature name", lambda: _validate_non_empty(f.name, "Output Feature name"))
            _capture(
                errors,
                section,
                "Output Feature type",
                lambda: setattr(
                    f,
                    "type",
                    _normalize_enum(f.type, "Output Feature type", allowed_output_types, output_aliases)
                )
            )
        _capture(errors, section, "Feature Type Distribution", lambda: _validate_non_empty(self.feature_type_distribution, "Feature Type Distribution"))
        _capture(errors, section, "Uncertainty Quantification", lambda: _validate_non_empty(self.uncertainty_quantification, "Uncertainty Quantification"))
        _capture(errors, section, "Output Interpretability", lambda: _validate_non_empty(self.output_interpretability, "Output Interpretability"))


@dataclass
class ValidationDataset:
    """Validation dataset specification"""
    name: str
    source_institution: str
    population_characteristics: str
    validation_type: str


@dataclass
class PerformanceMetric:
    """Performance metric with validation status"""
    metric_name: str
    value: float
    validation_status: str
    subgroup: Optional[str] = None


@dataclass
class PerformanceValidation:
    """Section 5: Performance & Validation"""
    validation_datasets: List[ValidationDataset]
    claimed_metrics: List[PerformanceMetric]
    validated_metrics: List[PerformanceMetric]

    calibration_analysis: Optional[str] = None
    fairness_assessment: Optional[str] = None
    metric_validation_status: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Validation Dataset(s)": [
                {
                    "name": vd.name,
                    "source_institution": vd.source_institution,
                    "population_characteristics": vd.population_characteristics,
                    "validation_type": vd.validation_type
                } for vd in self.validation_datasets
            ],
            "Claimed Metrics": [
                {
                    "metric_name": m.metric_name,
                    "value": m.value,
                    "validation_status": m.validation_status,
                    "subgroup": m.subgroup
                } for m in self.claimed_metrics
            ],
            "Validated Metrics": [
                {
                    "metric_name": m.metric_name,
                    "value": m.value,
                    "validation_status": m.validation_status,
                    "subgroup": m.subgroup
                } for m in self.validated_metrics
            ],
            "Calibration Analysis": self.calibration_analysis,
            "Fairness Assessment": self.fairness_assessment,
            "Metric Validation Status": self.metric_validation_status
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Performance & Validation"
        _capture(
            errors,
            section,
            "Validation Dataset(s)",
            lambda: None if self.validation_datasets else _validate_non_empty("", "Validation Dataset(s)")
        )
        allowed_statuses = ["claimed", "internal", "external", "validated"]

        def _validate_metric_status(status: str, field_name: str) -> None:
            if status is None:
                raise ValueError(f"{field_name} validation_status must be provided")
            normalized = status.lower()
            if not any(normalized.startswith(s) for s in allowed_statuses):
                raise ValueError(f"{field_name} validation_status must start with one of {allowed_statuses}")

        prob_metric_tokens = [
            "auc",
            "roc",
            "pr",
            "precision",
            "recall",
            "specificity",
            "sensitivity",
            "f1",
            "dice",
            "iou",
            "brier",
            "accuracy"
        ]

        def _validate_metric_value(metric: PerformanceMetric) -> None:
            if metric.value is None or not math.isfinite(metric.value):
                raise ValueError("PerformanceMetric value must be a finite number")
            name_norm = (metric.metric_name or "").lower()
            if any(tok in name_norm for tok in prob_metric_tokens):
                if metric.value < 0.0 or metric.value > 1.0:
                    raise ValueError(f"PerformanceMetric '{metric.metric_name}' must be within [0, 1]")

        for m in self.claimed_metrics + self.validated_metrics:
            _capture(errors, section, "PerformanceMetric validation_status", lambda: _validate_metric_status(m.validation_status, "PerformanceMetric"))
            _capture(errors, section, f"PerformanceMetric {m.metric_name} value", lambda: _validate_metric_value(m))
        _capture(errors, section, "Metric Validation Status", lambda: _validate_non_empty(self.metric_validation_status or "Validated", "Metric Validation Status"))


@dataclass
class Methodology:
    """Section 6: Methodology & Explainability"""
    model_development_workflow: str
    training_procedure: str
    data_preprocessing: str

    synthetic_data_usage: Optional[str] = None
    explainable_ai_method: Optional[str] = None
    global_vs_local_interpretability: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Model Development Workflow": self.model_development_workflow,
            "Training Procedure": self.training_procedure,
            "Data Preprocessing": self.data_preprocessing,
            "Synthetic Data Usage": self.synthetic_data_usage,
            "Explainable AI Method": self.explainable_ai_method,
            "Global vs. Local Interpretability": self.global_vs_local_interpretability
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Methodology & Explainability"
        _capture(errors, section, "Model Development Workflow", lambda: _validate_non_empty(self.model_development_workflow, "Model Development Workflow"))
        _capture(errors, section, "Training Procedure", lambda: _validate_non_empty(self.training_procedure, "Training Procedure"))
        _capture(errors, section, "Data Preprocessing", lambda: _validate_non_empty(self.data_preprocessing, "Data Preprocessing"))


@dataclass
class AdditionalInfo:
    """Section 7: Additional Information"""
    benefit_risk_summary: str
    ethical_considerations: str
    caveats_limitations: str
    recommendations_for_safe_use: str

    post_market_surveillance_plan: Optional[str] = None
    explainability_recommendations: Optional[str] = None
    supporting_documents: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Benefit–Risk Summary": self.benefit_risk_summary,
            "Post-Market Surveillance Plan": self.post_market_surveillance_plan,
            "Ethical Considerations": self.ethical_considerations,
            "Caveats & Limitations": self.caveats_limitations,
            "Recommendations for Safe Use": self.recommendations_for_safe_use,
            "Explainability Recommendations": self.explainability_recommendations,
            "Supporting Documents": self.supporting_documents or []
        }

    def validate(self, errors: Optional[List[str]] = None) -> None:
        section = "Additional Information"
        _capture(errors, section, "Benefit–Risk Summary", lambda: _validate_non_empty(self.benefit_risk_summary, "Benefit–Risk Summary"))
        _capture(errors, section, "Ethical Considerations", lambda: _validate_non_empty(self.ethical_considerations, "Ethical Considerations"))
        _capture(errors, section, "Caveats & Limitations", lambda: _validate_non_empty(self.caveats_limitations, "Caveats & Limitations"))
        _capture(errors, section, "Recommendations for Safe Use", lambda: _validate_non_empty(self.recommendations_for_safe_use, "Recommendations for Safe Use"))
        _check_phi_leak(self.benefit_risk_summary, "Benefit–Risk Summary", errors)
        _check_phi_leak(self.ethical_considerations, "Ethical Considerations", errors)
        _check_phi_leak(self.caveats_limitations, "Caveats & Limitations", errors)
        _check_phi_leak(self.recommendations_for_safe_use, "Recommendations for Safe Use", errors)
