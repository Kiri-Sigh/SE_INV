import requests

def refresh_access_token(refresh_token):
    # Request to refresh the access token
    response = requests.post('http://127.0.0.1:8000/api/token/refresh/', data={
        'refresh': refresh_token,
    })
    
    if response.status_code == 200:
        # Extract the new access token from the response
        new_access_token = response.json().get('access')
        return new_access_token
    else:
        raise Exception("Failed to refresh access token")

def make_api_request_with_retry(url, access_token, refresh_token, headers=None):
    # Set up headers, including the access token for authorization
    if headers is None:
        headers = {}
    headers['Authorization'] = f'Bearer {access_token}'
    
    # Make the initial request
    response = requests.get(url, headers=headers)
    
    # If the access token is invalid (401), refresh the token and retry the request
    if response.status_code == 401:
        print("Access token expired, refreshing token...")
        new_access_token = refresh_access_token(refresh_token)
        headers['Authorization'] = f'Bearer {new_access_token}'  # Update headers with the new token
        response = requests.get(url, headers=headers)
    
    return response




#example
# Example usage of the function to make an API request
# access_token = 'your_initial_access_token'
# refresh_token = 'your_refresh_token'

# url = 'https://yourapi.com/protected/resource/'

# # Make the API request with automatic retry if the access token expires
# response = make_api_request_with_retry(url, access_token, refresh_token)

# # Check if the request was successful
# if response.status_code == 200:
#     print("Request successful:", response.json())
# else:
#     print("Request failed:", response.status_code, response.text)
