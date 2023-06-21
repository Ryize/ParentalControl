import datetime

import peewee as pw
from uuid import getnode as mac

from user.config import USER, PASSWORD, DB_NAME, HOST

db = pw.MySQLDatabase(
    DB_NAME,
    host=HOST,
    user=USER,
    passwd=PASSWORD,
)


def get_mac():
    return str(mac())[:-1]


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


class ControlDate(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    monday = pw.CharField(max_length=5, default='23:59')
    tuesday = pw.CharField(max_length=5, default='23:59')
    wednesday = pw.CharField(max_length=5, default='23:59')
    thursday = pw.CharField(max_length=5, default='23:59')
    friday = pw.CharField(max_length=5, default='23:59')
    saturday = pw.CharField(max_length=5, default='23:59')
    sunday = pw.CharField(max_length=5, default='23:59')


class Adjustment(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    time = pw.CharField(max_length=5)
    done = pw.BooleanField(default=False)


class TimeDaySession(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    time = pw.CharField(max_length=5, default='00:00')
    day = pw.DateField(default=datetime.date.today)


class Ban(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')


class RequestTime(BaseModel):
    user = pw.ForeignKeyField(User, related_name='control_date')
    amount = pw.CharField(max_length=5, default='')
    day = pw.DateField(default=datetime.date.today)
    done = pw.BooleanField(default=False)
    is_send = pw.BooleanField(default=False)


User.create_table()
ConfirmLogin.create_table()
ControlDate.create_table()
Adjustment.create_table()
TimeDaySession.create_table()
Ban.create_table()
RequestTime.create_table()

if __name__ == "__main__":
    User(telegram='test').save()
