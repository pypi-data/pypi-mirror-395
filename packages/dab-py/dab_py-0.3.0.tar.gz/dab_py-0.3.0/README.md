# DAB Pythonic Client (dab-py)
A Python client for DAB functionalities, including DAB Terms API and WHOS API.

## Installation (0.3.0)
Install the core package (lightweight, it includes Pandas):
```bash
pip install dab-py
```

## DAB Terms API
This repository contains a minimal client for retrieving controlled vocabulary terms (e.g., instruments) from the Blue-Cloud/GeoDAB service using a token and view.
### Features
- Retrieve terms from the DAB Terms API with a single call.
- Simple object model: Term and Terms containers.
- Small dependency footprint (requests).
### Usage
```bash
from dabpy import TermsAPI

def main():
    # Blue-Cloud/GeoDAB provided credentials for the public terms view
    token = "my-token"
    view = "blue-cloud-terms"

    # Desired parameters
    term_type = "instrument"
    max_terms = 10

    # Call the API. The implementation prints:
    # - Number of terms received from API: <n>
    # - A header line and up to `max_terms` items
    api = TermsAPI(token=token, view=view)
    api.get_terms(type=term_type, max=max_terms)

if __name__ == "__main__":
    main()

```

## WHOS API `om_api`
This notebook and module are used to programmatically access WHOS DAB functionalities through the OGC OM-JSON based API, which is documented and available for testing here: https://whos.geodab.eu/gs-service/om-api.
### Features
- Pythonic, **object-oriented access** via `Feature` and `Observation` classes. 
- Retrieve **features** and **observations** as Python objects.
- Convert API responses to **Pandas DataFrames** for analysis.
- Support for **bounding box constraints**.  
### Usage
```bash
from dabpy import *

# Replace with your WHOS API token and optional view
token = "my-token"
view = "whos"
client = WHOSClient(token=token, view=view)

# 00: Define the bounding box (Finland Example Area)
south, west, north, east = 60.347, 22.438, 60.714, 23.012
constraints = Constraints(bbox=(south, west, north, east))

# 01: Get Features as Python objects
features = client.get_features(constraints)
# 01b: (optinal: Convert Features to DataFrame if needed)
features_df = client.features_to_df(features)
print("\n=== Features Table ===")
print(features_df)

# 02: Get Observations as Python objects
feature_id = features[4].id
observations = client.get_observations(feature_id)
# 02b: (optinal: Convert Observations to DataFrame if needed)
observations_df = client.observations_to_df(observations)
print("\n=== Observations Table ===")
print(observations_df)

# 03: Get first observation with data points
obs_with_data = client.get_observation_with_data(observations[0].id, begin="2025-01-01T00:00:00Z", end="2025-02-01T00:00:00Z")
# 03b: (optinal: Convert Observation Points to DataFrame if needed)
if obs_with_data:
    obs_points_df = client.points_to_df(obs_with_data)
    print("\n=== Observation Points Table ===")
    print(obs_points_df)
else:
    print("No observation data available for the requested time range.")
```

