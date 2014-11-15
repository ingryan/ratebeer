import unittest

from ratebeer import RateBeer


class TestSearch(unittest.TestCase):
    def test_search(self):
        results = RateBeer().search("deschutes inversion")
        self.assertListEqual(results['breweries'], [])
        self.assertIsNotNone(results['beers'])
        self.assertDictContainsSubset({
            'url': '/beer/deschutes-inversion-ipa/55610/', 
            'name': u'Deschutes Inversion IPA', 
            'id': '55610'
        }, results['beers'][0])

    def test_beer_404(self):
        rb = RateBeer()
        self.assertRaises(rb.PageNotFound, rb.beer, "/beer/sdfasdf")
        self.assertIsNotNone(rb.beer("/beer/new-belgium-tour-de-fall/279122/"))

    def test_beer(self):
        results = RateBeer().beer("/beer/new-belgium-tour-de-fall/279122/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'New Belgium Tour de Fall',
            'brewery': u'New Belgium Brewing Company',
            'brewery_url': u'/brewers/new-belgium-brewing-company/77/',
            'style': u'American Pale Ale',
            'ibu': u'38'
        }, results)

        results = RateBeer().beer("/beer/deschutes-inversion-ipa/55610/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'Deschutes Inversion IPA',
            'brewery': u'Deschutes Brewery',
            'brewery_url': u'/brewers/deschutes-brewery/233/',
            'style': u'India Pale Ale (IPA)',
            'ibu': u'80'
        }, results)

    def test_brewery(self):
        results = RateBeer().brewery("/brewers/deschutes-brewery/233/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'Deschutes Brewery',
            'type': u'Microbrewery',
            'city': u'Bend',
        }, results)

    def test_reviews(self):
        reviews = RateBeer().reviews("/beer/deschutes-inversion-ipa/55610/")
        self.assertIsNotNone(reviews)
        self.assertEqual(len(reviews), 10)

        reviews = RateBeer().reviews("/beer/deschutes-inversion-ipa/55610/", pages=2)
        self.assertIsNotNone(reviews)
        self.assertEqual(len(reviews), 20)
        self.assertNotEqual(reviews[0]['text'], reviews[-1]['text'])

if __name__ == '__main__':
    unittest.main()
