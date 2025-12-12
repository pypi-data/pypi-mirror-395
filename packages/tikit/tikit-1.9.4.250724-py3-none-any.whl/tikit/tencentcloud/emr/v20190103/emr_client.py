# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tikit.tencentcloud.common.abstract_client import AbstractClient
from tikit.tencentcloud.emr.v20190103 import models


class EmrClient(AbstractClient):
    _apiVersion = '2019-01-03'
    _endpoint = 'emr.tencentcloudapi.com'
    _service = 'emr'


    def DescribeClusterNodes(self, request):
        """查询硬件节点信息

        :param request: Request instance for DescribeClusterNodes.
        :type request: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeClusterNodesRequest`
        :rtype: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeClusterNodesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeClusterNodes", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterNodesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeKeyTabFile(self, request):
        """导出Keytab文件（用户管理）

        :param request: Request instance for DescribeKeyTabFile.
        :type request: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeKeyTabFileRequest`
        :rtype: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeKeyTabFileResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeKeyTabFile", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeKeyTabFileResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeServiceConfs(self, request):
        """查询服务配置

        :param request: Request instance for DescribeServiceConfs.
        :type request: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeServiceConfsRequest`
        :rtype: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeServiceConfsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeServiceConfs", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeServiceConfsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserManagerUserList(self, request):
        """查询用户列表（用户管理）

        :param request: Request instance for DescribeUserManagerUserList.
        :type request: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeUserManagerUserListRequest`
        :rtype: :class:`tikit.tencentcloud.emr.v20190103.models.DescribeUserManagerUserListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserManagerUserList", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserManagerUserListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)