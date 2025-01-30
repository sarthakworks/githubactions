from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import re

def get_file_content(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""  # Handle file not found gracefully

if __name__ == "__main__":
    model_path = './deepseek-r1/deepseek-coder-1.3b-base'  # Or your actual path
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto') # Use CUDA if available
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1) # Exit if model loading fails

    files_to_review = []
    with open('changed_files.txt', 'r') as f:
        files_to_review = f.read().splitlines()

    all_reviews = []

    for file in files_to_review:
        try:
            code = get_file_content(file)

            inputs = tokenizer(f'''
Review the following Python code for optimization opportunities, including performance, memory usage, and algorithmic complexity. Be specific and provide actionable suggestions. Format your output with bullet points for each suggestion, including the file name and line number if applicable. If no issues are found, say "No issues found in {file}".

```python
{code}
```''', return_tensors='pt').to('cuda')  # Use CUDA if available

            outputs = model.generate(**inputs, max_new_tokens=1024)  # Increased max_new_tokens
            review_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

            review_output += f'\n\nStatic Analysis Results for {file}:\n'
            review_output += f'Pylint:\n{get_file_content(f"{file}.pylint")}\n'
            review_output += f'Flake8:\n{get_file_content(f"{file}.flake8")}\n'
            review_output += f'Mypy:\n{get_file_content(f"{file}.mypy")}\n'

            all_reviews.append(f"**{file}**: \n{review_output}")

        except Exception as e:
            all_reviews.append(f"Error reviewing {file}: {e}")

    full_review = '\n\n'.join(all_reviews)
    print(full_review)  # Print to console for debugging

    with open('review_output.txt', 'w') as f:
        f.write(full_review)