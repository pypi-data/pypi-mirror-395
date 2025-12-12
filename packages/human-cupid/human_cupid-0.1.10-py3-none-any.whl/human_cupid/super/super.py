from typing import List, Tuple

from human_cupid.llm import LLM, ErrorResponse, Embed


class SuperprofileAnalyzer:
    def __init__(self, target: str, subprofiles: List[str]):
        self.target = target
        self.subprofiles = subprofiles

    def prompt(self):
        subprofile_summaries = []

        for i, subprofile_text in enumerate(self.subprofiles):
            context_summary = f"""
═══════════════════════════════════════════════════════
SUBPROFILE {i + 1}:
═══════════════════════════════════════════════════════

{subprofile_text}
"""
            subprofile_summaries.append(context_summary)
        
        all_summaries = "\n".join(subprofile_summaries)

        base_prompt = f"""You are an expert psychologist specializing in personality synthesis, cross-contextual behavioral analysis, and holistic human understanding.

Your task is to synthesize multiple context-specific personality profiles for {self.target} into a unified, comprehensive understanding of who they are as a complete person.

═══════════════════════════════════════════════════════
SUBPROFILE DATA FROM MULTIPLE CONTEXTS:
═══════════════════════════════════════════════════════

{all_summaries}

═══════════════════════════════════════════════════════
SYNTHESIS INSTRUCTIONS:
═══════════════════════════════════════════════════════

Create a holistic personality profile with the following structure:

CONTEXTS ANALYZED
List all relationship contexts that contributed to this profile (family, friends, work, romantic, social media, etc.)

THE AUTHENTIC SELF: CORE PERSONALITY SYNTHESIS

Who is {self.target} when you strip away context-specific adaptations? Describe their fundamental personality—the essence that remains constant across all relationships.

Address:
- Temperament baseline: Their natural energy, mood orientation, social inclination
- Core traits: Fundamental personality dimensions (openness, conscientiousness, extraversion, agreeableness, emotional stability)
- Cognitive patterns: How they think, process information, make decisions consistently
- Behavioral signatures: Actions or patterns that define them regardless of context
- Self-concept: How they see themselves and want to be seen
- Identity foundation: What makes them uniquely who they are

Synthesize evidence from ALL contexts to paint a picture of their true self.

FUNDAMENTAL VALUES & BELIEF SYSTEM

What principles, priorities, and beliefs drive {self.target} across ALL relationships?

Identify:
- Core values: What do they consistently prioritize, defend, or sacrifice for?
- Moral framework: What's right/wrong in their worldview?
- Life philosophy: What implicit or explicit beliefs guide their choices?
- Non-negotiables: What boundaries or standards do they maintain everywhere?
- Value hierarchy: Which values take precedence when they conflict?
- Cultural/spiritual influences: How these shape their worldview

Support each value with evidence from multiple contexts showing consistency.

COMMUNICATION SIGNATURE & ADAPTATION

How does {self.target} communicate as their authentic self, and how do they adapt across contexts?

Core Communication Style:
- Baseline formality, directness, emotional expression
- Persistent linguistic patterns, humor style, conversational tendencies
- Communication strengths (clarity, empathy, persuasion, storytelling)
- Communication challenges (conflict avoidance, over-explaining, assumption-making)
- Listening style and responsiveness

Contextual Adaptations:
- How they adjust for different audiences (professional, casual, intimate, familial)
- What stays the same vs what changes
- Communication flexibility and range
- Code-switching patterns and comfort level

Distinguish between their natural communication style and learned adaptations.

EMOTIONAL CORE & REGULATION

How does {self.target} fundamentally experience and manage their emotional world?

Analyze:
- Emotional baseline: General mood, emotional stability, intensity of feelings
- Stress response patterns: How they handle pressure, overwhelm, uncertainty across contexts
- Joy and enthusiasm: What genuinely excites them and how they express it
- Vulnerability approach: When and how they let their guard down
- Coping mechanisms: Consistent strategies for managing difficult emotions
- Empathy style: How they attune to and respond to others' emotions
- Emotional needs: What they require to feel secure, valued, and fulfilled
- Emotional expression: How comfortable they are showing feelings
- Regulation capacity: How well they manage emotional intensity

RELATIONSHIP PHILOSOPHY & APPROACH

What's {self.target}'s overarching approach to human connection?

Core Relationship Patterns:
- Connection style: How they form and maintain bonds (secure, anxious, avoidant, etc.)
- Trust building: What they need to trust and how they earn trust
- Boundary management: Their philosophy on closeness vs independence
- Loyalty expression: How they demonstrate commitment and reliability
- Conflict philosophy: Their beliefs about disagreement and resolution
- Care language: Primary ways they give and receive love/support
- Relationship investments: What they prioritize in maintaining connections
- Reciprocity expectations: How they think about give-and-take
- Intimacy comfort: How close they let people get

LIFE GOALS, ASPIRATIONS & MEANING

What is {self.target} working toward? What gives their life direction and purpose?

Explore:
- Career and achievement goals: Professional ambitions visible across contexts
- Personal growth areas: What they're actively developing in themselves
- Lifestyle aspirations: Family, travel, creativity, community, impact
- Sources of meaning: What makes life feel worthwhile to them
- Long-term vision: Where they see themselves in 5-10 years
- Current challenges: What they're working through right now
- Success definition: How they measure a life well-lived

CROSS-CONTEXT PATTERNS: THE CONSISTENT CORE

Identify 6-10 personality traits or behavioral patterns that appear consistently across multiple contexts:

For each pattern, provide:

Pattern Name: [Brief, memorable label]

Description: [2-3 sentences explaining this trait in detail]

Evidence Across Contexts: 
  - [Context 1]: [Specific examples and quotes]
  - [Context 2]: [Specific examples and quotes]
  - [Context 3]: [Specific examples and quotes]

Consistency Rating: High/Medium/Low - how reliably this appears everywhere

Relationship Impact: How this trait affects their connections with others

---

These patterns reveal who they truly are, independent of social context.

CONTEXTUAL ADAPTATIONS: THE FLEXIBLE SELF

How does {self.target} modify their behavior for different relationships while remaining authentic?

Analyze:
- Specific behavioral changes: What they do differently across contexts
- Adaptation drivers: What motivates changes (social norms, respect, strategy, safety, empathy)
- Authenticity balance: How they maintain core self while being appropriate
- Adaptation skill level: How naturally and comfortably they adjust
- Conscious vs automatic: Which adaptations are intentional vs habitual
- Adaptation cost: Whether it drains them or feels natural
- Consistency in adaptation: Do they adapt in predictable ways?

AUTHENTICITY SPECTRUM

When and where is {self.target} most genuinely themselves?

Map:
- Most authentic contexts: Where they can fully be themselves without filter
- Performance contexts: Where they feel they need to manage impressions
- Authenticity triggers: What situations, topics, or people bring out their true self
- Inauthenticity drivers: What makes them hide, censor, or adapt (fear, professionalism, respect, insecurity)
- Authenticity struggles: Internal conflicts between different aspects of self
- Integration level: How well they integrate different "selves" into a coherent whole

STRENGTHS ACROSS CONTEXTS

What does {self.target} do exceptionally well in relationships and life?

List 6-8 core strengths with evidence from multiple contexts:

[Strength Name]: [Detailed description with specific examples showing this across contexts]

Categories to consider:
- Interpersonal strengths: Connection, empathy, communication, conflict resolution
- Emotional strengths: Resilience, emotional intelligence, regulation
- Practical strengths: Organization, problem-solving, reliability, competence
- Character strengths: Integrity, courage, wisdom, curiosity, humor

GROWTH OPPORTUNITIES & LIMITATIONS

Based on patterns across all contexts, where could {self.target} develop?

Identify:
- Growth edges: Areas where development would significantly enhance their life
- Recurring challenges: Problems that appear across multiple contexts
- Self-limiting patterns: Behaviors or beliefs that hold them back
- Underdeveloped skills: Capabilities they could strengthen
- Relational blind spots: Things they might not realize about their impact on others
- Avoidance patterns: What they consistently shy away from
- Defense mechanisms: How they protect themselves (and the cost)

Frame as opportunities with compassion, not criticisms. Explain WHY each matters.

POTENTIAL BLIND SPOTS

What might {self.target} not realize about themselves or how others perceive them?

Consider:
- Self-perception gaps: Differences between how they see themselves and how they come across
- Impact blindness: Effects of their behavior they might not notice
- Pattern invisibility: Things they do habitually without awareness
- Assumption errors: What they believe about others' perceptions that may be wrong
- Projection tendencies: What they attribute to others that's actually about them
- Rationalization habits: How they explain away certain patterns

INTERESTS, ACTIVITIES & LIFESTYLE

What do they enjoy and how do they spend their time?

Synthesize across contexts:
- Hobbies and recreation: What they do for enjoyment
- Entertainment preferences: Media, arts, culture they consume
- Lifestyle values: Daily routines, health, productivity, leisure balance
- Social vs solitary: How they recharge and what energizes them
- Creative or intellectual pursuits: Learning, creating, exploring
- Physical activities: Movement, sports, outdoor engagement
- Social activities: How they prefer to connect with others

COMPATIBILITY IMPLICATIONS

For relationship matching and understanding dynamics with others:

Ideal Complement Profile:
- Communication match: What style would work best with theirs?
- Emotional fit: What emotional needs and capacities would complement theirs?
- Values alignment: Which values are non-negotiable vs flexible?
- Conflict compatibility: What conflict styles would mesh vs clash?
- Independence balance: How much autonomy vs togetherness do they need?
- Growth support: What kind of partner would help them develop?

Warning Signs & Red Flags:
- Relationship patterns that could become problematic
- Triggers or sensitivities to be aware of
- Behaviors that might push people away
- Unmet needs that could create issues

Thriving Conditions:
- What kind of relationship environment do they need to flourish?
- What brings out their best self?
- What support do they need to feel secure?

PROFILE CONFIDENCE & DATA ASSESSMENT

Overall Confidence Level: High / Medium / Low

Confidence Breakdown:
- High confidence areas: What we're most certain about (and why)
- Medium confidence areas: What seems likely but needs more data
- Low confidence areas: What remains ambiguous or contradictory

Data Completeness Analysis:
- Well-documented contexts: Which relationships are richly represented?
- Thin or missing contexts: What relationship types are under-represented?
- Time span coverage: How much history do we have? Any recent changes?
- Emotional range captured: Have we seen them in conflict, joy, stress, intimacy, crisis?
- Situational diversity: How many different types of situations are represented?

Data Quality Considerations:
- Potential biases in the data sources
- Whether data represents current state or past patterns
- Any major life transitions that might affect patterns

Recommendations for Profile Improvement:

List 5-7 specific types of additional data that would most enhance accuracy:

1. [Data type]: Why this would help and what it would reveal
2. [Data type]: Why this would help and what it would reveal
3. [Data type]: Why this would help and what it would reveal
[...]

Focus on: missing relationship contexts, temporal gaps, behavioral domains not yet observed, specific situations that would be revealing.

═══════════════════════════════════════════════════════
SYNTHESIS PRINCIPLES:
═══════════════════════════════════════════════════════

1. Prioritize patterns over single instances: Look for what appears repeatedly across contexts, not one-off behaviors

2. Weight evidence by confidence: Give more credibility to high-confidence subprofile insights; note when subprofiles disagree about confidence

3. Reconcile contradictions thoughtfully: When contexts disagree, explain why (contextual adaptation, personal growth over time, context-specific triggers, or genuine inconsistency)

4. Distinguish core vs contextual: Clearly separate who they fundamentally are from how they adapt to different situations

5. Ground everything in evidence: Every claim should reference specific examples from the subprofiles. Use phrases like "across family and work contexts, they consistently..." or "in romantic relationships they show X, while in friendships they show Y because..."

6. Embrace complexity and contradiction: Real people are multifaceted and sometimes contradictory—capture that nuance rather than forcing artificial consistency

7. Focus on psychological insight: Go beyond surface description to reveal underlying motivations, fears, needs, and patterns

8. Think compatibility and dynamics: Frame insights in terms useful for understanding how they'd relate to others—what works, what clashes, what they need

9. Be specific and concrete: Avoid generic statements that could apply to anyone. Use actual examples, quotes, and behavioral details

10. Maintain compassionate objectivity: Be honest about limitations and growth areas while respecting their humanity. Frame challenges as opportunities, not flaws.

═══════════════════════════════════════════════════════

Your goal is to create a profile that feels like truly knowing {self.target}—one that would help someone understand what it's like to be in relationship with them, what makes them tick, and how they navigate their world. Synthesize across all contexts to reveal the complete, complex human being."""

        return base_prompt

    def analyze(self) -> Tuple[str, List[float]]:
        try:
            llm = LLM("deepseek/deepseek-chat")
            response = llm.run(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a master psychologist specializing in personality synthesis and "
                            "cross-contextual analysis. You integrate insights from multiple relationship "
                            "contexts to reveal the complete person—both the consistent core self and contextual "
                            "adaptations. You create holistic psychological profiles that are evidence-based, "
                            "nuanced, and rich with insight about how people think, feel, relate, and navigate their world."
                        ),
                    },
                    {
                        "role": "user",
                        "content": self.prompt(),
                    },
                ]
            )

            content = getattr(response.choices[0].message, "content", None)
            if not isinstance(content, str):
                raise RuntimeError("Invalid response format: 'content' is missing or not a string.")

            embed = Embed()

            vectors = embed.run(content)

            return content, vectors

        except ErrorResponse as e:
            print("Error during superprofile analysis:", getattr(e, "details", str(e)))
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during analysis: {e}")


    def run(self):
        return self.analyze()