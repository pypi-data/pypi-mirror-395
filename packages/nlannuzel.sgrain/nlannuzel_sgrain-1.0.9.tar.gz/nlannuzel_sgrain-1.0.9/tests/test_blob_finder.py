import unittest
from nlannuzel.sgrain.graph import Color, Image, BLACK, BlobFinder

class TestBlobFinder(unittest.TestCase):
    def test_find_blob(self):
        image = Image(rows = [[Color.grey(v) for v in row] for row in [
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ],
            [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0 ],
            [ 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0 ],
            [ 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0 ],
            [ 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0 ],
            [ 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0 ],
            [ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            ]])
        self.assertEqual(image.width, 17)
        self.assertEqual(image.height, 9)

        count = 0
        for p in image.iter_area():
            if p.col != BLACK:
                count += 1
        self.assertEqual(count, 61)

        finder = BlobFinder(image)
        def count_blobs_of_size(n):
            count = 0
            for blob in finder.blobs:
                if len(blob) == n:
                    count += 1
            return count

        def blobs_overlap(b1, b2):
            for p1 in b1:
                for p2 in b2:
                    if p1.i == p2.i and p1.j == p2.j:
                        return True
            return False

        def blobs_are_contiguous(b1, b2):
            for p1 in b1:
                for p2 in b2:
                    if p1.i - 1 == p2.i and p1.j == p2.j:  # left
                        return True
                    if p1.i == p2.i and p1.j - 1 == p2.j:  # up
                        return True
                    if p1.i + 1 == p2.i and p1.j == p2.j:  # right
                        return True
                    if p1.i == p2.i and p1.j + 1 == p2.j:  # down
                        return True
            return False

        def no_contiguous_blobs():
            blobs = finder.blobs
            for k1 in range(0, len(blobs)):
                for k2 in range(0, len(blobs)):
                    if k1 == k2:
                        continue
                    if blobs_overlap(blobs[k1], blobs[k2]):
                        raise RuntimeError(f"{k1} overlaps with{k2}")
                    if blobs_are_contiguous(blobs[k1], blobs[k2]):
                        raise RuntimeError(f"{k1} and {k2} are contiguous: {blobs[k1]} {blobs[k2]}")
            return True

        self.assertTrue(no_contiguous_blobs())
        self.assertEqual(len(finder.blobs), 8)
        self.assertEqual(count_blobs_of_size(25), 1)
        self.assertEqual(count_blobs_of_size(18), 1)
        self.assertEqual(count_blobs_of_size(6), 2)
        self.assertEqual(count_blobs_of_size(2), 2)
        self.assertEqual(count_blobs_of_size(1), 2)
if __name__ == '__main__':
    unittest.main()
