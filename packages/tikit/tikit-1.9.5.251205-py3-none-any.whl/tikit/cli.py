import json
import os

import click
from prettytable import PrettyTable

from .client import Client

cred_path = os.path.join(os.path.expanduser("~"), ".tikit/credential")


def pretty_print_dict_list(l):
    if not l:
        return None
    table = PrettyTable()
    cols = l[0].keys()
    for col in cols:
        table.add_column(col, [])
    for dct in l:
        table.add_row([dct.get(c, "") for c in cols])
    return table


@click.group()
def cli():
    pass


@cli.command("config", help="configure to access qcloud api")
@click.option("--secret_id", required=True, help="your secret id to access qcloud api")
@click.option(
    "--secret_key", required=True, help="your secret key to access qcloud api"
)
@click.option("--region", default="ap-guangzhou", help="your region name")
def config_create_cmd(secret_id, secret_key, region):
    cred_path_dir = os.path.dirname(cred_path)
    if not os.path.isdir(cred_path_dir):
        os.makedirs(cred_path_dir)
    obj = {}
    obj["secret_id"] = secret_id
    obj["secret_key"] = secret_key
    obj["region"] = region
    with open(cred_path, "w") as f:
        json.dump(obj, f, indent=2)
    click.echo(f"credential file saved to {cred_path}")


def init_client() -> Client:
    if not os.path.exists(cred_path):
        raise click.ClickException(
            'Please run "tikit config" to ' "configure the secret first"
        )
    with open(cred_path, "r") as f:
        cred = json.loads(f.read())
    return Client(cred["secret_id"], cred["secret_key"], region=cred["region"])


@cli.command("create", help="create tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.option(
    "--init_file", is_flag=True, default=False, help="create a config file template"
)
@click.option(
    "-f", "--filename", default="", help="that contains the configuration to create"
)
def create_cmd(resource, init_file, filename):
    client = init_client()
    if resource == "service":
        try:
            if init_file is True:
                # 生成描述模版文件
                filename = filename if filename != "" else "service-config.yaml"
                dirname = os.path.dirname(__file__)
                with open(
                    os.path.join(dirname, "templates", "service_config.yaml"), "r"
                ) as infile:
                    config_template = infile.read()
                with open(filename, "w") as outfile:
                    outfile.write(config_template)
            else:
                msg = client._create_model_service_from_file(filename)
                click.echo(msg)
        except Exception as e:
            raise e
            # raise click.ClickException(str(e))


@cli.command("update", help="update tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.option(
    "-f", "--filename", default="", help="that contains the configuration to create"
)
def update_cmd(resource, filename):
    client = init_client()
    if resource == "service":
        try:
            msg = client._modify_model_service_from_file(filename)
            click.echo(msg)
        except Exception as e:
            raise click.ClickException(str(e))


@cli.command("balance", help="balance the traffic")
@click.argument("name", metavar="<NAME>|<SERVICE_GROUP_ID>")
@click.argument("weights", nargs=2, metavar="<VERSION1>:<WEIGHT1> ...")
def balance_cmd(name, weights):
    if not weights:
        raise click.ClickException("weights shoud not be empty")
    m = {}
    import re

    for wei in weights:
        group = wei.split(":")
        if len(group) != 2:
            raise click.ClickException(f"{wei} is invalid, " f"it should be like v1:30")
        group[0] = re.sub("VERSION", "", group[0])
        group[0] = re.sub("version", "", group[0])
        m[group[0].lstrip("vV")] = int(group[1])
    try:
        client = init_client()
        service_group_id = client.get_service_group_id_by_name(name)
        mm = {}
        for v, w in m.items():
            mm[f"{service_group_id}-{v}"] = w
        resp = client.modify_service_group_weights(service_group_id, mm)
        click.echo(f"change weights succeeded: req_id = {resp.RequestId}")
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command("stop", help="stop tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.argument("name", metavar="<ID>|(<NAME>:<VERSION>)")
def stop_cmd(resource, name: str):
    client = init_client()
    if resource == "service":
        if ":" in name:
            group = name.split(":")
            if len(group) != 2:
                raise click.ClickException(
                    f"service name({name}) is invalid, " f"should be <NAME>:<VERSION>"
                )
            service_id = client.get_service_id_by_name(group[0], group[1])
        else:
            service_id = name
        try:
            msg = client.stop_model_service(service_id)
            click.echo(msg)
        except Exception as e:
            raise click.ClickException(str(e))


@cli.command("start", help="start tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.argument("name", metavar="<ID>|(<NAME>:<VERSION>)")
def start_cmd(resource, name: str):
    client = init_client()
    if resource == "service":
        if ":" in name:
            group = name.split(":")
            if len(group) != 2:
                raise click.ClickException(
                    f"service name({name}) is invalid, " f"should be <NAME>:<VERSION>"
                )
            service_id = client.get_service_id_by_name(group[0], group[1])
        else:
            service_id = name
        try:
            msg = client.start_model_service(service_id)
            click.echo(msg)
        except Exception as e:
            raise click.ClickException(str(e))


@cli.command("delete", help="delete tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.argument("name", metavar="<ID>|(<NAME>:<VERSION>)")
def delete_cmd(resource, name: str):
    client = init_client()
    if resource == "service":
        if ":" in name:
            group = name.split(":")
            if len(group) != 2:
                raise click.ClickException(
                    f"service name({name}) is invalid, " f"should be <NAME>:<VERSION>"
                )
            service_id = client.get_service_id_by_name(group[0], group[1])
        else:
            service_id = name
        try:
            msg = client.delete_model_service(service_id)
            click.echo(msg)
        except Exception as e:
            raise click.ClickException(str(e))


@cli.command("get", help="get info of tione resource")
@click.argument("resource", type=click.Choice(["service"]))
@click.argument("name", metavar="<ID>|(<NAME>:<VERSION>)", required=False)
def get_cmd(resource, name: str):
    client = init_client()
    if resource == "service":
        if not name:
            # 返回所有的服务列表
            svcs = client.get_model_service_summary()
            click.echo(pretty_print_dict_list(svcs))
            return
        if ":" in name:
            group = name.split(":")
            if len(group) != 2:
                raise click.ClickException(
                    f"service name({name}) is invalid, " f"should be <NAME>:<VERSION>"
                )
            service_id = client.get_service_id_by_name(group[0], group[1])
        else:
            service_id = name
        try:
            resp = client.describe_model_service(service_id)
            click.echo(resp)
        except Exception as e:
            raise click.ClickException(str(e))
