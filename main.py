import os
import http.client
import urllib.parse
import json
import ssl
import tkinter as tk
from tkinter import filedialog
from google.cloud import bigquery

# Vertex AI imports
import vertexai
from vertexai.preview.vision_models import Image as VertexImage
from vertexai.preview.vision_models import ImageTextModel

# Replace with your actual GCP project ID and region
PROJECT_ID = ("project_id")
LOCATION = "us-central1"


def upload_to_bigquery(parsed_products):
    """
    Inserts product rows into a BigQuery table.
    Assumes the table schema is:
        product_title:STRING,
        product_price:FLOAT,
        product_star_rating:FLOAT,
        product_num_ratings:INT64,
        product_url:STRING
    """
    client = bigquery.Client()

    # Table ID in the format: "project_id.dataset_name.table_name"
    table_id = f"{PROJECT_ID}.my_dataset.amazon_products"

    # Insert rows into BigQuery
    errors = client.insert_rows_json(table_id, parsed_products)
    if errors:
        print("Encountered errors while inserting rows:", errors)
    else:
        print("New rows have been added to BigQuery.")


def analyze_image_with_vertex_ai(image_path):
    """
    Uses Vertex AI's Image-to-Text model ("imagetext@001") to caption an image.
    Returns a string combined from the top captions (e.g., "a pair of headphones on a desk").
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = ImageTextModel.from_pretrained("imagetext@001")

    source_img = VertexImage.load_from_file(location=image_path)
    captions = model.get_captions(
        image=source_img,
        language="en",
        number_of_results=2
    )
    print("The model returned these captions:", captions)
    query = " ".join(captions)
    return query


def main():
    # 1. Select an image file via Tkinter
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if not image_path:
        print("No file selected. Exiting.")
        return

    # 2. Get caption from Vertex AI
    vertex_query = analyze_image_with_vertex_ai(image_path)
    print(f"[DEBUG] Vertex AI caption combined into query: {vertex_query}")

    # 3. Search the Amazon Data API
    encoded_query = urllib.parse.quote_plus(vertex_query)
    ssl_context = ssl._create_unverified_context()  # optional
    conn = http.client.HTTPSConnection(
        "real-time-amazon-data.p.rapidapi.com",
        context=ssl_context
    )
    headers = {
        'x-rapidapi-key': "rapid_api_key",  # Replace with your actual RapidAPI key
        'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
    }
    endpoint = (
        f"/search?query={encoded_query}"
        "&page=1"
        "&country=US"
        "&sort_by=RELEVANCE"
        "&product_condition=ALL"
        "&is_prime=false"
        "&deals_and_discounts=NONE"
    )
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()

    try:
        json_data = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response.")
        conn.close()
        return

    print("Raw JSON response:")
    print(json.dumps(json_data, indent=2))

    # 4. Parse product data into a list of dictionaries
    #    We'll extract five fields: product_title, product_price, product_star_rating,
    #    product_num_ratings, product_url
    products = json_data["data"].get("products", [])
    parsed_products = []
    for p in products:
        title = p.get("product_title", None)
        url = p.get("product_url", None)
        star_str = p.get("product_star_rating", None)  # e.g. "4.3"
        num_ratings = p.get("product_num_ratings", 0)
        price_str = p.get("product_price", None)  # e.g. "$16.95"
        img = p.get("product_photo",None)
        # Convert star rating to float
        try:
            star_val = float(star_str) if star_str else None
        except ValueError:
            star_val = None

        # Convert price to float (remove leading "$")
        if price_str and price_str.startswith("$"):
            price_str = price_str.replace("$", "")
        try:
            price_val = float(price_str) if price_str else None
        except ValueError:
            price_val = None

        product_dict = {
            "product_title": title,
            "product_price": price_val,
            "product_star_rating": star_val,
            "product_num_ratings": num_ratings,
            "product_url": url,
            "product_image": img
        }
        parsed_products.append(product_dict)

    conn.close()

    # 5. Insert the parsed data into BigQuery
    if parsed_products:
        upload_to_bigquery(parsed_products)
    else:
        print("No products to upload.")


if __name__ == "__main__":
    main()
