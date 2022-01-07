import pytest
import requests
import enum
from datetime import datetime, timedelta


def get_complete_data():
    """Method which takes care of obtaining an expected json file, which can be used to validate the response data
       obtained from the API on applying the filters.
       our data set contains all currently known close approaches that have happened or will happen in the 20th and
       21st centuries!"""

    res = requests.get("https://ssd-api.jpl.nasa.gov/cad.api?date-min=1999-01-01&date-max=2100-01-01&dist-max=1")
    assert res.status_code == 200, res.status_code
    data = res.json()
    return data['data']

COMPLETE_DATA = get_complete_data()

class SBDBCloseApproachAPIResponseFields(enum.Enum):
    """Class where we have assigned enumerated values to the fields of API response body,
       which can be further used for validation. """
    des = 0
    orbit_id = 1
    jd = 2
    cd = 3
    dist = 4
    dist_min = 5
    dist_max = 6
    v_rel = 7
    v_inf = 8
    t_sigma_f = 9
    h = 10


class SBDBCloseApproachTestCase(object):
    """Testcase class where we pass the filters to be applied on the API """
    def __init__(self, **kwargs):
        self.filters = dict()
        # add default filters
        self.filters['date_min'] = 'now'
        default_date_max = datetime.now() + timedelta(days=60)
        self.filters['date_max'] = default_date_max.strftime('%Y-%m-%d')
        self.filters['dist_max'] = 0.05
        for key, value in kwargs.items():
            self.filters[key] = value

        self.expected_fields = [
            SBDBCloseApproachAPIResponseFields.des.name,
            SBDBCloseApproachAPIResponseFields.orbit_id.name,
            SBDBCloseApproachAPIResponseFields.jd.name,
            SBDBCloseApproachAPIResponseFields.cd.name,
            SBDBCloseApproachAPIResponseFields.dist.name,
            SBDBCloseApproachAPIResponseFields.dist_min.name,
            SBDBCloseApproachAPIResponseFields.dist_max.name,
            SBDBCloseApproachAPIResponseFields.v_rel.name,
            SBDBCloseApproachAPIResponseFields.v_inf.name,
            SBDBCloseApproachAPIResponseFields.t_sigma_f.name,
            SBDBCloseApproachAPIResponseFields.h.name
        ]

    def construct_api_based_on_filters(self):
        """Method where we construct the API based on the filters"""
        base_api = 'https://ssd-api.jpl.nasa.gov/cad.api'
        filters = self.filters.copy()
        base_api = '{}?{}={}'.format(base_api, list(filters.keys())[0], list(filters.values())[0])
        filters.pop(list(filters.keys())[0])
        for filter, value in filters.items():
            base_api = base_api + '&'
            base_api = '{}{}={}'.format(base_api, filter, value)
        api = base_api.replace('_', '-')
        print('final api: {}'.format(api))
        return api

    def get_filtered_expected_output(self):
        """
        Method where we apply the filters on the dataset obtained from the method get_complete_data().
        Below are the possible key values that can be provided to this function.
            date-min: exclude data earlier than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
            date-max: exclude data later than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
            dist-min: exclude data with an approach distance less than this, e.g., 0.05, 10LD (default units: au)
            dist-max: exclude data with an approach distance greater than this (see dist-min)
            min-dist-min: exclude data with an approach minimum-distance less than this, e.g., 0.05, 10LD (default units: au)
            min-dist-max: exclude data with an approach minimum-distance greater than this (see min-dist-min)
            h-min: exclude data from objects with H-values less than this (e.g., 22 meaning objects smaller than this)
            h-max: exclude data from objects with H-value greater than this (e.g., 17.75 meaning objects larger than this)
            v-inf-min: exclude data with V-infinity less than this positive value in km/s (e.g., 18.5)
            v-inf-max: exclude data with V-infinity greater than this positive value in km/s (e.g., 20)
            v-rel-min: exclude data with V-relative less than this positive value in km/s (e.g., 11.2)
            v-rel-max: exclude data with V-relative greater than this positive value in km/s (e.g., 19)
        :return: list of filtered data
        """
        filtered_data = COMPLETE_DATA
        for filter, value in self.filters.items():
            filtered_data = self.apply_filter(filtered_data, filter, value)
        return filtered_data

    def apply_filter(self, data, key, value):
        """Method where we format the value if necessary and apply filter(key) on data"""
        filtered_data = []
        if key in ['date_min', 'date_max']:
            if value == 'now':
                value = datetime.now()
            else:
                value = datetime.strptime(value, '%Y-%m-%d')
            if key == 'date_min':
                for row in data:
                    if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') > value:
                        filtered_data.append(row)
            elif key == 'date_max':
                for row in data:
                    if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') < value:
                        filtered_data.append(row)
        elif key == 'dist_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'dist_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'min_dist_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'min_dist_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'h_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.h.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'h_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.h.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'v_inf_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_inf.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'v_inf_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_inf.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'v_rel_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_rel.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'v_rel_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_rel.value]) < float(value):
                    filtered_data.append(row)
        return filtered_data


def get_api_positive_filter_conditions():
    api_filter_conditions = [
        SBDBCloseApproachTestCase(date_min='2021-12-01'),
        SBDBCloseApproachTestCase(date_min='2021-12-01', date_max='2022-01-06'),
        SBDBCloseApproachTestCase(date_min='2021-12-01', date_max='2022-01-06', dist_min='0.01'),
        SBDBCloseApproachTestCase(v_inf_min='18.5'),
        SBDBCloseApproachTestCase(date_min='2021-12-01', v_inf_min='18.5')
    ]
    # TODO: Similar to the above testcases, we can test other supported filter as well.
    return api_filter_conditions

def get_api_invalid_filter_format_conditions():
    api_filter_conditions = [
      SBDBCloseApproachTestCase(date_min='2021-dec-01'),
    ]
    # TODO: Similar to the above testcases, we can test other supported filters as well.
    return api_filter_conditions

def get_api_zero_count_conditions():
    api_filter_conditions = [
        SBDBCloseApproachTestCase(date_min='2021-12-01', dist_max='0')
    ]
    # TODO: Similar to the above testcases, we can test other supported filters as well.
    return api_filter_conditions

@pytest.fixture(scope='function', params=get_api_positive_filter_conditions())
def get_positive_testcases(request):
    return request.param

@pytest.fixture(scope='function', params=get_api_invalid_filter_format_conditions())
def get_invalid_filter_format_testcases(request):
    return request.param

@pytest.fixture(scope='function', params=get_api_zero_count_conditions())
def get_zero_count_testcases(request):
    return request.param

class TestSBDBCloseApproachAPI(object):
    def test_api_positive_filter_conditions(self, get_positive_testcases):
        """Testcase where we pass one or more filters to the API and validate the response of the API."""
        testcase = get_positive_testcases
        res = requests.get(testcase.construct_api_based_on_filters())
        assert res.status_code == 200, res.status_code
        response = res.json()
        expected_output = testcase.get_filtered_expected_output()
        assert response['signature']['version'] == '1.4', response['signature']['version']
        assert response['data'] == expected_output, "data do not match. data in response: {}, " \
                                                               "Expected: {},".format(response['data'],
                                                                                      testcase.expected_output)
        assert int(response['count']) == len(expected_output), "count does not match. Count in response: {}, " \
                                                                "Expected: {},".format(response['count'],
                                                                                       len(expected_output))
        assert response['fields'] == testcase.expected_fields, "Fields do not match. Fields in response: {}, " \
                                                                "Expected: {}, ".format(response['fields'],
                                                                                  testcase.expected_fields)

    def test_api_invalid_query_param_format(self, get_invalid_filter_format_testcases):
        """Testcase where we validate the error response when the filter value format is invalid."""
        testcase = get_invalid_filter_format_testcases
        res = requests.get(testcase.construct_api_based_on_filters())
        assert res.status_code == 400, res.status_code
        assert res.json() == {'moreInfo': 'https://ssd-api.jpl.nasa.gov/doc/cad.html',
                              'message': "invalid value specified for query parameter 'date-min': invalid datetime specified (expected 'YYYY-MM-DD', 'YYYY-MM-DDThh:mm:ss', 'YYYY-MM-DD_hh:mm:ss' or 'YYYY-MM-DD hh:mm:ss')", 'code': '400'}

    def test_api_zero_count_conditions(self, get_zero_count_testcases):
        """Testcase where we validate the response of API results in zero count."""
        testcase = get_zero_count_testcases
        res = requests.get(testcase.construct_api_based_on_filters())
        assert res.status_code == 200, res.status_code
        response = res.json()
        assert int(response['count']) == 0, res['count']
        assert res.json() == {'count': '0', 'signature': {'source': 'NASA/JPL SBDB Close Approach Data API', 'version': '1.4'}}
