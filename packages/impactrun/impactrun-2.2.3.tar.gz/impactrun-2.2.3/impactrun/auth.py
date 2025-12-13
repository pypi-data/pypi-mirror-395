
import json
import uuid

import requests


def authenticate():
    client_id = 'OmniCenterWeb'
    response_type = 'id_token token'
    redirect_uri = 'https://hoc-rrsc.omnicellcloud.com/OmniCenter/auth'
    scope = 'openid api'
    state = uuid.uuid4().hex  # '6885290715804cf591d3d913601917b0'
    nonce = uuid.uuid4().hex  # 'c7d5083c263d4dfebf5ca459e73498a9'
    URL = 'https://hoc-rrsc.omnicellcloud.com/IdentityProvider/connect/authorize'
    PARAMS = {'client_id': client_id, 'response_type': response_type, 'redirect_uri': redirect_uri,
              'scope': scope, 'state': state, 'nonce': nonce}
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/82.0.4069.0 Safari/537.36'),
        'Referer': 'https://hoc-rrsc.omnicellcloud.com/OmniCenter/'
    }
    URL = 'https://hoc-rrsc.omnicellcloud.com/IdentityProvider/connect/authorize'
    r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
    for resp in r.history:
        loginURL = resp.headers['Location']
        signin_cookie = resp.headers['Set-Cookie']
        if signin_cookie.endswith('; path=/IdentityProvider; secure; HttpOnly'):
            signin_cookie = signin_cookie.replace('; path=/IdentityProvider; secure; HttpOnly', '')

    print('SigninURL:' + loginURL, '\n', 'SignInMessageCookie:' + signin_cookie)
    idsrv_xsrf_cookie = r.headers['Set-Cookie']
    if idsrv_xsrf_cookie.endswith('; path=/IdentityProvider; secure; HttpOnly'):
        idsrv_xsrf_cookie = idsrv_xsrf_cookie.replace('; path=/IdentityProvider; secure; HttpOnly', '')

    print("idsrv.xsrf cookie: " + idsrv_xsrf_cookie)
    s = r.text
    # tart = s.find("loginUrl&quot;:&quot;") + len("loginUrl&quot;:&quot;")
    # end = s.find("&quot;,&quot;antiForgery")
    # loginURL = 'https://hoc-rrsc.omnicellcloud.com' + s[start:end]
    # print(loginURL)
    start = s.find("idsrv.xsrf&quot;,&quot;value&quot;:&quot;") + len("idsrv.xsrf&quot;,&quot;value&quot;:&quot;")
    end = s.find("&quot;},&quot;allowRememberMe")
    idsrv_xsrf_body = s[start:end]
    print("idsrv.xsrf body: " + idsrv_xsrf_body)

    # Second Request
    URL = "https://hoc-rrsc.omnicellcloud.com/IdentityProvider/api/tenants"
    login_cookie_header = signin_cookie + '; ' + idsrv_xsrf_cookie
    r = requests.get(url=URL, headers=HEADERS)
    print("Response for API Tenants:" + r.text)
    rsp_json = json.loads(r.text)
    tenant_id = rsp_json[0]['TenantId']
    # tenant_id = "031dffcd-dab3-4e98-b74c-ef361aac2d96"
    print("TenantID: " + tenant_id)

    # Signin URL
    HEADERS = {'Cookie': login_cookie_header}
    DATA = {'idsrv.xsrf': idsrv_xsrf_body, 'tenantId': tenant_id, 'username': '10', 'password': '10'}
    r = requests.post(url=loginURL, headers=HEADERS, data=DATA)
    for resp in r.history:
        tokenString = resp.headers['Location']
        idsrv_cookie = resp.headers['Set-Cookie']
        # print(idsrv_cookie)
    # print(r.text)
    access_token = tokenString.split('&')[1]
    access_token = access_token.split('=')[1]

    return access_token

    # Test access token
    URL = 'https://hoc-rrsc.omnicellcloud.com/IdentityProvider/connect/userinfo'
    r = requests.get(url=URL)
    print("No Auth Status Code: " + str(r.status_code))
    print("No Auth Response: " + r.text)
    bearer = 'Bearer ' + access_token
    HEADERS = {'Authorization': bearer}
    r = requests.get(url=URL, headers=HEADERS)
    print("Auth Status Code: " + str(r.status_code))
    print("Auth Response: " + r.text)


if __name__ == "__main__":
    omnicell_auth_flow()
