"""
Date and time utility functions and classes.
"""

from datetime import datetime, date, timedelta
import pytz
from typing import Optional, Union, List


class DateUtils:
    """
    Utility class for common date and time operations.
    
    This class provides methods for date manipulation, formatting,
    validation, and timezone handling.
    """
    
    @staticmethod
    def now(timezone: Optional[str] = None) -> datetime:
        """
        Get current datetime with optional timezone.
        
        Args:
            timezone: Timezone name (e.g., 'UTC', 'America/New_York')
            
        Returns:
            Current datetime
        """
        if timezone:
            tz = pytz.timezone(timezone)
            return datetime.now(tz)
        return datetime.now()
    
    @staticmethod
    def today(timezone: Optional[str] = None) -> date:
        """
        Get current date with optional timezone.
        
        Args:
            timezone: Timezone name
            
        Returns:
            Current date
        """
        return DateUtils.now(timezone).date()
    
    @staticmethod
    def parse_date(date_string: str, format_string: str = "%Y-%m-%d") -> date:
        """
        Parse a date string into a date object.
        
        Args:
            date_string: Date string to parse
            format_string: Format string for parsing
            
        Returns:
            Parsed date object
            
        Raises:
            ValueError: If date string cannot be parsed
        """
        try:
            return datetime.strptime(date_string, format_string).date()
        except ValueError as e:
            raise ValueError(f"Failed to parse date '{date_string}' with format '{format_string}': {e}")
    
    @staticmethod
    def parse_datetime(datetime_string: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """
        Parse a datetime string into a datetime object.
        
        Args:
            datetime_string: Datetime string to parse
            format_string: Format string for parsing
            
        Returns:
            Parsed datetime object
            
        Raises:
            ValueError: If datetime string cannot be parsed
        """
        try:
            return datetime.strptime(datetime_string, format_string)
        except ValueError as e:
            raise ValueError(f"Failed to parse datetime '{datetime_string}' with format '{format_string}': {e}")
    
    @staticmethod
    def format_date(date_obj: Union[date, datetime], format_string: str = "%Y-%m-%d") -> str:
        """
        Format a date or datetime object to string.
        
        Args:
            date_obj: Date or datetime object
            format_string: Format string for output
            
        Returns:
            Formatted date string
        """
        if isinstance(date_obj, datetime):
            return date_obj.strftime(format_string)
        return date_obj.strftime(format_string)
    
    @staticmethod
    def format_datetime(datetime_obj: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format a datetime object to string.
        
        Args:
            datetime_obj: Datetime object
            format_string: Format string for output
            
        Returns:
            Formatted datetime string
        """
        return datetime_obj.strftime(format_string)
    
    @staticmethod
    def add_days(date_obj: Union[date, datetime], days: int) -> Union[date, datetime]:
        """
        Add days to a date or datetime object.
        
        Args:
            date_obj: Date or datetime object
            days: Number of days to add (can be negative)
            
        Returns:
            New date or datetime object
        """
        if isinstance(date_obj, datetime):
            return date_obj + timedelta(days=days)
        return date_obj + timedelta(days=days)
    
    @staticmethod
    def add_hours(datetime_obj: datetime, hours: int) -> datetime:
        """
        Add hours to a datetime object.
        
        Args:
            datetime_obj: Datetime object
            hours: Number of hours to add (can be negative)
            
        Returns:
            New datetime object
        """
        return datetime_obj + timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(datetime_obj: datetime, minutes: int) -> datetime:
        """
        Add minutes to a datetime object.
        
        Args:
            datetime_obj: Datetime object
            minutes: Number of minutes to add (can be negative)
            
        Returns:
            New datetime object
        """
        return datetime_obj + timedelta(minutes=minutes)
    
    @staticmethod
    def days_between(date1: Union[date, datetime], date2: Union[date, datetime]) -> int:
        """
        Calculate the number of days between two dates.
        
        Args:
            date1: First date or datetime
            date2: Second date or datetime
            
        Returns:
            Number of days between the dates
        """
        # Convert to date objects if needed
        if isinstance(date1, datetime):
            date1 = date1.date()
        if isinstance(date2, datetime):
            date2 = date2.date()
        
        return (date2 - date1).days
    
    @staticmethod
    def hours_between(datetime1: datetime, datetime2: datetime) -> float:
        """
        Calculate the number of hours between two datetimes.
        
        Args:
            datetime1: First datetime
            datetime2: Second datetime
            
        Returns:
            Number of hours between the datetimes
        """
        delta = datetime2 - datetime1
        return delta.total_seconds() / 3600
    
    @staticmethod
    def is_weekend(date_obj: Union[date, datetime]) -> bool:
        """
        Check if a date falls on a weekend.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            True if the date is on a weekend
        """
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        
        return date_obj.weekday() >= 5  # Saturday = 5, Sunday = 6
    
    @staticmethod
    def is_weekday(date_obj: Union[date, datetime]) -> bool:
        """
        Check if a date falls on a weekday.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            True if the date is on a weekday
        """
        return not DateUtils.is_weekend(date_obj)
    
    @staticmethod
    def get_week_start(date_obj: Union[date, datetime]) -> date:
        """
        Get the start of the week (Monday) for a given date.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            Date object representing the start of the week
        """
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        
        # Monday is 0, so we subtract the weekday number to get to Monday
        days_since_monday = date_obj.weekday()
        return date_obj - timedelta(days=days_since_monday)
    
    @staticmethod
    def get_week_end(date_obj: Union[date, datetime]) -> date:
        """
        Get the end of the week (Sunday) for a given date.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            Date object representing the end of the week
        """
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        
        # Sunday is 6, so we add (6 - weekday) to get to Sunday
        days_until_sunday = 6 - date_obj.weekday()
        return date_obj + timedelta(days=days_until_sunday)
    
    @staticmethod
    def get_month_start(date_obj: Union[date, datetime]) -> date:
        """
        Get the first day of the month for a given date.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            Date object representing the first day of the month
        """
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        
        return date_obj.replace(day=1)
    
    @staticmethod
    def get_month_end(date_obj: Union[date, datetime]) -> date:
        """
        Get the last day of the month for a given date.
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            Date object representing the last day of the month
        """
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
        
        # Get the first day of the next month, then subtract one day
        if date_obj.month == 12:
            next_month = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            next_month = date_obj.replace(month=date_obj.month + 1, day=1)
        
        return next_month - timedelta(days=1)
    
    @staticmethod
    def convert_timezone(datetime_obj: datetime, target_timezone: str) -> datetime:
        """
        Convert a datetime to a different timezone.
        
        Args:
            datetime_obj: Datetime object (must be timezone-aware)
            target_timezone: Target timezone name
            
        Returns:
            Datetime object in the target timezone
            
        Raises:
            ValueError: If datetime is not timezone-aware
        """
        if datetime_obj.tzinfo is None:
            raise ValueError("Datetime object must be timezone-aware")
        
        target_tz = pytz.timezone(target_timezone)
        return datetime_obj.astimezone(target_tz)
    
    @staticmethod
    def make_timezone_aware(datetime_obj: datetime, timezone: str = "UTC") -> datetime:
        """
        Make a naive datetime timezone-aware.
        
        Args:
            datetime_obj: Naive datetime object
            timezone: Timezone to assign
            
        Returns:
            Timezone-aware datetime object
        """
        if datetime_obj.tzinfo is not None:
            return datetime_obj
        
        tz = pytz.timezone(timezone)
        return tz.localize(datetime_obj)
    
    @staticmethod
    def get_age(birth_date: Union[date, datetime], reference_date: Optional[Union[date, datetime]] = None) -> int:
        """
        Calculate age from birth date.
        
        Args:
            birth_date: Birth date or datetime
            reference_date: Reference date (defaults to today)
            
        Returns:
            Age in years
        """
        if reference_date is None:
            reference_date = DateUtils.today()
        
        # Convert to date objects if needed
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        if isinstance(reference_date, datetime):
            reference_date = reference_date.date()
        
        age = reference_date.year - birth_date.year
        if reference_date.month < birth_date.month or (reference_date.month == birth_date.month and reference_date.day < birth_date.day):
            age -= 1
        
        return age 