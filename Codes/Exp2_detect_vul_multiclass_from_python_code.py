from openai import OpenAI
import os
import time

# Initialize the client with the OpenAI API key
client = OpenAI(api_key="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")

# Define the list of vulnerabilities (CWEs) to check for
labels3 = [
    "CWE-379", "CWE-384", "CWE-385", "CWE-400", "CWE-406", "CWE-414", "CWE-425",
    "CWE-434", "CWE-454", "CWE-462", "CWE-477", "CWE-488", "CWE-502", "CWE-521",
    "CWE-522", "CWE-595", "CWE-601", "CWE-605", "CWE-611", "CWE-641", "CWE-643",
    "CWE-703", "CWE-730", "CWE-732", "CWE-759", "CWE-760", "CWE-776", "CWE-798",
    "CWE-827", "CWE-835", "CWE-841", "CWE-918", "CWE-941", "CWE-943", "CWE-352",
    "CWE-409", "CWE-266", "CWE-311", "CWE-315", "CWE-1240", "CWE-79", "CWE-489",
    "CWE-78", "CWE-94", "CWE-15", "CWE-22", "CWE-89", "CWE-1004", "CWE-614",
    "CWE-95", "CWE-20", "CWE-80", "CWE-90", "CWE-99", "CWE-113", "CWE-116",
    "CWE-117", "CWE-1204", "CWE-193", "CWE-200", "CWE-209", "CWE-215", "CWE-250",
    "CWE-252", "CWE-259", "CWE-269", "CWE-283", "CWE-284", "CWE-285", "CWE-295",
    "CWE-297", "CWE-306", "CWE-312", "CWE-319", "CWE-321", "CWE-326", "CWE-327",
    "CWE-329", "CWE-330", "CWE-331", "CWE-339", "CWE-347", "CWE-367", "CWE-377"
]

# Define the directory containing the dataset files
directory = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\Labeled_files'

# Iterate through all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Check if it is a file
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            Vul_code = file.read()

        # Define the prompt for Experiment 2
        prompt = f"""
        You will be provided with Python code delimited by triple backticks.
        Identify if any of the following vulnerabilities exist in the code. 
        Also, provide the line of the vulnerability in the code.

        Python code: ```{Vul_code}```

        List of vulnerabilities: {", ".join(labels3)}

        Format your response as a list of JSON objects with:
        "label" and "line of Code" as the keys for each element.
        Only respond with JSON.
        """
        
        # Call the API using the updated client syntax for GPT-4
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract and save the response
            response = completion.choices[0].message.content
            print(f"Processing {filename}:\n{response}\n")

            # Save the response to a CSV file
            with open(r"C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\output\test2.csv", "a") as output:
                formatted_response = response.replace('\n', ' ').strip()
                output.write(f"{filename},{formatted_response}\n")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
        
        # Delay to avoid rate limits
        time.sleep(20)





