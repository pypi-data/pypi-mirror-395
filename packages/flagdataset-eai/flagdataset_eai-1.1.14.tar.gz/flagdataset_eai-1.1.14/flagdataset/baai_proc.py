# -*- coding: utf-8 -*-

from pathlib import Path


def proc_data(cmd_args, prefix_paths=None):
    from .process.handle import handle_single_data


    save_path_arg = cmd_args.save_path # noqa
    data_path = Path(save_path_arg) / "data"
    logw_path = Path(save_path_arg) / "log"
    proc_path = Path(save_path_arg) / "proc"
    proc_path.mkdir(parents=True, exist_ok=True)

    output_type = cmd_args.output_type

    if not output_type:
        return

    print("============output_type==============")
    print(f"output_type: {output_type}\n")


    if not prefix_paths:
        for tem_path in prefix_paths:
            single_path = data_path / tem_path
            try:
                handle_single_data(single_path, [], proc_path, True, logw_path, output_type)
            except Exception as e:
                print(e)
            pass
    else:
        single_path = data_path / "data/collect"
        try:
            handle_single_data(single_path, [], proc_path, True, logw_path, output_type)
        except Exception as e:
            print(e)


    print()
    print(f"数据保存目录: {proc_path.absolute()}")
