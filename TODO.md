Implement more validators and tests for them
============================================

If you have your own idea, feel free to contact us or submit a merge request,
but here are some we know that are currently missing:

- **Check if provided bug trackers are valid**. We need a different validator
  for each bug tracker type, eg. one for GitHub issues, GitLab issues, Bugzillas
  etc.
  - The validator should pass if:
    - There is no bug tracker URL.
    - The provided bug tracker URL is valid. What "valid" means is specific to
      each tracker type, eg. for GitHub and GitLab issues it would mean the
      linked issue is open. For Bugzilla, it may mean the bug is open, assigned
      and contains acks (if the instance supports them) etc. The requirement on
      the actual existance of the bug is implied.
  - The validator option should be the base URL of the tracker, eg.
    `https://github.com/<project-name>` or `https://bugzilla.redhat.com`.
  - The validator should verify correctness of all the linked trackers, not
    only one. In case the patch solves multiple bugs, people may put more
    trackers into a single tag (separated by whitespace or `,`), or use multiple
    tags.
  - The validator should be able to deal with different acceptable formats of
    values. Eg. for GitHub issues, the value might be a direct link to the
    issue, a single number representing the issue or `#<number>`. Similarly for
    Bugzillas, it can be a link, a single number or something like `BZ123` or
    `BZ:123`.
  - Don't worry about trackers requiring a login, this is on the user to deal
    with.
- **Check the subject contains a required keyword**. There is more than a few
  projects which share a single mailing list or Patchwork project, and
  distinguishing between them is essential.
  - The validator should pass if the requested keyword or regex is present in
    the square brackets in the subject. Something like
    `.*\[.*<INSERT_OPTION_HERE>.*\].*` should work (not actually tested).
  - The option passed should be the expected string to be matched or a regex,
    similar to contains-keyval validator.
- **Generic patch dependency validator**. Check if a `Depends: <tag>` or similar
  field is present in the patch. If so, it usually means the patch depends on a
  different patch that is not merged yet and can't be tested properly without
  it.
  - The validator should fail if the patch depends on something else. The cover
    letter should be checked for the tags too.
  - The validator option should be either an empty string or a text/regex of
    other strings which should be checked.
    - By default, the validator should be checking for `Depends` and
      `Depends on`; but specific projects may also accept other things (which is
      what should be configurable by the option), eg. `Blocked by`.
- **Bugzilla patch dependency validator**.
  - Check if the `Bugzilla` (and accepted abbreviations) tag is present. If so,
    check if the linked bug has the "depends_on" field set. If so, verify those
    bugs are *not* in the "NEW", "ASSIGNED" or "POST" states. These states mean
    the patches for the bugs the currently checked patch depends on are not
    merged yet and the currently checked patch can't be properly tested.
  - Check if a `Depends`, `Depends on` or similar tag is present. This may
    contain the bugs we depend on directly. Check these for the states mentioned
    above.
  - The validator should fail if the patch is deemed to be dependent on patches
    that are not merged yet. The cover letter should be checked for the tags as
    well.
- **Mandatory cover letter for patch series**. If there are multiple patches in
  the checked series (passed to valligator), check if a cover letter is passed
  too.
  - The validator should fail if there is more than one patch and no cover.
- **No Bugzilla needed if the patch changes file X validator**. Some projects
  don't require a bug tracker for all the changes, eg. adding documentation or
  tests.
  - The validator option should be a file path or a regex of them.
  - The validator should check the patches for the list of modified files and
    see that only files that match it are changed. It should deal properly with
    the `a/b` prefixes git adds (these are not a part of the option).
  - The validator should pass if
    - There is a `Bugzilla|BZ` tag
    - There is no such tag but only files matching the option are modified.



Implement a way to run your own validator without it being part of the main repository
======================================================================================

In some cases, the code is super specific or contains too much internal data to
be published. That doesn't mean the people needing it don't have the right to
use them with valligator! We should have a way to specify custom validators,
residing in different files or directories, that are not included in
`__init__/VALLIDATORS`.

So, we need:
- A way for the user to specify which function to run from what file and with
  what option. The two can be separated, eg. having one option for including the
  validator and then specifying the option the same way as one from the default
  set.
- Actually being able to dynamically load and run the new validators.

