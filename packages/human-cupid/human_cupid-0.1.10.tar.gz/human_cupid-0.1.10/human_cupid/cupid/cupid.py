from typing import List
from human_cupid.llm.llm import LLM, ErrorResponse

from .schema import CompatibilityStructured, CompatibilityAnalysis

class Cupid:
    def __init__(self, superprofiles: List[str], person_names: List[str]):
        self.superprofiles = superprofiles
        self.person_names = person_names

    def prompt(self):
        profiles_summary = []

        for i, superprofile_text in enumerate(self.superprofiles):
            summary = f"""
═══════════════════════════════════════════════════════
PERSON {i+1}: {self.person_names[i].upper()}
═══════════════════════════════════════════════════════

{superprofile_text}
"""
            profiles_summary.append(summary)

        all_summaries = "\n".join(profiles_summary)

        if len(self.person_names) > 1:
            names_string = ', '.join(self.person_names[:-1]) + ' and ' + self.person_names[-1]
        else:
            names_string = self.person_names[0] if self.person_names else ''

        base_prompt = f"""You are an expert relationship psychologist and compatibility analyst with deep expertise in interpersonal dynamics, attachment theory, communication patterns, and the research-backed factors that predict relationship success.

Your task is to analyze the compatibility between {names_string} based on their comprehensive psychological profiles.

═══════════════════════════════════════════════════════
COMPLETE PERSONALITY PROFILES:
═══════════════════════════════════════════════════════

{all_summaries}

═══════════════════════════════════════════════════════
COMPATIBILITY ANALYSIS INSTRUCTIONS:
═══════════════════════════════════════════════════════

**CRITICAL ETHICAL GUIDELINES:**

1. **Red Flag Assessment**: Before proceeding with compatibility analysis, carefully review both profiles for serious concerns:
   - Patterns of manipulation, control, or abuse
   - Lack of empathy or disregard for others' wellbeing
   - Dishonesty or unethical behavior patterns
   - Active addiction or untreated mental health crises
   - Behaviors that could harm others
   
   **If you identify serious red flags, STOP the compatibility analysis and clearly state your concerns with specific evidence.**

2. **Relationship Type Focus**: This analysis should focus on **friendship, work partnership, family dynamics, or general interpersonal compatibility**. Do NOT frame this as romantic compatibility analysis unless explicitly requested and appropriate.

═══════════════════════════════════════════════════════

Create a comprehensive compatibility analysis with the following structure:

## EXECUTIVE SUMMARY

Provide a 2-3 paragraph overview answering:
- What's the overall compatibility picture?
- What's the relationship potential (realistic assessment)?
- What's the most important thing to know about their dynamic?
- Would you recommend they pursue this relationship? Why or why not?

## OVERALL COMPATIBILITY SCORE

**Total Compatibility: [X/100]**

Provide an honest percentage reflecting genuine compatibility. Not everyone is compatible—if the data shows fundamental misalignment, scores should reflect that (potentially below 50%).

**Confidence Level**: High / Medium / Low - How certain are you of this assessment based on available data?

## COMPATIBILITY STORY: THE RELATIONSHIP NARRATIVE

Write a detailed, realistic narrative (4-6 paragraphs) about what their relationship would actually look like:

- **Initial attraction/connection**: What would naturally draw them together? What would they appreciate in each other immediately?
- **Day-to-day dynamics**: How would they interact regularly? What would conversations be like? How would they spend time together?
- **Relationship flow**: What would feel easy and natural? What would require effort and compromise?
- **Challenge areas**: What friction points would emerge? How would their differences create tension?
- **Long-term trajectory**: Where would this relationship naturally go? What would sustain it or undermine it over time?

Make this concrete and specific to THEIR personalities, not generic relationship descriptions.

## DIMENSION-BY-DIMENSION ANALYSIS

### 1. VALUES ALIGNMENT [Score: X/100]

**Core Values Comparison:**
- Identify each person's top 5 values
- Map where they align, complement, or conflict
- Explain the significance of matches and mismatches

**Life Priorities:**
- Career vs relationships vs personal growth
- Family orientation and long-term vision
- Lifestyle preferences and life goals

**Belief Systems:**
- Moral frameworks and ethical approaches
- Worldviews and philosophies
- Deal-breakers and non-negotiables

**Why This Matters**: Explain why values alignment is the #1 predictor of relationship success and what their specific pattern means.

**Specific Examples**: Quote from profiles to illustrate alignment or misalignment.

### 2. PERSONALITY CHEMISTRY [Score: X/100]

**Core Personality Dynamics:**
- How their fundamental temperaments interact
- Complement vs clash patterns
- Energy level compatibility
- Introversion/extraversion balance
- Stability vs spontaneity
- Thinking vs feeling orientation

**Psychological Fit:**
- Attachment style compatibility (if apparent)
- How they'd fulfill or frustrate each other's emotional needs
- Power dynamics and control issues
- Independence vs closeness preferences

**Specific Interactions:**
- What would feel exciting/energizing about this pairing?
- What would feel draining or frustrating?
- How would they bring out each other's best/worst?

### 3. COMMUNICATION COMPATIBILITY [Score: X/100]

**Communication Style Match:**
- Directness levels: Do they speak the same language?
- Formality and emotional expression alignment
- Conflict approach compatibility (avoidant, confrontational, collaborative)
- Listening and validation styles
- Humor compatibility

**Potential Communication Challenges:**
- Misunderstanding patterns that would emerge
- How their communication differences could create problems
- What they'd need to bridge communication gaps

**Communication Strengths:**
- Natural understanding and ease
- Complementary communication gifts
- How they could enhance each other's expression

**Conflict Resolution Prediction:**
- How would they handle disagreements?
- What conflict patterns would emerge?
- Could they repair after fights?
- What would escalate vs de-escalate tension?

### 4. EMOTIONAL COMPATIBILITY [Score: X/100]

**Emotional Expression Match:**
- How they show and receive emotions
- Vulnerability comfort levels
- Emotional intensity compatibility
- Affection style alignment

**Support Needs & Capacities:**
- Can Person A provide what Person B needs emotionally?
- Can Person B provide what Person A needs emotionally?
- Empathy level match
- Stress response compatibility

**Emotional Challenges:**
- Where they might fail to meet each other's needs
- Emotional triggers or sensitivities
- How emotional differences could cause pain

### 5. LIFESTYLE COMPATIBILITY [Score: X/100]

**Daily Life Fit:**
- Energy levels and activity preferences
- Social needs (introvert/extrovert balance)
- Routine vs spontaneity preferences
- Alone time vs together time needs
- Cleanliness, organization, living habits

**Interests & Activities:**
- Shared hobbies and interests
- Activities they could enjoy together
- Separate interests and how they'd handle them

**Long-term Lifestyle:**
- Life pace and rhythm compatibility
- Future lifestyle goals (location, travel, adventure vs stability)
- Work-life balance alignment

### 6. GROWTH POTENTIAL [Score: X/100]

**Mutual Development:**
- What could Person A learn from Person B?
- What could Person B learn from Person A?
- How could they challenge each other to grow?
- What personal development could this relationship catalyze?

**Bringing Out Best Qualities:**
- What strengths would this relationship activate in each person?
- How would they inspire or motivate each other?
- What latent potential could they unlock in each other?

**Growth Challenges:**
- Where might they enable each other's limitations?
- What unhealthy patterns might they reinforce?
- How could they hold each other back?

## RELATIONSHIP SCENARIOS: REALISTIC PREDICTIONS

### Best Case Scenario (When Everything Clicks)

Describe in vivid detail what their relationship looks like at its best:
- Specific situations where they'd thrive together
- What would make them feel deeply connected
- The magic moments and peak experiences
- Why they'd be grateful for each other

### Typical Day/Week Together

Paint a realistic picture of ordinary time together:
- Morning routine if applicable
- Typical conversations and interactions
- How they'd spend weekends
- The texture of daily life together

### Conflict Scenario

Describe a realistic conflict and how they'd handle it:
- What would they fight about most?
- How would the argument unfold given their styles?
- Could they resolve it? How?
- What would happen after the conflict?

### Stress Test: Challenging Times

How would they handle life challenges together?
- Career stress, family crisis, health issues
- Would they pull together or apart?
- How would each support (or fail to support) the other?

### Long-Term Trajectory (1-5 years)

Where would this relationship realistically go?
- What would deepen over time?
- What would become more challenging?
- Would they grow together or apart?
- What's the most likely outcome?

## CHALLENGE AREAS & RISK FACTORS

### Major Incompatibilities

List and explain the most significant compatibility challenges (3-5):

**Challenge #1: [Name]**
- Specific description of the incompatibility
- Why this matters and how it would manifest
- Severity: Minor / Moderate / Major / Deal-breaker
- Whether it's workable with effort

[Repeat for each major challenge]

### Warning Signs to Watch For

Specific red flags or concerning patterns that could emerge:
- Early warning signs that things aren't working
- Behaviors that would indicate growing problems
- When to reconsider the relationship

### Deal-Breakers Analysis

Are there fundamental incompatibilities that make this relationship inadvisable?
- Values conflicts that can't be bridged
- Personality clashes that would create ongoing pain
- Lifestyle differences that would breed resentment
- Emotional mismatches that would leave both unfulfilled

**Honest Assessment**: Should they even pursue this relationship? Be direct if the answer is no.

## SUCCESS ROADMAP: MAKING IT WORK

**If compatibility is sufficient (>60%), provide this roadmap. If not, skip this section and explain why.**

### Phase 1: Early Foundation (Weeks 1-3)

**Critical Early Conversations:**
List 5-7 specific topics they MUST discuss early:
1. [Topic]: Why it matters and what they need to clarify
2. [Topic]: Why it matters and what they need to clarify
[etc.]

**Early Action Steps:**
- Specific activities to build connection
- How to establish healthy patterns from the start
- What to observe and learn about each other

### Phase 2: Navigating Differences (Months 1-3)

**Bridging Gaps:**
- How to handle their specific communication differences
- Strategies for meeting different emotional needs
- Compromises they'll need to make
- Boundaries they should establish

**Conflict Resolution Framework:**
Specific guidance for how THESE TWO people should handle disagreements based on their styles.

### Phase 3: Building Long-Term (Months 3+)

**Sustaining Connection:**
- Rituals and habits that would work for them
- How to keep growing together
- Preventing their specific drift patterns

**Leveraging Strengths:**
- How to build on what works naturally
- Utilizing complementary gifts
- Creating synergy from differences

## PRACTICAL GUIDANCE

### Essential Discussions (First 5 Conversations)

List specific conversations with talking points:

1. **[Topic]**: 
   - Why this matters for them specifically
   - Key questions to ask each other
   - What they need to hear from each other

[Repeat for 5 conversations]

### Activities to Strengthen Bond

Suggest 5-7 specific activities suited to THEIR interests and styles:
- Why each activity would work for them
- What it would reveal or develop
- How to make it meaningful

### Warning Signs to Monitor

Specific behaviors or patterns to watch for:
- Early indicators of problems
- When to have difficult conversations
- When professional help might be needed

### When to Walk Away

Honest criteria for when this relationship should end:
- Specific deal-breakers for this pairing
- Signs of toxicity or harm
- When trying harder would be unhealthy

## FINAL VERDICT & RECOMMENDATIONS

### Bottom Line Assessment

Be direct and honest:
- Should they pursue this relationship? Yes/No/Maybe
- What's the realistic potential?
- What would it take to make it work?
- Is that effort worth it given the likely outcome?

### Key Takeaways (3-5 Bullet Points)

The most important things to understand about this compatibility.

### Parting Wisdom

Final thoughts or advice specific to this pairing.

═══════════════════════════════════════════════════════
ANALYSIS PRINCIPLES:
═══════════════════════════════════════════════════════

1. **Honesty Over Optimism**: Don't force compatibility where it doesn't exist. Low compatibility scores (30-50%) are valid if the data supports it.

2. **Specificity**: Every insight should be grounded in their specific personality traits, not generic relationship advice. Use details from the profiles.

3. **Realistic Predictions**: Base scenarios on actual psychological patterns, not idealized versions. Show how their real personalities would interact.

4. **Evidence-Based**: Reference specific traits, values, and patterns from the profiles. Quote when relevant.

5. **Balanced Perspective**: Acknowledge both strengths and challenges. Don't sugarcoat problems, but don't overlook genuine compatibility either.

6. **Research-Backed**: Use established relationship science about what predicts success (values alignment, communication, emotional attunement, etc.).

7. **Actionable Guidance**: Provide specific, practical advice they could actually implement, not vague platitudes.

8. **Ethical Responsibility**: Flag serious concerns. Don't enable potentially harmful relationships. Prioritize wellbeing over compatibility scores.

9. **Appropriate Context**: Remember this is for friendship/work/general interpersonal dynamics, not romantic matchmaking unless specifically appropriate.

10. **Nuanced Complexity**: Real compatibility is complex. Capture contradictions and contextual factors. Avoid oversimplified assessments.

═══════════════════════════════════════════════════════

Your goal is to provide a deeply insightful, honest, and helpful compatibility analysis that genuinely serves the people involved—helping them understand what a relationship would really be like and make informed decisions about whether to pursue it."""

        return base_prompt
    
    def extract_structured_data(self, full_analysis: str) -> CompatibilityStructured:
        """
        Extract structured compatibility data using the model's schema enforcement.
        Throws an exception if extraction fails or no valid data is returned.
        """
        extraction_prompt = f"""Extract the following structured data from this compatibility analysis.

IMPORTANT RULES:
- NEVER include personal names or identifiers.
- Return ONLY valid structured data in the exact schema format.
- If any information is missing, infer it logically from context instead of omitting it.

Analysis:
{full_analysis}

Extract:
1. score_compatibility: integer (0–100)
2. shared_interests: list of 3–5 shared hobbies/interests (generic terms)
3. conversation_topics: list of 5–7 suitable discussion topics (generic terms only)
4. recommendation_summary: 2–3 sentence anonymous summary of relationship outlook
5. relationship_type: one of [friendship, work_partnership, mentor_mentee, casual_acquaintance, not_recommended]
"""

        try:
            llm = LLM("deepseek/deepseek-chat")
            response = llm.run(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a structured data extractor for compatibility analyses. "
                            "Always output data strictly following the provided schema. "
                            "Never include explanations or text outside the schema fields."
                        ),
                    },
                    {"role": "user", "content": extraction_prompt},
                ],
                response_format=CompatibilityStructured,
            )

            if not response:
                raise RuntimeError("No structured response returned from LLM.")
            if not isinstance(response, CompatibilityStructured):
                raise RuntimeError(
                    f"Invalid structured response type: expected CompatibilityStructured, got {type(response)}"
                )

            if (
                response.score_compatibility is None
                or not response.shared_interests
                or not response.conversation_topics
                or not response.recommendation_summary
                or not response.relationship_type
            ):
                raise RuntimeError("Structured data incomplete or missing required fields.")

            return response

        except ErrorResponse as e:
            print("Error during structured data extraction:", getattr(e, "details", str(e)))
            raise RuntimeError(f"LLM Error during structured extraction: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract structured data: {e}")

    def analyze(self) -> CompatibilityAnalysis:
        """
        Performs a full compatibility analysis and structured data extraction.
        Throws if either step fails.
        """
        try:
            llm = LLM("deepseek/deepseek-chat")
            response = llm.run(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert relationship psychologist specializing in compatibility "
                            "analysis and interpersonal dynamics. You integrate attachment theory, "
                            "personality psychology, and communication science to produce evidence-based "
                            "compatibility assessments. You value depth, accuracy, and honesty."
                        ),
                    },
                    {"role": "user", "content": self.prompt()},
                ],
            )

            full_analysis = getattr(response.choices[0].message, "content", None)
            if not isinstance(full_analysis, str) or not full_analysis.strip():
                raise RuntimeError("Invalid or empty text analysis from LLM.")

            structured_data = self.extract_structured_data(full_analysis)

            return CompatibilityAnalysis(
                analysis=full_analysis,
                structured=structured_data,
            )

        except ErrorResponse as e:
            print("Error during compatibility analysis:", getattr(e, "details", str(e)))
            raise RuntimeError(f"LLM Error during analysis: {e}")
        except Exception as e:
            raise RuntimeError(f"Compatibility analysis failed: {e}")
        
    def run(self):
        return self.analyze()