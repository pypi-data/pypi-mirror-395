"""
Auto-generated Pydantic models for BlackBox Schemas
Compatible with Pydantic v2.x
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from enum import Enum
import re


# Models from package/schema.py
from datetime import datetime, date
class CategoryEvaluation(BaseModel):
    category: str  = Field(description="The category name being evaluated")
    pros_cons: dict[str, list[str]]  = Field(
        description="Dictionary containing 'Pros' and 'Cons' keys, each with a list of points. Example: {'Pros':['pro1', 'pro 2', .... ], 'Cons':['Con 1', 'Con 2', ....]},",
        example={
            "Pros": ["pro1", "pro2", "pro3", "pro4"],
            "Cons": ["con1", "con2", "con3", "con4"],
        },
    )
    feasibility: str  = Field(description="Yes/No/moderate assessment of feasibility")
    observations: List[str]  = Field(
        description="List of observations for this category"
    )
    recommendations: List[str]  = Field(
        description="List of recommendations for this category"
    )



class Recommendation(BaseModel):
    decision: str  = Field(description="Go/No-Go decision/Moderate")
    summary: str  = Field(description="Summary of key factors influencing the decision")
    next_steps: List[str]  = Field(description="List of suggested next steps")



class SubmissionDetails(BaseModel):
    due_date: str  = Field(
        description="Exact submission deadline from RFP in YYYY-MM-DD format. Look for phrases like 'proposals due', 'submission deadline', 'closing date', or 'must be received by'."
    )
    submission_type: str  = Field(
        description="Type of submission method: 'online' (email, web portal, digital upload) or 'offline' (physical delivery, mail, in-person)"
    )
    submission_details: str  = Field(
        description="Specific submission location and method: email address, web portal URL, physical mailing address, or office location where proposals must be submitted"
    )
    submission_instructions: str  = Field(
        description="Detailed instructions for proposal preparation and submission: required format (PDF, hard copy), number of copies, file size limits, naming conventions, required sections, and any special submission requirements"
    )



class RFPEvaluation(BaseModel):
    evaluation: List[CategoryEvaluation]  = Field(
        description="List of category evaluations"
    )
    recommendation: Recommendation  = Field(description="Final recommendation")
    timeline_and_submission_details: SubmissionDetails  = Field(
        description="Timeline and submission details",
        alias="timeline_and_submission_details",
    )

    model_config = ConfigDict()


class LegalAdministrativeRequirements(BaseModel):
    insurance_requirements: Optional[str]
    company_info_requirements: Optional[str]
    certification_requirements: Optional[str]
    subcontracting_requirements: Optional[str]
    required_forms_and_attachments: Optional[str]
    other_admin_requirements: Optional[str]



class TechnicalOperationalRequirements(BaseModel):
    client_background: Optional[str]
    project_purpose_objectives: Optional[str]
    qualification_requirements: Optional[str]
    scope_of_work: Optional[str]
    deliverables: Optional[str]
    timeline_and_milestones: Optional[str]
    proposal_format: Optional[str]
    evaluation_criteria: Optional[str]
    budget_guidelines: Optional[str]
    location_requirements: Optional[str]
    technical_specifications: Optional[str]



class GuidanceAndClarifications(BaseModel):
    ambiguous_requirements: Optional[List[str]]  = Field(default_factory=list)
    implicit_requirements: Optional[List[str]]  = Field(default_factory=list)
    clarification_needed: Optional[List[str]]  = Field(default_factory=list)



class PageReferences(BaseModel):
    section_to_page: Optional[Dict[str, str]]  = Field(
        default_factory=dict, description="e.g., {'Scope of Work': 'Pg 6–8'}"
    )



class RFPAnalysisOutput(BaseModel):
    legal_admin_requirements: LegalAdministrativeRequirements
    technical_requirements: TechnicalOperationalRequirements
    guidance_notes: GuidanceAndClarifications
    page_references: Optional[PageReferences] = None
    rfp_metadata: Optional[Dict[str, str]]  = Field(
        default_factory=dict,
        description="Optional metadata like client name, issue date",
    )



class UserPreferencesSection(BaseModel):
    question: str  = Field(
        ..., description="The question to be answered by the content generator"
    )
    suggested_answer: str  = Field(
        ..., description="The suggested answer to the question"
    )



class UserPreferences(BaseModel):
    user_preferences: List[UserPreferencesSection]  = Field(...)



class TOCSubSection(BaseModel):
    subSectionNumber: str  = Field(..., description="The subsection number (e.g. '2.1')")
    subSectionTitle: str  = Field(..., description="The subsection title")



class TOCSection(BaseModel):
    sectionNumber: str  = Field(..., description="Section number (e.g. '2')")
    sectionTitle: str  = Field(..., description="Section title")
    subSections: List[TOCSubSection]  = Field(default_factory=list)
    specificInstruction: str  = Field(
        default="", description="Key instructions for what this section must cover"
    )
    generationStrategy: str  = Field(
        "all-at-once",
        description="The content generation method. Can be 'iterative' (subsection-by-subsection) or 'all-at-once' (entire section at once).",
    )



class TableOfContents(BaseModel):
    outline_json: List[TOCSection]  = Field(...)
    exec_summary_section_number: Optional[int]  = Field(
        ..., description="Section number for the executive summary"
    )



class RfpSection(BaseModel):
    heading: str  = Field(..., description="Most relevant name for this section")
    content: str  = Field(..., description="Actual content of the section")



class RfpSummary(BaseModel):
    rfp_sections: List[RfpSection]  = Field(
        ..., description="List of sections in the RFP"
    )



class RfpCompanyDataSection(BaseModel):
    heading: str  = Field(description="Most relevant name for this section")
    content: str  = Field(description="Actual content of the section")



class RfpCompanyData(BaseModel):
    rfp_sections: List[RfpCompanyDataSection]  = Field(
        description="List of sections in the RFP"
    )
    summary: str  = Field(description="Overall summary of the RFP document")



class PromptSubSection(BaseModel):
    """Subsection within a proposal section."""

    subSectionNumber: str  = Field(
        ..., description="The subsection number (e.g., '2.1')"
    )
    subSectionTitle: str  = Field(..., description="The title of the subsection")



class PromptSection(BaseModel):
    """Section within a proposal table of contents."""

    sectionNumber: str  = Field(..., description="The section number (e.g., '2')")
    sectionTitle: str  = Field(..., description="The title of the section")
    subSections: List[PromptSubSection]  = Field(
        default_factory=list, description="List of subsections within this section"
    )
    agentSpecialisation: str  = Field(
        ..., description="The type of agent specialized for this section"
    )
    specificInstruction: str  = Field(
        default="",
        description="Any particular instructions or guidelines relevant to this section",
    )
    relevant_sections: List[str]  = Field(
        default_factory=list, description="List of relevant sections for this section"
    )
    relevant_deep_research_sections: List[str]  = Field(
        default_factory=list,
        description="List of relevant deep research sections for this section",
    )
    prompt: str  = Field(..., description="This stores the prompt for this section")



class ContentGenerationSubsection(BaseModel):
    """Content for a subsection within a proposal section."""

    subsectionName: str  = Field(..., description="The name of the subsection")
    content: str  = Field(..., description="The content for this subsection")



class ContentGenerationSection(BaseModel):
    """Content for a section within a proposal document."""

    sectionName: str  = Field(..., description="The name of the section")
    content: str  = Field(..., description="The main content for this section")
    subsections: List[ContentGenerationSubsection]  = Field(
        default_factory=list,
        description="List of subsections within this section",
    )



class CostFormatingSections(BaseModel):
    sections: List[ContentGenerationSection]  = Field(
        ..., description="Contain all Sections"
    )



class CostItem(BaseModel):
    """A structured model for individual cost entries."""

    description: str  = Field(
        ..., description="Description of the cost, e.g., 'Annual AWS Subscription'."
    )
    amount: float  = Field(..., gt=0, description="The monetary value of the cost.")
    currency: str  = Field(
        default="USD", max_length=3, description="3-letter currency code, e.g., 'USD'."
    )



class ResourceGap(BaseModel):
    """A reusable model to define the gap between existing and required resources."""

    existing: List[str]  = Field(
        default_factory=list,
        description="A list of resources the client currently has.",
    )
    required: List[str]  = Field(
        ..., description="A list of resources the client needs."
    )



class HumanResourceSection(BaseModel):
    """Details related to human resources, including staffing gaps and associated costs."""

    staff: ResourceGap  = Field(
        ..., description="The gap between existing and required personnel."
    )
    costs: List[CostItem]  = Field(
        ..., description="A breakdown of costs related to hiring, salaries, etc."
    )



class LicenseSection(BaseModel):
    """Details related to software/legal licenses, including gaps and associated costs."""

    details: ResourceGap  = Field(
        ..., description="The gap between existing and required licenses."
    )
    costs: List[CostItem]  = Field(
        ..., description="A breakdown of licensing fees and related costs."
    )



class InfrastructureSection(BaseModel):
    """Details related to infrastructure, including asset gaps and associated costs."""

    assets: ResourceGap  = Field(
        ..., description="The gap between existing and required infrastructure assets."
    )
    costs: List[CostItem]  = Field(
        ..., description="A breakdown of hardware, cloud services, and other costs."
    )



class ProjectRequirements(BaseModel):
    """A container that groups all detailed requirement sections for a single project."""

    human_resources: HumanResourceSection
    licenses: LicenseSection
    infrastructure: InfrastructureSection



class RfpCostSummary(BaseModel):
    """The top-level model for a cost summary from a Request for Proposal (RFP)."""

    # Fields are more specific and better named
    location_name: str  = Field(
        ..., description="The official name of the city, town, or county."
    )
    state: str  = Field(..., description="The state or province name.")
    # This field is now a single object, which is more logical than a list
    requirements: ProjectRequirements  = Field(
        ..., description="Contains all requirement sections for the project."
    )
    cost_table_template: Optional[str]  = Field(
        None,
        description="The mandatory cost submission table format, extracted exactly as a Markdown string. This should be null if no specific template is provided in the RFP.",
    )



class License(BaseModel):
    license_name: str  = Field(description="License name present in rfp proposal")
    license_per_unit_cost: int  = Field(
        description="Actual per unit price or estimated price"
    )
    license_duration: str  = Field(description="annual or monthly duration of license")
    # license_description: str  = Field(description="Description of the license")
    license_quantity: int  = Field(description="number of licenses required")
    license_scope: str  = Field(description="scope of license")
    license_minimum_purchase_requirements: str  = Field(
        description="minimum purchase requirements"
    )
    license_source_reference: str  = Field(
        description="source reference of license in url formate"
    )
    license_discount: str  = Field(
        description="discount if any related to partner or vendor"
    )



class LicenseSubsection(BaseModel):
    mandatory: List[License]  = Field(
        ..., description="List of mandatory licenses and cost strategies"
    )
    additional: List[License]  = Field(
        ..., description="List of additional licenses and cost strategies"
    )



class LicenseList(BaseModel):
    licenses: LicenseSubsection  = Field(
        ..., description="List of licenses found in the RFP proposal"
    )



class CostSubSection(BaseModel):
    job_title: str  = Field(..., description="job title according to rfp proposal")
    hours: int  = Field(..., description="exact number of hours according to job title")
    description: str  = Field(..., description="The subsection content")



class JobTitle(BaseModel):
    old_job_title: str  = Field(..., description="Job title inside proposal")
    new_job_title: str  = Field(
        ..., description="exact number of hours according to job title"
    )
    Experience_level: str  = Field(..., description="Experience level")
    hours: int  = Field(..., description="exact number of hours according to job title")
    gpt_hourly_wage: int  = Field(..., description="Hourly rate")
    GSA_Rates: int  = Field(..., description="GSA Rates")
    remote: bool  = Field(..., description="Is the job remote?")
    on_site: bool  = Field(..., description="Is the job on-site?")
    description: str  = Field(..., description="The subsection content")



class JobTitleSubsection(BaseModel):
    mandatory: List[JobTitle]  = Field(..., description="Mandatory cost strategies")
    additional: List[JobTitle]  = Field(..., description="Additional cost strategies")



class CostSection(BaseModel):
    state: str  = Field(description="Exact state name")
    county_town_name: str  = Field(
        description="exact official name which match official U.S. Census Bureau or FIPS geographic entities"
    )
    job_title: JobTitleSubsection  = Field(description="Job titles and cost strategies")

    number_of_personnel: int  = Field(description="exact county of number of personnel")
    personnel_source_reference: str  = Field(
        description="source reference of personnel in url formate"
    )
    total_cost: str  = Field(
        description="total cost value with source reference (e.g., '$100,000 from RFP_SUMMARY' or '$150,000 from RFP_PROPOSAL' or 'No cost given in RFP')"
    )
    job_title_total_hours: int  = Field(description="only number")
    job_title_hours: List[CostSubSection]  = Field(
        description="job title hours explained in prompt"
    )
    cost_proposal: str  = Field(
        description="cost proposal in the format specified by the RFP else phase-wise cost estimation according to job title from Total hours, if it contain tables show them"
    )
    location_type: str  = Field(description="Location type")
    cost_field_name: List[str]  = Field(
        description="List of section names which contain cost"
    )



class InfrastructureItem(BaseModel):
    component: str  = Field(
        ..., description="Name of the infrastructure component or service"
    )
    requirement: str  = Field(
        ..., description="The explicit or inferred requirement from RFP"
    )
    fulfillment_strategy: str  = Field(
        ..., description="Best-practice strategy for meeting the requirement"
    )
    estimated_monthly_cost: float  = Field(
        ..., description="Estimated cost in USD per month"
    )
    estimated_annual_cost: float  = Field(
        ..., description="Estimated annual cost in USD"
    )
    notes: Optional[str]  = Field("", description="Assumptions or considerations")



class InfrastructureSubSection(BaseModel):
    mandatory: List[InfrastructureItem]  = Field(
        ...,
        description="List of mandatory infrastructure components and cost strategies",
    )
    additional: List[InfrastructureItem]  = Field(
        ...,
        description="List of additional infrastructure components and cost strategies",
    )



class InfrastructureSummary(BaseModel):
    items: InfrastructureSubSection  = Field(
        ..., description="List of infrastructure components and cost strategies"
    )
    total_monthly_cost: float  = Field(
        ..., description="Total estimated monthly cost for infrastructure"
    )
    total_annual_cost: float  = Field(
        ..., description="Total estimated annual cost for infrastructure"
    )
    additional_notes: Optional[str]  = Field(
        None, description="Optional compliance or pricing notes"
    )



class CostImageCalculationResult(BaseModel):
    table_result: str  = Field(
        ..., description="Generated cost table or explanation result"
    )



class HourlyJobTitleWages(BaseModel):
    old_job_title: str  = Field(description="The job title from the source")
    Experience_level: str  = Field(description="Experience level (e.g., level1, level2)")
    hours: float  = Field(description="List of hours for each job title")
    hourly_wage: Optional[float]  = Field(description="List of hourly wages")
    gpt_hourly_wage: Optional[float]  = Field(
        description="Hourly rate recommended by GPT"
    )
    GSA_Rates: Optional[float]  = Field(description="GSA Rates")
    description: str  = Field(
        description="How you exactly calculated the number of hours for each job title"
    )

    # Added these fields so the LLM knows to generate them for the backend logic
    remote: bool  = Field(default=False, description="Set to true if the role is remote")
    on_site: bool  = Field(
        default=False, description="Set to true if the role is on-site"
    )



class HourlySection(BaseModel):
    """
    Defines the root structure for the hourly wages section.
    Split into mandatory and additional to match the backend requirement.
    """

    mandatory: List[HourlyJobTitleWages]  = Field(
        description="List of core/mandatory hourly job title wages"
    )
    additional: List[HourlyJobTitleWages]  = Field(
        default_factory=list,
        description="List of optional or additional hourly job title wages",
    )



class QuestionItem(BaseModel):
    question: str  = Field(..., description="A research question")



class DeepResearchQueryResponse(BaseModel):
    agency_name: str
    research_categories: Dict[str, Dict[str, List[QuestionItem]]]



class RfpDates(BaseModel):
    due_date: Optional[date]  = Field(
        None, description="The final submission due date for the RFP."
    )
    pre_proposal_meeting_date: Optional[date]  = Field(
        None, description="The date for any pre-proposal or pre-bid meetings."
    )
    question_submission_date: Optional[date]  = Field(
        None, description="The deadline for submitting questions about the RFP."
    )
    description: Optional[str]  = Field(
        None,
        description="A brief summary or description of the RFP's core requirements.",
    )



class RetrievalItem(BaseModel):
    query: str  = Field(
        description="A specific, targeted question to retrieve information."
    )
    doc_type_filter: str  = Field(description="The type of document to search within.")



class AdvancedRetrievalPlan(BaseModel):
    retrieval_items: List[RetrievalItem]  = Field(
        description="A list of retrieval items."
    )



class LongTermMemoryItem(BaseModel):
    section_title: str
    key_themes: List[str]
    decisions_made: List[str]
    entities_introduced: Dict[str, str]



class RegenerationDecision(BaseModel):
    decision: str  = Field(
        description="The final decision, must be exactly 'refinement' or 'full_rerun'."
    )
    reasoning: str  = Field(description="A brief explanation for the decision.")
    confidence: float  = Field(
        description="Confidence level (0.0-1.0) in this decision", default=0.8
    )



class RerunTargets(BaseModel):
    targets: List[str]  = Field(
        description="A list of subsection titles that must be fully re-run to address the user's request."
    )
    reasoning: str  = Field(
        description="Explanation of why these specific subsections were selected."
    )


