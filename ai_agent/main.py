import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt


def main():
    # Load environment variables
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please set it in a .env file.")

    # --- Argument parsing ---
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Build messages list
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    # Call Gemini with system prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
    )

    # --- Token usage ---
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("No usage_metadata on response. The API request may have failed.")

    prompt_tokens = getattr(usage, "prompt_token_count", None)
    response_tokens = getattr(usage, "candidates_token_count", None)

    if prompt_tokens is None or response_tokens is None:
        raise RuntimeError(f"usage_metadata missing expected token fields: {usage}")

    # --- Output ---
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print(response.text)


if __name__ == "__main__":
    main()
