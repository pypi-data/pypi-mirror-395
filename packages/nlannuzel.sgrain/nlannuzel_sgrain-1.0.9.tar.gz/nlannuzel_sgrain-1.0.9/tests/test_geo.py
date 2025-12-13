import unittest
from nlannuzel.sgrain.geo import Location

class TestLoc(unittest.TestCase):
    def test_distance(self):
        merlion = Location(1.2868012156184587, 103.85447217129732)
        changi_jewel = Location(1.3600993711358866, 103.98980701072115)
        flyer = Location(1.289366192868755, 103.86315734141414)
        woodland_checkpoint = Location(1.4453921110423973, 103.76891392488915)
        self.assertAlmostEqual(merlion.distance_to(changi_jewel), 17.11, 1)
        self.assertAlmostEqual(merlion.distance_to(flyer), 1.01, 1)
        self.assertAlmostEqual(flyer.distance_to(changi_jewel), 16.12, 1)
        self.assertAlmostEqual(woodland_checkpoint.distance_to(changi_jewel), 26.32, 1)

if __name__ == '__main__':
    unittest.main()
