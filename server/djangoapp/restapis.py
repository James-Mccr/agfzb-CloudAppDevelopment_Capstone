import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        try:
            api_key = kwargs["api_key"]
        except:
            api_key = None

        if api_key is not None:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["language"] = kwargs["language"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
                                    
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    return requests.post(url, params=kwargs, json=json_payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"], state=dealer["state"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealer_id)
    if json_result:
        reviews = json_result
        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                    review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                    car_model=review["car_model"], car_year=review["car_year"], sentiment=sentiment, id=review["id"])
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    json_result = get_request("https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/00e40646-1413-4ce0-a556-ea0b7df735b1/v1/analyze", text=text, version="2022-04-07", features=["sentiment"], return_analyzed_text=False, api_key="tqE6MlvFLJuKW4cdkzGV0Xo9NzJgni8D3-n97SzLZOVI", language="en")
    return json_result["sentiment"]["document"]["label"]



