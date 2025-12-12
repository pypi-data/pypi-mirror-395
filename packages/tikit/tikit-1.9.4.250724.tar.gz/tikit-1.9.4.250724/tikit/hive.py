# -*- coding: utf-8 -*-
import os
import random
import string
import json
import time
import jwt
import requests
import base64
import xml.etree.ElementTree as ET
import configparser
import re
import shutil

from pyhive import hive
from hdfs import Client as HdfsClient
from tikit.tencentcloud.wedata.v20210820 import wedata_client
from tikit.tencentcloud.wedata.v20210820 import models as wedata_models
from tikit.tencentcloud.emr.v20190103 import emr_client
from tikit.tencentcloud.emr.v20190103 import models as emr_models
from tikit.tencentcloud.common import credential
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from hdfs.ext.kerberos import KerberosClient
from tqdm import tqdm
from tikit.tencentcloud.tione.v20211111 import models

NONE = 0
KERBEROS = 1
LDAP = 2
SIMPLE = 3


def _get_tmp_path():
    """
    返回随机生成的hdfs临时目录
    :return:    临时目录
    :rtype:     str
    """
    folder = "".join(
        random.sample(string.ascii_letters + string.digits, random.randint(12, 20))
    )
    return "/tmp/tikit/%s" % folder


def _get_host_port(server):
    """
    把服务地址解析成主机地址和端口
    :param server:  服务地址
    :type server:   str
    :return:        主机地址和端口
    :rtype:         list
    """
    parts = server.split(":")
    if len(parts) != 2:
        raise Exception('invalid hive_server, should like "10.0.0.1:7001"')
    return parts


def upload_to_hive_by_hdfs(
    local_path,
    hdfs_url,
    hive_server,
    table_name,
    database="default",
    auth="CUSTOM",
    username=None,
    password=None,
    overwrite=False,
    partition="",
):
    """把本地文件的数据导入到hive表中，hdfs作为中间存储。
    过程：先把本地文件上传到hdfs上，然后再从hdfs文件导入到hive中。

    :param local_path:      本地文件或者文件夹。文件夹中不能包含子文件夹。
    :type local_path:       str
    :param hdfs_url:        webhdfs的url，如：http://10.0.3.16:4008
    :type hdfs_url:         str
    :param hive_server:     HiveServer2的地址
    :type hive_server:      str
    :param table_name:      Hive表的名称
    :type table_name:       str
    :param database:        数据库名称
    :type database:         str
    :param auth:            认证的方式
    :type auth:             str
    :param username:        数据库认证的用户名
    :type username:         str
    :param password:        数据库认证的密码
    :type password:         str
    :param overwrite:       是否删掉原来的数据
    :type overwrite:        bool
    :param partition:       分区的选择
    :type partition:        str
    :return:
    :rtype:
    """
    hdfs_path = hdfs_tmp_path = _get_tmp_path()
    hdfs_client = HdfsClient(hdfs_url)
    # 上传文件到一个不存在的目录（斜杠结尾）的时候，hdfs库会把目录当成最终文件
    if os.path.isfile(local_path):
        hdfs_path = os.path.join(hdfs_path, os.path.basename(local_path))
    hdfs_client.upload(hdfs_path, local_path)
    try:
        insert_hdfs_into_hive(
            hdfs_path,
            hive_server,
            table_name,
            database,
            auth,
            username,
            password,
            overwrite,
            partition,
        )
    finally:
        hdfs_client.delete(hdfs_tmp_path, True)


def insert_hdfs_into_hive(
    hdfs_path,
    hive_server,
    table_name,
    database="default",
    auth="CUSTOM",
    username=None,
    password=None,
    overwrite=False,
    partition="",
):
    """把hdfs的文件数据导入到hive表中。

    :param hdfs_path:       hdfs上的文件或者文件夹。文件夹中不能包含子文件夹。如：/tmp/file.csv
    :type hdfs_path:        str
    :param hdfs_url:        webhdfs的url，如：http://10.0.3.16:4008
    :type hdfs_url:         str
    :param hive_server:     HiveServer2的地址
    :type hive_server:      str
    :param table_name:      Hive表的名称
    :type table_name:       str
    :param database:        数据库名称
    :type database:         str
    :param auth:            认证的方式
    :type auth:             str
    :param username:        数据库认证的用户名
    :type username:         str
    :param password:        数据库认证的密码
    :type password:         str
    :param overwrite:       是否删掉原来的数据
    :type overwrite:        bool
    :param partition:       分区的选择
    :type partition:        str
    :return:
    :rtype:
    """
    hive_host, hive_port = _get_host_port(hive_server)
    with hive.Connection(
        host=hive_host,
        port=hive_port,
        database=database,
        username=username,
        password=password,
        auth=auth,
    ) as conn:
        with conn.cursor() as cursor:
            sql = "LOAD DATA INPATH '{}' {} INTO TABLE {} {}".format(
                hdfs_path,
                "OVERWRITE" if overwrite else "",
                table_name,
                "" if partition == "" else "PARTITION (%s)" % partition,
            )
            cursor.execute(sql)


# def export_csv_from_hive(local_path, hive_server, table_name="", sql="", database="default", auth="CUSTOM",
#                          username=None, password=None):
#     """把hive表的数据读出，写到本地的csv文件
#
#     :param local_path:      本地文件或者文件夹。文件夹中不能包含子文件夹。
#     :type local_path:       str
#     :param hive_server:     HiveServer2的地址
#     :type hive_server:      str
#     :param table_name:      Hive表的名称。sql设置时忽略此参数
#     :type table_name:       str
#     :param sql:             查数据sql语句。如：select * from t1
#     :type sql:              str
#     :param database:        数据库名称
#     :type database:         str
#     :param auth:            认证的方式
#     :type auth:             str
#     :param username:        数据库认证的用户名
#     :type username:         str
#     :param password:        数据库认证的密码
#     :type password:         str
#     :return:
#     :rtype:
#     """
#     if local_path.endswith("/") or os.path.isdir(local_path):
#         local_path = os.path.join(local_path, "result.csv")
#     if os.path.exists(local_path):
#         raise Exception('"%s" is already existed' % local_path)
#     local_dir = os.path.dirname(local_path)
#     if local_dir != "" and not os.path.exists(local_dir):
#         os.makedirs(local_dir)
#     # 支持table_name、sql两种方式，sql优先
#     if table_name == "" and sql == "":
#         raise Exception('"table_name" and "sql" cannot both be empty')
#     if sql == "":
#         sql = "SELECT * FROM %s" % table_name
#     # 读出表内容，写入到文件
#     hive_host, hive_port = _get_host_port(hive_server)
#     with hive.Connection(host=hive_host, port=hive_port, database=database,
#                          username=username, password=password, auth=auth) as conn:
#         with conn.cursor() as cursor, open(local_path, 'w') as f:
#             writer = csv.writer(f)
#             cursor.execute(sql)
#             # 测试过使用 cursor.fetchmany(10000)的方式，性能更差（1000万条数据，183M）
#             for row in cursor:
#                 writer.writerow(row)
#     return local_path


def export_from_hive_by_hdfs(
    local_path,
    hdfs_url,
    hive_server,
    table_name="",
    sql="",
    database="default",
    auth="CUSTOM",
    username=None,
    password=None,
    row_format="row format delimited fields terminated by ','",
):
    """导出hive表到本地上，hdfs作为中间存储。对于大文件，这种方式比直接从hive表写到本地的效率更高。
    过程：先把hive导出到hdfs上，然后再从hdfs下载文件到本地。

    :param local_path:      本地的目录
    :type local_path:       str
    :param hdfs_url:        webhdfs的url，如：http://10.0.3.16:4008
    :type hdfs_url:         str
    :param hive_server:     HiveServer2的地址
    :type hive_server:      str
    :param table_name:      Hive表的名称。sql设置时忽略此参数
    :type table_name:       str
    :param sql:             查数据sql语句。如：select * from t1
    :type sql:              str
    :param database:        数据库名称
    :type database:         str
    :param auth:            认证的方式
    :type auth:             str
    :param username:        数据库认证的用户名
    :type username:         str
    :param password:        数据库认证的密码
    :type password:         str
    :param row_format:      行的输出格式
    :type row_format:       str
    :return:
    :rtype:
    """
    if os.path.isfile(local_path):
        raise Exception('"local_path" cannot be file')
    tmp_path = _get_tmp_path()
    hdfs_path = os.path.join(tmp_path, "result")
    hdfs_client = HdfsClient(hdfs_url)
    save_hive_to_hdfs(
        hdfs_path,
        hive_server,
        table_name,
        sql,
        database,
        auth,
        username,
        password,
        row_format,
    )
    try:
        local_dir = os.path.dirname(local_path)
        if local_dir != "" and not os.path.exists(local_dir):
            os.makedirs(local_dir)
        return hdfs_client.download(hdfs_path, local_path)
    finally:
        hdfs_client.delete(hdfs_path, True)


def save_hive_to_hdfs(
    hdfs_path,
    hive_server,
    table_name="",
    sql="",
    database="default",
    auth="CUSTOM",
    username=None,
    password=None,
    row_format="row format delimited fields terminated by ','",
):
    """把hive表的数据导出到hdfs上

    :param hdfs_path:       目标hdfs的保存路径
    :type hdfs_path:        str
    :param hive_server:     HiveServer2的地址
    :type hive_server:      str
    :param table_name:      Hive表的名称。sql设置时忽略此参数
    :type table_name:       str
    :param sql:             查数据sql语句。如：select * from t1
    :type sql:              str
    :param database:        数据库名称
    :type database:         str
    :param auth:            认证的方式
    :type auth:             str
    :param username:        数据库认证的用户名
    :type username:         str
    :param password:        数据库认证的密码
    :type password:         str
    :param row_format:      行的输出格式
    :type row_format:       str
    :return:
    :rtype:
    """
    if table_name == "" and sql == "":
        raise Exception('"table_name" and "sql" cannot both be empty')
    hive_host, hive_port = _get_host_port(hive_server)
    with hive.Connection(
        host=hive_host,
        port=hive_port,
        database=database,
        username=username,
        password=password,
        auth=auth,
    ) as conn:
        with conn.cursor() as cursor:
            # INSERT OVERWRITE [LOCAL] DIRECTORY directory1 SELECT ... FROM ...
            if sql == "":
                execute_sql = (
                    "INSERT OVERWRITE DIRECTORY '{}' {} SELECT {} FROM {}".format(
                        hdfs_path, row_format, "*", table_name
                    )
                )
                cursor.execute(execute_sql)
            else:
                execute_sql = "INSERT OVERWRITE DIRECTORY '{}' {} {}".format(
                    hdfs_path, row_format, sql
                )
                cursor.execute(execute_sql)
    return hdfs_path


class HiveInitial(object):
    def __init__(self, client):
        self._client = client
        self._keytab = "/tmp/hive.keytab"
        self._hive_site = os.getenv("SPARK_HOME") + "/conf/hive-site.xml"
        self._hdfs_site = os.getenv("SPARK_HOME") + "/conf/hdfs-site.xml"
        self._core_site = os.getenv("SPARK_HOME") + "/conf/core-site.xml"
        self._yarn_site = os.getenv("SPARK_HOME") + "/conf/yarn-site.xml"
        self._krb_conf = "/etc/krb5.conf"
        self._jwt_key = "tbds@2022"
        self._wedata_auth_info = {}
        self._client_info = client.get_client_info()
        self._hive_conn_cache = {}

        for v in [self._hive_site, self._hdfs_site, self._core_site, self._yarn_site]:
            if os.path.exists(v):
                os.remove(v)

    def __del__(self):
        for v in self._hive_conn_cache:
            self._hive_conn_cache[v].close()

    def spark_hive_initial_wedata(self, wedata_id, source_account=None):
        """为spark初始化wedata hive（调用改方法后，就可以使用spark做hive操作）

        :param wedata_id:       wedata数据源id
        :type wedata_id:        int
        :param source_account:     如果hive为系统源，则需要传使用账户uin
        :type source_account:      str
        :rtype:
        """
        datasource_conn_info = self._get_wedata_security_auth_info(
            wedata_id, source_account
        )
        if datasource_conn_info["config_file_empty"]:
            raise Exception("Get hive-site.xml failed")
        if datasource_conn_info["auth_type"] == KERBEROS:
            self._init_kerberos_ticket(
                datasource_conn_info["principal"], datasource_conn_info["keytab"]
            )

    def hive_initial_wedata(self, wedata_id, source_account=None):
        """获取wedata hive连接句柄

        :param wedata_id:       wedata数据源id
        :type wedata_id:        int
        :param source_account:     如果hive为系统源，则需要传使用账户uin
        :type source_account:      str
        :rtype:
        """
        datasource_conn_info = self._get_wedata_security_auth_info(
            wedata_id, source_account
        )
        self._wedata_auth_info = datasource_conn_info

        if datasource_conn_info["auth_type"] == KERBEROS:
            self._init_kerberos_ticket(
                datasource_conn_info["principal"], datasource_conn_info["keytab"]
            )
            conn = hive.connect(
                host=datasource_conn_info["host"],
                port=datasource_conn_info["port"],
                auth="KERBEROS",
                kerberos_service_name=datasource_conn_info["username"],
            )
        elif datasource_conn_info["auth_type"] == LDAP:
            conn = hive.connect(
                host=datasource_conn_info["host"],
                port=datasource_conn_info["port"],
                auth="LDAP",
                username=datasource_conn_info["username"],
                password=datasource_conn_info["passwd"],
            )
        else:
            kwargs = {
                "host": datasource_conn_info["host"],
                "port": datasource_conn_info["port"],
            }
            if datasource_conn_info["username"]:
                kwargs["username"] = datasource_conn_info["username"]
            if datasource_conn_info["passwd"]:
                kwargs["password"] = datasource_conn_info["passwd"]
            if datasource_conn_info["username"] and datasource_conn_info["passwd"]:
                kwargs["auth"] = "CUSTOM"
            conn = hive.connect(**kwargs)
        self._hive_conn_cache[wedata_id] = conn
        return conn

    def spark_hive_initial(self, emr_id, username=None, keytab=None):
        """为spark初始化emr hive（调用改方法后，就可以使用spark做hive操作）

        :param emr_id:       腾讯云emr id
        :type emr_id:        str
        :param username:     如果使用kerberos认证，则需要传入对应用户名
        :type username:      str
        :param keytab:       keytab文件路径。如果使用集群默认账户（如hadoop），则需要提供keytab路径
        :type keytab:        str
        :rtype:
        """
        emr_conn_info = self._get_emr_security_auth_info(emr_id, username, keytab)
        if emr_conn_info["keytab"] != "":
            self._init_kerberos_ticket(username, emr_conn_info["keytab"])

    def hive_initial(self, emr_id, username=None, keytab=None):
        """获取emr hive连接句柄

        :param emr_id:       腾讯云emr id
        :type emr_id:        str
        :param username:     如果使用kerberos认证，则需要传入对应用户名
        :type username:      str
        :param keytab:       keytab文件路径。如果使用集群默认账户（如hadoop），则需要提供keytab路径
        :type keytab:        str
        :rtype:
        """
        emr_conn_info = self._get_emr_security_auth_info(emr_id, username, keytab)
        if emr_conn_info["principal"] != "":
            service_name = (emr_conn_info["principal"].split("@")[0]).split("/")[0]
            self._init_kerberos_ticket(username, emr_conn_info["keytab"])
            return hive.connect(
                host=emr_conn_info["host"],
                port=emr_conn_info["port"],
                auth="KERBEROS",
                kerberos_service_name=service_name,
            )
        else:
            return hive.connect(host=emr_conn_info["host"], port=emr_conn_info["port"])

    def hive_initial_custom(
        self,
        host=None,
        port=None,
        scheme=None,
        username=None,
        database="default",
        auth=None,
        configuration=None,
        kerberos_service_name=None,
        password=None,
        check_hostname=None,
        ssl_cert=None,
        thrift_transport=None,
    ):
        """Connect to HiveServer2

        :param host: What host HiveServer2 runs on
        :param port: What port HiveServer2 runs on. Defaults to 10000.
        :param auth: The value of hive.server2.authentication used by HiveServer2.
            Defaults to ``NONE``.
        :param configuration: A dictionary of Hive settings (functionally same as the `set` command)
        :param kerberos_service_name: Use with auth='KERBEROS' only
        :param password: Use with auth='LDAP' or auth='CUSTOM' only
        :param thrift_transport: A ``TTransportBase`` for custom advanced usage.
            Incompatible with host, port, auth, kerberos_service_name, and password.

        The way to support LDAP and GSSAPI is originated from cloudera/Impyla:
        https://github.com/cloudera/impyla/blob/255b07ed973d47a3395214ed92d35ec0615ebf62
        /impala/_thrift_api.py#L152-L160
        """
        return hive.connect(
            host=host,
            port=port,
            scheme=scheme,
            username=username,
            database=database,
            auth=auth,
            configuration=configuration,
            kerberos_service_name=kerberos_service_name,
            password=password,
            check_hostname=check_hostname,
            ssl_cert=ssl_cert,
            thrift_transport=thrift_transport,
        )

    def upload_to_wedata_hive(
        self,
        wedata_id,
        local_path,
        table_name,
        database="default",
        overwrite=False,
        partition="",
        source_account=None,
    ):
        """上传文件到wedata hive

        :param wedata_id:       wedata 数据源id
        :type wedata_id:        int
        :param local_path:     本地文件路径
        :type local_path:      str
        :param table_name:     表名
        :type local_path:      str
        :param database:     数据库
        :type database:      str
        :param overwrite:       是否删掉原来的数据
        :type overwrite:        bool
        :param partition:       分区的选择
        :type partition:        str
        :param source_account:     如果hive为系统源，则需要传使用账户uin
        :type source_account:      str
        :rtype:
        """
        conn = self._get_hive_conn_cache(wedata_id, source_account)
        size = os.stat(local_path).st_size

        with conn.cursor() as cursor:
            hdfs_client = self._get_hdfs_client()
            hdfs_path = os.path.join(_get_tmp_path(), "result")

            def progress_callback(name, bytes):
                pbar.update(2**16)

            with tqdm(total=size, unit="B", unit_scale=True) as pbar:
                pbar.set_description("Uploading")
                hdfs_client.upload(
                    hdfs_path, local_path, progress=progress_callback, overwrite=True
                )

            cursor.execute("USE " + database)
            sql = "LOAD DATA INPATH '{}' {} INTO TABLE {} {}".format(
                hdfs_path,
                "OVERWRITE" if overwrite else "",
                table_name,
                "" if partition == "" else "PARTITION (%s)" % partition,
            )
            print("导入hive中...")
            cursor.execute(sql)
            print("导入完成")

    def export_from_wedata_hive(
        self,
        wedata_id,
        local_path,
        table_name="",
        database="default",
        sql="",
        row_format="row format delimited fields terminated by ','",
        source_account=None,
    ):
        """导出wedata hive数据到本地

        :param wedata_id:       wedata 数据源id
        :type wedata_id:        int
        :param local_path:     本地文件路径
        :type local_path:      str
        :param table_name:     表名
        :type local_path:      str
        :param database:     数据库
        :type database:      str
        :param sql:             查数据sql语句。如：select * from t1
        :type sql:              str
        :param row_format:      行的输出格式
        :type row_format:       str
        :param source_account:     如果hive为系统源，则需要传使用账户uin
        :type source_account:      str
        :rtype:
        """
        conn = self._get_hive_conn_cache(wedata_id, source_account)
        with conn.cursor() as cursor:
            hdfs_client = self._get_hdfs_client()
            hdfs_path = os.path.join(_get_tmp_path(), table_name)

            cursor.execute("USE " + database)
            if sql == "":
                execute_sql = (
                    "INSERT OVERWRITE DIRECTORY '{}' {} SELECT {} FROM {}".format(
                        hdfs_path, row_format, "*", table_name
                    )
                )
            else:
                execute_sql = "INSERT OVERWRITE DIRECTORY '{}' {} {}".format(
                    hdfs_path, row_format, sql
                )
            print("导出到hdfs中...")
            cursor.execute(execute_sql)
            print("导出到hdfs完成")

            def progress_callback(name, bytes):
                pbar.update(2**16)

            with tqdm(
                total=hdfs_client.status(hdfs_path)["length"], unit="B", unit_scale=True
            ) as pbar:
                pbar.set_description("Downloading")
                hdfs_client.download(
                    hdfs_path, local_path, progress=progress_callback, overwrite=True
                )

    def _get_hive_conn_cache(self, wedata_id, source_account):
        # if wedata_id in self._hive_conn_cache:
        #     return self._hive_conn_cache[wedata_id]
        return self.hive_initial_wedata(wedata_id, source_account)

    def _get_hdfs_client(self):
        hdfs_address = []
        open_kerberos = False
        tree = ET.ElementTree(file=self._hdfs_site)
        root = tree.getroot()
        for v in root:
            if v[0].text.startswith("dfs.namenode.http-address"):
                hdfs_address.append("http://" + v[1].text)
            if v[0].text == "dfs.namenode.kerberos.principal":
                open_kerberos = True
                self._init_kerberos_ticket(
                    self._wedata_auth_info["principal"],
                    self._wedata_auth_info["keytab"],
                )

        if not hdfs_address[0]:
            raise Exception("get hdfs address error")

        if open_kerberos:
            client = KerberosClient(hdfs_address[0])
            return client

        client = HdfsClient(hdfs_address[0])
        return client

    def _get_emr_security_auth_info(self, emr_id, username, keytab=None):
        ret = {
            "host": "",
            "port": "",
            "principal": "",
            "keytab": "",
        }

        cred = credential.Credential(
            self._client_info["secret_id"], self._client_info["secret_key"]
        )
        client = emr_client.EmrClient(cred, self._client_info["region"])

        node_req = emr_models.DescribeClusterNodesRequest()
        node_req.InstanceId = emr_id
        node_req.NodeFlag = "master"
        node_rsp = client.DescribeClusterNodes(node_req)
        if not node_rsp.NodeList:
            raise Exception("Emr NodeList is empty")
        master_host = node_rsp.NodeList[-1].Ip

        conf_req = emr_models.DescribeServiceConfsRequest()
        conf_req.InstanceId = emr_id
        conf_rsp = client.DescribeServiceConfs(conf_req)
        hive_site = hdfs_site = core_site = yarn_site = {}
        for v in conf_rsp.ServiceConfList:
            tmp_param = json.loads(base64.b64decode(v.OriParam).decode("ascii"))

            if v.FileName == "hdfs-site.xml":
                for v1 in tmp_param:
                    hdfs_site[v1["Name"]] = v1["Value"]
                self._save_xml(hdfs_site, self._hdfs_site)
                continue

            if v.FileName == "core-site.xml":
                for v1 in tmp_param:
                    core_site[v1["Name"]] = v1["Value"]
                self._save_xml(core_site, self._core_site)
                continue

            if v.FileName == "yarn-site.xml":
                for v1 in tmp_param:
                    yarn_site[v1["Name"]] = v1["Value"]
                self._save_xml(yarn_site, self._yarn_site)
                continue

            if v.FileName == "hive-site.xml":
                for v1 in tmp_param:
                    hive_site[v1["Name"]] = v1["Value"]
                    if v1["Name"] == "hive.server2.thrift.bind.host":
                        ret["host"] = v1["Value"]
                    if v1["Name"] == "hive.server2.thrift.port":
                        ret["port"] = v1["Value"]
                    if v1["Name"] == "hive.server2.authentication.kerberos.principal":
                        ret["principal"] = v1["Value"]

                if ret["host"] == "emr-default":
                    ret["host"] = master_host
                    hive_site["hive.server2.thrift.bind.host"] = master_host
                    ret["principal"] = ret["principal"].replace("_HOST", master_host)

                self._save_xml(hive_site, self._hive_site)
                if (
                    "hive.server2.authentication" in hive_site
                    and hive_site["hive.server2.authentication"] == "kerberos"
                ):
                    if not username:
                        raise Exception(
                            "The authentication mode is Kerberos, username is required"
                        )
                    if (username and username in ["root", "hadoop"]) and not keytab:
                        raise Exception("The %s account must have a KeyTab" % username)
                    if keytab:
                        shutil.copyfile(keytab, self._keytab)
                    else:
                        keytab_req = emr_models.DescribeKeyTabFileRequest()
                        keytab_req.InstanceId = emr_id
                        keytab_req.UserName = username
                        keytab_rsp = client.DescribeKeyTabFile(keytab_req)

                        if not keytab_rsp.DownLoadUrl:
                            raise Exception("DownLoadUrl is empty")
                        download_rsp = requests.get(keytab_rsp.DownLoadUrl)
                        with open(self._keytab, "w") as f:
                            f.write(download_rsp.text)
                    ret["keytab"] = self._keytab

            if v.FileName == "krb5.conf":
                realm = kdc = admin_server = ""
                port = 88
                tmp_param = json.loads(base64.b64decode(v.OriParam).decode("ascii"))
                for v1 in tmp_param:
                    if v1["Name"] == "active_kdc_server_ip":
                        kdc = v1["Value"]
                    if v1["Name"] == "active_admin_server":
                        admin_server = v1["Value"]
                    if v1["Name"] == "realm":
                        realm = v1["Value"]
                    if v1["Name"] == "kdc_server_port":
                        port = v1["Value"]

                realms = """[realms]
    %s = {
        kdc = %s
        admin_server = %s
    }
[domain_realm]""" % (
                    realm.upper(),
                    kdc + ":" + port,
                    admin_server,
                )
                default_realm = "default_realm = " + realm.upper()

                with open(self._krb_conf, "r") as f:
                    krb5_content = f.read()

                with open(self._krb_conf, "r+") as f:
                    a = re.sub("default_realm =.*", default_realm, krb5_content)
                    b = re.sub("\[realms\][\s\S]*\[domain_realm\]", realms, a)
                    f.write(b)

        if not hive_site:
            raise Exception("hive-site.xml does not exist")
        return ret

    def _save_xml(self, data, file):
        self._crete_default_xml(file)
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        root.clear()
        for k in data:
            prop = ET.SubElement(root, "property")
            name = ET.SubElement(prop, "name")
            name.text = k
            val = ET.SubElement(prop, "value")
            val.text = data[k]
        tree.write(file)

    def _crete_default_xml(self, file):
        if not os.path.exists(file):
            r = ET.Element("configuration")
            t = ET.ElementTree(r)
            t.write(file)

    def _init_kerberos_ticket(self, principal, keytab):
        active_str = "kinit -kt {0} {1}".format(keytab, principal)
        if os.system(active_str) != 0:
            raise Exception("kinit error")

    def _get_wedata_security_auth_info(self, wedata_id, source_account):
        # 获取数据源信息
        datasource_rsp = self._call_inside_action(
            "DescribeDatasource", {"Id": wedata_id}
        )
        if (
            "Data" not in datasource_rsp["Response"]
            or not datasource_rsp["Response"]["Data"]
        ):
            raise Exception(datasource_rsp)
        if datasource_rsp["Response"]["Data"]["Type"] != "HIVE":
            raise Exception("datasource type is not HIVE")
        datasource = datasource_rsp["Response"]["Data"]
        params = datasource["Params"]

        # 自定义源
        if datasource["Category"] == "DB":
            custom_file_rsp = self._call_inside_action(
                "DescribeDataSourceConfigFiles", {"Id": wedata_id}
            )
            host, port, config_file_empty = self._save_config_files(
                custom_file_rsp, datasource["Category"]
            )

            if params["authentication"] == "none":
                return {
                    "host": params["ip"],
                    "port": params["port"],
                    "auth_type": NONE,
                    "keytab": "",
                    "principal": "",
                    "username": "hadoop",  # TODO 先默认使用hadoop用户
                    "passwd": "",
                    "config_file_empty": config_file_empty,
                }
            elif params["authentication"] == "Kerberos":
                return {
                    "host": host,
                    "port": port,
                    "auth_type": KERBEROS,
                    "keytab": self._keytab,
                    "principal": params["principal"],
                    "username": "hadoop",  # TODO 先默认使用hadoop用户
                    "passwd": "",
                    "config_file_empty": config_file_empty,
                }
            else:
                raise Exception("Unsupported custom source authentication method")

        # 系统源
        if source_account is None:
            raise Exception("Param source_account cannot be None")
        sys_conf_file_rsp = self._call_inside_action(
            "DescribeConfigFiles", {"ClusterId": datasource["ClusterId"]}
        )
        host, port, config_file_empty = self._save_config_files(
            sys_conf_file_rsp, datasource["Category"]
        )

        # 安全认证
        auth_rsp = self._call_inside_action(
            "QueryAccountMapping",
            {
                "clusterId": datasource["ClusterId"],
                "projectId": datasource["OwnerProjectId"],
                "sourceAccount": source_account,
            },
        )
        if "Data" not in auth_rsp or auth_rsp["Data"] is None:
            raise Exception(auth_rsp)
        auth_data = auth_rsp["Data"]

        if auth_data["authenticationType"] == KERBEROS:  # kerberos
            if auth_data["securityKey"] is None:
                raise Exception("keytab is empty")
            keytab = base64.b64decode(auth_data["securityKey"])
            with open(self._keytab, "w") as f:
                f.write(str(keytab))

        return {
            "host": host,
            "port": port,
            "auth_type": auth_data["authenticationType"],
            "keytab": self._keytab,
            "principal": auth_data["targetAccount"]
            + "@"
            + auth_data["clusterId"].upper(),
            "username": auth_data["targetAccount"],
            "passwd": auth_data["securityKey"],
            "config_file_empty": config_file_empty,
        }

    def _call_inside_action(self, action, payload):
        req = models.DescribeInsideActionRequest()
        req.ActionParam = action
        req.PayloadParam = base64.b64encode(json.dumps(payload).encode("utf-8")).decode(
            "ascii"
        )
        rsp = self._client_info["tione_client"].DescribeInsideAction(req)
        return json.loads(rsp.Data)

    def _save_config_files(self, config_file_rsp, category):
        if "Data" not in config_file_rsp["Response"]:
            raise Exception(config_file_rsp["Response"])
        config_file = config_file_rsp["Response"]["Data"]

        have_hive_site_file = have_hdfs_site_file = False
        have_krb5_conf_file = have_keytab_file = False
        for v in config_file:
            if v["ConfigFileName"].endswith("hive-site.xml"):
                with open(self._hive_site, "w") as f:
                    f.write(v["ConfigFileDetail"])
                have_hive_site_file = True
            if v["ConfigFileName"].endswith("hdfs-site.xml"):
                with open(self._hdfs_site, "w") as f:
                    f.write(v["ConfigFileDetail"])
                have_hdfs_site_file = True
            if v["ConfigFileName"].endswith("krb5.conf"):
                with open(self._krb_conf, "w") as f:
                    f.write(v["ConfigFileDetail"])
                have_krb5_conf_file = True
            if v["ConfigFileName"].endswith(".keytab"):
                with open(self._keytab, "wb") as f:
                    f.write(base64.b64decode(v["ConfigFileBaseDetail"]))
                have_keytab_file = True

        if not have_hive_site_file:
            raise Exception("Please upload hive-site.xml on the wedata page")
        if not have_hdfs_site_file:
            raise Exception("Please upload hdfs-site.xml on the wedata page")

        host = port = ""
        self._crete_default_xml(self._hive_site)
        tree = ET.ElementTree(file=self._hive_site)
        root = tree.getroot()
        for v in root:
            if v[0].text == "hive.server2.thrift.bind.host":
                host = v[1].text
            if v[0].text == "hive.server2.thrift.port":
                port = v[1].text
            if v[0].text == "hive.server2.authentication" and v[1].text == "kerberos":
                if not have_krb5_conf_file and category == "DB":
                    raise Exception("Please upload krb5.conf on the wedata page")
                if not have_keytab_file and category == "DB":
                    raise Exception("Please upload keytab on the wedata page")

        return host, port, config_file == "" or len(config_file) == 0

    def _get_wedata_jwt_token(self, jwt_payload):
        jwt_headers = {"typ": "JWT", "alg": "HS256"}
        jwt_token = "Bearer " + jwt.encode(
            payload=jwt_payload,
            key=self._jwt_key,
            algorithm="HS256",
            headers=jwt_headers,
        )
        return jwt_token
