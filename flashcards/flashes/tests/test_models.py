from flashcards.flashes.models import Flash


def test_flash_get_absolute_url():
    flash = Flash(id=5, title='Test flashcard', content='something not important')
    assert flash.get_absolute_url() == '/flashcards/5'


def test_flash_string():
    flash = Flash(id=5, title='Test flashcard', content='something not important')
    assert flash.title == str(flash)
    assert str(flash) == 'Test flashcard'
