import requests
import json
import re


def fetch_ts_file(url):
    """ Fetch TypeScript file content from the provided URL """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return str(e)


def parse_harmonizer_templates(ts_code):
    """ Parse HARMONIZER_TEMPLATES from TypeScript code to a Python dictionary """
    # Remove TypeScript type annotations, comments, and 'export' keyword
    cleaned_code = re.sub(r"export\s+const\s+HARMONIZER_TEMPLATES\s*:\s*Record<string,\s*HarmonizerTemplateInfo>\s*=",
                          '', ts_code)
    cleaned_code = re.sub(r'//.*?$', '', cleaned_code, flags=re.MULTILINE)
    cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)

    # Extract the JSON-like dictionary string using regex that handles nested curly braces
    match = re.search(r"(\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\});", cleaned_code, re.DOTALL)
    if match:
        json_like_str = match.group(1)
        # Properly quote the keys, handle computed properties like [EMSL]
        json_like_str = re.sub(r'(\w+)\s*:', r'"\1":', json_like_str)
        json_like_str = json_like_str.replace("[EMSL]", '"EMSL"')
        json_like_str = json_like_str.replace("[JGI_MG]", '"JGI_MG"')
        json_like_str = json_like_str.replace("[JGI_MG_LR]", '"JGI_MG_LR"')
        json_like_str = json_like_str.replace("[JGT_MT]", '"JGT_MT"')
        # Replace single quotes with double quotes for JSON compatibility
        json_like_str = json_like_str.replace("'", '"')

        try:
            # Convert the string to a Python dictionary
            return json.loads(json_like_str)
        except json.JSONDecodeError as e:
            return f"Failed to parse JSON: {str(e)}"
    return "HARMONIZER_TEMPLATES constant not found."


# URL of the TypeScript file
url = "https://raw.githubusercontent.com/microbiomedata/nmdc-server/04165f8ed226c8ae8df5da5ac6be2f3a517ca15e/web/src/views/SubmissionPortal/harmonizerApi.ts"

# Fetch TypeScript file content
ts_content = fetch_ts_file(url)

# Parse the HARMONIZER_TEMPLATES constant
templates_dict = parse_harmonizer_templates(ts_content)
print(templates_dict)
