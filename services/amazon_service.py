import requests
from config import RAINFOREST_API_KEY


# ==========================================
# SHORT LINK FUNCTION
# ==========================================

def shorten_url(url):

    try:

        api = f"https://tinyurl.com/api-create.php?url={url}"

        response = requests.get(api)

        if response.status_code == 200:
            return response.text

        return url

    except:
        return url


# ==========================================
# DETECT SHOPPING QUERY
# ==========================================

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
        "smartphone",
        "earbuds",
        "headphones",
        "watch",
        "shoes"
    ]

    text = text.lower()

    return any(
        word in text
        for word in shopping_words
    )


# ==========================================
# SEARCH AMAZON PRODUCTS
# ==========================================

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

        # ==========================
        # PRICE
        # ==========================

        price_data = item.get("price")

        if isinstance(price_data, dict):
            price = price_data.get("raw", "N/A")
        else:
            price = "N/A"

        # ==========================
        # AMAZON AFFILIATE LINK
        # ==========================

        original_link = item.get("link", "")

        if "?" in original_link:
            affiliate_link = (
                original_link +
                "&tag=yuktiai-21"
            )
        else:
            affiliate_link = (
                original_link +
                "?tag=yuktiai-21"
            )

        # ==========================
        # SHORTEN LINK
        # ==========================

        short_link = shorten_url(
            affiliate_link
        )

        # ==========================
        # PRODUCT OBJECT
        # ==========================

        product = {
            "title": item.get(
                "title",
                "No title"
            ),

            "price": price,

            "link": short_link,

            "image": item.get(
                "image",
                ""
            ),

            "rating": item.get(
                "rating",
                "N/A"
            )
        }

        products.append(product)

    return products