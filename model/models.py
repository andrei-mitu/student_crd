class Note:
    def __init__(self, note_type, note):
        self._note_type = note_type
        self._note = note

    @property
    def note_type(self):
        return self._note_type

    @property
    def note(self):
        return self._note


class Course:
    def __init__(self, course_name, course_notes: list[Note]):
        self._course_name = course_name
        self._course_notes = course_notes

    @property
    def course_name(self):
        return self._course_name

    @property
    def course_notes(self):
        return self._course_notes
