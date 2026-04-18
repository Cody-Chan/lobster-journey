# 工作现场

> 🦞 龙虾智能体的工作现场说明 - 任何龙虾都能从此接手工作

---

## 当前状态

**更新时间**：2026-04-18 12:35

**当前任务**：第二项任务 - 工作现场保存机制

**进度**：
- ✅ 任务1：互动运营自动化（已完成）
- 🔄 任务2：工作现场保存机制（进行中）
- ⏳ 任务3：龙虾巡游100天策划（待开始）

---

## 最近工作

### 2026-04-18（今天）

#### 任务1：互动运营自动化 ✅

**已完成**：
- 创建分层架构设计（公司组织形式）
- 实现浏览器自动化模块（Playwright，200行）
- 实现互动动作控制（频率限制、风控，250行）
- 实现数据采集模块（SQLite，200行）
- 添加主程序协调器（150行）
- 总代码量：~800行Python

**关键文件**：
- `src/interaction/browser.py` - 浏览器自动化
- `src/interaction/actions.py` - 互动动作控制
- `src/data/collector.py` - 数据采集
- `scripts/run_interaction.py` - 主程序

**文档**：
- `docs/ARCHITECTURE.md` - 分层架构设计
- `docs/INTERACTION_STRATEGY.md` - 互动运营策略

**已推送到GitHub**：✅

#### 任务2：工作现场保存机制 🔄

**进行中**：
- 创建设计文档
- 实现保存脚本
- 创建私有仓库

---

## 项目结构

```
lobster-journey/
├── docs/                    # 文档
│   ├── ARCHITECTURE.md     # 架构设计
│   ├── INTERACTION_STRATEGY.md  # 互动策略
│   ├── INVESTOR_PITCH.md   # 投资人介绍
│   └── WORK_SNAPSHOT_DESIGN.md  # 工作现场设计
├── src/                     # 源代码
│   ├── interaction/        # 互动运营模块
│   │   ├── browser.py      # 浏览器自动化
│   │   └── actions.py      # 互动动作
│   └── data/               # 数据模块
│       └── collector.py    # 数据采集
├── scripts/                 # 脚本
│   └── run_interaction.py  # 运行互动任务
├── data/                    # 数据存储
├── branding/                # 品牌素材
│   └── assets/             # Logo、背景图等
├── MEMORY.md               # 记忆存储（工作区）
└── WORKSPACE.md            # 工作现场（本文件）
```

---

## 重要配置

### GitHub账号

- **用户名**：lobster-journey
- **仓库**：
  - lobster-journey（公开）
  - xiaohongshu-agent（待用）
  - ai-creator-starter（待用）

### 小红书账号

- **账号**：ai-report
- **状态**：已登录
- **MCP服务**：http://localhost:18060
- **Cookie位置**：/home/gem/.openclaw/mcp/cookies.json

### API密钥

- **Querit API**：querit-sk-XXX（已配置）
- **OneAPI令牌**：sk-XXX（已配置）

---

## 下一步计划

### 立即执行

1. 完成工作现场保存机制设计
2. 创建私有仓库
3. 实现保存脚本

### 本周计划

1. ✅ 任务1：互动运营自动化
2. 🔄 任务2：工作现场保存机制
3. ⏳ 任务3：龙虾巡游100天策划

### 后续计划

- 测试互动运营自动化
- 发布第一篇小红书内容
- 隐藏老笔记
- 启动数据飞轮

---

## 重要决策记录

### 2026-04-18

1. **分层架构设计**：采用公司组织形式的分层架构
   - 战略层、战术层、执行层、数据层、基础设施层

2. **技术选型**：
   - 浏览器自动化：Playwright
   - 数据存储：SQLite
   - 版本控制：Git/GitHub

3. **安全策略**：
   - 敏感信息存私有仓库
   - Cookie加密存储
   - 频率控制避免封号

---

## 接手指南

### 如果你是新的龙虾智能体

**步骤**：

1. **阅读本文档**：了解当前状态和工作进展

2. **阅读MEMORY.md**：了解项目背景和用户信息

3. **查看docs/目录**：了解架构设计和策略

4. **检查src/代码**：了解已实现的功能

5. **查看GitHub仓库**：确认代码已推送

6. **继续当前任务**：从"下一步计划"开始

### 需要的资源

- GitHub访问权限（lobster-journey组织）
- 小红书账号Cookie
- API密钥（Querit、OneAPI）
- OpenClaw环境

---

## 联系方式

**创建者**：陈 / comeL陈  
**联系渠道**：如流（chenke16）  
**时区**：Asia/Shanghai (GMT+8)

---

**创建时间**：2026-04-18  
**更新时间**：2026-04-18 12:35  
**维护者**：小龙虾 🦞
