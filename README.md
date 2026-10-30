# 小千部署 Skill

用于 Codex 的可复用部署流程：将小千 Harness 原生微信桥接器部署到 Windows 交互桌面，或进行代码升级、配置迁移、健康检查与回退。它整理的是经过一次 rc.4 部署验证的操作顺序，不包含小千程序本身，也不会自动连接任何服务器。

仓库名：`xiaoqian-deploy-skill`。机器、账号和部署路径由使用者指定；安装或运行此 skill 不会自动删除任何旧仓库。

## 支持范围

| 环境 | 范围 |
| --- | --- |
| Windows + 已登录的交互桌面 | 核心、真实微信 UI driver；必须在目标微信版本上验收 |
| 跨主机 / 新桌面 / 重建窗口身份 | 只支持准备与暂停核验；目标版本必须提供安全的身份恢复机制并通过历史不重放验收，否则阻止 resume |
| macOS / Linux | 核心与 fake/non-UI 测试；没有可用的真实微信 UI driver 声明 |
| SSH / Windows Session 0 | 源码、传包、离线验证和只读诊断；不能据此判断交互微信可控 |

流程针对 `@deepseek-ai/dsh` 和 `@deepseek-ai/dsh-tools` **0.2.1-rc.4**。Node 要求 ≥24，历史验证组合为 Node 24.22.1、Python 3.12.10。版本升级必须重新核对 Harness 工具注册、原生子任务、会话事件和 provider 端口，不能把本流程当成所有后续版本的兼容保证。

Windows UI 依赖基线：`uiautomation==2.0.29`、`comtypes==1.4.17`、`Pillow==12.0.0`。仅在新的隔离环境中按目标桥接仓库锁定文件准备；不覆盖正在运行的 venv。原主图书馆集成的历史基线为 Basic Memory 0.24.1，属于可选依赖，不是 skill 自身的依赖。官方来源见 [依赖与来源](skills/xiaoqian-deploy/references/dependencies-and-sources.md)。

## 安装到 Codex

取得本仓库后，把整个 `skills/xiaoqian-deploy` 文件夹复制到自己的 Codex skills 目录：优先 `$CODEX_HOME/skills`，未设置时通常是 `~/.codex/skills`。安装后应存在 `skills/xiaoqian-deploy/SKILL.md`，不要只复制该 Markdown 而遗漏 references 和 scripts。

本候选不自行安装或覆盖已有 skill；如已存在同名目录，先比较并保留旧版本。可在新对话中按名称调用：

```text
$xiaoqian-deploy
把指定提交部署到我授权的 Windows 主机。先只读盘点，核对交互桌面和当前控制器，
给出待切换代码、私有配置、备份和回退路径；本轮先不要切换。
```

也可用于“核对当前部署与代码是否一致”“准备新机器迁移”或“在保留 dedup/未知发送记录的前提下回退”。主机、SSH 别名、Windows 会话、提交 SHA、源码与数据路径均来自本次明确授权，不写死在 skill 中。

## 包含什么

- [SKILL.md](skills/xiaoqian-deploy/SKILL.md)：短工作流与引用入口。
- `references/`：Windows 会话、暂停配置、健康验收、私有备份恢复及切换回退。
- `scripts/verify_manifest.py`：只读校验显式文件清单的长度和 SHA256，不复制数据、不递归搜集文件、不执行部署。
- `tests/test_verify_manifest.py`：仅使用临时合成文件验证校验器。

此 skill 不附带安装器、常驻服务、自动重启、凭据文件或通用管理员 shell。对部署的授权不会隐含新账户、永久权限、公网端口、额外发送、付费模型测试、GitHub 发布或删除旧仓库的授权。

## 使用前提供的参数

至少需要目标源码仓库与提交、`SOURCE_ROOT`、`STATE_ROOT`、现有 Node/CLI 与 Python 路径、`NATIVE_PACKAGE_ROOT`、确认过的 owner 绑定及现有交互启动方式。升级还需要当前 release/配置记录、备份目标和上一版本。只有启用对应能力时，才提供主库端点、工作数据根、媒体解析环境或长任务日志根。

流程先审查参数，再生成 **paused** 配置；按已授权范围完成单控制器切换，并分别报告离线、宿主健康、实际账号验收证据。HTTP ready、静态截图、mock 测试或一次 UI 点击不能替代送达、动画或付费子任务的真实验收。

**备份字节一致不代表可以在新桌面继续接收。** 即便恢复了 `uia-row-v2` 和 `bootstrapped=true`，新的 UIA RuntimeId 仍可能让旧可见消息得到新 ID，被错误接收。必须完成 [跨桌面身份恢复门槛](skills/xiaoqian-deploy/references/cross-desktop-migration.md)，不能宣称自动无缝迁移。没有受支持的恢复方法时保持 paused；不得清账本、重置 bootstrapped 或直接 ACK 全屏消息来强行启动。

## 离线验证

在仓库根目录运行：

```text
python -B -m unittest discover -s tests -v
```

已有私有清单时可以只读核对：

```text
python -B skills/xiaoqian-deploy/scripts/verify_manifest.py --root RESTORED_ROOT --manifest PRIVATE_MANIFEST_JSON
```

清单格式与限制见 [备份恢复](skills/xiaoqian-deploy/references/backup-and-restore.md)。不要把真实清单、私有配置、聊天记录、日志、媒体或库数据提交到本仓库。测试不连接服务器，不访问微信或模型，不安装依赖、不重启服务。

本仓库当前未配置托管 CI；可按上述命令在本地独立环境重跑测试。清单校验器测试通过不代表目标 core 已通过跨桌面身份恢复，也不代表真实微信可上线；对应目标版本仍须单独完成上述接收决策验收。

## 经验来源与限制

流程从桥接器的 `REPRODUCIBLE-BATCH1/2/3.md`、暂停配置 renderer、锁定依赖和一次实际发布记录提炼。历史文档写“尚未上线”的位置必须用对应 release 记录和运行证据重新判断，不能把开发阶段说明当成当前状态。具体机器、账户、聊天、PID、日志和私有配置均未附带；本仓库不代表微信或 DeepSeek 的官方集成。
