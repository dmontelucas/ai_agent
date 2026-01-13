import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please set it in a .env file.")

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    # Conversation history starts with the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # Agent loop (limit iterations to avoid infinite spinning)
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # 1) Add model candidates to conversation history
        candidates = getattr(response, "candidates", None)
        if candidates:
            for c in candidates:
                if c.content is not None:
                    messages.append(c.content)

        # 2) If model requested tool calls, execute them
        function_calls = getattr(response, "function_calls", None)

        if function_calls:
            function_responses = []  # list of Part objects to feed back to the model

            for fc in function_calls:
                tool_content = call_function(fc, verbose=args.verbose)

                # Validate tool_content.parts[0].function_response.response exists
                if not tool_content.parts:
                    raise RuntimeError("Tool response had no parts.")

                fr = tool_content.parts[0].function_response
                if fr is None:
                    raise RuntimeError("Tool response part had no function_response.")

                if fr.response is None:
                    raise RuntimeError("FunctionResponse.response was None.")

                # Collect the Part (not the whole Content)
                function_responses.append(tool_content.parts[0])

                if args.verbose:
                    print(f"-> {fr.response}")

            # 3) Append tool results so the model can see them next iteration
            messages.append(types.Content(role="user", parts=function_responses))

        else:
            # No more tool calls: final response for user
            print("Final response:")
            print(response.text)
            return

    # If we hit max iterations without a final response
    print("Error: Reached maximum iterations without a final response.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
