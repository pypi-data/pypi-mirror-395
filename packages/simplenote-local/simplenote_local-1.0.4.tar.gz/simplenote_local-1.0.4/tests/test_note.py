"""Tests for Note class functionality."""

from simplenote_local import Note


class TestTitleAndBody:
    """Tests for Note.title_and_body() class method."""

    def test_simple_text(self):
        title, body = Note.title_and_body("First line\n\nBody text here.")
        assert title == "First line"
        assert body == "Body text here."

    def test_single_line(self):
        title, body = Note.title_and_body("Just a title")
        assert title == "Just a title"
        assert body == "\n"

    def test_long_first_line_trims_on_word_boundary(self):
        long_line = "This is a very long first line that exceeds sixty characters and should be trimmed"
        title, body = Note.title_and_body(long_line + "\n\nBody")
        assert len(title) <= 61
        assert title == "This is a very long first line that exceeds sixty characters"
        assert body.startswith("and")

    def test_long_first_line_no_spaces(self):
        long_line = "x" * 70
        title, body = Note.title_and_body(long_line + "\n\nBody")
        assert len(title) == 61
        assert title == "x" * 61

    def test_strips_forbidden_characters(self):
        title, body = Note.title_and_body("Title/with:forbidden*chars«and»more\n\nBody")
        assert title == "Titlewithforbiddencharsandmore"

    def test_strips_markdown_header_prefix(self):
        title, body = Note.title_and_body("## Markdown Header\n\nBody text")
        assert title == "Markdown Header"

    def test_converts_nbsp_to_space(self):
        title, body = Note.title_and_body("Title\xa0with\xa0nbsp\n\nBody")
        assert title == "Title with nbsp"

    def test_converts_cr_to_lf(self):
        title, body = Note.title_and_body("Title\r\n\r\nBody\rwith\rCR")
        assert title == "Title"
        assert "Body\nwith\nCR" in body

    def test_strips_leading_whitespace_from_title(self):
        title, body = Note.title_and_body("   Indented title\n\nBody")
        assert title == "Indented title"

    def test_body_without_double_newline_prefix(self):
        title, body = Note.title_and_body("Title\n\nBody starts here")
        assert not body.startswith("\n")
        assert body == "Body starts here"

    def test_empty_content(self):
        title, body = Note.title_and_body("")
        assert title == ""
        assert body == "\n"

    def test_overflow_goes_to_body(self):
        # Line is 66 chars, gets trimmed to last word boundary within 61 chars
        long_line = "Short title that fits well but then has extra words that overflow"
        title, body = Note.title_and_body(long_line + "\n\nMore body")
        # Trimmed at word boundary within first 61 chars
        assert title == "Short title that fits well but then has extra words that"
        assert body.startswith("overflow")


class TestIncrementFilename:
    """Tests for Note.increment_filename() method."""

    def test_first_increment(self):
        note = Note({'filename': 'test.txt'})
        note.increment_filename()
        assert note.filename == "test.1.txt"

    def test_second_increment(self):
        note = Note({'filename': 'test.1.txt'})
        note.increment_filename()
        assert note.filename == "test.2.txt"

    def test_double_digit_increment(self):
        note = Note({'filename': 'test.9.txt'})
        note.increment_filename()
        assert note.filename == "test.10.txt"

    def test_increment_with_dots_in_name(self):
        note = Note({'filename': 'my.note.txt'})
        note.increment_filename()
        assert note.filename == "my.note.1.txt"

    def test_increment_dotted_name_already_incremented(self):
        note = Note({'filename': 'my.note.5.txt'})
        note.increment_filename()
        assert note.filename == "my.note.6.txt"


class TestTagList:
    """Tests for Note.tag_list property."""

    def test_empty_tags(self):
        note = Note({'tags': []})
        assert note.tag_list == ""

    def test_single_tag(self):
        note = Note({'tags': ['work']})
        assert note.tag_list == "#work"

    def test_multiple_tags(self):
        note = Note({'tags': ['work', 'important']})
        assert note.tag_list == "#work #important"

    def test_excludes_email_addresses(self):
        note = Note({'tags': ['work', 'user@example.com', 'important']})
        assert note.tag_list == "#work #important"

    def test_only_email_addresses(self):
        note = Note({'tags': ['user@example.com', 'other@test.org']})
        assert note.tag_list == ""


class TestShareList:
    """Tests for Note.share_list property."""

    def test_empty_tags(self):
        note = Note({'tags': []})
        assert note.share_list == ""

    def test_no_email_addresses(self):
        note = Note({'tags': ['work', 'important']})
        assert note.share_list == ""

    def test_single_email(self):
        note = Note({'tags': ['user@example.com']})
        assert note.share_list == "user@example.com"

    def test_multiple_emails(self):
        note = Note({'tags': ['user@example.com', 'other@test.org']})
        assert note.share_list == "user@example.com other@test.org"

    def test_mixed_tags_and_emails(self):
        note = Note({'tags': ['work', 'user@example.com', 'important']})
        assert note.share_list == "user@example.com"


class TestPublishedUrl:
    """Tests for Note.published_url property."""

    def test_with_publish_url(self):
        note = Note({'publishURL': 'abc123'})
        assert note.published_url == "https://app.simplenote.com/p/abc123"

    def test_without_publish_url(self):
        note = Note({})
        assert note.published_url == ""


class TestNoteSerialisation:
    """Tests for Note as_dict() and __init__() round-trip."""

    def test_round_trip_preserves_data(self):
        original = Note({
            'tags': ['work', 'important'],
            'deleted': False,
            'shareURL': 'share123',
            'publishURL': 'pub456',
            'systemTags': ['pinned', 'markdown'],
            'modificationDate': 1234567890,
            'creationDate': 1234567800,
            'key': 'notekey123',
            'version': 5,
            'title': 'Test Note',
            'filename': 'Test Note.txt',
            'fingerprint': 'abc123hash',
        })

        restored = Note(original.as_dict())

        assert restored.tags == original.tags
        assert restored.deleted == original.deleted
        assert restored.share_url == original.share_url
        assert restored.publish_url == original.publish_url
        assert restored.system_tags == original.system_tags
        assert restored.modified == original.modified
        assert restored.created == original.created
        assert restored.key == original.key
        assert restored.version == original.version
        assert restored.title == original.title
        assert restored.filename == original.filename
        assert restored.fingerprint == original.fingerprint

    def test_init_with_content_derives_title_and_body(self):
        note = Note({
            'content': "My Title\n\nMy body text here.",
        })
        assert note.title == "My Title"
        assert note.body == "My body text here."
        assert note.fingerprint is not None

    def test_init_without_content_constructs_it(self):
        note = Note({
            'title': 'Given Title',
            'body': 'Given body',
        })
        assert note.content == "Given Title\n\nGiven body"

    def test_init_defaults(self):
        note = Note({})
        assert note.tags == []
        assert note.deleted is False
        assert note.share_url == ''
        assert note.publish_url == ''
        assert note.system_tags == []
        assert note.modified == 0
        assert note.created == 0
        assert note.key == ''
        assert note.version == 0
        assert note.title == 'new note'

    def test_fingerprint_is_sha256_of_body(self):
        import hashlib
        content = "Title\n\nBody content"
        note = Note({'content': content})
        expected_hash = hashlib.sha256(note.body.encode('utf-8')).hexdigest()
        assert note.fingerprint == expected_hash
