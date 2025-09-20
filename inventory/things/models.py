from django.db import connection, models

# Create your models here.


class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name_plural = "locations"

    def get_location_ancestry(self, location_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                WITH RECURSIVE location_ancestry AS (
                    SELECT id, name, location_id
                    FROM things_location
                    WHERE id = %s

                    UNION ALL

                    SELECT l.id, l.name, l.location_id
                    FROM things_location l
                    INNER JOIN location_ancestry la ON l.id = la.location_id
                )
                SELECT name FROM location_ancestry;
            """,
                [location_id],
            )
            return [row[0] for row in cursor.fetchall()]

    def __str__(self):
        if self.location:
            return " -> ".join(self.get_location_ancestry(self.id))
        return self.name


class Thing(models.Model):
    class ThingUnits(models.IntegerChoices):
        EACH = 1, "each"
        INCHES = 2, "inches"
        FEET = 3, "feet"
        KG = 4, "kg"
        LBS = 5, "lbs"
        OUNCES = 6, "ounces"
        LITERS = 7, "liters"
        GRAMS = 8, "grams"
        MILLILITERS = 9, "milliliters"
        METERS = 10, "meters"
        CENTIMETERS = 11, "centimeters"
        MILLIMETERS = 12, "millimeters"

    name = models.CharField(max_length=64)
    quantity = models.IntegerField(default=1, blank=False)
    units = models.IntegerField(default=1, blank=False, choices=ThingUnits)
    length = models
    description = models.TextField(blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=False,
    )

    def __str__(self):
        return self.name
