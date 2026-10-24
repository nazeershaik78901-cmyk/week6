
# MINI-LAB 1.6
# Role-Based and Negative Prompting

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.6-flash"

# Same question for all three prompts
question = "Explain the importance of exercise."

# 1. Baseline prompt
baseline_prompt = f"""
{question}
"""

# 2. Role-based prompt
role_prompt = f"""
You are a motivational fitness coach.

{question}
"""

# 3. Role + Negative prompting
negative_prompt = f"""
You are a motivational fitness coach.

Do not use any medical jargon.
Do not mention weight loss.

{question}
"""

# Send prompts to Gemini safely
def get_response(prompt, label):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return (
            response.text.strip()
            if response.text
            else "No response returned."
        )

    except Exception as e:
        print(f"\n{label} failed: {e}")
        return f"API request failed: {e}"


# Generate responses
baseline_text = get_response(
    baseline_prompt, "Baseline"
)

role_text = get_response(
    role_prompt, "Role-based"
)

negative_text = get_response(
    negative_prompt, "Negative prompting"
)

# Print responses
print("\n================ BASELINE ================")
print(baseline_text)

print("\n========== ROLE-BASED (FITNESS COACH) ==========")
print(role_text)

print("\n========== ROLE + NEGATIVE PROMPTING ==========")
print(negative_text)

# Analysis
print("\n================ ANALYSIS ================")

print("""
1. Tone:
The baseline response is generally neutral and informative.
The role-based response is more motivational and encouraging.

2. Vocabulary:
The role-based response uses more energetic and fitness-related words.

3. Negative constraints:
The final response should not use medical jargon
and should not mention weight loss.

4. Conclusion:
Role-based prompting changes the tone and style of the response.
Negative prompting helps control what information should not appear.
""")
