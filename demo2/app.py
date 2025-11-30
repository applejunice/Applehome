from flask import Flask, jsonify, request, g
from flask_cors import CORS
from functools import wraps
from decimal import Decimal
import toml
import jwt
import hashlib
from datetime import datetime, timedelta

from models import db, User, Transaction, init_db

# 設定読み込み
config = toml.load('config.toml')

app = Flask(__name__)
CORS(app)

# JWT 設定
JWT_SECRET = config['jwt']['secret_key']
JWT_EXPIRES_HOURS = config['jwt']['expires_hours']


def hash_password(password: str) -> str:
    """パスワードハッシュ"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(user_id: int, username: str) -> str:
    """JWT トークン生成"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRES_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def login_required(f):
    """ログイン認証デコレータ"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'error': '認証トークンがありません'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.current_user_id = payload['user_id']
            g.current_username = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'トークンの有効期限が切れています'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': '無効なトークンです'}), 401

        return f(*args, **kwargs)
    return decorated


@app.before_request
def before_request():
    """リクエスト前にデータベース接続"""
    db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    """リクエスト後にデータベース接続を閉じる"""
    if not db.is_closed():
        db.close()
    return response


@app.route('/')
def index():
    """API ルートパス"""
    return jsonify({
        'service': 'User Service API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/register': 'ユーザー登録',
            'POST /api/login': 'ユーザーログイン',
            'GET /api/users/balances': '全ユーザー残高照会',
            'POST /api/transfer': '送金 (ログイン必須)',
            'GET /api/me': '現在のユーザー情報取得 (ログイン必須)'
        }
    })


@app.route('/api/register', methods=['POST'])
def register():
    """ユーザー登録"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'リクエストデータが空です'}), 400

    username = data.get('username')
    password = data.get('password')
    initial_balance = data.get('balance', 0)

    if not username or not password:
        return jsonify({'success': False, 'error': 'ユーザー名とパスワードは必須です'}), 400

    if len(username) < 3 or len(username) > 50:
        return jsonify({'success': False, 'error': 'ユーザー名は3〜50文字で入力してください'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'error': 'パスワードは6文字以上で入力してください'}), 400

    try:
        # ユーザー名の重複チェック
        if User.select().where(User.username == username).exists():
            return jsonify({'success': False, 'error': 'このユーザー名は既に使用されています'}), 400

        # ユーザー作成
        user = User.create(
            username=username,
            password=hash_password(password),
            balance=Decimal(str(initial_balance))
        )

        return jsonify({
            'success': True,
            'message': '登録が完了しました',
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': float(user.balance)
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': f'登録に失敗しました: {str(e)}'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """ユーザーログイン"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'リクエストデータが空です'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'ユーザー名とパスワードは必須です'}), 400

    try:
        user = User.get_or_none(User.username == username)

        if not user or user.password != hash_password(password):
            return jsonify({'success': False, 'error': 'ユーザー名またはパスワードが間違っています'}), 401

        token = generate_token(user.id, user.username)

        return jsonify({
            'success': True,
            'message': 'ログインしました',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': float(user.balance)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'ログインに失敗しました: {str(e)}'}), 500


@app.route('/api/users/balances', methods=['GET'])
def get_all_balances():
    """全ユーザー残高照会"""
    try:
        users = User.select(User.id, User.username, User.balance)

        user_list = [{
            'id': user.id,
            'username': user.username,
            'balance': float(user.balance)
        } for user in users]

        return jsonify({
            'success': True,
            'count': len(user_list),
            'users': user_list
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'照会に失敗しました: {str(e)}'}), 500


@app.route('/api/transfer', methods=['POST'])
@login_required
def transfer():
    """送金 (ログイン必須)"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'リクエストデータが空です'}), 400

    to_username = data.get('to_username')
    amount = data.get('amount')

    if not to_username:
        return jsonify({'success': False, 'error': '送金先ユーザーを指定してください'}), 400

    if not amount or float(amount) <= 0:
        return jsonify({'success': False, 'error': '送金額は0より大きい値を指定してください'}), 400

    amount = Decimal(str(amount))

    try:
        with db.atomic():  # トランザクション
            # 現在のユーザーを取得
            from_user = User.get_by_id(g.current_user_id)

            # 残高チェック
            if from_user.balance < amount:
                return jsonify({'success': False, 'error': '残高が不足しています'}), 400

            # 送金先ユーザーを取得
            to_user = User.get_or_none(User.username == to_username)
            if not to_user:
                return jsonify({'success': False, 'error': '送金先ユーザーが存在しません'}), 404

            if to_user.id == from_user.id:
                return jsonify({'success': False, 'error': '自分自身には送金できません'}), 400

            # 送金実行
            from_user.balance -= amount
            to_user.balance += amount
            from_user.save()
            to_user.save()

            # 取引記録
            Transaction.create(
                from_user=from_user,
                to_user=to_user,
                amount=amount,
                transaction_type='transfer'
            )

            return jsonify({
                'success': True,
                'message': f'{to_username} へ {float(amount)} 円を送金しました',
                'from_balance': float(from_user.balance),
                'to_balance': float(to_user.balance)
            })

    except Exception as e:
        return jsonify({'success': False, 'error': f'送金に失敗しました: {str(e)}'}), 500


@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    """現在のログインユーザー情報取得"""
    try:
        user = User.get_by_id(g.current_user_id)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': float(user.balance),
                'created_at': user.created_at.isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'ユーザー情報の取得に失敗しました: {str(e)}'}), 500


if __name__ == '__main__':
    # データベース初期化
    init_db()

    server_config = config['server']
    print("=" * 50)
    print("User Service API 起動中...")
    print("=" * 50)
    print(f"サービスアドレス: http://{server_config['host']}:{server_config['port']}")
    print("=" * 50)

    app.run(
        debug=server_config['debug'],
        host=server_config['host'],
        port=server_config['port']
    )
