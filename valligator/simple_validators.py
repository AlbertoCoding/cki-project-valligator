"""Simple one-function validators."""
import logging
import re


def contains_keyval(cover, patches, key):
    """ Check if a 'key: <value>' is present. """
    pattern = re.compile(r'^{}:\s+\S+'.format(key), re.I | re.M)

    if pattern.search(cover):
        print("Pattern found in cover_letter")
        return True
    else:
        print("Pattern not found in cover_letter")

    to_return = True
    for index, patch in enumerate(patches):
        if not pattern.search(patch):
            logging.error('Patch %d doesn\'t contain %s!', index + 1, key)
            to_return = False

    return to_return


def check_bug_trackers(cover, patches, key):
    """ Check if provided bug trackers are valid  """

    return to_return


def ntimes_keyword(cover, key):
    """ Number of time a word appears in the text """
    pos = 0
    ntimes_key = 0
    new_init = 0

    while pos != -1:
        pos = cover[new_init:].find(key)
        if pos != -1:
            ntimes_key += 1
            new_init += pos+len(key)
        else:
            return ntimes_key


def subject_contains_keyword(cover, patches, key):
    """ Check the subject contains a required keyword  """

    subject_content = ""
    to_return = False

    print("The term 'Subject:' appears " +
          str(ntimes_keyword(cover, "Subject:")) +
          " times in the cover letter")

    cover_lines = cover.split('\n')
    for line in cover_lines:
        subject_pos = line.find("Subject:")
        if subject_pos != -1:
            subject_content = line[subject_pos+len("Subject:"):]
#           print(subject_content)
        if subject_content.find(key) != -1:
            to_return = True

    if to_return:
        print("Keyword " + key + " found in 'Subject:' content")
    else:
        print("Keyword " + key + " not found in 'Subject:' content")

    return to_return
