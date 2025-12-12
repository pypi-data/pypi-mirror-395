import math
import math
import re
import math
import re
import math
if True:
    def add_two(a, b):
        """Add two numbers together, return the result"""
        # LITERALAI: {"codeid": "d5ebe1d7ea51020ef7d3fa94c2d7c0447de36f2fe7d6321e0aac5ab8de0da956"}
        return a + b

def generate_slug(s):
    """Generate a slug (a string that's a valid python variable name,
    and still as similar as possible to the original) version of the
    string s."""
    # Use regular expressions for this.
    # LITERALAI: {"codeid": "f03c1cd2e4b9845798fd4da8946d5b265342fc22794c46eb135023f6a629f123"}
    s = re.sub('[^0-9a-zA-Z]+', '_', s)
    
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
    
    return s

class Point(object):
    """A point in 2d space. Should be possible to print, parse from string, measure
    distance between, rotate around another point, change to have
    another point as origo etc."""
    # LITERALAI: {"codeid": "70be4c495013189e2e6ad0e24ea0a1cee155dc8a8572bee05eef27216532c08e"}
    def __init__(self, x, y):
        """
        Initializes the point with given x and y coordinate.

        :param x: x-coordinate of the point.
        :param y: y-coordinate of the point.
        """
        # LITERALAI: {"genid": "7c0d3508f9b62b331a17311fe5372ad9c82e8358396883039c1280fff6f96647", "codeid": "7c0d3508f9b62b331a17311fe5372ad9c82e8358396883039c1280fff6f96647"}
        self.x = x
        self.y = y

    def __str__(self):
        """
        Returns a string representation of the point.

        :return: string representation of the point.
        """
        # LITERALAI: {"genid": "1ce7bd174d7c398e33a03ddf6ac95440ab71c05fb22891257d67987edb6394aa", "codeid": "1ce7bd174d7c398e33a03ddf6ac95440ab71c05fb22891257d67987edb6394aa"}
        return f"Point({self.x}, {self.y})"

    @classmethod
    def from_string(cls, point_str):
        """
        Parses a point from the given string.

        :param point_str: string representing a point.
        :return: a point object represented by the string.
        """
        # LITERALAI: {"genid": "38484059c4737fe120d02ccfb1f14279db250270c186c8de43a9b770bcb79965", "codeid": "38484059c4737fe120d02ccfb1f14279db250270c186c8de43a9b770bcb79965"}
        coordinates = point_str.split(',')

        # Create a new object of this class, parsing the coordinates to floats
        return cls(float(coordinates[0]), float(coordinates[1]))

    def distance_to(self, other_point):
        """
        Returns the euclidean distance from this point to the other_point.

        :param other_point: The other point to measure distance to.
        :return: distance to the other point.
        """
        # LITERALAI: {"genid": "f3c3dcfdaeb4d2939564eed95a38c4a78d44c3de2a89fc6950a81eea3af4d3f9", "codeid": "f3c3dcfdaeb4d2939564eed95a38c4a78d44c3de2a89fc6950a81eea3af4d3f9"}
        import math

        x_distance = other_point.x - self.x
        y_distance = other_point.y - self.y

        return math.sqrt(x_distance ** 2 + y_distance ** 2)

    def rotate_around(self, other_point, angle):
        """
        Rotates this point around the other_point by the given angle in degrees.

        :param other_point: The point to rotate around.
        :param angle: the angle in degrees.
        :return: None
        """
        # LITERALAI: {"genid": "474ec142a28d6cd1b4a0515956857ba8a484b418cd39cb4d0f23b8703cc06a51", "codeid": "474ec142a28d6cd1b4a0515956857ba8a484b418cd39cb4d0f23b8703cc06a51"}
        angle = math.radians(angle)
        
        # Shift self point so that other_point becomes the origin
        shifted_x = self[0] - other_point[0]
        shifted_y = self[1] - other_point[1]
        
        # Apply rotation about the origin
        rotated_x = shifted_x * math.cos(angle) - shifted_y * math.sin(angle)
        rotated_y = shifted_x * math.sin(angle) + shifted_y * math.cos(angle)
        
        # Shift the point back
        self[0] = rotated_x + other_point[0]
        self[1] = rotated_y + other_point[1]

    def change_origo(self, new_origo):
        """
        Changes the point to have new_origo as the origin.

        :param new_origo: The new origin point.
        :return: None
        """
        # LITERALAI: {"genid": "dd93fb0562187b4471d208f387151d28efda2b24f45205e3ca9f26959f68604d", "codeid": "dd93fb0562187b4471d208f387151d28efda2b24f45205e3ca9f26959f68604d"}
        self.origo = new_origo
        return None
