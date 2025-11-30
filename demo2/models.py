from peewee import *
from datetime import datetime
import toml

# 設定読み込み
config = toml.load('config.toml')
db_config = config['database']

# データベース接続
db = PostgresqlDatabase(
    db_config['name'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port']
)


class BaseModel(Model):
    """ベースモデル"""
    class Meta:
        database = db


class User(BaseModel):
    """ユーザーモデル"""
    id = AutoField()
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)  # ハッシュ化されたパスワード
    balance = DecimalField(decimal_places=2, default=0.00)  # 残高
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'users'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class Transaction(BaseModel):
    """取引記録モデル"""
    id = AutoField()
    from_user = ForeignKeyField(User, backref='sent_transactions', null=True)
    to_user = ForeignKeyField(User, backref='received_transactions')
    amount = DecimalField(decimal_places=2)
    transaction_type = CharField(max_length=20)  # transfer, deposit, withdraw
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'transactions'


def init_db():
    """データベーステーブル初期化"""
    db.connect()
    db.create_tables([User, Transaction], safe=True)
    print("データベーステーブルを作成しました")


if __name__ == '__main__':
    init_db()
