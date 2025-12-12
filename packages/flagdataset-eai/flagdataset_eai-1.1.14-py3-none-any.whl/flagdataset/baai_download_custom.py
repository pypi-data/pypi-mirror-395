# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)


def download_required(cmd_args):
    from .baai_downloader_custom import executor_download

    save_path_arg = cmd_args.save_path # noqa
    executor_download(save_path_arg, dir_path="")
