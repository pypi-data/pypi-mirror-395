# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkvod.endpoint import endpoint_data

class DescribeVodPlayerMetricDataRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'vod', '2017-03-21', 'DescribeVodPlayerMetricData','vod')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_Language(self): # String
		return self.get_query_params().get('Language')

	def set_Language(self, Language):  # String
		self.add_query_param('Language', Language)
	def get_StartTime(self): # String
		return self.get_query_params().get('StartTime')

	def set_StartTime(self, StartTime):  # String
		self.add_query_param('StartTime', StartTime)
	def get_PageNumber(self): # Long
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # Long
		self.add_query_param('PageNumber', PageNumber)
	def get_Top(self): # Long
		return self.get_query_params().get('Top')

	def set_Top(self, Top):  # Long
		self.add_query_param('Top', Top)
	def get_PageSize(self): # Long
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # Long
		self.add_query_param('PageSize', PageSize)
	def get_Os(self): # String
		return self.get_query_params().get('Os')

	def set_Os(self, Os):  # String
		self.add_query_param('Os', Os)
	def get_EndTime(self): # String
		return self.get_query_params().get('EndTime')

	def set_EndTime(self, EndTime):  # String
		self.add_query_param('EndTime', EndTime)
	def get_Filters(self): # String
		return self.get_query_params().get('Filters')

	def set_Filters(self, Filters):  # String
		self.add_query_param('Filters', Filters)
	def get_AppId(self): # String
		return self.get_query_params().get('AppId')

	def set_AppId(self, AppId):  # String
		self.add_query_param('AppId', AppId)
	def get_Interval(self): # String
		return self.get_query_params().get('Interval')

	def set_Interval(self, Interval):  # String
		self.add_query_param('Interval', Interval)
	def get_Metrics(self): # String
		return self.get_query_params().get('Metrics')

	def set_Metrics(self, Metrics):  # String
		self.add_query_param('Metrics', Metrics)
	def get_TerminalType(self): # String
		return self.get_query_params().get('TerminalType')

	def set_TerminalType(self, TerminalType):  # String
		self.add_query_param('TerminalType', TerminalType)
