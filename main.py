import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: raise RuntimeError("API key not found")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    function_results = []
    if not response.usage_metadata: raise RuntimeError("Failed API request")
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception("The function_call_result object should have a non-empty .parts list")
            if not function_call_result.parts[0].function_response:
                raise Exception("The function_call_result_parts[0].function_response shouldn't be NONE")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("The actual function result shouldn't be NONE")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)
    

if __name__ == "__main__": main()
