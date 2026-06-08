"""Unit tests for analyze_gps_jumps.py helper functions."""

import math
import pytest
from analyze_gps_jumps import parse_coords, haversine_distance


# ---------------------------------------------------------------------------
# parse_coords  (analyze_gps_jumps variant)
# ---------------------------------------------------------------------------

class TestParseCoords:
    def test_standard_degree_format(self):
        lat, lon = parse_coords("24.3198761°, 54.5381226°")
        assert lat == pytest.approx(24.3198761)
        assert lon == pytest.approx(54.5381226)

    def test_corrupted_encoding(self):
        lat, lon = parse_coords("24.3198761Â°, 54.5381226Â°")
        assert lat == pytest.approx(24.3198761)
        assert lon == pytest.approx(54.5381226)

    def test_negative_coordinates(self):
        lat, lon = parse_coords("-33.8688°, 151.2093°")
        assert lat == pytest.approx(-33.8688)
        assert lon == pytest.approx(151.2093)

    def test_plain_numeric_format(self):
        """Fallback path when no degree symbol is present."""
        lat, lon = parse_coords("24.3198761, 54.5381226")
        assert lat == pytest.approx(24.3198761)
        assert lon == pytest.approx(54.5381226)


# ---------------------------------------------------------------------------
# haversine_distance  (returns meters)
# ---------------------------------------------------------------------------

class TestHaversineDistance:
    def test_same_point_returns_zero(self):
        coord = (24.3198761, 54.5381226)
        assert haversine_distance(coord, coord) == pytest.approx(0.0)

    def test_known_distance_abu_dhabi_to_dubai(self):
        abu_dhabi = (24.4539, 54.3773)
        dubai = (25.2048, 55.2708)
        dist = haversine_distance(abu_dhabi, dubai)
        # ~125 km = ~125000 m
        assert 120_000 < dist < 130_000

    def test_short_distance(self):
        a = (24.3198761, 54.5381226)
        b = (24.3200000, 54.5383000)
        dist = haversine_distance(a, b)
        assert dist < 100  # less than 100 meters

    def test_symmetry(self):
        a = (24.4539, 54.3773)
        b = (25.2048, 55.2708)
        assert haversine_distance(a, b) == pytest.approx(haversine_distance(b, a))

    def test_antipodal_distance(self):
        north_pole = (90.0, 0.0)
        south_pole = (-90.0, 0.0)
        dist = haversine_distance(north_pole, south_pole)
        expected_m = math.pi * 6371000
        assert dist == pytest.approx(expected_m, rel=0.01)
