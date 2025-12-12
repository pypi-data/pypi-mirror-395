from datetime import datetime, timezone


class DateTimeHelper:
    @classmethod
    def days_remain(cls, input_datetime: datetime) -> int:
        """
        Checks how many days are left from current UTC time

        Args:
            input_datetime (datetime): value which is compared with UTC time

        Returns:
            int: days left
        """
        if not isinstance(input_datetime, datetime):
            return None

        diff = input_datetime - datetime.now(timezone.utc).replace(tzinfo=None)

        if diff.days < 0:
            return 0

        return diff.days

    @classmethod
    def hours_remain(cls, input_datetime: datetime) -> int:
        """
        Checks how many hours are left from current UTC time

        Args:
            input_datetime (datetime): value which is compared with UTC time

        Returns:
            int: days left
        """
        if not isinstance(input_datetime, datetime):
            return None

        diff = input_datetime - datetime.now(timezone.utc).replace(tzinfo=None)
        hours_left = diff.total_seconds() // 3600

        if hours_left < 0:
            return 0

        return int(hours_left)

    @classmethod
    def days_since(cls, input_datetime: datetime) -> int:
        """
        Checks how many days are left from current UTC time

        Args:
            input_datetime (datetime): value which is compared with UTC time

        Returns:
            int: days left
        """
        if not isinstance(input_datetime, datetime):
            return None

        diff = datetime.now(timezone.utc).replace(tzinfo=None) - input_datetime

        return diff.days

    @classmethod
    def has_time_expired(cls, input_datetime: datetime) -> bool:
        """
        Checks if time has expired

        Args:
            input_datetime (datetime): value which is compared with UTC time

        Returns:
            bool: Returns True if time has expired otherwise False
        """
        if not isinstance(input_datetime, datetime):
            return True

        return input_datetime > datetime.now(timezone.utc).replace(tzinfo=None)

    @classmethod
    def has_time_started(cls, input_datetime: datetime) -> bool:
        """
        Checks if time has started

        Args:
            input_datetime (datetime): value which is compared with UTC time

        Returns:
            bool: Returns True if time has started otherwise False
        """
        if not isinstance(input_datetime, datetime):
            return True

        return input_datetime < datetime.now(timezone.utc).replace(tzinfo=None)
