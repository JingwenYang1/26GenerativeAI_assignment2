from google import genai
import sys
import os
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
API_KEY = "AIzaSyAhYsKItMGZ0BSkymTPSmUssD_of5a3NA0"
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
You are an experienced game industry consultant helping indie developers 
write pitch emails to investors and publishers. 

Your emails should:
- Open with a compelling hook that captures the game's core appeal
- Describe the game concept clearly without using bullet points
- Explain what makes this game stand out in the current market
- Close with a specific and confident call to action
- Sound like it was written by a real person who believes in the project
- Be professional but not stiff, around 150 to 200 words
- Do not invent a game title unless the user provides one
- Do not use any markdown formatting such as bold, italic, or headers
- Do not invent gameplay mechanics, story details, or features that were not mentioned in the input
- Do not claim the team has a prototype or demo unless the user says so
- Sign the email as Jingwen Yang, Founder of Dawnveil Studio
"""

# ── Main function ───────────────────────────────────────────────
def generate_pitch_email(game_concept: str) -> str:
    client = genai.Client(api_key=API_KEY)

    prompt = f"""Write a pitch email for the following indie game concept:

{game_concept}

The email should be addressed to a potential investor or publisher."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    return response.text


def save_output(game_concept: str, email_text: str):
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/pitch_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("=== GAME CONCEPT ===\n")
        f.write(game_concept + "\n\n")
        f.write("=== GENERATED PITCH EMAIL ===\n")
        f.write(email_text + "\n")

    print(f"\nOutput saved to: {filename}")
    return filename


# ── Entry point ─────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        game_concept = " ".join(sys.argv[1:])
    else:
        print("Enter your game concept (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        game_concept = " ".join(lines)

    if not game_concept.strip():
        print("Error: no game concept provided.")
        sys.exit(1)

    print("\nGenerating pitch email...\n")
    email = generate_pitch_email(game_concept)

    print("=== GENERATED PITCH EMAIL ===")
    print(email)

    save_output(game_concept, email)
