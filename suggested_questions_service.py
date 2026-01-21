import json
from pathlib import Path
from openai import OpenAI
import os


# ---------------- OpenAI Client ----------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# ---------------- Static Questions Path ----------------
STATIC_Q_PATH = Path("rfp_questions.json")

#------ load static questions---------------------#
def load_static_questions() -> list[dict]:
    if not STATIC_Q_PATH.exists():
        return []

    try:
        with open(STATIC_Q_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        questions = data.get("static_questions", [])
        if not isinstance(questions, list):
            return []

        # Randomize order so callers don't always get the same ones
        import random
        random.shuffle(questions)

        return questions

    except Exception as e:
        print(f"Error loading static questions: {e}")
        return []



#---------------------- AI QUESTIONS GENERATION ---------------------#
def generate_ai_questions(context: str, limit: int = 2) -> list[dict]:
    """
    Generate contextual RFP discovery questions.
    These are ARCHITECT-led questions, not content extraction.
    """

    prompt = f"""
You are a SENIOR CMS PRESALES ARCHITECT.

Your task is to propose DISCOVERY QUESTIONS that a CMS architect
would naturally ask when analyzing THIS website for an RFP.

IMPORTANT GUIDELINES:
- Generate question strictly in and around the website context provided.
- These are NOT content summary questions
- These are ARCHITECTURE & ESTIMATION questions
- Even if the website content is limited or generic,
  you MUST still generate relevant CMS/RFP questions
- Use the website content ONLY to slightly tailor wording and focus

You MUST return exactly {limit} questions.

STRICT OUTPUT RULES:
- Return ONLY valid JSON
- No markdown
- No explanations
- Output must start with [ and end with ]

JSON FORMAT:
[
  {{
    "id": "string",
    "ui_label": "short one-line question shown in UI",
    "ai_prompt": "detailed analysis instruction tailored to this website"
  }}
]

Website Context (partial, for reference only):
{context[:6000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a CMS architect. "
                    "Never return an empty array. "
                    "Always return exactly the requested number of questions."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    raw = response.choices[0].message.content.strip()
    print("RAW AI QUESTIONS:", raw)

    try:
        data = json.loads(raw)
        if isinstance(data, list) and len(data) == limit:
            return data
    except Exception as e:
        print("AI JSON PARSE FAILED:", e)

    # 🚨 Safety fallback (should rarely trigger now)
    return [
        {
            "id": "content_modeling",
            "ui_label": "What content types and templates are needed?",
            "ai_prompt": (
                "Analyze the website to infer required content types, templates, "
                "and reusable content models suitable for CMS implementation."
            )
        },
        {
            "id": "navigation_structure",
            "ui_label": "How complex is the site's navigation and IA?",
            "ai_prompt": (
                "Evaluate navigation structure, page hierarchy, and internal linking "
                "to assess CMS navigation modeling and information architecture complexity."
            )
        }
    ][:limit]


#---------------------- COMBINED SUGGESTED QUESTIONS ---------------------#
import random

def get_suggested_questions(context: str) -> list[dict]:
    static_all = load_static_questions()
    static_questions = random.sample(
        static_all,
        k=min(2, len(static_all))
    )

    ai_questions = generate_ai_questions(
        context=context,
        limit=2
    )

    return static_questions + ai_questions