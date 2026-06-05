# Claude Code 新手启动包

一套开箱即用的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 配置 — 包含安全防护 hooks、权限预设、MCP 服务器推荐和项目指令模板。

[English](README.md)

## 架构总览

本配置包反映了一套经过实战验证的双轨工作流：

```
开发轨道                              文档轨道
────────                              ────────
VSCode                                Obsidian
├── Claude Code 插件                  ├── Claudian 插件（兼容 Claude 和 Codex）
├── Codex 插件                        └── 闪电说（语音输入）
└── 闪电说（语音输入）

共享基础设施
────────────
├── 5 个 MCP 服务器（fetch, time, playwright, gemini-search, firecrawl）
├── 7 个工作流 skills（计划/执行/调试/验证/代码审查闭环 + coreview 双 agent 互审）
├── 7 个斜杠命令（caveman, diagnose, grill-me, tdd, tidy, html-deck, pptx-design-supplement）
├── 3 个安全 hooks（bash 防护、写前思考、写后语法检查）
├── 自动记忆系统（跨会话持久化上下文）
└── Document skills 插件（anthropic-agent-skills 市场）
```

## 包含内容

```
├── CLAUDE.md                     # 项目指令模板
├── global-settings.json          # 全局配置模板（~/.claude/settings.json）
├── skills/
│   ├── coreview/                 # 双 agent 代码互审 skill
│   │   ├── SKILL.md              # Skill 定义（触发词、协议、模板）
│   │   ├── scripts/
│   │   │   ├── coreview_state.py # 状态管理 CLI（init/claim/release/prune/critical/gate）
│   │   │   └── install.py        # 跨平台安装（Windows junction / POSIX symlink）
│   │   └── references/
│   │       └── protocol.md       # 详细协议规范
│   ├── writing-plans/            # 把规格拆成逐任务 TDD 计划
│   ├── executing-plans/          # 按计划执行 + 检查点
│   ├── systematic-debugging/     # 四阶段根因调试（先找根因再改）
│   ├── verification-before-completion/  # 没跑过验证不准说"完成"
│   ├── requesting-code-review/   # 派 reviewer 子 agent 审 git diff
│   │   └── code-reviewer.md      # reviewer prompt 模板
│   ├── receiving-code-review/    # 批判性评估审查意见，不盲从
│   └── install_workflow_skills.py # 一键 junction 安装上面 6 个工作流 skill
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
> 注意：官方订阅锁定 200K 上下文。想要 1M 上下文，必须从会话起点就走中转站（中途切换不会扩大窗口）。

### 2. 项目配置

把 `CLAUDE.md` 和 `.claude/` 文件夹复制到你的项目根目录：

```bash
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### 3. MCP 服务器（推荐）

注册这些 MCP 服务器获得完整工具链：

```bash
claude mcp add fetch -- python -m mcp_server_fetch
claude mcp add time -- python -m mcp_server_time --local-timezone Asia/Shanghai
claude mcp add playwright -- npx @playwright/mcp@latest
claude mcp add gemini-google-search -- npx mcp-gemini-google-search
claude mcp add firecrawl -- npx -y firecrawl-mcp
```

| 服务器 | 用途 | 使用场景 |
| ------ | ---- | -------- |
| fetch | 原始 HTTP 请求 | API 测试、下载文件 |
| time | 时区感知时间戳 | 日程安排、日期计算 |
| playwright | 浏览器自动化 | UI 测试、截图、表单填写 |
| gemini-google-search | 网络搜索（免费额度） | 快速查询、获取最新信息 |
| firecrawl | 网页抓取/提取 | 深度内容提取（有额度限制） |

### 4. 验证

在项目目录下启动 Claude Code，随便执行一个命令，你应该能看到 "Safety check..." 的状态提示。

## Hooks 说明

| Hook | 触发时机 | 作用 |
| ---- | -------- | ---- |
| `bash_safety_guard.py` | 执行任何 Bash 命令前 | 拦截 `rm -rf /`、`git push --force`、`DROP TABLE`、fork bomb 等危险命令；同时拦截 `cat` 大文件、无限制 `git log` 等浪费 token 的命令 |
| `pre_write_think.py` | 编辑/写入代码文件前 | 弹出思考清单：最小改动？能复用现有代码吗？会破坏调用方吗？ |
| `post_write_check.py` | 编辑/写入代码文件后 | 自动运行语法检查：Python 用 `py_compile`，JS 用 `node --check`，TS 用 `tsc --noEmit` |

## 这套配置的优势

来自日常实战的关键设计决策：

1. **三层安全防护** — 危险命令在 hook 层拦截（不只靠权限），token 浪费在烧上下文前就被捕获，语法在写入后立即验证
2. **MCP 优于 shell** — 用 playwright 做浏览器测试、gemini 做搜索、firecrawl 做抓取。工具调用可见可审计，不会埋在 bash 里
3. **Skills 封装可重复工作流** — 一套覆盖"计划→执行→调试→验证→代码审查"的工作流 skill，加上 coreview 双 agent 互审。每个都封装了多步 SOP，不用每次重新解释
4. **斜杠命令切模式** — `/caveman` 省 token 的简洁模式、`/grill-me` 设计拷问、`/tdd` 测试驱动流程。切模式不丢上下文
5. **自动记忆保连续性** — 跨会话持久化记忆，分类型（user/feedback/project/reference）。消灭"上次我们做了什么来着"
6. **权限白名单 + 黑名单** — 常用开发命令预放行减少弹窗疲劳；特定危险工具（file_upload）显式禁止
7. **双轨分离** — 开发在 VSCode（Claude Code + Codex），文档在 Obsidian（Claudian）。语音输入（闪电说）桥接两端

## Coreview Skill — 双 Agent 代码互审

`skills/coreview/` 目录包含一套协调两个编码 agent（如 Claude Code + Codex）互相 review 同一代码库的协议。

**安装：**

```bash
python skills/coreview/scripts/install.py
```

这会在 `~/.claude/skills/coreview/` 创建一个 junction/symlink 指向 skill 源码。Codex 在项目内自动发现，无需额外安装。

**使用：**

对任一 agent 说 `"coreview <scope>"`、`"针对 xxx 进行 coreview"`、`"双 agent 互审"` 即可触发。流程：

1. 一方 review → 写 findings 到 `reviews/YYYY-MM-DD_<scope>.md`
2. Hard Critical 发现会冻结编辑，弹出来等你决策
3. 非 Critical 的 findings 按文件 claim，并行修复
4. 对方 counter-review → 验证 → gate 通过

两个 agent 通过你传话 — 每轮结束后，agent 会输出一段话让你粘给另一边。不需要共享 runtime 或后台进程。

**核心特性：**
- Append-only 审计日志（review markdown）
- Hard Critical = 强制人工 gate
- Claim-by-file 防止并行编辑冲突
- 30 分钟超时自动释放废弃 claim
- 原子 JSON 写入（不会出现半截文件）

详见 [SKILL.md](skills/coreview/SKILL.md) 了解完整协议，[protocol.md](skills/coreview/references/protocol.md) 了解状态机细节。

## 工作流 Skills — 计划/执行/调试/验证/审查闭环

`skills/` 下另有 6 个工作流 skill，覆盖一次完整开发的关键环节。它们互相引用，形成一个闭环：

```text
写计划 → 执行计划 → (遇 bug) 系统化调试 → 请求审查 → 接收审查 → 完成前验证
```

| Skill | 作用 | 触发时机 |
| ----- | ---- | -------- |
| `writing-plans` | 把规格拆成 2–5 分钟一步的 TDD 任务，精确文件路径 + 完整代码，禁止占位符 | 动手写代码前 |
| `executing-plans` | 按计划逐任务执行，每步验证，卡住就停不瞎猜 | 有了书面计划后 |
| `systematic-debugging` | 四阶段根因调试 + 铁律"没找到根因不准改"，3 次修复失败→质疑架构 | 碰到任何 bug / 测试失败 |
| `verification-before-completion` | 铁律"没跑过验证命令不准说完成"，附 claim→证据对照表 | 准备说"搞定/通过/修好了"之前 |
| `requesting-code-review` | 派一个 reviewer 子 agent 审 git diff（coreview 的轻量单 agent 版） | 完成一个任务 / 合并前 |
| `receiving-code-review` | 批判性评估审查意见，先核实再改，不盲从不表演性同意 | 收到审查反馈时 |

**安装（一次性 junction 上全部 6 个）：**

```bash
python skills/install_workflow_skills.py            # 安装
python skills/install_workflow_skills.py --dry-run  # 预览
python skills/install_workflow_skills.py --uninstall # 卸载
```

和 coreview 一样用目录 junction（Windows 免管理员/开发者模式，POSIX 用 symlink），源码留在 repo，链接指回来。装完重启 Claude Code 即可被自动发现并按 description 触发。

> **出处**：这 6 个 skill 改编自 [obra/superpowers](https://github.com/obra/superpowers)（MIT）。本包做了三处本地化：① 删掉原文里的角色扮演措辞，保留硬核纪律（铁律 / Gate / 红旗表）；② 把断链的 `superpowers:` 交叉引用改写为指向本包已有的 `/tdd`、`coreview` 等；③ 软化对未打包辅助文件的依赖。

## 权限预设

项目 `settings.json` 预设了常用开发命令（git、npm、pip、python、文件操作、docker、ssh 等）的自动放行，避免每次都要手动确认。根据你的需要增减即可。

## 自定义建议

- 修改 `CLAUDE.md` 描述你的背景、编码风格和项目上下文
- 在 `.claude/settings.json` 的权限列表中增减命令
- 在 `bash_safety_guard.py` 中添加更多拦截规则
- 在 `~/.claude/skills/` 中添加自定义 skills 封装你的可重复工作流
- 在 `~/.claude/commands/` 中添加斜杠命令做模式切换

## 环境要求

- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+（hook 脚本需要）
- Node.js（MCP 服务器和 JS/TS 语法检查需要）

## 许可证

[MIT](LICENSE)
