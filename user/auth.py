from server.models import *

MAC = str(get_mac())[:-1]


class AuthSystem:
    @staticmethod
    def authorize_by_data(login: str, password: str) -> bool:
        user = User.get_or_none(
            User.login == login,
            User.password == password
        )
        if user:
            if user.mac != MAC:
                user.mac = str(MAC)[:-1]
                user.save()
            return True
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
