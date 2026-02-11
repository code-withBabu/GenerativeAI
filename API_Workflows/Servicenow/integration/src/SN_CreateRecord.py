#This script will create a record from a specified ServiceNow table using the ServiceNow REST API.

import requests

# Eg. User name="admin", Password="admin" for this code sample.
user = 'admin'
userid = 'dev251560'    
#retrieving the password from the .env file
from dotenv import load_dotenv
import os
load_dotenv()
pwd = os.getenv("API_Secret")

def createrecord(short_description,urgency):
    # Set the request parameters
    # url = f'https://{userid}.service-now.com/api/now/table/sc_req_item/{systemid}'
    url = url = f'https://{userid}.service-now.com/api/now/table/sc_req_item?sysparm_fields=short_description&short_description={short_description}'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    # response = requests.patch(url, auth=(user, pwd), headers=headers ,data=f'{{"short_description":"{short_description}"}}')
    response = requests.post(url, auth=(user, pwd), headers=headers ,data=f'{{"short_description":"{short_description}","urgency":"{urgency}"}}')
    # Check for HTTP codes other than 201
    if response.status_code != 201: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    else:
        print('Request was successful and record created. Status Code:', response.status_code)
    return response.json()

json_response = createrecord('Request for High End Laptop', '1')

#Extracting the required fields from the response
if 'result' in json_response and len(json_response['result']) > 0:
    result = json_response['result']  
    short_description = result.get('short_description', 'N/A')
    print(f"Short Description: {short_description}")