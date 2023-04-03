from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, quote_plus
import webbrowser
import requests
import sys
import json
import jwt
import secrets
import base64
import hashlib

# Begin Configuration
client_id ="PUT YOUR CLIENT ID HERE"
client_secret= "PUT YOUR CLIENT SECRET HERE"
auth_uri = "https://accounts.google.com/o/oauth2/v2/auth"
token_uri = "https://oauth2.googleapis.com/token"
redirect_uri = "http://localhost:8000"
# End Configuration

class AccessCodeHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    global access_code
    query = parse_qs(urlparse (self.path).query)
    code = query.get('code', None)
    if code != None:
      access_code = code[0]
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>Python3 OAuth by controlthings.gr</title></head>", "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    self.wfile.write(bytes("<p>You can now close the browser and return to the application.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))

access_code = ""
code_verifier = secrets.token_urlsafe(64) #PKCE code verifier, must be > 32 bytes for google, it must also be < 128 characters
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip("=")
redirect_uri_urlencoded = quote_plus(redirect_uri )
_authorization_url = f"""{auth_uri}?
response_type=code&
client_id={client_id}&
scope=openid%20email&
redirect_uri={redirect_uri_urlencoded}&
code_challenge={code_challenge}&
code_challenge_method=S256
""".replace("\n", "")

print("...Opening browser")
webbrowser.open(_authorization_url)
print("...Running server to receive access code")
httpd = HTTPServer(('127.0.0.1', 8000), AccessCodeHandler)
httpd.handle_request()
print(access_code)
if (access_code == ""):
  print("Code was not received. Inspect errors in the output")
  sys.exit()

print("...Requesting token")
_token_post_data = {
  'code': access_code,
  'client_id': client_id,
  'client_secret':client_secret,
  'redirect_uri':redirect_uri,
  'grant_type':'authorization_code',
  'code_verifier':code_verifier
}

token_response = requests.post(token_uri, data=_token_post_data)
#assuming correct response
token_response_json =  json.loads(token_response.text)
id_token = id_token = jwt.decode(token_response_json['id_token'], options={"verify_signature": False}) # It came directly from google, no need to verify signature https://developers.google.com/identity/openid-connect/openid-connect#obtainuserinfo
print(id_token)

