from typing import List, Optional, Tuple
from human_cupid.llm import LLM, ErrorResponse, Embed

class SubprofileAnalyzer:
    def __init__(
        self,
        target: str, 
        conversation: list[dict[str, str]] = [], 
        profile: Optional[str] = None
    ):
        self.target = target
        self.conversation = conversation
        self.profile = profile

    def prompt(self):
        conversation_text = "\n".join(
            [f"{msg['sender']}: {msg['content']}" for msg in self.conversation]
        )
        
        base_prompt = f"""You are an expert psychologist specializing in communication analysis, personality assessment, and interpersonal dynamics. Your task is to create a deep, nuanced psychological profile of {self.target} based on their conversation patterns.

CONVERSATION DATA:
{conversation_text}

Create a comprehensive psychological profile with the following structure:

CONTEXT & OVERVIEW
- Identify the relationship context (family, friends, work, romantic, social media, etc.)
- Provide a high-level summary of {self.target}'s presence in this context
- Note the data quality: conversation depth, time span, emotional range captured

CORE PERSONALITY ANALYSIS
Describe how {self.target} shows up in this context:
- Behavioral patterns: What do they consistently do? How do they initiate, respond, engage?
- Energy and presence: Are they high/low energy? Dominant/supportive? Leader/follower?
- Mood baseline: Generally optimistic, pragmatic, cautious, playful? How stable is their mood?
- Cognitive style: Abstract vs concrete? Detail-oriented vs big picture? Analytical vs intuitive?

Support every observation with specific examples and quotes.

COMMUNICATION SIGNATURE
Analyze the distinctive way {self.target} communicates:
- Formality level: Professional, casual, code-switching between levels?
- Directness: Blunt, diplomatic, indirect, context-dependent?
- Linguistic patterns: Favorite phrases, sentence structure, vocabulary choices, verbal tics
- Humor style: Sarcastic, wholesome, self-deprecating, observational, dry, absent?
- Emotional expressiveness: Reserved, effusive, selective? Do they name emotions or show them indirectly?
- Response patterns: Quick or delayed? Long or short? Do they answer questions directly?
- Conversational role: Do they ask questions, listen, share, teach, entertain, vent?

Identify 3-5 distinctive communication markers that make {self.target} recognizable.

VALUES & PRIORITIES
What matters to {self.target} based on what they:
- Defend or advocate for: What principles do they stand by?
- Get excited about: What lights them up or energizes them?
- Criticize or complain about: What bothers them or violates their values?
- Invest time in: What do they prioritize in practice, not just words?
- Show pride in: What accomplishments or qualities do they value in themselves?

Connect each value to specific quotes and moments from the conversation.

EMOTIONAL INTELLIGENCE & PATTERNS
How does {self.target} handle their emotional world?
- Emotional awareness: Do they recognize and name their feelings?
- Stress response: Fight, flight, freeze, fawn? How do they cope under pressure?
- Joy expression: How do they share happiness? Reserved or enthusiastic?
- Frustration handling: Patient, explosive, passive-aggressive, constructive?
- Vulnerability: When and how do they show weakness or ask for help?
- Empathy style: Do they validate feelings, problem-solve, or both? Are they emotionally attuned to others?
- Support patterns: How do they seek support? How do they offer it?

RELATIONSHIP DYNAMICS
How does {self.target} operate within this specific relationship?
- Role played: Caretaker, challenger, comedian, advisor, student, equal?
- Boundary management: Clear/unclear? Flexible/rigid? Respectful of others' boundaries?
- Care expression: Acts of service, words of affirmation, quality time, gifts, physical touch?
- Conflict approach: Avoidant, confrontational, collaborative? Do they repair after conflicts?
- Needs expression: Direct about what they want? Hint at needs? Suppress them?
- Power dynamics: Do they seek control, share it, or defer to others?

INTERESTS & LIFESTYLE GLIMPSES
What activities, hobbies, and preferences emerge?
- Topics they bring up repeatedly or enthusiastically
- Entertainment preferences (books, movies, music, games, sports)
- How they spend free time
- Lifestyle values (health, productivity, creativity, relaxation)
- Aspirations or goals mentioned

AUTHENTICITY SPECTRUM
When is {self.target} most and least authentic?
- Most genuine moments: When do they drop pretense? What topics or situations bring out their true self?
- Performance/adaptation moments: When do they seem to be managing impressions or playing a role?
- Drivers of adaptation: Why do they adapt? Social pressure, kindness, fear, habit?
- Consistency level: Is there a coherent sense of self across different moments?

CONTEXT-SPECIFIC VS UNIVERSAL TRAITS
- Unique to this context: Behaviors likely specific to this relationship type
- Likely universal: Core traits probably consistent across contexts
- Context triggers: What about this relationship brings out specific behaviors?

COMPATIBILITY IMPLICATIONS
For future relationship matching, note:
- What kind of communication partner would complement them?
- What values alignment would be essential vs nice-to-have?
- What emotional needs must a compatible partner meet?
- What conflict styles would clash vs harmonize?
- What red flags or deal-breakers appear in their patterns?

CONFIDENCE ASSESSMENT
- Overall confidence level: High/Medium/Low
- Strong signals: What are you most certain about?
- Ambiguous areas: What needs more data?
- Limitations: What can't be determined from this conversation?
- Contradictions: Any inconsistencies that need more context?

KEY EVIDENCE
List 5-10 most revealing quotes that capture {self.target}'s essence in this context.
List 3-5 behavioral examples that exemplify their personality patterns.

---

Analysis Guidelines:
- Ground EVERY claim in specific evidence from the conversation
- Avoid generic statements that could apply to anyone
- Capture nuance and complexity—people are contradictory
- Note both strengths and growth areas without judgment
- Focus on patterns, not one-off moments
- Be specific about what you observe vs what you infer
- Use psychological terminology accurately but explain it clearly"""

        if self.profile:
            base_prompt += f"""

═══════════════════════════════════════════════════════

EXISTING PROFILE CONTEXT

You are updating an existing profile, not creating one from scratch. Here is the current profile:

{self.profile}

    UPDATE INSTRUCTIONS

Your role is to EVOLVE this profile, not replace it.

1. Foundation First: Treat the existing profile as your baseline truth. It represents patterns identified across previous conversations.

2. Integration Approach:
   - ADD new insights that extend or deepen existing observations
   - REFINE existing points with new examples or nuance
   - CONFIRM patterns that the new data supports
   - ENRICH thin areas with newly available detail

3. Handling Contradictions:
   - Only flag contradictions when new data CLEARLY and CONSISTENTLY conflicts with the existing profile
   - Consider whether apparent contradictions might be:
     * Contextual variations (they act differently in different situations)
     * Mood/timing differences (bad day vs good day)
     * Relationship evolution (they've grown or changed)
     * Original profile misinterpretation (new data clarifies ambiguity)
   - If genuine contradiction exists, acknowledge it explicitly: "Previous analysis suggested X, but new data shows Y. Possible explanations: ..."

4. What NOT to change without strong evidence:
   - Core communication style
   - Fundamental values
   - Basic personality orientation
   - Established behavioral patterns

5. What TO update readily:
   - Confidence levels (increase with more data)
   - Specific examples and quotes
   - Depth of understanding in any dimension
   - Context-specific nuances
   - Ambiguous areas that are now clearer

6. Quality Standards:
   - Maintain narrative continuity with the existing profile
   - Build on previous insights rather than repeating them
   - Note what's new: "This conversation reveals..." or "New data confirms..."
   - Preserve the person's complexity—don't oversimplify for consistency

Your updated profile should feel like chapter 2 of the same story, not a different book."""
        
        return base_prompt

    def analyze(self) -> Tuple[str, List[float]]:
        try:
            llm = LLM("deepseek/deepseek-chat")
            response = llm.run(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert psychologist specializing in personality assessment, "
                            "communication analysis, and relationship dynamics. You create deep, "
                            "evidence-based psychological profiles that reveal how people think, feel, "
                            "communicate, and relate to others. Your analyses are nuanced, specific, "
                            "and grounded in observable patterns."
                        ),
                    },
                    {
                        "role": "user",
                        "content": self.prompt(),
                    },
                ]
            )

            content = response.choices[0].message.content

            if isinstance(content, str):
                embed = Embed()

                vectors = embed.run(content)

                return content, vectors
            else:
                raise TypeError("Expected response.choices[0].message.content to be a string")

        except ErrorResponse as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during analysis: {e}")


    def run(self):
        return self.analyze()