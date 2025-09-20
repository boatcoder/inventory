from django.test import TestCase

# Create your tests here.
from .models import Location


class TestLocation(TestCase):
    def setUp(self):
        self.location1 = Location.objects.create(name="Location 1")
        self.location2 = Location.objects.create(name="Location 2", location=self.location1)
        self.location3 = Location.objects.create(name="Location 3", location=self.location2)

    def test_get_location_ancestry(self):
        ancestry = self.location3.get_location_ancestry(self.location3.id)
        self.assertEqual(ancestry, ["Location 3", "Location 2", "Location 1"])

        ancestry = self.location2.get_location_ancestry(self.location2.id)
        self.assertEqual(ancestry, ["Location 2", "Location 1"])

        ancestry = self.location1.get_location_ancestry(self.location1.id)
        self.assertEqual(ancestry, ["Location 1"])

    def test_str_method(self):
        self.assertEqual(str(self.location1), "Location 1")
        self.assertEqual(str(self.location2), "Location 2 -> Location 1")
        self.assertEqual(str(self.location3), "Location 3 -> Location 2 -> Location 1")
