valligator -- a framework for email patch series validation
===========================================================

insert a cute logo with alligator here

Do you have a list of rules which the patches should follow? A specific format
of subject, metadata present in the commit message, links to bug trackers?
valligator will make it easier for you to write a plugin to impose any rules
needed and validate a patch or email. Pick any combination of validators and
run valligator against the patch series or single patches.


How to run the validator
------------------------

valligator uses Python 3.7. The usual command line would look like

```
python3.7 -m valligator [<--validator> <option>] ... \
                        [--cover-letter <path_or_url>] \
                        <patch_1_path_or_url> ... <patch_n_path_or_url>
```

A validator can be specified multiple times with different options (or even the
same ones, but not sure what you'd like to solve with that :) ).

All validators take a string argument so quote it if you use weird symbols.
A configuration YAML is supported so the validators and their options don't
need to be specified on the command line all the time.

```
python3.7 -m valligator --config <path> \
                        [--cover-letter <path_or_url>] \
                        <patch_1_path_or_url> ... <patch_n_path_or_url>
```

Then, a YAML configuration file would use a list syntax:

```
validator_1:
  - "option_1"
  - "option_2"
validator_2:
  - "option_1"
```

Configuration file and command line arguments are combined, so you can specify
a configuration file with validators but can add some more checks on the command
line if you wish. Cover letter and patches can only be specified on the command
line.


A list of currently existing validators
---------------------------------------

* `--contains-keyval <key>`: Check if a `<key>: value` line is present in the
  patch. This is useful eg. if each patch needs to contain a link to a bug
  tracker. The check is case-insensitive. `<key>` can be a regex, eg.
  `Bugzilla|BZ` is a valid option. The validator passes if a cover letter is
  passed and contains the key.



Developer info
==============

Feel free to add new validators! If possible, make them generic (like the
`contains-keyval` validator), but don't be afraid to propose more specific
complex validators either.

* Write tests for your validator! The GitLab CI contains a coverage report so
  you can just check the pipeline logs to see what is missing, no need to run
  anything yourself.
* Add the validator into the list of validators above, with a brief explanation
  of what it checks.
* Add the validator option and function call to the `VALIDATORS` dictionary in
  `valligator/__init__.py` file.
* Each validator should take 3 arguments, in this order:
  * cover -- A string representing the text of the cover letter. Empty string
    if no cover letter was passed.
  * patches -- a list of strings representing the passed patches.
  * option -- string option the validator takes
* The `cover` and `patches` are split on purpose, so you have an easy time
  implementing validators that only check cover letters, or consider patches
  passing if a cover letter itself passes the validator.
* The validator should return `False` if it fails and `True` if it passes. This
  goes hand in hand with the user-friendly naming of the options, which should
  state what the validator does. Does the patch contain a keyval? Yes (`True`)
  or no (`False`)? You get the idea ;)
* If the validator is more complicated, please use a separate file for it.
