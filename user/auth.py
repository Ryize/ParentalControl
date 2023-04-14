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
            return user.mac == str(MAC)
        return False

    @staticmethod
    def authorize_by_telegram() -> None:
        user = User.get_or_none(User.mac == MAC)
        if not user:
            return
        for i in ConfirmLogin.select().where(ConfirmLogin.user == user):
            i.delete_instance()
        ConfirmLogin.create(user=user)


AuthSystem().authorize_by_telegram()
