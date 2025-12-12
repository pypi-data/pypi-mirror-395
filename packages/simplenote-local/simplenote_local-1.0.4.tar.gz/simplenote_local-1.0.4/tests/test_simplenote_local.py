"""Tests for SimplenoteLocal class functionality."""

import os
import pickle
from unittest.mock import Mock, patch

import pytest

from simplenote_local import SimplenoteLocal, Note


@pytest.fixture
def mock_simplenote():
    """Mock the Simplenote API client."""
    with patch('simplenote_local.Simplenote') as mock_class:
        mock_instance = Mock()
        mock_class.return_value = mock_instance
        mock_instance.get_note_list.return_value = ([], 0)
        mock_instance.current = ''
        yield mock_instance


@pytest.fixture
def notes_dir(tmp_path):
    """Provide a temporary directory for note storage."""
    directory = tmp_path / "notes"
    directory.mkdir()
    return directory


@pytest.fixture
def local(notes_dir, mock_simplenote):
    """Provide a SimplenoteLocal instance with mocked API."""
    return SimplenoteLocal(
        directory=str(notes_dir),
        user='test@example.com',
        password='testpass',
    )


class TestGetNoteByFilename:
    """Tests for SimplenoteLocal.get_note_by_filename() method."""

    def test_finds_exact_match(self, local):
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'My Note.txt',
                'deleted': False,
            }),
        }
        result = local.get_note_by_filename('My Note.txt')
        assert result is not None
        assert result.key == 'key1'

    def test_finds_case_insensitive_match(self, local):
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'My Note.txt',
                'deleted': False,
            }),
        }
        result = local.get_note_by_filename('my note.txt')
        assert result is not None
        assert result.key == 'key1'

    def test_returns_none_for_no_match(self, local):
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Other Note.txt',
                'deleted': False,
            }),
        }
        result = local.get_note_by_filename('My Note.txt')
        assert result is None

    def test_skips_deleted_notes(self, local):
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'My Note.txt',
                'deleted': True,
            }),
        }
        result = local.get_note_by_filename('My Note.txt')
        assert result is None


class TestGetLocalNoteState:
    """Tests for SimplenoteLocal.get_local_note_state() method."""

    def test_detects_new_file(self, local, notes_dir):
        # Create a file that's not in the notes dict
        note_path = notes_dir / "New Note.txt"
        note_path.write_text("This is a new note")

        local.notes = {}
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].state == 'new'
        assert states[0].filename == 'New Note.txt'

    def test_detects_unchanged_file(self, local, notes_dir):
        note_path = notes_dir / "Existing Note.txt"
        note_path.write_text("Body content")
        mtime = int(os.path.getmtime(str(note_path)))

        import hashlib
        fingerprint = hashlib.sha256(b"Body content").hexdigest()

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Existing Note.txt',
                'title': 'Existing Note',
                'modificationDate': mtime,
                'fingerprint': fingerprint,
                'deleted': False,
            }),
        }
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].state == 'unchanged'

    def test_detects_changed_file_by_mtime(self, local, notes_dir):
        note_path = notes_dir / "Changed Note.txt"
        note_path.write_text("Body content")

        import hashlib
        fingerprint = hashlib.sha256(b"Body content").hexdigest()

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Changed Note.txt',
                'title': 'Changed Note',
                'modificationDate': 0,  # old timestamp
                'fingerprint': fingerprint,
                'deleted': False,
            }),
        }
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].state == 'changed'

    def test_detects_changed_file_by_content(self, local, notes_dir):
        note_path = notes_dir / "Changed Note.txt"
        note_path.write_text("New content")
        mtime = int(os.path.getmtime(str(note_path)))

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Changed Note.txt',
                'title': 'Changed Note',
                'modificationDate': mtime,
                'fingerprint': 'oldhash',
                'deleted': False,
            }),
        }
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].state == 'changed'

    def test_detects_deleted_file(self, local, notes_dir):
        # Note exists in dict but not on disk
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Deleted Note.txt',
                'title': 'Deleted Note',
                'deleted': False,
            }),
        }
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].state == 'deleted'

    def test_ignores_hidden_files(self, local, notes_dir):
        (notes_dir / ".hidden.txt").write_text("hidden")
        (notes_dir / "Visible Note.txt").write_text("visible")

        local.notes = {}
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].filename == 'Visible Note.txt'

    def test_ignores_non_txt_files(self, local, notes_dir):
        (notes_dir / "readme.md").write_text("markdown")
        (notes_dir / "Real Note.txt").write_text("note")

        local.notes = {}
        states = local.get_local_note_state()

        assert len(states) == 1
        assert states[0].filename == 'Real Note.txt'


class TestSaveAndRemoveNoteFile:
    """Tests for file save/remove operations."""

    def test_save_note_file_creates_file(self, local, notes_dir):
        note = Note({
            'filename': 'New Note.txt',
            'title': 'New Note',
            'body': 'Note body content',
            'modificationDate': 1234567890,
        })

        local.save_note_file(note)

        note_path = notes_dir / "New Note.txt"
        assert note_path.exists()
        assert note_path.read_text() == 'Note body content'

    def test_save_note_file_updates_mtime(self, local, notes_dir):
        note = Note({
            'filename': 'Timed Note.txt',
            'title': 'Timed Note',
            'body': 'content',
            'modificationDate': 1234567890,
        })

        local.save_note_file(note)

        note_path = notes_dir / "Timed Note.txt"
        assert int(os.path.getmtime(str(note_path))) == 1234567890

    def test_remove_note_file_deletes_file(self, local, notes_dir):
        note_path = notes_dir / "To Delete.txt"
        note_path.write_text("content")

        note = Note({
            'filename': 'To Delete.txt',
        })

        local.remove_note_file(note, quiet=True)

        assert not note_path.exists()

    def test_remove_note_file_handles_missing_file(self, local, notes_dir):
        note = Note({
            'filename': 'Nonexistent.txt',
        })
        # Should not raise
        local.remove_note_file(note, quiet=True)


class TestFindMatchingNotes:
    """Tests for SimplenoteLocal.find_matching_notes() method."""

    def test_matches_by_tag(self, local, notes_dir):
        (notes_dir / "Tagged Note.txt").write_text("content")

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Tagged Note.txt',
                'title': 'Tagged Note',
                'tags': ['work', 'important'],
                'deleted': False,
            }),
            'key2': Note({
                'key': 'key2',
                'filename': 'Other Note.txt',
                'title': 'Other Note',
                'tags': ['personal'],
                'deleted': False,
            }),
        }

        matches = local.find_matching_notes(['#work'])
        assert len(matches) == 1
        assert matches[0].key == 'key1'

    def test_matches_by_filename_with_space(self, local, notes_dir):
        (notes_dir / "Shopping List.txt").write_text("content")
        (notes_dir / "Other Note.txt").write_text("content")

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Shopping List.txt',
                'title': 'Shopping List',
                'deleted': False,
            }),
            'key2': Note({
                'key': 'key2',
                'filename': 'Other Note.txt',
                'title': 'Other Note',
                'deleted': False,
            }),
        }

        matches = local.find_matching_notes(['Shopping List'])
        assert len(matches) == 1
        assert matches[0].key == 'key1'

    def test_matches_by_word_in_cache(self, local, notes_dir):
        (notes_dir / "Python Tutorial.txt").write_text("content")
        (notes_dir / "Java Guide.txt").write_text("content")

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Python Tutorial.txt',
                'title': 'Python Tutorial',
                'deleted': False,
            }),
            'key2': Note({
                'key': 'key2',
                'filename': 'Java Guide.txt',
                'title': 'Java Guide',
                'deleted': False,
            }),
        }
        local.words = {
            'python': ['Python Tutorial.txt'],
            'tutorial': ['Python Tutorial.txt'],
            'java': ['Java Guide.txt'],
            'guide': ['Java Guide.txt'],
        }

        matches = local.find_matching_notes(['python'])
        assert len(matches) == 1
        assert matches[0].key == 'key1'

    def test_matches_intersection_of_criteria(self, local, notes_dir):
        (notes_dir / "Python Tutorial.txt").write_text("content")
        (notes_dir / "Python Reference.txt").write_text("content")

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Python Tutorial.txt',
                'title': 'Python Tutorial',
                'tags': ['learning'],
                'deleted': False,
            }),
            'key2': Note({
                'key': 'key2',
                'filename': 'Python Reference.txt',
                'title': 'Python Reference',
                'tags': ['reference'],
                'deleted': False,
            }),
        }
        local.words = {
            'python': ['Python Tutorial.txt', 'Python Reference.txt'],
            'tutorial': ['Python Tutorial.txt'],
            'reference': ['Python Reference.txt'],
        }

        matches = local.find_matching_notes(['python', '#learning'])
        assert len(matches) == 1
        assert matches[0].key == 'key1'

    def test_sorts_by_pinned_then_modified(self, local, notes_dir):
        import hashlib

        (notes_dir / "Old Pinned.txt").write_text("content")
        (notes_dir / "New Unpinned.txt").write_text("content")
        (notes_dir / "Old Unpinned.txt").write_text("content")

        # Set file mtimes to match the modificationDate values
        os.utime(notes_dir / "Old Pinned.txt", (1000, 1000))
        os.utime(notes_dir / "New Unpinned.txt", (3000, 3000))
        os.utime(notes_dir / "Old Unpinned.txt", (2000, 2000))

        fingerprint = hashlib.sha256(b"content").hexdigest()

        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Old Pinned.txt',
                'title': 'Old Pinned',
                'modificationDate': 1000,
                'fingerprint': fingerprint,
                'systemTags': ['pinned'],
                'tags': ['sorttest'],
                'deleted': False,
            }),
            'key2': Note({
                'key': 'key2',
                'filename': 'New Unpinned.txt',
                'title': 'New Unpinned',
                'modificationDate': 3000,
                'fingerprint': fingerprint,
                'systemTags': [],
                'tags': ['sorttest'],
                'deleted': False,
            }),
            'key3': Note({
                'key': 'key3',
                'filename': 'Old Unpinned.txt',
                'title': 'Old Unpinned',
                'modificationDate': 2000,
                'fingerprint': fingerprint,
                'systemTags': [],
                'tags': ['sorttest'],
                'deleted': False,
            }),
        }

        matches = local.find_matching_notes(['#sorttest'])
        # Pinned first, then by modified date descending
        assert len(matches) == 3
        assert matches[0].key == 'key1'  # pinned
        assert matches[1].key == 'key2'  # newer
        assert matches[2].key == 'key3'  # older


class TestWordsCache:
    """Tests for word cache operations."""

    def test_add_to_words_cache_extracts_words(self, local):
        local.words = {}
        local.add_to_words_cache('Test Note.txt', 'Hello world this is a test')

        assert 'hello' in local.words
        assert 'world' in local.words
        assert 'test' in local.words
        assert 'Test Note.txt' in local.words['hello']

    def test_add_to_words_cache_ignores_short_words(self, local):
        local.words = {}
        local.add_to_words_cache('Test Note.txt', 'a to is the an')

        # Words with 2 or fewer chars should not be indexed
        assert 'a' not in local.words
        assert 'to' not in local.words
        assert 'is' not in local.words
        assert 'an' not in local.words
        assert 'the' in local.words  # 3 chars, should be included

    def test_add_to_words_cache_truncates_long_words(self, local):
        local.words = {}
        long_word = 'x' * 100
        local.add_to_words_cache('Test Note.txt', long_word)

        # Words should be truncated to 60 chars
        assert ('x' * 60) in local.words
        assert long_word not in local.words

    def test_remove_file_from_words_cache(self, local):
        local.words = {
            'hello': ['Note1.txt', 'Note2.txt'],
            'world': ['Note1.txt'],
        }

        local.remove_file_from_words_cache('Note1.txt')

        assert 'Note1.txt' not in local.words['hello']
        assert 'Note2.txt' in local.words['hello']
        assert 'Note1.txt' not in local.words['world']

    def test_add_replaces_previous_entries(self, local):
        local.words = {
            'oldword': ['Test Note.txt'],
        }

        local.add_to_words_cache('Test Note.txt', 'newword content')

        assert 'Test Note.txt' not in local.words.get('oldword', [])
        assert 'Test Note.txt' in local.words['newword']


class TestDataPersistence:
    """Tests for load_data() and save_data() methods."""

    def test_save_and_load_round_trip(self, local, notes_dir):
        local.notes = {
            'key1': Note({
                'key': 'key1',
                'filename': 'Test Note.txt',
                'title': 'Test Note',
                'tags': ['tag1', 'tag2'],
                'modificationDate': 1234567890,
                'deleted': False,
            }),
        }
        local.cursor = 'cursor123'
        local.words = {'test': ['Test Note.txt']}

        local.save_data()

        # Reload
        notes, cursor, words = local.load_data()

        assert 'key1' in notes
        assert notes['key1'].filename == 'Test Note.txt'
        assert notes['key1'].tags == ['tag1', 'tag2']
        assert cursor == 'cursor123'
        assert words == {'test': ['Test Note.txt']}

    def test_load_data_handles_missing_file(self, local, notes_dir):
        # Ensure no data file exists
        data_path = notes_dir / "notes.data"
        if data_path.exists():
            data_path.unlink()

        notes, cursor, words = local.load_data()

        assert notes == {}
        assert cursor == ''
        assert words == {}

    def test_save_creates_pickle_file(self, local, notes_dir):
        local.notes = {}
        local.cursor = ''
        local.words = {}

        local.save_data()

        assert (notes_dir / "notes.data").exists()

    def test_save_creates_toml_file(self, local, notes_dir):
        local.notes = {}
        local.cursor = ''
        local.words = {}

        local.save_data()

        assert (notes_dir / "notes.toml").exists()


class TestAPIInteractions:
    """Tests for Simplenote API interactions with mocked client."""

    def test_send_note_update_calls_api(self, local, mock_simplenote):
        mock_simplenote.update_note.return_value = (
            {
                'key': 'newkey123',
                'content': "Test Title\n\nTest body",
                'modificationDate': 1234567890,
                'creationDate': 1234567800,
                'version': 1,
                'tags': [],
                'systemTags': [],
            },
            0,
        )

        note = Note({
            'content': "Test Title\n\nTest body",
            'modificationDate': 1234567890,
            'creationDate': 1234567800,
            'tags': ['work'],
            'systemTags': ['markdown'],
        })

        result = local.send_note_update(note)

        mock_simplenote.update_note.assert_called_once()
        call_args = mock_simplenote.update_note.call_args[0][0]
        assert call_args['content'] == "Test Title\n\nTest body"
        assert call_args['tags'] == ['work']
        assert call_args['systemTags'] == ['markdown']
        assert result.key == 'newkey123'

    def test_send_note_update_includes_key_for_existing(self, local, mock_simplenote):
        mock_simplenote.update_note.return_value = (
            {
                'key': 'existingkey',
                'content': "Updated\n\nbody",
                'modificationDate': 1234567890,
                'version': 2,
            },
            0,
        )

        note = Note({
            'key': 'existingkey',
            'version': 1,
            'content': "Updated\n\nbody",
        })

        local.send_note_update(note)

        call_args = mock_simplenote.update_note.call_args[0][0]
        assert call_args['key'] == 'existingkey'
        assert call_args['version'] == 1

    def test_send_note_update_raises_on_error(self, local, mock_simplenote):
        mock_simplenote.update_note.return_value = ('Error message', -1)

        note = Note({
            'content': "Test\n\nbody",
            'filename': 'Test.txt',
        })

        with pytest.raises(Exception) as exc_info:
            local.send_note_update(note)
        assert 'Error updating note' in str(exc_info.value)

    def test_trash_note_calls_api(self, local, mock_simplenote):
        mock_simplenote.trash_note.return_value = (
            {
                'key': 'key123',
                'deleted': True,
            },
            0,
        )

        note = Note({
            'key': 'key123',
            'filename': 'Test Note.txt',
        })

        result = local.trash_note(note)

        mock_simplenote.trash_note.assert_called_once_with('key123')
        assert result['deleted'] is True

    def test_trash_note_raises_on_error(self, local, mock_simplenote):
        mock_simplenote.trash_note.return_value = ('Error message', -1)

        note = Note({
            'key': 'key123',
            'filename': 'Test Note.txt',
        })

        with pytest.raises(Exception) as exc_info:
            local.trash_note(note)
        assert 'Error deleting' in str(exc_info.value)

    def test_get_note_updates_calls_api(self, local, mock_simplenote):
        mock_simplenote.get_note_list.return_value = (
            [
                {
                    'key': 'key1',
                    'content': "Note 1\n\nbody",
                    'creationDate': 1000,
                    'modificationDate': 2000,
                },
                {
                    'key': 'key2',
                    'content': "Note 2\n\nbody",
                    'creationDate': 500,
                    'modificationDate': 1500,
                },
            ],
            0,
        )
        mock_simplenote.current = 'newcursor'

        local.cursor = 'oldcursor'
        updates = local.get_note_updates()

        mock_simplenote.get_note_list.assert_called_with(since='oldcursor')
        # Should be sorted by creation date
        assert updates[0]['key'] == 'key2'  # created earlier
        assert updates[1]['key'] == 'key1'
        assert local.cursor == 'newcursor'

    def test_get_note_updates_raises_on_error(self, local, mock_simplenote):
        mock_simplenote.get_note_list.return_value = ([], -1)

        with pytest.raises(Exception) as exc_info:
            local.get_note_updates()
        assert 'API error' in str(exc_info.value)

    def test_fetch_changes_creates_new_note(self, local, mock_simplenote, notes_dir):
        mock_simplenote.get_note_list.return_value = (
            [
                {
                    'key': 'newkey',
                    'content': "New Note\n\nThis is new content",
                    'creationDate': 1234567800,
                    'modificationDate': 1234567890,
                    'version': 1,
                    'tags': [],
                    'systemTags': [],
                    'deleted': False,
                },
            ],
            0,
        )
        mock_simplenote.current = 'cursor1'

        local.notes = {}
        local.fetch_changes()

        assert 'newkey' in local.notes
        assert local.notes['newkey'].title == 'New Note'
        note_path = notes_dir / "New Note.txt"
        assert note_path.exists()

    def test_fetch_changes_updates_existing_note(self, local, mock_simplenote, notes_dir):
        # Create existing file
        (notes_dir / "Existing Note.txt").write_text("old content")

        mock_simplenote.get_note_list.return_value = (
            [
                {
                    'key': 'existingkey',
                    'content': "Existing Note\n\nUpdated content",
                    'creationDate': 1234567800,
                    'modificationDate': 1234567900,
                    'version': 2,
                    'tags': [],
                    'systemTags': [],
                    'deleted': False,
                },
            ],
            0,
        )
        mock_simplenote.current = 'cursor1'

        local.notes = {
            'existingkey': Note({
                'key': 'existingkey',
                'filename': 'Existing Note.txt',
                'title': 'Existing Note',
                'version': 1,
                'deleted': False,
            }),
        }

        local.fetch_changes()

        assert local.notes['existingkey'].version == 2
        note_path = notes_dir / "Existing Note.txt"
        assert note_path.read_text() == "Updated content"

    def test_fetch_changes_handles_deleted_note(self, local, mock_simplenote, notes_dir):
        # Create existing file
        note_path = notes_dir / "To Delete.txt"
        note_path.write_text("content")

        mock_simplenote.get_note_list.return_value = (
            [
                {
                    'key': 'deletekey',
                    'content': "To Delete\n\ncontent",
                    'creationDate': 1234567800,
                    'modificationDate': 1234567900,
                    'version': 2,
                    'tags': [],
                    'systemTags': [],
                    'deleted': True,
                },
            ],
            0,
        )
        mock_simplenote.current = 'cursor1'

        local.notes = {
            'deletekey': Note({
                'key': 'deletekey',
                'filename': 'To Delete.txt',
                'title': 'To Delete',
                'version': 1,
                'deleted': False,
            }),
        }

        local.fetch_changes()

        assert local.notes['deletekey'].deleted is True
        assert not note_path.exists()

    def test_fetch_changes_resolves_filename_conflict(self, local, mock_simplenote, notes_dir):
        # Create existing file with same name
        (notes_dir / "Duplicate.txt").write_text("existing content")

        mock_simplenote.get_note_list.return_value = (
            [
                {
                    'key': 'newkey',
                    'content': "Duplicate\n\nNew content with same title",
                    'creationDate': 1234567800,
                    'modificationDate': 1234567890,
                    'version': 1,
                    'tags': [],
                    'systemTags': [],
                    'deleted': False,
                },
            ],
            0,
        )
        mock_simplenote.current = 'cursor1'

        local.notes = {
            'otherkey': Note({
                'key': 'otherkey',
                'filename': 'Duplicate.txt',
                'title': 'Duplicate',
                'deleted': False,
            }),
        }

        local.fetch_changes()

        # New note should get incremented filename
        assert local.notes['newkey'].filename == 'Duplicate.1.txt'
        assert (notes_dir / "Duplicate.1.txt").exists()
