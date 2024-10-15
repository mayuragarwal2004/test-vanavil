import os
import requests

# Load the pull request diff (code changes)
with open("pr_diff.txt", "r") as file:
    pr_diff = file.read()

# Prepare the payload for the Perplexity API
payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": f"Review the following code diff:\n\n{pr_diff}"
        }
    ],
    "temperature": 0.2,
    "top_p": 0.9,
    "return_citations": False,
    "return_images": False,
    "return_related_questions": False,
    "stream": False
}

# Prepare headers for the API request
headers = {
    "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_TOKEN')}",  # Get API token from environment variable
    "Content-Type": "application/json"
}

# Send the request to Perplexity API
response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)

# Check if the response was successful
if response.status_code == 200:
    # Get the code review from the response
    review = response.json().get("choices", [{}])[0].get("content", "No response from Perplexity AI.")
else:
    review = f"Error: Unable to get a response from Perplexity AI. Status code: {response.status_code}"

# Output the review to a markdown file
with open("code_review.md", "w") as file:
    file.write(f"# Code Review\n\n{review}")
