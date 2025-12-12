# -*- coding: utf-8 -*-

import json
import logging
import pathlib

from .helper.baai_login import auth_user_login


logger = logging.getLogger(__name__)


def new_downloader(ak, sk):
    return Downloader(ak, sk)


class Downloader:
    def __init__(self, ak: str, sk: str):
        self.ak = ak
        self.sk = sk

        auth_user_login(self.ak, self.sk)

    @staticmethod
    def download(target_ids: str, save_path=".", output_type=None):
        import traceback

        try:

            from .baai_meta import meta_download
            from .baai_proc import proc_data

            from .baai_config import Application
            from .baai_downloader import save_remote_meta, read_remote_meta
            from .helper.baai_read import read_base_meta, read_local_meta
            from .baai_downloader_custom import executor_download
            from .process.handle import handle_single_data

            save_path_arg = cmd_args.save_path  # noqa
            executor_download(save_path_arg, dir_path="")

            # meta
            meta_path = pathlib.Path(save_path) / "meta" # noqa

            meta_list = meta_path.glob("*.bin")
            for idx, meta_file in enumerate(meta_list):
                print(f"{meta_file.absolute()}")
                if idx >= 5:
                    break

            config = Application()
            post_api = config.meta_download_api

            target_ids_arg = target_ids
            if not target_ids_arg:
                print("请提供目标id")
            target_ids = target_ids_arg.split(",")

            for target_id in target_ids:
                try:
                    req_data = {"app_scope": "jswx", "app_param": json.dumps({"taskIds": [target_id]})}
                    resp_meta_ = read_remote_meta(f"{post_api}", json=req_data)
                except AssertionError as e:
                    logger.error(e)
                    raise e
                else:
                    meta_part_path = meta_path / f"{target_id}.bin"
                    meta_data_part = resp_meta_.get("data").get("download_set")
                    if len(meta_data_part) != 0:
                        save_remote_meta(meta_part_path, meta_data_part)

            # down
            save_path_arg = cmd_args.save_path  # noqa
            executor_download(save_path_arg, dir_path="")

            # proc
            if not output_type:
                return

            save_path_arg = cmd_args.save_path  # noqa
            data_path =  pathlib.Path(save_path_arg) / "data"
            logw_path =  pathlib.Path(save_path_arg) / "log"
            proc_path =  pathlib.Path(save_path_arg) / "proc"
            proc_path.mkdir(parents=True, exist_ok=True)

            single_path = data_path / "data/contest"


            print("============output_type==============")
            print(f"output_type: {output_type}\n")

            try:
                handle_single_data(single_path, [], proc_path, True, logw_path, output_type)
            except Exception as e:
                print(e)

            print()
            print(f"数据保存目录: {proc_path.absolute()}")

        except Exception as e:
            print(e)
            traceback.print_exc()
