import os
import argparse
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    apiKey = os.environ.get("GEMINI_API_KEY")
    if not apiKey:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=apiKey)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User promp")
    args = parser.parse_args()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=args.user_prompt
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    metadata = response.usage_metadata

    print("Prompt tokens:", metadata.prompt_token_count)
    print("Response tokens:", metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
