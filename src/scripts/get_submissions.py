import requests
from dotenv import load_dotenv
import os
from collections import defaultdict
from tqdm import tqdm
import csv

from tabulate import tabulate

# Load environment variables from .env file
env_path = "../../local/.env"
load_dotenv(dotenv_path=env_path)

# Get the session cookie value from the environment variable
session_cookie = os.getenv("NMDC_DATA_PORTAL_SESSION_COOKIE")

# Set the base URL of the API
base_url = "https://data.microbiomedata.org"
# "https://data-dev.microbiomedata.org"
# "https://data-sandbox.microbiomedata.org"
# "https://data.microbiomedata.org"

# Set the endpoint path for fetching metadata submissions
endpoint = "/api/metadata_submission"

# Set the query parameters for the request
params = {
    "limit": 100,  # Adjust the limit as needed
    "offset": 0
}

# Set the headers with the session cookie
headers = {
    "Cookie": f"session={session_cookie}"
}

# Initialize a dictionary to store the package name counts
package_name_counts = defaultdict(int)

# Get the total count of submissions
response = requests.get(base_url + endpoint, params={"limit": 1}, headers=headers)
total_count = response.json()["count"]

# Create a progress bar
progress_bar = tqdm(total=total_count, unit="submission")

# Fetch submissions in batches until all submissions are retrieved
while True:
    # Make the GET request to the API endpoint
    response = requests.get(base_url + endpoint, params=params, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        data = response.json()

        # Extract the documents from the response
        documents = data["results"]

        # Process the fetched documents
        for document in documents:
            # Access the packageName from metadata_submission
            package_name = document["metadata_submission"]["packageName"]
            package_name_counts[package_name] += 1

            # Update the progress bar
            progress_bar.update(1)

        # Check if there are more submissions to fetch
        if len(documents) < params["limit"]:
            break

        # Update the offset for the next batch
        params["offset"] += params["limit"]
    else:
        # Request failed
        print(f"Request failed with status code: {response.status_code}")
        break

# Close the progress bar
progress_bar.close()

# Prepare the data for tabulation
table_data = [[package_name, count] for package_name, count in package_name_counts.items()]
headers = ["Package Name", "Count"]

# Display the table
print(tabulate(table_data, headers, tablefmt="grid"))

# Save the package name counts as a TSV file
output_file = "package_name_counts.tsv"
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerow(["Package Name", "Count"])  # Write the header row
    for package_name, count in package_name_counts.items():
        writer.writerow([package_name, count])  # Write each row of data

print(f"Package name counts saved to {output_file}")
