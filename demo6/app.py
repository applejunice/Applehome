"""
GitHub OAuth Demo with Flask
"""
import os
import secrets
from flask import Flask, redirect, request, jsonify, session, url_for
import requests

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# GitHub OAuth 配置
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', 'your_client_id')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', 'your_client_secret')
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com'


@app.route('/')
def index():
    """首页"""
    if 'access_token' in session:
        return jsonify({
            'message': 'You are logged in',
            'endpoints': {
                'user_info': '/api/user',
                'logout': '/logout'
            }
        })
    return jsonify({
        'message': 'Welcome to GitHub OAuth Demo',
        'endpoints': {
            'login': '/login'
        }
    })


@app.route('/login')
def login():
    """
    1. Login API - 跳转到 GitHub 授权页面
    """
    # 生成随机 state 防止 CSRF 攻击
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    # 构建 GitHub 授权 URL
    params = {
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': url_for('callback', _external=True),
        'scope': 'read:user user:email',
        'state': state
    }

    auth_url = f"{GITHUB_AUTHORIZE_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    """
    GitHub OAuth 回调处理
    """
    # 验证 state
    if request.args.get('state') != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400

    # 检查错误
    error = request.args.get('error')
    if error:
        return jsonify({
            'error': error,
            'error_description': request.args.get('error_description')
        }), 400

    # 获取授权码
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    # 用授权码换取 access_token
    token_response = requests.post(
        GITHUB_TOKEN_URL,
        data={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': url_for('callback', _external=True)
        },
        headers={'Accept': 'application/json'}
    )

    token_data = token_response.json()

    if 'error' in token_data:
        return jsonify({
            'error': token_data.get('error'),
            'error_description': token_data.get('error_description')
        }), 400

    # 保存 access_token 到 session
    session['access_token'] = token_data.get('access_token')

    return jsonify({
        'message': 'Login successful',
        'next': '/api/user'
    })


@app.route('/api/user')
def get_user():
    """
    2. 获取基础信息 API - 获取 GitHub 用户信息
    """
    access_token = session.get('access_token')

    if not access_token:
        return jsonify({'error': 'Not authenticated', 'login_url': '/login'}), 401

    # 获取用户基本信息
    user_response = requests.get(
        f'{GITHUB_API_URL}/user',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    if user_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch user info'}), user_response.status_code

    user_data = user_response.json()

    # 获取用户邮箱
    email_response = requests.get(
        f'{GITHUB_API_URL}/user/emails',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    emails = []
    if email_response.status_code == 200:
        emails = email_response.json()

    # 返回用户基础信息
    return jsonify({
        'id': user_data.get('id'),
        'login': user_data.get('login'),
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'emails': [e.get('email') for e in emails if e.get('verified')],
        'avatar_url': user_data.get('avatar_url'),
        'bio': user_data.get('bio'),
        'company': user_data.get('company'),
        'location': user_data.get('location'),
        'public_repos': user_data.get('public_repos'),
        'followers': user_data.get('followers'),
        'following': user_data.get('following'),
        'created_at': user_data.get('created_at')
    })


@app.route('/logout')
def logout():
    """登出"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
