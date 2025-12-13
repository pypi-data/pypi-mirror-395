import unittest
from nlannuzel.sgrain.graph import Color, Pixel, Box, BLACK, RED

class TestGraph(unittest.TestCase):
    def test_color(self):
        self.assertTrue(Color.grey(111).is_grey())
        self.assertTrue(BLACK.is_grey())
        self.assertFalse(RED.is_grey())

    def test_posterize(self):

        palette = [Color(r, g, b) for r, g, b, in [
            [0  , 0  , 0],
            [255, 0  , 0],
            [255, 255, 0],
        ]]

        self.assertEqual( Color(0  , 0  , 0  ).posterize(palette), 0 )
        self.assertEqual( Color(1  , 1  , 1  ).posterize(palette), 0 )
        self.assertEqual( Color(127, 0  , 0  ).posterize(palette), 0 )
        self.assertEqual( Color(128, 0  , 0  ).posterize(palette), 1 )
        self.assertEqual( Color(254, 0  , 0  ).posterize(palette), 1 )
        self.assertEqual( Color(255, 0  , 0  ).posterize(palette), 1 )
        self.assertEqual( Color(255, 127, 0  ).posterize(palette), 1 )
        self.assertEqual( Color(255, 128, 0  ).posterize(palette), 2 )
        self.assertEqual( Color(254, 254, 0  ).posterize(palette), 2 )
        self.assertEqual( Color(255, 255, 0  ).posterize(palette), 2 )
        self.assertEqual( Color(255, 255, 255).posterize(palette), 2 )

    def test_distance(self):
        a = Color(0, 0, 0)
        b = Color(127, 0, 0)
        c = Color(255, 0, 0)
        d = Color(0, 127, 0)
        self.assertTrue(a.distance_to(b) < a.distance_to(c))
        self.assertEqual(a.distance_to(b), a.distance_to(d))

    def test_box(self):
        with self.assertRaises(RuntimeError):
            b = Box.from_coordinates(0, 0, 0, 0)
        with self.assertRaises(RuntimeError):
            b = Box.from_coordinates(0, 0, 0, 10)
        with self.assertRaises(RuntimeError):
            b = Box.from_coordinates(0, 0, 10, 0)
        with self.assertRaises(RuntimeError):
            b = Box.from_coordinates(10, 10, 5, 5)

        a = []
        b = Box.from_coordinates(0, 0, 1, 1)
        for i in b.iter_width():
            a.append(i)
        self.assertEqual( len(a), 2 )
        self.assertEqual( a[0], 0 )
        self.assertEqual( a[1], 1 )

        a = []
        b = Box.from_coordinates(0, 0, 5, 3)
        for i in b.iter_width():
            a.append(i)
        self.assertEqual( len(a), 6 )
        self.assertEqual( a[0], 0 )
        self.assertEqual( a[1], 1 )
        self.assertEqual( a[2], 2 )
        self.assertEqual( a[3], 3 )
        self.assertEqual( a[4], 4 )
        self.assertEqual( a[5], 5 )

        a = []
        b = Box.from_coordinates(0, 0, 1, 1)
        for i in b.iter_height():
            a.append(i)
        self.assertEqual( len(a), 2 )
        self.assertEqual( a[0], 0 )
        self.assertEqual( a[1], 1 )

        a = []
        b = Box.from_coordinates(0, 0, 5, 3)
        for i in b.iter_width():
            a.append(i)
        self.assertEqual( len(a), 6 )
        self.assertEqual( a[0], 0 )
        self.assertEqual( a[1], 1 )
        self.assertEqual( a[2], 2 )
        self.assertEqual( a[3], 3 )
        self.assertEqual( a[4], 4 )
        self.assertEqual( a[5], 5 )

        a = []
        b = Box.from_coordinates(3, 4, 5, 6)
        for i, j in b.iter_area():
            a.append([i, j])
        self.assertEqual( len(a), 9 )

        self.assertEqual( a[0][0], 3 )
        self.assertEqual( a[0][1], 4 )

        self.assertEqual( a[1][0], 4 )
        self.assertEqual( a[1][1], 4 )

        self.assertEqual( a[2][0], 5 )
        self.assertEqual( a[2][1], 4 )

        self.assertEqual( a[3][0], 3 )
        self.assertEqual( a[3][1], 5 )

        self.assertEqual( a[4][0], 4 )
        self.assertEqual( a[4][1], 5 )

        self.assertEqual( a[5][0], 5 )
        self.assertEqual( a[5][1], 5 )

        self.assertEqual( a[6][0], 3 )
        self.assertEqual( a[6][1], 6 )

        self.assertEqual( a[7][0], 4 )
        self.assertEqual( a[7][1], 6 )

        self.assertEqual( a[8][0], 5 )
        self.assertEqual( a[8][1], 6 )

        a = []
        b = Box.from_coordinates(3, 4, 5, 6)
        for i, j in b.iter_boundary():
            a.append([i, j])
        self.assertEqual( len(a), 8 )  # 6 + 6 + 1 + 1

    def test_angle(self):
        a = Pixel(5, 5)
        with self.assertRaises(RuntimeError):
            a.angle_to(Pixel(5, 5))
        self.assertAlmostEqual(a.angle_to(Pixel(5 , 0 )), 0  )
        self.assertAlmostEqual(a.angle_to(Pixel(10, 0 )), 45 )
        self.assertAlmostEqual(a.angle_to(Pixel(10, 5 )), 90 )
        self.assertAlmostEqual(a.angle_to(Pixel(10, 10)), 135)
        self.assertAlmostEqual(a.angle_to(Pixel(5 , 10)), 180)
        self.assertAlmostEqual(a.angle_to(Pixel(0 , 10)), 225)
        self.assertAlmostEqual(a.angle_to(Pixel(0 , 5 )), 270)
        self.assertAlmostEqual(a.angle_to(Pixel(0 , 0 )), 315)

if __name__ == '__main__':
    unittest.main()
