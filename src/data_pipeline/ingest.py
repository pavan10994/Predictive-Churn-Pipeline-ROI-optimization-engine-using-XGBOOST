import os
import zipfile

# 1. Set your Kaggle credentials here BEFORE importing KaggleApi
os.environ['KAGGLE_USERNAME'] = 'Pavan_12345'
os.environ['KAGGLE_KEY'] = 'KGAT_72a6220c06e89b59703221191e8cb376'

# 2. Now import the Kaggle API
from kaggle.api.kaggle_api_extended import KaggleApi

def download_data():
    print("Connecting to Kaggle...")
    api = KaggleApi()
    api.authenticate()
    
    # This is the exact Kaggle path for the IBM Telco dataset
    dataset = "blastchar/telco-customer-churn"
    download_folder = "data/raw"
    zip_path = os.path.join(download_folder, "telco-customer-churn.zip")
    
    print("Downloading dataset...")
    api.dataset_download_files(dataset, path=download_folder, unzip=False)
    
    print("Extracting files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(download_folder)
        
    # Delete the zip file to keep things clean
    os.remove(zip_path)
    print(f"Success! Data saved to {download_folder}")

if __name__ == "__main__":
    download_data()