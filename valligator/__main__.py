"""valligator runner."""
import argparse
import logging
import sys
from yaml import load, Loader

from . import VALIDATORS
from . import utils


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.DEBUG,
                        stream=sys.stdout)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser(description='Patch validation')
    for validator in VALIDATORS.keys():
        parser.add_argument('--' + validator, action='append', default=[])
    parser.add_argument('--cover-letter', type=str)
    parser.add_argument(
        '--login',
        action='store_true',
        help=('Use environment variables `PATCHWORK_LOGIN` and '
              '`PATCHWORK_PASSWORD` to log in to Patchwork to retrieve the '
              'patches.')
    )
    parser.add_argument(
        '--config',
        type=str,
        help='YAML configuration in the format `validator: list-of-options`'
    )

    opts, patchlist = parser.parse_known_args()
    if opts.config:
        with open(opts.config) as config_file:
            config = load(config_file, Loader=Loader)

        # Check the provided config file doesn't contain invalid validators
        for validator in config.keys():
            if validator not in VALIDATORS:
                raise ValueError(
                    'Invalid validator in configuration file: {}!'.format(
                        validator
                    )
                )
    else:
        config = {}

    session = None
    if opts.login:
        # Grab any of the patches and get the base Patchwork URL.
        patchwork_url = patchlist[0].rsplit('patch', 1)[0]
        session = utils.login_to_patchwork(patchwork_url)

    cover = ''
    patches = []
    if opts.cover_letter:
        cover = utils.get_content(opts.cover_letter, session)
    for patch in patchlist:
        patches.append(utils.get_content(patch, session))

    failed_validations = 0
    for validator in VALIDATORS.keys():
        validator_arguments = getattr(opts, validator.replace('-', '_'))
        config_arguments = config.get(validator, [])
        for argument in validator_arguments + config_arguments:
            if not VALIDATORS[validator](cover, patches, argument):
                failed_validations += 1

    return failed_validations


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
