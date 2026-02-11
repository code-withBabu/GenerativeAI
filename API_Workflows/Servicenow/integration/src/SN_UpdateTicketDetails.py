#import requests library to make HTTP requests
import requests

# Eg. User name="admin", Password="admin" for this code sample.
user = 'admin'
userid = 'dev251560'    
#retrieving the password from the .env file
from dotenv import load_dotenv
import os
load_dotenv()
pwd = os.getenv("API_Secret")

#update the ticket details based on the ticket number provided by the user. Eg. RITM0000002

def update_ticket_details(systemid, short_description):
    # Set the request parameters
    url = f'https://{userid}.service-now.com/api/now/table/sc_req_item/{systemid}'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data=f'{{"short_description":"{short_description}"}}')

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    else:
        print('Request was successful. Status Code:', response.status_code)
    return response.json()

def update_ticket_status(systemid, statenumber,notes):
    # Set the request parameters
    url = f'https://{userid}.service-now.com/api/now/table/sc_req_item/{systemid}'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data=f'{{"state":"{statenumber}","work_notes":"{notes}"}}')

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    else:
        print('Request was successful. Status Code:', response.status_code)
    return response.json()

# json_response = update_ticket_details('18779506eb43011008f2951ff152283a', 'Request for Mobile Phone')
json_response = update_ticket_status('18779506eb43011008f2951ff152283a', 3, 'Ticket is being processed.')
    
#Extracting the required fields from the response
# if 'result' in json_response and len(json_response['result']) > 0:
#     result = json_response['result']  
#     short_description = result.get('short_description', 'N/A')
#     print(f"Short Description: {short_description}")
# else:
#     print("No results found for the given ticket number.")
if 'result' in json_response and len(json_response['result']) > 0:
    result = json_response['result']  
    closingnotes = result.get('work_notes', 'N/A')
    print(f"Closing Notes: {closingnotes}")
else:
    print("No results found for the given ticket number.")
