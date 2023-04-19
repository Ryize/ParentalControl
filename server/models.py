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


class BotText(BaseModel):
    tag = pw.CharField(max_length=28, unique=True)
    text = pw.TextField(default='Текст не задан!')


class ConfirmLogin(BaseModel):
    user = pw.ForeignKeyField(User, related_name='confirm_login')
    status = pw.IntegerField(default=-1)


class AccountLinking(BaseModel):
    user = pw.ForeignKeyField(User, related_name='account_linking')
    os_info = pw.CharField(max_length=256, null=False)


class ControlDate(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    monday = pw.CharField(max_length=5, default='24:00')
    tuesday = pw.CharField(max_length=5, default='24:00')
    wednesday = pw.CharField(max_length=5, default='24:00')
    thursday = pw.CharField(max_length=5, default='24:00')
    friday = pw.CharField(max_length=5, default='24:00')
    saturday = pw.CharField(max_length=5, default='24:00')
    sunday = pw.CharField(max_length=5, default='24:00')


class Adjustment(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    time = pw.CharField(max_length=5)
    done = pw.BooleanField(default=False)


User.create_table()
BotText.create_table()
ConfirmLogin.create_table()
ControlDate.create_table()
Adjustment.create_table()

if __name__ == '__main__':
    User(telegram='test').save()
