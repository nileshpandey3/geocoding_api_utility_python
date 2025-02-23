
import json
import subprocess

import pytest

@pytest.mark.city_and_state_test
class TestLocationByCityState:
    """
    Test Class to run integration tests on the 'Coordinates by location name' api endpoint
    """

    @pytest.mark.single_valid_location
    def test_single_valid_location(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state","Madison, WI"], capture_output=True, text=True)
        assert result.returncode == 0
        assert result.stderr == ''
        result = json.loads(result.stdout)
        zip_code_result = result['data']

        assert zip_code_result['City'] == 'Madison'
        assert zip_code_result['State'] == 'Wisconsin'
        assert zip_code_result['Country'] ==  'US'
        assert zip_code_result['Latitude'] ==  43.074761
        assert zip_code_result['Longitude'] == -89.3837613

    @pytest.mark.multiple_valid_locations
    def test_multiple_valid_locations(self):
        # Verify results of multiple zip cities search
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state",'Chicago, IL', 'Madison, WI'], capture_output=True, text=True)
        json_objects = result.stdout.strip().split("\n")
        assert json_objects is not None, "No results found"
        assert result.returncode == 0
        assert result.stderr == ''
        first_result = json_objects[0]
        first_location_details = json.loads(first_result)['data']

        # Verify the details of the first city location
        assert first_location_details['City'] == 'Chicago'
        assert first_location_details['State'] == 'Illinois'
        assert first_location_details['Country'] ==  'US'
        assert first_location_details['Latitude'] ==  41.8755616
        assert first_location_details['Longitude'] == -87.6244212

        second_result = json_objects[1]
        second_location_details = json.loads(second_result)['data']
        # Verify the details of the second city location
        assert second_location_details['City'] == 'Madison'
        assert second_location_details['State'] == 'Wisconsin'
        assert second_location_details['Country'] ==  'US'
        assert second_location_details['Latitude'] ==  43.074761
        assert second_location_details['Longitude'] == -89.3837613

    @pytest.mark.invalid_location
    def test_invalid_location(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state", "invalid"], capture_output=True, text=True)
        assert "Invalid input format for city and state: ['invalid']" in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.empty_location
    def test_empty_location(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state", ""], capture_output=True, text=True)
        assert "Invalid input format for city and state: ['']" in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.missing_state
    def test_missing_state(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state", "Madison"], capture_output=True, text=True)
        assert "Invalid input format for city and state: ['Madison']" in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.missing_city
    def test_missing_city(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state", "WI"], capture_output=True, text=True)
        assert "Invalid input format for city and state: ['WI']" in result.stdout
        assert 'please refer to the --help option for expected input format' in result.stdout

    @pytest.mark.no_location_input
    def test_no_location_input(self):
        result = subprocess.run(["python", "cli_tool.py", "--city_and_state"], capture_output=True, text=True)
        assert result.stdout == ''
        assert result.returncode == 2
        assert 'error: argument --city_and_state: expected at least one argument' in result.stderr

    @pytest.mark.invalid_input_args
    def test_invalid_input_args(self):
        result = subprocess.run(["python", "cli_tool.py"], capture_output=True, text=True)
        assert 'Invalid input arguments, please see --help for options' in result.stdout