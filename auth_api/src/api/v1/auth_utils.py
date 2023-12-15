from settings.config import OAuthYandexSettings
import requests


async def login_using_yandex(code) -> str:
    oauth_yandex = OAuthYandexSettings()

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': oauth_yandex.client_id,
        'client_secret': oauth_yandex.client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(
        oauth_yandex.token_url, headers=headers, data=data)

    token_data = response.json()
    yandex_access_token = token_data['access_token']

    headers = {'Authorization': f'OAuth {yandex_access_token}'}
    user_info = requests.get(
        oauth_yandex.user_info_url, headers=headers).json()

    email = user_info['default_email']
    return email
