import unittest

import app
from settings import site_down

class IsReachableTestCase(unittest.TestCase):
    """Tests the is_reachable function."""
    
    def test_is_google_reachable(self):
        result = app.is_reachable('www.google.com')
        self.assertTrue(result)
    
    def test_is_nonsense_reachable(self):
        result = app.is_reachable('ishskbeosjei.com')
        self.assertFalse(result)

class GetStatusCodeTestCase(unittest.TestCase):
    """Tests the get_status_code function."""
    
    def test_google_status_code(self):
        result = app.get_status_code('https://www.google.com')
        self.assertEqual(result, 200)
    
    def test_404_status_code(self):
        result = app.get_status_code('https://www.bbc.co.uk/404')
        self.assertEqual(result, 404)
    
class CheckSingleURLTestCase(unittest.TestCase):
    """Tests the check_single_url function"""
    
    def test_bbc_sport_url(self):
        result = app.check_single_url('http://www.bbc.co.uk/sport')
        self.assertEqual(result, '200')
    
    def test_nonsense_url(self):
        result = app.check_single_url('https://ksjsjsbdk.ievrygqlsp.com')
        self.assertEqual(result, site_down)
    
    def test_timeout_url(self):
        result = app.check_single_url('https://www.bbc.co.uk:90')
        self.assertEqual(result, site_down)
    
    def test_connrefused_url(self):
        result = app.check_single_url('http://127.0.0.1:8080')
        self.assertEqual(result, site_down)

class CheckMultipleURLsTestCase(unittest.TestCase):
    """Tests the check_multiple_urls function"""
    
    def test_check_multiple_url(self):
        app.checkurls = {
"BBC": [
        "https://www.bbc.co.uk", 
        "http://doesnotexist.bbc.co.uk",
        "https://www.bbc.co.uk/404"
        ],
"Google": [
        "https://www.google.com",
        "http://localhost:8080"
        ]
}
        expected = {
"https://www.bbc.co.uk": "200",
"http://doesnotexist.bbc.co.uk": "UNREACHABLE",
"https://www.bbc.co.uk/404": "404",
"https://www.google.com": "200",
"http://localhost:8080": "UNREACHABLE",
}
        result = app.check_multiple_urls()
        self.assertEqual(result, expected)

unittest.main()