import requests
import pandas as pd
import urllib.parse

def obfuscate_token(url, token):
    """Replace the token in a URL with '***' for safe printing."""
    return url.replace(token, "***")

class Feature:
    """Python representation of a WHOS feature."""
    def __init__(self, feature_json):
        self.id = feature_json["id"]
        self.name = feature_json["name"]
        self.coordinates = feature_json["shape"]["coordinates"]
        self.parameters = {param["name"]: param["value"] for param in feature_json["parameter"]}
        self.related_party = feature_json.get("relatedParty", [])

        if self.related_party:
            self.contact_name = self.related_party[0].get("individualName", "")
            self.contact_email = self.related_party[0].get("electronicMailAddress", "")
        else:
            self.contact_name = ""
            self.contact_email = ""

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Coordinates": f"{self.coordinates[0]}, {self.coordinates[1]}",
            "Source": self.parameters.get("source", ""),
            "Identifier": self.parameters.get("identifier", ""),
            "Contact Name": self.contact_name,
            "Contact Email": self.contact_email
        }

    def __repr__(self):
        return f"<Feature id={self.id} name={self.name}>"

class Observation:
    """Python representation of a WHOS observation."""
    def __init__(self, obs_json):
        params = {param["name"]: param["value"] for param in obs_json.get("parameter", [])}
        self.id = obs_json["id"]
        self.type = obs_json.get("type")
        self.source = params.get("source")
        self.observed_property_definition = params.get("observedPropertyDefinition")
        self.original_observed_property = params.get("originalObservedProperty")
        self.observed_property = obs_json.get("observedProperty", {}).get("title")
        self.phenomenon_time_begin = obs_json.get("phenomenonTime", {}).get("begin")
        self.phenomenon_time_end = obs_json.get("phenomenonTime", {}).get("end")
        self.feature_of_interest_href = obs_json.get("featureOfInterest", {}).get("href")
        result_meta = obs_json.get("result", {}).get("defaultPointMetadata", {})
        self.uom = result_meta.get("uom")
        self.interpolation_type = result_meta.get("interpolationType", {}).get("title")
        self.points = obs_json.get("result", {}).get("points", [])

    def to_dict(self):
        return {
            "ID": self.id,
            "Source": self.source,
            "Observed Property Definition": self.observed_property_definition,
            "Original Observed Property": self.original_observed_property,
            "Observed Property": self.observed_property,
            "Phenomenon Time Begin": self.phenomenon_time_begin,
            "Phenomenon Time End": self.phenomenon_time_end,
            "Feature of Interest Href": self.feature_of_interest_href,
            "Observation Type": self.type,
            "Unit of Measurement": self.uom,
            "Interpolation Type": self.interpolation_type
        }

    def __repr__(self):
        return f"<Observation id={self.id} property={self.observed_property}>"

class WHOSClient:
    """WHOS API client to retrieve features and observations as Python objects or Pandas DataFrame."""
    def __init__(self, token, view="whos"):
        self.token = token
        self.view = view
        self.base_url = f"https://whos.geodab.eu/gs-service/services/essi/token/{token}/view/{view}/om-api/"

    # --- Retrieve features / observations as objects ---
    def get_features(self, constraints):
        url = self.base_url + "features?" + constraints.to_query()
        print("Retrieving " + obfuscate_token(url, self.token))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"HTTP GET failed: {response.status_code}")
        data = response.json()
        if "results" not in data:
            return []
        return [Feature(f) for f in data["results"]]

    def get_observations(self, feature_id):
        if not feature_id:
            raise ValueError("feature_id must be provided")
        url = self.base_url + "observations?feature=" + feature_id
        print("Retrieving " + obfuscate_token(url, self.token))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"HTTP GET failed: {response.status_code}")
        data = response.json()
        if "member" not in data:
            return []
        return [Observation(obs) for obs in data["member"]]

    def get_observation_with_data(self, observation_id, begin=None, end=None):
        url = self.base_url + f"observations?includeData=true&observationIdentifier={urllib.parse.quote(observation_id)}"
        if begin:
            url += "&beginPosition=" + urllib.parse.quote(begin)
        if end:
            url += "&endPosition=" + urllib.parse.quote(end)

        print("Retrieving " + obfuscate_token(url, self.token))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"HTTP GET failed: {response.status_code}")
        data = response.json()
        if "member" not in data or not data["member"]:
            return None
        return Observation(data["member"][0])

    # --- Convert existing objects to DataFrame without calling API ---
    def features_to_df(self, features):
        dict_list = [f.to_dict() for f in features]
        return pd.DataFrame(dict_list)

    def observations_to_df(self, observations):
        dict_list = [obs.to_dict() for obs in observations]
        return pd.DataFrame(dict_list)

    def points_to_df(self, observation):
        """Convert Observation points to a DataFrame with proper Time and Value columns."""
        if not observation.points:
            return pd.DataFrame(columns=["Time", "Value"])

        dict_list = []
        for p in observation.points:
            time = p.get("time", {}).get("instant")  # Extract 'instant' from 'time' dict
            value = p.get("value")
            dict_list.append({"Time": time, "Value": value})

        return pd.DataFrame(dict_list)