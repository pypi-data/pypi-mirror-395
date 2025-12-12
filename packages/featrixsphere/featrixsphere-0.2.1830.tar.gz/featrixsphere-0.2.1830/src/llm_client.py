import requests
import json
import traceback

# Ollama server endpoint
OLLAMA_HOST = "http://taco.local:11434"
MODEL = "llama3.2"  # Change this to your preferred model


def ask_ollama(schema, prompt):
    """Send a prompt to the Ollama server and return the full response."""
    url = f"{OLLAMA_HOST}/api/chat"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": "mistral",  # Change model if needed
        "messages": [{"role": "user", "content": prompt}],
        "format": "json",
        "schema": schema,
        # "stream": True  # Enable streaming response
    }

    response_text = ""

    try:
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Raise an error if request fails
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        response_text += chunk.get("message", {}).get("content", "")  # Adjusted key
                    except json.JSONDecodeError:
                        traceback.print_exc()
                        pass  # Skip invalid JSON lines

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    response_text = response_text.strip()
    js = json.loads(response_text)
    return json.dumps(js, indent=4)
    return response_text

def ask_ollama_old(schema, prompt):
    """Send a prompt to the Ollama server and return the full response."""
    url = f"{OLLAMA_HOST}/api/chat"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        # "format": "json",
        # "schema": schema
        # "stream": False
    }

    # response = requests.post(url, headers=headers, json=payload)

    response_text = ""

    with requests.post(url, headers=headers, json=payload) as response:
        for line in response.iter_lines():
            # print(line)
            if line:
                try:
                    chunk = json.loads(line)
                    response_text += chunk.get("response", "")
                except json.JSONDecodeError:
                    traceback.print_exc()
                    pass  # Skip invalid JSON lines

    return response_text

# Example usage
if __name__ == "__main__":
    schema = {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "A concise, human-readable file name that accurately represents the file's contents."
            },
            "file_description": {
                "type": "string",
                "description": "A structured summary of the file's data, highlighting key attributes, categories, and potential use cases."
            },
        },
        "required": ["file_name", "file_description"]
    }

    question = """

    You are DataFileSummarizeGPT, an AI specialized in understanding and summarizing structured data.

    The text below represents sample rows from a CSV file. Your task is to:
    1. **Summarize the file contents** in a structured, informative way. Focus on key attributes, their significance, and the overall purpose of the dataset.
    2. **Propose a file name** that concisely reflects the file's contents.

    ### **Guidelines for Summarization**
    - Identify **key attributes** that help understand the data (e.g., customer information, transactions, product details, etc.).
    - Describe the **type of data**, its **purpose**, and any significant patterns.
    - Ensure the summary is **concise, clear, and jargon-free**, making it useful for researchers, analysts, and general users.

    ### **Guidelines for File Naming**
    - The file name should be **short, descriptive, and human-readable**.
    - Use **snake_case or kebab-case** (e.g., `customer_purchase_history.csv` or `customer-data-summary.csv`).
    - Avoid generic terms like "data", "file", or "info".

    Here is the data:

__typename,id,firstName,lastName,email,tags,provinceCode,zip,city,countryCodeV2,phone,createdAt,numberOfOrders,amount,currencyCode,lastOrderCreatedAt,rfm
Customer,628533461110,Joel,Tanner,joel@tikilandtrading.com,"['[TIMEZONE: America/Los_Angeles]' 'America/Los_Angeles' 'Survey'
 'TikiLandMugSocietyMember2023' 'TikiLandMugSocietyMember2023DELUXE'
 'TMS2023SHIRT' 'tms2023stillnoshirt' 'TMSKISS10']",CA,92651,Laguna Beach,US,+19494456414,2018-05-15 20:09:11,23,0.000,USD,2024-11-29 14:54:44,Loyal Customers
Customer,633126289526,nathan,Kranda,nkranda@aol.com,"['[TIMEZONE: America/Los_Angeles]' 'America/Los_Angeles' 'gender_male'
 'male']",CA,90740,Seal Beach,US,,2018-05-19 16:56:21,1,22.100,USD,2018-05-19 16:59:33,At Risk
Customer,633326862454,Seaira,Kovach,srkovach@gmail.com,"['[TIMEZONE: America/New_York]' 'America/New_York' 'gender_unknown'
 'unknown']",FL,32712,Apopka,US,(386) 341-5041,2018-05-19 21:03:48,4,367.000,USD,2020-11-17 19:22:33,At Risk
Customer,633347932278,Lisa,Weiss,laweiss888@gmail.com,"['[TIMEZONE: America/Los_Angeles]' 'America/Los_Angeles' 'female'
 'gender_female']",CA,92610,Foothill Ranch,US,+19494337053,2018-05-19 21:31:44,8,593.330,USD,2025-01-13 20:53:43,Loyal Customers
Customer,633356779638,Lisa,Weiss,angelelement444@aol.com,"['[TIMEZONE: America/Los_Angeles]' 'America/Los_Angeles' 'female'
 'gender_female']",CA,92610,Foothill Ranch,US,+19493052304,2018-05-19 21:44:54,9,816.240,USD,2024-08-31 11:57:06,Champions
"""

    answer = ask_ollama(schema, question)
    print("Ollama:", answer)


