"""Tests for valligator.utils"""
import os
import unittest

import mock
import requests
import responses

from valligator import utils


class TestGetContent(unittest.TestCase):
    """Tests for utils.get_content()."""
    @responses.activate
    def test_url_valid(self):
        """Verify get_content works when a valid URL is passed."""
        url = 'http://url.org/patch'
        patch_body = 'patch body'
        responses.add(responses.GET, url, status=200, body=patch_body)
        self.assertEqual(patch_body, utils.get_content(url, None))

    @responses.activate
    def test_url_with_session(self):
        """Verify get_content works when a valid URL and session is passed."""
        url = 'http://url.org/patch'
        patch_body = 'patch body'
        session = requests.session()

        responses.add(responses.GET, url, status=200, body=patch_body)
        self.assertEqual(patch_body, utils.get_content(url, session))

    @responses.activate
    def test_url_invalid(self):
        """
        Verify get_content raises an exception if it gets unexpected response
        from the server.
        """
        url = 'http://url.org/patch'
        responses.add(responses.GET, url, status=500)
        with self.assertRaises(utils.UnexpectedResponse):
            utils.get_content(url, None)

    @mock.patch('builtins.open',
                new_callable=mock.mock_open,
                read_data='patch data')
    def test_filepath_valid(self, mock_file):
        """Verify get_content works if a valid filepath is passed."""
        self.assertEqual('patch data', utils.get_content('path', None))

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_filepath_invalid(self, mock_open):
        """
        Verify get_content raises an exception if it fails to open the file.
        """
        mock_open.side_effect = IOError
        with self.assertRaises(IOError):
            utils.get_content('nonexistent_file', None)


class TestPatchworkLogin(unittest.TestCase):
    """Tests for utils.login_to_patchwork()."""
    def test_no_variables(self):
        """Verify an Exception is raised if required variables are missing."""
        with self.assertRaises(Exception):  # Missing login
            utils.login_to_patchwork('url')

        os.environ.update({'PATCHWORK_LOGIN': 'username'})
        with self.assertRaises(Exception):  # Missing password
            utils.login_to_patchwork('url')

        del os.environ['PATCHWORK_LOGIN']

    @responses.activate
    def test_bad_login(self):
        """
        Verify an UnexpectedResponse is raised if the Patchwork instance
        returns bad response (eg. unable to login).
        """
        patchwork_url = 'http://patchwork.test/'
        responses.add(responses.POST,
                      patchwork_url + 'accounts/login/',
                      status=500)

        os.environ.update({'PATCHWORK_LOGIN': 'username',
                           'PATCHWORK_PASSWORD': 'password'})

        with self.assertRaises(utils.UnexpectedResponse):
            utils.login_to_patchwork(patchwork_url)

        del os.environ['PATCHWORK_LOGIN']
        del os.environ['PATCHWORK_PASSWORD']

    @responses.activate
    def test_valid_login(self):
        """Verify a session is returned if the login succeeds."""
        patchwork_url = 'http://patchwork.test/'
        responses.add(responses.POST,
                      patchwork_url + 'accounts/login/',
                      status=200)

        os.environ.update({'PATCHWORK_LOGIN': 'username',
                           'PATCHWORK_PASSWORD': 'password'})

        returned = utils.login_to_patchwork(patchwork_url)
        self.assertIsInstance(returned, requests.Session)

        del os.environ['PATCHWORK_LOGIN']
        del os.environ['PATCHWORK_PASSWORD']
