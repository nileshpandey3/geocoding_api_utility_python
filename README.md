Requirement
-----------------------
To run this application and the tests within, Python3.9 or above is needed:
https://www.python.org/downloads/release

Install
-----------------------
Clone the repo
```shell
git clone https://github.com/nileshpandey3/geocoding_api_utility
```

After cloning the repo, cd into it
```shell
cd geo-coding-api-application
```

Install dependencies
```
pip3 install -r requirements.txt
```
Usage
-----
To run tests in parallel, with your choice of pytest mark tags, generate html report, rerun failed test and allow ipdb tracing
```shell
cd to the integration tests directory "tests/integration_tests"
pytest tests/integration_tests -n auto --dist=loadscope -m "mark_of_your_choice" --html report.html --reruns 2 --reruns-delay 5 -s
```
To simply run all the tests
```shell
pytest tests/integration_tests -s
```
To run the command line utility and do a zip code based search run the following command
```shell
python cli_tool.py --zip_code "90034"
```
OR you can also search for multiple zip codes e.g.
```shell
python cli_tool.py --zip_code "91381","90034"
```

To run the command line utility and do a location (city & state) based search run the following command
```shell
python cli_tool.py --city_and_state "Madison, WI" 
```
OR you can also search for multiple locations e.g.
```shell
python cli_tool.py --city_and_state "Madison, WI" "Chicago, IL"
```
Debugging
-----------------------
Install & Import ipdb and use `ipdb.set_trace()`
