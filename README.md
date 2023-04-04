
# About
A Python3 script that authenticates users based on their Google account, using
OpenID connect. It uses Proof Key for Code Exchange (PKCE) for security.  

# Prerequisites
python -m pip install requests
python -m pip install pyjwt

# Configuration
Obtain a `client id` and a `client secret` following [these instructions](https://developers.google.com/identity/openid-connect/openid-connect).
Make sure that in Google console you have added `openid` scope in the OAuth consent screen
and you have define the `Application type` to be `Desktop`.

Put your `client id` and `client secret` in lines 13 and 14 of the script.

# Running
Simply execute:

```
python3 google-openidc.py
```
# More information
You can read [my blog post](https://respected-professor.blogspot.com/2023/04/authenticate-users-in-python-scripts.html). Open an issue if you need support.