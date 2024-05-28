from model.models import Note


class User:
    def __init__(self, chat_id, username, email=None, idnp=None, notes: list[Note] = None):
        self._idnp = idnp
        self._email = email
        self._notes = notes
        self._chat_id = chat_id
        self._username = username

    @property
    def username(self):
        return self._username

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def email(self):
        return self._email

    @property
    def idnp(self):
        return self._idnp

    @idnp.setter
    def idnp(self, idnp):
        self._idnp = idnp

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @classmethod
    def from_dict(cls, item):
        return cls(item['_chat_id'], item['_username'], item['_email'], item['_idnp']) if item else None
