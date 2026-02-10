#This script retrieves the details of a ServiceNow ticket based on the ticket number provided by the user. It uses the ServiceNow REST API to fetch the ticket information and displays specific fields such as the ticket number, stage, system ID, and creation date. The script also handles authentication using credentials stored in environment variables and checks for successful API responses.

#easy_install requests
import requests

# Eg. User name="admin", Password="admin" for this code sample.
user = 'admin'
userid = 'dev251560'
#retrieving the password from the .env file
from dotenv import load_dotenv
import os   
load_dotenv()
pwd = os.getenv("API_Secret")

#get the ticket details from the user Eg. RITM0000002
ticket_number = input("Enter the ticket number (e.g., RITM0000002): ")

# Set the request parameters
url = f'https://{userid}.service-now.com/api/now/table/sc_req_item?sysparm_query=number%3D{ticket_number}&sysparm_limit=10'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()
else:
    print('Request was successful. Status Code:', response.status_code)

# Decode the JSON response into a dictionary and use the data
data = response.json()

#Extracting the required fields from the response
if 'result' in data and len(data['result']) > 0:
    result = data['result'][0]  
    number = result.get('number', 'N/A')
    stage = result.get('stage', 'N/A')
    sysid = result.get('sys_id', 'N/A')
    sys_created_on = result.get('sys_created_on', 'N/A')

    print(f"Ticket Number: {number}")
    print(f"Stage: {stage}")
    print(f"System ID: {sysid}")
    print(f"Created On: {sys_created_on}")
else:
    print("No results found for the given ticket number.")