# Claude Code 新手启动包

一套开箱即用的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 配置 — 包含安全防护 hooks、权限预设和项目指令模板。

[English](README.md)

## 包含内容

```
├── CLAUDE.md                     # 项目指令模板
├── global-settings.json          # 全局配置模板（~/.claude/settings.json）
└── .claude/
    ├── settings.json             # 项目级权限 + hooks 配置
    └── scripts/
        ├── bash_safety_guard.py  # 拦截危险命令 & token 浪费命令
        ├── pre_write_think.py    # 写代码前的思考清单
        └── post_write_check.py   # 写完代码后自动语法检查
```

## 快速开始

### 1. 全局配置

把 `global-settings.json` 复制到你的 Claude 配置目录：

- Windows: `C:\Users\<用户名>\.claude\settings.json`
- Mac/Linux: `~/.claude/settings.json`

填入你自己的 API 凭证：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "填你的key",
    "ANTHROPIC_BASE_URL": "填你的API地址"
  }
}
```

> 如果你用的是 Anthropic 官方订阅（Max plan），不需要 `env` 字段，直接删掉即可。

### 2. 项目配置

把 `CLAUDE.md` 和 `.claude/` 文件夹复制到你的项目根目录：

```bash
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### 3. 验证

在项目目录下启动 Claude Code，随便执行一个命令，你应该能看到 "Safety check..." 的状态提示。

## Hooks 说明

| Hook | 触发时机 | 作用 |
|------|---------|------|
| `bash_safety_guard.py` | 执行任何 Bash 命令前 | 拦截 `rm -rf /`、`git push --force`、`DROP TABLE`、fork bomb 等危险命令；同时拦截 `cat` 大文件、无限制 `git log` 等浪费 token 的命令 |
| `pre_write_think.py` | 编辑/写入代码文件前 | 弹出思考清单：最小改动？能复用现有代码吗？会破坏调用方吗？ |
| `post_write_check.py` | 编辑/写入代码文件后 | 自动运行语法检查：Python 用 `py_compile`，JS 用 `node --check`，TS 用 `tsc --noEmit` |

## 权限预设

项目 `settings.json` 预设了常用开发命令（git、npm、pip、python、文件操作等）的自动放行，避免每次都要手动确认。根据你的需要增减即可。

## 自定义建议

- 修改 `CLAUDE.md` 描述你的背景、编码风格和项目上下文
- 在 `.claude/settings.json` 的权限列表中增减命令
- 在 `bash_safety_guard.py` 中添加更多拦截规则

## 环境要求

- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+（hook 脚本需要）
- Node.js（可选，用于 JS/TS 语法检查）

## 许可证

[MIT](LICENSE)
