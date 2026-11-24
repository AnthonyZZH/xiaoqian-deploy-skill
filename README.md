# 小千部署 Skill

[小千公开主仓](https://github.com/AnthonyZZH/xiaoqian-weixin) · [主仓中的部署 Skill](https://github.com/AnthonyZZH/xiaoqian-weixin/tree/main/skills/xiaoqian-deploy)

主仓维护部署流程、参考资料和校验脚本。本仓保留可离线安装的完整发布快照，对应的主仓提交见 [UPSTREAM_COMMIT](UPSTREAM_COMMIT)。更新内容请提交到主仓。

## 安装

从本仓下载 ZIP 或使用 Git 克隆，复制整个 `skills/xiaoqian-deploy` 到 Codex 的技能目录。使用主仓的同名目录也可以安装。在 Windows PowerShell 中，从下载后的仓库根目录运行：

```powershell
$SkillHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$Dest = Join-Path $SkillHome 'skills\xiaoqian-deploy'
if (Test-Path -LiteralPath $Dest) { throw '已安装同名技能，请先核对并保存需要保留的本地修改。' }
New-Item -ItemType Directory -Force (Split-Path $Dest) | Out-Null
Copy-Item -LiteralPath '.\skills\xiaoqian-deploy' -Destination $Dest -Recurse
```

在新对话中使用 `$xiaoqian-deploy`，例如“核对这台 Windows 机器上的小千版本和交互桌面，本次只做检查”。技能支持部署、升级、回退、跨桌面迁移和只读校验。涉及实际收发、生产切换和模型调用时，以当前任务授权为准。

## 验证快照

```text
python -B -m unittest discover -s tests -p test_verify_manifest.py -v
```

这组测试使用合成文件验证清单校验器。完整桥接器的配置生成器、Windows 驱动、依赖和离线集成测试在公开主仓。私有配置、凭据、聊天及运行数据保存在各自的部署中。

## 维护者发布

在主仓合并技能变更后，于本仓运行下列命令。最后一个参数应替换成公开主仓 `main` 上选定提交的完整 40 位 SHA。

```text
python -B scripts/sync_skill.py FULL_MAIN_COMMIT
python -B -m unittest discover -s tests -p test_verify_manifest.py -v
git diff --cached --check
git diff --cached --stat
```

同步脚本从固定的公开主仓读取，核对提交属于 `main`，将整个技能目录、清单校验器测试和 `UPSTREAM_COMMIT` 暂存到本仓。重复同步同一份已发布快照会保持工作树干净。维护者审阅暂存差异后在本仓提交并推送。两次手动发布之间，本仓提供上次核验的版本。
