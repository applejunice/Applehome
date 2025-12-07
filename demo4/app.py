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

# 管理员配置
ADMIN_USERNAME = config['admin']['username']
ADMIN_PASSWORD = config['admin']['password']


def hash_password(password: str) -> str:
    """パスワードハッシュ"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(user_id: int, username: str, is_admin: bool = False) -> str:
    """JWT トークン生成"""
    payload = {
        'user_id': user_id,
        'username': username,
        'is_admin': is_admin,
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
            g.is_admin = payload.get('is_admin', False)
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'トークンの有効期限が切れています'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': '無効なトークンです'}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """管理员权限检查装饰器"""
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
            g.is_admin = payload.get('is_admin', False)

            if not g.is_admin:
                return jsonify({'success': False, 'error': '管理员权限が必要です'}), 403
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
            'POST /api/login': 'ユーザーログイン（管理员/普通用户共用）',
            'GET /api/me': '現在のユーザー情報取得 (ログイン必須)',
            'POST /api/transfer': '送金 (ログイン必須)',
            'GET /api/my/balance': '自分の残高照会 (ログイン必須)',
            'GET /api/my/transactions': '自分の転送記録照会 (ログイン必須)',
            'GET /api/users/balances': '全ユーザー残高照会 (管理员専用)',
            'GET /api/transactions': '全転送記録照会 (管理员専用)',
            'PUT /api/admin/balance': 'ユーザー残高修正 (管理员専用)'
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
    """ユーザーログイン（管理员和普通用户共用）"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'リクエストデータが空です'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'ユーザー名とパスワードは必須です'}), 400

    try:
        # 检查是否是管理员登录
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            token = generate_token(user_id=0, username=ADMIN_USERNAME, is_admin=True)
            return jsonify({
                'success': True,
                'message': '管理员ログインしました',
                'token': token,
                'user': {
                    'id': 0,
                    'username': ADMIN_USERNAME,
                    'is_admin': True
                }
            })

        # 普通用户登录
        user = User.get_or_none(User.username == username)

        if not user or user.password != hash_password(password):
            return jsonify({'success': False, 'error': 'ユーザー名またはパスワードが間違っています'}), 401

        token = generate_token(user.id, user.username, is_admin=False)

        return jsonify({
            'success': True,
            'message': 'ログインしました',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': float(user.balance),
                'is_admin': False
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'ログインに失敗しました: {str(e)}'}), 500


@app.route('/api/users/balances', methods=['GET'])
@admin_required
def get_all_balances():
    """全ユーザー残高照会（管理员专用）"""
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
        # 管理员直接返回管理员信息
        if g.is_admin:
            return jsonify({
                'success': True,
                'user': {
                    'id': 0,
                    'username': g.current_username,
                    'is_admin': True
                }
            })

        user = User.get_by_id(g.current_user_id)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': float(user.balance),
                'is_admin': False,
                'created_at': user.created_at.isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'ユーザー情報の取得に失敗しました: {str(e)}'}), 500


@app.route('/api/transactions', methods=['GET'])
@admin_required
def get_all_transactions():
    """全転送記録照会（管理员专用）"""
    try:
        transactions = (Transaction
                        .select(Transaction, User)
                        .join(User, on=(Transaction.from_user == User.id).alias('from_user'))
                        .switch(Transaction)
                        .join(User, on=(Transaction.to_user == User.id).alias('to_user'))
                        .order_by(Transaction.created_at.desc()))

        transaction_list = []
        for t in Transaction.select().order_by(Transaction.created_at.desc()):
            from_username = t.from_user.username if t.from_user else None
            to_username = t.to_user.username if t.to_user else None
            transaction_list.append({
                'id': t.id,
                'from_user': from_username,
                'to_user': to_username,
                'amount': float(t.amount),
                'type': t.transaction_type,
                'created_at': t.created_at.isoformat()
            })

        return jsonify({
            'success': True,
            'count': len(transaction_list),
            'transactions': transaction_list
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'照会に失敗しました: {str(e)}'}), 500


@app.route('/api/admin/balance', methods=['PUT'])
@admin_required
def admin_update_balance():
    """管理员修改用户余额"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'リクエストデータが空です'}), 400

    username = data.get('username')
    new_balance = data.get('balance')

    if not username:
        return jsonify({'success': False, 'error': 'ユーザー名を指定してください'}), 400

    if new_balance is None:
        return jsonify({'success': False, 'error': '新しい残高を指定してください'}), 400

    try:
        new_balance = Decimal(str(new_balance))
        if new_balance < 0:
            return jsonify({'success': False, 'error': '残高は0以上で指定してください'}), 400

        user = User.get_or_none(User.username == username)
        if not user:
            return jsonify({'success': False, 'error': 'ユーザーが存在しません'}), 404

        old_balance = user.balance
        user.balance = new_balance
        user.save()

        return jsonify({
            'success': True,
            'message': f'{username} の残高を更新しました',
            'user': {
                'id': user.id,
                'username': user.username,
                'old_balance': float(old_balance),
                'new_balance': float(user.balance)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'残高更新に失敗しました: {str(e)}'}), 500


@app.route('/api/my/balance', methods=['GET'])
@login_required
def get_my_balance():
    """普通用户查看自己的余额"""
    try:
        if g.is_admin:
            return jsonify({'success': False, 'error': '管理员には残高がありません'}), 400

        user = User.get_by_id(g.current_user_id)
        return jsonify({
            'success': True,
            'balance': float(user.balance)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'残高照会に失敗しました: {str(e)}'}), 500


@app.route('/api/my/transactions', methods=['GET'])
@login_required
def get_my_transactions():
    """普通用户查看自己的转账记录"""
    try:
        if g.is_admin:
            return jsonify({'success': False, 'error': '管理员用の転送記録はありません。/api/transactions を使用してください'}), 400

        user_id = g.current_user_id

        # 查询发送和接收的转账记录
        transactions = (Transaction
                        .select()
                        .where((Transaction.from_user == user_id) | (Transaction.to_user == user_id))
                        .order_by(Transaction.created_at.desc()))

        transaction_list = []
        for t in transactions:
            from_username = t.from_user.username if t.from_user else None
            to_username = t.to_user.username if t.to_user else None

            # 判断是发送还是接收
            if t.from_user and t.from_user.id == user_id:
                direction = 'sent'
            else:
                direction = 'received'

            transaction_list.append({
                'id': t.id,
                'from_user': from_username,
                'to_user': to_username,
                'amount': float(t.amount),
                'type': t.transaction_type,
                'direction': direction,
                'created_at': t.created_at.isoformat()
            })

        return jsonify({
            'success': True,
            'count': len(transaction_list),
            'transactions': transaction_list
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'照会に失敗しました: {str(e)}'}), 500


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
