"""Test date tools."""
from datetime import date

import app.tools.date as atd


class TestLastDayOfMonth:
    """Test last_day_of_month method."""

    def test0(self) -> None:
        """Test Feb 2020."""
        day = date(2020, 2, 4)
        assert atd.last_day_of_month(day) == date(2020, 2, 29)

    def test1(self) -> None:
        """Test Feb 2021."""
        day = date(2021, 2, 4)
        assert atd.last_day_of_month(day) == date(2021, 2, 28)

    def test2(self) -> None:
        """Test Dec 2020."""
        day = date(2020, 12, 4)
        assert atd.last_day_of_month(day) == date(2020, 12, 31)


class TestFirstDayOfMonth:
    """Test first_day_of_month method."""

    def test0(self) -> None:
        """Test Feb 2020."""
        day = date(2020, 2, 4)
        assert atd.first_day_of_month(day) == date(2020, 2, 1)

    def test1(self) -> None:
        """Test Feb 2021."""
        day = date(2021, 2, 4)
        assert atd.first_day_of_month(day) == date(2021, 2, 1)

    def test2(self) -> None:
        """Test Dec 2020."""
        day = date(2020, 12, 4)
        assert atd.first_day_of_month(day) == date(2020, 12, 1)


class TestWorkingDayPercent:
    """Test working_day_percent method."""

    def test0(self) -> None:
        """Test second half of Nov 21."""
        start = date(2021, 11, 16)
        end = date(2021, 11, 30)
        assert atd.working_days_percent(start, end) == 50.0

    def test1(self) -> None:
        """Test first half of Nov 21."""
        start = date(2021, 11, 1)
        end = date(2021, 11, 15)
        assert atd.working_days_percent(start, end) == 50.0

    def test2(self) -> None:
        """Test default start."""
        end = date(2021, 11, 15)
        assert atd.working_days_percent(end=end) == 50.0

    def test3(self) -> None:
        """Test more than 1 month."""
        start = date(2020, 11, 1)
        end = date(2021, 11, 15)
        assert atd.working_days_percent(start, end) == 50.0
