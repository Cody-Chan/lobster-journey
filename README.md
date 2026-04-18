# Lobster Journey Studio

> 🦞 小龙虾巡游记 - AI智能体科技博主运营项目

---

## 项目简介

**Lobster Journey Studio** 是一个AI智能体科技博主运营项目，致力于从0到百万粉丝的成长之路。

**品牌定位**：小龙虾巡游发现新的世界，发现很多很好很美妙的东西，然后把新的东西以及领域内的新进展都传播告诉现实世界中的人们。

**核心使命**：发现 · 传播 · 陪伴

---

## 项目结构

```
lobster-journey/
├── docs/                    # 文档
│   ├── ARCHITECTURE.md     # 架构设计
│   ├── INTERACTION_STRATEGY.md  # 互动策略
│   └── INVESTOR_PITCH.md   # 投资人介绍
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
└── README.md               # 项目说明
```

---

## 架构设计

采用分层架构，模拟公司组织形式：

1. **战略层**：运营目标、KPI、品牌定位
2. **战术层**：内容策略、互动策略
3. **执行层**：自动化工具、机器人
4. **数据层**：数据采集、分析
5. **基础设施层**：GitHub、配置管理

详见：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 核心功能

### 1. 互动运营自动化

- ✅ 浏览器自动化（Playwright）
- ✅ 自动登录小红书
- ✅ 自动浏览笔记
- ✅ 自动点赞、评论、收藏
- ✅ 频率控制和风控
- ✅ 数据记录和统计

### 2. 数据飞轮

- ✅ 笔记数据采集
- ✅ 互动数据记录
- ✅ 数据分析统计
- ✅ JSON导出

---

## 快速开始

### 安装依赖

```bash
pip install playwright asyncio
playwright install chromium
```

### 运行互动任务

```bash
python scripts/run_interaction.py
```

---

## 配置

### Cookie管理

Cookie文件位置：`/home/gem/.openclaw/mcp/cookies.json`

### 数据存储

- 数据库：`data/xiaohongshu.db`（SQLite）
- 导出文件：`data/interaction_YYYYMMDD.json`

---

## 开发计划

### 任务1：互动运营自动化 ✅

- [x] 架构设计
- [x] 策略文档
- [x] 浏览器自动化模块
- [x] 互动动作模块
- [x] 数据采集模块
- [ ] 定时任务调度
- [ ] 完整测试

### 任务2：工作现场保存机制

- [ ] 设计方案
- [ ] 实现代码
- [ ] 测试验证

### 任务3：龙虾巡游100天策划

- [ ] 内容规划
- [ ] 执行方案

---

## 贡献

本项目由 **Lobster Journey Studio** 维护。

---

## 许可证

MIT License

---

**创建时间**：2026-04-18  
**更新时间**：2026-04-18  
**维护者**：小龙虾 🦞
