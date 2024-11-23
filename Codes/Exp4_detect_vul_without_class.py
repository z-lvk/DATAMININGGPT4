from openai import OpenAI
import os
import time
import pandas as pd

# Initialize the OpenAI client with the API key
client = OpenAI(api_key="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")

# Define the directory containing the labeled Python files
directory = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\Labeled_files'

# Prepare a list to store GPT-4 responses
gpt_response_list = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    # Check if it is a file
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            Vul_code = file.read()

            # Define the prompt
            prompt = f"""
            Your task is to determine whether the following Python code, delimited with triple backticks, is vulnerable or not.
            Identify the following items:
                - CWE of its vulnerabilities.
                - Lines of vulnerable code.
            Format your response as a list of JSON objects with "label" and "line of Code" as the keys for each vulnerability.
            If the information isn't present, use "unknown" as the value.
            Make your response as short as possible and only answer with JSON.

            Python code: ```{Vul_code}```
            """

            # Call GPT-4 using the OpenAI client
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )

                response = completion.choices[0].message.content
                gpt_response_list.append({"filename": filename, "response": response})
                print(f"GPT-4 Response for {filename}:\n{response}\n")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

            # Delay to avoid rate limits
            time.sleep(20)

# Save GPT responses to a CSV file
output_path = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\output\test4.csv'
responses_df = pd.DataFrame(gpt_response_list)
responses_df.to_csv(output_path, index=False)
print(f"Responses saved to {output_path}")

