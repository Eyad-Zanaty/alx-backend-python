#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures

"""Unittest module for GithubOrgClient class"""
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"mocked": True}),
        ("abc", {"mocked": True})
    ])
    @patch('client.get_json', return_value={"mocked": True})
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that .org() returns the correct payload"""
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct url from org payload"""
        client = GithubOrgClient("testorg")
        fake_org = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=fake_org
        ):
            self.assertEqual(client._public_repos_url, fake_org["repos_url"])

    @patch('client.get_json', return_value=[{"name": "repo1", "license": {"key": "r1"}},
                                           {"name": "repo2", "license": {"key": "r2"}}])
    def test_public_repos(self, mock_get_json):
        """Test .public_repos() returns repo names and calls correct properties"""
        client = GithubOrgClient("org")
        fake_url = "https://api.github.com/orgs/org/repos"
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value=fake_url) as mock_url:
            repos = client.public_repos()
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)
            self.assertIsInstance(repos, list)
            self.assertEqual(sorted(repos), ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos
        )
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to return fixture JSONs"""
        cls.get_patcher = patch('client.requests.get')
        mocked_get = cls.get_patcher.start()
        # define side_effect based on URL
        def get_side_effect(url, *args, **kwargs):
            mock_resp = unittest.mock.Mock()
            if url.endswith('/orgs/octocat'):
                mock_resp.json.return_value = cls.org_payload
            else:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp
        mocked_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: .public_repos returns expected repos"""
        client = GithubOrgClient("octocat")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: filter by apache-2.0 license"""
        client = GithubOrgClient("octocat")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
    #!/usr/bin/env python3


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns correct org data"""
        mock_get_json.return_value = self.org_payload
        client = GithubOrgClient("google")
        self.assertEqual(client.org, self.org_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns expected repository list"""
        mock_get_json.return_value = self.repos_payload
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = self.org_payload
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), self.expected_repos)
            mock_get_json.assert_called_once()

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos method returns repos with specific license"""
        mock_get_json.return_value = self.repos_payload
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = self.org_payload
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(license="apache-2.0"),
                self.apache2_repos
            )
            mock_get_json.assert_called_once()

