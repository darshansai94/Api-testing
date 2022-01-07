**Overview:**
This project is an API test automation suite, which tests Californian Institute of Technology’s(CIT) SBDB Close-ApproachDataAPI.

Documentation of the API can be found here: https://ssd-api.jpl.nasa.gov/doc/cad.html
API under testing is "https://ssd-api.jpl.nasa.gov/cad.api".


**Steps for Execution:**
Pre-requisite:
Docker should be installed in the machine.

**Step1:**
Unzip the folder and build the Docker file using the below command:
docker build -t sbdbcloseapproach:1.0 .
Note: Assuming the command is executed from the same location where the Docker file resides.

**Step2:**
start the container in detached mode exposing port 80 to view the python test results by executing the below command:
docker run -d -it --name python-server -p 80:7000 sbdbcloseapproach:1.0

**step3:**
Open the https:localhost:80 url in the browser and to visually see the report.


**High level explanation of the project:**
The main intention of the project is to test the close-approach data obtained from the API with different filter conditions and their combinations.
1.Expected_dataset - We firstly obtain a dataset from the same API, 
  which contains all currently known close approaches that have happened or will happen in the 20th and 21st centuries.
2.Testcases - We have a set of testcases which obtains the data from the API based on the filters applied.
  The above obtained response is validated with the data we have as expected_dataset by applying the same condition.
3. We have three set of testcases: 
   1. Positive filter value testcases - which tests the response of API on providing positive values for the supported filters.
   2. Zero count condition testcases - which tests the response of API on providing values which results in zero count.
   3. Invalid filter format testcases - which tests the response of API on providing values which are invalid wrt format for the supported filters.
   **Note:** For every above type we have one or two test cases defined, similarly we can define multiple testcases covering all supported filters.
4.Filter conditions supported in the test suite for fetching the data from the API are as below:
    1.date-min: exclude data earlier than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
    2.date-max: exclude data later than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
    3.dist-min: exclude data with an approach distance less than this, e.g., 0.05, 10LD (default units: au)
    4.dist-max: exclude data with an approach distance greater than this (see dist-min)
    5.min-dist-min: exclude data with an approach minimum-distance less than this, e.g., 0.05, 10LD (default units: au)
    6.min-dist-max: exclude data with an approach minimum-distance greater than this (see min-dist-min)
    7.h-min: exclude data from objects with H-values less than this (e.g., 22 meaning objects smaller than this)
    8.h-max: exclude data from objects with H-value greater than this (e.g., 17.75 meaning objects larger than this)
    9.v-inf-min: exclude data with V-infinity less than this positive value in km/s (e.g., 18.5)
    10.v-inf-max: exclude data with V-infinity greater than this positive value in km/s (e.g., 20)
    11.v-rel-min: exclude data with V-relative less than this positive value in km/s (e.g., 11.2)
    12.v-rel-max: exclude data with V-relative greater than this positive value in km/s (e.g., 19)

**Project structure:**
1. Dockerfile - Which is responsible for bringing up the container with necessary packages and server.
2. Requirements.txt - Text file which contains necessary python packages needed for the execution.
3. start.sh - Entry point in the Docker file, which triggers the execution of the testcase and brings up the simple python http server.
4. testcases.py - python file which is responsible for obtaining expected dataset and executing testcases.





