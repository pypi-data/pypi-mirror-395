# flagdataset-eai
---------------------

flagdataset-eai 是一个用于下载数据的 Python 包。


## PyTorch CPU 版本安装（重要）


由于 ABI 兼容性问题，需要额外安装 CPU 优化版本的 PyTorch：


```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## 示例

使用cli下载指定任务的数据


### cli

```sh
# 安装
pip install -U flagdataset-eai

# 查看帮助
bf -h

# 使用AK,SK登录
bf auth login

# 下载任务
# -t . 是保存到当前目录
bf down --target-ids=405,414,415 -t .
```
