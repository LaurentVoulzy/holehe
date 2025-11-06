"""Claude AI analysis engine for marketing research."""
import json
from typing import Dict, Any, List
from anthropic import Anthropic
from .config import Config


class ClaudeAnalyzer:
    """Use Claude AI to analyze marketing data and generate creative ideas."""

    def __init__(self):
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.CLAUDE_MODEL
        self.max_tokens = Config.CLAUDE_MAX_TOKENS

    def analyze(
        self,
        company_name: str,
        company_url: str,
        competitor_urls: List[str],
        ad_data: Dict[str, Any],
        trends_data: Dict[str, Any]
    ) -> str:
        """
        Send all data to Claude for comprehensive analysis.

        Args:
            company_name: Target company name
            company_url: Company website URL
            competitor_urls: List of competitor URLs
            ad_data: Scraped ad data
            trends_data: Trends analysis data

        Returns:
            Claude's analysis and creative ideas
        """
        # Build the research context
        context = self._build_research_context(
            company_name,
            company_url,
            competitor_urls,
            ad_data,
            trends_data
        )

        # Build the analysis prompt
        prompt = self._build_analysis_prompt(company_name, context)

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=1.0,
                system=self._get_system_prompt(),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the response text
            result = response.content[0].text

            return result

        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def _get_system_prompt(self) -> str:
        """Get the system prompt for Claude."""
        return """SYSTEM ROLE
You are an advanced AI marketing strategist and creative director. Your task is to research, analyze, and generate high-impact ad and content ideas for a given company.

GOALS
When provided with research data about a company and its competitors:

1. Analyze the company's ads and social media content across all collected platforms
2. Analyze 3-7 competitors and their ads/social posts
3. Find their top-performing content ("winner creatives") — the top 10% by engagement
4. Analyze creative patterns (hook types, tone, pacing, CTAs, visuals, duration, editing styles, emotional triggers)
5. Gather industry and audience insights
6. Review this week's viral trends across all platforms
7. Generate creative ideas that combine all these insights

OUTPUT STRUCTURE
Produce a well-formatted creative report with these ordered sections:

1. Company Analysis
- Summarize what the company is currently doing on ads and social content
- Platforms where it is most active
- Strengths and weaknesses in creative strategy
- Visual style, tone, and messaging
- Observed engagement behavior

2. Competitor Analysis
- List 3–7 close competitors with brief notes on each
- Key creative patterns or winning campaigns
- What's working best for them (hooks, visuals, voice, CTAs)
- What's overused or missing in the category
- What differentiates the target company from competitors

3. This Week's Viral Trends (Global Overview)
A separate section listing the most relevant platform trends at the time of query. For each platform, provide:
- Trend Name / Pattern
- Example of its Use (short summary)
- Why It's Trending
- What Audience It Resonates With

4. Trend Adaptation for [Company Name]
Explain how the above trends can be repurposed for this company's industry and audience. For each trend:
- How it can fit the company's tone and brand
- One ad idea and one organic content idea inspired by that trend

5. Ad Concepts (Minimum 10 Ideas)
Generate 10 or more ad ideas. Each ad concept must include:
- Target Group:
- Duration:
- Idea:
- Why It Will Be Successful:
- Script:

Script Requirements:
- Include clear, vivid visual direction
- Incorporate psychological or emotional triggers from the analysis
- Be optimized for the target platform (Meta, TikTok, YouTube, etc.)
- Include full VO lines and tone notes
- Avoid generic "user testimonials" unless specific ugc type of videos are trending or vague storytelling — make them unique, creative, specific, and fresh with the goal to bring back roi and get views

6. Social Content Ideas (Minimum 10 Ideas)
Generate 10 or more social media content ideas (reels, shorts, carousels, stills). Each idea must include:
- Target Group:
- Duration:
- Idea:
- Why It Will Be Successful:
- Script:

- Tailor each idea to a platform (mention which one)
- Make scripts engaging, trend-aware, and authentic
- Include VO or caption text
- Be creative and unexpected

STYLE & TONE
- Write clearly and visually — like a professional creative brief
- Avoid filler language, buzzwords, or hype
- Use plain formatting (no JSON)
- Use clean headings, spacing, and numbering
- Integrate real-world examples where possible

CONSTRAINTS
- Do not invent fake data or names
- Do not reveal internal reasoning or sources
- Always explain why each idea would perform well
- Keep output readable and presentation-ready"""

    def _build_research_context(
        self,
        company_name: str,
        company_url: str,
        competitor_urls: List[str],
        ad_data: Dict[str, Any],
        trends_data: Dict[str, Any]
    ) -> str:
        """Build the research context for Claude."""
        context_parts = []

        # Company info
        context_parts.append(f"TARGET COMPANY: {company_name}")
        context_parts.append(f"WEBSITE: {company_url}")
        context_parts.append("")

        # Competitors
        context_parts.append("COMPETITORS:")
        for i, url in enumerate(competitor_urls, 1):
            context_parts.append(f"{i}. {url}")
        context_parts.append("")

        # Ad data
        context_parts.append("AD DATA COLLECTED:")
        context_parts.append(json.dumps(ad_data, indent=2))
        context_parts.append("")

        # Trends data
        context_parts.append("THIS WEEK'S TRENDS:")
        context_parts.append(json.dumps(trends_data, indent=2))
        context_parts.append("")

        return "\n".join(context_parts)

    def _build_analysis_prompt(self, company_name: str, context: str) -> str:
        """Build the analysis prompt for Claude."""
        prompt = f"""Please analyze the following marketing research data and generate a comprehensive creative report for {company_name}.

RESEARCH DATA:
{context}

---

Please provide your analysis following the exact structure defined in your system prompt:

1. Company Analysis
2. Competitor Analysis
3. This Week's Viral Trends (Global Overview)
4. Trend Adaptation for {company_name}
5. Ad Concepts (Minimum 10 Ideas)
6. Social Content Ideas (Minimum 10 Ideas)

Remember to:
- Be specific and actionable
- Base insights on the provided data
- Generate creative, unique ideas
- Include full scripts with visual direction
- Explain why each idea will be successful
- Make the output presentation-ready

Begin your analysis now:"""

        return prompt

    def test_connection(self) -> bool:
        """
        Test the Claude API connection.

        Returns:
            True if connection is successful
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, this is a test. Please respond with 'OK'."
                    }
                ]
            )

            return True

        except Exception as e:
            print(f"Claude API connection test failed: {e}")
            return False
