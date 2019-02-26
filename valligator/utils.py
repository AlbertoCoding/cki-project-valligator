"""Various utilities and common code."""
import logging
import os
import urllib.parse

import requests


class UnexpectedResponse(Exception):
    """Got an unexpected response from web server."""


def get_content(path, session):
    """
    Read the file from the passed path or URL.

    Args:
        path:    URL or filepath.
        session: Patchwork session in case the patches reside in a private
                 Patchwork instance.

    Returns: A string representing contents of the file.

    Raises:
        UnexpectedResponse if path is an URL which can't be reached.
        IOError or OSError if path is a filepath that can't be read.
    """
    try:
        if session:
            response = session.get(path)
        else:
            response = requests.get(path)

        if response.status_code == 200:
            return response.content.decode()

        # We always expect the status 200. If the URL redirects, it's
        # suspicious too.
        raise UnexpectedResponse('Unexpected response {} from {} !'.format(
            response.status_code, path
        ))
    except requests.RequestException:
        logging.debug('File path `%s` detected.', path)

    with open(path, 'r') as opened_file:
        return opened_file.read()


def login_to_patchwork(patchwork_url):
    """
    Use environment variables `PATCHWORK_LOGIN` and `PATCHWORK_PASSWORD` to log
    in to Patchwork to retrieve the patches.

    Args:
        patchwork_url: Base URL of the Patchwork instance.

    Raises:
        Exception if the environment variables are not found.
        UnexpectedResponse if the login didn't work.

    Returns:
        A requests.Session object to be used with the patch retrieval.
    """
    login = os.getenv('PATCHWORK_LOGIN')
    password = os.getenv('PATCHWORK_PASSWORD')
    if not (login and password):
        raise Exception(
            'PATCHWORK_LOGIN or PATCHWORK_PASSWORD envvar is missing!'
        )

    user_data = urllib.parse.urlencode({'username': login,
                                        'password': password})
    session = requests.session()
    response = session.post(
        urllib.parse.urljoin(patchwork_url, 'accounts/login/'),
        data=user_data
    )
    if response.status_code != 200:
        raise UnexpectedResponse(
            'Can\'t login to Patchwork: got {} !'.format(response.status_code)
        )

    return session
