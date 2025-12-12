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


class CdbInfo(AbstractModel):
    """出参

    """

    def __init__(self):
        r"""
        :param InstanceName: 数据库实例
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param Ip: 数据库IP
注意：此字段可能返回 null，表示取不到有效值。
        :type Ip: str
        :param Port: 数据库端口
注意：此字段可能返回 null，表示取不到有效值。
        :type Port: int
        :param MemSize: 数据库内存规格
注意：此字段可能返回 null，表示取不到有效值。
        :type MemSize: int
        :param Volume: 数据库磁盘规格
注意：此字段可能返回 null，表示取不到有效值。
        :type Volume: int
        :param Service: 服务标识
注意：此字段可能返回 null，表示取不到有效值。
        :type Service: str
        :param ExpireTime: 过期时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireTime: str
        :param ApplyTime: 申请时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ApplyTime: str
        :param PayType: 付费类型
注意：此字段可能返回 null，表示取不到有效值。
        :type PayType: int
        :param ExpireFlag: 过期标识
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireFlag: bool
        :param Status: 数据库状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: int
        :param IsAutoRenew: 续费标识
注意：此字段可能返回 null，表示取不到有效值。
        :type IsAutoRenew: int
        :param SerialNo: 数据库字符串
注意：此字段可能返回 null，表示取不到有效值。
        :type SerialNo: str
        :param ZoneId: ZoneId
注意：此字段可能返回 null，表示取不到有效值。
        :type ZoneId: int
        :param RegionId: RegionId
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionId: int
        """
        self.InstanceName = None
        self.Ip = None
        self.Port = None
        self.MemSize = None
        self.Volume = None
        self.Service = None
        self.ExpireTime = None
        self.ApplyTime = None
        self.PayType = None
        self.ExpireFlag = None
        self.Status = None
        self.IsAutoRenew = None
        self.SerialNo = None
        self.ZoneId = None
        self.RegionId = None


    def _deserialize(self, params):
        self.InstanceName = params.get("InstanceName")
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        self.MemSize = params.get("MemSize")
        self.Volume = params.get("Volume")
        self.Service = params.get("Service")
        self.ExpireTime = params.get("ExpireTime")
        self.ApplyTime = params.get("ApplyTime")
        self.PayType = params.get("PayType")
        self.ExpireFlag = params.get("ExpireFlag")
        self.Status = params.get("Status")
        self.IsAutoRenew = params.get("IsAutoRenew")
        self.SerialNo = params.get("SerialNo")
        self.ZoneId = params.get("ZoneId")
        self.RegionId = params.get("RegionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodesRequest(AbstractModel):
    """DescribeClusterNodes请求参数结构体

    """

    def __init__(self):
        r"""
        :param InstanceId: 集群实例ID,实例ID形如: emr-xxxxxxxx
        :type InstanceId: str
        :param NodeFlag: 节点标识，取值为：
<li>all：表示获取全部类型节点，cdb信息除外。</li>
<li>master：表示获取master节点信息。</li>
<li>core：表示获取core节点信息。</li>
<li>task：表示获取task节点信息。</li>
<li>common：表示获取common节点信息。</li>
<li>router：表示获取router节点信息。</li>
<li>db：表示获取正常状态的cdb信息。</li>
<li>recyle：表示获取回收站隔离中的节点信息，包括cdb信息。</li>
<li>renew：表示获取所有待续费的节点信息，包括cdb信息，自动续费节点不会返回。</li>
注意：现在只支持以上取值，输入其他值会导致错误。
        :type NodeFlag: str
        :param Offset: 页编号，默认值为0，表示第一页。
        :type Offset: int
        :param Limit: 每页返回数量，默认值为100，最大值为100。
        :type Limit: int
        :param HardwareResourceType: 资源类型:支持all/host/pod，默认为all
        :type HardwareResourceType: str
        :param SearchFields: 支持搜索的字段
        :type SearchFields: list of SearchItem
        """
        self.InstanceId = None
        self.NodeFlag = None
        self.Offset = None
        self.Limit = None
        self.HardwareResourceType = None
        self.SearchFields = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.NodeFlag = params.get("NodeFlag")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.HardwareResourceType = params.get("HardwareResourceType")
        if params.get("SearchFields") is not None:
            self.SearchFields = []
            for item in params.get("SearchFields"):
                obj = SearchItem()
                obj._deserialize(item)
                self.SearchFields.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodesResponse(AbstractModel):
    """DescribeClusterNodes返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCnt: 查询到的节点总数
        :type TotalCnt: int
        :param NodeList: 节点详细信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type NodeList: list of NodeHardwareInfo
        :param TagKeys: 用户所有的标签键列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TagKeys: list of str
        :param HardwareResourceTypeList: 资源类型列表
注意：此字段可能返回 null，表示取不到有效值。
        :type HardwareResourceTypeList: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCnt = None
        self.NodeList = None
        self.TagKeys = None
        self.HardwareResourceTypeList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCnt = params.get("TotalCnt")
        if params.get("NodeList") is not None:
            self.NodeList = []
            for item in params.get("NodeList"):
                obj = NodeHardwareInfo()
                obj._deserialize(item)
                self.NodeList.append(obj)
        self.TagKeys = params.get("TagKeys")
        self.HardwareResourceTypeList = params.get("HardwareResourceTypeList")
        self.RequestId = params.get("RequestId")


class DescribeKeyTabFileRequest(AbstractModel):
    """DescribeKeyTabFile请求参数结构体

    """

    def __init__(self):
        r"""
        :param InstanceId: 集群实例ID
        :type InstanceId: str
        :param UserName: 用户名
        :type UserName: str
        """
        self.InstanceId = None
        self.UserName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeKeyTabFileResponse(AbstractModel):
    """DescribeKeyTabFile返回参数结构体

    """

    def __init__(self):
        r"""
        :param DownLoadUrl: 下载地址
注意：此字段可能返回 null，表示取不到有效值。
        :type DownLoadUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DownLoadUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DownLoadUrl = params.get("DownLoadUrl")
        self.RequestId = params.get("RequestId")


class DescribeServiceConfsRequest(AbstractModel):
    """DescribeServiceConfs请求参数结构体

    """

    def __init__(self):
        r"""
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param IpList: IP列表
        :type IpList: list of str
        :param ConfFileName: 文件名
        :type ConfFileName: str
        :param ServiceType: 服务类型
        :type ServiceType: int
        :param ConfGroupId: 配置组ID
        :type ConfGroupId: int
        """
        self.InstanceId = None
        self.IpList = None
        self.ConfFileName = None
        self.ServiceType = None
        self.ConfGroupId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.IpList = params.get("IpList")
        self.ConfFileName = params.get("ConfFileName")
        self.ServiceType = params.get("ServiceType")
        self.ConfGroupId = params.get("ConfGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeServiceConfsResponse(AbstractModel):
    """DescribeServiceConfs返回参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceConfList: 配置列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceConfList: list of ServiceConf
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceConfList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ServiceConfList") is not None:
            self.ServiceConfList = []
            for item in params.get("ServiceConfList"):
                obj = ServiceConf()
                obj._deserialize(item)
                self.ServiceConfList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUserManagerUserListRequest(AbstractModel):
    """DescribeUserManagerUserList请求参数结构体

    """

    def __init__(self):
        r"""
        :param InstanceId: 集群实例ID
        :type InstanceId: str
        :param PageNo: 页码
        :type PageNo: int
        :param PageSize: 分页的大小
        :type PageSize: int
        :param UserManagerFilter: 查询用户列表过滤器
        :type UserManagerFilter: :class:`tikit.tencentcloud.emr.v20190103.models.UserManagerFilter`
        """
        self.InstanceId = None
        self.PageNo = None
        self.PageSize = None
        self.UserManagerFilter = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")
        if params.get("UserManagerFilter") is not None:
            self.UserManagerFilter = UserManagerFilter()
            self.UserManagerFilter._deserialize(params.get("UserManagerFilter"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserManagerUserListResponse(AbstractModel):
    """DescribeUserManagerUserList返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserManagerUserList: 用户信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type UserManagerUserList: list of UserManagerUser
        :param TotalCnt: 总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCnt: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserManagerUserList = None
        self.TotalCnt = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("UserManagerUserList") is not None:
            self.UserManagerUserList = []
            for item in params.get("UserManagerUserList"):
                obj = UserManagerUser()
                obj._deserialize(item)
                self.UserManagerUserList.append(obj)
        self.TotalCnt = params.get("TotalCnt")
        self.RequestId = params.get("RequestId")


class MultiDiskMC(AbstractModel):
    """多云盘参数

    """

    def __init__(self):
        r"""
        :param Count: 该类型云盘个数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        :param Type: 磁盘类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: int
        :param Volume: 云盘大小
注意：此字段可能返回 null，表示取不到有效值。
        :type Volume: int
        """
        self.Count = None
        self.Type = None
        self.Volume = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Type = params.get("Type")
        self.Volume = params.get("Volume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeHardwareInfo(AbstractModel):
    """节点硬件信息

    """

    def __init__(self):
        r"""
        :param AppId: 用户APPID
注意：此字段可能返回 null，表示取不到有效值。
        :type AppId: int
        :param SerialNo: 序列号
注意：此字段可能返回 null，表示取不到有效值。
        :type SerialNo: str
        :param OrderNo: 机器实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type OrderNo: str
        :param WanIp: master节点绑定外网IP
注意：此字段可能返回 null，表示取不到有效值。
        :type WanIp: str
        :param Flag: 节点类型。0:common节点；1:master节点
；2:core节点；3:task节点
注意：此字段可能返回 null，表示取不到有效值。
        :type Flag: int
        :param Spec: 节点规格
注意：此字段可能返回 null，表示取不到有效值。
        :type Spec: str
        :param CpuNum: 节点核数
注意：此字段可能返回 null，表示取不到有效值。
        :type CpuNum: int
        :param MemSize: 节点内存
注意：此字段可能返回 null，表示取不到有效值。
        :type MemSize: int
        :param MemDesc: 节点内存描述
注意：此字段可能返回 null，表示取不到有效值。
        :type MemDesc: str
        :param RegionId: 节点所在region
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionId: int
        :param ZoneId: 节点所在Zone
注意：此字段可能返回 null，表示取不到有效值。
        :type ZoneId: int
        :param ApplyTime: 申请时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ApplyTime: str
        :param FreeTime: 释放时间
注意：此字段可能返回 null，表示取不到有效值。
        :type FreeTime: str
        :param DiskSize: 硬盘大小
注意：此字段可能返回 null，表示取不到有效值。
        :type DiskSize: str
        :param NameTag: 节点描述
注意：此字段可能返回 null，表示取不到有效值。
        :type NameTag: str
        :param Services: 节点部署服务
注意：此字段可能返回 null，表示取不到有效值。
        :type Services: str
        :param StorageType: 磁盘类型
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageType: int
        :param RootSize: 系统盘大小
注意：此字段可能返回 null，表示取不到有效值。
        :type RootSize: int
        :param ChargeType: 付费类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: int
        :param CdbIp: 数据库IP
注意：此字段可能返回 null，表示取不到有效值。
        :type CdbIp: str
        :param CdbPort: 数据库端口
注意：此字段可能返回 null，表示取不到有效值。
        :type CdbPort: int
        :param HwDiskSize: 硬盘容量
注意：此字段可能返回 null，表示取不到有效值。
        :type HwDiskSize: int
        :param HwDiskSizeDesc: 硬盘容量描述
注意：此字段可能返回 null，表示取不到有效值。
        :type HwDiskSizeDesc: str
        :param HwMemSize: 内存容量
注意：此字段可能返回 null，表示取不到有效值。
        :type HwMemSize: int
        :param HwMemSizeDesc: 内存容量描述
注意：此字段可能返回 null，表示取不到有效值。
        :type HwMemSizeDesc: str
        :param ExpireTime: 过期时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireTime: str
        :param EmrResourceId: 节点资源ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EmrResourceId: str
        :param IsAutoRenew: 续费标志
注意：此字段可能返回 null，表示取不到有效值。
        :type IsAutoRenew: int
        :param DeviceClass: 设备标识
注意：此字段可能返回 null，表示取不到有效值。
        :type DeviceClass: str
        :param Mutable: 支持变配
注意：此字段可能返回 null，表示取不到有效值。
        :type Mutable: int
        :param MCMultiDisk: 多云盘
注意：此字段可能返回 null，表示取不到有效值。
        :type MCMultiDisk: list of MultiDiskMC
        :param CdbNodeInfo: 数据库信息
注意：此字段可能返回 null，表示取不到有效值。
        :type CdbNodeInfo: :class:`tikit.tencentcloud.emr.v20190103.models.CdbInfo`
        :param Ip: 内网IP
注意：此字段可能返回 null，表示取不到有效值。
        :type Ip: str
        :param Destroyable: 此节点是否可销毁，1可销毁，0不可销毁
注意：此字段可能返回 null，表示取不到有效值。
        :type Destroyable: int
        :param Tags: 节点绑定的标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param AutoFlag: 是否是自动扩缩容节点，0为普通节点，1为自动扩缩容节点。
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoFlag: int
        :param HardwareResourceType: 资源类型, host/pod
注意：此字段可能返回 null，表示取不到有效值。
        :type HardwareResourceType: str
        :param IsDynamicSpec: 是否浮动规格，1是，0否
注意：此字段可能返回 null，表示取不到有效值。
        :type IsDynamicSpec: int
        :param DynamicPodSpec: 浮动规格值json字符串
注意：此字段可能返回 null，表示取不到有效值。
        :type DynamicPodSpec: str
        :param SupportModifyPayMode: 是否支持变更计费类型 1是，0否
注意：此字段可能返回 null，表示取不到有效值。
        :type SupportModifyPayMode: int
        :param RootStorageType: 系统盘类型
注意：此字段可能返回 null，表示取不到有效值。
        :type RootStorageType: int
        :param Zone: 可用区信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Zone: str
        :param SubnetInfo: 子网
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetInfo: :class:`tikit.tencentcloud.emr.v20190103.models.SubnetInfo`
        :param Clients: 客户端
注意：此字段可能返回 null，表示取不到有效值。
        :type Clients: str
        """
        self.AppId = None
        self.SerialNo = None
        self.OrderNo = None
        self.WanIp = None
        self.Flag = None
        self.Spec = None
        self.CpuNum = None
        self.MemSize = None
        self.MemDesc = None
        self.RegionId = None
        self.ZoneId = None
        self.ApplyTime = None
        self.FreeTime = None
        self.DiskSize = None
        self.NameTag = None
        self.Services = None
        self.StorageType = None
        self.RootSize = None
        self.ChargeType = None
        self.CdbIp = None
        self.CdbPort = None
        self.HwDiskSize = None
        self.HwDiskSizeDesc = None
        self.HwMemSize = None
        self.HwMemSizeDesc = None
        self.ExpireTime = None
        self.EmrResourceId = None
        self.IsAutoRenew = None
        self.DeviceClass = None
        self.Mutable = None
        self.MCMultiDisk = None
        self.CdbNodeInfo = None
        self.Ip = None
        self.Destroyable = None
        self.Tags = None
        self.AutoFlag = None
        self.HardwareResourceType = None
        self.IsDynamicSpec = None
        self.DynamicPodSpec = None
        self.SupportModifyPayMode = None
        self.RootStorageType = None
        self.Zone = None
        self.SubnetInfo = None
        self.Clients = None


    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.SerialNo = params.get("SerialNo")
        self.OrderNo = params.get("OrderNo")
        self.WanIp = params.get("WanIp")
        self.Flag = params.get("Flag")
        self.Spec = params.get("Spec")
        self.CpuNum = params.get("CpuNum")
        self.MemSize = params.get("MemSize")
        self.MemDesc = params.get("MemDesc")
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")
        self.ApplyTime = params.get("ApplyTime")
        self.FreeTime = params.get("FreeTime")
        self.DiskSize = params.get("DiskSize")
        self.NameTag = params.get("NameTag")
        self.Services = params.get("Services")
        self.StorageType = params.get("StorageType")
        self.RootSize = params.get("RootSize")
        self.ChargeType = params.get("ChargeType")
        self.CdbIp = params.get("CdbIp")
        self.CdbPort = params.get("CdbPort")
        self.HwDiskSize = params.get("HwDiskSize")
        self.HwDiskSizeDesc = params.get("HwDiskSizeDesc")
        self.HwMemSize = params.get("HwMemSize")
        self.HwMemSizeDesc = params.get("HwMemSizeDesc")
        self.ExpireTime = params.get("ExpireTime")
        self.EmrResourceId = params.get("EmrResourceId")
        self.IsAutoRenew = params.get("IsAutoRenew")
        self.DeviceClass = params.get("DeviceClass")
        self.Mutable = params.get("Mutable")
        if params.get("MCMultiDisk") is not None:
            self.MCMultiDisk = []
            for item in params.get("MCMultiDisk"):
                obj = MultiDiskMC()
                obj._deserialize(item)
                self.MCMultiDisk.append(obj)
        if params.get("CdbNodeInfo") is not None:
            self.CdbNodeInfo = CdbInfo()
            self.CdbNodeInfo._deserialize(params.get("CdbNodeInfo"))
        self.Ip = params.get("Ip")
        self.Destroyable = params.get("Destroyable")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoFlag = params.get("AutoFlag")
        self.HardwareResourceType = params.get("HardwareResourceType")
        self.IsDynamicSpec = params.get("IsDynamicSpec")
        self.DynamicPodSpec = params.get("DynamicPodSpec")
        self.SupportModifyPayMode = params.get("SupportModifyPayMode")
        self.RootStorageType = params.get("RootStorageType")
        self.Zone = params.get("Zone")
        if params.get("SubnetInfo") is not None:
            self.SubnetInfo = SubnetInfo()
            self.SubnetInfo._deserialize(params.get("SubnetInfo"))
        self.Clients = params.get("Clients")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchItem(AbstractModel):
    """搜索字段

    """

    def __init__(self):
        r"""
        :param SearchType: 支持搜索的类型
        :type SearchType: str
        :param SearchValue: 支持搜索的值
        :type SearchValue: str
        """
        self.SearchType = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.SearchType = params.get("SearchType")
        self.SearchValue = params.get("SearchValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceConf(AbstractModel):
    """服务配置

    """

    def __init__(self):
        r"""
        :param ServiceType: 组件类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceType: int
        :param SoftName: 组件名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SoftName: str
        :param FileName: 文件名
注意：此字段可能返回 null，表示取不到有效值。
        :type FileName: str
        :param FileConf: 文件属性
注意：此字段可能返回 null，表示取不到有效值。
        :type FileConf: str
        :param KeyConf: 关键字配置
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyConf: str
        :param OriParam: 文件参数
注意：此字段可能返回 null，表示取不到有效值。
        :type OriParam: str
        """
        self.ServiceType = None
        self.SoftName = None
        self.FileName = None
        self.FileConf = None
        self.KeyConf = None
        self.OriParam = None


    def _deserialize(self, params):
        self.ServiceType = params.get("ServiceType")
        self.SoftName = params.get("SoftName")
        self.FileName = params.get("FileName")
        self.FileConf = params.get("FileConf")
        self.KeyConf = params.get("KeyConf")
        self.OriParam = params.get("OriParam")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubnetInfo(AbstractModel):
    """子网信息

    """

    def __init__(self):
        r"""
        :param SubnetName: 子网信息（名字）
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetName: str
        :param SubnetId: 子网信息（ID）
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        """
        self.SubnetName = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.SubnetName = params.get("SubnetName")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """标签

    """

    def __init__(self):
        r"""
        :param TagKey: 标签键
        :type TagKey: str
        :param TagValue: 标签值
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserManagerFilter(AbstractModel):
    """用户管理列表过滤器

    """

    def __init__(self):
        r"""
        :param UserName: 用户名
注意：此字段可能返回 null，表示取不到有效值。
        :type UserName: str
        """
        self.UserName = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserManagerUser(AbstractModel):
    """用户管理列表信息（用户管理）

    """

    def __init__(self):
        r"""
        :param UserName: 用户名
注意：此字段可能返回 null，表示取不到有效值。
        :type UserName: str
        :param UserGroup: 用户组
注意：此字段可能返回 null，表示取不到有效值。
        :type UserGroup: str
        :param PassWord: 用户密码
注意：此字段可能返回 null，表示取不到有效值。
        :type PassWord: str
        :param ReMark: 备注
注意：此字段可能返回 null，表示取不到有效值。
        :type ReMark: str
        :param CAMUserName: CAM关联的用户名
注意：此字段可能返回 null，表示取不到有效值。
        :type CAMUserName: str
        :param CAMUserUin: 对应的账号UIN
注意：此字段可能返回 null，表示取不到有效值。
        :type CAMUserUin: str
        :param UserType: 用户类型，无需填写
注意：此字段可能返回 null，表示取不到有效值。
        :type UserType: str
        :param CreateTime: 创建时间，无需填写
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param SupportDownLoadKeyTab: 是否支持下载keytab
注意：此字段可能返回 null，表示取不到有效值。
        :type SupportDownLoadKeyTab: bool
        :param SupportModifyPwd: 是否支持修改密码
注意：此字段可能返回 null，表示取不到有效值。
        :type SupportModifyPwd: bool
        :param SupportDelete: 是否支持删除
注意：此字段可能返回 null，表示取不到有效值。
        :type SupportDelete: bool
        """
        self.UserName = None
        self.UserGroup = None
        self.PassWord = None
        self.ReMark = None
        self.CAMUserName = None
        self.CAMUserUin = None
        self.UserType = None
        self.CreateTime = None
        self.SupportDownLoadKeyTab = None
        self.SupportModifyPwd = None
        self.SupportDelete = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.UserGroup = params.get("UserGroup")
        self.PassWord = params.get("PassWord")
        self.ReMark = params.get("ReMark")
        self.CAMUserName = params.get("CAMUserName")
        self.CAMUserUin = params.get("CAMUserUin")
        self.UserType = params.get("UserType")
        self.CreateTime = params.get("CreateTime")
        self.SupportDownLoadKeyTab = params.get("SupportDownLoadKeyTab")
        self.SupportModifyPwd = params.get("SupportModifyPwd")
        self.SupportDelete = params.get("SupportDelete")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        