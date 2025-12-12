#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apollo 配置加载启动器
用途：在应用启动前从 Apollo 配置中心拉取配置，并注入到环境变量中，然后启动目标应用。
"""

import os
import sys
import json
import urllib.request
import signal

def fetch_apollo_configs():
    """从 Apollo 拉取配置并返回字典"""
    apollo_url = os.environ.get("APOLLO_URL")
    app_id = os.environ.get("APOLLO_APP_ID")
    cluster = os.environ.get("CLUSTER_NAME", "default")
    namespace = os.environ.get("APOLLO_NAMESPACE", "application")

    # 检查必要环境变量
    if not (apollo_url and app_id):
        print("[ApolloLauncher] ⚠️  APOLLO_URL or APOLLO_APP_ID not set, skipping config fetch.")
        return {}

    # 构造 URL (移除末尾斜杠以防万一)
    apollo_url = apollo_url.rstrip("/")
    url = f"{apollo_url}/configs/{app_id}/{cluster}/{namespace}"
    
    print(f"[ApolloLauncher] 🚀 Fetching configs from: {url}")

    try:
        # 设置超时时间，避免阻塞太久
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                configurations = data.get("configurations", {})
                print(f"[ApolloLauncher] ✅ Successfully loaded {len(configurations)} configurations:")
                for key, value in configurations.items():
                    print(f"[ApolloLauncher]    - {key}: {value}")
                return configurations
            else:
                print(f"[ApolloLauncher] ❌ Failed to fetch configs: HTTP {response.status}")
                return {}
    except Exception as e:
        print(f"[ApolloLauncher] ❌ Error fetching Apollo configs: {e}")
        return {}

def main():
    # 1. 获取 Apollo 配置
    configs = fetch_apollo_configs()

    # 2. 注入环境变量
    for key, value in configs.items():
        str_value = str(value)
        os.environ[key] = str_value

    # 3. 执行目标命令
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        args = sys.argv[1:]
        
        print(f"[ApolloLauncher] ▶️  Starting application: {' '.join(args)}")
        sys.stdout.flush()

        try:
            os.execvp(cmd, args)
        except FileNotFoundError:
            print(f"[ApolloLauncher] ❌ Command not found: {cmd}")
            sys.exit(1)
        except Exception as e:
            print(f"[ApolloLauncher] ❌ Failed to execute command: {e}")
            sys.exit(1)
    else:
        print("[ApolloLauncher] ❌ No command provided to execute.")
        print("Usage: apollo-launcher <command> [args...]")
        sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    main()
