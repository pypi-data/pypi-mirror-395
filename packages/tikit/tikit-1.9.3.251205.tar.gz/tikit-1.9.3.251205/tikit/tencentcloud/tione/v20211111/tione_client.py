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
from tikit.tencentcloud.tione.v20211111 import models


class TioneClient(AbstractClient):
    _apiVersion = '2021-11-11'
    _endpoint = 'tione.tencentcloudapi.com'
    _service = 'tione'


    def AddDocumentToKnowledgeBase(self, request):
        """添加文档到知识库

        :param request: Request instance for AddDocumentToKnowledgeBase.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddDocumentToKnowledgeBaseRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddDocumentToKnowledgeBaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddDocumentToKnowledgeBase", params, headers=headers)
            response = json.loads(body)
            model = models.AddDocumentToKnowledgeBaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def AddTaskTrainSample(self, request):
        """往训练集添加训练语料

        :param request: Request instance for AddTaskTrainSample.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddTaskTrainSampleRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddTaskTrainSampleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTaskTrainSample", params, headers=headers)
            response = json.loads(body)
            model = models.AddTaskTrainSampleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def AddTencentLabWhitelist(self, request):
        """为腾学会上课的子用户添加白名单接口，仅供制定腾学会运营账号调用

        :param request: Request instance for AddTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            model = models.AddTencentLabWhitelistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def AddTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户添加白名单接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for AddTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            model = models.AddTencentLabWhitelistTestResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def AttachClusterResourceInstanceDataDisk(self, request):
        """挂载资源组节点上的闲置数据盘

        :param request: Request instance for AttachClusterResourceInstanceDataDisk.
        :type request: :class:`tencentcloud.tione.v20211111.models.AttachClusterResourceInstanceDataDiskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AttachClusterResourceInstanceDataDiskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AttachClusterResourceInstanceDataDisk", params, headers=headers)
            response = json.loads(body)
            model = models.AttachClusterResourceInstanceDataDiskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ChatCompletion(self, request):
        """该接口支持与自行部署的大模型的聊天。

        :param request: Request instance for ChatCompletion.
        :type request: :class:`tencentcloud.tione.v20211111.models.ChatCompletionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ChatCompletionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ChatCompletion", params, headers=headers)
            response = json.loads(body)
            model = models.ChatCompletionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CheckAutoMLTaskNameExist(self, request):
        """自动学习任务名称重名校验

        :param request: Request instance for CheckAutoMLTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckAutoMLTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckAutoMLTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckAutoMLTaskNameExist", params, headers=headers)
            response = json.loads(body)
            model = models.CheckAutoMLTaskNameExistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CheckBillingOwnUin(self, request):
        """判断主账号是否是云梯在用账号

        :param request: Request instance for CheckBillingOwnUin.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckBillingOwnUinRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckBillingOwnUinResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckBillingOwnUin", params, headers=headers)
            response = json.loads(body)
            model = models.CheckBillingOwnUinResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CheckBillingWhitelist(self, request):
        """判断用户是否为白名单用户

        :param request: Request instance for CheckBillingWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckBillingWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckBillingWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckBillingWhitelist", params, headers=headers)
            response = json.loads(body)
            model = models.CheckBillingWhitelistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CheckDatasetName(self, request):
        """数据集重名校验

        :param request: Request instance for CheckDatasetName.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckDatasetNameRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckDatasetNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDatasetName", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDatasetNameResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CheckModelAccTaskNameExist(self, request):
        """校验模型加速任务重名

        :param request: Request instance for CheckModelAccTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckModelAccTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckModelAccTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckModelAccTaskNameExist", params, headers=headers)
            response = json.loads(body)
            model = models.CheckModelAccTaskNameExistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CopyFlow(self, request):
        """复制工作流

        :param request: Request instance for CopyFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.CopyFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CopyFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CopyFlow", params, headers=headers)
            response = json.loads(body)
            model = models.CopyFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CopyFromDemoFlow(self, request):
        """复制案例工作流到普通工作流

        :param request: Request instance for CopyFromDemoFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.CopyFromDemoFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CopyFromDemoFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CopyFromDemoFlow", params, headers=headers)
            response = json.loads(body)
            model = models.CopyFromDemoFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAlgoNotebook(self, request):
        """创建AI市场算法对应的Notebook

        :param request: Request instance for CreateAlgoNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAlgoNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAlgoNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAlgoNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAlgoNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAnnotateTask(self, request):
        """创建任务

        :param request: Request instance for CreateAnnotateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAnnotateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAnnotateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAnnotateTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAnnotateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAnnotationKey(self, request):
        """【OCR】 新建key名字典元素

        :param request: Request instance for CreateAnnotationKey.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAnnotationKeyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAnnotationKeyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAnnotationKey", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAnnotationKeyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAutoMLEMSTask(self, request):
        """创建自动学习模型服务发布任务

        :param request: Request instance for CreateAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAutoMLEMSTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAutoMLTask(self, request):
        """创建自动学习任务

        :param request: Request instance for CreateAutoMLTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAutoMLTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateAutoMLTaskEvaluationConfusionMatrixUrl(self, request):
        """生成混淆矩阵下载链接

        :param request: Request instance for CreateAutoMLTaskEvaluationConfusionMatrixUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskEvaluationConfusionMatrixUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskEvaluationConfusionMatrixUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLTaskEvaluationConfusionMatrixUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAutoMLTaskEvaluationConfusionMatrixUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateBatchModelAccTasks(self, request):
        """批量创建模型加速任务

        :param request: Request instance for CreateBatchModelAccTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBatchModelAccTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBatchModelAccTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBatchModelAccTasks", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBatchModelAccTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateBatchTask(self, request):
        """创建批量预测任务

        :param request: Request instance for CreateBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBatchTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBatchTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateBillingPostpaidSWInstances(self, request):
        """创建按量计费的资源组纳管节点

        :param request: Request instance for CreateBillingPostpaidSWInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBillingPostpaidSWInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBillingPostpaidSWInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBillingPostpaidSWInstances", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBillingPostpaidSWInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateBillingResourceGroup(self, request):
        """创建资源组

        :param request: Request instance for CreateBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBillingResourceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateBillingResourceInstance(self, request):
        """真实下单购买节点请至控制台！
        此接口仅用于校验子账号添加资源组节点资格(CAM鉴权)；
        支持场景(资源组添加节点);


        :param request: Request instance for CreateBillingResourceInstance.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceInstanceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBillingResourceInstance", params, headers=headers)
            response = json.loads(body)
            model = models.CreateBillingResourceInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateChatWhiteListUser(self, request):
        """创建聊天白名单用户

        :param request: Request instance for CreateChatWhiteListUser.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateChatWhiteListUserRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateChatWhiteListUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateChatWhiteListUser", params, headers=headers)
            response = json.loads(body)
            model = models.CreateChatWhiteListUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateCodeRepo(self, request):
        """创建代码仓库

        :param request: Request instance for CreateCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateCodeRepo", params, headers=headers)
            response = json.loads(body)
            model = models.CreateCodeRepoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDataPipelineTask(self, request):
        """创建数据构建任务

        :param request: Request instance for CreateDataPipelineTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDataPipelineTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDataPipelineTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDataPipelineTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDataPipelineTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDataset(self, request):
        """创建数据集

        :param request: Request instance for CreateDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDataset", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDatasetResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDatasetDetailText(self, request):
        """开启文本数据集详情

        :param request: Request instance for CreateDatasetDetailText.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetDetailTextRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetDetailTextResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatasetDetailText", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDatasetDetailTextResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDatasetTextAnalyze(self, request):
        """开启文本数据透视

        :param request: Request instance for CreateDatasetTextAnalyze.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetTextAnalyzeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetTextAnalyzeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatasetTextAnalyze", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDatasetTextAnalyzeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDemoWhite(self, request):
        """动手实验室体验白名单

        :param request: Request instance for CreateDemoWhite.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDemoWhiteRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDemoWhiteResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDemoWhite", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDemoWhiteResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateDirectory(self, request):
        """新建文件夹

        :param request: Request instance for CreateDirectory.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDirectoryRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDirectoryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDirectory", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDirectoryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateExport(self, request):
        """创建任务式建模训练任务，Notebook，在线服务和批量预测任务日志下载任务API

        :param request: Request instance for CreateExport.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateExportRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateExportResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateExport", params, headers=headers)
            response = json.loads(body)
            model = models.CreateExportResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateExportAutoMLSDKTask(self, request):
        """创建自动学习模型导出SDK任务

        :param request: Request instance for CreateExportAutoMLSDKTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateExportAutoMLSDKTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateExportAutoMLSDKTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateExportAutoMLSDKTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateExportAutoMLSDKTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateFilePreviewUrl(self, request):
        """预览文件

        :param request: Request instance for CreateFilePreviewUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateFilePreviewUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateFilePreviewUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateFilePreviewUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreateFilePreviewUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateFlow(self, request):
        """创建工作流

        :param request: Request instance for CreateFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateFlow", params, headers=headers)
            response = json.loads(body)
            model = models.CreateFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateFlowTensorBoardUrl(self, request):
        """创建可视化建模tensorboard url； 只在tensorboard运行时才可生成

        :param request: Request instance for CreateFlowTensorBoardUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateFlowTensorBoardUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateFlowTensorBoardUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateFlowTensorBoardUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreateFlowTensorBoardUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateInferGateway(self, request):
        """创建独立部署的推理服务用专享网关

        :param request: Request instance for CreateInferGateway.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateInferGatewayRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateInferGatewayResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateInferGateway", params, headers=headers)
            response = json.loads(body)
            model = models.CreateInferGatewayResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateLifecycleScript(self, request):
        """创建生命周期脚本

        :param request: Request instance for CreateLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateLifecycleScript", params, headers=headers)
            response = json.loads(body)
            model = models.CreateLifecycleScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateModel(self, request):
        """新版模型仓库创建接口

        :param request: Request instance for CreateModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModel", params, headers=headers)
            response = json.loads(body)
            model = models.CreateModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateModelAccelerateTask(self, request):
        """创建模型加速任务

        :param request: Request instance for CreateModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateModelService(self, request):
        """用于创建、发布一个新的模型服务

        :param request: Request instance for CreateModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModelService", params, headers=headers)
            response = json.loads(body)
            model = models.CreateModelServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateModelServicePodUrl(self, request):
        """创建模型服务实例登录URL

        :param request: Request instance for CreateModelServicePodUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelServicePodUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelServicePodUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModelServicePodUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreateModelServicePodUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateNotebook(self, request):
        """创建Notebook

        :param request: Request instance for CreateNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.CreateNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateNotebookImage(self, request):
        """保存镜像

        :param request: Request instance for CreateNotebookImage.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateNotebookImageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateNotebookImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebookImage", params, headers=headers)
            response = json.loads(body)
            model = models.CreateNotebookImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateObjectiveEvaluation(self, request):
        """创建客观评测接口

        :param request: Request instance for CreateObjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateObjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateObjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateObjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.CreateObjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateOptimizedModel(self, request):
        """保存优化模型

        :param request: Request instance for CreateOptimizedModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateOptimizedModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateOptimizedModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateOptimizedModel", params, headers=headers)
            response = json.loads(body)
            model = models.CreateOptimizedModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreatePreSignedTensorBoardUrl(self, request):
        """创建TensorBoard授权Url

        :param request: Request instance for CreatePreSignedTensorBoardUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreatePreSignedTensorBoardUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreatePreSignedTensorBoardUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreatePreSignedTensorBoardUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreatePreSignedTensorBoardUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreatePresignedNotebookUrl(self, request):
        """生成Notebook访问链接

        :param request: Request instance for CreatePresignedNotebookUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreatePresignedNotebookUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreatePresignedNotebookUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreatePresignedNotebookUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreatePresignedNotebookUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreatePrivateLink(self, request):
        """用于创建用户VPC到TIONE的私有连接通道

        :param request: Request instance for CreatePrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreatePrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreatePrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreatePrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.CreatePrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateProject(self, request):
        """创建工程

        :param request: Request instance for CreateProject.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateProjectRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateProjectResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateProject", params, headers=headers)
            response = json.loads(body)
            model = models.CreateProjectResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateRecyclePolicy(self, request):
        """创建回收策略

        :param request: Request instance for CreateRecyclePolicy.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateRecyclePolicyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateRecyclePolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateRecyclePolicy", params, headers=headers)
            response = json.loads(body)
            model = models.CreateRecyclePolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateSDWebUIUrl(self, request):
        """生成sd-webui网址

        :param request: Request instance for CreateSDWebUIUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateSDWebUIUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateSDWebUIUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSDWebUIUrl", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSDWebUIUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateSubjectiveEvaluation(self, request):
        """创建主观评测接口

        :param request: Request instance for CreateSubjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateSubjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateSubjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSubjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSubjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateSyncReviewImageTask(self, request):
        """支持审核单张可访问的图片链接

        :param request: Request instance for CreateSyncReviewImageTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateSyncReviewImageTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateSyncReviewImageTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSyncReviewImageTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSyncReviewImageTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateTaskComparison(self, request):
        """创建对比评测任务

        :param request: Request instance for CreateTaskComparison.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTaskComparisonRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTaskComparisonResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTaskComparison", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTaskComparisonResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateTensorBoardTask(self, request):
        """创建TensorBoard任务

        :param request: Request instance for CreateTensorBoardTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTensorBoardTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTensorBoardTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTensorBoardTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTensorBoardTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateTrainingModel(self, request):
        """导入模型

        :param request: Request instance for CreateTrainingModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTrainingModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTrainingModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTrainingModel", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTrainingModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateTrainingTask(self, request):
        """创建模型训练任务

        :param request: Request instance for CreateTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateVpcPrivateLink(self, request):
        """创建VPC私有连接

        :param request: Request instance for CreateVpcPrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateVpcPrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateVpcPrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateVpcPrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.CreateVpcPrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAlgoGroup(self, request):
        """删除个人算法组接口

        :param request: Request instance for DeleteAlgoGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAlgoGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAlgoGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAlgoGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAlgoGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAlgoVersion(self, request):
        """删除个人算法版本接口

        :param request: Request instance for DeleteAlgoVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAlgoVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAlgoVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAlgoVersion", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAlgoVersionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAnnotateRecords(self, request):
        """删除标注样本

        :param request: Request instance for DeleteAnnotateRecords.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotateRecordsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotateRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAnnotateRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAnnotateRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAnnotatedTask(self, request):
        """本接口(DeleteAnnotatedTask)用于删除标注任务

        :param request: Request instance for DeleteAnnotatedTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotatedTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotatedTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAnnotatedTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAnnotatedTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAutoMLNLPPredictRecord(self, request):
        """删除文本分类预测记录

        :param request: Request instance for DeleteAutoMLNLPPredictRecord.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLNLPPredictRecordRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLNLPPredictRecordResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAutoMLNLPPredictRecord", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAutoMLNLPPredictRecordResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteAutoMLTask(self, request):
        """删除自动学习任务

        :param request: Request instance for DeleteAutoMLTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAutoMLTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteAutoMLTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteBatchTask(self, request):
        """删除批量预测任务

        :param request: Request instance for DeleteBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBatchTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteBatchTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteBillingResourceGroup(self, request):
        """删除资源组，支持场景：资源组下节点不存在部署中，运行中，释放中状态

        :param request: Request instance for DeleteBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteBillingResourceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteBillingResourceInstance(self, request):
        """删除资源组节点；支持场景：部署失败和已释放节点

        :param request: Request instance for DeleteBillingResourceInstance.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceInstanceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBillingResourceInstance", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteBillingResourceInstanceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteChatWhiteListUser(self, request):
        """删除聊天白名单用户

        :param request: Request instance for DeleteChatWhiteListUser.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteChatWhiteListUserRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteChatWhiteListUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteChatWhiteListUser", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteChatWhiteListUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteCodeRepo(self, request):
        """删除代码仓库

        :param request: Request instance for DeleteCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteCodeRepo", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteCodeRepoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteDataPipelineTask(self, request):
        """删除数据构建任务

        :param request: Request instance for DeleteDataPipelineTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteDataPipelineTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteDataPipelineTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataPipelineTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDataPipelineTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteDataSource(self, request):
        """删除数据源

        :param request: Request instance for DeleteDataSource.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteDataSourceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteDataSourceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataSource", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDataSourceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteDataset(self, request):
        """删除数据集

        :param request: Request instance for DeleteDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataset", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDatasetResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteExport(self, request):
        """删除任务式建模训练任务，Notebook，在线服务和批量预测任务日志导出任务API

        :param request: Request instance for DeleteExport.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteExportRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteExportResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteExport", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteExportResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteFlow(self, request):
        """删除工作流

        :param request: Request instance for DeleteFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteFlow", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteFlowRun(self, request):
        """删除工作流的一次执行

        :param request: Request instance for DeleteFlowRun.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteFlowRunRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteFlowRunResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteFlowRun", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteFlowRunResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteInferGateway(self, request):
        """删除推理服务使用的独立部署的专享网关及对应的

        :param request: Request instance for DeleteInferGateway.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteInferGatewayRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteInferGatewayResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteInferGateway", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteInferGatewayResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteLifecycleScript(self, request):
        """删除生命周期脚本

        :param request: Request instance for DeleteLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteLifecycleScript", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteLifecycleScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteModel(self, request):
        """编辑模型标签

        :param request: Request instance for DeleteModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModel", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteModelAccelerateTask(self, request):
        """删除模型加速任务

        :param request: Request instance for DeleteModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteModelAccelerateTasks(self, request):
        """批量删除模型加速任务

        :param request: Request instance for DeleteModelAccelerateTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelAccelerateTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteModelAccelerateTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteModelService(self, request):
        """根据服务id删除模型服务

        :param request: Request instance for DeleteModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelService", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteModelServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteModelServiceGroup(self, request):
        """根据服务组id删除服务组下所有模型服务

        :param request: Request instance for DeleteModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelServiceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteModelServiceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteNotebook(self, request):
        """删除Notebook

        :param request: Request instance for DeleteNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteNotebookImageRecord(self, request):
        """删除notebook镜像保存记录

        :param request: Request instance for DeleteNotebookImageRecord.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookImageRecordRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookImageRecordResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteNotebookImageRecord", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteNotebookImageRecordResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteObjectiveEvaluation(self, request):
        """删除客观评测接口

        :param request: Request instance for DeleteObjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteObjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteObjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteObjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteObjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeletePrivateLink(self, request):
        """用于删除用户VPC到TIONE的私有连接通道

        :param request: Request instance for DeletePrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeletePrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeletePrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeletePrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.DeletePrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteProject(self, request):
        """删除工程

        :param request: Request instance for DeleteProject.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteProjectRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteProjectResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteProject", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteProjectResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteRecyclePolicy(self, request):
        """删除回收策略

        :param request: Request instance for DeleteRecyclePolicy.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteRecyclePolicyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteRecyclePolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteRecyclePolicy", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteRecyclePolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteSubjectiveEvaluation(self, request):
        """删除主观评测接口

        :param request: Request instance for DeleteSubjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteSubjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteSubjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSubjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSubjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTaskComparison(self, request):
        """删除对比评测任务

        :param request: Request instance for DeleteTaskComparison.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTaskComparisonRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTaskComparisonResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTaskComparison", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTaskComparisonResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTaskProcess(self, request):
        """删除任务进度

        :param request: Request instance for DeleteTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTaskProcess", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTaskProcessResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTencentLabWhitelist(self, request):
        """为腾学会上课的子用户删除上课的子用户的白名单和资源的接口，仅供制定腾学会运营账号调用

        :param request: Request instance for DeleteTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTencentLabWhitelistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户删除上课的子用户的白名单和资源的接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for DeleteTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTencentLabWhitelistTestResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTrainingMetrics(self, request):
        """删除训练自定义指标

        :param request: Request instance for DeleteTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTrainingModel(self, request):
        """删除模型

        :param request: Request instance for DeleteTrainingModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingModel", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTrainingModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTrainingModelVersion(self, request):
        """删除模型版本

        :param request: Request instance for DeleteTrainingModelVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingModelVersion", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTrainingModelVersionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteTrainingTask(self, request):
        """删除训练任务

        :param request: Request instance for DeleteTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteVpcPrivateLink(self, request):
        """删除VPC私有连接

        :param request: Request instance for DeleteVpcPrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteVpcPrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteVpcPrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteVpcPrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteVpcPrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeliverBillingResource(self, request):
        """续费资源组节点

        :param request: Request instance for DeliverBillingResource.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeliverBillingResourceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeliverBillingResourceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeliverBillingResource", params, headers=headers)
            response = json.loads(body)
            model = models.DeliverBillingResourceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAPIConfigs(self, request):
        """列举API

        :param request: Request instance for DescribeAPIConfigs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAPIConfigsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAPIConfigsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAPIConfigs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAPIConfigsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAlgoGroupList(self, request):
        """个人算法列表

        :param request: Request instance for DescribeAlgoGroupList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAlgoGroupListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAlgoGroupListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAlgoGroupList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAlgoGroupListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAlgoVersionList(self, request):
        """个人算法版本列表

        :param request: Request instance for DescribeAlgoVersionList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAlgoVersionListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAlgoVersionListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAlgoVersionList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAlgoVersionListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAnnotateRecordList(self, request):
        """获取标注样本列表

        :param request: Request instance for DescribeAnnotateRecordList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateRecordListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateRecordListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotateRecordList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAnnotateRecordListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAnnotateTaskStatus(self, request):
        """查询标注任务状态

        :param request: Request instance for DescribeAnnotateTaskStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateTaskStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateTaskStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotateTaskStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAnnotateTaskStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAnnotateTaskTempCosInfo(self, request):
        """获取用于上传标注图片的临时密钥

        :param request: Request instance for DescribeAnnotateTaskTempCosInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateTaskTempCosInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotateTaskTempCosInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotateTaskTempCosInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAnnotateTaskTempCosInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAnnotatedTaskList(self, request):
        """本接口（DescribeAnnotatedTaskList）用于查询用户标注任务详细信息列表；支持各种过滤条件；

        :param request: Request instance for DescribeAnnotatedTaskList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotatedTaskListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotatedTaskListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotatedTaskList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAnnotatedTaskListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAnnotationKeys(self, request):
        """【OCR】查询数据集下的key名字典详情

        :param request: Request instance for DescribeAnnotationKeys.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotationKeysRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotationKeysResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotationKeys", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAnnotationKeysResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAsyncChatMessage(self, request):
        """查询异步对话的结果

        :param request: Request instance for DescribeAsyncChatMessage.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAsyncChatMessageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAsyncChatMessageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAsyncChatMessage", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAsyncChatMessageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAsyncTaskStatus(self, request):
        """查询指定异步任务状态和结果

        :param request: Request instance for DescribeAsyncTaskStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAsyncTaskStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAsyncTaskStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAsyncTaskStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAsyncTaskStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEMSAPIInfo(self, request):
        """查询自动学习发布模型服务接口调用信息

        :param request: Request instance for DescribeAutoMLEMSAPIInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSAPIInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSAPIInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSAPIInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEMSAPIInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEMSTask(self, request):
        """查询自动学习发布模型服务任务详情

        :param request: Request instance for DescribeAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEMSTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEMSTasks(self, request):
        """查询自动学习模型服务任务列表

        :param request: Request instance for DescribeAutoMLEMSTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEMSTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEMSTasksTrainLabels(self, request):
        """获取当前发布任务所用到的训练集kv

        :param request: Request instance for DescribeAutoMLEMSTasksTrainLabels.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksTrainLabelsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksTrainLabelsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTasksTrainLabels", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEMSTasksTrainLabelsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEMSTempCosInfo(self, request):
        """获取自动学习任务服务测试Cos信息

        :param request: Request instance for DescribeAutoMLEMSTempCosInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTempCosInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTempCosInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTempCosInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEMSTempCosInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEvaluationIdByAutoMLTaskId(self, request):
        """根据自动学习任务id查询评测id

        :param request: Request instance for DescribeAutoMLEvaluationIdByAutoMLTaskId.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationIdByAutoMLTaskIdRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationIdByAutoMLTaskIdResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationIdByAutoMLTaskId", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEvaluationIdByAutoMLTaskIdResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEvaluationNLUTaskReportUrl(self, request):
        """获取NLU评测报告下载链接

        :param request: Request instance for DescribeAutoMLEvaluationNLUTaskReportUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationNLUTaskReportUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationNLUTaskReportUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationNLUTaskReportUrl", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEvaluationNLUTaskReportUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEvaluationTaskStatus(self, request):
        """查询自动学习评测任务状态

        :param request: Request instance for DescribeAutoMLEvaluationTaskStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTaskStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTaskStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationTaskStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEvaluationTaskStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLEvaluationTasks(self, request):
        """查询自动学习评测任务列表信息

        :param request: Request instance for DescribeAutoMLEvaluationTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLEvaluationTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLModelServiceInfo(self, request):
        """获取EMS正式发布所需信息

        :param request: Request instance for DescribeAutoMLModelServiceInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLModelServiceInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLModelServiceInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLModelServiceInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLModelServiceInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLNLPPredictRecords(self, request):
        """查询自动学习文本分类推理记录列表

        :param request: Request instance for DescribeAutoMLNLPPredictRecords.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLNLPPredictRecordsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLNLPPredictRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLNLPPredictRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLNLPPredictRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskCommonEvaluationBadCases(self, request):
        """查询评测任务badcase

        :param request: Request instance for DescribeAutoMLTaskCommonEvaluationBadCases.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationBadCasesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationBadCasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskCommonEvaluationBadCases", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskCommonEvaluationBadCasesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskCommonEvaluationDetail(self, request):
        """获取评测任务的基础信息

        :param request: Request instance for DescribeAutoMLTaskCommonEvaluationDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskCommonEvaluationDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskCommonEvaluationDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskCommonEvaluationIndicator(self, request):
        """获取评测任务指标

        :param request: Request instance for DescribeAutoMLTaskCommonEvaluationIndicator.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationIndicatorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskCommonEvaluationIndicatorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskCommonEvaluationIndicator", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskCommonEvaluationIndicatorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskConfig(self, request):
        """查询自动学习任务配置

        :param request: Request instance for DescribeAutoMLTaskConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEMSTempCosInfo(self, request):
        """获取自动学习任务服务测试Cos信息

        :param request: Request instance for DescribeAutoMLTaskEMSTempCosInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEMSTempCosInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEMSTempCosInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEMSTempCosInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEMSTempCosInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationASRBadcase(self, request):
        """获取自动学习ASR评测任务badcase信息

        :param request: Request instance for DescribeAutoMLTaskEvaluationASRBadcase.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRBadcaseRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRBadcaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationASRBadcase", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationASRBadcaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationASRBaseIndicator(self, request):
        """获取ASR评测任务基础指标

        :param request: Request instance for DescribeAutoMLTaskEvaluationASRBaseIndicator.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRBaseIndicatorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRBaseIndicatorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationASRBaseIndicator", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationASRBaseIndicatorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationASRDetail(self, request):
        """查询ASR评测任务的基础信息

        :param request: Request instance for DescribeAutoMLTaskEvaluationASRDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationASRDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationASRDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationASRDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationBadcases(self, request):
        """查询自动学习评测任务badcase详情

        :param request: Request instance for DescribeAutoMLTaskEvaluationBadcases.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBadcasesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBadcasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationBadcases", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationBadcasesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationBaseIndicators(self, request):
        """查询自动学习评测结果基础指标

        :param request: Request instance for DescribeAutoMLTaskEvaluationBaseIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBaseIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBaseIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationBaseIndicators", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationBaseIndicatorsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationDetail(self, request):
        """查询自动学习评测任务基本详情

        :param request: Request instance for DescribeAutoMLTaskEvaluationDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationNLUSeniorIndicator(self, request):
        """获取NLU评测任务的细节指标

        :param request: Request instance for DescribeAutoMLTaskEvaluationNLUSeniorIndicator.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationNLUSeniorIndicatorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationNLUSeniorIndicatorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationNLUSeniorIndicator", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationNLUSeniorIndicatorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskEvaluationSeniorIndicators(self, request):
        """查询自动学习评测任务高阶指标信息

        :param request: Request instance for DescribeAutoMLTaskEvaluationSeniorIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationSeniorIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationSeniorIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationSeniorIndicators", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskEvaluationSeniorIndicatorsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskNLPEvaluationBadcases(self, request):
        """查询自动学习NLP评测任务badcase详情

        :param request: Request instance for DescribeAutoMLTaskNLPEvaluationBadcases.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLPEvaluationBadcasesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLPEvaluationBadcasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskNLPEvaluationBadcases", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskNLPEvaluationBadcasesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskNLUEvaluationBaseIndicator(self, request):
        """获取NLU评测任务的整体指标

        :param request: Request instance for DescribeAutoMLTaskNLUEvaluationBaseIndicator.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLUEvaluationBaseIndicatorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLUEvaluationBaseIndicatorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskNLUEvaluationBaseIndicator", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskNLUEvaluationBaseIndicatorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskNLUEvaluationSeniorIndicator(self, request):
        """获取云小微NLP任务的进阶指标

        :param request: Request instance for DescribeAutoMLTaskNLUEvaluationSeniorIndicator.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLUEvaluationSeniorIndicatorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLUEvaluationSeniorIndicatorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskNLUEvaluationSeniorIndicator", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskNLUEvaluationSeniorIndicatorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskTrainDetail(self, request):
        """查询训练任务详情

        :param request: Request instance for DescribeAutoMLTaskTrainDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskTrainDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskTrainDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTaskTrainIndicators(self, request):
        """查询训练任务指标

        :param request: Request instance for DescribeAutoMLTaskTrainIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskTrainIndicators", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTaskTrainIndicatorsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMLTrainTasks(self, request):
        """列举自动学习训练任务组列表

        :param request: Request instance for DescribeAutoMLTrainTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTrainTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTrainTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTrainTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMLTrainTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoMlTaskIntentSlots(self, request):
        """获取意图槽位列表

        :param request: Request instance for DescribeAutoMlTaskIntentSlots.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMlTaskIntentSlotsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMlTaskIntentSlotsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMlTaskIntentSlots", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoMlTaskIntentSlotsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAutoOcrPrediction(self, request):
        """自动文字识别预测

        :param request: Request instance for DescribeAutoOcrPrediction.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoOcrPredictionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoOcrPredictionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoOcrPrediction", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAutoOcrPredictionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAvailableNodeStatistic(self, request):
        """列取按照可用节点数聚合的资源组信息

        :param request: Request instance for DescribeAvailableNodeStatistic.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAvailableNodeStatisticRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAvailableNodeStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAvailableNodeStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAvailableNodeStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeAvailableSWInstances(self, request):
        """获取可纳管实例

        :param request: Request instance for DescribeAvailableSWInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAvailableSWInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAvailableSWInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAvailableSWInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAvailableSWInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBadcasePreviewStatus(self, request):
        """查询自动学习badcase图片预览设置状态

        :param request: Request instance for DescribeBadcasePreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBadcasePreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBadcasePreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBadcasePreviewStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBadcasePreviewStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBatchTask(self, request):
        """查询批量预测任务

        :param request: Request instance for DescribeBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBatchTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBatchTaskInstances(self, request):
        """查询批量预测任务实例列表

        :param request: Request instance for DescribeBatchTaskInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBatchTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBatchTasks(self, request):
        """查询批量预测任务列表信息

        :param request: Request instance for DescribeBatchTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBatchTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceGroup(self, request):
        """查询资源组节点列表

        :param request: Request instance for DescribeBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceGroupRunningJobs(self, request):
        """查询资源组运行中的任务

        :param request: Request instance for DescribeBillingResourceGroupRunningJobs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupRunningJobsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupRunningJobsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceGroupRunningJobs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceGroupRunningJobsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceGroups(self, request):
        """查询资源组详情

        :param request: Request instance for DescribeBillingResourceGroups.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceInstanceGroupByGpuType(self, request):
        """查询资源组下按GPU型号聚合的节点列表

        :param request: Request instance for DescribeBillingResourceInstanceGroupByGpuType.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceGroupByGpuTypeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceGroupByGpuTypeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstanceGroupByGpuType", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceInstanceGroupByGpuTypeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceInstanceRunningJobs(self, request):
        """查询资源组节点运行中的任务

        :param request: Request instance for DescribeBillingResourceInstanceRunningJobs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceRunningJobsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceRunningJobsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstanceRunningJobs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceInstanceRunningJobsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceInstanceRunningJobsBatch(self, request):
        """批量查询资源组节点运行中任务

        :param request: Request instance for DescribeBillingResourceInstanceRunningJobsBatch.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceRunningJobsBatchRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceRunningJobsBatchResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstanceRunningJobsBatch", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceInstanceRunningJobsBatchResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceInstanceStatusStatistic(self, request):
        """查询资源组节点状态统计

        :param request: Request instance for DescribeBillingResourceInstanceStatusStatistic.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceStatusStatisticRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceStatusStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstanceStatusStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceInstanceStatusStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingResourceInstances(self, request):
        """查询资源组节点列表详情

        :param request: Request instance for DescribeBillingResourceInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingResourceInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingSpecs(self, request):
        """本接口(DescribeBillingSpecs) 提供查询计费项列表

        :param request: Request instance for DescribeBillingSpecs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingSpecs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingSpecsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingSpecsPrice(self, request):
        """本接口(DescribeBillingSpecsPrice)用于查询按量计费计费项价格。

        :param request: Request instance for DescribeBillingSpecsPrice.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingSpecsPrice", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingSpecsPriceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBillingUserList(self, request):
        """本接口(DescribeBillingUserList)查询并返回指定用户列表

        :param request: Request instance for DescribeBillingUserList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingUserListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingUserListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingUserList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBillingUserListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeBuildInImages(self, request):
        """获取内置镜像列表

        :param request: Request instance for DescribeBuildInImages.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBuildInImagesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBuildInImagesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBuildInImages", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBuildInImagesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeCVMSemiPrecheck(self, request):
        """在纳管CVM节点前，检查CVM节点的配置是否符合纳管要求

        :param request: Request instance for DescribeCVMSemiPrecheck.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCVMSemiPrecheckRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCVMSemiPrecheckResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCVMSemiPrecheck", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCVMSemiPrecheckResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeChatServiceStatus(self, request):
        """获取聊天服务可用状态

        :param request: Request instance for DescribeChatServiceStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeChatServiceStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeChatServiceStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeChatServiceStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeChatServiceStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeCheckpointList(self, request):
        """查询 Checkpoint 列表

        :param request: Request instance for DescribeCheckpointList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCheckpointListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCheckpointListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCheckpointList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCheckpointListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeCodeRepo(self, request):
        """代码仓库详情

        :param request: Request instance for DescribeCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCodeRepo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCodeRepoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeCodeRepos(self, request):
        """代码仓库列表

        :param request: Request instance for DescribeCodeRepos.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCodeReposRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCodeReposResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCodeRepos", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCodeReposResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeComparisonResults(self, request):
        """对比大模型评测

        :param request: Request instance for DescribeComparisonResults.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeComparisonResultsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeComparisonResultsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeComparisonResults", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeComparisonResultsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeComparisonsOutputs(self, request):
        """下载对比结果

        :param request: Request instance for DescribeComparisonsOutputs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeComparisonsOutputsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeComparisonsOutputsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeComparisonsOutputs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeComparisonsOutputsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeContentByMD5(self, request):
        """根据MD5查询文本内容

        :param request: Request instance for DescribeContentByMD5.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeContentByMD5Request`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeContentByMD5Response`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeContentByMD5", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeContentByMD5Response()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDataPipelineConfig(self, request):
        """获取数据构建任务可选配置

        :param request: Request instance for DescribeDataPipelineConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataPipelineConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataPipelineConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDataPipelineTask(self, request):
        """查询数据构建任务

        :param request: Request instance for DescribeDataPipelineTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataPipelineTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataPipelineTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDataPipelineTasks(self, request):
        """查询数据构建任务列表

        :param request: Request instance for DescribeDataPipelineTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDataPipelineTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataPipelineTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataPipelineTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetAnnotationPreview(self, request):
        """预览标注工作台

        :param request: Request instance for DescribeDatasetAnnotationPreview.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetAnnotationPreviewRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetAnnotationPreviewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetAnnotationPreview", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetAnnotationPreviewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetConfig(self, request):
        """查询数据集建模场景配置

        :param request: Request instance for DescribeDatasetConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDetailLLM(self, request):
        """查询大模型数据集样本详情

        :param request: Request instance for DescribeDatasetDetailLLM.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailLLMRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailLLMResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailLLM", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDetailLLMResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDetailStructured(self, request):
        """查询结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailStructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailStructured", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDetailStructuredResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDetailText(self, request):
        """查询文本数据集详情

        :param request: Request instance for DescribeDatasetDetailText.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailTextRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailTextResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailText", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDetailTextResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDetailUnstructured(self, request):
        """查询非结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailUnstructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailUnstructured", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDetailUnstructuredResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDistributionStructured(self, request):
        """查询表格类数据集字段分布统计

        :param request: Request instance for DescribeDatasetDistributionStructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionStructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionStructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDistributionStructured", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDistributionStructuredResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetDistributionUnstructured(self, request):
        """查询非结构化标签分布详情

        :param request: Request instance for DescribeDatasetDistributionUnstructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionUnstructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionUnstructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDistributionUnstructured", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetDistributionUnstructuredResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetFileList(self, request):
        """查询数据集文件列表详情

        :param request: Request instance for DescribeDatasetFileList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetFileListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetFileListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetFileList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetFileListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetImageUrls(self, request):
        """查询数据集图片下载链接

        :param request: Request instance for DescribeDatasetImageUrls.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetImageUrlsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetImageUrlsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetImageUrls", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetImageUrlsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetOcrScene(self, request):
        """查询OCR场景数据集的标签子类别

        :param request: Request instance for DescribeDatasetOcrScene.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetOcrSceneRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetOcrSceneResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetOcrScene", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetOcrSceneResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetPerspectiveStatus(self, request):
        """查询文本数据集数据透视预览状态

        :param request: Request instance for DescribeDatasetPerspectiveStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPerspectiveStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPerspectiveStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetPerspectiveStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetPerspectiveStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetPreview(self, request):
        """获取数据集以供预览

        :param request: Request instance for DescribeDatasetPreview.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetPreview", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetPreviewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetPreviewStatus(self, request):
        """查询数据集预览状态

        :param request: Request instance for DescribeDatasetPreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetPreviewStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetPreviewStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetSchema(self, request):
        """查询表格数据集头信息

        :param request: Request instance for DescribeDatasetSchema.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetSchema", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetSchemaResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetSchemaPreview(self, request):
        """获取schema以供预览

        :param request: Request instance for DescribeDatasetSchemaPreview.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaPreviewRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaPreviewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetSchemaPreview", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetSchemaPreviewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetSchemaTasks(self, request):
        """查询数据集Schema任务列表

        :param request: Request instance for DescribeDatasetSchemaTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetSchemaTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetSchemaTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasetTextAnalyze(self, request):
        """查询文本数据透视

        :param request: Request instance for DescribeDatasetTextAnalyze.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetTextAnalyzeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetTextAnalyzeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetTextAnalyze", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetTextAnalyzeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDatasets(self, request):
        """查询数据集列表

        :param request: Request instance for DescribeDatasets.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasets", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasetsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDealOrder(self, request):
        """查询订单详情

        :param request: Request instance for DescribeDealOrder.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDealOrderRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDealOrderResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDealOrder", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDealOrderResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDemoFlow(self, request):
        """获取案例工作流的结构、参数

        :param request: Request instance for DescribeDemoFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDemoFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDemoFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDemoFlow", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDemoFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDemoFlows(self, request):
        """查询案例工作流列表

        :param request: Request instance for DescribeDemoFlows.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDemoFlowsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDemoFlowsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDemoFlows", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDemoFlowsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDemoProjects(self, request):
        """查看案例工程列表

        :param request: Request instance for DescribeDemoProjects.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDemoProjectsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDemoProjectsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDemoProjects", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDemoProjectsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeDirectoryContents(self, request):
        """拉取指定路径下的文件（夹）列表

        :param request: Request instance for DescribeDirectoryContents.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDirectoryContentsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDirectoryContentsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDirectoryContents", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDirectoryContentsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeEvaluationBuiltInDatasets(self, request):
        """获取内置评测集

        :param request: Request instance for DescribeEvaluationBuiltInDatasets.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeEvaluationBuiltInDatasetsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeEvaluationBuiltInDatasetsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEvaluationBuiltInDatasets", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeEvaluationBuiltInDatasetsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeEvaluationSummaries(self, request):
        """获取评测结果

        :param request: Request instance for DescribeEvaluationSummaries.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeEvaluationSummariesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeEvaluationSummariesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEvaluationSummaries", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeEvaluationSummariesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeEvents(self, request):
        """获取任务式建模训练任务，Notebook，在线服务和批量预测任务的事件API

        :param request: Request instance for DescribeEvents.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeEventsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeEventsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEvents", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeEventsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeExport(self, request):
        """查看任务式建模训练任务，Notebook，在线服务和批量预测任务日志下载任务状态API

        :param request: Request instance for DescribeExport.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeExportRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeExportResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeExport", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeExportResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFilePreviewUrl(self, request):
        """预览文件

        :param request: Request instance for DescribeFilePreviewUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFilePreviewUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFilePreviewUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFilePreviewUrl", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFilePreviewUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFileStatus(self, request):
        """获取文件状态

        :param request: Request instance for DescribeFileStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFileStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFileStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFileStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFileStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFileSystemsWithPathAccessibility(self, request):
        """创建任务式建模、Notebook时，列取包含当前用户可访问路径的CFS实例列表

        :param request: Request instance for DescribeFileSystemsWithPathAccessibility.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFileSystemsWithPathAccessibilityRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFileSystemsWithPathAccessibilityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFileSystemsWithPathAccessibility", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFileSystemsWithPathAccessibilityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFixedPoint(self, request):
        """本接口(DescribeFixedPoint)用于获取固定点数

        :param request: Request instance for DescribeFixedPoint.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFixedPointRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFixedPointResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFixedPoint", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFixedPointResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlow(self, request):
        """获取工作流的结构、参数和基本状态（画布的状态、最新运行时间）

        :param request: Request instance for DescribeFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlow", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowEvaluationDetail(self, request):
        """查看工作流评估报告

        :param request: Request instance for DescribeFlowEvaluationDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowEvaluationDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowEvaluationDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowEvaluationDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowEvaluationDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowModelTree(self, request):
        """查看工作流算子模型树

        :param request: Request instance for DescribeFlowModelTree.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowModelTreeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowModelTreeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowModelTree", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowModelTreeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowOperatorCategories(self, request):
        """查询算子类别目录结构

        :param request: Request instance for DescribeFlowOperatorCategories.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowOperatorCategoriesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowOperatorCategoriesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowOperatorCategories", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowOperatorCategoriesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowOperators(self, request):
        """批量查询算子详情

        :param request: Request instance for DescribeFlowOperators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowOperatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowOperatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowOperators", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowOperatorsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowPreviewColumn(self, request):
        """工作流节点数据预览列统计值

        :param request: Request instance for DescribeFlowPreviewColumn.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewColumnRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewColumnResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowPreviewColumn", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowPreviewColumnResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowPreviewDatas(self, request):
        """预览工作流节点数据

        :param request: Request instance for DescribeFlowPreviewDatas.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewDatasRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewDatasResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowPreviewDatas", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowPreviewDatasResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowPreviewPath(self, request):
        """查看工作流节点数据预览路径

        :param request: Request instance for DescribeFlowPreviewPath.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewPathRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowPreviewPathResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowPreviewPath", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowPreviewPathResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowRun(self, request):
        """查看工作流执行的详情

        :param request: Request instance for DescribeFlowRun.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowRunRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowRunResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowRun", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowRunResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowRuns(self, request):
        """查看工作流执行列表

        :param request: Request instance for DescribeFlowRuns.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowRunsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowRunsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowRuns", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowRunsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlowSummary(self, request):
        """获取工作流的基本状态（画布的状态、最新运行时间。 轻量的查询，不含节点和边信息）

        :param request: Request instance for DescribeFlowSummary.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowSummaryRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowSummaryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlowSummary", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowSummaryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeFlows(self, request):
        """查询工作流列表

        :param request: Request instance for DescribeFlows.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFlowsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFlowsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFlows", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFlowsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeILabelDataValidity(self, request):
        """检查标签是否满足指定场景的测试数据标注文本格式

        :param request: Request instance for DescribeILabelDataValidity.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeILabelDataValidityRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeILabelDataValidityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeILabelDataValidity", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeILabelDataValidityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeImagesInfo(self, request):
        """本接口(DescribeImagesInfo)用于获取图片及信息

        :param request: Request instance for DescribeImagesInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeImagesInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeImagesInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeImagesInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeImagesInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInferCode(self, request):
        """查询推理代码的状态

        :param request: Request instance for DescribeInferCode.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInferCodeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInferCodeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInferCode", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInferCodeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInferGatewayStatus(self, request):
        """查询推理专项网关的运行状态

        :param request: Request instance for DescribeInferGatewayStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInferGatewayStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInferGatewayStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInferGatewayStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInferGatewayStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInferTemplates(self, request):
        """查询推理镜像模板

        :param request: Request instance for DescribeInferTemplates.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInferTemplatesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInferTemplatesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInferTemplates", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInferTemplatesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInsideAction(self, request):
        """调用内网服务接口

        :param request: Request instance for DescribeInsideAction.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInsideActionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInsideActionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInsideAction", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInsideActionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInstanceCredential(self, request):
        """获取实例内用户临时秘钥

        :param request: Request instance for DescribeInstanceCredential.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceCredentialRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceCredentialResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInstanceCredential", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInstanceCredentialResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeInstanceSemiProgress(self, request):
        """查询实例纳管进度

        :param request: Request instance for DescribeInstanceSemiProgress.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceSemiProgressRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceSemiProgressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInstanceSemiProgress", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInstanceSemiProgressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeIsTaskNameExist(self, request):
        """本接口(DescribeIsTaskNameExist)用来查询新建标注任务时的名称是否重复

        :param request: Request instance for DescribeIsTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeIsTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeIsTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeIsTaskNameExist", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeIsTaskNameExistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLabelColor(self, request):
        """本接口(DescribeLabelColor)用于获取标签颜色

        :param request: Request instance for DescribeLabelColor.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLabelColorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLabelColorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLabelColor", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLabelColorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLastRunNodes(self, request):
        """获取工作流画布的状态（包含全部节点的所有执行里面最新的状态）

        :param request: Request instance for DescribeLastRunNodes.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLastRunNodesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLastRunNodesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLastRunNodes", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLastRunNodesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLatestComparisonEvaluations(self, request):
        """获取该子用户上一次的模型对比情况，包括所选的任务，以及对应任务包含的模型、CFS评测集/开源数据集

        :param request: Request instance for DescribeLatestComparisonEvaluations.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLatestComparisonEvaluationsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLatestComparisonEvaluationsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLatestComparisonEvaluations", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLatestComparisonEvaluationsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLatestTrainingMetrics(self, request):
        """查询最近上报的训练自定义指标

        :param request: Request instance for DescribeLatestTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLatestTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLatestTrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLifecycleScript(self, request):
        """查看生命周期脚本详情

        :param request: Request instance for DescribeLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLifecycleScript", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLifecycleScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLifecycleScripts(self, request):
        """查看生命周期脚本列表

        :param request: Request instance for DescribeLifecycleScripts.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLifecycleScripts", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLifecycleScriptsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeLogs(self, request):
        """获取任务式建模训练任务，Notebook，在线服务和批量预测任务的日志API

        :param request: Request instance for DescribeLogs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLogsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLogsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLogs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLogsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModel(self, request):
        """新版模型仓库创建接口

        :param request: Request instance for DescribeModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModel", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelAccEngineVersions(self, request):
        """查询模型加速引擎版本列表

        :param request: Request instance for DescribeModelAccEngineVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccEngineVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccEngineVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccEngineVersions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelAccEngineVersionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelAccOptimizedReport(self, request):
        """查询模型加速优化报告

        :param request: Request instance for DescribeModelAccOptimizedReport.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccOptimizedReportRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccOptimizedReportResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccOptimizedReport", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelAccOptimizedReportResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelAccelerateTask(self, request):
        """查询模型优化任务详情

        :param request: Request instance for DescribeModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelAccelerateTasks(self, request):
        """查询模型加速任务列表

        :param request: Request instance for DescribeModelAccelerateTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelAccelerateTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelAccelerateVersions(self, request):
        """模型加速之后的模型版本列表

        :param request: Request instance for DescribeModelAccelerateVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateVersions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelAccelerateVersionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelList(self, request):
        """模型列表

        :param request: Request instance for DescribeModelList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelService(self, request):
        """查询单个服务

        :param request: Request instance for DescribeModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelService", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceCallInfo(self, request):
        """展示服务的调用信息

        :param request: Request instance for DescribeModelServiceCallInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceCallInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceCallInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceGroup(self, request):
        """查询单个服务组

        :param request: Request instance for DescribeModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceGroups(self, request):
        """列举在线推理服务组

        :param request: Request instance for DescribeModelServiceGroups.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceHistory(self, request):
        """展示服务的历史版本

        :param request: Request instance for DescribeModelServiceHistory.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHistoryRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHistoryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceHistory", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceHistoryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceHotUpdated(self, request):
        """用于查询模型服务能否开启热更新

        :param request: Request instance for DescribeModelServiceHotUpdated.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHotUpdatedRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHotUpdatedResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceHotUpdated", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceHotUpdatedResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServiceUserInfo(self, request):
        """内部接口，用于查询部分白名单用户的特殊配额信息

        :param request: Request instance for DescribeModelServiceUserInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceUserInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceUserInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceUserInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServiceUserInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelServices(self, request):
        """查询多个服务

        :param request: Request instance for DescribeModelServices.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServices", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelServicesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeModelTags(self, request):
        """新版模型仓库创建接口

        :param request: Request instance for DescribeModelTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelTags", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeModelTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeMonitorData(self, request):
        """查询监控数据

        :param request: Request instance for DescribeMonitorData.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeMonitorDataRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeMonitorDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMonitorData", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMonitorDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNLPDatasetContent(self, request):
        """根据datasetid和MD5获取文本内容

        :param request: Request instance for DescribeNLPDatasetContent.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNLPDatasetContentRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNLPDatasetContentResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNLPDatasetContent", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNLPDatasetContentResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNetworkConfig(self, request):
        """解析创建任务的配置信息

        :param request: Request instance for DescribeNetworkConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNetworkConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNetworkConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNetworkConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNetworkConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebook(self, request):
        """Notebook详情

        :param request: Request instance for DescribeNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebookImageKernels(self, request):
        """查询镜像kernel

        :param request: Request instance for DescribeNotebookImageKernels.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookImageKernelsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookImageKernelsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookImageKernels", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookImageKernelsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebookImageRecords(self, request):
        """查看notebook镜像保存记录

        :param request: Request instance for DescribeNotebookImageRecords.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookImageRecordsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookImageRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookImageRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookImageRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebookSaveImageConfig(self, request):
        """获取Notebook保存镜像配置信息

        :param request: Request instance for DescribeNotebookSaveImageConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookSaveImageConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookSaveImageConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSaveImageConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSaveImageConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebookSecondaryStatus(self, request):
        """查询Notebook实例二级状态

        :param request: Request instance for DescribeNotebookSecondaryStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookSecondaryStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookSecondaryStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSecondaryStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSecondaryStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebookStorageQuota(self, request):
        """获取notebook白名单存储配额

        :param request: Request instance for DescribeNotebookStorageQuota.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookStorageQuotaRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookStorageQuotaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookStorageQuota", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookStorageQuotaResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeNotebooks(self, request):
        """Notebook列表

        :param request: Request instance for DescribeNotebooks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebooksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebooksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebooks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebooksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeObjectiveEvaluation(self, request):
        """获取客观评测详情

        :param request: Request instance for DescribeObjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeObjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeObjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeObjectiveEvaluationOutputs(self, request):
        """获取客观评测模型推理输出

        :param request: Request instance for DescribeObjectiveEvaluationOutputs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationOutputsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationOutputsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeObjectiveEvaluationOutputs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeObjectiveEvaluationOutputsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeObjectiveEvaluationProgress(self, request):
        """获取客观评测推理进度

        :param request: Request instance for DescribeObjectiveEvaluationProgress.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationProgressRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationProgressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeObjectiveEvaluationProgress", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeObjectiveEvaluationProgressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeObjectiveEvaluations(self, request):
        """获取客观评测任务列表

        :param request: Request instance for DescribeObjectiveEvaluations.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeObjectiveEvaluationsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeObjectiveEvaluations", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeObjectiveEvaluationsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePendingTrainingTasksByPriority(self, request):
        """训练任务排队优先级队列

        :param request: Request instance for DescribePendingTrainingTasksByPriority.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePendingTrainingTasksByPriorityRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePendingTrainingTasksByPriorityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePendingTrainingTasksByPriority", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePendingTrainingTasksByPriorityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePlatformImages(self, request):
        """查询平台镜像信息

        :param request: Request instance for DescribePlatformImages.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePlatformImagesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePlatformImagesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePlatformImages", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePlatformImagesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeProject(self, request):
        """工程详情

        :param request: Request instance for DescribeProject.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeProjectRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeProjectResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeProject", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeProjectResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeProjects(self, request):
        """查询工程列表

        :param request: Request instance for DescribeProjects.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeProjectsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeProjectsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeProjects", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeProjectsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePublicAlgoGroupList(self, request):
        """公共算法列表

        :param request: Request instance for DescribePublicAlgoGroupList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoGroupListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoGroupListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePublicAlgoGroupList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePublicAlgoGroupListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePublicAlgoSeriesList(self, request):
        """公共算法系列列表

        :param request: Request instance for DescribePublicAlgoSeriesList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoSeriesListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoSeriesListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePublicAlgoSeriesList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePublicAlgoSeriesListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePublicAlgoVersionList(self, request):
        """公共算法版本列表

        :param request: Request instance for DescribePublicAlgoVersionList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoVersionListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePublicAlgoVersionListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePublicAlgoVersionList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePublicAlgoVersionListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribePublicKey(self, request):
        """查询密钥加密的公钥

        :param request: Request instance for DescribePublicKey.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribePublicKeyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribePublicKeyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribePublicKey", params, headers=headers)
            response = json.loads(body)
            model = models.DescribePublicKeyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeRecommendedBillingSpec(self, request):
        """本接口(DescribeRecommendedBillingSpec) 查询托管按量计费有库存的最低推荐机型

        :param request: Request instance for DescribeRecommendedBillingSpec.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeRecommendedBillingSpecRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeRecommendedBillingSpecResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeRecommendedBillingSpec", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRecommendedBillingSpecResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeRecyclePolicies(self, request):
        """查询回收策略

        :param request: Request instance for DescribeRecyclePolicies.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeRecyclePoliciesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeRecyclePoliciesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeRecyclePolicies", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRecyclePoliciesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSceneList(self, request):
        """获取自动学习场景列表

        :param request: Request instance for DescribeSceneList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSceneListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSceneListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSceneList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSceneListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSchemaTask(self, request):
        """查询schema任务

        :param request: Request instance for DescribeSchemaTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSchemaTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSchemaTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSchemaTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSchemaTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeScoringDetail(self, request):
        """获取打分页面的信息

        :param request: Request instance for DescribeScoringDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeScoringDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeScoringDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeScoringDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeScoringDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeStorage(self, request):
        """查询用户下的存储信息

        :param request: Request instance for DescribeStorage.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeStorageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeStorageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeStorage", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeStorageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSubjectiveEvaluation(self, request):
        """获取主观评测详情

        :param request: Request instance for DescribeSubjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSubjectiveEvaluationOutputs(self, request):
        """获取主观评测模型推理输出

        :param request: Request instance for DescribeSubjectiveEvaluationOutputs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationOutputsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationOutputsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubjectiveEvaluationOutputs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubjectiveEvaluationOutputsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSubjectiveEvaluationProgress(self, request):
        """获取主观评测推理进度接口

        :param request: Request instance for DescribeSubjectiveEvaluationProgress.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationProgressRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationProgressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubjectiveEvaluationProgress", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubjectiveEvaluationProgressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSubjectiveEvaluations(self, request):
        """获取主观评测任务列表

        :param request: Request instance for DescribeSubjectiveEvaluations.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSubjectiveEvaluationsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubjectiveEvaluations", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubjectiveEvaluationsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSubuinDependencyAccessibility(self, request):
        """描述子账号依赖项可访问性

        :param request: Request instance for DescribeSubuinDependencyAccessibility.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSubuinDependencyAccessibilityRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSubuinDependencyAccessibilityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubuinDependencyAccessibility", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubuinDependencyAccessibilityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeSupportedInstanceType(self, request):
        """根据传入的模型加速任务列表，给出共同可用的GPU实例类型列表。

        :param request: Request instance for DescribeSupportedInstanceType.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSupportedInstanceTypeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSupportedInstanceTypeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSupportedInstanceType", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSupportedInstanceTypeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTAIJITemplate(self, request):
        """查询太极训练模版

        :param request: Request instance for DescribeTAIJITemplate.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITemplateRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITemplateResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTAIJITemplate", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTAIJITemplateResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTAIJITemplateList(self, request):
        """查询太极训练模版列表

        :param request: Request instance for DescribeTAIJITemplateList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITemplateListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITemplateListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTAIJITemplateList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTAIJITemplateListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTAIJITrainingMetrics(self, request):
        """查询太极任务训练自定义指标

        :param request: Request instance for DescribeTAIJITrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTAIJITrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTAIJITrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTAIJITrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTJResourceDetail(self, request):
        """查询太极应用组资源详情

        :param request: Request instance for DescribeTJResourceDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTJResourceDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTJResourceDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTJResourceDetail", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTJResourceDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskComparison(self, request):
        """获取对比评测任务详情

        :param request: Request instance for DescribeTaskComparison.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskComparison", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskComparisonResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskComparisonASRBadCaseInfo(self, request):
        """获取ASR对比评测任务的BadCase详情

        :param request: Request instance for DescribeTaskComparisonASRBadCaseInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonASRBadCaseInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonASRBadCaseInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskComparisonASRBadCaseInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskComparisonASRBadCaseInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskComparisonNLUBadCaseInfo(self, request):
        """获取NLU对比评测任务的BadCase详情

        :param request: Request instance for DescribeTaskComparisonNLUBadCaseInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonNLUBadCaseInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonNLUBadCaseInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskComparisonNLUBadCaseInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskComparisonNLUBadCaseInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskComparisons(self, request):
        """列取对比评测任务列表

        :param request: Request instance for DescribeTaskComparisons.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskComparisonsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskComparisons", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskComparisonsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskDisplayConfig(self, request):
        """本接口(DescribeTaskDisplayConfig)获取标注显示配置

        :param request: Request instance for DescribeTaskDisplayConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskDisplayConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskDisplayConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskDisplayConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskDisplayConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTaskProcess(self, request):
        """查询任务的进度

        :param request: Request instance for DescribeTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskProcess", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskProcessResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTempCosInfo(self, request):
        """获取自动学习任务服务测试Cos信息

        :param request: Request instance for DescribeTempCosInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTempCosInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTempCosInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTempCosInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTempCosInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTencentLabClassInfo(self, request):
        """正在上课的腾学汇账户调用，查询当前正在使用的腾学汇课程信息。若无对应课程，则所有返回的字段为空。

        :param request: Request instance for DescribeTencentLabClassInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTencentLabClassInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTencentLabClassInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTencentLabClassInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTencentLabClassInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTensorBoardTask(self, request):
        """TensorBoard任务详情

        :param request: Request instance for DescribeTensorBoardTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTensorBoardTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTensorBoardTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTensorBoardTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTensorBoardTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTextTaskInfo(self, request):
        """获取文本信息

        :param request: Request instance for DescribeTextTaskInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTextTaskInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTextTaskInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTextTaskInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTextTaskInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingFrameworks(self, request):
        """训练框架列表

        :param request: Request instance for DescribeTrainingFrameworks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingFrameworks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingFrameworksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingMetrics(self, request):
        """查询训练自定义指标

        :param request: Request instance for DescribeTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingModelVersion(self, request):
        """查询模型版本

        :param request: Request instance for DescribeTrainingModelVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModelVersion", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingModelVersionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingModelVersions(self, request):
        """模型版本列表

        :param request: Request instance for DescribeTrainingModelVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModelVersions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingModelVersionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingModels(self, request):
        """模型列表

        :param request: Request instance for DescribeTrainingModels.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModels", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingModelsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTask(self, request):
        """训练任务详情

        :param request: Request instance for DescribeTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTaskPlugin(self, request):
        """查询训练任务插件

        :param request: Request instance for DescribeTrainingTaskPlugin.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPluginRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPluginResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTaskPlugin", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTaskPluginResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTaskPodUrl(self, request):
        """获取单个训练任务实例的登录链接

        :param request: Request instance for DescribeTrainingTaskPodUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTaskPodUrl", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTaskPodUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTaskPods(self, request):
        """训练任务pod列表

        :param request: Request instance for DescribeTrainingTaskPods.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTaskPods", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTaskPodsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTaskSecondaryStatus(self, request):
        """查询 Checkpoint 列表

        :param request: Request instance for DescribeTrainingTaskSecondaryStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskSecondaryStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskSecondaryStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTaskSecondaryStatus", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTaskSecondaryStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTrainingTasks(self, request):
        """训练任务列表

        :param request: Request instance for DescribeTrainingTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrainingTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeUserNetworkTopology(self, request):
        """查询用户的在线服务网络拓扑

        :param request: Request instance for DescribeUserNetworkTopology.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeUserNetworkTopologyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeUserNetworkTopologyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserNetworkTopology", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserNetworkTopologyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeUserSceneTags(self, request):
        """查询数据集标签

        :param request: Request instance for DescribeUserSceneTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeUserSceneTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeUserSceneTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserSceneTags", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserSceneTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeVpcPrivateLink(self, request):
        """查询VPC私有连接详情

        :param request: Request instance for DescribeVpcPrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeVpcPrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeVpcPrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeVpcPrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeVpcPrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeVpcPrivateLinks(self, request):
        """查询VPC私有连接列表

        :param request: Request instance for DescribeVpcPrivateLinks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeVpcPrivateLinksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeVpcPrivateLinksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeVpcPrivateLinks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeVpcPrivateLinksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DestroyBillingResource(self, request):
        """释放资源组节点; 适用场景：运行中和异常状态的节点

        :param request: Request instance for DestroyBillingResource.
        :type request: :class:`tencentcloud.tione.v20211111.models.DestroyBillingResourceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DestroyBillingResourceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DestroyBillingResource", params, headers=headers)
            response = json.loads(body)
            model = models.DestroyBillingResourceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DownloadTrainingMetrics(self, request):
        """下载训练自定义指标

        :param request: Request instance for DownloadTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DownloadTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DownloadTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DownloadTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DownloadTrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DropKnowledgeBase(self, request):
        """删除知识库

        :param request: Request instance for DropKnowledgeBase.
        :type request: :class:`tencentcloud.tione.v20211111.models.DropKnowledgeBaseRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DropKnowledgeBaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropKnowledgeBase", params, headers=headers)
            response = json.loads(body)
            model = models.DropKnowledgeBaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def EnableBatchTaskClsConfig(self, request):
        """开启或者关闭批量预测任务 CLS日志投递

        :param request: Request instance for EnableBatchTaskClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableBatchTaskClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableBatchTaskClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableBatchTaskClsConfig", params, headers=headers)
            response = json.loads(body)
            model = models.EnableBatchTaskClsConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def EnableNotebookClsConfig(self, request):
        """开启或者关闭Notebook CLS日志投递

        :param request: Request instance for EnableNotebookClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableNotebookClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableNotebookClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableNotebookClsConfig", params, headers=headers)
            response = json.loads(body)
            model = models.EnableNotebookClsConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def EnableTrainingTaskClsConfig(self, request):
        """开启CLS日志投递

        :param request: Request instance for EnableTrainingTaskClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableTrainingTaskClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableTrainingTaskClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableTrainingTaskClsConfig", params, headers=headers)
            response = json.loads(body)
            model = models.EnableTrainingTaskClsConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def FetchJob(self, request):
        """拉取CFS任务

        :param request: Request instance for FetchJob.
        :type request: :class:`tencentcloud.tione.v20211111.models.FetchJobRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.FetchJobResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("FetchJob", params, headers=headers)
            response = json.loads(body)
            model = models.FetchJobResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetComparedPredictions(self, request):
        """查询对比评测报告

        :param request: Request instance for GetComparedPredictions.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetComparedPredictionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetComparedPredictionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetComparedPredictions", params, headers=headers)
            response = json.loads(body)
            model = models.GetComparedPredictionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetEvaluationSummaries(self, request):
        """获取评测结果

        :param request: Request instance for GetEvaluationSummaries.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetEvaluationSummariesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetEvaluationSummariesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetEvaluationSummaries", params, headers=headers)
            response = json.loads(body)
            model = models.GetEvaluationSummariesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetMonitorData(self, request):
        """获取云产品的监控数据。

        :param request: Request instance for GetMonitorData.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetMonitorDataRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetMonitorDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetMonitorData", params, headers=headers)
            response = json.loads(body)
            model = models.GetMonitorDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetObjectiveEvaluationOutputs(self, request):
        """获取客观评测模型推理输出

        :param request: Request instance for GetObjectiveEvaluationOutputs.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationOutputsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationOutputsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetObjectiveEvaluationOutputs", params, headers=headers)
            response = json.loads(body)
            model = models.GetObjectiveEvaluationOutputsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetObjectiveEvaluationProgress(self, request):
        """获取客观评测推理进度

        :param request: Request instance for GetObjectiveEvaluationProgress.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationProgressRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationProgressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetObjectiveEvaluationProgress", params, headers=headers)
            response = json.loads(body)
            model = models.GetObjectiveEvaluationProgressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetObjectiveEvaluations(self, request):
        """获取客观评测任务列表

        :param request: Request instance for GetObjectiveEvaluations.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetObjectiveEvaluationsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetObjectiveEvaluations", params, headers=headers)
            response = json.loads(body)
            model = models.GetObjectiveEvaluationsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetPublicKey(self, request):
        """查询密钥加密的公钥

        :param request: Request instance for GetPublicKey.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetPublicKeyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetPublicKeyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetPublicKey", params, headers=headers)
            response = json.loads(body)
            model = models.GetPublicKeyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetSubjectiveEvaluationOutputs(self, request):
        """获取主观评测模型推理输出

        :param request: Request instance for GetSubjectiveEvaluationOutputs.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationOutputsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationOutputsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetSubjectiveEvaluationOutputs", params, headers=headers)
            response = json.loads(body)
            model = models.GetSubjectiveEvaluationOutputsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetSubjectiveEvaluationProgress(self, request):
        """获取主观评测推理进度接口

        :param request: Request instance for GetSubjectiveEvaluationProgress.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationProgressRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationProgressResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetSubjectiveEvaluationProgress", params, headers=headers)
            response = json.loads(body)
            model = models.GetSubjectiveEvaluationProgressResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetSubjectiveEvaluations(self, request):
        """获取主观评测任务列表

        :param request: Request instance for GetSubjectiveEvaluations.
        :type request: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.GetSubjectiveEvaluationsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetSubjectiveEvaluations", params, headers=headers)
            response = json.loads(body)
            model = models.GetSubjectiveEvaluationsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ImportAlgo(self, request):
        """导入算法接口

        :param request: Request instance for ImportAlgo.
        :type request: :class:`tencentcloud.tione.v20211111.models.ImportAlgoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ImportAlgoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ImportAlgo", params, headers=headers)
            response = json.loads(body)
            model = models.ImportAlgoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def InferEMSProxy(self, request):
        """在线服务请求代理

        :param request: Request instance for InferEMSProxy.
        :type request: :class:`tencentcloud.tione.v20211111.models.InferEMSProxyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.InferEMSProxyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InferEMSProxy", params, headers=headers)
            response = json.loads(body)
            model = models.InferEMSProxyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def InterfaceCallTest(self, request):
        """测试用户的接口调用

        :param request: Request instance for InterfaceCallTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.InterfaceCallTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.InterfaceCallTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InterfaceCallTest", params, headers=headers)
            response = json.loads(body)
            model = models.InterfaceCallTestResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAllAnnotatedResult(self, request):
        """修改标注任务的所有标注结果状态

        :param request: Request instance for ModifyAllAnnotatedResult.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAllAnnotatedResultRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAllAnnotatedResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAllAnnotatedResult", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAllAnnotatedResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAnnotateTaskReopen(self, request):
        """重新打开标注

        :param request: Request instance for ModifyAnnotateTaskReopen.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskReopenRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskReopenResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskReopen", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAnnotateTaskReopenResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAnnotateTaskTags(self, request):
        """本接口(ModifyTaskTags)用于更新任务绑定的标签

        :param request: Request instance for ModifyAnnotateTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAnnotateTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAnnotateTaskToSubmit(self, request):
        """提交标注任务结果

        :param request: Request instance for ModifyAnnotateTaskToSubmit.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskToSubmitRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskToSubmitResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskToSubmit", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAnnotateTaskToSubmitResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAnnotatedResult(self, request):
        """本及接口(ModifyAnnotatedResult)用于修改标注结果

        :param request: Request instance for ModifyAnnotatedResult.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotatedResultRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotatedResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotatedResult", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAnnotatedResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAnnotationKeys(self, request):
        """【OCR】 更新某数据集下的key名字典

        :param request: Request instance for ModifyAnnotationKeys.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotationKeysRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotationKeysResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotationKeys", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAnnotationKeysResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyAutoMLTaskTags(self, request):
        """修改自动学习任务标签

        :param request: Request instance for ModifyAutoMLTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAutoMLTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAutoMLTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAutoMLTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAutoMLTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyBadcasePreviewStatus(self, request):
        """修改自动学习badcase图片预览设置状态

        :param request: Request instance for ModifyBadcasePreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBadcasePreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBadcasePreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBadcasePreviewStatus", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyBadcasePreviewStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyBatchTaskTags(self, request):
        """本接口(ModifyBatchTaskTags)用于更新批量预测任务绑定的标签

        :param request: Request instance for ModifyBatchTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBatchTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBatchTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBatchTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyBatchTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyBillingDeal(self, request):
        """订单状态修改

        :param request: Request instance for ModifyBillingDeal.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBillingDealRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBillingDealResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBillingDeal", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyBillingDealResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyBillingResourceGroup(self, request):
        """更新资源组名称以及标签绑定

        :param request: Request instance for ModifyBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyBillingResourceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyBillingResourceInstanceName(self, request):
        """修改资源组节点名称; 适用场景：未删除的节点

        :param request: Request instance for ModifyBillingResourceInstanceName.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceInstanceNameRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceInstanceNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBillingResourceInstanceName", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyBillingResourceInstanceNameResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyCodeRepo(self, request):
        """修改存储库

        :param request: Request instance for ModifyCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyCodeRepo", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyCodeRepoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDataPipelineTaskTags(self, request):
        """修改数据构建任务标签信息

        :param request: Request instance for ModifyDataPipelineTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDataPipelineTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDataPipelineTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDataPipelineTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDataPipelineTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetAnnotationStatus(self, request):
        """修改数据集标注状态

        :param request: Request instance for ModifyDatasetAnnotationStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetAnnotationStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetAnnotationStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetAnnotationStatus", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetAnnotationStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetDetailAnnotation(self, request):
        """更新数据集标注状态

        :param request: Request instance for ModifyDatasetDetailAnnotation.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetDetailAnnotationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetDetailAnnotationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetDetailAnnotation", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetDetailAnnotationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetPerspectiveStatus(self, request):
        """更新文本数据集数据透视预览状态

        :param request: Request instance for ModifyDatasetPerspectiveStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPerspectiveStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPerspectiveStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetPerspectiveStatus", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetPerspectiveStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetPreviewStatus(self, request):
        """修改数据集预览状态

        :param request: Request instance for ModifyDatasetPreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetPreviewStatus", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetPreviewStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetSceneTags(self, request):
        """更新数据集场景标签

        :param request: Request instance for ModifyDatasetSceneTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetSceneTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetSceneTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetSceneTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetSceneTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetSchemaToSubmit(self, request):
        """正式提交schema生成待标注数据

        :param request: Request instance for ModifyDatasetSchemaToSubmit.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetSchemaToSubmitRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetSchemaToSubmitResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetSchemaToSubmit", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetSchemaToSubmitResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyDatasetTags(self, request):
        """修改数据集标签信息

        :param request: Request instance for ModifyDatasetTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasetTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyFixedPoint(self, request):
        """本接口(ModifyFixedPoint)用于修改固定点数

        :param request: Request instance for ModifyFixedPoint.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyFixedPointRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyFixedPointResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyFixedPoint", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyFixedPointResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyFlow(self, request):
        """编辑工作流

        :param request: Request instance for ModifyFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyFlow", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyFlowWhiteListWait(self, request):
        """设置白名单等待时间

        :param request: Request instance for ModifyFlowWhiteListWait.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyFlowWhiteListWaitRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyFlowWhiteListWaitResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyFlowWhiteListWait", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyFlowWhiteListWaitResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyLifecycleScript(self, request):
        """编辑生命周期脚本

        :param request: Request instance for ModifyLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyLifecycleScript", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyLifecycleScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyModelAccTaskTags(self, request):
        """修改模型加速任务标签

        :param request: Request instance for ModifyModelAccTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelAccTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelAccTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelAccTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyModelAccTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyModelService(self, request):
        """用于更新模型服务

        :param request: Request instance for ModifyModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelService", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyModelServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyModelServiceAuthorization(self, request):
        """修改服务鉴权配置

        :param request: Request instance for ModifyModelServiceAuthorization.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceAuthorizationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceAuthorizationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelServiceAuthorization", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyModelServiceAuthorizationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyModelServicePartialConfig(self, request):
        """增量更新在线推理服务的部分配置，不更新的配置项不需要传入

        :param request: Request instance for ModifyModelServicePartialConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelServicePartialConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelServicePartialConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelServicePartialConfig", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyModelServicePartialConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyModelTags(self, request):
        """编辑模型标签

        :param request: Request instance for ModifyModelTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyModelTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyNotebook(self, request):
        """修改Notebook

        :param request: Request instance for ModifyNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyNotebookAutoStopping(self, request):
        """修改自动停止配置

        :param request: Request instance for ModifyNotebookAutoStopping.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookAutoStoppingRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookAutoStoppingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebookAutoStopping", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyNotebookAutoStoppingResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyNotebookTags(self, request):
        """修改Notebook标签

        :param request: Request instance for ModifyNotebookTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebookTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyNotebookTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyObjevalTags(self, request):
        """修改客观评测任务标签

        :param request: Request instance for ModifyObjevalTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyObjevalTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyObjevalTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyObjevalTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyObjevalTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyProject(self, request):
        """编辑工程

        :param request: Request instance for ModifyProject.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyProjectRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyProjectResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyProject", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyProjectResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyRecyclePolicy(self, request):
        """编辑回收策略

        :param request: Request instance for ModifyRecyclePolicy.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyRecyclePolicyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyRecyclePolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyRecyclePolicy", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyRecyclePolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyServiceGroupWeights(self, request):
        """更新推理服务组流量分配

        :param request: Request instance for ModifyServiceGroupWeights.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyServiceGroupWeights", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyServiceGroupWeightsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyStorageToKeepAlive(self, request):
        """保活已挂载存储

        :param request: Request instance for ModifyStorageToKeepAlive.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyStorageToKeepAliveRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyStorageToKeepAliveResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyStorageToKeepAlive", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyStorageToKeepAliveResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifySubevalTags(self, request):
        """修改主观评测任务标签

        :param request: Request instance for ModifySubevalTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifySubevalTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifySubevalTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySubevalTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySubevalTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTags(self, request):
        """编辑模型服务的标签

        :param request: Request instance for ModifyTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTaskDisplayConfig(self, request):
        """本接口(ModifyTaskDisplayConfig)修改标注显示配置

        :param request: Request instance for ModifyTaskDisplayConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskDisplayConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskDisplayConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskDisplayConfig", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTaskDisplayConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTaskLabelValue(self, request):
        """本接口(ModifyTaskLabelValue)修改任务标签值

        :param request: Request instance for ModifyTaskLabelValue.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskLabelValueRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskLabelValueResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskLabelValue", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTaskLabelValueResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTaskProcessingStatus(self, request):
        """本接口(ModifyTaskProcessingStatus)修改标注任务处理状态

        :param request: Request instance for ModifyTaskProcessingStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskProcessingStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskProcessingStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskProcessingStatus", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTaskProcessingStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTaskTags(self, request):
        """本接口(ModifyTaskTags)用于更新任务绑定的标签

        :param request: Request instance for ModifyTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskTags", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTaskTagsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyTrainingTask(self, request):
        """修改训练任务

        :param request: Request instance for ModifyTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyVpcPrivateLink(self, request):
        """修改VPC私有连接

        :param request: Request instance for ModifyVpcPrivateLink.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyVpcPrivateLinkRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyVpcPrivateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyVpcPrivateLink", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyVpcPrivateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def PublishDataset(self, request):
        """发布数据集

        :param request: Request instance for PublishDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.PublishDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PublishDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PublishDataset", params, headers=headers)
            response = json.loads(body)
            model = models.PublishDatasetResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def PushTaskProcess(self, request):
        """上报任务进度

        :param request: Request instance for PushTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.PushTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PushTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PushTaskProcess", params, headers=headers)
            response = json.loads(body)
            model = models.PushTaskProcessResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def PushTrainingMetrics(self, request):
        """上报训练自定义指标

        :param request: Request instance for PushTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.PushTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PushTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PushTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.PushTrainingMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RebuildModelServicePod(self, request):
        """重建模型服务中的单个Pod

        :param request: Request instance for RebuildModelServicePod.
        :type request: :class:`tencentcloud.tione.v20211111.models.RebuildModelServicePodRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RebuildModelServicePodResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RebuildModelServicePod", params, headers=headers)
            response = json.loads(body)
            model = models.RebuildModelServicePodResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ReleaseBillingPostpaidSWInstances(self, request):
        """释放按量计费的纳管节点

        :param request: Request instance for ReleaseBillingPostpaidSWInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.ReleaseBillingPostpaidSWInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ReleaseBillingPostpaidSWInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ReleaseBillingPostpaidSWInstances", params, headers=headers)
            response = json.loads(body)
            model = models.ReleaseBillingPostpaidSWInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RenewMountedStorage(self, request):
        """保活已挂载存储

        :param request: Request instance for RenewMountedStorage.
        :type request: :class:`tencentcloud.tione.v20211111.models.RenewMountedStorageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RenewMountedStorageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewMountedStorage", params, headers=headers)
            response = json.loads(body)
            model = models.RenewMountedStorageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RenewTencentLabWhitelist(self, request):
        """为腾学会上课的子用户续期白名单接口，仅供制定腾学会运营账号调用

        :param request: Request instance for RenewTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            model = models.RenewTencentLabWhitelistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RenewTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户续期白名单接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for RenewTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            model = models.RenewTencentLabWhitelistTestResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ReportCheckpointList(self, request):
        """上报 Checkpoint 列表

        :param request: Request instance for ReportCheckpointList.
        :type request: :class:`tencentcloud.tione.v20211111.models.ReportCheckpointListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ReportCheckpointListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ReportCheckpointList", params, headers=headers)
            response = json.loads(body)
            model = models.ReportCheckpointListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ReportJob(self, request):
        """上报CFS任务结果

        :param request: Request instance for ReportJob.
        :type request: :class:`tencentcloud.tione.v20211111.models.ReportJobRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ReportJobResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ReportJob", params, headers=headers)
            response = json.loads(body)
            model = models.ReportJobResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ReportWorker(self, request):
        """上报CFS Worker心跳

        :param request: Request instance for ReportWorker.
        :type request: :class:`tencentcloud.tione.v20211111.models.ReportWorkerRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ReportWorkerResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ReportWorker", params, headers=headers)
            response = json.loads(body)
            model = models.ReportWorkerResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RestartAutoMLModelAccelerateTask(self, request):
        """自动学习重启模型优化任务

        :param request: Request instance for RestartAutoMLModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartAutoMLModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartAutoMLModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartAutoMLModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.RestartAutoMLModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RestartModelAccelerateTask(self, request):
        """重启模型加速任务

        :param request: Request instance for RestartModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.RestartModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RestartObjectiveEvaluation(self, request):
        """重启客观评测接口

        :param request: Request instance for RestartObjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartObjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartObjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartObjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.RestartObjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RestartSubjectiveEvaluation(self, request):
        """重启主观评测接口

        :param request: Request instance for RestartSubjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartSubjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartSubjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartSubjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.RestartSubjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RunFlow(self, request):
        """运行工作流

        :param request: Request instance for RunFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.RunFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RunFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RunFlow", params, headers=headers)
            response = json.loads(body)
            model = models.RunFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SaveFlow(self, request):
        """保存工作流的画布信息

        :param request: Request instance for SaveFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.SaveFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SaveFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SaveFlow", params, headers=headers)
            response = json.loads(body)
            model = models.SaveFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SendAsyncChatMessage(self, request):
        """异步发送对话信息

        :param request: Request instance for SendAsyncChatMessage.
        :type request: :class:`tencentcloud.tione.v20211111.models.SendAsyncChatMessageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SendAsyncChatMessageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SendAsyncChatMessage", params, headers=headers)
            response = json.loads(body)
            model = models.SendAsyncChatMessageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SendChatMessage(self, request):
        """这是一个供您体验大模型聊天的接口。

        :param request: Request instance for SendChatMessage.
        :type request: :class:`tencentcloud.tione.v20211111.models.SendChatMessageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SendChatMessageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SendChatMessage", params, headers=headers)
            response = json.loads(body)
            model = models.SendChatMessageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SetRenewBillingResourceFlag(self, request):
        """设置资源组节点自动续费状态

        :param request: Request instance for SetRenewBillingResourceFlag.
        :type request: :class:`tencentcloud.tione.v20211111.models.SetRenewBillingResourceFlagRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SetRenewBillingResourceFlagResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SetRenewBillingResourceFlag", params, headers=headers)
            response = json.loads(body)
            model = models.SetRenewBillingResourceFlagResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StartAutoMLEvaluationTask(self, request):
        """启动自动学习评测任务

        :param request: Request instance for StartAutoMLEvaluationTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartAutoMLEvaluationTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartAutoMLEvaluationTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartAutoMLEvaluationTask", params, headers=headers)
            response = json.loads(body)
            model = models.StartAutoMLEvaluationTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StartAutoMLTaskTrain(self, request):
        """开始训练任务

        :param request: Request instance for StartAutoMLTaskTrain.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartAutoMLTaskTrainRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartAutoMLTaskTrainResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartAutoMLTaskTrain", params, headers=headers)
            response = json.loads(body)
            model = models.StartAutoMLTaskTrainResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StartLightEvalService(self, request):
        """启动 Checkpoint 对应的轻量体验服务，若不存在，则创建服务

        :param request: Request instance for StartLightEvalService.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartLightEvalServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartLightEvalServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartLightEvalService", params, headers=headers)
            response = json.loads(body)
            model = models.StartLightEvalServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StartNotebook(self, request):
        """启动Notebook

        :param request: Request instance for StartNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.StartNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StartTrainingTask(self, request):
        """启动模型训练任务

        :param request: Request instance for StartTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.StartTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopAutoMLEMSTask(self, request):
        """停止自动学习发布的模型服务

        :param request: Request instance for StopAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopAutoMLEMSTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopAutoMLEvaluationTask(self, request):
        """停止自动学习评测任务

        :param request: Request instance for StopAutoMLEvaluationTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEvaluationTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEvaluationTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLEvaluationTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopAutoMLEvaluationTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopAutoMLModelAccelerateTask(self, request):
        """停止自动学习模型优化任务

        :param request: Request instance for StopAutoMLModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopAutoMLModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopAutoMLTaskTrain(self, request):
        """停止训练任务

        :param request: Request instance for StopAutoMLTaskTrain.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLTaskTrainRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLTaskTrainResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLTaskTrain", params, headers=headers)
            response = json.loads(body)
            model = models.StopAutoMLTaskTrainResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopBatchTask(self, request):
        """停止批量预测任务

        :param request: Request instance for StopBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopBatchTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopBatchTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopCreatingImage(self, request):
        """停止保存镜像

        :param request: Request instance for StopCreatingImage.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopCreatingImageRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopCreatingImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopCreatingImage", params, headers=headers)
            response = json.loads(body)
            model = models.StopCreatingImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopFlow(self, request):
        """停止工作流

        :param request: Request instance for StopFlow.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopFlowRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopFlowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopFlow", params, headers=headers)
            response = json.loads(body)
            model = models.StopFlowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopFlowRun(self, request):
        """停止工作流（通过执行ID）

        :param request: Request instance for StopFlowRun.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopFlowRunRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopFlowRunResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopFlowRun", params, headers=headers)
            response = json.loads(body)
            model = models.StopFlowRunResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopFlowRunNode(self, request):
        """停止工作流的节点

        :param request: Request instance for StopFlowRunNode.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopFlowRunNodeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopFlowRunNodeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopFlowRunNode", params, headers=headers)
            response = json.loads(body)
            model = models.StopFlowRunNodeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopLightEvalService(self, request):
        """停止 Checkpoint 对应的轻量体验服务

        :param request: Request instance for StopLightEvalService.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopLightEvalServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopLightEvalServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopLightEvalService", params, headers=headers)
            response = json.loads(body)
            model = models.StopLightEvalServiceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopModelAccelerateTask(self, request):
        """停止模型加速任务

        :param request: Request instance for StopModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopModelAccelerateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopNotebook(self, request):
        """停止Notebook

        :param request: Request instance for StopNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopNotebook", params, headers=headers)
            response = json.loads(body)
            model = models.StopNotebookResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopObjectiveEvaluation(self, request):
        """停止客观评测接口

        :param request: Request instance for StopObjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopObjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopObjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopObjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.StopObjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopSubjectiveEvaluation(self, request):
        """停止主观评测接口

        :param request: Request instance for StopSubjectiveEvaluation.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopSubjectiveEvaluationRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopSubjectiveEvaluationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopSubjectiveEvaluation", params, headers=headers)
            response = json.loads(body)
            model = models.StopSubjectiveEvaluationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopTaskComparison(self, request):
        """停止对比评测任务

        :param request: Request instance for StopTaskComparison.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopTaskComparisonRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopTaskComparisonResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopTaskComparison", params, headers=headers)
            response = json.loads(body)
            model = models.StopTaskComparisonResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def StopTrainingTask(self, request):
        """停止模型训练任务

        :param request: Request instance for StopTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopTrainingTask", params, headers=headers)
            response = json.loads(body)
            model = models.StopTrainingTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SubmitEvaluationScore(self, request):
        """对在线服务的回复进行打分

        :param request: Request instance for SubmitEvaluationScore.
        :type request: :class:`tencentcloud.tione.v20211111.models.SubmitEvaluationScoreRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SubmitEvaluationScoreResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SubmitEvaluationScore", params, headers=headers)
            response = json.loads(body)
            model = models.SubmitEvaluationScoreResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def SyncDataset(self, request):
        """同步数据集

        :param request: Request instance for SyncDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.SyncDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SyncDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SyncDataset", params, headers=headers)
            response = json.loads(body)
            model = models.SyncDatasetResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def TransferResourceInstancesToResourceGroup(self, request):
        """移动节点至其他资源组

        :param request: Request instance for TransferResourceInstancesToResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.TransferResourceInstancesToResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.TransferResourceInstancesToResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("TransferResourceInstancesToResourceGroup", params, headers=headers)
            response = json.loads(body)
            model = models.TransferResourceInstancesToResourceGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateAlgoVersion(self, request):
        """更新个人算法版本接口

        :param request: Request instance for UpdateAlgoVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateAlgoVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateAlgoVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateAlgoVersion", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateAlgoVersionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateAutoMLCLSLogConfig(self, request):
        """更新训练任务CLS日志投递

        :param request: Request instance for UpdateAutoMLCLSLogConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLCLSLogConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLCLSLogConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateAutoMLCLSLogConfig", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateAutoMLCLSLogConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateAutoMLTaskConfigReq(self, request):
        """更新自动学习任务配置

        :param request: Request instance for UpdateAutoMLTaskConfigReq.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLTaskConfigReqRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLTaskConfigReqResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateAutoMLTaskConfigReq", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateAutoMLTaskConfigReqResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateDataSourceStatus(self, request):
        """用于验证数据源有效性后修改数据源状态

        :param request: Request instance for UpdateDataSourceStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateDataSourceStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateDataSourceStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateDataSourceStatus", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateDataSourceStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateModel(self, request):
        """编辑模型标签

        :param request: Request instance for UpdateModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateModel", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateModelResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateNotebookInfo(self, request):
        """更新Notebook实例运行信息

        :param request: Request instance for UpdateNotebookInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateNotebookInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateNotebookInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateNotebookInfo", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateNotebookInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateTensorBoardTask(self, request):
        """更新TensorBoard任务

        :param request: Request instance for UpdateTensorBoardTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateTensorBoardTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateTensorBoardTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateTensorBoardTask", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateTensorBoardTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UpdateTrainingTaskPlugin(self, request):
        """更新训练任务插件

        :param request: Request instance for UpdateTrainingTaskPlugin.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateTrainingTaskPluginRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateTrainingTaskPluginResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateTrainingTaskPlugin", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateTrainingTaskPluginResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def UploadData(self, request):
        """上传数据

        :param request: Request instance for UploadData.
        :type request: :class:`tencentcloud.tione.v20211111.models.UploadDataRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UploadDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UploadData", params, headers=headers)
            response = json.loads(body)
            model = models.UploadDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))