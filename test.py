#!/usr/local/bin/python
# coding: utf-8
import unittest

from ratebeer import RateBeer


class TestSearch(unittest.TestCase):
    def test_search(self):
        ''' Test out the search function with str and unicode searches '''
        results = RateBeer().search("deschutes inversion")
        self.assertListEqual(results['breweries'], [])
        self.assertIsNotNone(results['beers'])
        self.assertDictContainsSubset({
            'url': '/beer/deschutes-inversion-ipa/55610/',
            'name': u'Deschutes Inversion IPA',
            'id': 55610
        }, results['beers'][0])

        # Test a beer that requires encoding
        results = RateBeer().search("to øl jule mælk")
        self.assertListEqual(results['breweries'], [])
        self.assertIsNotNone(results['beers'])
        self.assertDictContainsSubset({
            'url': '/beer/to-ol-jule-maelk/235066/',
            'name': u'To Øl Jule Mælk',
            'id': 235066
        }, results['beers'][0])

    def test_beer_404(self):
        ''' Checks to make sure that we appropriately raise a page not found '''
        rb = RateBeer()
        self.assertRaises(rb.PageNotFound, rb.beer, "/beer/sdfasdf")
        self.assertIsNotNone(rb.beer("/beer/new-belgium-tour-de-fall/279122/"))

    def test_beer(self):
        ''' Make sure the results for a beer contain the expected data '''
        results = RateBeer().beer("/beer/new-belgium-tour-de-fall/279122/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'New Belgium Tour de Fall',
            'brewery': u'New Belgium Brewing Company',
            'brewery_url': u'/brewers/new-belgium-brewing-company/77/',
            'brewery_country': u'USA',
            'style': u'American Pale Ale',
            'ibu': 38
        }, results)

        results = RateBeer().beer("/beer/deschutes-inversion-ipa/55610/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'Deschutes Inversion IPA',
            'brewery': u'Deschutes Brewery',
            'brewery_url': u'/brewers/deschutes-brewery/233/',
            'brewery_country': u'USA',
            'style': u'India Pale Ale (IPA)',
            'ibu': 80
        }, results)

        results = RateBeer().beer("/beer/rochefort-trappistes-10/2360/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'Rochefort Trappistes 10',
            'brewery': u'Brasserie Rochefort',
            'brewery_url': u'/brewers/brasserie-rochefort/406/',
            'brewery_country': u'Belgium',
            'style': u'Abt/Quadrupel',
            'abv': 11.3
        }, results)

    def test_brewery(self):
        ''' Make sure the results for a brewery contain the expected data '''
        results = RateBeer().brewery("/brewers/deschutes-brewery/233/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'name': u'Deschutes Brewery',
            'type': u'Microbrewery',
            'city': u'Bend',
        }, results)

    def test_contract_brewery(self):
        ''' Beers brewed at contract brewers will have 'brewed_at' and
            'brewed_at_url' fields, in addition to the normal fields '''
        results = RateBeer().brewery("/brewers/minhas-craft-brewery/1185/")
        self.assertIsNotNone(results)
        self.assertDictContainsSubset({
            'brewed_at': u'Minhas Craft Brewery',
            'brewed_at_url': '/brewers/minhas-craft-brewery/1185/',
            'brewery': u'Berghoff Brewery Inc.',
            'brewery_url': '/brewers/berghoff-brewery-inc/15529/'
        }, results['beers'].next())

    def test_reviews(self):
        ''' Check to make multi-page review searches work properly '''
        reviews = [r for r in RateBeer().reviews("/beer/triumph-rauchbier/37254/")]
        self.assertIsNotNone(reviews)

if __name__ == '__main__':
    unittest.main()
