import requests
import csv

# Define the endpoint URL
url = "https://reqres.in/api/users"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the list of users
    users = data.get('data', [])
    
    # Define the CSV file name
    csv_file = 'users_data.csv'
    
    # Write data to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Avatar'])
        
        # Write the user data
        for user in users:
            writer.writerow([user['id'], user['first_name'], user['last_name'], user['email'], user['avatar']])
    
    print(f"Data has been saved to {csv_file}")
else:
    print("Failed to retrieve data:", response.status_code)
