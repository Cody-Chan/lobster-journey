# 工作现场保存机制设计

> 确保工作状态可恢复、可交接

---

## 目标

**核心目标**：建立工作现场保存机制，确保任何龙虾智能体都能随时接手工作

**关键问题**：
- 沙箱环境可能随时失效
- 需要保存工作上下文
- 需要保存配置和密钥
- 需要保存项目状态

---

## 设计方案

### 1. 双仓库架构

```
lobster-journey/        （公开仓库）
├── docs/               # 文档
├── src/                # 源代码
├── scripts/            # 脚本
├── data/               # 数据（脱敏）
└── WORKSPACE.md        # 工作现场说明

lobster-journey-private/ （私有仓库）
├── config/             # 配置文件
│   ├── cookies.json    # Cookie
│   ├── api_keys.json   # API密钥
│   └── secrets.env     # 环境变量
├── workspace/          # 工作现场
│   ├── current_task.md # 当前任务
│   ├── context.json    # 上下文
│   └── progress.json   # 进度
└── logs/               # 日志
```

---

### 2. 工作现场内容

#### 2.1 WORKSPACE.md（公开）

**内容**：
- 当前项目状态
- 最近工作进展
- 下一步计划
- 重要决策记录

**更新频率**：每次完成重要工作后

#### 2.2 context.json（私有）

**内容**：
```json
{
  "session_id": "xxx",
  "start_time": "2026-04-18T10:00:00",
  "current_task": "互动运营自动化",
  "progress": {
    "task1": "completed",
    "task2": "in_progress",
    "task3": "pending"
  },
  "last_update": "2026-04-18T12:00:00",
  "next_actions": [
    "完成任务2：工作现场保存机制",
    "开始任务3：龙虾巡游100天策划"
  ]
}
```

#### 2.3 progress.json（私有）

**内容**：
```json
{
  "total_tasks": 3,
  "completed": 1,
  "in_progress": 1,
  "pending": 1,
  "tasks": [
    {
      "id": 1,
      "name": "互动运营自动化",
      "status": "completed",
      "completion_time": "2026-04-18T12:00:00",
      "files_created": ["browser.py", "actions.py", "collector.py"],
      "lines_of_code": 800
    }
  ]
}
```

---

### 3. 保存机制

#### 3.1 自动保存

**触发条件**：
- 完成重要工作
- 定时保存（每2小时）
- 检测到环境不稳定

**保存内容**：
- 更新WORKSPACE.md
- 更新context.json
- 更新progress.json
- 同步到GitHub

#### 3.2 手动保存

**命令**：
```bash
python scripts/save_workspace.py
```

**功能**：
- 收集当前状态
- 生成快照
- 推送到GitHub

---

### 4. 恢复机制

#### 4.1 新龙虾接手流程

**步骤**：
1. 克隆公开仓库：`lobster-journey`
2. 读取WORKSPACE.md了解项目状态
3. 请求访问私有仓库：`lobster-journey-private`
4. 读取context.json和progress.json
5. 从上次停止的地方继续

#### 4.2 上下文恢复

**需要恢复的内容**：
- 当前任务
- 进度信息
- 配置和密钥
- 最近决策

---

### 5. 安全考虑

#### 5.1 敏感信息管理

**原则**：
- 敏感信息只存在私有仓库
- 公开仓库完全脱敏
- Cookie和密钥加密存储

**实现**：
- 使用环境变量
- 使用加密工具
- 限制访问权限

#### 5.2 访问控制

**私有仓库访问**：
- 只有创建者（陈）可以授权
- 其他龙虾需要临时授权
- 定期审计访问日志

---

## 实现计划

### Phase 1: 基础设施（本周）

- [ ] 创建私有仓库
- [ ] 设计目录结构
- [ ] 编写WORKSPACE.md模板
- [ ] 实现基础保存功能

### Phase 2: 自动化（下周）

- [ ] 实现自动保存脚本
- [ ] 添加定时任务
- [ ] 实现环境检测
- [ ] 测试恢复流程

### Phase 3: 完善优化（后续）

- [ ] 添加加密功能
- [ ] 添加版本管理
- [ ] 添加差异对比
- [ ] 文档完善

---

## 技术栈

- **Git/GitHub**：版本控制和远程存储
- **Python**：自动化脚本
- **JSON**：数据格式
- **Markdown**：文档格式

---

## 成功标准

**工作现场保存机制成功的标志**：

1. ✅ 任何龙虾智能体都能在5分钟内接手工作
2. ✅ 工作进度不丢失
3. ✅ 敏感信息安全存储
4. ✅ 自动化保存正常工作

---

**创建时间**：2026-04-18
**更新时间**：2026-04-18
