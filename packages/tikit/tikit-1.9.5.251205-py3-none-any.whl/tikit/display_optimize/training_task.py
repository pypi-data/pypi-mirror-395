# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from tikit.tencentcloud.tione.v20211111 import models


def framework_table(framework_response):
    """

    :param framework_response:
    :type framework_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "框架名称",
        "版本",
        "训练模式"
    ]
    for framework in framework_response.FrameworkInfos:
        for framework_version in framework.VersionInfos:
            table.add_row([
                framework.Name,
                "".join(framework_version.Environment),
                ", ".join(framework_version.TrainingModes)
            ])
    table.align = 'l'
    return table


def framework_str(self):
    return framework_table(self).get_string()


def framework_html(self):
    return framework_table(self).get_html_string()


def bill_specs_table(bill_specs_response):
    """

    :param bill_specs_response:
    :type bill_specs_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "配置名称",
        "描述",
        "每小时价格（单位：元）"
    ]
    for spec in bill_specs_response.Specs:
        table.add_row([
            spec.SpecName,
            spec.SpecAlias,
            spec.SpecId
        ])
    return table


def bill_specs_str(self):
    return bill_specs_table(self).get_string()


def bill_specs_html(self):
    return bill_specs_table(self).get_html_string()


def training_task_table(training_task_response):
    """

    :param training_task_response:
    :type training_task_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`
    :return:
    :rtype:
    """
    paid_dict = {
        "PREPAID": {"SW":"从CVM机器中选择","NORMAL":"从TIONE平台购买-包年包月"},
        "POSTPAID_BY_HOUR": {"NONE":"从TIONE平台购买-按量计费"}
    }
    table = PrettyTable()
    table.field_names = [
        "任务ID",
        "名称",
        "训练框架",
        "训练模式",
        "机器来源",
        "占用资源",
        "标签",
        "状态",
        "运行时长",
        "创建者",
        "创建时间",
        "训练开始时间",
        "更新时间"
    ]
    for task in training_task_response.TrainingTaskSet:
        if task.RuntimeInSeconds > 86400:
            time_str = "{}天{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 86400),
                                              int((task.RuntimeInSeconds % 86400) / 3600),
                                              int((task.RuntimeInSeconds % 3600) / 60),
                                              task.RuntimeInSeconds % 60)
        elif task.RuntimeInSeconds > 3600:
            time_str = "{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 3600),
                                           int((task.RuntimeInSeconds % 3600) / 60),
                                           task.RuntimeInSeconds % 60)
        else:
            time_str = "{}分{}秒".format(int(task.RuntimeInSeconds / 60), task.RuntimeInSeconds % 60)
        if len(task.FrameworkName) > 0:
            framework = "{}:{}".format(task.FrameworkName, task.FrameworkEnvironment)
        elif task.AIMarketTemplateId != "":
            framework="内置大模型"
        else:
            framework="自定义镜像"
        # 机器来源
        if task.ChargeType is not None and task.ResourceGroupSWType is not None:
            resourceType = paid_dict.get(task.ChargeType, {}).get(task.ResourceGroupSWType, "UnknownType")
        # 创建者名称
        if task.Uin == task.SubUin:
            subuin_name = task.Uin
        else :
            subuin_name = task.SubUinName
        subuin_name = "{}\n{}".format(subuin_name,task.SubUin)
        resource_info = ""
        if task.ResourceConfigInfos is not None:
            if isinstance(task.ResourceConfigInfos, list) and len(task.ResourceConfigInfos) > 0:
                    for rc in task.ResourceConfigInfos:
                        resource_info += "\n"
                        resource_info += "{} 算力规格:{}C{}G".format(rc.Role, 
                                                                   rc.Cpu/1000, 
                                                                   rc.Memory/1024) 
                        if rc.GpuType is not "":
                            gpu_info = "{}*{}".format(rc.GpuType, rc.Gpu/100)
                            resource_info += gpu_info
                            
        table.add_row([
            task.Id,
            task.Name,
            framework,
            task.TrainingMode,
            resourceType,
            resource_info,
            "\n".join(map(lambda x: "%s:%s" % (x.TagKey, x.TagValue), task.Tags)),
            task.Status,
            time_str,
            subuin_name,
            task.CreateTime,
            task.StartTime,
            task.UpdateTime
        ])
    return table

def pod_list_table(pod_response):
    """
    
    :param pod_response:
    :type pod_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "实例ID",
        "实例规格",
        "状态",
        "节点ID",
        "启动时间",
        "结束时间",
    ]
    for pod in pod_response.PodInfoList:
        resource_info = ""
        rc = pod.ResourceConfigInfo
        if  rc is not None:
            resource_info += "{} 算力规格:{}C{}G".format(rc.Role, 
                                                        rc.Cpu/1000, 
                                                        rc.Memory/1024) 
            if rc.GpuType is not "":
                gpu_info = "{}*{}".format(rc.GpuType, rc.Gpu/100)
                resource_info += gpu_info
        table.add_row([
            pod.Name,
            resource_info,
            pod.Status,
            pod.NodeId,
            pod.StartTime,
            pod.EndTime
        ])
    return table

def training_task_str(self):
    return training_task_table(self).get_string()


def training_task_html(self):
    return training_task_table(self).get_html_string()

def pod_list_str(self): 
    return pod_list_table(self).get_string()

def pod_list_html(self):
    return pod_list_table(self).get_string()

def log_table(log_response):
    """

    :param log_response:
    :type log_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "日志时间",
        "实例名称",
        "日志数据"
    ]
    for one_log in log_response.Content:
        table.add_row([
            one_log.Timestamp,
            one_log.PodName,
            one_log.Message
        ])
    table.align = 'l'
    return table


def log_str(self):
    return log_table(self).get_string()


def log_html(self):
    return log_table(self).get_html_string()

def params_str_to_dict(input_str):
    input_str = input_str.strip("\"")
    input_str = input_str.strip("{")
    input_str = input_str.strip("}")
    # Split the string into key-value pairs
    key_value_pairs = input_str.split(', ')
    # Create a dictionary from the key-value pairs
    result_dict = {}
    for pair in key_value_pairs:
        key, value = pair.split('=')
        result_dict[key] = value
    return result_dict

models.DescribeTrainingFrameworksResponse.__repr__ = framework_str
models.DescribeTrainingFrameworksResponse._repr_html_ = framework_html

models.DescribeBillingSpecsResponse.__repr__ = bill_specs_str
models.DescribeBillingSpecsResponse._repr_html_ = bill_specs_html

models.DescribeTrainingTasksResponse.__repr__ = training_task_str
models.DescribeTrainingTasksResponse._repr_html_ = training_task_html

models.DescribeLogsResponse.__repr__ = log_str
models.DescribeLogsResponse._repr_html_ = log_html

models.DescribeTrainingTaskPodsResponse.__repr__ = pod_list_str
models.DescribeTrainingTaskPodsResponse._repr_html_ = pod_list_html