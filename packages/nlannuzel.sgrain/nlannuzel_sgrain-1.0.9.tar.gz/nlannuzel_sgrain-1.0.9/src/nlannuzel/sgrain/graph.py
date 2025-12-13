"""Classes for basic in-memory image handling"""
from math import atan, degrees


class Color:
    """A color stored as either a grey level, or red, green, blue 8
    bits components"""
    def __init__(self, r, g, b):
        """Build a new Color object from r, g, and b components
        between 0 and 255"""

        if r is None or g is None or b is None:
            raise Exception("some colors are missing")
        for c in (r, g, b):
            if c < 0:
                raise Exception("color cannot be negative")
        if r == b and r == g and b == g:
            # grey level
            self.g = g
            self.r = None
            return
        self.r = r
        self.g = g
        self.b = b

    def is_grey(self):
        return self.r is None

    def __repr__(self):
        if self.is_grey():
            return f"Color({self.g})"
        return f"Color({self.r},{self.r},{self.b})"

    def distance_to(self, other):
        """returns the distance between this color and another one"""
        if self.is_grey():
            if other.is_grey():
                return ( 3*(other.g - self.g)**2 )**0.5
            return ((other.r - self.g)**2 + (other.g - self.g)**2 + (other.b - self.g)**2)**0.5
        if other.is_grey():
            return ((other.g - self.r)**2 + (other.g - self.g)**2 + (other.g - self.g)**2)**0.5
        return ((other.r - self.r)**2 + (other.g - self.g)**2 + (other.b - self.b)**2)**0.5

    def posterize(self, palette):
        """find the closest color in a palette, and return the index
        of the color in the palette.

        parameters:
          palette: tuples of Color
        returns:
          position of the nearest color in the palette
        """
        min_d = None
        for i in range(0, len(palette)):
            d = self.distance_to(palette[i])
            if min_d is None or min_d > d:
                min_d = d
                min_i = i
        return min_i

    @classmethod
    def grey(cls, level):
        """returns a grey level from black to white"""
        return cls(level, level, level)

    def __eq__(self, other):
        """returns True if this Color represents the same color as the
        other one, and False otherwise"""
        if self.is_grey():
            if other.is_grey():
                return self.g == other.g
            return False
        if other.is_grey():
            return False
        if self.r != other.r:
            return False
        if self.g != other.g:
            return False
        if self.b != other.b:
            return False
        return True


BLACK   = Color( 0  , 0  , 0   )
WHITE   = Color( 255, 255, 255 )
RED     = Color( 255, 0  , 0   )
GREEN   = Color( 0  , 255, 0   )
BLUE    = Color( 0  , 0  , 255 )
YELLOW  = Color( 255, 255, 0   )
PURPLE  = Color( 255, 0  , 255 )
CYAN    = Color( 0  , 255, 255 )


class Pixel:
    """A set of i and j coordinates, and optionally a Color"""
    def __init__(self, i, j, col=None):
        if i < 0 or j < 0:
            raise Exception("coordinates cannot be negative")
        self.i = i
        self.j = j
        self.col = col

    def __repr__(self):
        s = f"Pixel({self.i},{self.j})"
        if self.col is not None:
            s += f" = {self.col}"
        return s

    def distance_to(self, other):
        """distance to another pixel"""
        return ((other.i - self.i)**2 + (other.j - self.j)**2)**0.5

    def angle_to(self, other):
        """angle in dgrees of a line formed by this pixel and another
        pixel, counted clockwise, with 0 at 12 o'clock"""
        if other.i == self.i:
            if other.j == self.j:
                raise RuntimeError("no angle between identical points")
            return 0 if other.j < self.j else 180
        elif other.j == self.j:
            return 90 if other.i > self.i else 270

        offset = 90 if other.i > self.i else 270
        return offset + degrees(atan((other.j - self.j) / (other.i - self.i)))


class Box:
    """an area in the image represented by two pixels at the top-left
    (tl) and bottom-right (br)"""
    def __init__(self, tl, br):
        if br.i <= tl.i or br.j <= tl.j:
            raise RuntimeError("invalid box")
        self.tl = tl
        self.br = br

    @classmethod
    def from_coordinates(cls, ia, ja, ib, jb):
        tl = Pixel(i=ia, j=ja)
        br = Pixel(i=ib, j=jb)
        return Box(tl, br)

    def iter_width(self):
        """returns an iterator on the width of this box"""
        return range(self.tl.i, self.br.i+1)

    def iter_height(self):
        """returns an iterator on the height of this box"""
        return range(self.tl.j, self.br.j+1)

    def iter_area(self):
        """returns an iterator on all the coordinates making up the
        inside and boundary of this box"""
        for j in self.iter_height():
            for i in self.iter_width():
                yield [i, j]

    def iter_boundary(self):
        """returns an iterator on all the coordinates making up the
        boundary of this box"""
        for j in self.iter_height():
            yield [self.tl.i, j]
            yield [self.br.i, j]
        for i in range(self.tl.i + 1, self.br.i):
            yield [i, self.tl.j]
            yield [i, self.br.j]


class Image:
    """a 8 bits image in memory stored as rows of Color"""
    def __init__(self, width=None, height=None, rows=None):
        """

        parameters:
          width and height: dimensions of the image
          rows: list of list of Color object

        Either (width and height) or rows are needed.
        If width and height are given, rows is initialized as a all
        black image.
        If rows is given, width and height are calculated from the
        number of rows, and length of each row.
        """
        if rows is None:
            if width is None or height is None:
                raise RuntimeError("at least width and height or rows must be given")
        self._rows = rows
        self._height = height
        self._width = width
        self._box = None

    def __repr__(self):
        return f"Image ({self.width}x{self.height})"

    @property
    def rows(self):
        if self._rows is None:
            self._rows = []
            for j in range(0, self.height):
                row = []
                row.extend([ BLACK for i in range(0, self.width) ])
                self._rows.append(row)
        return self._rows

    @property
    def height(self):
        if self._height is None:
            self._height = len(self.rows)
        return self._height

    @property
    def width(self):
        if self._width is None:
            self._width = len(self.rows[0])
        return self._width

    @property
    def box(self):
        if self._box is None:
            self._box = Box.from_coordinates(0, 0, self.width - 1, self.height - 1)
        return self._box

    @classmethod
    def from_rgb_rows(cls, rows, has_alpha=False):
        """generate a new image from a list of (r, g, b, r, g, b...)
        lists instead of list of list Color"""
        skip = 4 if has_alpha else 3
        new_rows = []
        for row in rows:
            new_row = [ Color(row[i], row[i+1], row[i+2]) for i in range(0, len(row), skip) ]
            new_rows.append(new_row)
        return Image(rows=new_rows)

    def to_rgb_rows(self):
        """export the image as a list of (r, g, b, r, g, b...) lists
        """
        rows = []
        for row in self.rows:
            new_row = []
            for i in range(0, len(row)):
                col = row[i]
                a = [col.g, col.g, col.g] if col.is_grey() else [col.r, col.g, col.b]
                new_row.extend(a)
            rows.append(new_row)
        return rows

    def get_color_at(self, i, j):
        """Return the color at location (i, j) as a Color object"""
        return self.rows[j][i]

    def set_color_at(self, i, j, col):
        """Set the color at location (i, j) to the given Color"""
        self.rows[j][i] = col

    def get_pixel_at(self, i, j):
        """Return the color at location (i, j) in the form of a new
        Pixel object"""
        return Pixel(i, j, self.get_color_at(i, j))

    def get_pixel(self, pixel):
        """Update the given Pixel object with the color stored at
        location(i, j)"""
        pixel.col = self.get_color_at(pixel.i, pixel.j)
        return pixel

    def set_pixel(self, pixel):
        """Set the color at location (i, j) to the color set in the
        given Pixel object"""
        self.set_color_at(pixel.i, pixel.j, pixel.col)

    def iter_rectangle_area(self, box):
        """Returns an iterator on all pixels within the given box
        area"""
        for pos in box.iter_area():
            yield self.get_pixel_at(pos[0], pos[1])

    def iter_area(self):
        """Returns an iterator on all pixels of this image"""
        return self.iter_rectangle_area(self.box)

    def iter_rectangle_boundary(self, box):
        """Returns an iterator on all pixels within the boundary of
        given box area"""
        for pos in box.iter_boundary():
            yield self.get_pixel_at(pos[0], pos[1])

    def box_around(self, pixel, d):
        """Returns a box (size d x d) centered on the given pixel"""
        if d <= 0:
            raise RuntimeError("d must be strictly positive")
        return Box.from_coordinates(
            max( 0          , pixel.i - d ),
            max( 0          , pixel.j - d ),
            min( self.width , pixel.i + d ),
            min( self.height, pixel.j + d ))

    def iter_neighbours_r(self, pixel, d):
        """Returns an iterator on all pixels within a box (size d x d)
        centered on the given pixel"""
        return self.iter_rectangle_area(self.box_around(pixel, d))

    def iter_neighbours_r_boundary(self, pixel, d):
        """Returns an iterator on all pixels on the boundary of a box
        (size d x d) centered on the given pixel"""
        return self.iter_rectangle_boundary(self.box_around(pixel, d))

    def transform(self, func):
        """

        Apply functiopn `func` on all pixels of this image, and return a new image.
        `func` takes a Pixel object and must return a Color object.
        """
        new_image = Image(width=self.width, height=self.height)
        for pixel in self.iter_area():
            new_image.set_color_at(pixel.i, pixel.j, func(pixel))
        return new_image

    def draw_box(self, box, color):
        """draw a box in a given color"""
        for i, j in box.iter_boundary():
            self.set_color_at(i, j, color)


class BlobFinder:
    def __init__(self, image, bg_col=BLACK):
        self.image = image
        self.bg_col = bg_col
        self._blobmap = None
        self._blobs = None

    def _first_pass(self):
        """Loop through all pixels and tries to identify
        neighbours. Pixels are assigned a label, pixels with the same
        label are part of the same blob. Potential new blobs, or for
        those where connection to existing blobs is not known yet, are
        given a new label. later, when two labels are found to be
        actually in the same blob, their labels is added to a
        "equivalence" table that forms a cyclic graph, where nodes in
        a cycle are equivalent:
        e.g.:
            1: 2, 3
            2: 1, 3
            3: 1
            4: 6
            5:
            6: 4, 7
            7: 6

            1, 2, and 3 are equivalents
            4, 6 and 7 are equivalent
        """
        graph = {}
        blob_id = 0
        blobmap = Image(self.image.width, self.image.height)

        def set_equivalence(label1, label2):
            if label1 is None or label2 is None:
                raise RuntimeError("None labels")
            if label1 == label2:
                raise RuntimeError("equal labels")
            if label1 not in graph:
                graph[label1] = [label2]
                return
            if label2 not in graph[label1]:
                graph[label1].append(label2)

        def non_bg_color_at(i, j):
            col = blobmap.get_color_at(i, j)
            if col == self.bg_col:
                return None
            return col

        for pixel in self.image.iter_area():
            if pixel.col == self.bg_col:
                continue
            i = pixel.i
            j = pixel.j
            left = non_bg_color_at(i - 1, j    ) if i > 0 else None
            up   = non_bg_color_at(i    , j - 1) if j > 0 else None
            if up is None and left is None:
                blob_id += 1   # no known neighbours, maybe a new blob ?
                blobmap.set_color_at(i, j, Color.grey(blob_id))
                graph[blob_id] = []
                continue
            if up is not None:
                blobmap.set_color_at(i, j, up)  # belongs to the same blob as "up"
                if left is not None and left != up:
                    set_equivalence(left.g, up.g)
                    set_equivalence(up.g, left.g)
                continue
            blobmap.set_color_at(i, j, left)  # belongs to the same blob as "left"
        return (blobmap, graph)

    def _resolve_labels(self, graph):
        """walk through the equivalence graph built in 1st pass,
        Returns a new structure where all labels are "resolved" to the
        smallest label
        e.g. input:
            1: 2, 3
            2: 1, 3
            3: 1
            4: 6
            5:
            6: 4, 7
            7: 6

        output:
            1: 1
            2: 1
            3: 1
            4: 4
            5: 5
            6: 4
            7: 4
"""

        resolved = {}

        def smallest_label(label, explored=[]):
            if label in resolved:
                return resolved[label]
            smallest = label
            for label in graph[label]:
                if label < smallest:
                    smallest = label
                if label in explored:
                    continue
                x = smallest_label(label, explored + [label])
                if x < smallest:
                    smallest = x
            return smallest

        for label in graph:
            resolved[label] = smallest_label(label)
        return resolved

    def _second_pass(self, blobmap, resolved):
        """In the blobmap, replace each label by its "resolved"
        value"""
        for pixel in blobmap.iter_area():
            label = pixel.col.g
            if label == 0:
                continue
            label = resolved[label]
            blobmap.set_color_at(pixel.i, pixel.j, Color.grey(label))

    @property
    def blobmap(self):
        if self._blobmap is None:
            blobmap, graph = self._first_pass()
            resolved = self._resolve_labels(graph)
            self._second_pass(blobmap, resolved)
            self._blobmap = blobmap
        return self._blobmap

    @property
    def blobs(self):
        if self._blobs is None:
            blobs = {}
            for pixel in self.image.iter_area():
                label = self.blobmap.get_pixel_at(pixel.i, pixel.j).col.g
                if label == 0:
                    continue
                if label in blobs:
                    blobs[label].append(pixel)
                else:
                    blobs[label] = [pixel]
            self._blobs = list(blobs.values())
        return self._blobs
