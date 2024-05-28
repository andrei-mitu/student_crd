from typing import List

from database.client.MongoClientI import MongoClientI
from database.repository.CrudRepository import CrudRepository
from model.entity.user import User
from model.models import Course, Note
from service.web import notes


class UserRepository(CrudRepository):
    def __init__(self):
        super().__init__(MongoClientI(), 'users')

    def find_by_chat_id(self, _id):
        exists: List = super().find_all_by_column('_chat_id', _id)
        if exists is None or exists == []:
            return None
        return User.from_dict(exists[0])

    def exists(self, _id):
        return super().find(_id) is not None

    def notes(self, _id, semester=None) -> list[Note]:
        user: User = User.from_dict(super().find(_id))
        if user is None:
            raise ValueError(f'User with id {_id} not found')
        if user.notes:
            return user.notes
        else:
            actual = notes.get(user.idnp, semester)
            user.notes = actual
            super().update(user)
            return actual
