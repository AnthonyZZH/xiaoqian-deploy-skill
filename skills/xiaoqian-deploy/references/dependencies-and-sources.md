# 依赖、来源与版本边界

## 可复核基线

| 组件 | 该流程的历史验证版本 | 来源与限制 |
| --- | --- | --- |
| Node.js | 要求 ≥24；测试 24.22.1 | [Node 官方下载](https://nodejs.org/en/download)。新大版本需要重跑兼容测试 |
| Python | 3.12；测试 3.12.10 | [Python 官方下载](https://www.python.org/downloads/)，使用目标系统的受控环境 |
| Harness | `@deepseek-ai/dsh@0.2.1-rc.4` | [官方代码仓库](https://github.com/deepseek-ai/deepseek-harness)、[npm 包](https://www.npmjs.com/package/@deepseek-ai/dsh) |
| Harness tools | `@deepseek-ai/dsh-tools@0.2.1-rc.4` | [npm 包](https://www.npmjs.com/package/@deepseek-ai/dsh-tools)，与 Harness 同一 rc.4 |
| Windows UI Automation | `uiautomation==2.0.29` | [PyPI 版本](https://pypi.org/project/uiautomation/2.0.29/)、[作者仓库](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows) |
| COM | `comtypes==1.4.17` | [PyPI 版本](https://pypi.org/project/comtypes/1.4.17/) |
| 图片解析 | `Pillow==12.0.0` | [PyPI 版本](https://pypi.org/project/pillow/12.0.0/) |
| 主库，可选 | `basic-memory==0.24.1` | [作者仓库](https://github.com/basicmachines-co/basic-memory)、[官方文档](https://docs.basicmemory.com/) |

以上是复现基线，不是最新版本推荐或安全更新承诺。选择不同版本时，核对目标锁文件、来源和 API，记录差异并重跑测试。不要从社区镜像猜测官方包，不执行网页提供的未知安装脚本；npm 页面不可达不意味着安装包已经核验。

rc.4 的 Agent/tool 注册、子任务 activation/query/recovery、会话事件内容及 completed reason 的形状有严格约束。不要用名称相似的端口或返回值替代；按桥接仓库的针对性测试检查实际安装的公共 package metadata 和导出。provider balance shim 如启用，还需要核实官方 provider、精确已安装包版本/源文件摘要及模块解析；缺失时报告不可用，不改写原包或读取凭据。

## 平台边界

Windows 是当前真实微信 UI driver 的适配目标。macOS/Linux 可以运行适用的核心、模拟 driver、脚本和非 UI 测试；遇到 `LIVE_DRIVER_REQUIRES_WINDOWS` 不能绕过为“已支持”。迁移真实微信 UI 必须另写并在目标平台验收适配器。

## 经验与证据优先级

该流程从原桥接源码的 `docs/REPRODUCIBLE-BATCH1.md`、`BATCH2.md`、`BATCH3.md`、`tools/render-owner-deployment.mjs`、`requirements-windows.txt` 与一次 `31d6009` 发布提炼；未再分发这些源码或私有记录。

Batch 文档是历史源码整合记录：其中“未上线”不代表后续一直未上线。判断当前机器时，应关联其当前 release manifest、精确源码摘要及同一运行进程的健康证据。清单上的 commit 字符串本身不能证明进程加载的代码；PID 也会复用。核对启动时间、启动参数指向的路径、构建摘要及 scoped 工具注册，敏感参数只在宿主内核验。

不将旧环境的 PID、Session 编号、路径、主库端点、聊天名或价格策略写成所有部署的默认值。未重现的动画、附件接收、模型子任务或多平台能力要保留为待验收项。
