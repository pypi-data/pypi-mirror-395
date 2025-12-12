# Apollo Launcher

这是一个简单的 Python 工具，用于在应用启动前从 Apollo 配置中心拉取配置，并将其注入到环境变量中。

## 功能

- 从 Apollo 拉取配置 (支持命名空间)
- 将配置注入到环境变量
- 启动目标应用 (使用 `execvp` 替换进程，保留 PID)

## 安装

```bash
pip install .
# 或者
pip install tec-do-apollo-env-launcher
```

## 使用方法

在启动命令前加上 `apollo-launcher` 即可：

```bash
# 假设原命令是 python app.py
apollo-launcher python app.py
```

或者使用 `python -m` 方式 (模块名为 `apollo_launcher`)：

```bash
python -m apollo_launcher.main python app.py
```

## 环境变量配置

工具依赖以下环境变量：

- `APOLLO_URL`: Apollo 配置中心地址 (必需)
- `APOLLO_APP_ID`: 应用 ID (必需)
- `CLUSTER_NAME`: 集群名称 (默认: `default`)
- `APOLLO_NAMESPACE`: 命名空间 (默认: `application`)

## 示例

```bash
export APOLLO_URL=http://apollo-dev.example.com
export APOLLO_APP_ID=my-service
export CLUSTER_NAME=dev

apollo-launcher uvicorn main:app --host 0.0.0.0
```
