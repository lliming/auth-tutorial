#!/usr/bin/env python3

import globus_sdk,json

CLIENT_ID = '02a65a67-d996-4765-85b9-9522fb410d14'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(requested_scopes='openid email profile urn:globus:auth:scope:auth.globus.org:view_identity_set')

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}\n'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server['auth.globus.org']

# most specifically, you want these tokens as strings
AUTH_TOKEN = globus_auth_data['access_token']

# Let the user know that he/she is authenticated
ids = token_response.decode_id_token(client)

print("\n\nHere's what I know about you:\n")
print(json.dumps(ids,indent=3))

# get the stored access token for the Auth API and use it 
# to authorize stuff AS THE AUTHENTICATED USER
ac = globus_sdk.AuthClient(authorizer=globus_sdk.AccessTokenAuthorizer(AUTH_TOKEN))

# use Auth API to get the standard OIDC userinfo fields (like any OIDC client)
oidcinfo = ac.oauth2_userinfo()

print("\n\nAnd here's what oauth2_userinfo() returns:\n")
print(json.dumps(oidcinfo.data,indent=3))
