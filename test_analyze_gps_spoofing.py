"""Unit tests for analyze_gps_spoofing.py helper functions."""

import math
import pytest
from analyze_gps_spoofing import (
    parse_coords,
    haversine_distance,
    time_diff_minutes,
    calculate_velocity,
)


# ---------------------------------------------------------------------------
# parse_coords
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

    def test_zero_coordinates(self):
        lat, lon = parse_coords("0.0°, 0.0°")
        assert lat == pytest.approx(0.0)
        assert lon == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# haversine_distance  (returns km)
# ---------------------------------------------------------------------------

class TestHaversineDistance:
    def test_same_point_returns_zero(self):
        coord = (24.3198761, 54.5381226)
        assert haversine_distance(coord, coord) == pytest.approx(0.0)

    def test_known_distance_abu_dhabi_to_dubai(self):
        abu_dhabi = (24.4539, 54.3773)
        dubai = (25.2048, 55.2708)
        dist = haversine_distance(abu_dhabi, dubai)
        assert 120 < dist < 130  # ~125 km

    def test_short_distance(self):
        a = (24.3198761, 54.5381226)
        b = (24.3200000, 54.5383000)
        dist = haversine_distance(a, b)
        assert dist < 1  # less than 1 km

    def test_symmetry(self):
        a = (24.4539, 54.3773)
        b = (25.2048, 55.2708)
        assert haversine_distance(a, b) == pytest.approx(haversine_distance(b, a))

    def test_antipodal_distance(self):
        north_pole = (90.0, 0.0)
        south_pole = (-90.0, 0.0)
        dist = haversine_distance(north_pole, south_pole)
        assert dist == pytest.approx(math.pi * 6371, rel=0.01)


# ---------------------------------------------------------------------------
# time_diff_minutes
# ---------------------------------------------------------------------------

class TestTimeDiffMinutes:
    def test_one_hour_difference(self):
        t1 = "2026-04-07T10:00:00"
        t2 = "2026-04-07T11:00:00"
        assert time_diff_minutes(t1, t2) == pytest.approx(60.0)

    def test_same_time_returns_zero(self):
        t = "2026-04-07T12:30:00"
        assert time_diff_minutes(t, t) == pytest.approx(0.0)

    def test_reversed_order_returns_positive(self):
        t1 = "2026-04-07T14:00:00"
        t2 = "2026-04-07T13:00:00"
        assert time_diff_minutes(t1, t2) == pytest.approx(60.0)

    def test_fractional_minutes(self):
        t1 = "2026-04-07T10:00:00"
        t2 = "2026-04-07T10:01:30"
        assert time_diff_minutes(t1, t2) == pytest.approx(1.5)


# ---------------------------------------------------------------------------
# calculate_velocity
# ---------------------------------------------------------------------------

class TestCalculateVelocity:
    def test_basic_velocity(self):
        # 60 km in 60 minutes = 60 km/h
        assert calculate_velocity(60, 60) == pytest.approx(60.0)

    def test_zero_time_returns_zero(self):
        assert calculate_velocity(100, 0) == 0

    def test_high_speed(self):
        # 250 km in 1 minute = 15000 km/h
        assert calculate_velocity(250, 1) == pytest.approx(15000.0)

    def test_zero_distance(self):
        assert calculate_velocity(0, 30) == pytest.approx(0.0)
