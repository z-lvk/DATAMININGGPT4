from openai import OpenAI
import os
import time

# Initialize the client with the OpenAI API key from an environment variable
client = OpenAI(api_key="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")

directory = r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\PyT1\Labeled_files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        with open(f, 'r') as file:
            Vul_code = file.read()
        
        # Define the prompt with triple backticks for Python code
        prompt = f"""
        You will be provided with Python code delimited by triple backticks.
        If it contains any security vulnerability, identify all the lines of vulnerable code and write only the line in quotation.
        If the code does not contain a vulnerability, then simply write "None."

        Python code: ```{Vul_code}```
        """
        
        # Call the API using the updated client syntax
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract and save the response
        print(completion.choices[0].message.content)
        response = completion.choices[0].message.content
        
        # Write the filename and response to the output CSV
        with open(r"C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\output/testTT.csv", "a") as output:
            s = response.replace('\n', ' ').strip()
            output.write(f"{filename},{s}\n")
        
        time.sleep(20)  # Delay to avoid rate limits
