from openai import OpenAI
import os
import time
import pandas as pd
import re

# Initialize the OpenAI client with the API key
client = OpenAI(api_key="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")

# Load the dataset
df = pd.read_excel(r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\PyT2\ZFINALLABELS_EXP3.xlsx')

# Define the directory containing the labeled Python files
directory = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\PyT2\Labeled_files'
gpt_response_list = []

# Clean and process the Bandit labels
df['Bandit'] = df['Bandit'].astype(str)
df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))
df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    filename = str(row['Filename'])
    banditLabels = str(row['Bandit'])
    semgrepLabels = str(row['Semgrep'])
    sonarLabels = str(row['Sonar'])

    # Combine labels and clean up NaN values
    labels = ",".join([banditLabels, semgrepLabels, sonarLabels]).replace(',nan', '').replace('nan,', '')
    print(f"Processing: {filename}")
    print(f"Labels: {labels}")

    # Extract CWE labels from tools
    labelsList = labels.split(',')
    listOfLabels = []
    for i in labelsList:
        if labels != 'nan':
            res = re.search(r'\(.*\)', i)
            if res:
                value = res.group(0)
                if value not in listOfLabels:
                    listOfLabels.append(value)
    print(f"Extracted Labels: {listOfLabels}")

    # Process the file content and send it to GPT-4
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            Vul_code = file.read()

            # Define the prompt
            prompt = f"""
            Which of the following vulnerabilities from the list of vulnerabilities exist in the Python code
            delimited with triple backticks? Also, provide the line of the vulnerability in the code.

            Python code: ```{Vul_code}```

            List of vulnerabilities: {", ".join(listOfLabels)}

            Format your response as a list of JSON objects with "label" and "line of Code" as the keys for each element.
            Only respond with JSON.
            """

            # Call GPT-4 using the OpenAI client
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )

                response = completion.choices[0].message.content
                gpt_response_list.append(response)
                print(f"GPT-4 Response for {filename}:\n{response}\n")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

            # Delay to avoid rate limits
            time.sleep(20)

# Add GPT responses to the DataFrame and save to Excel
df['gpt_perClass_response'] = gpt_response_list
output_path = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\PyT2\output\test3.xlsx'
with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, sheet_name='Experiment3')
    print(f"Responses saved to {output_path}")
