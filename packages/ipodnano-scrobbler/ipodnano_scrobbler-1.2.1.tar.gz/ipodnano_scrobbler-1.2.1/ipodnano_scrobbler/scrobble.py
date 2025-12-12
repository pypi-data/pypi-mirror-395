# Last.fm Syncing Tool
# Lean, fast, and functional
import os
import time
import requests
import hashlib
from pathlib import Path

api_head = 'http://ws.audioscrobbler.com/2.0/'

def get_config_folder():
    home = Path.home()
    config_folder = home / ".config" / "ipodnano-scrobbler"
    config_folder.mkdir(exist_ok=True)
    apikey_folder = config_folder / "apikey" 
    apikey_folder.mkdir(exist_ok=True)
    return config_folder, apikey_folder

def hashRequest(obj, secretKey):
    string = ''
    items = obj.keys()
    items = sorted(items)
    for i in items:
        string += i
        string += obj[i]
    string += secretKey
    stringToHash = string.encode('utf8')
    requestHash = hashlib.md5(stringToHash).hexdigest()
    return requestHash

def authorize(user_token, api_key, api_secret):
    params = {
            'api_key': api_key,
            'method': 'auth.getSession',
            'token': user_token
            }
    requestHash = hashRequest(params, api_secret)
    params['api_sig'] = requestHash
    apiResp = requests.post(api_head, params)
    return apiResp.text

def scrobble(song_name, artist_name, session_key, api_key, api_secret, timestamp=None):
    # Currently this sort of cheats the timestamp protocol
    params = {
            'method': 'track.scrobble',
            'api_key': api_key,
            'timestamp': str( int(time.time() - 30) ) if timestamp is None else timestamp,
            'track': song_name,
            'artist': artist_name,
            'sk': session_key
            }
    try:
        requestHash = hashRequest(params, api_secret)
    except Exception as e:
        return "hasherror"

    params['api_sig'] = requestHash
    apiResp = requests.post(api_head, params)
    return apiResp

def parse_session_key(response):
    lines = str(response).split("\n")
    lines = [l for l in lines if "<key>" in l]
    assert len(lines) == 1, "Session key should be in the response"
    line = lines[0]
    return line.split("<key>")[-1].split("</key>")[0]

def login():
    config_folder, apikey_folder = get_config_folder()

    LAST_FM_API_FILE = (apikey_folder / "LAST_FM_API")
    LAST_FM_API_SECRET_FILE = (apikey_folder / "LAST_FM_API_SECRET")

    if LAST_FM_API_FILE.exists():
        print("Api key already saved. Loading...")
        LAST_FM_API = LAST_FM_API_FILE.open().read()
        LAST_FM_API_SECRET = LAST_FM_API_SECRET_FILE.open().read()
    else:
        print("Go to https://www.last.fm/api/authentication to create / locate your API key")
        print()
        LAST_FM_API = input("API key:")
        LAST_FM_API_SECRET = input("API key secret:")
        with LAST_FM_API_FILE.open("w") as f:
            f.write(LAST_FM_API)
        with LAST_FM_API_SECRET_FILE.open("w") as f:
            f.write(LAST_FM_API_SECRET)

    instructions =  [f"Go to http://www.last.fm/api/auth?api_key={LAST_FM_API}&cb=http://localhost:5555",
    "Make sure nothing is running at port 5555, as we will be manually retreiving the token.",
    'Click "Allow Access"',
    "Now copy the token from the resulting url (e.g. http://localhost:5555/?token=TOKEN_YOU_WANT)"]
    
    SESSION_KEY = None
    SESSION_KEY_FILE = (apikey_folder / "SESSION_KEY")
    if SESSION_KEY_FILE.exists():
        SESSION_KEY = SESSION_KEY_FILE.open().read()
    else:
        print()
        print("\n".join(instructions))
        print()
        token = input("Token:")
        auth_result = authorize(token, LAST_FM_API, LAST_FM_API_SECRET)
        print(auth_result)
        SESSION_KEY = parse_session_key(auth_result)
        print("Session key:", SESSION_KEY)
        with SESSION_KEY_FILE.open("w") as f:
            f.write(SESSION_KEY)

    return SESSION_KEY, LAST_FM_API, LAST_FM_API_SECRET
