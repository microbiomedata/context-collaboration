import requests
import pandas as pd
from tqdm import tqdm


def get_all_biosamples(base_url, collection_name):
    endpoint = f"{base_url}/nmdcschema/{collection_name}"
    biosamples = []
    page_token = None
    first_iteration = True
    progress_bar = None

    try:
        while True:
            params = {
                "max_page_size": 100,
                "page_token": page_token
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Initialize or update progress bar upon receiving total count
            if first_iteration:
                total_count = data.get('total_count', 0)
                progress_bar = tqdm(total=total_count)
                first_iteration = False

            current_page_samples = data.get('resources', [])
            biosamples.extend(current_page_samples)
            progress_bar.update(len(current_page_samples))

            page_token = data.get('next_page_token')
            if not page_token:
                break
    finally:
        if progress_bar is not None:
            progress_bar.close()

    return biosamples


def count_env_package_values(biosamples):
    df = pd.DataFrame(biosamples)
    if 'env_package' in df.columns:
        df['env_package_value'] = df['env_package'].apply(
            lambda x: x.get('has_raw_value') if isinstance(x, dict) else None)
        value_counts = df['env_package_value'].value_counts()
    else:
        value_counts = pd.Series([])

    return value_counts


# API Base URL
api_base_url = "https://api.microbiomedata.org"

# Collection name for biosamples
biosample_collection = "biosample_set"

# Fetch all biosamples
all_biosamples = get_all_biosamples(api_base_url, biosample_collection)

# Count env_package.has_raw_value values
env_package_counts = count_env_package_values(all_biosamples)
print("Count of env_package.has_raw_value values:")
print(env_package_counts)
