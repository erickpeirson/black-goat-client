import unittest, mock, json, os, sys


sys.path.append('.')
import goat
os.environ.setdefault('GOAT_WAIT_INTERVAL', '0.001')

goat.GOAT_APP_TOKEN = 'd22bbda9b5b507dc6cd032d80d6a3d299fda10fe'
goat.GOAT = 'http://127.0.0.1:8000'


class MockResponse(object):
    def __init__(self, content, status_code):
        self._status_code = status_code
        self.content = content

    def json(self):
        return json.loads(self.content)

    @property
    def status_code(self):
        return self._status_code


class MockSearchResponse(MockResponse):
    url = 'http://mock/url/'

    def __init__(self, parent, pending_content, success_content, max_calls=3,):
        self.max_calls = 3
        self.parent = parent
        self.pending_content = pending_content
        self.success_content = success_content

    def json(self):
        if self.parent.call_count < self.max_calls:
            return json.loads(self.pending_content)
        return json.loads(self.success_content)

    @property
    def status_code(self):
        if self.parent.call_count < self.max_calls:
            return 202
        return 200


class TestGoatAuthority(unittest.TestCase):
    @mock.patch('requests.get')
    def test_list(self, mock_get):
        goat.GOAT = 'http://goat.goat/goat'
        with open('tests/data/system_list.json', 'r') as f:
            mock_get.return_value = MockResponse(f.read(), 200)

        authorities = goat.GoatAuthority.list()

        args, kwargs = mock_get.call_args
        self.assertEqual(mock_get.call_count, 1,
                         "Should make a single GET request.")
        self.assertEqual(goat.GOAT + '/authority/', args[0],
                         "Should call the ``/authority/`` endpoint.")
        self.assertEqual(len(authorities), 3,
                         "There should be 3 items in the result set.")
        for authority in authorities:
            self.assertIsInstance(authority, goat.GoatAuthority,
                                  "Each of which should be a GoatAuthority.")

    @mock.patch('requests.post')
    def test_create(self, mock_post):
        goat.GOAT = 'http://goat.goat/goat'
        with open('tests/data/authority_created.json', 'r') as f:
            mock_post.return_value = MockResponse(f.read(), 201)

        authority = goat.GoatAuthority(name='GoatTest', description='The Test')
        authority.create()
        self.assertTrue(authority.id is not None)


class TestGoatIdentitySystem(unittest.TestCase):
    @mock.patch('requests.get')
    def test_list(self, mock_get):
        goat.GOAT = 'http://goat.goat/goat'
        with open('tests/data/system_list.json', 'r') as f:
            mock_get.return_value = MockResponse(f.read(), 200)

        systems = goat.GoatIdentitySystem.list()
        args, kwargs = mock_get.call_args
        self.assertEqual(mock_get.call_count, 1,
                         "Should make a single GET request.")
        self.assertEqual(goat.GOAT + '/identitysystem/', args[0],
                         "Should call the ``/identitysystem/`` endpoint.")
        self.assertEqual(len(systems), 3,
                         "There should be 3 items in the result set.")
        for system in systems:
            self.assertIsInstance(system, goat.GoatIdentitySystem,
                                  "Each of which should be a"
                                  " GoatIdentitySystem.")

    @mock.patch('requests.post')
    def test_create(self, mock_post):
        with open('tests/data/system_created.json', 'r') as f:
            mock_post.return_value = MockResponse(f.read(), 201)

        goat.GOAT = 'http://127.0.0.1:8000'
        system = goat.GoatIdentitySystem(name='GoatTest', description='The Test')
        system.create()

        self.assertTrue(system.id is not None)


class TestGoatIdentity(unittest.TestCase):
    @mock.patch('requests.get')
    def test_list(self, mock_get):
        goat.GOAT = 'http://goat.goat/goat'
        with open('tests/data/identity_list.json', 'r') as f:
            mock_get.return_value = MockResponse(f.read(), 200)

        identities = goat.GoatIdentity.list()
        args, kwargs = mock_get.call_args

        self.assertEqual(mock_get.call_count, 1,
                         "Should make a single GET request.")
        self.assertEqual(goat.GOAT + '/identity/', args[0],
                         "Should call the ``/identity/`` endpoint.")
        self.assertEqual(len(identities), 7,
                         "There should be 7 items in the result set.")

    @mock.patch('requests.post')
    def test_create(self,  mock_post):
        goat.GOAT = 'http://goat.goat/goat'
        with open('tests/data/identity_created.json', 'r') as f:
            mock_post.return_value = MockResponse(f.read(), 201)

        identity = goat.GoatIdentity(name='GoatTest', concepts=['http://test.com/test3/', 'http://test.com/test2/'], part_of=4)
        identity.create()

        self.assertTrue(identity.id is not None)


class TestGoatConcept(unittest.TestCase):
    @mock.patch('requests.get')
    def test_list(self, mock_get):
        goat.GOAT = 'http://goat.goat/goat'

        with open('tests/data/concept_list_response.json', 'r') as f:
            mock_get.return_value = MockResponse(f.read(), 200)

        concepts = goat.GoatConcept.list()
        args, kwargs = mock_get.call_args

        self.assertEqual(mock_get.call_count, 1,
                         "Should make a single GET request.")
        self.assertEqual(goat.GOAT + '/concept/', args[0],
                         "Should call the ``/concept/`` endpoint.")
        self.assertEqual(len(concepts), 19,
                         "There should be 19 items in the result set.")
        for concept in concepts:
            self.assertIsInstance(concept, goat.GoatConcept,
                                  "Each of which should be a GoatConcept.")

    @mock.patch('requests.get')
    def test_search(self, mock_get):
        with open('tests/data/concept_search_results.json', 'r') as f:
            with open('tests/data/concept_search_created.json', 'r') as f2:
                mock_get.return_value = MockSearchResponse(mock_get, f2.read(), f.read(), 200)

        max_calls = 3

        concepts = goat.GoatConcept.search(q='Bradshaw')
        self.assertEqual(mock_get.call_count, max_calls,
                         "Should keep calling if status code 202 is received.")
        args, kwargs =  mock_get.call_args
        self.assertEqual(args[0], MockSearchResponse.url,
                         "Should follow the redirect URL.")
        self.assertEqual(len(concepts), 10,
                         "There should be 10 items in the result set.")
        for concept in concepts:
            self.assertIsInstance(concept, goat.GoatConcept,
                                  "Each of which should be a GoatConcept.")

    @mock.patch('requests.post')
    def test_create(self, mock_post):
        with open('tests/data/concept_created.json', 'r') as f:
            mock_post.return_value = MockResponse(f.read(), 201)

        concept = goat.GoatConcept(name='GoatTest', identifier='http://test.com/test3/')
        concept.create()

        self.assertTrue(concept.id is not None)

    @mock.patch('requests.get')
    def test_identical(self, mock_get):
        goat.GOAT = 'http://goat.goat/goat'

        with open('tests/data/concept_identical.json', 'r') as f:
            mock_get.return_value = MockResponse(f.read(), 200)

        concepts = goat.GoatConcept.identical(identifier='http://test.com/test3/')

        args, kwargs = mock_get.call_args

        self.assertEqual(mock_get.call_count, 1,
                         "Should make a single GET request.")
        self.assertEqual(goat.GOAT + '/identical/', args[0],
                         "Should call the ``/identical/`` endpoint.")
        self.assertEqual(len(concepts), 2,
                         "There should be 2 items in the result set.")
        for concept in concepts:
            self.assertIsInstance(concept, goat.GoatConcept,
                                  "Each of which should be a GoatConcept.")


if __name__ == '__main__':
    unittest.main()
