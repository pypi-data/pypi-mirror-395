from enum import Enum
from typing import Dict, List

from pydantic import Field

from human_cupid.utils.model import Model
from human_cupid.utils.schemas import ConfidenceLevel


class CompatibilityLevel(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    CHALLENGING = "challenging"
    INCOMPATIBLE = "incompatible"

class CompatibilityFactor(Model):    
    factor_name: str
    compatibility_level: CompatibilityLevel
    percentage_score: int
    why_this_score: str = Field(description="Clear explanation of why they got this compatibility score")
    practical_implications: str = Field(description="What this means for their day-to-day relationship")
    specific_evidence: str = Field(description="Concrete examples from their personalities that support this assessment")
    strengths_in_this_area: List[str]
    challenges_in_this_area: List[str]

class RelationshipScenario(Model):    
    scenario_type: str = Field(description="best_case, typical_day, conflict_situation, etc.")
    detailed_narrative: str = Field(description="Rich, specific story of how this scenario would play out based on their personalities")
    key_dynamics_at_play: List[str] = Field(description="Which personality patterns drive this scenario")

class Compatibility(Model):
    id: str = Field("ID_PLACEHOLDER")
    relationship_type: str = Field(description="friendship, work_partnership, family, etc.")
    overall_compatibility_story: str = Field(description="Comprehensive narrative explaining their relationship potential, dynamics, and trajectory")
    overall_score: CompatibilityLevel = Field(description="Overall compatibility rating")
    values_alignment: CompatibilityFactor
    personality_chemistry: CompatibilityFactor
    communication_compatibility: CompatibilityFactor
    lifestyle_fit: CompatibilityFactor 
    emotional_compatibility: CompatibilityFactor
    growth_compatibility: CompatibilityFactor
    shared_interests: CompatibilityFactor
    relationship_scenarios: List[RelationshipScenario]
    success_roadmap: str = Field(description="Specific, actionable plan for making this relationship work, with concrete steps and timeline")
    critical_conversations: List[str] = Field(description="Essential topics they must discuss and when to have these conversations")
    warning_signs_to_monitor: List[str] = Field(description="Specific red flags or concerning patterns to watch for")   
    relationship_enhancers: List[str] = Field(description="Specific activities, behaviors, or practices that would strengthen their bond")
    alternative_relationship_types: Dict[str, str] = Field(description="How they'd work as friends, colleagues, etc.")
    analysis_confidence: ConfidenceLevel
    unique_insights: str = Field(description="Surprising or counterintuitive insights about this specific pairing")
    data_limitations: List[str] = Field(description="What information is missing that would improve this analysis")

class RelationshipType(str, Enum):
    FRIENDSHIP = "friendship"
    WORK_PARTNERSHIP = "work_partnership"
    MENTOR_MENTEE = "mentor_mentee"
    CASUAL_ACQUAINTANCE = "casual_acquaintance"
    NOT_RECOMMENDED = "not_recommended"

class CompatibilityStructured(Model):
    score_compatibility: int = Field(
        description="Overall compatibility score from 0-100",
        ge=0,
        le=100
    )
    shared_interests: List[str] = Field(
        description="List of 3-5 shared interests, hobbies, or activities they both enjoy. No personal names or identifiers.",
        min_length=3,
        max_length=5
    )
    conversation_topics: List[str] = Field(
        description="List of 5-7 topics they could naturally talk about together. No personal names or identifiers.",
        min_length=5,
        max_length=7
    )
    recommendation_summary: str = Field(
        description="Brief 2-3 sentence paragraph explaining why this relationship is or isn't recommended. Anonymous, no names."
    )
    relationship_type: RelationshipType = Field(
        description="Type of relationship this would work best as"
    )

class CompatibilityAnalysis(Model):
    structured: CompatibilityStructured
    analysis: str