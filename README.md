ProductAssistant is a Python-based application that leverages Google Cloud’s Vertex AI for image recognition to identify products from user-uploaded images. It then fetches relevant product data from Amazon using the Real-Time Amazon Data API via RapidAPI, stores the data in Google BigQuery for further analysis, and provides interactive visualizations using Looker Studio. Additionally, the project integrates a chatbot to help users filter and query product information dynamically.

Table of Contents
Features
Demo
Technology Stack
Prerequisites
BigQuery Setup
Data Visualization

Features
Image Upload & Recognition: Users can upload images, and Vertex AI generates descriptive captions.
Amazon Product Search: Fetches real-time product data from Amazon based on image captions.
Data Storage: Stores structured product data in Google BigQuery for scalable storage and querying.
Data Visualization: Visualizes product data using Looker Studio for insightful analytics.

Demo

<img width="585" alt="Screenshot 2025-01-27 at 3 25 05 PM" src="https://github.com/user-attachments/assets/e3d4fcd1-718f-49c3-ba78-a9fe120ab742" />

Selecting an image of a product 



Amazon API fetched data and pushes into bigquery 

<img width="1408" alt="Screenshot 2025-01-27 at 3 26 57 PM" src="https://github.com/user-attachments/assets/45c4e9e2-484c-41b4-8973-81cab0e95c3d" />

The results can be viewed and analysed using google looker studio

<img width="942" alt="Screenshot 2025-01-27 at 3 27 25 PM" src="https://github.com/user-attachments/assets/e1350618-76be-4c24-9df3-f892b09d44bd" />



Technology Stack
Programming Language: Python 3.12
Cloud Services:
Google Vertex AI for image recognition
Google BigQuery for data storage
Looker Studio for data visualization
APIs:
Real-Time Amazon Data API via RapidAPI
Libraries:
vertexai
google-cloud-bigquery
tkinter for GUI
http.client, urllib.parse, json, ssl for API interactions
Prerequisites
Before you begin, ensure you have met the following requirements:
Python 3.12 installed on your machine. You can download it from here.
A Google Cloud Platform (GCP) account with:
Vertex AI and BigQuery APIs enabled.
A service account with appropriate permissions (e.g., BigQuery Data Editor, Vertex AI User).
A RapidAPI account with access to the Real-Time Amazon Data API.
Git installed for version control.
GitHub account for repository hosting.
BigQuery Setup
1. Create a Dataset and Table
Create a Dataset
In the BigQuery Console, click Create Dataset.
Dataset ID: my_dataset
Data Location: US (or your preferred location)
Click Create Dataset.
Create a Table
Within my_dataset, click Create Table.
Source: Select Empty table.
Table ID: amazon_products
Schema: Define the following fields:
Field Name
Type
Description
product_title
STRING
Title of the product
product_price
FLOAT
Price of the product (e.g., 19.99)
product_star_rating
FLOAT
Average star rating
product_num_ratings
INT64
Number of ratings
product_url
STRING
URL to the Amazon product
product_image
STRING
URL to the product image


Click Create Table.
2. Verify the Table
After creation, you should see the amazon_products table with the defined schema.
Your Python script will now insert data into this table.
Data Visualization
Set Up Looker Studio
Go to Looker Studio.
Click Create > Data Source.
Select BigQuery.
Authorize access and select your project, dataset (my_dataset), and table (amazon_products).
Click Connect.
Create a Report
After connecting, click Create Report.
Add charts, tables, and filters as desired.
Examples:
Bar Chart: Average product price by category.
Table: List of products with ratings and prices.
Filter Control: Filter products by product_type or price range.





