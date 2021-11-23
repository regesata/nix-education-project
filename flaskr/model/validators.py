"""Validator class"""
from datetime import date
import re


class Validators:
    """
    Class realize validate methods

    Methods
    -------
    validate_name(cls, name: str) -> bool: validates name argument, is must be not None and
        has length between 2 and 100
        :return Bool
    validate_date_of_birth(cls, date_of_birth: date) -> bool validates data_of_birth,
        it must be between 1800-1-1 and today date
        :return Bool
    validate_email(cls, email: str) -> bool: validates email, it must be valid email
        :return Bool
    validate_rate(cls, rate: int) -> bool: validates rate, it should be not None
        and value between 1 and 10
        :return Bool
    """

    @classmethod
    def validate_name(cls, name: str) -> bool:
        """Validate method for name or titles"""
        if not name:
            return False
        if 2 > len(name) > 100:
            return False
        return True

    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> bool:
        """Validate method for date of birth"""

        if date_of_birth < date(year=1800, month=1, day=1) or date_of_birth >= date.today():
            return False
        if not date_of_birth:
            return False
        return True

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email"""
        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not re.match(pattern, email):
            return False
        return True

    @classmethod
    def validate_rate(cls, rate: int) -> bool:
        """Validate rate. Rate should be between 1 and 10"""
        if 1 > rate > 10:
            return False
        return True
