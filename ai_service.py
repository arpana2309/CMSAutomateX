import os
from dotenv import load_dotenv
import json

load_dotenv()  # loads .env into environment variables
from openai import OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")
client = OpenAI(api_key=OPENAI_API_KEY)


def ask_ai(user_question, website_context):
    system_prompt = """
You are an expert UI/UX analyst and CMS architect.

You have been given structured content extracted from a website.
This content represents the COMPLETE and TRUSTED source of truth.

Your job:
- Analyze the website structure
- Identify page types, components, layouts, and patterns
- Infer reasonable conclusions even if labels are not explicit

IMPORTANT RULES:
- NEVER say "I don't know" if the information can be inferred
- If something is not explicitly stated, say "Based on the structure, it appears that..."
- Answer ONLY using the provided website context
- Be concise, structured, and confident
"""

    user_prompt = f"""
WEBSITE CONTENT:
----------------
{website_context}
----------------

USER QUESTION:
{user_question}

INSTRUCTIONS:
- Answer specifically about this website
- List components or page types when applicable
- Use bullet points if helpful
- Do not repeat the question
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4.1 if available
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
# ---------------- RFP MODE  ----------------
def generate_rfp_analysis(website_context: str) -> dict:
    """
    Generates structured RFP-ready website analysis.
    Output is STRICT JSON to support Excel export.
    """

    prompt = f"""
You are acting as a SENIOR CMS SOLUTION ARCHITECT preparing a
DETAILED RFP ANALYSIS DOCUMENT.

The goal is to extract MAXIMUM STRUCTURAL INFORMATION from the website,
similar to what would be produced during a full manual site audit.

------------------------------------------------------------
OUTPUT FORMAT (STRICT – MUST MATCH EXACTLY)
------------------------------------------------------------
{{
  "overview": {{
    "website_purpose": "",
    "industry": "",
    "overall_structure": ""
  }},
  "page_types": [
    {{
      "name": "",
      "description": "",
      "complexity": "Low | Medium | High"
    }}
  ],
  "components": [
    {{
      "name": "",
      "description": "",
      "used_on_pages": "",
      "media_type": "None | Image | Video | Gallery | Image+Text",
      "media_count": "",
      "cms_managed": "Yes | No",
      "third_party_dependency": "",
      "complexity": "Low | Medium | High",
      "effort_estimate_days": ""
    }}
  ],
  "pages": [
    {{
      "url": "",
      "page_type": "",
      "components": [],
      "complexity": "Low | Medium | High"
    }}
  ],
  "third_party_integrations": [
    {{
      "name": "",
      "category": "",
      "purpose": "",
      "evidence_or_inference": ""
    }}
  ],
  "recommendations": []
}}

------------------------------------------------------------
ANALYSIS INSTRUCTIONS (VERY IMPORTANT)
------------------------------------------------------------
1. Be EXHAUSTIVE:
   - List ALL identifiable page types
   - Over-enumerate components rather than under-listing
   - Break large components into smaller reusable ones where possible

2. COMPONENT ANALYSIS:
   - Identify layout components (header, footer, grid, cards)
   - Identify content components (hero, banner, text blocks)
   - Identify interactive components (forms, search, filters)
   - Identify media components (images, videos, galleries, carousels)
   - Assume CMS-driven components unless clearly static

3. COMPLEXITY & EFFORT:
   - Low: static content, simple text/images
   - Medium: forms, filters, reusable components
   - High: personalization, search, integrations, video platforms
   - Effort should be realistic RFP-style estimates (e.g. "2–3", "4–6")

4. THIRD-PARTY INTEGRATIONS:
   - Detect analytics, tag managers, marketing tools, DAM/CDN, video, chat
   - If not explicit, infer based on structure or behavior
   - DO NOT invent integrations without reasonable signals

5. PAGE COVERAGE:
   - Assume content is aggregated from multiple pages and sitemap.xml
   - Treat the site as a complete system, not isolated pages

6. LANGUAGE & QUALITY:
   - Use professional presales terminology
   - Write content suitable for direct Excel export
   - DO NOT include explanations outside the JSON

------------------------------------------------------------
WEBSITE CONTENT (SOURCE OF TRUTH)
------------------------------------------------------------
{website_context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return json.loads(response.choices[0].message.content)