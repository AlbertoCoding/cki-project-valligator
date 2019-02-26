"""Tests for valligator.simple_validators."""
import re
import unittest

from valligator import simple_validators


class TestContainsKeyval(unittest.TestCase):
    """Tests for simple_validators.contains_keyval()."""
    def test_no_keyval(self):
        """Verify contains_keyval fails if the key is not present."""
        patch = 'This is a sample text in the patch'
        self.assertFalse(
            simple_validators.contains_keyval('', [patch], 'key')
        )

    def test_keyval_missing_patch(self):
        """
        Verify contains_keyval fails if the key is not present in all patches.
        """
        patch_true = 'text\nkey: value'
        patch_false = 'This is a sample text in the patch'
        self.assertFalse(simple_validators.contains_keyval(
            '', [patch_true, patch_false], 'key'
        ))

    def test_keyval_in_cover(self):
        """Verify contains_keyval passes if the key is in the cover."""
        cover = 'text\nkey: value'
        patch = 'This is a sample text in the patch'
        self.assertTrue(
            simple_validators.contains_keyval(cover, [patch], 'key')
        )

    def test_keyval_in_patches(self):
        """
        Verify contains_keyval passes if the key is present in all patches.
        """
        patches = ['text\nkey: value', 'something\n\nkey: value2\n\n']
        self.assertTrue(
            simple_validators.contains_keyval('', patches, 'key')
        )
