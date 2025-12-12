# om_api

Python client for the WHOS API.

## Installation


pip install om_api

## Usage

```bash
import om_api

client = om_api.WHOSClient(token="your-token")

# 00: Define the bounding box
constraints = om_api.Constraints(
    bbox=(60.347, 22.438, 60.714, 23.012)
)

# 01: Get features as Python objects
features = client.get_features(constraints)
for f in features:
    print(f.id, f.name, f.coordinates, f.contact_name)

# 02: Get observations as Python objects
feature_id = features[4].id
observations = client.get_observations(feature_id)
for obs in observations:
    print(obs.id, obs.observed_property, obs.uom)

# 03: Plot first observation
obs_with_data = client.get_observation_with_data(observations[0].id,
                                                 begin="2025-01-01T00:00:00Z",
                                                 end="2025-02-01T00:00:00Z")

if obs_with_data is not None:
    client.plot_observation(obs_with_data)
else:
    print("No observation data available for the requested time range.")
    
# Optional: only if want to print in the table
from tabulate import tabulate
# Optional: get feature and observations as DataFrame and print nicely
features_df = client.get_features_df(constraints)
print(tabulate(features_df, headers='keys', tablefmt='psql'))
observations_df = client.get_observations_df(feature_id)
print(tabulate(observations_df, headers='keys', tablefmt='psql'))


