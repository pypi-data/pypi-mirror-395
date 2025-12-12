# -*- coding: utf-8 -*-

import base64
import datetime
import json
import os
import time
import types
from typing import List

from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_threadpool import SimpleThreadPool

from tikit import models as TiModels
from tikit.kitlog import kitlog
from tikit.tencentcloud.cfs.v20190719 import cfs_client
from tikit.tencentcloud.cfs.v20190719 import models as cfs_models
from tikit.tencentcloud.common import credential
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tikit.tencentcloud.common.profile.client_profile import ClientProfile
from tikit.tencentcloud.common.profile.http_profile import HttpProfile
from tikit.tencentcloud.tione.v20211111 import models, tione_client

from .util import parse_cos_str

SCHEMA_INFO_VALUE_TYPES = ["TYPE_INT", "TYPE_STRING", "TYPE_BOOL", "TYPE_FLOAT"]
ANNOTATION_TYPES = [
    "ANNOTATION_TYPE_CLASSIFICATION",
    "ANNOTATION_TYPE_DETECTION",
    "ANNOTATION_TYPE_SEGMENTATION",
    "ANNOTATION_TYPE_TRACKING",
    "ANNOTATION_TYPE_OCR",
]
ANNOTATION_FORMATS = [
    "ANNOTATION_FORMAT_TI",
    "ANNOTATION_FORMAT_PASCAL",
    "ANNOTATION_FORMAT_COCO",
    "ANNOTATION_FORMAT_FILE",
]
ALL_SUPPORT_TRAINING_MODES = ["PS_WORKER", "DDP", "MPI", "HOROVOD", "SPARK", "RAY"]
REGION_DICT = {"ap-guangzhou": 1, "ap-shanghai": 4, "ap-beijing": 8, "ap-nanjing": 33}

MAX_CHUNK_SIZE = 190


class Client(object):
    # 临时秘钥使用，提前获取临时秘钥，避免访问的时候失败
    _secret_ahead_time = 60 * 5

    def __init__(
        self,
        secret_id=None,
        secret_key=None,
        region=None,
        token=None,
        proxies=None,
        tione_endpoint=None,
        protocol=None,
    ):
        """初始化，保存用户的信息

        :param secret_id:   秘钥SecretId
        :type secret_id:    str
        :param secret_key:  秘钥SecretKey
        :type secret_key:   str
        :param region:      地域信息
        :type region:       str
        :param token:       临时秘钥使用的token
        :type token:        str
        :param proxies:     使用代理来访问，内容如：{"https": "127.0.0.1:443"}.
        :type proxies:      dict
        :param tione_endpoint: 网关地址，默认tione.internal.tencentcloudapi.com
        :type tione_endpoint: str
        :param protocol:    协议，默认https
        :type protocol:     str
        """
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._region = region if region is not None else os.getenv("REGION")
        self._token = token
        self._proxies = proxies
        self._platform_public_key_info = None

        self._cos_client = None
        self._tione_client = None
        self._kit_log = None
        self._expired_time = 0

        self._protocol = (
            protocol
            if protocol is not None
            else os.getenv("TCE_API_SCHEMA", "http")  # 如果环境变量不存在则默认 "http"
        )
        # 处理 tione_endpoint 逻辑
        if tione_endpoint is not None:
            self._tione_endpoint = tione_endpoint
        else:
            api_root_domain = os.getenv("TCE_API_ROOT_DOMAIN")
            if not api_root_domain:
                raise ValueError(
                    "必须提供 tione_endpoint 或设置 TCE_API_ROOT_DOMAIN 环境变量"
                )
            self._tione_endpoint = f"tione.{api_root_domain}"

        if secret_id is not None:
            self._init_client()

    def _init_client(self):
        config = CosConfig(
            Region=self._region,
            SecretId=self._secret_id,
            SecretKey=self._secret_key,
            Token=self._token,
            Proxies=self._proxies,
        )
        self._cos_client = CosS3Client(config)

        cred = credential.Credential(self._secret_id, self._secret_key, self._token)
        proxy = None if self._proxies is None else self._proxies.get("https", None)
        http_profile = HttpProfile(
            protocol=self._protocol, endpoint=self._tione_endpoint, proxy=proxy, keepAlive=True
        )
        client_profile = ClientProfile(httpProfile=http_profile)
        self._tione_client = tione_client.TioneClient(
            cred, self._region, client_profile
        )
        self._kit_log = kitlog.KitLog(self._tione_client)

    def _update_secret(self):
        # self._region = os.getenv("REGION")
        # # TODO 从环境变量的认证URL中获取临时认证信息
        # self._secret_id = os.getenv("SECRET_ID")
        # self._secret_key = os.getenv("SECRET_KEY")
        # self._token =
        # self._expired_time =
        raise Exception("auto authentication is not supported")

    def _init_public_key(self):
        # 初始化公钥id  用作加密保存镜像密钥
        try:
            req = models.DescribePublicKeyRequest()
            req.EncryptAlgorithm = "RSA_2048"
            rsp = self._tione_client.DescribePublicKey(req)
            if rsp is not None:
                self._platform_public_key_info = rsp
        except Exception as e:
            raise TencentCloudSDKException(message=str(e))

    def guarantee_valid(self):
        if self._expired_time - self._secret_ahead_time < int(time.time()):
            self._update_secret()
            self._init_client()

    def describe_cos_buckets(self):
        """列出所有bucket

        :return:    bucket列表
        :rtype:     dict
        返回的结果如：
        {
          "Owner": {
            "ID": "qcs::cam::uin/100011011262:uin/100011011262",
            "DisplayName": "100011011162"
          },
          "Buckets": {
            "Bucket": [
              {
                "Name": "bucket-58565",
                "Location": "ap-beijing-fsi",
                "CreationDate": "2021-07-21T11:06:00Z",
                "BucketType": "cos"
              },
              {
                "Name": "tai-1300158565",
                "Location": "ap-guangzhou",
                "CreationDate": "2021-10-22T11:04:40Z",
                "BucketType": "cos"
              }
            ]
          }
        }
        """
        return self._cos_client.list_buckets()

    def is_cos_dir(self, bucket, path):
        """判断目录是否为文件夹

        :param bucket:
        :type bucket:
        :param path:
        :type path:
        :return:
        :rtype:
        """
        objects = self._cos_client.list_objects(
            Bucket=bucket, Prefix=path.strip("/") + "/", MaxKeys=1
        )
        if "Contents" in objects and len(objects["Contents"]) > 0:
            return True
        return False

    def check_object_exist(self, bucket, cos_path):
        """判断某个object是否存在
        如果是判断某个目录存在，需要保证cos_path 以 / 结尾
        如果是判断某个文件存在，需要保证cos_path 不以 / 结尾

        :param bucket:      cos上的桶
        :param cos_path:    cos上的路径key
        :return:            指定对象是否存在
        :rtype:             bool, 错误信息通过 raise 给出
        """
        rsp = self._cos_client.object_exists(bucket, cos_path)
        return rsp

    def mkdir(self, bucket, cos_path):
        """cos上创建目录
        注: 对象存储本身是没有目录概念, 为了保证用户的使用习惯, 此处创建一个以cos_path为指定key, key以 / 结尾的0kb大小的对象

        :param bucket:      cos上的桶
        :param cos_path:    cos上的路径key
        :return:            None, 错误信息通过 raise 给出
        """
        cos_path = str(cos_path)
        if not cos_path.endswith("/"):
            cos_path = os.path.dirname(cos_path)
            cos_path = cos_path + "/"

        if cos_path == "/":
            return

        self._cos_client.put_object(Bucket=bucket, Key=cos_path, Body=b"")

    def upload_to_cos(self, local_path, bucket, cos_path):
        """把本地路径下的文件或者目录上传到cos上

        :param local_path:  本地路径
        :type local_path:   str
        :param bucket:      cos上的桶
        :type bucket:       str
        :param cos_path:    cos上的路径
        :type cos_path:     str
        :return:            None. 错误信息通过 raise 给出。
        :rtype:
        """
        if not os.path.exists(local_path):
            raise Exception("local path is not exist, please check it.")

        local_path = os.path.abspath(local_path)

        if cos_path == "":
            cos_path = "/"

        self.mkdir(bucket, cos_path)

        if os.path.isfile(local_path):
            if cos_path.endswith("/"):
                cos_path = os.path.join(cos_path, os.path.basename(local_path))
            self._cos_client.upload_file(
                Bucket=bucket, LocalFilePath=local_path, Key=cos_path, EnableMD5=True
            )
            return

        if not os.path.isdir(local_path):
            raise Exception("invalid local path type", local_path)

        if not local_path.endswith("/"):
            # src不带 /, 代表上传源目录
            if cos_path.endswith("/"):
                # dst 带 /, 代表上传到dst的目录下
                cos_path = os.path.join(cos_path, os.path.basename(local_path))
        else:
            # src 带 /, 代表上传源目录下的文件
            if not cos_path.endswith("/"):
                cos_path = cos_path + "/"

        pool = SimpleThreadPool()
        walker = os.walk(local_path)
        for path, dir_list, file_list in walker:
            pre_path = os.path.join(cos_path, path[len(local_path) :].strip("/"))
            for file_name in file_list:
                src_key = os.path.join(path, file_name)
                cos_object_key = os.path.join(pre_path, file_name).strip("/")
                # 假如存在错误的软链时, 或者其他意外情况导致的文件不存在时, 跳过
                if not os.path.exists(src_key):
                    print(src_key, "does not exist, ignore it")
                    continue
                pool.add_task(
                    self._cos_client.upload_file, bucket, cos_object_key, src_key
                )

        pool.wait_completion()
        result = pool.get_result()
        if not result["success_all"]:
            self.__dump_error_result(result)
            raise Exception("failed to upload files to cos, please retry")
        return

    def describe_cos_path(
        self, bucket, path, maker="", max_keys=1000, encoding_type=""
    ):
        """获取cos的目录的信息。目录下的内容最多显示1000个。要显示目录下的文件和文件夹，请以"/"结尾

        :param bucket:          cos的桶
        :type bucket:           str
        :param path:            路径
        :type path:             str
        :return:                目录信息
        :rtype:                 dict
        :param maker:           从marker开始列出条目
        :type maker:            str
        :param max_keys:        设置单次返回最大的数量,最大为1000.
        :type max_keys:         int
        :param encoding_type:   设置返回结果编码方式,只能设置为url.
        :type encoding_type:    str
        """
        return self._cos_client.list_objects(
            Bucket=bucket,
            Prefix=path,
            Delimiter="/",
            Marker=maker,
            MaxKeys=max_keys,
            EncodingType=encoding_type,
        )

    def delete_cos_files(self, bucket, file_infos):
        """删除cos的一个或者多个文件

        :param bucket:
        :type bucket:
        :param file_infos:
        :type file_infos:
        :return:
        :rtype:
        """
        delete_list = []
        for file in file_infos:
            delete_list.append({"Key": file["Key"]})

        response = self._cos_client.delete_objects(
            Bucket=bucket, Delete={"Object": delete_list}
        )
        print(response)

    def delete_cos_path(self, bucket, delete_path):
        """删除cos目录。要删除目录下的文件和文件夹，请以"/"结尾，即：不带斜杠的，当成文件来删除；带斜杠的，当成文件夹来删除

        :param bucket:      cos的桶
        :type bucket:       str
        :param delete_path: 要删除的路径
        :type delete_path:  str
        """
        if not delete_path.endswith("/"):
            return self._cos_client.delete_object(
                Bucket=bucket,
                Key=delete_path,
            )
            return

        pool = SimpleThreadPool()
        marker = ""
        while True:
            file_infos = []
            response = self._cos_client.list_objects(
                Bucket=bucket, Prefix=delete_path, Marker=marker, MaxKeys=100
            )
            if "Contents" in response:
                contents = response.get("Contents")
                file_infos.extend(contents)
                pool.add_task(self.delete_cos_files, bucket, file_infos)
            # 列举完成，退出
            if response["IsTruncated"] == "false":
                break

            # 列举下一页
            marker = response["NextMarker"]

        pool.wait_completion()
        result = pool.get_result()
        if not result["success_all"]:
            raise Exception("failed to delete files, please retry")

    def __dump_error_result(self, result):
        """
        私有方法, 用来dump出cos的SimpleThreadPool运行过程中的错误信息
        """
        if "detail" not in result:
            return

        detail = result["detail"]
        for tp in detail:
            if tp[1] != 0:
                # 当failed的任务个数不为0时，打印第三个返回值, 即错误信息
                print(tp[2])

    def download_from_cos(self, bucket, cos_path, local_path):
        """从cos上下载文件或者目录本地。
        注意：本地文件存在会直接覆盖。 cos_path为目录且local_path 为存在的目录的时候，cos_path的文件夹名会作为子目录保留。

        :param bucket:      cos上的桶
        :type bucket:       str
        :param cos_path:    cos上的路径
        :type cos_path:     str
        :param local_path:  本地路径, 需要为目录
        :type local_path:   str
        :return:            None. 错误信息通过 raise 给出。
        :rtype:
        """
        file_infos = self.get_cos_sub_files(bucket, cos_path)
        if len(file_infos) == 0:
            raise Exception('cos path "%s" not existed' % cos_path)
        if os.path.isfile(local_path):
            raise Exception(
                'local_path parameter "%s" should be directory' % local_path
            )

        # 下载目录时，如果不存在则创建
        os.makedirs(local_path, exist_ok=True)
        target_path = local_path
        # local_path 为存在的目录的时候
        if os.path.isdir(local_path):
            target_path = os.path.join(target_path, os.path.basename(cos_path))
        cos_path_length = len(cos_path)
        pool = SimpleThreadPool()
        for file in file_infos:
            # 文件下载 获取文件到本地
            file_cos_key = file["Key"]
            local_name = os.path.join(
                target_path, file_cos_key[cos_path_length:].strip("/")
            ).strip("/")

            # 如果存在目录类型的object, 则直接跳过不做下载操作
            file_cos_key = str(file_cos_key)
            if file_cos_key.endswith("/") and int(file["Size"]) == 0:
                continue

            # 如果本地目录结构不存在，递归创建
            local_dir = os.path.dirname(local_name)
            if local_dir != "" and not os.path.exists(local_dir):
                os.makedirs(local_dir)

            # 使用线程池方式
            if self.__need_download_from_cos(bucket, file_cos_key, local_name):
                pool.add_task(
                    self._cos_client.download_file, bucket, file_cos_key, local_name
                )

        pool.wait_completion()
        result = pool.get_result()
        print(result)
        if not result["success_all"]:
            self.__dump_error_result(result)
            raise Exception("failed to download files, please retry")

    def get_cos_sub_files(self, bucket, prefix):
        """列出当前目录子节点，返回所有子节点信息

        :param bucket:
        :type bucket:
        :param prefix:
        :type prefix:
        :return:
        :rtype:
        """
        file_infos = []
        marker = ""
        while True:
            response = self._cos_client.list_objects(bucket, prefix, "", marker)
            if "Contents" in response:
                contents = response.get("Contents")
                file_infos.extend(contents)

            if "NextMarker" in response.keys():
                marker = response["NextMarker"]
            else:
                break

        sorted(file_infos, key=lambda file_info: file_info["Key"])
        # for file in file_infos:
        #     print(file)
        return file_infos

    def __need_download_from_cos(self, bucket, key, local_path):
        """判断当前文件是否需要下载

        :param bucket:              cos bucket
        :type bucket:               str
        :param key:                 cos file key
        :type key:                  str
        :param local_file_path:     local file path
        :type local_file_path:      str
        :return:                    是否需要下载当前文件
        :rtype:                     bool
        """
        # 如果最后有'/'，则移除
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            # 本地不存在，则需要从cos上下载
            return True

        local_file_size = os.path.getsize(local_path)
        try:
            response = self._cos_client.head_object(Bucket=bucket, Key=key)
            if "Content-Length" not in response:
                # 异常情况, 重新下载
                print("Content-Length field is not exist, cos file key:", key)
                return True

            # 根据文件大小是否相同决定是否下载
            return int(response["Content-Length"]) != int(local_file_size)
        except TencentCloudSDKException as err:
            raise

    def describe_train_resource_groups(
        self, offset=0, limit=20, search_word="", tag_filters=None
    ):
        """获取训练资源组列表

        @deprecated 1.6.8版本开始资源组不再区分训练、推理类型，请使用`describe_resource_groups`进行查询。

        :param offset: 偏移量，默认为0；分页查询起始位置，如：Limit为100，第一页Offset为0，第二页OffSet为100....即每页左边为开区间
        :type offset: int
        :param limit: 返回数量，默认为20，最大值为30；分页查询每页大小，最大30
        :type limit: int
        :param search_word: 支持模糊查找资源组id和资源组名
        :type search_word: str
        :param tag_filters: 标签过滤
        :type tag_filters: list of tikit.tencentcloud.tione.v20211111.models.TagFilter
        :return:
        :rtype:    :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`

        .. deprecated:: 1.6.8

        """
        try:
            req = models.DescribeBillingResourceGroupsRequest()
            req.Type = "TRAIN"
            req.Offset = offset
            req.Limit = limit
            req.SearchWord = search_word
            req.TagFilters = tag_filters
            return self._tione_client.DescribeBillingResourceGroups(req)
        except TencentCloudSDKException as err:
            raise

    def describe_inference_resource_groups(
        self, offset=0, limit=20, search_word="", tag_filters=None
    ):
        """获取推理训练组列表

        @deprecated 1.6.8版本开始资源组不再区分训练、推理类型，请使用`describe_resource_groups`进行查询。

        :param offset: 偏移量，默认为0；分页查询起始位置，如：Limit为100，第一页Offset为0，第二页OffSet为100....即每页左边为开区间
        :type offset: int
        :param limit: 返回数量，默认为20，最大值为30；分页查询每页大小，最大30
        :type limit: int
        :param search_word: 支持模糊查找资源组id和资源组名
        :type search_word: str
        :param tag_filters: 标签过滤
        :type tag_filters: list of tikit.tencentcloud.tione.v20211111.models.TagFilter
        :return:
        :rtype:    :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`

        .. deprecated:: 1.6.8
        """
        try:
            req = models.DescribeBillingResourceGroupsRequest()
            req.Type = "INFERENCE"
            req.Offset = offset
            req.Limit = limit
            req.SearchWord = search_word
            req.TagFilters = tag_filters
            return self._tione_client.DescribeBillingResourceGroups(req)
        except TencentCloudSDKException as err:
            raise

    def describe_resource_groups(
        self, offset=0, limit=20, search_word="", tag_filters=None
    ):
        """获取资源组列表

        :param offset: 偏移量，默认为0；分页查询起始位置，如：Limit为100，第一页Offset为0，第二页OffSet为100....即每页左边为开区间
        :type offset: int
        :param limit: 返回数量，默认为20，最大值为30；分页查询每页大小，最大30
        :type limit: int
        :param search_word: 支持模糊查找资源组id和资源组名
        :type search_word: str
        :param tag_filters: 标签过滤
        :type tag_filters: list of tikit.tencentcloud.tione.v20211111.models.TagFilter
        :return:
        :rtype:    :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`
        """
        try:
            req = models.DescribeBillingResourceGroupsRequest()
            req.Offset = offset
            req.Limit = limit
            req.SearchWord = search_word
            req.TagFilters = tag_filters
            return self._tione_client.DescribeBillingResourceGroups(req)
        except TencentCloudSDKException as err:
            raise

    def describe_postpaid_training_price(self):
        """查询每种配置的每小时的价格，价格单位：元

        :rtype:     tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse
        """
        try:
            req = models.DescribeBillingSpecsRequest()
            req.TaskType = "TRAIN"
            req.ChargeType = "POSTPAID_BY_HOUR"
            specs = self._tione_client.DescribeBillingSpecs(req)

            price_req = models.DescribeBillingSpecsPriceRequest()
            price_req.SpecsParam = []
            for spec in specs.Specs:
                price_req.SpecsParam.append({"SpecName": spec.SpecName, "SpecCount": 1})
            price_result = self._tione_client.DescribeBillingSpecsPrice(price_req)
            for i in range(len(price_result.SpecsPrice)):
                specs.Specs[i].SpecId = str(
                    price_result.SpecsPrice[i].RealTotalCost / 100.0
                )
            return specs
        except TencentCloudSDKException as err:
            raise

    def describe_postpaid_reasoning_price(self):
        """查询每种配置的每小时的价格，价格单位：元

        :rtype:     tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse
        """
        try:
            req = models.DescribeBillingSpecsRequest()
            req.TaskType = "INFERENCE"
            req.ChargeType = "POSTPAID_BY_HOUR"
            specs = self._tione_client.DescribeBillingSpecs(req)

            price_req = models.DescribeBillingSpecsPriceRequest()
            price_req.SpecsParam = []
            for spec in specs.Specs:
                price_req.SpecsParam.append({"SpecName": spec.SpecName, "SpecCount": 1})
            price_result = self._tione_client.DescribeBillingSpecsPrice(price_req)
            for i in range(len(price_result.SpecsPrice)):
                specs.Specs[i].SpecId = str(
                    price_result.SpecsPrice[i].RealTotalCost / 100.0
                )
            return specs
        except TencentCloudSDKException as err:
            raise

    def describe_training_tasks(
        self,
        filters=None,
        tag_filters=None,
        offset=0,
        limit=50,
        order="DESC",
        order_field="UpdateTime",
    ):
        """获取训练任务列表

        :param filters:     过滤器，eg：[{ "Name": "TaskStatus", "Values": ["Running"] }]
        :type filters:      list of Filter
        :param tag_filters: 标签过滤器，eg：[{ "TagKey": "TagKeyA", "TagValue": ["TagValueA"] }]
        :type tag_filters:  list of TagFilter
        :param offset:      偏移量，默认为0
        :type offset:       int
        :param limit:       返回数量，默认为50
        :type limit:        int
        :param order:       输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列
        :type order:        str
        :param order_field: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type order_field:  str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`
        """
        try:
            # 优化参数的显示
            req = models.DescribeTrainingTasksRequest()
            req.Filters = filters
            req.TagFilters = tag_filters
            req.Offset = offset
            req.Limit = limit
            req.Order = order
            req.OrderField = order_field
            return self._tione_client.DescribeTrainingTasks(req)
        except TencentCloudSDKException as err:
            raise

    def describe_training_task(self, task_id):
        """获取单个训练任务信息

        :param task_id: 训练任务ID
        :type task_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskResponse`
        """
        try:
            # 优化参数的显示
            req = models.DescribeTrainingTaskRequest()
            req.Id = task_id
            # TODO 优化显示结果
            return self._tione_client.DescribeTrainingTask(req)
        except TencentCloudSDKException as err:
            raise

    def parse_cos_info(self, cos_str):
        """解析cos 字符串成结构体

        :param cos_str: 格式如： <bucket>/<cos path>
        :type cos_str: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        cos_info = parse_cos_str(cos_str)
        cos_info.Region = self._region
        return cos_info

    def create_training_task(
        self,
        name="",
        framework=None,
        cos_output=None,
        worker_resource=None,
        code_package_path=None,
        code_repos=None,
        ps_resource=None,
        head_resource=None,
        worker_resource_group=None,
        input_data_config=None,
        worker_start_cmd=None,
        ps_start_cmd=None,
        tags=None,
        tuning_parameters_dict={},
        resource_group_id="",
        remark=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        vpc_id=None,
        sub_net_id=None,
        enable_rdma=False,
        restart_limit=0,
    ):
        """创建训练任务

        :param name:        任务名称
        :type name:         str
        :param framework:   运行的框架环境
        :type framework:    :class:`tikit.models.FrameworkInfo`
        :param cos_output:          输出的cos信息
        :type cos_output:           str
        :param worker_resource:     worker节点的配置
        :type worker_resource:      :class:`tikit.models.ResourceConfigInfo`
        :param code_package_path:   代码的cos信息
        :type code_package_path:    str
        :parm code_repos:           git repo list
        :type code_repos:           list of :class:`tikit.tencentcloud.tione.v20211111.models.CodeRepoConfig`
        :param ps_resource:         ps节点的配置
        :type ps_resource:          :class:`tikit.models.ResourceConfigInfo`
        :param head_resource:       head节点的配置
        :type head_resource:        :class:`tikit.models.ResourceConfigInfo`
        :param worker_resource_group: worker节点的配置列表
        :type worker_resource_group:  list of :class:`tikit.models.ResourceConfigInfo`
        :param input_data_config:   输入的数据信息
        :type input_data_config:    list of :class:`tikit.models.TrainingDataConfig`
        :param worker_start_cmd:    worker的启动命令
        :type worker_start_cmd:     str
        :param ps_start_cmd:        ps节点的启动命令
        :type ps_start_cmd:         str
        :param tags:                标签
        :type tags:                 list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :param tuning_parameters_dict:  调参字典
        :type tuning_parameters_dict:   dict
        :param resource_group_id:   预付费的资源组id
        :type resource_group_id:    str
        :param remark:              描述
        :type remark:               str
        :param log_enable:          日志开关
        :type log_enable:           bool
        :param log_logset_id:       日志集id
        :type log_logset_id:        str
        :param log_topic_id:        日志的topic id
        :type log_topic_id:         str
        :param vpc_id:              vpc的id
        :type vpc_id:               str
        :param sub_net_id:          子网id
        :type sub_net_id:           str
        :param enable_rdma:         是否使用 RMDA 网卡，只有机型支持该参数才可生效
        :type enable_rdma:          bool
        :param restart_limit:       当前任务最大重启次数，最高10次，超过后任务被标记为异常
        :type restart_limit:          int
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`
        """
        try:
            if name == "":
                raise TencentCloudSDKException(message="task name cannot be empty")
            if framework is None:
                raise TencentCloudSDKException(
                    message="missing parameter {}".format("framework")
                )
            if worker_resource is None and worker_resource_group is None:
                raise TencentCloudSDKException(
                    message="missing parameter {}".format("worker_resource")
                )
            if worker_start_cmd is None and ps_start_cmd is None:
                raise TencentCloudSDKException(
                    message="missing parameter {}".format("worker_start_cmd")
                )

            if worker_resource is None and len(worker_resource_group) > 0:
                worker_resource = worker_resource_group[0]

            req = models.CreateTrainingTaskRequest()
            req.Name = name
            req.TrainingMode = framework.TrainingMode
            if not framework:
                raise TencentCloudSDKException(message="framework cannot be empty")
            if framework.Name == "CUSTOM":
                req.ImageInfo = models.ImageInfo()
                req.ImageInfo.ImageType = framework.ImageType
                req.ImageInfo.ImageUrl = framework.ImageUrl
                req.ImageInfo.RegistryRegion = framework.RegistryRegion
                req.ImageInfo.RegistryId = framework.RegistryId
                if framework.UserName is not None and framework.Passwd is not None:
                    passwdEncrypted = self._encrypt(framework.Passwd)
                    req.ImageInfo.ImageSecret = models.ImageSecret()
                    req.ImageInfo.ImageSecret.Username = framework.UserName
                    req.ImageInfo.ImageSecret.Password = passwdEncrypted
                    req.ImageInfo.ImageSecret.KeyId = (
                        self._platform_public_key_info.KeyId
                    )
            else:
                req.FrameworkName = framework.Name
                req.FrameworkEnvironment = framework.FrameworkEnvironment
            if req.TrainingMode not in ALL_SUPPORT_TRAINING_MODES:
                raise TencentCloudSDKException(
                    message="only support these training modes {}".format(
                        ALL_SUPPORT_TRAINING_MODES
                    )
                )

            if req.TrainingMode == "PS_WORKER":
                if not ps_resource:
                    raise TencentCloudSDKException(
                        message='PS_WORKER training mode, need the argument "ps_resource"'
                    )
                if worker_resource.ChargeType != ps_resource.ChargeType:
                    raise TencentCloudSDKException(
                        message="worker_resource charge type should be same with ps_resource"
                    )
            elif ps_resource:
                raise TencentCloudSDKException(
                    message='only PS_WORKER training mode,need the argument "ps_resource"'
                )

            req.ChargeType = worker_resource.ChargeType
            req.ResourceGroupId = resource_group_id
            if req.TrainingMode == "SPARK":
                if worker_resource.InstanceNum != 1:
                    raise TencentCloudSDKException(
                        message="SPARK task only support one instance"
                    )
                driver_info = models.ResourceConfigInfo()
                driver_info.Role = "DRIVER"
                driver_info.Cpu = worker_resource.Cpu
                driver_info.Memory = worker_resource.Memory
                driver_info.InstanceType = worker_resource.InstanceType
                driver_info.InstanceNum = worker_resource.InstanceNum
                executor_info = models.ResourceConfigInfo()
                executor_info.Role = "EXECUTOR"
                executor_info.Cpu = worker_resource.Cpu
                executor_info.Memory = worker_resource.Memory
                executor_info.InstanceType = worker_resource.InstanceType
                executor_info.InstanceNum = worker_resource.InstanceNum
                req.ResourceConfigInfos = [driver_info, executor_info]
            elif req.TrainingMode == "RAY":
                if head_resource.InstanceNum != 1:
                    raise TencentCloudSDKException(
                        message="RAY task head only support one instance"
                    )
                head_info = models.ResourceConfigInfo()
                head_info.Role = "HEAD"
                head_info.Cpu = head_resource.Cpu
                head_info.Gpu = head_resource.Gpu
                head_info.GpuType = head_resource.GpuType
                head_info.Memory = head_resource.Memory
                head_info.InstanceType = head_resource.InstanceType
                head_info.InstanceNum = head_resource.InstanceNum
                req.ResourceConfigInfos = [head_info]
                for worker_resource in worker_resource_group:
                    worker_info = models.ResourceConfigInfo()
                    worker_info.Role = "WORKER"
                    worker_info.InstanceNum = worker_resource.InstanceNum
                    worker_info.Cpu = worker_resource.Cpu
                    worker_info.Memory = worker_resource.Memory
                    worker_info.GpuType = worker_resource.GpuType
                    worker_info.Gpu = worker_resource.Gpu
                    worker_info.InstanceType = worker_resource.InstanceType
                    req.ResourceConfigInfos.append(worker_info)
            else:
                worker_info = models.ResourceConfigInfo()
                worker_info.Role = "WORKER"
                worker_info.InstanceNum = worker_resource.InstanceNum
                worker_info.Cpu = worker_resource.Cpu
                worker_info.Memory = worker_resource.Memory
                worker_info.GpuType = worker_resource.GpuType
                worker_info.Gpu = worker_resource.Gpu
                worker_info.InstanceType = worker_resource.InstanceType
                if enable_rdma:
                    rdma_config = models.RDMAConfig()
                    rdma_config.Enable = enable_rdma
                    worker_info.RDMAConfig = rdma_config
                req.ResourceConfigInfos = [worker_info]

                if ps_resource:
                    ps_info = models.ResourceConfigInfo()
                    ps_info.Role = "PS"
                    ps_info.InstanceNum = ps_resource.InstanceNum
                    ps_info.Cpu = ps_resource.Cpu
                    ps_info.Memory = ps_resource.Memory
                    ps_info.GpuType = ps_resource.GpuType
                    ps_info.Gpu = ps_resource.Gpu
                    ps_info.InstanceType = ps_resource.InstanceType
                    if enable_rdma:
                        rdma_config = models.RDMAConfig()
                        rdma_config.Enable = enable_rdma
                        ps_info.RDMAConfig = rdma_config
                    req.ResourceConfigInfos.append(ps_info)

            req.Output = self.parse_cos_info(cos_output) if cos_output else None
            req.Tags = tags
            req.CodePackagePath = (
                self.parse_cos_info(code_package_path) if code_package_path else None
            )
            req.CodeRepos = code_repos if code_repos else None

            start_cmd_info = models.StartCmdInfo()
            if req.TrainingMode == "SPARK":
                start_cmd_info.StartCmd = worker_start_cmd
            else:
                start_cmd_info.WorkerStartCmd = worker_start_cmd
                start_cmd_info.PsStartCmd = ps_start_cmd
            req.EncodedStartCmdInfo = models.EncodedStartCmdInfo()
            req.EncodedStartCmdInfo.StartCmdInfo = base64.b64encode(
                start_cmd_info.to_json_string().encode("utf-8")
            ).decode("ascii")

            if input_data_config is not None:
                req.DataConfigs, req.DataSource = self._parse_training_task_input_data(
                    input_data_config
                )

            req.TuningParameters = json.dumps(tuning_parameters_dict)
            req.Remark = remark
            req.LogEnable = log_enable
            if log_enable:
                req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = log_logset_id
                req.LogConfig.TopicId = log_topic_id

            req.VpcId = vpc_id
            req.SubnetId = sub_net_id
            if restart_limit != 0:
                if restart_limit > 10:
                    raise TencentCloudSDKException(
                        message="restart_limit should be less than 10"
                    )
                req.SchedulePolicy = models.SchedulePolicy()
                req.SchedulePolicy.BackOffLimit = restart_limit
            return self._tione_client.CreateTrainingTask(req)
        except TencentCloudSDKException as err:
            raise

    def _encrypt(self, text):
        if text is None:
            return None
        if self._platform_public_key_info is None:
            self._init_public_key()
        from .encrypt import rsa_encrypt

        byte_text = text.encode("utf-8")
        if len(byte_text) <= MAX_CHUNK_SIZE:
            return rsa_encrypt(
                self._platform_public_key_info.PublicKeyPem, byte_text
            ).decode("utf-8")
        encrypted_results = []
        start_index = 0
        while start_index < len(byte_text):
            end_index = start_index + MAX_CHUNK_SIZE
            if end_index > len(byte_text):
                end_index = len(byte_text)
            chunk = byte_text[start_index:end_index]
            encrypted_chunk = rsa_encrypt(
                self._platform_public_key_info.PublicKeyPem, chunk
            )
            if encrypted_chunk:
                encrypted_results.append(encrypted_chunk.decode("utf-8"))
            else:
                raise TencentCloudSDKException(
                    message="rsa encrypt error, encrypted_chunk is None"
                )
            start_index = end_index
        return ",".join(encrypted_results)

    def _convert_data_config_old(self, input_data_item) -> List[models.DataConfig]:
        # 兼容旧版本的处理
        result = []
        for key in input_data_item.DataConfigDict:
            data_config = models.DataConfig()
            data_config.DataSourceType = input_data_item.DataSource
            data_config.MappingPath = input_data_item.DataConfigDict[key]
            if input_data_item.DataSource == "COS":
                data_config.COSSource = self.parse_cos_info(key)
            elif input_data_item.DataSource == "DATASET":
                data_config.DataSetSource = models.DataSetConfig()
                data_config.DataSetSource.Id = key
            else:
                print(
                    "warning! not supported DataSourceType", input_data_item.DataSource
                )
                return []
            result.append(data_config)
        return result

    def _convert_data_config(self, input_data_item) -> models.DataConfig:
        data_config = models.DataConfig()
        data_config.DataSourceType = input_data_item.DataSource
        data_config.DataSourceUsage = input_data_item.DataSourceUsage
        data_config.MappingPath = input_data_item.TargetPath
        if input_data_item.DataSource == "COS":
            assert (
                input_data_item.CosStr
            ), 'example input: tikit.models.TrainingDataConfig.new_mount_cos("cos_str","target_path")'
            data_config.COSSource = self.parse_cos_info(input_data_item.CosStr)
        elif input_data_item.DataSource == "COSFS":
            assert (
                input_data_item.CosStr
            ), 'example input: tikit.models.TrainingDataConfig.new_mount_cos("cos_str","target_path")'
            data_config.COSSource = self.parse_cos_info(input_data_item.CosStr)
        elif input_data_item.DataSource == "DATASET":
            data_config.DataSetSource = models.DataSetConfig()
            assert (
                input_data_item.DatasetId
            ), 'example input: tikit.models.TrainingDataConfig.new_dataset_mount("dataset_id","target_path")'
            data_config.DataSetSource.Id = input_data_item.DatasetId
        elif (
            input_data_item.DataSource == "CFS"
            or input_data_item.DataSource == "CFSTurbo"
        ):
            assert input_data_item.CfsId
            data_config.CFSSource = models.CFSConfig()
            data_config.CFSSource.Id = input_data_item.CfsId
            data_config.CFSSource.Path = input_data_item.CfsPath
            data_config.DataSourceType = "CFS"
        elif input_data_item.DataSource == "HDFS":
            data_config.HDFSSource = models.HDFSConfig()
            assert input_data_item.HdfsId
            data_config.HDFSSource.Id = input_data_item.HdfsId
            data_config.HDFSSource.Path = input_data_item.HdfsPath
        elif input_data_item.DataSource == "WEDATA_HDFS":
            data_config.WeDataHDFSSource = models.WeDataHDFSConfig()
            assert input_data_item.WedataId
            data_config.WeDataHDFSSource.Id = input_data_item.WedataId
            data_config.WeDataHDFSSource.Path = input_data_item.HdfsPath
        elif input_data_item.DataSource == "AIMarket_Algo_PreModel":
            data_config.AIMarketAlgoPreModelSource = models.AIMarketAlgo()
            assert input_data_item.AIMarketAlgoId
            data_config.AIMarketAlgoPreModelSource.Id = input_data_item.AIMarketAlgoId
        elif input_data_item.DataSource == "GooseFS":
            data_config.GooseFSSource = models.GooseFS()
            assert input_data_item.GooseFSId
            assert input_data_item.GooseFSNameSpace
            data_config.GooseFSSource.Id = input_data_item.GooseFSId
            data_config.GooseFSSource.NameSpace = input_data_item.GooseFSNameSpace
            data_config.GooseFSSource.Path = input_data_item.GooseFSPath
            data_config.GooseFSSource.Type = "GooseFS"
        elif input_data_item.DataSource == "GooseFSx":
            data_config.GooseFSSource = models.GooseFS()
            assert input_data_item.GooseFSId
            data_config.GooseFSSource.Id = input_data_item.GooseFSId
            data_config.GooseFSSource.Path = input_data_item.GooseFSxPath
            data_config.GooseFSSource.Type = "GooseFSx"
        elif input_data_item.DataSource == "AIMarket_Algo_Data":
            data_config.AIMarketAlgoDataSource = models.AIMarketAlgo()
            assert input_data_item.AIMarketAlgoId
            assert input_data_item.AIMarketAlgoGroup
            data_config.AIMarketAlgoDataSource.Id = input_data_item.AIMarketAlgoId
            data_config.AIMarketAlgoDataSource.Group = input_data_item.AIMarketAlgoGroup
            data_config.AIMarketAlgoDataSource.MaterialName = "Model"
        else:
            print("warning! not supported DataSourceType", input_data_item.DataSource)
            return None
        return data_config

    def _get_storage_type(self, cfsId):
        try:
            cred = credential.Credential(self._secret_id, self._secret_key)
            client = cfs_client.CfsClient(cred, self._region)
            req = cfs_models.DescribeCfsFileSystemsRequest()
            params = {"FileSystemId": cfsId}

            req.from_json_string(json.dumps(params))
            rsp = client.DescribeCfsFileSystems(req)
            if isinstance(rsp.FileSystems, list):
                for fs in rsp.FileSystems:
                    if fs.FileSystemId == cfsId:
                        # CFS存储类型，HP：通用性能型；SD：通用标准型；TP:turbo性能型；TB：turbo标准型；THP：吞吐型
                        if fs.StorageType == "HP" or fs.StorageType == "SD":
                            return "cfs"
                        elif fs.StorageType == "TP" or fs.StorageType == "TB":
                            return "turbo"
                        else:
                            return "unknown"
            else:
                raise TencentCloudSDKException(message="get cfs storage type failed")
        except TencentCloudSDKException as err:
            raise

    def _parse_training_task_input_data(self, input_data_config):
        if not isinstance(input_data_config, list) and input_data_config.DataConfigDict:
            # 兼容旧版本的处理
            data_configs = self._convert_data_config_old(input_data_config)
            return data_configs, input_data_config.DataSource
        if not isinstance(input_data_config, list):
            input_data_config = [input_data_config]

        data_configs = []
        data_type = ""
        for input_data_item in input_data_config:
            data_config = self._convert_data_config(input_data_item)
            if not data_config:
                continue
            data_configs.append(data_config)
            data_type = input_data_item.DataSource
            if data_type == "AIMarket_Algo_PreModel":
                data_type = "COS"
        return data_configs, data_type

    def stop_training_task(self, task_id):
        """停止某个训练任务

        :param task_id: 训练任务ID
        :type task_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StopTrainingTaskResponse`
        """
        try:
            req = models.StopTrainingTaskRequest()
            req.Id = task_id
            return self._tione_client.StopTrainingTask(req)
        except TencentCloudSDKException as err:
            raise

    def describe_training_frameworks(self):
        """查看训练框架

        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`
        print返回的结果，输出如下：
        +------------+----------------------------------------+-------------------------+
        | 框架名称   | 版本                                   | 训练模式                |
        +------------+----------------------------------------+-------------------------+
        | TENSORFLOW | ti-acc1.0-tf1.15-py3.6-cuda10.0-gpu    | PS_WORKER               |
        | TENSORFLOW | light3.1.3-tf2.4-py3.8-cuda11.1-gpu    | MPI, HOROVOD            |
        | TENSORFLOW | tf1.15-py3.7-cpu                       | PS_WORKER, MPI, HOROVOD |
        | TENSORFLOW | tf1.15-py3.7-cuda10.0-gpu              | PS_WORKER, MPI, HOROVOD |
        | TENSORFLOW | tf2.4-py3.8-cpu                        | PS_WORKER, MPI, HOROVOD |
        | TENSORFLOW | tf2.4-py3.8-cuda11.1-gpu               | PS_WORKER, MPI, HOROVOD |
        | PYTORCH    | ti-acc1.0-torch1.9-py3.8-cuda11.1-gpu  | DDP                     |
        | PYTORCH    | light3.1.3-torch1.9-py3.8-cuda11.1-gpu | DDP, MPI, HOROVOD       |
        | PYTORCH    | torch1.9-py3.8-cuda11.1-gpu            | DDP, MPI, HOROVOD       |
        | SPARK      | spark2.4.5-cpu                         | SPARK                   |
        | PYSPARK    | spark2.4.5-py3.6-cpu                   | SPARK                   |
        +------------+----------------------------------------+-------------------------+
        """
        try:
            req = models.DescribeTrainingFrameworksRequest()
            return self._tione_client.DescribeTrainingFrameworks(req)
        except TencentCloudSDKException as err:
            raise

    def delete_training_task(self, task_id):
        """删除某个训练任务

        :param task_id: 训练任务ID
        :type task_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingTaskResponse`
        """
        try:
            req = models.DeleteTrainingTaskRequest()
            req.Id = task_id
            return self._tione_client.DeleteTrainingTask(req)
        except TencentCloudSDKException as err:
            raise

    def describe_training_task_pods(self, task_id):
        """获取训练任务的pod列表

        :param task_id: 训练任务ID
        :type task_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsResponse`
        """
        try:
            req = models.DescribeTrainingTaskPodsRequest()
            req.Id = task_id
            return self._tione_client.DescribeTrainingTaskPods(req)
        except TencentCloudSDKException as err:
            raise

    def _describe_logs(
        self,
        service,
        pod_name,
        start_time=None,
        end_time=None,
        limit=None,
        order=None,
        context=None,
        filters=None,
    ):
        """查看pod的日志

        :param service: 查询哪种类型的日志。 TRAIN：训练任务； NOTEBOOK：Notebook服务； INFER：推理服务；
        :type service: str
        """
        try:
            req = models.DescribeLogsRequest()
            req.Service = service
            req.PodName = pod_name
            req.StartTime = start_time
            req.EndTime = end_time
            req.Limit = limit
            req.Order = order
            req.Context = context
            req.Filters = filters
            return self._tione_client.DescribeLogs(req)
        except TencentCloudSDKException as err:
            raise

    def save_log(self, path, compress=None, service=None, service_id=None, pod_name=None, start_time=None,
                 end_time=None, order=None):
        """下载日志文件到本地

        :param path: 日志文件保存的本地路径
        :type path: str
        :param compress: 是否压缩日志文件，默认不压缩
        :type compress: bool
        :param service: 下载哪种类型的日志。 TRAIN：训练任务； NOTEBOOK：Notebook服务； INFER：推理服务；
        :type service: str
        :param service_id: 服务ID
        :type service: str
        :param pod_name: 查询哪个Pod的日志，支持支持结尾通配符。查看某个训练任务的全部pod的日志可以填： "<task_id>*"，如：train-51cd6bf7ec1000*
        :type pod_name: str
        :param start_time: 日志查询开始时间。RFC3339格式的时间字符串，比如2021-12-16T13:20:24+08:00，默认值为当前时间的前一个小时
        :type start_time: str
        :param end_time: 日志查询结束时间。RFC3339格式的时间字符串，比如2021-12-16T13:20:24+08:00，默认值为当前时间
        :type end_time: str
        :param order: 排序方向。(ASC | DESC) 默认值为ASC
        :type order: str
        """
        self._kit_log.save(path, compress, service, service_id, pod_name, start_time, end_time, order)

    def describe_train_logs(
        self,
        pod_name,
        start_time=None,
        end_time=None,
        limit=None,
        order=None,
        context=None,
        filters=None,
    ):
        """查看训练任务的日志

        :param pod_name: 查询哪个Pod的日志，支持通配符。查看某个训练任务的全部pod的日志可以填： "<task_id>*"，如：train-51cd6bf7ec1000*
        :type pod_name: str
        :param start_time: 日志查询开始时间。RFC3339格式的时间字符串，比如2021-12-16T13:20:24+08:00，默认值为当前时间的前一个小时
        :type start_time: str
        :param end_time: 日志查询结束时间。RFC3339格式的时间字符串，比如2021-12-16T13:20:24+08:00，默认值为当前时间
        :type end_time: str
        :param limit: 日志查询条数，默认值100，最大值100
        :type limit: int
        :param order: 排序方向。(ASC | DESC) 默认值为DESC
        :type order: str
        :param context: 分页的游标
        :type context: str
        :param filters: 过滤Filters
        :type filters: list of tikit.tencentcloud.tione.v20211111.models.Filter
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`

            返回的对象如果非空，就会有 next() 方法，能不断地获取下一页的日志（如果有多页的话），如下：
            now_time = datetime.datetime.now(datetime.timezone.utc)
            now_time_str = now_time.isoformat()
            result = client.describe_train_logs("train-51cd6bf7ec1000-37c5p5nlr01s-launcher",
                                                "2021-12-10T09:32:03.823509+00:00",
                                                now_time_str,
                                                limit=30)
            print(result)
            print(result.next())
            print(result.next())
            print(result.next())
        """
        result = self._describe_logs(
            "TRAIN", pod_name, start_time, end_time, limit, order, context, filters
        )

        def get_next_data(xx):
            if result.Context != "":
                next_result = self.describe_train_logs(
                    pod_name,
                    start_time,
                    end_time,
                    limit,
                    order,
                    result.Context,
                    filters,
                )
                result.Context = next_result.Context
                result.Content = next_result.Content
                result.RequestId = next_result.RequestId
                return result
            else:
                print("All logs are displayed! Return None.")
                return None

        result.next = types.MethodType(get_next_data, result)
        return result

    def create_table_dataset(
        self,
        dataset_name,
        storage_data_path,
        storage_label_path,
        dataset_tags=None,
        is_schema_existed=None,
        schema_info_dict=None,
    ):
        """创建表格数据集

        :param dataset_name: 数据集名称
        :type dataset_name: str
        :param storage_data_path: 数据源cos路径。格式：<bucket>/<cos path>/
        :type storage_data_path:  str
        :param storage_label_path: 数据集标签cos存储路径。格式：<bucket>/<cos path>/
        :type storage_label_path:  str
        :param dataset_tags: 数据集标签
        :type dataset_tags: list of tikit.tencentcloud.tione.v20211111.models.Tag
        :param is_schema_existed: 数据是否存在表头。
            若数据文件包含表头，则请您严格按照表格列名配置Schema信息，否则校验不通过会造成导入数据集失败；
            若数据文件不包含表头，则平台会根据您定义的Schema信息依次为您解析表格数据
        :type is_schema_existed: bool
        :param schema_info_dict: 表头信息。格式： 字段名称 -> 数据类型。字段的数据类型包括：
            TYPE_INT:       整型
            TYPE_STRING:    字符串
            TYPE_BOOL:      布尔型
            TYPE_FLOAT:     浮点型
        :type dict
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateDatasetResponse`
        """
        try:
            req = models.CreateDatasetRequest()
            req.DatasetName = dataset_name
            req.DatasetType = "TYPE_DATASET_TABLE"
            req.StorageDataPath = self.parse_cos_info(storage_data_path)
            req.StorageLabelPath = self.parse_cos_info(storage_label_path)
            req.DatasetTags = dataset_tags
            req.IsSchemaExisted = is_schema_existed
            req.SchemaInfos = []
            for field in schema_info_dict:
                schema_info = models.SchemaInfo()
                if field == "":
                    raise TencentCloudSDKException(
                        message="schema_info.Name must be non-empty string"
                    )
                if schema_info_dict[field] not in SCHEMA_INFO_VALUE_TYPES:
                    raise TencentCloudSDKException(
                        message="schema_info.Type must in {}".format(
                            SCHEMA_INFO_VALUE_TYPES
                        )
                    )
                schema_info.Name = field
                schema_info.Type = schema_info_dict[field]
                req.SchemaInfos.append(schema_info)
            return self._tione_client.CreateDataset(req)
        except TencentCloudSDKException as err:
            raise

    def create_image_dataset(
        self,
        dataset_name,
        storage_data_path,
        storage_label_path,
        dataset_tags=None,
        with_annotation=False,
        annotation_type=None,
        annotation_format=None,
    ):
        """创建图片数据集

        :param dataset_name: 数据集名称
        :type dataset_name: str
        :param storage_data_path: 数据源cos路径。格式：<bucket>/<cos path>/
        :type storage_data_path:  str
        :param storage_label_path: 数据集标签cos存储路径。格式：<bucket>/<cos path>/
        :type storage_label_path:  str
        :param dataset_tags: 数据集标签
        :type dataset_tags: list of tikit.tencentcloud.tione.v20211111.models.Tag
        :param with_annotation: 是否已经标注
        :type with_annotation: bool
        :param annotation_type: 标注类型。可选值如下：
            ANNOTATION_TYPE_CLASSIFICATION: 图片分类
            ANNOTATION_TYPE_DETECTION:      目标检测
            ANNOTATION_TYPE_SEGMENTATION:   图片分割
            ANNOTATION_TYPE_TRACKING:       目标跟踪
        :type annotation_type: str
        :param annotation_format: 标注格式。可选值如下：
            ANNOTATION_FORMAT_TI:       TI平台格式
            ANNOTATION_FORMAT_PASCAL:   Pascal Voc
            ANNOTATION_FORMAT_COCO:     COCO
            ANNOTATION_FORMAT_FILE:     文件目录结构
        :type annotation_format: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateDatasetResponse`
        """
        try:
            req = models.CreateDatasetRequest()
            req.DatasetName = dataset_name
            req.DatasetType = "TYPE_DATASET_IMAGE"
            req.StorageDataPath = self.parse_cos_info(storage_data_path)
            req.StorageLabelPath = self.parse_cos_info(storage_label_path)
            req.DatasetTags = dataset_tags
            req.AnnotationStatus = (
                "STATUS_ANNOTATED" if with_annotation else "STATUS_NON_ANNOTATED"
            )
            if with_annotation:
                if annotation_type not in ANNOTATION_TYPES:
                    raise TencentCloudSDKException(
                        message="annotation_type must in {}".format(ANNOTATION_TYPES)
                    )
                if annotation_format not in ANNOTATION_FORMATS:
                    raise TencentCloudSDKException(
                        message="annotation_format must in {}".format(
                            ANNOTATION_FORMATS
                        )
                    )
            req.AnnotationType = annotation_type
            req.AnnotationFormat = annotation_format
            return self._tione_client.CreateDataset(req)
        except TencentCloudSDKException as err:
            raise

    def create_other_dataset(
        self, dataset_name, storage_data_path, storage_label_path, dataset_tags=None
    ):
        """创建其他类型的数据集

        :param dataset_name: 数据集名称
        :type dataset_name: str
        :param storage_data_path: 数据源cos路径。格式：<bucket>/<cos path>/
        :type storage_data_path:  str
        :param storage_label_path: 数据集标签cos存储路径。格式：<bucket>/<cos path>/
        :type storage_label_path:  str
        :param dataset_tags: 数据集标签
        :type dataset_tags: list of tikit.tencentcloud.tione.v20211111.models.Tag
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateDatasetResponse`
        """
        try:
            req = models.CreateDatasetRequest()
            req.DatasetName = dataset_name
            req.DatasetType = "TYPE_DATASET_OTHER"
            req.StorageDataPath = self.parse_cos_info(storage_data_path)
            req.StorageLabelPath = self.parse_cos_info(storage_label_path)
            req.DatasetTags = dataset_tags
            return self._tione_client.CreateDataset(req)
        except TencentCloudSDKException as err:
            raise

    def _check_model_clean_params(
        self,
        req,
        model_auto_clean=None,
        model_clean_period=None,
        max_reserved_models=None,
    ):
        if model_auto_clean is not None:
            req.AutoClean = model_auto_clean
        if model_clean_period is not None:
            if model_clean_period == 0:
                req.ModelCleanPeriod = 65535
            else:
                req.ModelCleanPeriod = model_clean_period
        if max_reserved_models is not None:
            if max_reserved_models == 0:
                req.MaxReservedModels = 65535
            else:
                req.MaxReservedModels = max_reserved_models


    def _set_cos_path_info(self, req, model_output_path):
        if isinstance(model_output_path, str):
            req.ModelOutputPath = self.parse_cos_info(model_output_path)
            return
        cos_path_info = models.CosPathInfo()
        cos_path_info.Bucket = model_output_path.Bucket
        cos_path_info.Region = model_output_path.Region
        cos_path_info.Paths = [model_output_path.Path]
        cos_path_info.Uin = model_output_path.Uin
        cos_path_info.SubUin = model_output_path.SubUin
        req.ModelOutputPath = cos_path_info

    def _set_task_cos_path_info(self, req, training_model_cos_path):
        if isinstance(training_model_cos_path, str):
            req.TrainingModelCosPath = self.parse_cos_info(training_model_cos_path)
            return
        cos_path_info = models.CosPathInfo()
        cos_path_info.Bucket = training_model_cos_path.Bucket
        cos_path_info.Region = training_model_cos_path.Region
        cos_path_info.Paths = [training_model_cos_path.Path]
        cos_path_info.Uin = training_model_cos_path.Uin
        cos_path_info.SubUin = training_model_cos_path.SubUin
        req.TrainingModelCosPath = cos_path_info


    def create_taiji_hy_model_by_task(
        self, training_model_name, training_job_id, tags=None
    ):
        """使用现有的任务的结果来创建新的taiji_hy模型

        :param training_model_name: 模型名称
        :type training_model_name: str
        :param training_job_id: 训练任务id
        :type training_job_id: str
        :param tags: 标签配置
        :type tags: list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingModelResponse`
        返回的内容如下：
        {
          "Id": "m-23054253294030848",
          "TrainingModelVersionId": "mv-v1-558585918986294017",
          "RequestId": "c8f9b70e-bf4d-4c34-9480-21d902d3b341"
        }
        """
        req = models.CreateTrainingModelRequest()
        req.ImportMethod = "MODEL"
        req.TrainingModelName = training_model_name
        req.ModelAffiliation = "AI_MARKET"

        return self._create_taiji_hy_model_by_task(req, training_job_id, tags=tags)

    def describe_training_model_version(self, training_model_version_id):
        """查看单个版本的信息

        :param training_model_version_id: 模型版本id
        :type training_model_version_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionResponse`
        """
        try:
            req = models.DescribeTrainingModelVersionRequest()
            req.TrainingModelVersionId = training_model_version_id
            return self._tione_client.DescribeTrainingModelVersion(req)
        except TencentCloudSDKException as err:
            raise

    def _parse_batch_cos_target_path(self, data_config):
        if not isinstance(data_config, list):
            # 兼容旧版本的处理
            if data_config.DataSource == "COS":
                for cos_str in data_config.DataConfigDict:
                    data_config.DataConfigDict[cos_str] = ""
            return data_config

        for i in range(len(data_config)):
            if data_config[i].DataSource == "COS":
                data_config[i].TargetPath = ""
        return data_config

    def _new_name_filter(self, name, value):
        filter = models.Filter()
        filter.Name = name
        filter.Values = [value]
        filter.Fuzzy = False
        return [filter]

    def create_model_service_version(
        self,
        worker_resource,
        framework,
        service_group_id=None,
        service_description=None,
        resource_group_id=None,
        model_config_info=None,
        model_cos_path=None,
        volume_mount=None,
        service_limit=None,
        scheduled_action=None,
        model_hot_update_enable=False,
        env=None,
        scale_mode="MANUAL",
        replicas=1,
        horizontal_pod_autoscaler=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        authorization_enable=False,
        tags=None,
        cron_scale_jobs=None,
        scale_strategy=None,
        hybrid_billing_prepaid_replicas=None,
        command=None,
    ):
        """创建模型服务版本

        :param worker_resource:        worker节点的配置
        :type worker_resource:         :class:`tikit.models.ModelServiceResourceConfigInfo`
        :param framework:              运行的框架环境
        :type framework:               :class:`tikit.models.FrameworkInfo`
        :param service_group_id:       服务id
        :type service_group_id:        str
        :param service_description:    服务描述
        :type service_description:     str
        :param resource_group_id:      预付费模式下所属的资源组id
        :type resource_group_id:       str
        :param model_config_info:      模型信息
        :type model_config_info:       :class:`tikit.models.ModelConfigInfo`
        :param model_cos_path:         模型cos信息
        :type model_cos_path:          str
        :param volume_mount:           挂载的存储信息
        :type volume_mount:            :class:`tikit.tencentcloud.tione.v20211111.models.VolumeMount`
        :param service_limit:          服务限流
        :type service_limit:           :class:`tikit.tencentcloud.tione.v20211111.models.ServiceLimit`
        :param scheduled_action:       定时停止的任务配置
        :type scheduled_action:        :class:`tikit.tencentcloud.tione.v20211111.models.ScheduledAction`
        :param model_hot_update_enable :是否开启模型的热更新。默认不开启
        :type model_hot_update_enable: bool
        :param env:                    环境变量
        :type env:                     list of :class:`tikit.tencentcloud.tione.v20211111.models.EnvVar`
        :param scale_mode:             扩缩容类型
        :type scale_mode:              str
        :param replicas:               实例数量
        :type replicas:                int
        :param horizontal_pod_autoscaler: 自动伸缩信息
        :type horizontal_pod_autoscaler:  :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param log_enable:             日志开关
        :type log_enable:              bool
        :param log_logset_id:          日志集id
        :type log_logset_id:           str
        :param log_topic_id:           日志的topic id
        :type log_topic_id:            str
        :param authorization_enable:   接口鉴权开关
        :type authorization_enable:    bool
        :param tags:                   标签
        :type tags:                    list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :param cron_scale_jobs:        定时任务配置
        :type cron_scale_jobs:         list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :param scale_strategy:         自动伸缩策略配置 HPA
        :type scale_strategy:          str
        :param hybrid_billing_prepaid_replicas: 混合计费模式下预付费实例数
        :type hybrid_billing_prepaid_replicas:  int
        :param model_hot_update_enable: 是否开启模型的热更新。默认不开启
        :type model_hot_update_enable: bool
        :param command:                启动命令
        :type command:                 str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateModelServiceResponse`
        """

        return self._create_model_service_do(
            "",
            worker_resource,
            framework,
            service_group_id,
            service_description,
            resource_group_id,
            model_config_info,
            model_cos_path,
            volume_mount,
            service_limit,
            scheduled_action,
            model_hot_update_enable,
            env,
            scale_mode,
            replicas,
            horizontal_pod_autoscaler,
            log_enable,
            log_logset_id,
            log_topic_id,
            authorization_enable,
            tags,
            cron_scale_jobs,
            scale_strategy,
            hybrid_billing_prepaid_replicas,
            command,
            True,
        )

    def create_model_service(
        self,
        service_group_name,
        worker_resource,
        framework=None,
        service_description=None,
        resource_group_id=None,
        model_config_info=None,
        model_cos_path=None,
        volume_mount=None,
        service_limit=None,
        scheduled_action=None,
        model_hot_update_enable=False,
        env=None,
        scale_mode="MANUAL",
        replicas=1,
        horizontal_pod_autoscaler=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        authorization_enable=False,
        tags=None,
        cron_scale_jobs=None,
        scale_strategy=None,
        hybrid_billing_prepaid_replicas=None,
        command=None,
    ):
        """创建模型服务

        :param service_group_name:     服务名称
        :type service_group_name:      str
        :param worker_resource:        worker节点的配置
        :type worker_resource:         :class:`tikit.models.ModelServiceResourceConfigInfo`
        :param framework:              运行的框架环境
        :type framework:               :class:`tikit.models.FrameworkInfo`
        :param service_description:    服务描述
        :type service_description:     str
        :param resource_group_id:      预付费模式下所属的资源组id
        :type resource_group_id:       str
        :param model_config_info:      模型信息
        :type model_config_info:       :class:`tikit.models.ModelConfigInfo`
        :param model_cos_path:         模型cos信息
        :type model_cos_path:          str
        :param volume_mount:           挂载的存储信息
        :type volume_mount:            :class:`tikit.tencentcloud.tione.v20211111.models.VolumeMount`
        :param service_limit:          服务限流
        :type service_limit:           :class:`tikit.tencentcloud.tione.v20211111.models.ServiceLimit`
        :param scheduled_action:       定时停止的任务配置
        :type scheduled_action:        :class:`tikit.tencentcloud.tione.v20211111.models.ScheduledAction`
        :param model_hot_update_enable :是否开启模型的热更新。默认不开启
        :type model_hot_update_enable: bool
        :param env:                    环境变量
        :type env:                     list of :class:`tikit.tencentcloud.tione.v20211111.models.EnvVar`
        :param scale_mode:             扩缩容类型
        :type scale_mode:              str
        :param replicas:               实例数量
        :type replicas:                int
        :param horizontal_pod_autoscaler: 自动伸缩信息
        :type horizontal_pod_autoscaler:  :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param log_enable:             日志开关
        :type log_enable:              bool
        :param log_logset_id:          日志集id
        :type log_logset_id:           str
        :param log_topic_id:           日志的topic id
        :type log_topic_id:            str
        :param authorization_enable:   接口鉴权开关
        :type authorization_enable:    bool
        :param tags:                   标签
        :type tags:                    list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :param cron_scale_jobs:        定时任务配置
        :type cron_scale_jobs:         list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :param scale_strategy:         自动伸缩策略配置 HPA
        :type scale_strategy:          str
        :param hybrid_billing_prepaid_replicas: 混合计费模式下预付费实例数
        :type hybrid_billing_prepaid_replicas:  int
        :param command:                启动命令
        :type command:                 str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateModelServiceResponse`
        """

        return self._create_model_service_do(
            service_group_name,
            worker_resource,
            framework,
            "",
            service_description,
            resource_group_id,
            model_config_info,
            model_cos_path,
            volume_mount,
            service_limit,
            scheduled_action,
            model_hot_update_enable,
            env,
            scale_mode,
            replicas,
            horizontal_pod_autoscaler,
            log_enable,
            log_logset_id,
            log_topic_id,
            authorization_enable,
            tags,
            cron_scale_jobs,
            scale_strategy,
            hybrid_billing_prepaid_replicas,
            command,
            False,
        )

    def _create_model_service_from_file(self, filename: str):
        """从模型服务描述文件创建服务

        :param filename:     模型文件描述文件
        :type filename:      str
        """
        args = self._create_model_service_file_to_arguments(filename)
        result = self._create_model_service_do(**args)
        if (
            result.Service
            and result.Service.ServiceGroupId
            and result.Service.ServiceId
        ):
            service_group_id = result.Service.ServiceGroupId
            service_id = result.Service.ServiceId
            content = ""
            with open(filename, "r") as infile:
                sgi_found = False
                si_found = False
                for line in infile:
                    if line.startswith("service_id"):
                        content += f"service_id: {service_id}\n"
                        si_found = True
                    elif line.startswith("service_group_id"):
                        content += f"service_group_id: {service_group_id}\n"
                        sgi_found = True
                    else:
                        content += line
                if not sgi_found:
                    content += f"service_group_id: {service_group_id}\n"
                if not si_found:
                    content += f"service_id: {service_id}\n"
            with open(filename, "w") as outfile:
                outfile.write(content)
            return f"成功创建服务{service_id}，服务ID已经写入文件{filename}。如果需要创建新版本，需要新建一个配置文件，切勿重用文件{filename}，否则会丢失本次新建的服务配置。"

    def _create_model_service_file_to_arguments(self, filename: str) -> dict:
        result = {}
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        import yaml

        with open(filename, "r") as infile:
            data = yaml.load(infile, Loader=yaml.SafeLoader)

        if data.get("new_version"):
            service_group_id = data.get("service_group_id")
            if not service_group_id:
                raise ValueError(
                    "service_group_id should not be empty when you want to add a new version"
                )
            result["new_version"] = True
            result["service_group_id"] = service_group_id
            result["service_group_name"] = data.get("service_group_name", "")
        else:
            if not data.get("service_group_name"):
                raise ValueError("service_group_name should not be empty")
            result["service_group_name"] = data["service_group_name"]
            if data.get("service_group_description"):
                result["service_description"] = data["service_group_description"]

        charge_type = data.get("charge_type")
        if charge_type == "PREPAID":
            if not data.get("resource_group_id"):
                raise ValueError(
                    "resource_group_id should not be empty when charge_type is PREPAID"
                )
            result["resource_group_id"] = data["resource_group_id"]
            resources = data.get("resources")
            if not resources:
                raise ValueError(
                    "resources should not be empty when charge_type is PREPAID"
                )
            result["worker_resource"] = (
                TiModels.ModelServiceResourceConfigInfo.new_prepaid(
                    resources.get("cpu") / 1000,
                    resources.get("memory") / 1024,
                    gpu=None if not resources.get("gpu") else resources["gpu"] / 100,
                    gpu_type=(
                        None if not resources.get("gpu_type") else resources["gpu_type"]
                    ),
                )
            )
        elif charge_type == "POSTPAID_BY_HOUR":
            instance_type = data.get("instance_type")
            if not instance_type:
                raise ValueError(
                    "instance_type should not be empty when charge_type is POSTPAID_BY_HOUR"
                )
            result["worker_resource"] = (
                TiModels.ModelServiceResourceConfigInfo.new_postpaid(instance_type)
            )
        elif charge_type == "HYBRID_PAID":
            if not data.get("resource_group_id"):
                raise ValueError(
                    "resource_group_id should not be empty when charge_type is HYBRID_PAID"
                )
            result["resource_group_id"] = data["resource_group_id"]
            instance_type = data.get("instance_type")
            if not instance_type:
                raise ValueError(
                    "instance_type should not be empty when charge_type is HYBRID_PAID"
                )
            result["worker_resource"] = (
                TiModels.ModelServiceResourceConfigInfo.new_hybridpaid(instance_type)
            )
            hybrid_billing_prepaid_replicas = data.get(
                "hybrid_billing_prepaid_replicas"
            )
            if not hybrid_billing_prepaid_replicas:
                raise ValueError(
                    "hybrid_billing_prepaid_replicas should not be empty when charge_type is HYBRID_PAID"
                )
            result["hybrid_billing_prepaid_replicas"] = hybrid_billing_prepaid_replicas

        model_type = data.get("model_type", "normal").upper()
        model_version_id = data.get("model_version_id")
        if model_version_id:
            result["model_config_info"] = (
                TiModels.ModelConfigInfo.new_model_reference_lite(
                    model_version_id, model_type
                )
            )
        if not model_version_id and not data.get("image_info"):
            # 模型 与 镜像 必须要有一个
            raise ValueError("image_info should not be empty when no model chosed")
        if not model_version_id and data.get("image_info"):
            image_info = data["image_info"]
            result["framework"] = TiModels.FrameworkInfo.new_custom_image(
                image_info.get("image_type"),
                image_info.get("image_url"),
                registry_region=(
                    None
                    if not image_info.get("registry_region")
                    else image_info["registry_region"]
                ),
                registry_id=(
                    None
                    if not image_info.get("registry_id")
                    else image_info["registry_id"]
                ),
            )
        if data.get("model_hot_update_enable"):
            result["model_hot_update_enable"] = True

        if data.get("env"):
            result["env"] = []
            for e in data.get("env"):
                ev = models.EnvVar()
                ev.Name = e["name"]
                ev.Value = e["value"]
                result["env"].append(ev)

        if data.get("replicas") is None:
            raise ValueError("replicas should not be empty")
        result["replicas"] = data["replicas"]
        scale_mode = data.get("scale_mode", "MANUAL")
        result["scale_mode"] = scale_mode
        scale_strategy = data.get("scale_strategy", None)
        if scale_strategy:
            result["scale_strategy"] = scale_strategy
        if scale_mode == "AUTO" and scale_strategy == "HPA":
            hpa = data.get("horizontal_pod_autoscaler")
            if not hpa:
                raise ValueError("horizontal_pod_autoscaler should not be empty")
            scaler = models.HorizontalPodAutoscaler()
            hpa_metrics = hpa.get("hpa_metrics")
            if not hpa_metrics:
                raise ValueError("hpa_metrics should not be empty")
            scaler.HpaMetrics = []
            for me in hpa_metrics:
                met = models.Option()
                met.Name = me.get("name")
                met.Value = me.get("value")
                scaler.HpaMetrics.append(met)
            scaler.MinReplicas = hpa.get("min_replicas", 1)
            scaler.MaxReplicas = hpa.get("max_replicas", 1)
            result["horizontal_pod_autoscaler"] = scaler
        elif scale_mode == "AUTO" and scale_strategy == "CRON":
            jobs = data.get("cron_scale_jobs")
            if not jobs:
                raise ValueError("cron_scale_jobs should not be empty")
            cron_jobs = []
            for j in jobs:
                job = models.CronScaleJob()
                job.Name = j.get("name")
                job.MinReplicas = j.get("min_replicas")
                job.MaxReplicas = j.get("max_replicas")
                job.TargetReplicas = j.get("target_replicas")
                job.Schedule = j.get("schedule")
                cron_jobs.append(job)
            result["cron_scale_jobs"] = cron_jobs
        elif scale_mode == "MANUAL" and not scale_strategy:
            pass
        else:
            message = f"invalid value: (scale_mode x scale_strategy) tuple should only be one of [(MANUAL, NONE), (AUTO, HPA), (AUTO, CRON)], but your input is ({scale_mode}, {scale_strategy})"
            raise ValueError(message)

        if data.get("log_enable"):
            result["log_enable"] = True
            result["log_logset_id"] = data.get("log_config").get("logset_id")
            result["log_topic_id"] = data.get("log_config").get("topic_id")
        if data.get("authorization_enable"):
            result["authorization_enable"] = True
        if data.get("tags"):
            tags = []
            for t in data.get("tags"):
                tag = models.Tag()
                tag.TagKey = t.get("tag_key")
                tag.TagValue = t.get("tag_value")
                tags.append(tag)
            result["tags"] = tags
        _svc_limit = data.get("service_limit")
        if _svc_limit:
            service_limit = models.ServiceLimit()
            service_limit.EnableInstanceRpsLimit = _svc_limit.get(
                "enable_instance_rps_limit", False
            )
            service_limit.InstanceRpsLimit = _svc_limit.get("instance_rps_limit", 0)
            result["service_limit"] = service_limit
        _vol_mount = data.get("volume_mount")
        if _vol_mount:
            volume_mount = models.VolumeMount()
            volume_mount.VolumeSourceType = _vol_mount.get("volume_source_type", "CFS")
            cfs_config = _vol_mount.get("cfs_config")
            if not cfs_config:
                raise ValueError("cfs_config should not be empty")
            cfg = models.CFSConfig()
            cfg.Id = cfs_config.get("id")
            cfg.Path = cfs_config.get("path")
            volume_mount.CFSConfig = cfg
            result["volume_mount"] = volume_mount
        _sch_action = data.get("scheduled_action")
        if _sch_action:
            schedule_action = models.ScheduledAction()
            schedule_action.ScheduleStop = _sch_action.get("schedule_stop", False)
            stop_time = _sch_action.get("schedule_stop_time")
            if isinstance(stop_time, datetime.datetime):
                schedule_action.ScheduleStopTime = stop_time.astimezone().isoformat()
            else:
                schedule_action.ScheduleStopTime = stop_time
            result["scheduled_action"] = schedule_action
        return result

    def _create_model_service_do(
        self,
        service_group_name,
        worker_resource,
        framework=None,
        service_group_id=None,
        service_description=None,
        resource_group_id=None,
        model_config_info=None,
        model_cos_path=None,
        volume_mount=None,
        service_limit=None,
        scheduled_action=None,
        model_hot_update_enable=False,
        env=None,
        scale_mode="MANUAL",
        replicas=1,
        horizontal_pod_autoscaler=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        authorization_enable=False,
        tags=None,
        cron_scale_jobs=None,
        scale_strategy=None,
        hybrid_billing_prepaid_replicas=None,
        command=None,
        new_version=False,
    ):
        """创建模型服务

        :param service_group_name:     服务名称
        :type service_group_name:      str
        :param worker_resource:        worker节点的配置
        :type worker_resource:         :class:`tikit.models.ModelServiceResourceConfigInfo`
        :param framework:              运行的框架环境
        :type framework:               :class:`tikit.models.FrameworkInfo`
        :param service_group_id:       服务id
        :type service_group_id:        str
        :param service_description:    服务描述
        :type service_description:     str
        :param resource_group_id:      预付费模式下所属的资源组id
        :type resource_group_id:       str
        :param model_config_info:      模型信息
        :type model_config_info:       :class:`tikit.models.ModelConfigInfo`
        :param model_cos_path:         模型cos信息
        :type model_cos_path:          str
        :param volume_mount:           环境变量
        :type volume_mount:            :class:`tikit.tencentcloud.tione.v20211111.models.VolumeMount`
        :param service_limit:          服务限流
        :type service_limit:           :class:`tikit.tencentcloud.tione.v20211111.models.ServiceLimit`
        :param scheduled_action:       服务限流
        :type scheduled_action:        :class:`tikit.tencentcloud.tione.v20211111.models.ScheduledAction`
        :param model_hot_update_enable:是否开启模型的热更新。默认不开启
        :type model_hot_update_enable: bool
        :param env:                    环境变量
        :type env:                     list of :class:`tikit.tencentcloud.tione.v20211111.models.EnvVar`
        :param scale_mode:             扩缩容类型
        :type scale_mode:              str
        :param replicas:               实例数量
        :type replicas:                int
        :param horizontal_pod_autoscaler: 自动伸缩信息
        :type horizontal_pod_autoscaler:  :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param log_enable:             日志开关
        :type log_enable:              bool
        :param log_logset_id:          日志集id
        :type log_logset_id:           str
        :param log_topic_id:           日志的topic id
        :type log_topic_id:            str
        :param authorization_enable:   接口鉴权开关
        :type authorization_enable:    bool
        :param tags:                   标签
        :type tags:                    list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :param cron_scale_jobs:        定时任务配置
        :type cron_scale_jobs:         list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :param scale_strategy:         自动伸缩策略配置 HPA
        :type scale_strategy:          str
        :param hybrid_billing_prepaid_replicas: 混合计费模式下预付费实例数
        :type hybrid_billing_prepaid_replicas:  int
        :param new_version:            新建版本
        :type new_version:             bool
        :param model_hot_update_enable: 是否开启模型的热更新。默认不开启
        :type model_hot_update_enable: bool
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateModelServiceResponse`
        """

        try:
            req = models.CreateModelServiceRequest()
            req.ServiceGroupName = service_group_name
            charge_type = worker_resource.ChargeType
            req.ChargeType = charge_type
            req.Command = command

            if not framework:
                if not model_config_info or not model_config_info.ModelVersionId:
                    raise ValueError(
                        "framework should not be empty when no models chosen"
                    )
                modelInfo = self.describe_training_model_version(
                    model_config_info.ModelVersionId
                )
                framework = TiModels.FrameworkInfo.new_custom_image(
                    "PRESET", modelInfo.TrainingModelVersion.ReasoningEnvironment
                )
            if framework.Name == "CUSTOM":
                req.ImageInfo = models.ImageInfo()
                req.ImageInfo.ImageType = framework.ImageType
                req.ImageInfo.ImageUrl = framework.ImageUrl
                req.ImageInfo.RegistryRegion = framework.RegistryRegion
                req.ImageInfo.RegistryId = framework.RegistryId
            req.ServiceGroupId = service_group_id
            req.ServiceDescription = service_description
            if charge_type == "PREPAID" or charge_type == "HYBRID_PAID":
                req.ResourceGroupId = resource_group_id

            if model_config_info is not None:
                req.ModelInfo = models.ModelInfo()
                req.ModelInfo.ModelId = model_config_info.ModelId
                req.ModelInfo.ModelName = model_config_info.ModelName
                req.ModelInfo.ModelVersionId = model_config_info.ModelVersionId
                req.ModelInfo.ModelVersion = model_config_info.ModelVersion
                req.ModelInfo.ModelSource = model_config_info.ModelSource
                # req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path) if model_cos_path else None
                if model_cos_path:
                    req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path)
                else:
                    req.ModelInfo.CosPathInfo = model_config_info.CosPathInfo
                req.ModelInfo.AlgorithmFramework = model_config_info.AlgorithmFramework
                req.ModelInfo.ModelType = model_config_info.ModelType

            req.Env = env

            req.VolumeMount = volume_mount
            req.ServiceLimit = service_limit
            req.ScheduledAction = scheduled_action
            req.ModelHotUpdateEnable = model_hot_update_enable

            worker_info = models.ResourceInfo()
            if charge_type == "PREPAID" or charge_type == "HYBRID_PAID":
                worker_info.Cpu = worker_resource.Cpu
                worker_info.Memory = worker_resource.Memory
                worker_info.Gpu = worker_resource.Gpu
                worker_info.GpuType = worker_resource.GpuType
            req.Resources = worker_info

            req.InstanceType = worker_resource.InstanceType
            req.ScaleMode = scale_mode
            req.Replicas = replicas
            req.HorizontalPodAutoscaler = horizontal_pod_autoscaler

            req.LogEnable = log_enable
            if log_enable:
                req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = log_logset_id
                req.LogConfig.TopicId = log_topic_id
            req.AuthorizationEnable = authorization_enable
            req.Tags = tags
            req.CronScaleJobs = cron_scale_jobs
            req.ScaleStrategy = scale_strategy
            req.HybridBillingPrepaidReplicas = hybrid_billing_prepaid_replicas
            req.NewVersion = new_version
            #
            if req.Command is not None:
                req.CommandBase64 = base64.b64encode(req.Command.encode()).decode(
                    "utf-8"
                )

            print(req._serialize())
            return self._tione_client.CreateModelService(req)
        except TencentCloudSDKException as err:
            raise

    def _modify_model_service_from_file(self, filename: str):
        """从模型服务描述文件更改服务

        :param filename:     模型文件描述文件
        :type filename:      str
        """
        args = self._modify_model_service_file_to_arguments(filename)
        result = self.modify_model_service(**args)
        if (
            result.Service
            and result.Service.ServiceGroupId
            and result.Service.ServiceId
        ):
            return f"success to update ModelService {result.Service.ServiceId}"

    def _modify_model_service_file_to_arguments(self, filename: str) -> dict:
        result = {}
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        import yaml

        with open(filename, "r") as infile:
            data = yaml.load(infile, Loader=yaml.SafeLoader)

        service_id = data.get("service_id")
        if not service_id:
            raise ValueError(
                "service_id should not be empty when you want to add a new version"
            )
        result["service_id"] = service_id

        if data.get("service_group_description"):
            result["service_description"] = data["service_group_description"]

        model_type = data.get("model_type", "normal").upper()
        model_version_id = data.get("model_version_id")
        if data.get("model_version_id"):
            result["model_config_info"] = (
                TiModels.ModelConfigInfo.new_model_reference_lite(
                    model_version_id,
                    model_type,
                )
            )
        if not model_version_id and not data.get("image_info"):
            # 模型 与 镜像 必须要有一个
            raise ValueError("image_info should not be empty when no model chosed")
        if not model_version_id and data.get("image_info"):
            image_info = data["image_info"]
            result["framework"] = TiModels.FrameworkInfo.new_custom_image(
                image_info.get("image_type"),
                image_info.get("image_url"),
                registry_region=(
                    None
                    if not image_info.get("registry_region")
                    else image_info["registry_region"]
                ),
                registry_id=(
                    None
                    if not image_info.get("registry_id")
                    else image_info["registry_id"]
                ),
            )
        if data.get("model_hot_update_enable"):
            result["model_hot_update_enable"] = True

        if data.get("env"):
            result["env"] = []
            for e in data.get("env"):
                ev = models.EnvVar()
                ev.Name = e["name"]
                ev.Value = e["value"]
                result["env"].append(ev)

        if data.get("replicas") is None:
            raise ValueError("replicas should not be empty")
        result["replicas"] = data["replicas"]
        hybrid_billing_prepaid_replicas = data.get("hybrid_billing_prepaid_replicas")
        if hybrid_billing_prepaid_replicas:
            result["hybrid_billing_prepaid_replicas"] = hybrid_billing_prepaid_replicas
        scale_mode = data.get("scale_mode", "MANUAL")
        result["scale_mode"] = scale_mode
        scale_strategy = data.get("scale_strategy", None)
        if scale_strategy:
            result["scale_strategy"] = scale_strategy
        if scale_mode == "AUTO" and scale_strategy == "HPA":
            hpa = data.get("horizontal_pod_autoscaler")
            if not hpa:
                raise ValueError("horizontal_pod_autoscaler should not be empty")
            scaler = models.HorizontalPodAutoscaler()
            hpa_metrics = hpa.get("hpa_metrics")
            if not hpa_metrics:
                raise ValueError("hpa_metrics should not be empty")
            scaler.HpaMetrics = []
            for me in hpa_metrics:
                met = models.Option()
                met.Name = me.get("name")
                met.Value = me.get("value")
                scaler.HpaMetrics.append(met)
            scaler.MinReplicas = hpa.get("min_replicas", 1)
            scaler.MaxReplicas = hpa.get("max_replicas", 1)
            result["horizontal_pod_autoscaler"] = scaler
        elif scale_mode == "AUTO" and scale_strategy == "CRON":
            jobs = data.get("cron_scale_jobs")
            if not jobs:
                raise ValueError("cron_scale_jobs should not be empty")
            cron_jobs = []
            for j in jobs:
                job = models.CronScaleJob()
                job.Name = j.get("name")
                job.MinReplicas = j.get("min_replicas")
                job.MaxReplicas = j.get("max_replicas")
                job.TargetReplicas = j.get("target_replicas")
                job.Schedule = j.get("schedule")
                cron_jobs.append(job)
            result["cron_scale_jobs"] = cron_jobs
        elif scale_mode == "MANUAL" and not scale_strategy:
            pass
        else:
            message = f"invalid value: (scale_mode x scale_strategy) tuple should only be one of [(MANUAL, NONE), (AUTO, HPA), (AUTO, CRON)], but your input is ({scale_mode}, {scale_strategy})"
            raise ValueError(message)

        if data.get("log_enable"):
            result["log_enable"] = True
            result["log_logset_id"] = data.get("log_config").get("logset_id")
            result["log_topic_id"] = data.get("log_config").get("topic_id")
        if data.get("authorization_enable"):
            result["authorization_enable"] = True
        _svc_limit = data.get("service_limit")
        if _svc_limit:
            service_limit = models.ServiceLimit()
            service_limit.EnableInstanceRpsLimit = _svc_limit.get(
                "enable_instance_rps_limit", False
            )
            service_limit.InstanceRpsLimit = _svc_limit.get("instance_rps_limit", 0)
            result["service_limit"] = service_limit
        _vol_mount = data.get("volume_mount")
        if _vol_mount:
            volume_mount = models.VolumeMount()
            volume_mount.VolumeSourceType = _vol_mount.get("volume_source_type", "CFS")
            cfs_config = _vol_mount.get("cfs_config")
            if not cfs_config:
                raise ValueError("cfs_config should not be empty")
            cfg = models.CFSConfig()
            cfg.Id = cfs_config.get("id")
            cfg.Path = cfs_config.get("path")
            volume_mount.CFSConfig = cfg
            result["volume_mount"] = volume_mount
        _sch_action = data.get("scheduled_action")
        if _sch_action:
            schedule_action = models.ScheduledAction()
            schedule_action.ScheduleStop = _sch_action.get("schedule_stop", False)
            stop_time = _sch_action.get("schedule_stop_time")
            if isinstance(stop_time, datetime.datetime):
                schedule_action.ScheduleStopTime = stop_time.astimezone().isoformat()
            else:
                schedule_action.ScheduleStopTime = stop_time
            result["scheduled_action"] = schedule_action
        return result

    def modify_model_service(
        self,
        service_id,
        model_config_info=None,
        model_cos_path=None,
        framework=None,
        volume_mount=None,
        service_limit=None,
        scheduled_action=None,
        model_hot_update_enable=None,
        env=None,
        worker_resource=None,
        scale_mode="MANUAL",
        replicas=1,
        horizontal_pod_autoscaler=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        service_action=None,
        service_description=None,
        scale_strategy=None,
        cron_scale_jobs=None,
        hybrid_billing_prepaid_replicas=None,
        command=None,
    ) -> models.ModifyModelServiceResponse:
        """更新模型服务版本

        :param service_id:                 服务版本id
        :type service_id:                  str
        :param model_config_info:          模型信息
        :type model_config_info:           :class:`tikit.models.ModelConfigInfo`
        :param model_cos_path:             模型cos信息
        :type model_cos_path:              str
        :param framework:                  运行的框架环境
        :type framework:                   :class:`tikit.models.FrameworkInfo`
        :param volume_mount:               挂载的存储信息
        :type volume_mount:                :class:`tikit.tencentcloud.tione.v20211111.models.VolumeMount`
        :param service_limit:              服务限流
        :type service_limit:               :class:`tikit.tencentcloud.tione.v20211111.models.ServiceLimit`
        :param scheduled_action:           定时停止的任务配置
        :type scheduled_action:            :class:`tikit.tencentcloud.tione.v20211111.models.ScheduledAction`
        :param model_hot_update_enable     :是否开启模型的热更新。默认不开启
        :type model_hot_update_enable:     bool
        :param env:                        环境变量
        :type env:                         list of :class:`tikit.tencentcloud.tione.v20211111.models.EnvVar`
        :param worker_resource:            worker节点配置
        :type worker_resource:             :class:`tikit.models.ModelServiceResourceConfigInfo`
        :param scale_mode:                 扩缩容类型
        :type scale_mode:                  str
        :param replicas:                   实例数量
        :type replicas:                    int
        :param horizontal_pod_autoscaler:  自动伸缩信息
        :type horizontal_pod_autoscaler:   :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param log_enable:                 日志开关
        :type log_enable:                  bool
        :param log_logset_id:              日志id
        :type log_logset_id:               str
        :param log_topic_id:               日志topic id
        :type log_topic_id:                str
        :param service_action:             特殊更新行为
        :type service_action:              str
        :param service_description:        服务描述
        :type service_description:         str
        :param scale_strategy:             自动伸缩策略
        :type scale_strategy:              str
        :param cron_scale_jobs:            自动伸缩策略配置 HPA
        :type cron_scale_jobs:             list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :param hybrid_billing_prepaid_replicas:  混合计费模式下预付费实例数
        :type hybrid_billing_prepaid_replicas:   int
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`
        """

        try:
            req = models.ModifyModelServiceRequest()
            req.ServiceId = service_id
            req.Command = command

            if model_config_info is not None:
                req.ModelInfo = models.ModelInfo()
                req.ModelInfo.ModelId = model_config_info.ModelId
                req.ModelInfo.ModelName = model_config_info.ModelName
                req.ModelInfo.ModelVersionId = model_config_info.ModelVersionId
                req.ModelInfo.ModelVersion = model_config_info.ModelVersion
                req.ModelInfo.ModelSource = model_config_info.ModelSource
                # req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path) if model_cos_path else None
                if model_cos_path:
                    req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path)
                else:
                    req.ModelInfo.CosPathInfo = model_config_info.CosPathInfo
                req.ModelInfo.AlgorithmFramework = model_config_info.AlgorithmFramework
                req.ModelInfo.ModelType = model_config_info.ModelType

            if framework and framework.Name == "CUSTOM":
                req.ImageInfo = models.ImageInfo()
                req.ImageInfo.ImageType = framework.ImageType
                req.ImageInfo.ImageUrl = framework.ImageUrl
                req.ImageInfo.RegistryRegion = framework.RegistryRegion
                req.ImageInfo.RegistryId = framework.RegistryId

            req.Env = env

            req.VolumeMount = volume_mount
            req.ServiceLimit = service_limit
            req.ScheduledAction = scheduled_action
            req.ModelHotUpdateEnable = model_hot_update_enable

            worker_info = models.ResourceInfo()
            if worker_resource:
                if worker_resource.ChargeType == "PREPAID":
                    worker_info.Cpu = worker_resource.Cpu
                    worker_info.Memory = worker_resource.Memory
                    worker_info.Gpu = worker_resource.Gpu
                    worker_info.GpuType = worker_resource.GpuType
                else:
                    req.InstanceType = worker_resource.InstanceType
            req.Resources = worker_info

            req.ScaleMode = scale_mode
            req.Replicas = replicas
            req.HorizontalPodAutoscaler = horizontal_pod_autoscaler
            req.LogEnable = log_enable
            if log_enable:
                req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = log_logset_id
                req.LogConfig.TopicId = log_topic_id

            req.ServiceAction = service_action
            req.ServiceDescription = service_description
            req.ScaleStrategy = scale_strategy
            req.CronScaleJobs = cron_scale_jobs
            req.HybridBillingPrepaidReplicas = hybrid_billing_prepaid_replicas
            if req.Command is not None:
                req.CommandBase64 = base64.b64encode(req.Command.encode()).decode(
                    "utf-8"
                )

            print(req._serialize())
            return self._tione_client.ModifyModelService(req)
        except TencentCloudSDKException as err:
            raise

    def patch_model_service(
        self,
        service_id,
        model_config_info=None,
        model_cos_path=None,
        framework=None,
        volume_mount=None,
        service_limit=None,
        scheduled_action=None,
        model_hot_update_enable=None,
        env=None,
        worker_resource=None,
        scale_mode=None,
        replicas=None,
        horizontal_pod_autoscaler=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        service_action=None,
        service_description=None,
        scale_strategy=None,
        cron_scale_jobs=None,
    ):
        """部分更新模型服务版本，不传的参数默认不更新

        :param service_id:                 服务版本id
        :type service_id:                  str
        :param model_config_info:          模型信息
        :type model_config_info:           :class:`tikit.models.ModelConfigInfo`
        :param model_cos_path:             模型cos信息
        :type model_cos_path:              str
        :param framework:                  运行的框架环境
        :type framework:                   :class:`tikit.models.FrameworkInfo`
        :param volume_mount:               挂载的存储信息
        :type volume_mount:                :class:`tikit.tencentcloud.tione.v20211111.models.VolumeMount`
        :param service_limit:              服务限流
        :type service_limit:               :class:`tikit.tencentcloud.tione.v20211111.models.ServiceLimit`
        :param scheduled_action:           定时停止的任务配置
        :type scheduled_action:            :class:`tikit.tencentcloud.tione.v20211111.models.ScheduledAction`
        :param model_hot_update_enable     :是否开启模型的热更新。默认不开启
        :type model_hot_update_enable:     bool
        :param env:                        环境变量
        :type env:                         list of :class:`tikit.tencentcloud.tione.v20211111.models.EnvVar`
        :param worker_resource:            worker节点配置
        :type worker_resource:             :class:`tikit.models.ModelServiceResourceConfigInfo`
        :param scale_mode:                 扩缩容类型
        :type scale_mode:                  str
        :param replicas:                   实例数量
        :type replicas:                    int
        :param horizontal_pod_autoscaler:  自动伸缩信息
        :type horizontal_pod_autoscaler:   :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param log_enable:                 日志开关
        :type log_enable:                  bool
        :param log_logset_id:              日志id
        :type log_logset_id:               str
        :param log_topic_id:               日志topic id
        :type log_topic_id:                str
        :param service_action:             特殊更新行为
        :type service_action:              str
        :param service_description:        服务版本描述
        :type service_description:         str
        :param scale_strategy:             自动伸缩策略
        :type scale_strategy:              str
        :param cron_scale_jobs:            自动伸缩策略配置 HPA
        :type cron_scale_jobs:             list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`
        """

        try:
            query_req = models.DescribeModelServiceRequest()
            query_req.ServiceId = service_id
            query_rsp = self._tione_client.DescribeModelService(query_req)
            if isinstance(query_rsp, TencentCloudSDKException):
                # error
                raise
            oldService = query_rsp.Service

            req = models.ModifyModelServiceRequest()
            req.ServiceId = service_id

            if model_config_info is not None:
                req.ModelInfo = models.ModelInfo()
                req.ModelInfo.ModelId = model_config_info.ModelId
                req.ModelInfo.ModelName = model_config_info.ModelName
                req.ModelInfo.ModelVersionId = model_config_info.ModelVersionId
                req.ModelInfo.ModelVersion = model_config_info.ModelVersion
                req.ModelInfo.ModelSource = model_config_info.ModelSource
                # req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path) if model_cos_path else None
                if model_cos_path:
                    req.ModelInfo.CosPathInfo = self.parse_cos_info(model_cos_path)
                else:
                    req.ModelInfo.CosPathInfo = model_config_info.CosPathInfo
                req.ModelInfo.AlgorithmFramework = model_config_info.AlgorithmFramework
                req.ModelInfo.ModelType = model_config_info.ModelType
            else:
                req.ModelInfo = oldService.ServiceInfo.ModelInfo

            if framework and framework.Name == "CUSTOM":
                req.ImageInfo = models.ImageInfo()
                req.ImageInfo.ImageType = framework.ImageType
                req.ImageInfo.ImageUrl = framework.ImageUrl
                req.ImageInfo.RegistryRegion = framework.RegistryRegion
                req.ImageInfo.RegistryId = framework.RegistryId
            else:
                req.ImageInfo = oldService.ServiceInfo.ImageInfo

            if env is not None:
                req.Env = env
            else:
                req.Env = oldService.ServiceInfo.Env

            if volume_mount is not None:
                req.VolumeMount = volume_mount
            else:
                req.VolumeMount = oldService.ServiceInfo.VolumeMount

            if service_limit is not None:
                req.ServiceLimit = service_limit
            else:
                req.ServiceLimit = oldService.ServiceLimit

            if scheduled_action is not None:
                req.ScheduledAction = scheduled_action
            else:
                req.ScheduledAction = oldService.ScheduledAction

            if model_hot_update_enable is not None:
                req.ModelHotUpdateEnable = model_hot_update_enable
            else:
                req.ModelHotUpdateEnable = oldService.ServiceInfo.ModelHotUpdateEnable

            if oldService.ChargeType == "PREPAID":
                worker_info = models.ResourceInfo()
                if worker_resource is not None:
                    worker_info.Cpu = worker_resource.Cpu
                    worker_info.Memory = worker_resource.Memory
                    worker_info.Gpu = worker_resource.Gpu
                    worker_info.GpuType = worker_resource.GpuType
                else:
                    worker_info = oldService.ServiceInfo.Resources
                req.Resources = worker_info
            else:
                if worker_resource is not None:
                    req.InstanceType = worker_resource.InstanceType
                else:
                    req.InstanceType = oldService.ServiceInfo.InstanceType

            if req.ScaleMode is not None:
                req.ScaleMode = scale_mode
            else:
                req.ScaleMode = oldService.ServiceInfo.ScaleMode

            if req.Replicas is not None:
                req.Replicas = replicas
            else:
                req.Replicas = oldService.ServiceInfo.Replicas

            if horizontal_pod_autoscaler is not None:
                req.HorizontalPodAutoscaler = horizontal_pod_autoscaler
            else:
                req.HorizontalPodAutoscaler = (
                    oldService.ServiceInfo.HorizontalPodAutoscaler
                )

            if log_enable is not None:
                req.LogEnable = log_enable
                if log_enable:
                    req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = log_logset_id
                req.LogConfig.TopicId = log_topic_id
            else:
                req.LogEnable = oldService.ServiceInfo.LogEnable
                if log_enable:
                    req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = oldService.ServiceInfo.LogConfig.LogsetId
                req.LogConfig.TopicId = oldService.ServiceInfo.LogConfig.TopicId

            req.ServiceAction = service_action
            if service_description is not None:
                req.ServiceDescription = service_description
            else:
                req.ServiceDescription = oldService.ServiceDescription

            if scale_strategy is not None:
                req.ScaleStrategy = scale_strategy
            else:
                req.ScaleStrategy = oldService.ServiceInfo.ScaleStrategy

            if cron_scale_jobs is not None:
                req.CronScaleJobs = cron_scale_jobs
            else:
                req.CronScaleJobs = oldService.ServiceInfo.CronScaleJobs

            print(req._serialize())
            return self._tione_client.ModifyModelService(req)
        except TencentCloudSDKException as err:
            raise

    def scale_model_service(
        self,
        service_id,
        scale_mode="MANUAL",
        replicas=1,
        horizontal_pod_autoscaler=None,
        scale_strategy=None,
        cron_scale_jobs=None,
    ):
        """模型服务版本扩缩容

        :param service_id:                 服务版本id
        :type service_id:                  str
        :param scale_mode:                 扩缩容类型
        :type scale_mode:                  str
        :param replicas:                   实例数量
        :type replicas:                    int
        :param horizontal_pod_autoscaler:  自动伸缩信息
        :type horizontal_pod_autoscaler:   :class:`tikit.tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param scale_strategy:             自动伸缩策略
        :type scale_strategy:              str
        :param cron_scale_jobs:            自动伸缩策略配置 HPA
        :type cron_scale_jobs:             list of :class:`tikit.tencentcloud.tione.v20211111.models.CronScaleJob`
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`
        """

        try:
            req = models.ModifyModelServiceRequest()
            req.ServiceId = service_id
            req.ScaleMode = scale_mode
            req.Replicas = replicas
            req.HorizontalPodAutoscaler = horizontal_pod_autoscaler
            req.ServiceAction = "SCALE"
            req.ScaleStrategy = scale_strategy
            req.CronScaleJobs = cron_scale_jobs
            print(req._serialize())
            return self._tione_client.ModifyModelService(req)
        except TencentCloudSDKException as err:
            raise

    def describe_api_configs(
        self, service_group_id: str
    ) -> models.DescribeAPIConfigsResponse:
        """查看服务对应的API

        :param service_group_id: 服务id
        :type service_group_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeAPIConfigsResponse`
        """
        req = models.DescribeAPIConfigsRequest()
        f = models.Filter()
        f.Name = "ServiceGroupId"
        f.Values = [service_group_id]
        req.Filters = [f]
        try:
            return self._tione_client.DescribeAPIConfigs(req)
        except TencentCloudSDKException as err:
            raise

    def describe_service_call_info(
        self, service_group_id: str
    ) -> models.DescribeModelServiceCallInfoResponse:
        """查看服务对应的调用信息

        :param service_group_id: 服务id
        :type service_group_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoResponse`
        """
        req = models.DescribeModelServiceCallInfoRequest()
        req.ServiceGroupId = service_group_id
        try:
            return self._tione_client.DescribeModelServiceCallInfo(req)
        except TencentCloudSDKException as err:
            raise

    def get_model_service_summary(self):
        """查询所有服务的概要

        :return:
        :rtype: list
        """
        resp = self.describe_model_service_groups()
        if not resp.ServiceGroups:
            return None
        svcs = []
        for group in resp.ServiceGroups:
            group_id = group.ServiceGroupId
            group_name = group.ServiceGroupName
            for svc in group.Services:
                svc_id = svc.ServiceId
                svc_desc = svc.ServiceDescription
                charge_type = svc.ChargeType
                svcs.append(
                    {
                        "Name": group_name,
                        "ServiceGroupId": group_id,
                        "ServiceId": svc_id,
                        "Description": svc_desc,
                        "ChargeType": charge_type,
                    }
                )
        return svcs

    def describe_model_service_groups(
        self,
        filters=None,
        order_field=None,
        order=None,
        offset=None,
        limit=None,
        tag_filters=None,
    ):
        """查看所有在线推理服务

        :param filters: 过滤器
        :type filters: list of Filter
        :param order_field: 排序字段
        :type order_field: str
        :param order: 排序方式，ASC/DESC
        :type order: str
        :param offset: 偏移量
        :type offset: int
        :param limit: 返回结果数量
        :type limit: int
        :param tag_filters: 标签过滤
        :type tag_filters: list of TagFilter
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsResponse`
        """
        try:
            req = models.DescribeModelServiceGroupsRequest()
            req.Filters = filters
            req.OrderField = order_field
            req.Order = order
            req.Offset = offset
            req.Limit = limit
            req.TagFilters = tag_filters
            return self._tione_client.DescribeModelServiceGroups(req)
        except TencentCloudSDKException as err:
            raise

    def describe_model_service_group(self, service_group_id):
        """查寻单个服务

        :param service_group_id: 服务id
        :type service_group_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelServiceGroupResponse`
        """
        try:
            req = models.DescribeModelServiceGroupRequest()
            req.ServiceGroupId = service_group_id
            return self._tione_client.DescribeModelServiceGroup(req)
        except TencentCloudSDKException as err:
            raise

    def describe_model_services(
        self,
        filters=None,
        order_field=None,
        order=None,
        offset=None,
        limit=None,
        tag_filters=None,
    ):
        """查询多个服务版本

        :param filters: 过滤器
        :type filters: list of Filter
        :param order_field: 排序字段
        :type order_field: str
        :param order: 排序方式，ASC/DESC
        :type order: str
        :param offset: 偏移量
        :type offset: int
        :param limit: 返回结果数量
        :type limit: int
        :param tag_filters: 标签过滤
        :type tag_filters: list of TagFilter
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelServicesResponse`
        """
        try:
            req = models.DescribeModelServicesRequest()
            req.Filters = filters
            req.OrderField = order_field
            req.Order = order
            req.Offset = offset
            req.Limit = limit
            req.TagFilters = tag_filters
            return self._tione_client.DescribeModelServices(req)
        except TencentCloudSDKException as err:
            raise

    def describe_model_service(self, service_id):
        """查询单个服务版本

        :param service_id: 服务版本id
        :type service_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelServiceResponse`
        """
        try:
            req = models.DescribeModelServiceRequest()
            req.ServiceId = service_id
            return self._tione_client.DescribeModelService(req)
        except TencentCloudSDKException as err:
            raise

    def stop_model_service(self, service_id: str):
        """关闭服务版本

        :param service_id: 服务版本id
        :type service_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`
        """
        try:
            return self.modify_model_service(
                service_id=service_id, service_action="STOP"
            )
        except TencentCloudSDKException as err:
            raise

    def start_model_service(self, service_id):
        """启动已经关闭的服务版本

        :param service_id: 服务版本id
        :type service_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`
        """
        try:
            return self.modify_model_service(
                service_id=service_id, service_action="RESUME"
            )
        except TencentCloudSDKException as err:
            raise

    def delete_model_service(self, service_id):
        """删除已经关闭的服务版本

        :param service_id: 服务版本id
        :type service_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteModelServiceResponse`
        """
        try:
            req = models.DeleteModelServiceRequest()
            req.ServiceId = service_id
            return self._tione_client.DeleteModelService(req)
        except TencentCloudSDKException as err:
            raise

    def delete_model_service_group(self, service_group_id):
        """删除服务

        :param service_group_id: 服务id
        :type service_group_id: str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteModelServiceGroupResponse`
        """
        try:
            req = models.DeleteModelServiceGroupRequest()
            req.ServiceGroupId = service_group_id
            return self._tione_client.DeleteModelServiceGroup(req)
        except TencentCloudSDKException as err:
            raise

    def modify_service_group_weights(self, service_group_id, service_id_to_weight):
        """更改服务的权重分配

        :param service_group_id: 服务id
        :type service_group_id: str
        :param service_id_to_weight: 服务版本id与权重对
        :type service_id_to_weight: dict
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsResponse`
        """
        try:
            req = models.ModifyServiceGroupWeightsRequest()
            req.ServiceGroupId = service_group_id
            req.Weights = []
            for service_id, weight in service_id_to_weight.items():
                entry = models.WeightEntry()
                entry.ServiceId = service_id
                entry.Weight = weight
                req.Weights.append(entry)
            return self._tione_client.ModifyServiceGroupWeights(req)
        except TencentCloudSDKException as err:
            raise

    def get_service_group_id_by_name(self, name: str) -> str:
        """根据服务名字查询服务ID

        :param name: 服务名字
        :type order: str
        :return:
        :rtype: str
        """
        if not name:
            raise ValueError("name should not be empty")
        f = models.Filter()
        f.Name = "ServiceGroupName"
        f.Values = [name]
        resp = self.describe_model_service_groups(filters=[f])
        if len(resp.ServiceGroups) > 1:
            raise ValueError(
                f"name should be unique, but {len(resp.ServiceGroups)} service groups found"
            )
        if len(resp.ServiceGroups) == 1:
            return resp.ServiceGroups[0].ServiceGroupId
        return name

    def describe_infer_templates(self) -> models.DescribeInferTemplatesResponse:
        """查询推理框架信息

        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeInferTemplatesResponse`
        """
        try:
            req = models.DescribeInferTemplatesRequest()
            return self._tione_client.DescribeInferTemplates(req)
        except TencentCloudSDKException as err:
            raise

    def describe_reasoning_env(self) -> models.DescribeInferTemplatesResponse:
        """查询推理环境信息

        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeInferTemplatesResponse`
        """
        return self.describe_infer_templates()

    def get_service_id_by_name(self, name: str, version: str) -> str:
        """根据服务版本名字查询服务版本ID

        :param name: 服务版本名字
        :type order: str
        :return:
        :rtype: str
        """
        if not name:
            raise ValueError("name should not be empty")
        if not version:
            raise ValueError("version should not be empty")
        version = version.lstrip("vV")
        f = models.Filter()
        f.Name = "ServiceGroupName"
        f.Values = [name]
        resp = self.describe_model_services(filters=[f])
        if not resp.Services or len(resp.Services) == 0:
            raise ValueError(f"no service found for {name}:{version})")
        service_id = ""
        for svc in resp.Services:
            if svc.Version == version:
                service_id = svc.ServiceId
                break
        if not service_id:
            raise ValueError(f"no service found for {name}:{version})")
        return service_id

    def start_training_task(self, task_id):
        """启动某个训练任务

        :param task_id: 训练任务ID
        :type task_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StartTrainingTaskResponse`
        """
        try:
            req = models.StartTrainingTaskRequest()
            req.Id = task_id
            return self._tione_client.StartTrainingTask(req)
        except TencentCloudSDKException as err:
            raise

    def get_client_info(self):
        return {
            "secret_id": self._secret_id,
            "secret_key": self._secret_key,
            "region": self._region,
            "tione_client": self._tione_client,
        }

    def describe_model_accelerate_tasks(
        self,
        filters=None,
        order_field=None,
        order=None,
        offset=None,
        limit=None,
        tag_filters=None,
    ):
        """查看加速任务列表

        :param filters:         过滤器
        :type filters:          list of Filter
        :param order_field:     排序字段
        :type order_field:      str
        :param order:           排序方式，ASC/DESC
        :type order:            str
        :param offset:          偏移量
        :type offset:           int
        :param limit:           返回结果数量
        :type limit:            int
        :param tag_filters:     标签过滤
        :type tag_filters:      list of TagFilter
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelAccelerateTasksResponse`

        """
        try:
            req = models.DescribeModelAccelerateTasksRequest()
            req.Filters = filters
            req.OrderField = order_field
            req.Order = order
            req.Offset = offset
            req.Limit = limit
            req.TagFilters = tag_filters
            return self._tione_client.DescribeModelAccelerateTasks(req)
        except TencentCloudSDKException as err:
            raise

    def _set_cos_input_path_info(self, req, model_input_path):
        if isinstance(model_input_path, str):
            req.ModelInputPath = self.parse_cos_info(model_input_path)
            return
        cos_path_info = models.CosPathInfo()
        cos_path_info.Bucket = model_input_path.Bucket
        cos_path_info.Region = model_input_path.Region
        cos_path_info.Paths = [model_input_path.Path]
        cos_path_info.Uin = model_input_path.Uin
        cos_path_info.SubUin = model_input_path.SubUin
        req.ModelInputPath = cos_path_info

    def create_notebook(
        self,
        name,
        image_info=None,
        resource_info=None,
        input_data_config=None,
        ssh_config=None,
        tags=None,
        resource_group_id="",
        lifecycle_script_id="",
        code_repo_id_list=None,
        auto_stop_enable=False,
        auto_stop_time=None,
        log_enable=False,
        log_logset_id=None,
        log_topic_id=None,
        vpc_id=None,
        subnet_id=None,
    ):
        """创建Notebook实例
        :param name:        实例名称
        :type name:         str
        :param image_info:   实例镜像信息
        :type image_info:    :class:`tikit.models.ImageInfo`
        :param resource_info:     实例资源配置配置
        :type resource_info:      :class:`tikit.models.ResourceConfigInfo`
        :param input_data_config:   输入的存储信息
        :type input_data_config:    list or :class:`tikit.models.NotebookDataConfig`
        :param ssh_config:  ssh配置信息
        :type ssh_config:   :class:`tikit.models.SSHConfig`
        :param tags:                标签
        :type tags:                 list of :class:`tikit.tencentcloud.tione.v20211111.models.Tag`
        :param resource_group_id:   预付费的资源组id
        :type resource_group_id:    str
        :param lifecycle_script_id: 生命周期脚本id
        :type lifecycle_script_id:  str
        :param code_repo_id_list:   git存储库id列表
        :type code_repo_id_list:    list
        :param auto_stop_enable:    自动停止开关
        :type auto_stop_enable:     bool
        :param auto_stop_time:      自动停止时间，单位小时
        :type auto_stop_time:       int
        :param log_enable:          日志开关
        :type log_enable:           bool
        :param log_logset_id:       日志集id
        :type log_logset_id:        str
        :param log_topic_id:        日志的topic id
        :type log_topic_id:         str
        :param vpc_id:   挂载cfs或者turbofs时，需要打通的vpc_id
        :type vpc_id:    str
        :param subnet_id:   挂载cfs或者turbofs时，vpc下的subnet
        :type subnet_id:    str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`
        """
        try:
            req = models.CreateNotebookRequest()
            req.Name = name
            req.DirectInternetAccess = True
            req.Tags = tags
            req.RootAccess = True
            if vpc_id is not None:
                req.VpcId = vpc_id
            if subnet_id is not None:
                req.SubnetId = subnet_id

            # 构造ImageInfo参数
            req.ImageInfo = models.ImageInfo()
            req.ImageInfo.ImageId = image_info.ImageId
            req.ImageInfo.ImageName = image_info.ImageName
            req.ImageInfo.ImageType = image_info.ImageType
            req.ImageInfo.ImageUrl = image_info.ImageUrl
            req.ImageInfo.RegistryRegion = image_info.RegistryRegion
            req.ImageInfo.RegistryId = image_info.RegistryId

            if image_info.ImageType == "SYSTEM":
                req.ImageType = "SYSTEM"
            else:
                req.ImageType = "CUSTOM"

            # 设置资源
            req.ResourceGroupId = resource_group_id
            resource_conf = models.ResourceConf()
            resource_conf.Cpu = resource_info.Cpu
            resource_conf.Gpu = resource_info.Gpu
            resource_conf.Memory = resource_info.Memory
            resource_conf.GpuType = resource_info.GpuType
            resource_conf.InstanceType = resource_info.InstanceType
            req.ResourceConf = resource_conf
            req.ChargeType = resource_info.ChargeType
            if resource_info.ChargeType == "PREPAID" and resource_group_id is None:
                raise TencentCloudSDKException(message="please set resource group id")

            # 设置挂载
            if input_data_config is None:
                raise TencentCloudSDKException(
                    message="please configure at least one data config"
                )
            else:
                req.DataConfigs, req.VolumeSourceType = self._parse_notebook_input_data(
                    input_data_config
                )

            # 设置生命周期
            if lifecycle_script_id is not None:
                req.LifecycleScriptId = lifecycle_script_id

            # 设置Git存储
            if code_repo_id_list is not None:
                additional_code_repo_ids = []
                for i, git_repo_id in enumerate(code_repo_id_list):
                    if i == 1:
                        req.DefaultCodeRepoId = git_repo_id
                    else:
                        additional_code_repo_ids.append(git_repo_id)
                if len(additional_code_repo_ids) > 0:
                    req.AdditionalCodeRepoIds = additional_code_repo_ids

            # 设置自动停止
            req.AutoStopping = auto_stop_enable
            if auto_stop_enable:
                req.AutomaticStopTime = auto_stop_time

            # 设置日志
            req.LogEnable = log_enable
            if log_enable:
                req.LogConfig = models.LogConfig()
                req.LogConfig.LogsetId = log_logset_id
                req.LogConfig.TopicId = log_topic_id

            # 设置SSH配置
            if ssh_config is not None and ssh_config.Enable:
                req.SSHConfig = models.SSHConfig()
                req.SSHConfig.Enable = True
                req.SSHConfig.PublicKey = ssh_config.PublicKey

            return self._tione_client.CreateNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def modify_notebook(
        self,
        notebook_id,
        image_info=None,
        resource_info=None,
        input_data_config=None,
        ssh_config=None,
        resource_group_id=None,
        lifecycle_script_id=None,
        code_repo_id_list=None,
        auto_stop_enable=None,
        auto_stop_time=None,
        log_enable=None,
        log_logset_id=None,
        log_topic_id=None,
        vpc_id=None,
        subnet_id=None,
    ):
        """编辑Notebook实例
        :param notebook_id:  实例ID
        :type notebook_id:   str
        :param image_info:   实例镜像信息
        :type image_info:    :class:`tikit.models.ImageInfo`
        :param resource_info:     实例资源配置配置
        :type resource_info:      :class:`tikit.models.ResourceConfigInfo`
        :param input_data_config:   输入的存储信息
        :type input_data_config:    list or :class:`tikit.models.NotebookDataConfig`
        :param ssh_config:  ssh配置信息
        :type ssh_config:   :class:`tikit.models.SSHConfig`
        :param resource_group_id:   预付费的资源组id
        :type resource_group_id:    str
        :param lifecycle_script_id: 生命周期脚本id
        :type lifecycle_script_id:  str
        :param code_repo_id_list:   git存储库id列表
        :type code_repo_id_list:    list
        :param auto_stop_enable:    自动停止开关
        :type auto_stop_enable:     bool
        :param auto_stop_time:      自动停止时间，单位小时
        :type auto_stop_time:       int
        :param log_enable:          日志开关
        :type log_enable:           bool
        :param log_logset_id:       日志集id
        :type log_logset_id:        str
        :param log_topic_id:        日志的topic id
        :type log_topic_id:         str
        :param vpc_id:   挂载cfs或者turbofs时，需要打通的vpc_id
        :type vpc_id:    str
        :param subnet_id:   挂载cfs或者turbofs时，vpc下的subnet
        :type subnet_id:    str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`
        """
        try:
            rsp = self.describe_notebook(notebook_id=notebook_id)
            notebook_instance = rsp.NotebookDetail
            req = models.ModifyNotebookRequest()
            req.Id = notebook_id
            req.Name = notebook_instance.Name
            req.DirectInternetAccess = True
            req.Tags = notebook_instance.Tags
            req.RootAccess = True
            req.VpcId = notebook_instance.VpcId
            if vpc_id is not None:
                req.VpcId = vpc_id
            req.SubnetId = notebook_instance.SubnetId
            if subnet_id is not None:
                req.SubnetId = subnet_id

            # 构造ImageInfo参数
            req.ImageInfo = notebook_instance.ImageInfo
            if image_info is not None:
                req.ImageInfo.ImageName = image_info.ImageName
                req.ImageInfo.ImageType = image_info.ImageType
                req.ImageInfo.ImageUrl = image_info.ImageUrl
                req.ImageInfo.RegistryRegion = image_info.RegistryRegion
                req.ImageInfo.RegistryId = image_info.RegistryId
                if image_info.ImageType == "SYSTEM":
                    req.ImageType = "SYSTEM"
                else:
                    req.ImageType = "CUSTOM"

            # 设置资源
            req.ResourceGroupId = notebook_instance.ResourceGroupId
            if resource_group_id is not None:
                req.ResourceGroupId = resource_group_id
            req.ResourceConf = notebook_instance.ResourceConf
            if resource_info is not None:
                resource_conf = models.ResourceConf()
                resource_conf.Cpu = resource_info.Cpu
                resource_conf.Gpu = resource_info.Gpu
                resource_conf.Memory = resource_info.Memory
                resource_conf.GpuType = resource_info.GpuType
                resource_conf.InstanceType = resource_info.InstanceType
                req.ResourceConf = resource_conf
                req.ChargeType = resource_info.ChargeType
                if resource_info.ChargeType == "PREPAID" and resource_group_id is None:
                    raise TencentCloudSDKException(
                        message="please set resource group id"
                    )

            # 设置挂载
            req.DataConfigs = notebook_instance.DataConfigs
            if input_data_config is not None:
                req.DataConfigs, req.VolumeSourceType = self._parse_notebook_input_data(
                    input_data_config
                )

            # 设置生命周期
            req.LifecycleScriptId = notebook_instance.LifecycleScriptId
            if lifecycle_script_id is not None:
                req.LifecycleScriptId = lifecycle_script_id

            # 设置Git存储
            req.DefaultCodeRepoId = notebook_instance.DefaultCodeRepoId
            req.AdditionalCodeRepoIds = notebook_instance.AdditionalCodeRepoIds
            if code_repo_id_list is not None:
                if len(code_repo_id_list) > 0:
                    additional_code_repo_ids = []
                    for i, git_repo_id in enumerate(code_repo_id_list):
                        if i == 0:
                            req.DefaultCodeRepoId = git_repo_id
                        else:
                            additional_code_repo_ids.append(git_repo_id)
                    req.AdditionalCodeRepoIds = additional_code_repo_ids
                else:
                    req.DefaultCodeRepoId = ""
                    req.AdditionalCodeRepoIds = []

            # 设置自动停止
            req.AutoStopping = notebook_instance.AutoStopping
            req.AutomaticStopTime = notebook_instance.AutomaticStopTime
            if auto_stop_enable is not None:
                req.AutoStopping = auto_stop_enable
                if auto_stop_enable:
                    req.AutomaticStopTime = auto_stop_time
                else:
                    req.AutomaticStopTime = 0

            # 设置日志
            req.LogEnable = notebook_instance.LogEnable
            req.LogConfig = notebook_instance.LogConfig
            if log_enable is not None:
                req.LogEnable = log_enable
                req.LogConfig = models.LogConfig()
                if req.LogEnable:
                    req.LogConfig.LogsetId = log_logset_id
                    req.LogConfig.TopicId = log_topic_id
                else:
                    req.LogConfig.LogsetId = ""
                    req.LogConfig.TopicId = ""

            # 设置SSH配置
            req.SSHConfig = notebook_instance.SSHConfig
            if ssh_config is not None:
                req.SSHConfig = models.SSHConfig()
                req.SSHConfig.Enable = ssh_config.Enable
                req.SSHConfig.PublicKey = ssh_config.PublicKey

            return self._tione_client.ModifyNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def _parse_notebook_input_data(self, input_data_config):
        data_configs = []
        data_type = ""
        for input_data_item in input_data_config:
            data_config = self._convert_notebook_data_config(input_data_item)
            if not data_config:
                continue
            data_configs.append(data_config)
            data_type = input_data_item.DataSource
        return data_configs, data_type

    def _convert_notebook_data_config(self, input_data_item) -> models.DataConfig:
        data_config = models.DataConfig()
        data_config.DataSourceType = input_data_item.DataSource
        data_config.MappingPath = input_data_item.TargetPath
        if (
            input_data_item.DataSource == "CFS"
            or input_data_item.DataSource == "CFS_TURBO"
        ):
            assert input_data_item.CfsId
            data_config.CFSSource = models.CFSConfig()
            data_config.CFSSource.Id = input_data_item.CfsId
            data_config.CFSSource.Path = input_data_item.CfsPath
            data_config.DataSourceType = "CFS"
        elif (
            input_data_item.DataSource == "CLOUD_PREMIUM"
            or input_data_item.DataSource == "CLOUD_SSD"
        ):
            data_config.CBSSource = models.CBSConfig()
            assert input_data_item.VolumeSize
            data_config.CBSSource.VolumeSizeInGB = input_data_item.VolumeSize
        elif input_data_item.DataSource == "LOCAL_DISK":
            data_config.LocalDiskSource = models.LocalDisk()
            assert input_data_item.InstanceId
            data_config.LocalDiskSource.InstanceId = input_data_item.InstanceId
        elif input_data_item.DataSource == "GooseFS":
            data_config.GooseFSSource = models.GooseFS()
            assert input_data_item.GooseFSId
            assert input_data_item.GooseFSNameSpace
            data_config.GooseFSSource.Id = input_data_item.GooseFSId
            data_config.GooseFSSource.NameSpace = input_data_item.GooseFSNameSpace
            data_config.GooseFSSource.Path = input_data_item.GooseFSPath
        elif input_data_item.DataSource == "GooseFSx":
            data_config.GooseFSSource = models.GooseFS()
            assert input_data_item.GooseFSId
            data_config.GooseFSSource.Id = input_data_item.GooseFSId
            data_config.GooseFSSource.Path = input_data_item.GooseFSxPath
        else:
            print("warning! not supported DataSourceType", input_data_item.DataSource)
            return None
        return data_config

    def stop_notebook(self, notebook_id):
        """停止某个notebook实例

        :param notebook_id: notebookID
        :type notebook_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StopNotebookResponse`
        """
        try:
            if len(notebook_id.strip()) == 0:
                raise TencentCloudSDKException(
                    code="InvalidParameterValue", message="notebook id is empty"
                )

            req = models.StopNotebookRequest()
            req.Id = notebook_id
            return self._tione_client.StopNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def delete_notebook(self, notebook_id):
        """删除某个notebook实例

        :param notebook_id: notebookID
        :type notebook_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteNotebookResponse`
        """
        try:
            if len(notebook_id.strip()) == 0:
                raise TencentCloudSDKException(
                    code="InvalidParameterValue", message="notebook id is empty"
                )

            req = models.DeleteNotebookRequest()
            req.Id = notebook_id
            return self._tione_client.DeleteNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def start_notebook(self, notebook_id):
        """启动某个notebook实例

        :param notebook_id: notebookID
        :type notebook_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StartNotebookResponse`
        """
        try:
            if len(notebook_id.strip()) == 0:
                raise TencentCloudSDKException(
                    code="InvalidParameterValue", message="notebook id is empty"
                )

            req = models.StartNotebookRequest()
            req.Id = notebook_id
            return self._tione_client.StartNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def describe_notebooks(
        self,
        filters=None,
        tag_filters=None,
        offset=0,
        limit=10,
        order="DESC",
        order_field="UpdateTime",
    ):
        """获取notebook列表

        :param filters:     过滤器，eg：[{ "Name": "Status", "Values": ["Running"], "Fuzzy": False}]
        Name（名称）：notebook1，支持模糊匹配
        Id（notebook ID）：nb-123456789, 支持模糊匹配
        Status（状态）：Submitting / Starting / Running / Stopped / Stopping / Failed / SubmitFailed / ImageSaving
        ChargeType（计费类型）：PREPAID（预付费）/ POSTPAID_BY_HOUR（后付费）
        ChargeStatus（计费状态）：NOT_BILLING（未开始计费）/ BILLING（计费中）/ BILLING_STORAGE（存储计费中）/ARREARS_STOP（欠费停止）
        :type filters:      list of Filter
        :param tag_filters: 标签过滤器，eg：[{ "TagKey": "TagKeyA", "TagValue": ["TagValueA"] }]
        :type tag_filters:  list of TagFilter
        :param offset:      偏移量，默认为0
        :type offset:       int
        :param limit:       返回数量，默认为50
        :type limit:        int
        :param order:       输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列
        :type order:        str
        :param order_field: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type order_field:  str
        :return:
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeNotebooksResponse`
        """
        try:
            # 优化参数的显示
            req = models.DescribeNotebooksRequest()
            req.Filters = filters
            req.TagFilters = tag_filters
            req.Offset = offset
            req.Limit = limit
            req.Order = order
            req.OrderField = order_field
            return self._tione_client.DescribeNotebooks(req)
        except TencentCloudSDKException as err:
            raise

    def describe_notebook(self, notebook_id):
        """获取单个notebook任务信息

        :param notebook_id: notebookID
        :type notebook_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeNotebooksResponse`
        """
        try:
            # 优化参数的显示
            req = models.DescribeNotebookRequest()
            req.Id = notebook_id
            # TODO 优化显示结果
            return self._tione_client.DescribeNotebook(req)
        except TencentCloudSDKException as err:
            raise

    def describe_notebook_buildin_images(self):
        """获取单个notebook任务信息

        :param notebook_id: notebookID
        :type notebook_id: str
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBuildInImagesResponse`
        """
        try:
            # 优化参数的显示
            req = models.DescribeBuildInImagesRequest()
            imageFilter = {"Name": "Attr", "Values": ["DataPipeline"], "Negative": True}
            req.ImageFilters = [imageFilter]
            # TODO 优化显示结果
            return self._tione_client.DescribeBuildInImages(req)
        except TencentCloudSDKException as err:
            raise
