# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from tikit.tencentcloud.tione.v20211111 import models

def notebook_image_table(buildin_images_response):
    """

    :param buildin_images_response:
    :type buildin_images_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBuildInImagesResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "内置镜像ID","内置镜像名称"
    ]
    for image_info in buildin_images_response.BuildInImageInfos:
        table.add_row([
            image_info.ImageId,
            image_info.ImageName,
        ])

    table.align = 'l'
    return table


def notebook_image_str(self):
    return notebook_image_table(self).get_string()


def notebook_image_html(self):
    return notebook_image_table(self).get_html_string()


models.DescribeBuildInImagesResponse.__repr__ = notebook_image_str
models.DescribeBuildInImagesResponse._repr_html_ = notebook_image_html