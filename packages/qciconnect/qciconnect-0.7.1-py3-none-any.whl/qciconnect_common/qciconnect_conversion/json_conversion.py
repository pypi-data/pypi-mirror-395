"""Provides helper methods to convert between JSON and Python data formats."""

from datetime import datetime, timedelta
from json import dumps, loads

import numpy as np
from numpy import asarray
from qciconnect_common.qciconnect_logging.logger import QCIConnectLogging

logger = QCIConnectLogging().get_logger()


class JSONNumpyConverter:
    """Provides helper methods to convert between JSON and numpy data formats."""

    @staticmethod
    def nparray_to_json_list(nparray: np.ndarray):
        """Convert NumPy array to JSON list.

        Args:
            nparray (np.array): NumPy array to be converted

        Returns:
            json_list: JSON list equivalent to nparray
        """
        python_list = nparray.tolist()
        json_list = dumps(python_list)
        return json_list

    @staticmethod
    def json_list_to_nparray(json_list: str):
        """Convert JSON list to NumPy array.

        Args:
            json_list (JSON list): JSON list to be converted

        Returns:
            np.array: NumPy array representation of json_list
        """
        python_list = loads(json_list)
        try:
            nparray = asarray(python_list)
        except ValueError:
            logger.error(
                """
                Invalid input. 
                Content or shape of input JSON list is not compatible with NumPy array 
                (e.g. inhomogenous shape or datatypes).
                """
            )
        except TypeError:
            logger.error("Invalid input. Input is not a (JSON) string.")
        else:
            return nparray

    @staticmethod
    def dict_to_json(dictionary: dict):
        """Convert Python dictionary to JSON object.

        Args:
            dictionary (dict): Dictionary to be converted

        Returns:
            JSON list: JSON list equivalent to dictionary
        """
        return dumps(dictionary)

    @staticmethod
    def json_to_dict(json_object: str):
        """Convert JSON object to Python dictionary.

        Args:
            json_object (JSON list): JSON list to be converted

        Returns:
            dict: Dictionary equivalent to json_object
        """
        return loads(json_object)

    @staticmethod
    def complex_python_to_json(complex_number: complex):
        """Convert Python complex number to string.

        Args:
            complex_number (complex): Complex number to be converted

        Returns:
            str: String representation of complex number.
            Example: a Python complex number 1.1+2.2j (or complex(1.1, 2.2) ) with real part 1.1
            and imaginary part 2.2 becomes '(1.1+2.2j)'.
        """
        if isinstance(complex_number, complex):
            json_complex_number = str(complex_number)
            return json_complex_number
        else:
            error = TypeError(f"Input {complex_number} is not a valid number of type complex.")
            logger.error(error)
            raise error

    @staticmethod
    def complex_json_to_python(json_complex_number: str):
        """Convert JSON string representation of complex number to Python complex.

        Args:
            json_complex_number (str): Complex number to be converted, must be of forms
            '(1.1+2.2j)', '1.1+2.2j', '2.2j + 1.1', '1.1', or '2.2j'.

        Returns:
            complex: Complex number in standard Python format.
        """
        try:
            complex_number = complex(json_complex_number)
        except ValueError:
            logger.error("Invalid input string. Cannot be converted to complex.")
        except TypeError:
            logger.error(
                """
                Invalid input format. 
                Must be string of form '(1.1+2.2j)', '1.1+2.2j', '2.2j + 1.1', '1.1', or '2.2j'.
                """
            )
        else:
            return complex_number

    @staticmethod
    def complex_nparray_to_json_list(complex_array: np.ndarray):
        """Convert NumPy array with complex numbers as entries to JSON list.

        Args:
            complex_array (np.array, dtype = complex): Complex NumPy array to be converted.

        Raises:
            error: TypeError if entries are not complex.
            error: TypeError if input is not a np.array.

        Returns:
            str: JSON list with string representations (e.g. '(1.1+2.2j)') of complex entries.
        """
        if isinstance(complex_array, np.ndarray):
            if (complex_array.dtype != complex) and (complex_array.dtype != "complex128"):
                error = TypeError(
                    f"Entries of {complex_array} are not dtype=complex, but {complex_array.dtype}."
                )
                logger.error(error)
                raise error
            else:
                complex_list = complex_array.tolist()
                json_list = str(complex_list)
                return json_list
        else:
            error = TypeError(f"Input {complex_array} is not a -NumPy array with dtype = complex.")
            logger.error(error)
            raise error


class JSONDateTimeConverter:
    """Provides helper methods to convert between JSON and Python datetime formats."""

    @staticmethod
    def datetime_to_json_datetime(datetime_object: datetime):
        """Converts Python datetime object to ISO JSON string.

        Args:
            datetime_object (datetime): Python datetime object to be converted,

        Raises:
            error: TypeError if input is not a datetime object.

        Returns:
            str: JSON string representation of datetime in ISO format with microsecond precison
            (e.g. "2020-02-02T01:02:03.000004Z").
        """
        if isinstance(datetime_object, datetime):
            datetime_json = datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f")
            return datetime_json
        else:
            error = TypeError(f"Input {datetime_object} is not a valid datetime object.")
            logger.error(error)
            raise error

    @staticmethod
    def json_datetime_to_datetime(datetime_str: str):
        """Converts Python datetime object to ISO JSON string.

        Args:
            datetime_object (datetime): Python datetime object to be converted,

        Raises:
            error: TypeError if input is not a datetime object.

        Returns:
            str: JSON string representation of datetime in ISO format with microsecond precison
            (e.g. "2020-02-02T01:02:03.000004Z").
        """
        if isinstance(datetime_str, str):
            datetime_object = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
            return datetime_object
        else:
            error = TypeError(f"Input {datetime_str} is not a valid datetime object.")
            logger.error(error)
            raise error


    @staticmethod
    def timedelta_to_json(timedelta_object: timedelta):
        """Converts Python datetime.timedelta object to JSON float (string) in seconds.

        Args:
            timedelta_object (datetime.timedelta): Python datetime.timedelta object to be
            converted.

        Raises:
            error: TypeError if input is not a datetime.timedelta object.

        Returns:
            str: JSON string (float) representation of datetime.timedelta in seconds.
        """
        if isinstance(timedelta_object, timedelta):
            timedelta_float = timedelta_object.total_seconds()
            timedelta_json = dumps(timedelta_float)
            return timedelta_json
        else:
            error = TypeError(f"Input {timedelta_object} is not a valid datetime.timedelta object.")
            logger.error(error)
            raise error
