"""Patch validation."""
from . import simple_validators

VALIDATORS = {
    'contains-keyval': simple_validators.contains_keyval,
    'check-trackers': simple_validators.check_bug_trackers,
    'subject-contains-keyword': simple_validators.subject_contains_keyword
}
