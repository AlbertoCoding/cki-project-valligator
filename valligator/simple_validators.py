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


def subject_contains_keyval(cover, patches, key):
    """ Example function to start with the tool  """

    #pattern = re.compile(r'^{}Subject:\s+\S+'.format(key), re.I | re.M)
    #if pattern.search(cover)
    subject_pos = cover.find("Subject:")

    cover_lines = cover.split('\n')

#    cover_lines = cover.getlines()
    for line in cover_lines:
        pos = line.find("Subject:")
        if pos != -1:
            print("Printing subject content:")
            print(line[pos+len("Subject:"):])

#    print()
    #print(cover[subject_pos:end_subject_line])
    to_return = True
    return to_return
