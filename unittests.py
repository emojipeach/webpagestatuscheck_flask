import unittest

from test import is_reachable, get_status_code, check_single_url

class IsReachableTestCase(unittest.TestCase):
    """Tests the is_reachable function."""
    
    def test_is_google_reachable(self):
        result = is_reachable('www.google.com')
        self.assertTrue(result)
    
    def test_is_nonsense_reachable(self):
        result = is_reachable('ishskbeosjei.com')
        self.assertFalse(result)

class GetStatusCodeTestCase(unittest.TestCase):
    """Tests the get_status_code function."""
    
    def test_google_status_code(self):
        result = get_status_code('https://www.google.com')
        self.assertEqual(result, 200)
    
    def test_404_status_code(self):
        result = get_status_code('https://www.bbc.co.uk/404')
        self.assertEqual(result, 404)
    
class CheckSingleURLTestCase(unittest.TestCase):
    """Tests the check_single_url function"""
    
    def test_bbc_sport_url(self):
        result = check_single_url('http://www.bbc.co.uk/sport')
        self.assertEqual(result, '200')
    
    def test_nonsense_url(self):
        result = check_single_url('https://ksjsjsbdk.ievrygqlsp.com')
        self.assertEqual(result, 'UNREACHABLE')
    
    def test_timeout_url(self):
        result = check_single_url('https://www.bbc.co.uk:90')
        self.assertEqual(result, 'UNREACHABLE')
    
    def test_connrefused_url(self):
        result = check_single_url('http://127.0.0.1:8080')
        self.assertEqual(result, 'UNREACHABLE')

unittest.main()