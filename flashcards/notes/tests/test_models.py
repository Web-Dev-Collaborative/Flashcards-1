from flashcards.notes.models import Note


def test_flash_get_absolute_url():
    note = Note(id=5, title='Test flashcard', content='something not important')
    assert note.get_absolute_url() == '/notes/5'


def test_flash_string():
    note = Note(id=5, title='Test flashcard', content='something not important')
    assert note.title == str(note)
    assert str(note) == 'Test flashcard'
