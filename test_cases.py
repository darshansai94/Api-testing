
import pytest

def test_demo():
    pass

# import pytest
# import requests
# import json
# import enum
# from datetime import datetime, timedelta
#
#
# def get_complete_data():
#     """Method which takes care of obtaining an expected json file, which can be used to validate the response obtained
#        from the API on applying the filters.
#        our data set contains all currently known close approaches that have happened or will happen in the 20th and 21st centuries!"""
#
#     res = requests.get("https://ssd-api.jpl.nasa.gov/cad.api?date-min=1999-01-01&date-max=2023-01-01&dist-max=1")
#     assert res.status_code == 200, res.status_code
#     data = res.json()
#     return data['data']
#
#
# COMPLETE_DATA = get_complete_data()
#
#
# class SBDBCloseApproachAPIResponseFields(enum.Enum):
#     des = 0
#     orbit_id = 1
#     jd = 2
#     cd = 3
#     dist = 4
#     dist_min = 5
#     dist_max = 6
#     v_rel = 7
#     v_inf = 8
#     t_sigma_f = 9
#     h = 10
#
#
# class SBDBCloseApproachTestCase(object):
#     def __init__(self, **kwargs):
#         self.filters = dict()
#         # add default filters
#         self.filters['date_min'] = 'now'
#         default_date_max = datetime.now() + timedelta(days=60)
#         self.filters['date_max'] = default_date_max.strftime('%Y-%m-%d')
#         self.filters['dist_max'] = 0.05
#         for key, value in kwargs.items():
#             self.filters[key] = value
#         print("printing filters")
#         for key, value in self.filters.items():
#             print("{}:{}".format(key, value))
#
#         self.expected_fields = [
#             SBDBCloseApproachAPIResponseFields.des.name,
#             SBDBCloseApproachAPIResponseFields.orbit_id.name,
#             SBDBCloseApproachAPIResponseFields.jd.name,
#             SBDBCloseApproachAPIResponseFields.cd.name,
#             SBDBCloseApproachAPIResponseFields.dist.name,
#             SBDBCloseApproachAPIResponseFields.dist_min.name,
#             SBDBCloseApproachAPIResponseFields.dist_max.name,
#             SBDBCloseApproachAPIResponseFields.v_rel.name,
#             SBDBCloseApproachAPIResponseFields.v_inf.name,
#             SBDBCloseApproachAPIResponseFields.t_sigma_f.name,
#             SBDBCloseApproachAPIResponseFields.h.name
#         ]
#
#     def construct_api_based_on_filters(self):
#         base_api = 'https://ssd-api.jpl.nasa.gov/cad.api'
#         filters = self.filters.copy()
#         base_api = '{}?{}={}'.format(base_api, list(filters.keys())[0], list(filters.values())[0])
#         filters.pop(list(filters.keys())[0])
#         print('filter after pop')
#         for key,val in self.filters.items():
#             print('{}:{}'.format(key, val))
#         for filter, value in filters.items():
#             base_api = base_api + '&'
#             base_api = '{}{}={}'.format(base_api, filter,value)
#         api = base_api.replace('_', '-')
#         print('final api: {}'.format(api))
#         return api
#
#     def apply_filter(self, data, key, value):
#         print('len of data to be filtered = {}'.format(len(data)))
#         filtered_data = []
#         if key in ['date_min', 'date_max']:
#             if value == 'now':
#                 value = datetime.now()
#             else:
#                 value = datetime.strptime(value, '%Y-%m-%d')
#             if key == 'date_min':
#                 for row in data:
#                     if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') > value:
#                         filtered_data.append(row)
#             elif key == 'date_max':
#                 for row in data:
#                     if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') < value:
#                         filtered_data.append(row)
#         elif key == 'dist_min':
#             for row in data:
#                 if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) > float(value):
#                     filtered_data.append(row)
#         elif key == 'dist_max':
#             for row in data:
#                 if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) < float(value):
#                     filtered_data.append(row)
#         elif key == 'min_dist_min':
#             for row in data:
#                 if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) > float(value):
#                     filtered_data.append(row)
#         elif key == 'min_dist_max':
#              for row in data:
#                  if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) < float(value):
#                      filtered_data.append(row)
#         elif key == 'max_dist_min':
#             for row in data:
#                 if float(row[SBDBCloseApproachAPIResponseFields.dist_max.value]) > float(value):
#                     filtered_data.append(row)
#         elif key == 'max_dist_max':
#             for row in data:
#                 if float(row[SBDBCloseApproachAPIResponseFields.dist_max.value]) < float(value):
#                     filtered_data.append(row)
#         return filtered_data
#
#     def get_filtered_expected_output(self):
#         """
#         Below are the possible key values that can be provided to this function:
#          date-min: exclude data earlier than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the
#                          current date.
#          date-max: exclude data later than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
#          dist-min: exclude data with an approach distance less than this, e.g., 0.05, 10LD (default units: au)
#          dist-max: exclude data with an approach distance greater than this (see dist-min)
#          min-dist-min: exclude data with an approach minimum-distance less than this, e.g., 0.05, 10LD (default units: au)
#          min-dist-max: exclude data with an approach minimum-distance greater than this (see min-dist-min)
#          h-min: exclude data from objects with H-values less than this (e.g., 22 meaning objects smaller than this)
#          h-max: exclude data from objects with H-value greater than this (e.g., 17.75 meaning objects larger than this)
#          v-inf-min: exclude data with V-infinity less than this positive value in km/s (e.g., 18.5)
#          v-inf-max: exclude data with V-infinity greater than this positive value in km/s (e.g., 20)
#          v-rel-min: exclude data with V-relative less than this positive value in km/s (e.g., 11.2)
#          v-rel-max: exclude data with V-relative greater than this positive value in km/s (e.g., 19)
#         """
#         filtered_data = COMPLETE_DATA
#         print('length of complete data: {}'.format(len(filtered_data)))
#         for filter, value in self.filters.items():
#             filtered_data = self.apply_filter(filtered_data, filter, value)
#             print('len of filtered data - iterations: {}'.format(len(filtered_data)))
#         print('len of final filtered_data: {}'.format(len(filtered_data)))
#         return filtered_data
#
#
# def api_filter_conditions():
#     api_filter_conditions = [
#         SBDBCloseApproachTestCase(date_min='2021-12-01'),
#         SBDBCloseApproachTestCase(date_min='2021-12-01', date_max='2022-01-06'),
#         SBDBCloseApproachTestCase(date_min='2021-12-01', date_max='2022-01-06', dist_min='0.01')
#     ]
#     return api_filter_conditions
#
#
# @pytest.fixture(scope='function', params=api_filter_conditions())
# def get_testcases(request):
#     return request.param
#
#
# class TestSBDBCloseApproachAPI(object):
#     def test_api(self, get_testcases):
#         testcase = get_testcases
#         res = requests.get(testcase.construct_api_based_on_filters())
#         assert res.status_code == 200, res.status_code
#         response = res.json()
#         expected_output = testcase.get_filtered_expected_output()
#         assert response['data'] == expected_output, "response:{} \n expected:{} ".format(response['data'], expected_output)
#         assert int(response['count']) == len(expected_output), "count does not match. Count in response: {}, Expected: {},".format(response['count'], len(expected_output))
#         assert response['fields'] == testcase.expected_fields, "Fields do not match. Fields in response: {}, Expected: {}, ".format(
#                                                                                      response['fields'], testcase.expected_fields,)
#         assert response['data'] == expected_output