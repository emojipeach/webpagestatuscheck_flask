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
    
    @unittest.skip("takes too long, reenable if necessary")
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
        app.list_urls = app.generate_list_urls(app.checkurls)
        
        expected = {
"https://www.bbc.co.uk": "200",
"http://doesnotexist.bbc.co.uk": "UNREACHABLE",
"https://www.bbc.co.uk/404": "404",
"https://www.google.com": "200",
"http://localhost:8080": "UNREACHABLE",
}
        result = app.check_multiple_urls()
        self.assertEqual(result, expected)
        
class CompareSubmittedTestCase(unittest.TestCase):
    """Tests the compare_submitted function."""
    
    def test_known_submitted_url(self):
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
        submitted = 'https://www.bbc.co.uk'
        result = app.compare_submitted(submitted)
        self.assertEqual(submitted, result[1])
        self.assertTrue(result[0])
        
    def test_unknown_submitted_url(self):
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
        submitted = 'https://unknown.com'
        result = app.compare_submitted(submitted)
        self.assertEqual(submitted, result[1])
        self.assertFalse(result[0])
    
    def test_whitespace_stripping_submitted_url(self):
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
        submitted = '  https://www.bbc.co.uk   '
        result = app.compare_submitted(submitted)
        self.assertEqual('https://www.bbc.co.uk', result[1])
        self.assertTrue(result[0])

class HTTPSStartStripTestCase(unittest.TestCase):
    """Tests the https_start_strip function."""
    
    def test_google_url(self):
        result = app.https_start_strip('https://www.google.com')
        self.assertEqual(result, 'https://www.google.com')
    
    def test_whitespace_url(self):
        result = app.https_start_strip('       https://www.google.com    ')
        self.assertEqual(result, 'https://www.google.com')

    def test_no_https_url(self):
        result = app.https_start_strip('www.google.com')
        self.assertEqual(result, 'https://www.google.com')
    
    def test_uppercase_url(self):
        result = app.https_start_strip('HTTPS://WWW.GOOGLE.COM')
        self.assertEqual(result, 'https://www.google.com')


unittest.main()