#!/usr/bin/env python3
#
# -- This example shows how to authenticate a user in a Python script
#    using the Globus Python SDK and what the identity data look like.
#
# -- Note that it's less than 20 lines of code, and much of it is just 
#    printing stuff so you can see what it looks like.
#
# -- When you run the script, it will generate a URL and print it on 
#    the command line. The user must open the URL in a Web browser and 
#    authenticate with their identity provider: campus, Google, etc.
#
# -- When authentication is finished, the user will be given a code in 
#    the browser, which he/she must copy and paste back into the 
#    command line.
#
# -- The script will then print the information that Globus Auth 
#    returns about the user.

import globus_sdk
import json        # Used only for pretty-printing Auth results

# -- The CLIENT_ID is obtained from Globus Auth when you register 
#    a "native app." The ID here is for an app that I registered.
# -- You can register your own native app at 
#    https://developers.globus.org/.  It's fun and easy!
# -- Because this is a native app (runs locally on your system), my
#    CLIENT_ID will work anywhere. But if I unregister my app, it 
#    will stop working for you. Replace it with your own.
CLIENT_ID = '02a65a67-d996-4765-85b9-9522fb410d14'

# -- Use the CLIENT_ID to instantiate a client object that will allow
#    native (local) authentication.
# -- The first three scopes are standard for OIDC clients.
# -- The fourth scope only works with Globus and it allows the script 
#    to see the user's "linked identities:" any other IDs they've 
#    linked in Globus to the one they authenticate with. You only need 
#    to specify this scope if you want to see the linked IDs.
client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(requested_scopes='openid email profile urn:globus:auth:scope:auth.globus.org:view_identity_set')

# Use the client object to generate a login URL for the user, then
# print it on the terminal for the user to copy and paste.
authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}\n'.format(authorize_url))

# -- This rather complicated user input code handles the differences 
#    between Python2 and Python3.
# -- If you only use one Python version, you can simplify this.
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()

# -- Now that the user has authenticated with Globus Auth and given 
#    us the code, we can use the code with the Auth API to retrieve 
#    the user's identity information.
# -- The first step is to trade in the code for basic information about
#    the user, PLUS any API access tokens we specified in the scopes
#    above.
# -- The API access tokens will allow us to use the Auth API on the 
#    user's behalf to get more detailed identity information.
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

# -- Before doing anything else, we'll display the information that
#    we got when the user authenticated and we traded in his/her code
#    for tokens. (The token_response was obtained above.)
ids = token_response.decode_id_token(client)
print("\n\nHere's what I know about you:\n")
print(json.dumps(ids,indent=3))

# -- Now, we'll look deeper into the response and find the access_token 
#    for the Auth API (auth.globus.org).
# -- We'll use this Auth API access token to access the Auth API AS THE 
#    AUTHENTICATED USER and obtain more details about his/her identity.
AUTH_TOKEN = token_response.by_resource_server['auth.globus.org']['access_token']
ac = globus_sdk.AuthClient(authorizer=globus_sdk.AccessTokenAuthorizer(AUTH_TOKEN))

# -- This is the standard OIDC userinfo call.
# -- The response provides a standard OIDC user profile.
# -- Because we requested the view_identity_set scope when the user
#    authenticated (see above), this will also include info on any
#    linked identities the user has added in Globus.
oidcinfo = ac.oauth2_userinfo()
print("\n\nAnd here's what oauth2_userinfo() returns:\n")
print(json.dumps(oidcinfo.data,indent=3))

# -- That's all, folks.

