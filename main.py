import requests
from requests.auth import HTTPBasicAuth
import json

# Azure DevOps configuration
ORGANIZATION = ""  
PROJECT = ""            
PAT = ""

# Base URL for Azure DevOps REST API
BASE_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/distributedtask/deploymentgroups"


def get_deployment_groups():
    url = f"{BASE_URL}?api-version=7.1"
    response = requests.get(url, auth=(HTTPBasicAuth('', PAT)))
    response.raise_for_status()
    return response.json().get("value", [])



def main():
    try:
        print("Fetching deployment groups...")
        deployment_groups = get_deployment_groups()

        for dg in deployment_groups:
             if "app" in dg["name"].lower():  # Case-insensitive match for "demo"
                dg_id = dg["id"]
                dg_name = dg["name"]
                print(f"Adding tag 'web' to shared deployment group: {dg_name} (ID: {dg_id})")

                def fetch_target_id():
                    url = f"{BASE_URL}/{dg_id}/targets?api-version=7.1"
                    response = requests.get(url, auth=(HTTPBasicAuth('', PAT)))
                    response.raise_for_status()
                    data = response.json()['value'][0]['id']
                    return data 
                
                target_id = fetch_target_id()
                
                def update_tags():
                    url = f"{BASE_URL}/{dg_id}/targets/{target_id}?api-version=7.1"
                    response = requests.get(url, auth=(HTTPBasicAuth('', PAT)))
                    response.raise_for_status()
                    data = response.json()
                    
                    
                    data['tags'] = ['APP-Specific-use']
                    
                    response = requests.patch(url, auth=(HTTPBasicAuth('', PAT)), json=data)
                    response.raise_for_status()
                    data = response.json()
                    print(data)

                update_tags()

        print("Tagging completed successfully.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()