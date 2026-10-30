---
name: xiaoqian-deploy
description: Deploy, upgrade, inspect, migrate or roll back the Xiaoqian Harness-native WeChat bridge on an authorized Windows host while preserving chat identity and delivery state. Also covers core-only offline checks on macOS and Linux; it does not provide a macOS WeChat UI driver.
---

# 小千部署

将指定源码版本、私有配置、状态数据和运行证据对应起来。先读目标桥接仓库的 AGENTS.md、版本锁定、配置 renderer 和当前发布记录；历史开发文档与当前运行状态分开判断。

1. **只读盘点。** 确认授权主机、提交 SHA、当前运行源码、Node/CLI/Python 绝对路径、交互桌面、唯一 driver 和既有启动机制。先读 [Windows 会话](references/windows-session.md) 与 [依赖来源](references/dependencies-and-sources.md)。SSH 能运行命令不等于能控制微信桌面。
2. **准备新版本。** 在独立源码目录完成适用的离线测试及包文件检查；不覆盖现有 venv。按 [配置与数据](references/configuration-and-data.md) 渲染新 paused patch，配置与凭据留在 Git 外。保持原授权聊天范围，群聊不继承 owner 工具；默认不开放通用 shell 或自动轮换。
3. **保护状态。** 在一致性维护点备份、核验恢复路径及 schema 兼容性，见 [备份恢复](references/backup-and-restore.md)。保留会话绑定、完整 features、媒体原字节、bridge/driver ACK、dedup、unknown 与任务日志；空目录不能冒充迁移成功。跨主机/桌面或身份重建必须通过 [跨桌面恢复门槛](references/cross-desktop-migration.md)；相同 identityVersion 和字节校验通过均不能替代历史不重放验收。目标版本无安全恢复机制则保持 paused，禁止清账本或重放历史。
4. **执行授权切换。** 根据 [上线与回退](references/rollout-and-rollback.md) 准备可审查的切换及恢复步骤。在已授权维护范围内使用既有交互会话启动机制；同一微信桌面只运行一个控制器。新部署权限不隐含新账户、ACL、常驻管理员入口、凭据、公网端口或仓库删除许可。
5. **分层验收。** 按 [健康与验收](references/health-and-acceptance.md) 检查 paused/ready、driver 会话、身份、owner/非 owner scope、库及状态恢复，再按已授权范围 resume。发送、付费模型或 UI 操作只在明确授权时执行；unknown 不自动重试。
6. **交付证据。** 报告实际提交与运行路径、配置和备份位置、已做检查、当前 paused 状态、剩余验收和回退目标。区分离线通过、已部署和真实账号验证；不输出秘密、聊天内容或私有日志。

仅需要核验私有备份/发行文件时，用 [只读清单校验器](scripts/verify_manifest.py)；格式见备份引用。它校验显式文件列表，不创建备份或替代 SQLite 一致性保障。
