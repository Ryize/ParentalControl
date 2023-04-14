import peewee as pw
from uuid import getnode as get_mac

from user.config import USER, PASSWORD, DB_NAME, HOST

db = pw.MySQLDatabase(
    DB_NAME,
    host=HOST,
    user=USER,
    passwd=PASSWORD,
)


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    mac = pw.CharField(max_length=64, default=get_mac, unique=True)
    telegram = pw.CharField(max_length=64)
    login = pw.CharField(max_length=64, unique=True, null=False)
    password = pw.CharField(max_length=128, null=False)


class ConfirmLogin(BaseModel):
    user = pw.ForeignKeyField(User, related_name='confirm_login')
    status = pw.IntegerField(default=-1)


User.create_table()
ConfirmLogin.create_table()

if __name__ == "__main__":
    User(telegram='test').save()