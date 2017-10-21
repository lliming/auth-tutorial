#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:44:23 2017

@author: liming
"""

from flask import Flask, url_for, session, redirect, request
import globus_sdk
import json

app = Flask(__name__)
app.config.from_pyfile('auth_example.conf')

def load_app_client():
    return globus_sdk.ConfidentialAppAuthClient(
        app.config['APP_CLIENT_ID'], app.config['APP_CLIENT_SECRET'])

@app.route("/", methods=['GET'])
def index():
    """
    This could be any page you like, rendered by Flask.
    For this simple example, it will either redirect you to login, or print
    a simple message.
    """
    if not session.get('is_authenticated'):
        return redirect(url_for('login'))
    logout_uri = url_for('logout', _external=True)
    auth_token = str(session.get('tokens')['auth.globus.org']['access_token'])
    ac = globus_sdk.AuthClient(authorizer=globus_sdk.AccessTokenAuthorizer(auth_token))
    myoidc = session.get('id_token')
    myids = ac.get_identities(ids=str(session.get('username'))).data
    oidcinfo = ac.oauth2_userinfo()
    page = '<html><body>\n<p>' + str(session.get('realname')) + ', you are logged in.</p>\n\n'
    page = page + '<p>Your local username is: ' + str(session.get('username')) + '</p>\n\n'
    page = page + '<p><a href="'+logout_uri+'">Logout now.</a></p>\n\n'
    page = page + '<p>OIDC UserInfo says your effective ID is ' + oidcinfo["sub"]
    page = page + ', your name is ' + oidcinfo["name"]
    page = page + ', and your email is ' + oidcinfo["email"] + '.</p>\n\n'
    page = page + '<p>Your OIDC identity is:</p>\n<pre>' + json.dumps(myoidc,indent=3) + '</pre>\n\n'
    page = page + '<p>Your Globus Auth identity is:</p>\n<pre>' + json.dumps(myids,indent=3) + '</pre>\n\n'
    page = page + '</body></html>'
    return(page)

@app.route("/login", methods=['GET'])
def login():
    """
    Login via Globus Auth.
    May be invoked in one of two scenarios:

      1. Login is starting, no state in Globus Auth yet
      2. Returning to application during login, already have short-lived
         code from Globus Auth to exchange for tokens, encoded in a query
         param
    """
    # the redirect URI, as a complete URI (not relative path)
    redirect_uri = url_for('login', _external=True)

    auth_client = load_app_client()
    auth_client.oauth2_start_flow(redirect_uri)

    # If there's no "code" query string parameter, we're in this route
    # starting a Globus Auth login flow.
    # Redirect out to Globus Auth
    if 'code' not in request.args:
        auth_uri = auth_client.oauth2_get_authorize_url()
        return redirect(auth_uri)
    # If we do have a "code" param, we're coming back from Globus Auth
    # and can start the process of exchanging an auth code for a token.
    else:
        code = request.args.get('code')
        tokens_response = auth_client.oauth2_exchange_code_for_tokens(code)
        ids = tokens_response.decode_id_token(auth_client)
        session.update(
                tokens=tokens_response.by_resource_server,
                id_token=ids,
                username=ids['sub'],
                realname=ids['name'],
                is_authenticated=True
                )
        return redirect(url_for('index'))

@app.route("/logout", methods=['GET'])
def logout():
    """
    - Revoke the tokens with Globus Auth.
    - Destroy the session state.
    - Redirect the user to the Globus Auth logout page.
    """
    client = load_app_client()

    # Revoke the tokens with Globus Auth
    for token in (token_info['access_token']
                  for token_info in session['tokens'].values()):
        client.oauth2_revoke_token(token)

    # Destroy the session state
    session.clear()

    # the return redirection location to give to Globus AUth
    redirect_uri = url_for('index', _external=True)

    # build the logout URI with query params
    # there is no tool to help build this (yet!)
    globus_logout_url = (
        'https://auth.globus.org/v2/web/logout' +
        '?client={}'.format(app.config['APP_CLIENT_ID']) +
        '&redirect_uri={}'.format(redirect_uri) +
        '&redirect_name=Your Flask App')

    # Redirect the user to the Globus Auth logout page
    return redirect(globus_logout_url)

# actually run the app if this is called as a script
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,ssl_context=('./keys/server.crt', './keys/server.key'))

