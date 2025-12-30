from src.domain.entities.user.user import User
from src.domain.entities.user.user_facade import UserFacade


class UserRepo(UserFacade):

    def get_current(self) -> User:
        return User(id=1, name="COG CHE Front")
