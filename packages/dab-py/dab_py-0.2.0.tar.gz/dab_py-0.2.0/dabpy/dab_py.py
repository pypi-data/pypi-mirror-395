import requests
import json

class Term:
  def __init__(self, count, value):
    self.count = count
    self.value = value

  def get_count(self) -> int:
    return self.count

  def get_value(self) -> str:
    return self.value


class Terms:
  def __init__(self):
    self.terms = []

  def get_terms(self) -> list:
    return self.terms

  def get_next_terms(self):
    return self.terms.pop()

  def get_next_terms(self, max):
    return self.terms[:max]



class TermsAPI:
  def __init__(self, token, view):
    self.token = token
    self.view = view

  def get_terms(self, type, max):
    terms = Terms()  # Initialize terms here
    url = "https://gs-service-preproduction.geodab.eu/gs-service/services/essi/token/{token}/view/{view}/terms-api/terms?type={type}&max={max}"
    request_url = url.format(token=self.token, view=self.view, type=type, max=max)
    response = requests.get(request_url)

    if response.status_code == 200:
      try:
          response_json = response.json()

          if 'terms' in response_json:
              for term_data in response_json['terms']:
                  if 'count' in term_data and 'value' in term_data:
                      term = Term(term_data['count'], term_data['value'])
                      terms.terms.append(term)
                  else:
                      print(f"Skipping term_data due to missing keys: {term_data}")

          print(f"Number of terms received from API: {len(terms.get_terms())}") 
          print()
          print("Terms from API (showing up to max):")
          # Modify the loop to print only up to 'max' terms
          for i, term in enumerate(terms.get_terms()):
              if i < max:
                  print(f"Value: {term.get_value()}, Count: {term.get_count()}")
              else:
                  break


      except json.JSONDecodeError:
          print("Error decoding JSON response.")
          print("Response text:", response.text)
    else:
        print(f"API request failed with status code: {response.status_code}")
        print("Response text:", response.text)

    return terms 