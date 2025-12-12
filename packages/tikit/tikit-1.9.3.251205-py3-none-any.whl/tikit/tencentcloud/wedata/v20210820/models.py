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

import warnings

from tikit.tencentcloud.common.abstract_model import AbstractModel


class DataSourceInfo(AbstractModel):
    """数据源对象

    """

    def __init__(self):
        r"""
        :param DatabaseName: 若数据源列表为绑定数据库，则为db名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseName: str
        :param Description: 数据源描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param ID: 数据源ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ID: int
        :param Instance: 数据源引擎的实例ID，如CDB实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type Instance: str
        :param Name: 数据源名称，在相同SpaceName下，数据源名称不能为空
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Region: 数据源引擎所属区域
注意：此字段可能返回 null，表示取不到有效值。
        :type Region: str
        :param Type: 数据源类型:枚举值
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param ClusterId: 数据源所属的集群id
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        :param AppId: 应用ID AppId
注意：此字段可能返回 null，表示取不到有效值。
        :type AppId: int
        :param BizParams: 业务侧数据源的配置信息扩展
注意：此字段可能返回 null，表示取不到有效值。
        :type BizParams: str
        :param Category: 数据源类别：绑定引擎、绑定数据库
注意：此字段可能返回 null，表示取不到有效值。
        :type Category: str
        :param Display: 数据源展示名，为了可视化查看
注意：此字段可能返回 null，表示取不到有效值。
        :type Display: str
        :param OwnerAccount: 数据源责任人账号ID
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnerAccount: int
        :param Params: 数据源的配置信息，以JSON KV存储，根据每个数据源类型不同，而KV存储信息不同
注意：此字段可能返回 null，表示取不到有效值。
        :type Params: str
        :type ParamsString: str
        :param Status: 数据源数据源的可见性，1为可见、0为不可见。默认为1
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: int
        :param OwnerAccountName: 数据源责任人账号名称
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnerAccountName: str
        :param ClusterName: 集群名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterName: str
        :param OwnerProjectId: 归属项目ID
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnerProjectId: str
        :param OwnerProjectName: 归属项目Name
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnerProjectName: str
        :param OwnerProjectIdent: 归属项目标识
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnerProjectIdent: str
        :param AuthorityProjectName: 授权项目
注意：此字段可能返回 null，表示取不到有效值。
        :type AuthorityProjectName: str
        :param AuthorityUserName: 授权用户
注意：此字段可能返回 null，表示取不到有效值。
        :type AuthorityUserName: str
        :param Edit: 是否有编辑权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Edit: bool
        :param Author: 是否有授权权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Author: bool
        :param Deliver: 是否有转交权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Deliver: bool
        :param DataSourceStatus: 数据源状态
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSourceStatus: str
        """
        self.DatabaseName = None
        self.Description = None
        self.ID = None
        self.Instance = None
        self.Name = None
        self.Region = None
        self.Type = None
        self.ClusterId = None
        self.AppId = None
        self.BizParams = None
        self.Category = None
        self.Display = None
        self.OwnerAccount = None
        self.Params = None
        self.ParamsString = None
        self.Status = None
        self.OwnerAccountName = None
        self.ClusterName = None
        self.OwnerProjectId = None
        self.OwnerProjectName = None
        self.OwnerProjectIdent = None
        self.AuthorityProjectName = None
        self.AuthorityUserName = None
        self.Edit = None
        self.Author = None
        self.Deliver = None
        self.DataSourceStatus = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Description = params.get("Description")
        self.ID = params.get("ID")
        self.Instance = params.get("Instance")
        self.Name = params.get("Name")
        self.Region = params.get("Region")
        self.Type = params.get("Type")
        self.ClusterId = params.get("ClusterId")
        self.AppId = params.get("AppId")
        self.BizParams = params.get("BizParams")
        self.Category = params.get("Category")
        self.Display = params.get("Display")
        self.OwnerAccount = params.get("OwnerAccount")
        self.Params = params.get("Params")
        self.ParamsString = params.get("ParamsString")
        self.Status = params.get("Status")
        self.OwnerAccountName = params.get("OwnerAccountName")
        self.ClusterName = params.get("ClusterName")
        self.OwnerProjectId = params.get("OwnerProjectId")
        self.OwnerProjectName = params.get("OwnerProjectName")
        self.OwnerProjectIdent = params.get("OwnerProjectIdent")
        self.AuthorityProjectName = params.get("AuthorityProjectName")
        self.AuthorityUserName = params.get("AuthorityUserName")
        self.Edit = params.get("Edit")
        self.Author = params.get("Author")
        self.Deliver = params.get("Deliver")
        self.DataSourceStatus = params.get("DataSourceStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataSourceInfoPage(AbstractModel):
    """查询数据源分页列表

    """

    def __init__(self):
        r"""
        :param PageNumber: 分页页码
注意：此字段可能返回 null，表示取不到有效值。
        :type PageNumber: int
        :param PageSize: 分页大小
注意：此字段可能返回 null，表示取不到有效值。
        :type PageSize: int
        :param Rows: 数据源列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Rows: :class:`tikit.tencentcloud.wedata.v20210820.models.DataSourceInfo`
        :param TotalCount: 总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param TotalPageNumber: 总分页页码
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalPageNumber: int
        """
        self.PageNumber = None
        self.PageSize = None
        self.Rows = None
        self.TotalCount = None
        self.TotalPageNumber = None


    def _deserialize(self, params):
        self.PageNumber = params.get("PageNumber")
        self.PageSize = params.get("PageSize")
        if params.get("Rows") is not None:
            self.Rows = DataSourceInfo()
            self.Rows._deserialize(params.get("Rows"))
        self.TotalCount = params.get("TotalCount")
        self.TotalPageNumber = params.get("TotalPageNumber")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasourceBaseInfo(AbstractModel):
    """数据源对象

    """

    def __init__(self):
        r"""
        :param DatabaseNames: 若数据源列表为绑定数据库，则为db名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseNames: list of str
        :param Description: 数据源描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param ID: 数据源ID
        :type ID: int
        :param Instance: 数据源引擎的实例ID，如CDB实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type Instance: str
        :param Name: 数据源名称，在相同SpaceName下，数据源名称不能为空
        :type Name: str
        :param Region: 数据源引擎所属区域
注意：此字段可能返回 null，表示取不到有效值。
        :type Region: str
        :param Type: 数据源类型:枚举值
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param ClusterId: 数据源所属的集群id
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        """
        self.DatabaseNames = None
        self.Description = None
        self.ID = None
        self.Instance = None
        self.Name = None
        self.Region = None
        self.Type = None
        self.ClusterId = None


    def _deserialize(self, params):
        self.DatabaseNames = params.get("DatabaseNames")
        self.Description = params.get("Description")
        self.ID = params.get("ID")
        self.Instance = params.get("Instance")
        self.Name = params.get("Name")
        self.Region = params.get("Region")
        self.Type = params.get("Type")
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataSourceInfoListRequest(AbstractModel):
    """DescribeDataSourceInfoList请求参数结构体

    """

    def __init__(self):
        r"""
        :param ProjectId: 工作空间id
        :type ProjectId: str
        :param PageNumber: 页码
        :type PageNumber: int
        :param PageSize: 页数
        :type PageSize: int
        :param Filters: 可选过滤条件，Filter可选配置(参考): "Name": { "type": "string", "description": "数据源名称" }, "Type": { "type": "string", "description": "类型" }, "ClusterId": { "type": "string", "description": "集群id" }, "CategoryId": { "type": "string", "description": "分类，项目或空间id" }
        :type Filters: :class:`tikit.tencentcloud.wedata.v20210820.models.Filter`
        :param OrderFields: 排序配置
        :type OrderFields: :class:`tikit.tencentcloud.wedata.v20210820.models.OrderField`
        :param Type: 数据源类型
        :type Type: str
        :param DatasourceName: 数据源名称过滤用
        :type DatasourceName: str
        """
        self.ProjectId = None
        self.PageNumber = None
        self.PageSize = None
        self.Filters = None
        self.OrderFields = None
        self.Type = None
        self.DatasourceName = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.PageNumber = params.get("PageNumber")
        self.PageSize = params.get("PageSize")
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))
        if params.get("OrderFields") is not None:
            self.OrderFields = OrderField()
            self.OrderFields._deserialize(params.get("OrderFields"))
        self.Type = params.get("Type")
        self.DatasourceName = params.get("DatasourceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataSourceInfoListResponse(AbstractModel):
    """DescribeDataSourceInfoList返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 总条数。
        :type TotalCount: int
        :param DatasourceInfoSet: 数据源信息列表。
        :type DatasourceInfoSet: list of DatasourceBaseInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DatasourceInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DatasourceInfoSet") is not None:
            self.DatasourceInfoSet = []
            for item in params.get("DatasourceInfoSet"):
                obj = DatasourceBaseInfo()
                obj._deserialize(item)
                self.DatasourceInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataSourceListRequest(AbstractModel):
    """DescribeDataSourceList请求参数结构体

    """

    def __init__(self):
        r"""
        :param PageNumber: 页码
        :type PageNumber: int
        :param PageSize: 返回数量
        :type PageSize: int
        :param OrderFields: 排序配置
        :type OrderFields: list of OrderField
        :param Filters: 可选过滤条件，Filter可选配置(参考): "Name": { "type": "string", "description": "数据源名称" }, "Type": { "type": "string", "description": "类型" }, "ClusterId": { "type": "string", "description": "集群id" }, "CategoryId": { "type": "string", "description": "分类，项目或空间id" }
        :type Filters: list of Filter
        """
        self.PageNumber = None
        self.PageSize = None
        self.OrderFields = None
        self.Filters = None


    def _deserialize(self, params):
        self.PageNumber = params.get("PageNumber")
        self.PageSize = params.get("PageSize")
        if params.get("OrderFields") is not None:
            self.OrderFields = []
            for item in params.get("OrderFields"):
                obj = OrderField()
                obj._deserialize(item)
                self.OrderFields.append(obj)
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataSourceListResponse(AbstractModel):
    """DescribeDataSourceList返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 数据源列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: :class:`tikit.tencentcloud.wedata.v20210820.models.DataSourceInfoPage`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DataSourceInfoPage()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeDatasourceRequest(AbstractModel):
    """DescribeDatasource请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 对象唯一ID
        :type Id: int
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasourceResponse(AbstractModel):
    """DescribeDatasource返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 数据源对象
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: :class:`tikit.tencentcloud.wedata.v20210820.models.DataSourceInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DataSourceInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class Filter(AbstractModel):
    """通用过滤器

    """

    def __init__(self):
        r"""
        :param Name: 过滤字段名称
        :type Name: str
        :param Values: 过滤值列表
        :type Values: list of str
        """
        self.Name = None
        self.Values = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OrderField(AbstractModel):
    """通用排序字段

    """

    def __init__(self):
        r"""
        :param Name: 排序字段名称
        :type Name: str
        :param Direction: 排序方向：ASC|DESC
        :type Direction: str
        """
        self.Name = None
        self.Direction = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        