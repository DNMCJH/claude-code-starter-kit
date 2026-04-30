# Claude Code 新手启动包

一套开箱即用的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 配置 — 包含安全防护 hooks、权限预设和项目指令模板。

[English](README.md)

## 包含内容

```
├── CLAUDE.md                     # 项目指令模板（告诉 Claude 怎么跟你协作）
├── global-settings.json          # 全局配置模板（~/.claude/settings.json）
└── .claude/
    ├── settings.json             # 项目级权限 + hooks 配置
    └── scripts/
        ├── bash_safety_guard.py  # 拦截危险命令 & token 浪费命令
        ├── pre_write_think.py    # 写代码前的思考清单
        └── post_write_check.py   # 写完代码后自动语法检查
```

## 快速开始

### 方式一：让 Claude Code 帮你装（最省事）

如果你已经能用 Claude Code 了，直接把下面这段话发给它：

```
帮我安装 Claude Code 新手配置包。
仓库地址：https://github.com/DNMCJH/claude-code-starter-kit
请读取这个仓库的 README，然后：
1. 把 global-settings.json 的内容写入我的 ~/.claude/settings.json（保留我已有的 env 配置）
2. 把 CLAUDE.md 和 .claude/ 文件夹复制到我当前项目的根目录
3. 帮我修改 CLAUDE.md 的 User Context，写上我的专业背景
4. 验证 hooks 是否生效
```

Claude Code 会自动读取仓库、下载文件、帮你配置好一切。

### 方式二：手动安装

### 第 1 步：全局配置

把 `global-settings.json` 的内容复制到你的 Claude 配置文件：

- Windows: `C:\Users\<用户名>\.claude\settings.json`
- Mac/Linux: `~/.claude/settings.json`

然后填入你的 API 凭证：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "填你的key",
    "ANTHROPIC_BASE_URL": "填你的API地址"
  },
  "model": "sonnet",
  "effortLevel": "medium",
  "includeCoAuthoredBy": false
}
```

> 如果你用的是 Anthropic 官方订阅（Max plan），不需要 `env` 字段，直接删掉即可。

### 第 2 步：项目配置

把 `CLAUDE.md` 和 `.claude/` 文件夹复制到你的项目根目录：

```bash
# Windows (在项目根目录执行)
# 把下载的 CLAUDE.md 复制到项目根目录
# 把下载的 .claude/ 文件夹整个复制到项目根目录

# Mac/Linux
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### 第 3 步：修改 CLAUDE.md

打开项目里的 `CLAUDE.md`，把 `User Context` 部分改成你自己的情况，比如：

```markdown
## User Context
通信工程大三，熟悉 Python 和 MATLAB，正在做数字水印方向的毕设。
```

### 第 4 步：验证

在项目目录下启动 Claude Code，试试这三个操作：

1. 让 Claude 执行 `ls` — 你应该能看到状态栏闪过 "Safety check..."
2. 让 Claude 执行 `rm -rf /` — 应该被安全防护**拦截**
3. 让 Claude 编辑一个 `.py` 文件 — 应该先看到 "Think before write..." 再看到 "Checking syntax..."

三个都正常就说明配置成功了。

## Hooks 说明

| Hook | 触发时机 | 作用 |
|------|---------|------|
| `bash_safety_guard.py` | 执行任何 Bash 命令前 | 拦截 `rm -rf /`、`git push --force`、`DROP TABLE`、fork bomb 等危险命令；同时拦截 `cat` 大文件、无限制 `git log` 等浪费 token 的命令 |
| `pre_write_think.py` | 编辑/写入代码文件前 | 弹出思考清单：最小改动？能复用现有代码吗？会破坏调用方吗？ |
| `post_write_check.py` | 编辑/写入代码文件后 | 自动运行语法检查：Python 用 `py_compile`，JS 用 `node --check`，TS 用 `tsc --noEmit` |

## CLAUDE.md 是什么

`CLAUDE.md` 是项目指令文件，Claude 每次对话开始时都会读取它。模板包含：

- **用户背景** — 告诉 Claude 你的技术水平，让它调整解释深度
- **沟通偏好** — 语言偏好、commit message 格式
- **代码风格** — 最小代码、不做过度抽象
- **Token 效率** — effort level 建议、工具偏好、上下文管理
- **工作流** — Hook 状态提醒

根据你自己的情况修改即可。

## 权限预设

项目 `settings.json` 预设了常用开发命令的自动放行：

- **Git**：所有常用操作（add、commit、push、pull、branch 等）
- **包管理器**：npm、pnpm、pip
- **运行时**：node、npx、python、python3
- **文件操作**：mkdir、cp、mv、rm、touch、chmod、curl
- **常用工具**：ls、find、cat、head、tail、wc、echo、pwd、which、diff、grep
- **编辑器**：code（VS Code）
- **工具**：Write、Edit（文件编辑）

需要更多？在 `.claude/settings.json` 的 `allow` 列表里加 `"Bash(docker *)"` 、`"Bash(ssh *)"` 等即可。

## 全局配置说明

| 字段 | 作用 | 可选值 |
|------|------|--------|
| `env.ANTHROPIC_AUTH_TOKEN` | API 密钥（仅代理用户需要） | 你的 API key |
| `env.ANTHROPIC_BASE_URL` | API 地址（仅代理用户需要） | 你的代理地址 |
| `model` | 默认模型 | `sonnet`、`opus`、`haiku`，或带上下文：`opus[1m]` |
| `effortLevel` | 回复努力程度 | `low`、`medium`、`high` |
| `includeCoAuthoredBy` | commit 中添加 co-author 标签 | `true` / `false` |

## 自定义指南

### 入门级
1. 修改 `CLAUDE.md` — 把 User Context 改成你自己的情况
2. 在 `~/.claude/settings.json` 填入 API 凭证
3. 开始使用 Claude Code

### 进阶级
4. 在 `.claude/settings.json` 的权限列表中增减命令
5. 在 `bash_safety_guard.py` 中添加更多拦截规则
6. 在 `post_write_check.py` 中添加更多语言的语法检查

### 高级
7. 添加 MCP 工具权限（Playwright、Firecrawl 等）
8. 添加自定义 hooks（如 firecrawl 爬取限制、浏览器 URL 安全检查）
9. 创建自定义 slash commands（`~/.claude/commands/`）

## 常见问题

**执行命令时没有看到 "Safety check..."**
- 确认 `.claude/scripts/` 目录在项目根目录下
- 检查 Python 版本：`python --version`（需要 3.10+）
- Mac/Linux 上确保脚本有执行权限：`chmod +x .claude/scripts/*.py`

**已经配置了权限但还是弹出确认提示**
- 确认 `.claude/settings.json` 在项目根目录（不是子目录）
- 检查命令模式是否匹配 — `Bash(git *)` 覆盖 `git status`、`git add .` 等

**TypeScript 语法检查不生效**
- 确认项目中有 `tsconfig.json`
- 安装 TypeScript：`npm install -D typescript`

**Mac 上提示 "python: command not found"**
- Hook 命令已经自动先尝试 `python3` 再回退到 `python`。如果都不行，安装 Python 3：`brew install python`

## 环境要求

- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+（hook 脚本需要）
- Node.js（可选，用于 JS/TS 语法检查）

## 许可证

[MIT](LICENSE)
