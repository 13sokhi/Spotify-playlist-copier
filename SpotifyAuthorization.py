from config import base_authorization_url
from config import token_url
from SpotifyToken import SpotifyToken
import requests
import base64


def get_authorization_code(client_id: str, redirect_uri: str):
    url = base_authorization_url
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": "state"
    }
    param_tuple = tuple(params.items())
    url += "?"
    for i in range(len(params.items())):  # this loop will generate the URL that will take the user to authorization
        url += f"{param_tuple[i][0]}={param_tuple[i][1]}" if i == len(param_tuple) - 1 else f"{param_tuple[i][0]}={param_tuple[i][1]}&"

    print(f"\nGo to this URL to provide authorization: {url}")
    authorization_code = input("\nEnter the Authorization code from directed URL: ")
    return authorization_code

def get_token(client_id: str, client_secret: str, authorization_code: str, redirect_uri: str) -> SpotifyToken:
    params = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    id_secret = f"{client_id}:{client_secret}"
    base64_id_secret = str(base64.b64encode(id_secret.encode('utf-8')), 'utf-8')  # we need base64 encode string of format <client_id:client_secret>
    header = {
        "Authorization": f"Basic {base64_id_secret}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url=token_url, params=params, headers=header).json()
    access_token = response['access_token']
    expires_in = response['expires_in']
    refresh_token = response['refresh_token']
    return SpotifyToken(access_token=access_token, expires_in=expires_in, refresh_token=refresh_token)

# method refreshes access token
# new access token is given without a new refresh token
# so same refresh token remains valid for next use
def refresh_token(client_id: str, client_secret: str, refresh_token: str) -> SpotifyToken: # token is the one that needs to be refreshed
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    id_secret = f"{client_id}:{client_secret}"
    base64_id_secret = str(base64.b64encode(id_secret.encode('utf-8')), 'utf-8')  # we need base64 encode string of format <client_id:client_secret>
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64_id_secret}'
    }
    response = requests.post(url='https://accounts.spotify.com/api/token', headers=header, params=params).json()
    access_token = response['access_token']
    expires_in = response['expires_in']
    ref_token = response.get('refresh_token', refresh_token) # this dictionary method returns the specified key, the default value is returned (2nd parameter) if key is absent in dictionary
    return SpotifyToken(access_token=access_token, expires_in=expires_in, refresh_token=ref_token)