from Common_Modual.common_functionality import *
from pymongo import MongoClient
import os
from datetime import datetime


obj = RequestsManager()

website = "jet2holidays"
# region = ""
today = datetime.today().strftime("%Y_%m_%d")

conn = MongoClient("mongodb://localhost:27017/")
db = conn[f"Xwiz_Jet2holidays"]

# search_data = db[f'Search_Data_{today}']
search_data = db[f'BA_inputs']
# static_search = db[f'Static_Data_{today}']
product_data = db[f'Product_Data_{today}']

# Use url or another identifier instead of ProductCode
# search_data.create_index("url", unique=True)
# static_search.create_index("url", unique=True)
# search_data.create_index("variant_id", unique=True)
# product_data.create_index("Website Hotel ID", unique=True)
# main_data.create_index("Package_id", unique=True)




# Base path
base_path = f"d:\\jet2holidays_more\\Crawl_Data_Collection\\{website}\\{today}\\{website}"

# Define paths for different file types
html_path = os.path.join(base_path, "Data_Files", "HTML_Files")
excel_path = os.path.join(base_path, "Data_Files", "Excel_Files")

# Create directories
os.makedirs(html_path, exist_ok=True)
os.makedirs(excel_path, exist_ok=True)

print(f"HTML files path: {html_path}")
print(f"Excel files path: {excel_path}")
def generate_hash_id(*args):
    hash_input = "|".join(str(a) for a in args)
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

# current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

proxy = "http://592bad980b59a17a0c900e1e055ca7bd26166239:@api.zenrows.com:8001"
zen_proxies = {"http": proxy, "https": proxy}
