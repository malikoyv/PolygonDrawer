import unittest


class TestPolygonFunctions(unittest.TestCase):

    def setUp(self):
        self.gdansk_coordinates = [
            (54.380125, 18.587927),
            (54.373425, 18.604137),
            (54.375684, 18.629654),
            (54.387119, 18.629246),
            (54.387630, 18.610150)
        ]

    def test_create_polygon(self):
        from google_maps_polygon import create_polygon  # Import the function to test
        polygon = create_polygon(self.gdansk_coordinates)
        self.assertEqual(polygon['paths'][0], self.gdansk_coordinates)
        self.assertEqual(polygon['strokeColor'], "#FF0000")
        self.assertEqual(polygon['strokeOpacity'], 0.8)
        self.assertEqual(polygon['strokeWeight'], 2)
        self.assertEqual(polygon['fillColor'], "#FF0000")
        self.assertEqual(polygon['fillOpacity'], 0.35)

    def test_calculate_polygon_area(self):
        from google_maps_polygon import calculate_polygon_area  # Import the function to test
        area = calculate_polygon_area(self.gdansk_coordinates)
        expected_area = 3.02  # Approximate expected area in square kilometers
        self.assertAlmostEqual(area, expected_area, places=3)


if __name__ == '__main__':
    unittest.main()
