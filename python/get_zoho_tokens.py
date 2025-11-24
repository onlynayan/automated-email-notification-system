import requests

# One-time script to exchange authorization code for access_token + refresh_token.
# Do NOT store real client_secret / code in GitHub – keep this local or load from env variables.

CLIENT_ID = "write_your_zoho_client_id_here"
CLIENT_SECRET = "write_your_zoho_client_secret_here"
REDIRECT_URI = "http://localhost:8080/"
AUTH_CODE = "paste_authorization_code_here_once"

url = "https://accounts.zoho.com/oauth/v2/token"

data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE,
}

response = requests.post(url, data=data)
print(response.text)