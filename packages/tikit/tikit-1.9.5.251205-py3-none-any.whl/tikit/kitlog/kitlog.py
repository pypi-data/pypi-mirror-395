import types
import os
import re
import shutil

from tikit.tencentcloud.tione.v20211111 import models

# 日志查询条数的最大值
LIMIT = 1000


class KitLog(object):
    
    def __init__(self, tione_client):
        self._tione_client = tione_client

    def save(self, path, compress=None, service=None, service_id=None, pod_name=None, start_time=None, end_time=None, order=None):
        # 安全处理 service_id 为空的情况
        base_dir = str(service_id) if service_id is not None else "unknown_service"

        # 创建唯一目标目录
        target_dir = os.path.join(path, base_dir)
        suffix = 1
        while os.path.exists(target_dir):
            target_dir = os.path.join(path, f"{base_dir}_{suffix}")
            suffix += 1
        os.makedirs(target_dir)

        # 准备文件句柄字典和文件名映射
        file_handles = {}
        sanitized_names = {}

        # 清理文件名非法字符的函数
        def sanitize_filename(name):
            return re.sub(r'[\\/*?:"<>|]', "_", name)

        try:
            # 初始化分页查询
            result = self.download(service, service_id, pod_name, start_time, end_time, LIMIT, order)

            # 处理时间格式（用于文件名）
            start_str = format_time_for_filename(start_time) if start_time else "None"
            end_str = format_time_for_filename(end_time) if end_time else "None"

            # 分页获取所有日志
            while result is not None and result.Content is not None:
                for log in result.Content:
                    # 获取Pod名称（处理空值）
                    pod = log.PodName.strip() if log.PodName and log.PodName.strip() else "unknown_pod"

                    # 清理特殊字符并创建唯一文件名
                    safe_pod = sanitize_filename(pod)
                    if safe_pod not in sanitized_names:
                        # 生成实际文件名（带时间范围）
                        filename = f"{safe_pod}-{start_str}-{end_str}.log"
                        sanitized_names[safe_pod] = filename
                        file_path = os.path.join(target_dir, filename)

                        # 以追加模式打开文件
                        file_handles[safe_pod] = open(file_path, "a", encoding="utf-8")

                    # 写入日志内容（确保每行一个日志）
                    if log.Message:
                        # 移除行尾换行符后添加统一换行
                        message = log.Timestamp + " " + log.Message.rstrip("\n") + "\n"
                        file_handles[safe_pod].write(message)

                # 获取下一页
                result = result.next()

        finally:
            # 确保所有文件句柄正确关闭
            for handle in file_handles.values():
                handle.close()
            # 新增的压缩功能
            if compress:
                # 创建压缩文件的路径
                compress_dir = os.path.dirname(target_dir)  # 上级目录
                compress_name = os.path.basename(target_dir)  # 目录名作为压缩文件名
                compress_path = os.path.join(compress_dir, compress_name)

                # 创建压缩文件
                shutil.make_archive(compress_path, 'zip', root_dir=compress_dir, base_dir=compress_name)

                # 移除原始文件夹
                shutil.rmtree(target_dir)
                print(f"已压缩日志文件到: {compress_path}.zip")

    def download(
        self,
        service=None,
        id=None,
        pod_name=None,
        start_time=None,
        end_time=None,
        limit=None,
        order=None,
        context=None,
    ):
        """下载日志文件到本地

        :param service: 下载哪种类型的日志。 TRAIN：训练任务； NOTEBOOK：Notebook服务； INFER：推理服务；
        :type service: str
        :param id: 业务的ID，即训练任务的ID:train-1400005989227889408、NOTEBOOK的ID:nb-1400149432817087744，或者在线服务的ID:ms-q4lt86ph-1
        :type id: str
        :param pod_name: 查询哪个Pod的日志，支持支持结尾通配符。查看某个训练任务的全部pod的日志可以填： "<task_id>*"，如：train-51cd6bf7ec1000*
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
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`

            返回的对象如果非空，就会有 next() 方法，能不断地获取下一页的日志（如果有多页的话），如下：
            now_time = datetime.datetime.now(datetime.timezone.utc)
            now_time_str = now_time.isoformat()
            result = client.download_logs("train-51cd6bf7ec1000-37c5p5nlr01s-launcher",
                                                "2021-12-10T09:32:03.823509+00:00",
                                                now_time_str,
                                                limit=30)
            print(result)
            print(result.next())
            print(result.next())
            print(result.next())

        """
        if order is None:
            order = "ASC"

        service_id = id
        if service == "TRAIN":
            train_req = models.DescribeTrainingTaskRequest()
            train_req.Id = id
            train_rsp = self._tione_client.DescribeTrainingTask(train_req)
            service_id = train_rsp.TrainingTaskDetail.LatestInstanceId
        elif service == "NOTEBOOK":
            notebook_req = models.DescribeNotebookRequest()
            notebook_req.Id = id
            notebook_rsp = self._tione_client.DescribeNotebook(notebook_req)
            service_id = notebook_rsp.NotebookDetail.PodName

        req = models.DescribeLogsRequest()
        req.Service = service
        req.ServiceId = service_id
        req.PodName = pod_name
        req.StartTime = start_time
        req.EndTime = end_time
        req.Limit = limit
        req.Order = order
        req.Context = context
        result = self._tione_client.DescribeLogs(req)

        def get_next_data(xx):
            if result.Context != "":
                next_result = self.download(
                    service,
                    service_id,
                    pod_name,
                    start_time,
                    end_time,
                    limit,
                    order,
                    result.Context,
                )
                result.Context = next_result.Context
                result.Content = next_result.Content
                result.RequestId = next_result.RequestId
                return result
            else:
                print("Download finished")
                return None

        result.next = types.MethodType(get_next_data, result)
        return result


def format_time_for_filename(time_str):
    if not time_str:
        return "None"
    # 移除时区信息和特殊字符，转换为YYYYMMDDHHMMSS格式
    return time_str[:19].replace("-", "").replace(":", "").replace("T", "")