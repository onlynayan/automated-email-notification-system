import requests

ACCESS_TOKEN = "paste_temporary_access_token_here"

url = "https://mail.zoho.com/api/accounts"
headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)
print(response.text)
