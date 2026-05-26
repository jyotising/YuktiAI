import requests
from config import RAINFOREST_API_KEY

def is_shopping_query(text):

    shopping_words = [
        "buy",
        "best",
        "price",
        "under",
        "amazon",
        "recommend",
        "laptop",
        "phone",
        "earbuds"
    ]

    text = text.lower()

    return any(
        word in text
        for word in shopping_words
    )

def search_amazon_products(query):

    url = "https://api.rainforestapi.com/request"

    params = {
        "api_key": RAINFOREST_API_KEY,
        "type": "search",
        "amazon_domain": "amazon.in",
        "search_term": query
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    products = []

    if "search_results" not in data:
        return []

    for item in data["search_results"][:5]:

        price_data = item.get("price")

        if isinstance(price_data, dict):
            price = price_data.get("raw", "N/A")
        else:
            price = "N/A"

        products.append({
            "title": item.get("title", "No title"),
            "price": price,
            "link": item.get("link", ""),
            "image": item.get("image", ""),
            "rating": item.get("rating", "N/A")
        })

    return products
