import json
import subprocess

import pytest

@pytest.mark.zip_code_test
class TestLocationByZip:
    """
    Test Class to run integration tests on the 'Coordinates by zip/post' code api endpoint
    """

    @pytest.mark.single_valid_zip_code
    def test_single_valid_zip_code(self):
        result = subprocess.run(["python", "cli_tool.py", "--zip_code","91381"], capture_output=True, text=True)
        assert result.returncode == 0
        assert result.stderr == ''
        result = json.loads(result.stdout)
        zip_code_result = result['data']
        assert zip_code_result['Zip Code'] == '91381'
        assert zip_code_result['Location Name'] == 'Los Angeles County'
        assert zip_code_result['Country'] ==  'US'
        assert zip_code_result['Latitude'] ==  34.3775
        assert zip_code_result['Longitude'] == -118.6131

    @pytest.mark.multiple_valid_zip_code
    def test_multiple_valid_zip_code(self):
        # Verify results of multiple zip code search
        result = subprocess.run(["python", "cli_tool.py", "--zip_code","90034,91381"], capture_output=True, text=True)
        json_objects = result.stdout.strip().split("\n")
        assert json_objects is not None, "No results found"
        assert result.returncode == 0
        assert result.stderr == ''
        first_result = json_objects[0]
        first_zip_code_details = json.loads(first_result)['data']

        # Verify the details of the first zip location
        assert first_zip_code_details['Zip Code'] == '90034'
        assert first_zip_code_details['Location Name'] == 'Los Angeles'
        assert first_zip_code_details['Country'] ==  'US'
        assert first_zip_code_details['Latitude'] ==  34.029
        assert first_zip_code_details['Longitude'] == -118.4005

        second_result = json_objects[1]
        second_zip_code_details = json.loads(second_result)['data']
        # Verify the details of the second zip location
        assert second_zip_code_details['Zip Code'] == '91381'
        assert second_zip_code_details['Location Name'] == 'Los Angeles County'
        assert second_zip_code_details['Country'] ==  'US'
        assert second_zip_code_details['Latitude'] ==  34.3775
        assert second_zip_code_details['Longitude'] == -118.6131

    @pytest.mark.word_as_zip_code
    def test_word_as_zip_code(self):
        # Verify the response when the user enters a word string instead of a valid zip code
        result = subprocess.run(["python", "cli_tool.py", "--zip_code", "invalid"], capture_output=True, text=True)
        assert 'Invalid input format for zip code: invalid' in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.empty_string_as_zip_code
    def test_empty_string_as_zip_code(self):
        result = subprocess.run(["python", "cli_tool.py", "--zip_code", ""], capture_output=True, text=True)
        assert 'Invalid input format for zip code: ' in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.less_than_5_digit_zip_code
    def test_less_than_5_digit_zip_code(self):
        # Verify the response when a user enters a non-standard 5 digit US zip code
        result = subprocess.run(["python", "cli_tool.py", "--zip_code", "123"], capture_output=True, text=True)
        assert 'Invalid input format for zip code: 123' in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.no_zip_input
    def test_no_zip_input(self):
        result = subprocess.run(["python", "cli_tool.py", "--zip_code"], capture_output=True, text=True)
        assert result.stdout == ''
        assert result.returncode == 2
        assert 'error: argument --zip_code: expected at least one argument' in result.stderr

    @pytest.mark.invalid_input_args
    def test_invalid_input_args(self):
        # Verify the response when the user doesn't even pass the required args to the cmd
        result = subprocess.run(["python", "cli_tool.py"], capture_output=True, text=True)
        assert 'Invalid input arguments, please see --help for options' in result.stdout

    @pytest.mark.not_found
    def test_not_found(self):
        # Verify that if you input a zip that does not exist in the official USPS database then it returns a 404 error
        result = subprocess.run(["python", "cli_tool.py", "--zip_code", "98761"], capture_output=True, text=True)
        assert '"error": "404 Client Error: Not Found' in result.stdout