"""Unit tests for conversion between NumPy arrays and JSON."""

import pytest
from numpy import array
from qciconnect_common.qciconnect_conversion.json_conversion import JSONNumpyConverter

conv = JSONNumpyConverter()


class TestJSONNumpyConverter:
    """Contains unit tests for conversion between NumPy arrays and JSON."""

    @pytest.mark.parametrize(
        ("numpy_array_input", "json_list_input"),
        [
            (
                array([0, 1, 2]),
                "[0, 1, 2]",
            ),
            (
                array([0.1, 1.2, 2.3]),
                "[0.1, 1.2, 2.3]",
            ),
            (
                array([]),
                "[]",
            ),
            (
                array([[0.1, 1.2, 2.3], [0.1, 1.2, 2.3]]),
                "[[0.1, 1.2, 2.3], [0.1, 1.2, 2.3]]",
            ),
            (
                array(
                    [
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 1],
                        [1, 1, 1, 0, 1],
                        [0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 1],
                    ]
                ),
                "[[0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], "
                "[1, 1, 1, 0, 1], [0, 0, 0, 0, 0], [1, 1, 0, 0, 1]]",
            ),
        ],
    )
    def test_nparray_to_json_list(self, numpy_array_input, json_list_input):
        """Test conversion from NumPy array to JSON compatible list.

        Args:
            numpy_array_input (nparray): Test input array.
            json_list_input (str): Expected JSON list output.
        """
        converted_input = conv.nparray_to_json_list(numpy_array_input)
        assert converted_input == json_list_input

    @pytest.mark.parametrize(
        ("numpy_array_input", "json_list_input"),
        [
            (
                array([0, 1, 2]),
                "[0, 1, 2]",
            ),
            (
                array([0.1, 1.2, 2.3]),
                "[0.1, 1.2, 2.3]",
            ),
            (
                array([]),
                "[]",
            ),
            (
                array([[0.1, 1.2, 2.3], [0.1, 1.2, 2.3]]),
                "[[0.1, 1.2, 2.3], [0.1, 1.2, 2.3]]",
            ),
            (
                array(
                    [
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 1],
                        [1, 1, 1, 0, 1],
                        [0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 1],
                    ]
                ),
                "[[0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], "
                "[1, 1, 1, 0, 1], [0, 0, 0, 0, 0], [1, 1, 0, 0, 1]]",
            ),
        ],
    )
    def test_json_list_to_nparray(self, numpy_array_input, json_list_input):
        """Test conversion from JSON compatible list to NumPy array.

        Args:
            numpy_array_input (nparray): Expected output array.
            json_list_input (str): JSON list input.
        """
        converted_input = conv.json_list_to_nparray(json_list_input)
        assert converted_input.all() == numpy_array_input.all()

    @pytest.mark.parametrize(
        ("complex_python_input", "complex_json_input"),
        [
            (
                1.23j,
                "1.23j",
            ),
            (
                0j,
                "0j",
            ),
            (
                1.0 + 1.23j,
                "(1+1.23j)",
            ),
            (
                1.1 + 1.23j,
                "(1.1+1.23j)",
            ),
            (
                1 + 2j,
                "(1+2j)",
            ),
            (
                -1.1 - 1.23j,
                "(-1.1-1.23j)",
            ),
            (
                1.0j,
                "1j",
            ),
            (
                1.1 + 0.0j,
                "(1.1+0j)",
            ),
        ],
    )
    def test_complex_python_to_json(self, complex_python_input, complex_json_input):
        """Test conversion from Python complex no. (complex) to JSON compatible string.

        Args:
            complex_python_input (complex): Complex number input.
            complex_json_input (str): Expected JSON compatible output.
        """
        converted_input = conv.complex_python_to_json(complex_python_input)
        assert converted_input == complex_json_input

    @pytest.mark.parametrize(
        ("complex_python_input", "complex_json_input"),
        [
            (
                1.23j,
                "1.23j",
            ),
            (
                0j,
                "0j",
            ),
            (
                1.0 + 1.23j,
                "(1+1.23j)",
            ),
            (
                1.1 + 1.23j,
                "(1.1+1.23j)",
            ),
            (
                1 + 2j,
                "(1+2j)",
            ),
            (
                -1.1 - 1.23j,
                "(-1.1-1.23j)",
            ),
            (
                1.0j,
                "1j",
            ),
            (
                1.1 + 0.0j,
                "(1.1+0j)",
            ),
            (
                1.1 + 1.23j,
                "1.1+1.23j",
            ),
            (
                1.23,
                "1.23",
            ),
            (
                -1j,
                "-j",
            ),
        ],
    )
    def test_complex_json_to_python(self, complex_python_input, complex_json_input):
        """Test conversion from JSON to Python.
        
        Convert JSON compatible string decribing complex no. to Python complex no. (complex).

        Args:
            complex_python_input (complex): Expected complex number output.
            complex_json_input (str):  JSON compatible input.
        """
        converted_input = conv.complex_json_to_python(complex_json_input)
        assert converted_input == complex_python_input

    @pytest.mark.parametrize(
        ("complex_array_input", "complex_json_input"),
        [
            (
                array([1.0 + 1.23j]),
                "[(1+1.23j)]",
            ),
            (
                array([[1.1 + 2.2j, -1.1 + 2.2j], [1.1 - 2.2j, -1.1 - 2.2j]]),
                "[[(1.1+2.2j), (-1.1+2.2j)], [(1.1-2.2j), (-1.1-2.2j)]]",
            ),
        ],
    )
    def test_complex_nparray_to_json_list(
        self, complex_array_input, complex_json_input
    ):
        """Test conversion of NumPy array of type complex to JSON compatible list.

        Args:
            complex_array_input (nparray, dtype=complex): Complex array input.
            complex_json_input (str): Expected JSON compatible list output.
        """
        converted_input = conv.complex_nparray_to_json_list(complex_array_input)
        assert converted_input == complex_json_input
