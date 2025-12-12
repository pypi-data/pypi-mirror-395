import os
import logging
import numpy as np
import cv2
from tqdm import tqdm
import argparse
import json
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import re


from .data_utils.pose_transform import quat_to_6d, euler_to_6d, compute_d6_axis_angle_deltas
from .data_utils.action_token.action_chunk_to_fast_token import ActionChunkProcessor

## TODO 根据具体的相机数目和位置修改prompt对于视角的描述
PROMPT = [
    "You are controlling a Franka single-arm robot. Your task is to adjust the end effector (EEF) poses at 10Hz to complete a specified task. ",
    "You need to output control tokens that can be decoded into a 30×7 action sequence. ",
    "The sequence has 30 consecutive actions, each with 7 dimensions. ",
    "Each EEPose here includes 3 delta position(xyz) + 3 delta orientation(axis-angle) + 1 gripper(opening range)\n\n",
    "Your current visual inputs are: robot front image<image> and robot wrist image<image>\n",
    "Your specific task is: {lan}"
]

_TOKENIZER_CACHE: dict[int, ActionChunkProcessor] = {}


def get_tokenizer(max_len: int) -> ActionChunkProcessor:
    """Return a cached ActionChunkProcessor (one per process).

    每个 Ray worker 进程各自维护 _TOKENIZER_CACHE，首次调用时才实例化。
    """
    tok = _TOKENIZER_CACHE.get(max_len)
    if tok is None:
        tok = ActionChunkProcessor(max_len=max_len)
        _TOKENIZER_CACHE[max_len] = tok
    return tok


def _to_serialisable(obj):
    """Convert numpy types to JSON-serialisable Python types."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    raise TypeError(f"Type {type(obj)} not serialisable")


def get_args(argv=None):  # 新增 argv 参数
    parser = argparse.ArgumentParser(description="轨迹数据处理参数")
    parser.add_argument("--data_path", type=str,
                        default='/share/project/dumengfei/code/corobot/刷透明试管_试用角色测试新建模版_346',
                        help='corobot data path')
    parser.add_argument("--output_data_path", type=str, default=f"/share/project/dumengfei/code/corobot/data_output",
                        help='output data path')
    parser.add_argument("--padding", type=int, default=0, help='padding size')
    parser.add_argument("--chunk", type=int, default=30, help='action chunk size')

    args = parser.parse_args(args=argv)  # 关键：允许传入外部参数列表
    return args


class AdvancedQuantileNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self, lower_quantile=0.01, upper_quantile=0.99,
                 target_range=(-1, 1), clip=True):
        """
        增强版分位数归一化器

        参数:
            lower_quantile: 下分位数(默认1%)
            upper_quantile: 上分位数(默认99%)
            target_range: 目标范围元组(默认[-1, 1])
            clip: 是否将超出范围的值裁剪到边界(默认True)
        """
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile
        self.target_min, self.target_max = target_range
        self.clip = clip
        self.quantiles_low_ = None
        self.quantiles_high_ = None
        self.scale_ = None
        self.offset_ = None

    def fit(self, X, y=None):
        """计算各维度的分位数和缩放参数"""
        X = np.asarray(X)
        self.quantiles_low_ = np.quantile(X, self.lower_quantile, axis=0)
        self.quantiles_high_ = np.quantile(X, self.upper_quantile, axis=0)

        # 计算缩放参数
        self.scale_ = (self.target_max - self.target_min) / (
            self.quantiles_high_ - self.quantiles_low_ + 1e-8)  # 避免除零
        self.offset_ = self.target_min - self.quantiles_low_ * self.scale_

        return {
            "quantiles_low_": self.quantiles_low_,
            "quantiles_high_": self.quantiles_high_,
            "scale_": self.scale_,
            "offset_": self.offset_
        }

    def transform(self, X):
        """应用归一化"""
        X = np.asarray(X)
        X_norm = X * self.scale_ + self.offset_

        if self.clip:
            np.clip(X_norm, self.target_min, self.target_max, out=X_norm)

        return X_norm

    def inverse_transform(self, X_norm):
        """反归一化"""
        X_norm = np.asarray(X_norm)
        return (X_norm - self.offset_) / self.scale_

    def get_feature_names(self):
        """获取特征名称(用于pipeline)"""
        return [f"norm_dim_{i}" for i in range(len(self.quantiles_low_))]


class CoRobot2Train:
    def __init__(self, args):
        """初始化轨迹处理器

        Args:
            args: 包含各种配置参数的对象
        """
        self.args = args
        self.normalizer = AdvancedQuantileNormalizer(
            lower_quantile=0.01,
            upper_quantile=0.99,
            target_range=(-1, 1)
        )

    def _load_normalization_parameters(self):
        """加载归一化参数"""
        with open(self.args.norm_path, 'r', encoding='utf-8') as f:
            norm_para = json.load(f)

        self.action_eepose_scale = np.array(norm_para["action.eepose"]['scale_'])  # delta
        self.action_eepose_offset = np.array(norm_para["action.eepose"]['offset_'])
        self.action_qpos_scale = np.array(norm_para["action.qpos"]['scale_'])  # delta
        self.action_qpos_offset = np.array(norm_para["action.qpos"]['offset_'])

    def transform(self, x: np.array, scale: np.array, offset: np.array, clip: bool = True) -> np.array:
        x_norm = x * scale + offset
        if clip:
            np.clip(x_norm, -1, 1, out=x_norm)
        return x_norm

    def inverse_transform(self, x_norm: np.array, scale: np.array, offset: np.array) -> np.array:
        x_norm = np.asarray(x_norm)
        return (x_norm - offset) / scale

    def save_video_frames(self, video_paths, output_dir, start_frame, end_frame, image_format: str = "jpg"):
        for video_path in video_paths:
            view_name = (
                f"{video_path.split('/')[-2].replace('.', '_')}"
            )

            if not os.path.exists(video_path):
                return 0

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return 0

            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for frame_idx in range(start_frame, end_frame + 1):
                ret, frame = cap.read()
                if not ret: break

                filename = f"{view_name}_{frame_idx}.{image_format}"
                output_path = os.path.join(output_dir, filename)
                if not os.path.exists(output_path):
                    resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(output_path, resized_frame)
            cap.release()

        return 1

    def compute_norm(self):
        action_qpos_list = []
        action_eepose_list = []
        state_eepose_list = []
        state_qpos_list = []

        for episode_i, episode_path in enumerate(self.all_episodes):
            df = pd.read_parquet(episode_path)

            action = df['action']
            state = df['observation.state']

            ## TODO 考虑到比赛使用的是Franka，理论上这里的样例维度和比赛采集的数据有所不同，这里只选用右手数据
            action_column_names = self.info["features"]["action"]["names"]
            state_column_names = self.info["features"]["observation.state"]["names"]
            eepose_target_names = [
                "main_follower_pose_x",
                "main_follower_pose_y",
                "main_follower_pose_z",
                "main_follower_rotation_euler_roll",
                "main_follower_rotation_euler_pitch",
                "main_follower_rotation_euler_yaw",
                "main_follower_gripper",  # main_follower_gripper_open
            ]
            qpos_target_names = [
                "main_follower_joint_1",
                "main_follower_joint_2",
                "main_follower_joint_3",
                "main_follower_joint_4",
                "main_follower_joint_5",
                "main_follower_joint_6",
                "main_follower_joint_7",
                "main_follower_gripper",  # main_follower_gripper_open
            ]

            ## compute delta action eepose
            ### 1, get absolute action eepose
            ### 2, transfer action eepose to delta action eepose
            #### (1) compute delta
            #### (2) transfer quat to delta axis angle
            target_eepose_indices = [action_column_names.index(dim) for dim in eepose_target_names]
            action_eepose = np.array(np.array([[lst[idx] for idx in target_eepose_indices] for lst in action]))
            action_eepose = np.concatenate(
                [
                    action_eepose[1:, :3] - action_eepose[:-1, :3],
                    compute_d6_axis_angle_deltas(euler_to_6d(action_eepose[:, 3:6])),
                    action_eepose[1:, [6]],
                ],
                axis=-1
            )
            ## xyz + delta axis angle + gripper = 7
            action_eepose_list.extend(action_eepose)

            ## compute delta action qpos
            ### 1, get absolute action qpos
            ### 2, transfer action qpos to delta action qpos
            #### (1) compute delta
            target_qpos_indices = [action_column_names.index(dim) for dim in qpos_target_names]
            action_qpos = np.array(np.array([[lst[idx] for idx in target_qpos_indices] for lst in action]))
            action_qpos = np.concatenate(
                [
                    action_qpos[1:, :7] - action_qpos[:-1, :7],
                    action_qpos[1:, [7]],
                ],
                axis=-1
            )
            ## joint7 + gripper = 8
            action_qpos_list.extend(action_qpos)

            ## compute state eepose
            ### 1, get state eepose
            ### 2, transfer state eepose
            #### (1) transfer quat to 6d
            target_eepose_indices = [state_column_names.index(dim) for dim in eepose_target_names]
            state_eepose = np.array([[lst[idx] for idx in target_eepose_indices] for lst in state])
            state_eepose = np.concatenate(
                [
                    state_eepose[1:, :3],
                    euler_to_6d(state_eepose[1:, 3:6]),
                    state_eepose[1:, [6]],
                ],
                axis=-1
            )
            ## xyz + 6d + gripper = 10
            state_eepose_list.extend(state_eepose)

            ## compute state qpos
            ### 1, get state qpos
            ### 2, transfer state
            target_qpos_indices = [state_column_names.index(dim) for dim in qpos_target_names]
            state_qpos = np.array([[lst[idx] for idx in target_qpos_indices] for lst in state])

            ## joint7 + gripper = 8
            state_qpos_list.extend(state_qpos)

        processed_data = {
            "action_eepose": np.array(action_eepose_list),
            "action_qpos": np.array(action_qpos_list),
            "state_eepose": np.array(state_eepose_list),
            "state_qpos": np.array(state_qpos_list)
        }
        norm_params = self.compute_normalization(processed_data)

        # 4. 保存归一化参数
        print("保存归一化参数...")
        with open(self.args.norm_path, "w", encoding="utf-8") as f:
            json.dump(norm_params, f, indent=4, ensure_ascii=False)
        print(f"归一化参数已保存至: {self.args.norm_path}")

    def compute_normalization(self, processed_data):
        """计算归一化参数"""
        result_dict = {}

        for key, data in processed_data.items():
            if data.size > 0:
                norm_params = self.normalizer.fit(data)
                result_dict[key.replace("_", ".")] = {k: _to_serialisable(v) for k, v in norm_params.items()}
            else:
                print(f"警告: {key}为空，跳过归一化拟合")
        return result_dict

    def is_video_valid(self, video_path):
        """检查视频文件是否可被 OpenCV 读取"""
        if not os.path.exists(video_path):
            return False
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False
        # 尝试读取 1 帧（避免读取整个文件）
        ret, _ = cap.read()
        cap.release()
        return ret

    def process_trajectory(self):
        action_tokenizer = get_tokenizer(max_len=256)
        for episode_i, episode_path in tqdm(enumerate(self.all_episodes)):
            try:
                try:
                    video_path = episode_path.replace('/data/', '/videos/').replace('.parquet', '.mp4')
                    image_names = ['observation.images.image_front', 'observation.images.image_wrist']
                    front_mp4_path, wrist_mp4_path = [
                        "/".join(video_path.split('/')[:-1] + [_] + video_path.split('/')[-1:]) for _ in image_names]
                    # cmd = ["ffmpeg", "-v", "error", "-i", front_mp4_path, "-f", "null", "-"]
                    # subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
                    # cmd = ["ffmpeg", "-v", "error", "-i", wrist_mp4_path, "-f", "null", "-"]
                    # subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
                    # 用轻量级校验替代 ffmpeg
                    if not self.is_video_valid(front_mp4_path) or not self.is_video_valid(wrist_mp4_path):
                        continue  # 无效文件跳过
                except:
                    continue
                df = pd.read_parquet(episode_path)
                action = df['action']
                state = df['observation.state']

                video_path = episode_path.replace('/data/', '/videos/').replace('.parquet', '.mp4')
                image_names = ['observation.images.image_front', 'observation.images.image_wrist']
                front_mp4_path, wrist_mp4_path = [
                    "/".join(video_path.split('/')[:-1] + [_] + video_path.split('/')[-1:]) for _ in image_names]
                ## TODO 考虑到比赛使用的是Franka，理论上这里的样例维度和比赛采集的数据有所不同，这里只选用右手数据
                action_column_names = self.info["features"]["action"]["names"]
                state_column_names = self.info["features"]["observation.state"]["names"]
                eepose_target_names = [
                    "main_follower_pose_x",
                    "main_follower_pose_y",
                    "main_follower_pose_z",
                    "main_follower_rotation_euler_roll",
                    "main_follower_rotation_euler_pitch",
                    "main_follower_rotation_euler_yaw",
                    "main_follower_gripper",  # main_follower_gripper_open
                ]
                qpos_target_names = [
                    "main_follower_joint_1",
                    "main_follower_joint_2",
                    "main_follower_joint_3",
                    "main_follower_joint_4",
                    "main_follower_joint_5",
                    "main_follower_joint_6",
                    "main_follower_joint_7",
                    "main_follower_gripper",  # main_follower_gripper_open
                ]

                ## compute delta action eepose
                ### 1, get absolute action eepose
                ### 2, transfer action eepose to delta action eepose
                #### (1) compute delta
                #### (2) transfer quat to delta axis angle
                target_eepose_indices = [action_column_names.index(dim) for dim in eepose_target_names]
                action_eepose = np.array(np.array([[lst[idx] for idx in target_eepose_indices] for lst in action]))

                ## compute delta action qpos
                ### 1, get absolute action qpos
                ### 2, transfer action qpos to delta action qpos
                #### (1) compute delta
                target_qpos_indices = [action_column_names.index(dim) for dim in qpos_target_names]
                action_qpos = np.array(np.array([[lst[idx] for idx in target_qpos_indices] for lst in action]))

                ## compute state eepose
                ### 1, get state eepose
                ### 2, transfer state eepose
                #### (1) transfer quat to 6d
                target_eepose_indices = [state_column_names.index(dim) for dim in eepose_target_names]
                state_eepose = np.array([[lst[idx] for idx in target_eepose_indices] for lst in state])
                state_eepose = np.concatenate(
                    [
                        state_eepose[1:, :3],
                        euler_to_6d(state_eepose[1:, 3:6]),
                        state_eepose[1:, [6]],
                    ],
                    axis=-1
                )

                ## compute state qpos
                ### 1, get state qpos
                ### 2, transfer state
                target_qpos_indices = [state_column_names.index(dim) for dim in qpos_target_names]
                state_qpos = np.array([[lst[idx] for idx in target_qpos_indices] for lst in state])

                uuid = f"{self.info['robot_type']}_{df['task_index'][0]}_{df['episode_index'][0]}"
                images_path = os.path.join(self.args.output_image_path, uuid)
                os.makedirs(images_path, exist_ok=True)

                ## directly use corobot record task name
                task_name_json = self.common_record['task_name'].split('_')[0]

                # 检查是否包含英文字母
                if re.search(r'[a-zA-Z]', task_name_json):
                    # 如果包含英文，提取开头的英文部分
                    match = re.match(r'^[a-zA-Z\s.]+', task_name_json)
                    raw_task = match.group() if match else task_name_json
                    sub_task = match.group() if match else task_name_json
                else:
                    # 如果不包含英文，直接使用原字符串
                    raw_task = task_name_json
                    sub_task = task_name_json

                ## split trajectory
                json_entries = []
                start = int(df['frame_index'][0])
                end = len(df['frame_index']) - 1
                construct_num = max(1, end + self.args.padding - self.args.chunk)

                ## save video frame
                result = self.save_video_frames(
                    video_paths=[front_mp4_path, wrist_mp4_path],
                    output_dir=images_path,
                    start_frame=start,
                    end_frame=end,
                    image_format="jpg",
                )
                if not result:
                    return []

                for i in range(construct_num):
                    # 选择分块索引 - 用min确保不超出边界
                    index = [min(i + j, end - 1) for j in range(self.args.chunk + 1)]
                    # 获取过滤后的数据块
                    action_eepose_chunk = action_eepose[index]
                    action_qpos_chunk = action_qpos[index]
                    state_eepose_chunk = state_eepose[index]
                    state_qpos_chunk = state_qpos[index]
                    # 计算delta – 确保形状匹配
                    try:
                        action_eepose_delta = np.concatenate(
                            [
                                action_eepose_chunk[1:, :3] - action_eepose_chunk[:-1, :3],
                                compute_d6_axis_angle_deltas(euler_to_6d(action_eepose_chunk[:, 3:6])),
                                action_eepose_chunk[1:, [6]],
                            ],
                            axis=-1,
                        )
                        action_qpos_delta = np.concatenate(
                            [
                                action_qpos_chunk[1:, :7] - action_qpos_chunk[:-1, :7],
                                action_qpos_chunk[1:, [7]],
                            ],
                            axis=-1,
                        )
                    except Exception as exc:
                        print("Failed to build action delta for item %s/%s – %s", uuid, i, exc)
                        continue

                    nor_action_delta = self.transform(action_eepose_delta, self.action_eepose_scale,
                                                      self.action_eepose_offset)
                    nor_action_qpos = self.transform(action_qpos_delta, self.action_qpos_scale, self.action_qpos_offset)

                    state_eepose_chunk = state_eepose_chunk[:-1]
                    state_qpos_chunk = state_qpos_chunk[:-1]
                    # 保存数组
                    # 保持0为关闭，大于1为打开
                    # 使用inverse的gripper动作作为action token
                    action_eepose_token = action_tokenizer.process_action_chunk_to_fast_token(nor_action_delta)
                    action_qpos_token = action_tokenizer.process_action_chunk_to_fast_token(nor_action_qpos)

                    image_path_list = [
                        os.path.join(images_path, f"{view}_{i}.jpg")
                        for view in ["observation_images_image_front", "observation_images_image_wrist"]
                    ]

                    # construct data item
                    action_str_list = ['<action_token>'] * 1
                    action_str = '<action_split>'.join(action_str_list)
                    json_item = {
                        "sample_id": f"{uuid}_{i}",
                        "raw_task": raw_task,
                        "task": sub_task,
                        "image": image_path_list,
                        "action_eepose_token": action_eepose_token,
                        "action_qpos_token": action_qpos_token,
                        "state": {
                            "eepose": state_eepose_chunk.tolist(),
                            "qpos": state_qpos_chunk.tolist(),
                        },
                        "action": {
                            "eepose": action_eepose_delta.tolist(),
                            "qpos": action_qpos_delta.tolist(),
                        },
                        "conversations": [
                            {
                                "from": "human",
                                "value": "".join(PROMPT).format(lan=sub_task.lower())
                            },
                            {
                                "from": "gpt",
                                "value": action_str
                            }
                        ]
                    }
                    json_entries.append(json_item)

                ## store training samples
                for json_item in json_entries:
                    json_line = json.dumps(json_item)
                    self.json_file_writer.write(json_line + '\n')
            except Exception as e:
                continue

    def run(self):
        # task list
        self.all_episodes = []
        for chunk in os.listdir(os.path.join(self.args.data_path, 'data')):
            for episode in os.listdir(os.path.join(self.args.data_path, 'data', chunk)):
                self.all_episodes.append(os.path.join(self.args.data_path, 'data', chunk, episode))

        if not os.path.exists(self.args.output_data_path):
            os.makedirs(self.args.output_data_path, exist_ok=True)
        ## new data path
        self.args.output_image_path = os.path.join(self.args.output_data_path, 'images')
        self.args.norm_path = os.path.join(self.args.output_data_path, 'norm_para.json')

        with open(os.path.join(self.args.data_path, 'meta', 'info.json')) as f:
            self.info = json.load(f)

        with open(os.path.join(self.args.data_path, 'meta', 'common_record.json')) as f:
            self.common_record = json.load(f)

        ## compute and load action norm para
        if not os.path.exists(self.args.norm_path):
            self.compute_norm()
        self._load_normalization_parameters()

        ## process trajectory data to training format
        self.json_file_writer = open(os.path.join(self.args.output_data_path, 'train_data.jsonl'), 'w')
        self.process_trajectory()
        self.json_file_writer.close()


if __name__ == "__main__":
    argv = [
        "--data_path", "/home/liuyou/Documents/merge_data/CoRobot/刷透明试管_试用角色测试新建模版_346",
        "--output_data_path", "/home/liuyou/Documents/merge_data/robotics/刷透明试管_试用角色测试新建模版_346"
    ]
    args = get_args()
    processor = CoRobot2Train(args)
    processor.run()
