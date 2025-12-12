# -*- coding: utf-8 -*-

import pathlib
import argparse

from ..baai_config import config_read

from ..helper.baai_update import run_update
from ..helper.baai_print import print_figlet
from ..baai_config import print_config, HOME
from ..helper.baai_logger import logger_init
from ..baai_environment import show_environment

def runcmd_option():

    root_parser = argparse.ArgumentParser(add_help=False)
    root_parser.add_argument('-t', '--save-path', type=str, default=".", help='保存路径(默认当前文件夹)')
    root_parser.add_argument('-w', '--workers-down', type=int, help='同时进行下载的文件的数量')
    root_parser.add_argument('-j', '--jobs-down', type=int, help='同时执行下载的下载器数量')
    root_parser.add_argument('-m', '--merges-down', type=int, help='执行合并的数量')
    root_parser.add_argument('--host', type=str, help='服务地址')
    root_parser.add_argument('--sign-download-api', type=str, help='sign-download-api')
    root_parser.add_argument('--meta-download-api', type=str, help='meta-download-api')
    root_parser.add_argument('--auth-login-api', type=str, help='auth-login-api')

    # flagdataset
    parser = argparse.ArgumentParser(prog='flagdataset', description="flagdataset 命令行工具: bf")
    subparsers = parser.add_subparsers(dest='command')

    # show
    show_parser = subparsers.add_parser('show', help='获取当前运行环境信息', parents=[root_parser])
    show_parser.set_defaults(func=show)

    auth_parser = subparsers.add_parser('auth', help='认证相关命令')
    auth_subparsers = auth_parser.add_subparsers(dest='auth_command')

    # auth login 子命令
    login_parser = auth_subparsers.add_parser('login', help='登录数据平台')
    login_parser.set_defaults(func=auth_login)

    # down
    down_parser = subparsers.add_parser('down', help='下载资源', parents=[root_parser])
    down_parser.add_argument('--target-name', type=str, default="default", help='目标ID名字')
    down_parser.add_argument('--target-ids', type=str, help='目标ID: 1,2,3,4')
    down_parser.add_argument('--output_type', type=str, default=None, help='output_type')
    down_parser.set_defaults(func=down)

    # meta
    meta_parser = subparsers.add_parser('meta', help='下载数据meta信息')
    meta_subparsers = meta_parser.add_subparsers(dest='meta_cmd')

    meta_desc_parse = meta_subparsers.add_parser('desc', help='查看数据集描述信息', parents=[root_parser])
    meta_desc_parse.set_defaults(func=meta_desc)

    meta_list_parse = meta_subparsers.add_parser('list', help='查看数据集列表', parents=[root_parser])
    meta_list_parse.add_argument('--grep', type=str, default="*", help='grep')
    meta_list_parse.add_argument('--line', type=int, default=100, help='line')
    meta_list_parse.set_defaults(func=meta_list_grep)

    # 数据处理 format
    proc_parser = subparsers.add_parser('proc', help='数据处理',  parents=[root_parser])
    proc_parser.add_argument('--output_type', type=str, default=None, help='output_type')
    proc_parser.set_defaults(func=proc_format)


    # 解析命令行参数
    cmd_args = parser.parse_args()

    run_update(cmd_args)

    # logger
    if hasattr(cmd_args, 'save_path'):
        logger_init(pathlib.Path(cmd_args.save_path)/"log")
    else:
        home_loggr = pathlib.Path(HOME) / "log"
        home_loggr.mkdir(parents=True, exist_ok=True)
        logger_init(home_loggr)

    if hasattr(cmd_args, 'func'):
        try:
            cmd_args.func(cmd_args)
        except Exception: # noqa
            pass
        except KeyboardInterrupt:
            print()
            pass
    else:
        parser.print_help()


def show(cmd_args):

    print_figlet()
    show_environment(cmd_args)


def auth_login(cmd_args):
    from ..helper.baai_login import auth_user_login

    print_figlet()

    config_default = config_read()

    ak = input(f"请输入ak[{config_default.get('ak', '-')}]: ") or config_default.get("ak")
    sk = input(f"请输入sk[{config_default.get('sk', '-')}]: ") or config_default.get("sk")

    try:
        resp_data = auth_user_login(ak, sk)
    except AssertionError as e:
        print(e)


def meta_desc(cmd_args):

    from ..baai_meta import meta_descript
    print_figlet()
    print_config()
    meta_descript(cmd_args)


def meta_list_grep(cmd_args):
    from ..baai_meta import meta_list

    print_figlet()
    print_config()

    meta_list(cmd_args)


def download(cmd_args):
    from ..baai_download import download_dataset

    print_figlet()
    print_config()
    print("------download---------")

    download_dataset(cmd_args)


def get(cmd_args):
    from ..baai_download import download_required

    print_figlet()
    print_config()
    print("------get---------")

    download_required(cmd_args)


def down(cmd_args):
    import traceback

    try:

        from ..baai_meta import meta_download
        from ..baai_download_custom import download_required
        from ..baai_proc import proc_data

        print_figlet()
        print_config()
        print("------download target---------")

        try:
            prefix_paths = meta_download(cmd_args)
        except Exception as e:
            print(e)
            return

        download_required(cmd_args)

        if cmd_args.output_type:
            proc_data(cmd_args, prefix_paths)
    except Exception as e:
        traceback.print_exc()
        print(e)


def proc_format(cmd_args):
    from ..baai_proc import proc_data

    print_figlet()
    print("------proc data---------")
    proc_data(cmd_args)
