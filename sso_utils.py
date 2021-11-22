import webbrowser

from requests_oauthlib import OAuth2Session

CLIENT_ID = '####'
CLIENT_SECRET = '####'


def oauth_session():
    oauth = OAuth2Session(
        CLIENT_ID,
        redirect_uri='https://localhost/callback/',
        scope=[
            'publicData',
            'esi-skills.read_skills.v1',
            'esi-wallet.read_character_wallet.v1',
            'esi-ui.open_window.v1',
            'esi-markets.structure_markets.v1',
        ]
    )

    auth_url, state = oauth.authorization_url('https://login.eveonline.com/oauth/authorize')
    webbrowser.open(auth_url)

    auth_response = input('Enter the callback URL > ')

    oauth.fetch_token(
        'https://login.eveonline.com/oauth/token',
        authorization_response=auth_response,
        client_secret=CLIENT_SECRET
    )

    return oauth


def get_character(session):
    if not session:
        return None

    res = session.get('https://login.eveonline.com/oauth/verify')
    return res.json()['CharacterName']


if __name__ == '__main__':
    session = oauth_session()
    print(f"Logged in as {get_character(session)}!")
