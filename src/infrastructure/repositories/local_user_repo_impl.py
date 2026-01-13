from src.domain.entities.user.user import User
from src.domain.entities.user.user_repo import UserRepo


class LocalUserRepoImpl(UserRepo):

    @property
    def user(self) -> User:
        return User(id=1, name="COG CHE Front")
