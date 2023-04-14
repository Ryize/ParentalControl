from server.models import *

MAC = get_mac()


class AuthSystem:
    @staticmethod
    def authorize_by_data(login: str, password: str) -> bool:
        user = User.get_or_none(
            User.login == login,
            User.password == password
        )
        if user:
            if user.mac == '-1':
                user.mac = str(MAC)
                user.save()
            return user.mac == str(MAC)
        return False

    @staticmethod
    def authorize_by_telegram() -> bool:
        user = User.get_or_none(User.mac == MAC)
        if not user:
            return False
        for i in ConfirmLogin.select().where(ConfirmLogin.user == user):
            i.delete_instance()
        ConfirmLogin.create(user=user)
        return True


AuthSystem().authorize_by_telegram()
