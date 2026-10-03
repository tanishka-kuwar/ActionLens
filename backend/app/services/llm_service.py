import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


def generate_response(prompt: str) -> str:

    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as error:

            if "503" in str(error) or "UNAVAILABLE" in str(error):

                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

            else:
                raise