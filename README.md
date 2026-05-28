
#  智能客服Agent系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange.svg)](https://deepseek.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-red.svg)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于 **Function Calling** 架构的企业级智能客服系统。系统能够理解用户意图、查询订单、跟踪物流、处理退款，并在必要时转接人工客服。

##  核心功能

| 功能模块 | 说明 | 状态 |
|---------|------|------|
|  用户管理 | 注册、登录、JWT Token认证 | ✅ |
|  智能问答 | 基于DeepSeek大模型的语义理解 | ✅ |
|  订单查询 | 查询订单状态、产品信息 | ✅ |
|  物流跟踪 | 查询快递物流轨迹 | ✅ |
|  退款处理 | 申请退款、业务规则校验 | ✅ |
|  转人工 | 情绪识别、自动创建工单 | ✅ |
|  会话管理 | 多轮对话、历史记录缓存 | ✅ |

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用户请求                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    API路由层 (routers/)                              │
│              接收请求、参数验证、返回响应                              │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Agent核心 (agent/)                                │
│         理解意图、决定工具、组织语言、多轮对话                         │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
        ┌───────────────────┐           ┌───────────────────┐
        │   直接回答         │           │   调用工具         │
        │   "您好！有什么    │           │   check_order      │
        │   可以帮您？"      │           │   check_shipping   │
        └───────────────────┘           │   apply_refund     │
                                        │   transfer_human   │
                                        └───────────────────┘
                                                    ↓
                                        ┌───────────────────┐
                                        │   数据层 (crud/)   │
                                        │   MySQL数据库      │
                                        └───────────────────┘
```

## 📁 项目结构

```
customer_service_agent/
│
├── .env                      #  配置文件（API密钥、数据库密码）
├── requirements.txt          #  依赖清单
├── config.py                 #  读取配置
├── database.py               #  数据库连接
├── init_db.py                #  数据库初始化脚本
├── main.py                   #  程序入口
│
├── models/                   #  数据模型
│   ├── base.py              # 基础模型 + 时间戳混入类
│   ├── user.py              # 用户表
│   ├── conversation.py      # 会话表
│   ├── message.py           # 消息表
│   ├── order.py             # 订单表
│   └── ticket.py            # 工单表
│
├── schemas/                  #  Pydantic模型
│   ├── user.py              # 注册/登录请求格式
│   └── chat.py              # 聊天请求/响应格式
│
├── crud/                     #  CRUD操作
│   ├── user.py              # 用户：注册、登录、认证
│   ├── conversation.py      # 会话：创建、查询、缓存更新
│   ├── message.py           # 消息：保存、查询
│   ├── order.py             # 订单：查询、退款更新
│   └── ticket.py            # 工单：创建
│
├── tools/                    #  Agent工具
│   ├── order_tools.py       # 订单查询、物流、退款的具体实现
│   └── agent_tools.py       # 工具映射表 + 给AI的说明书
│
├── agent/                    #  Agent核心
│   └── customer_agent.py    # 对话处理核心
│
├── routers/                  #  API路由
│   ├── user.py              # 用户注册/登录接口
│   └── chat.py              # 聊天接口
│
└── utils/                    # 🛠️ 工具函数
    └── auth.py              # 密码加密、Token生成
```

##  快速开始

### 环境要求

- Python 3.9+
- MySQL 5.7+
- DeepSeek API Key

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/pppyyz1233/customer_service_agent.git
cd customer_service_agent
```

#### 2. 创建虚拟环境

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=customer_service_agent
```

#### 5. 初始化数据库

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE customer_service_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 初始化表结构和测试数据
python init_db.py
```

#### 6. 启动服务

```bash
python main.py
```

服务启动后访问：
- **API文档**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

##  API 接口文档

### 用户管理

| 方法 | 路径 | 功能 | 请求体 |
|------|------|------|--------|
| POST | `/users/register` | 用户注册 | `{"username":"test","password":"123456"}` |
| POST | `/users/login` | 用户登录 | `{"username":"test","password":"123456"}` |

### 智能问答

| 方法 | 路径 | 功能 | 请求体 |
|------|------|------|--------|
| POST | `/api/chat` | 智能问答 | `{"session_id":"","message":"查订单ORD-001"}` |

##  使用示例

### 1. 注册用户

```bash
curl -X POST "http://127.0.0.1:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"张三","password":"123456"}'
```

**响应：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": 1,
    "username": "张三",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### 2. 智能问答

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"","message":"查询订单ORD-001"}'
```

**响应：**
```json
{
  "code": 200,
  "message": "问答成功",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "response": "订单ORD-001的商品是【机械键盘】，当前状态：已发货",
    "status": "success"
  }
}
```

### 3. 申请退款

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"xxx","message":"ORD-001质量有问题，我要退款"}'
```

## 🔧 核心机制详解

### Function Calling 工作流程

```
用户："查订单ORD-001"
    ↓
1. AI分析意图 → 需要调用 check_order_status 工具
    ↓
2. 返回：{"name": "check_order_status", "arguments": {"order_id": "ORD-001"}}
    ↓
3. 程序执行工具 → 查询数据库
    ↓
4. 把结果返回给AI
    ↓
5. AI生成回答："订单ORD-001已发货，预计2天后送达"
```

### Agent 核心循环

```python
while iteration < MAX_TOOL_ITERATIONS:
    # 1. 调用大模型
    response = client.chat.completions.create(...)
    
    # 2. 判断是否需要工具
    if not response.tool_calls:
        return response.content
    
    # 3. 执行工具
    for tool_call in response.tool_calls:
        result = await TOOL_MAP[tool_call.name](**args)
        messages.append({"role": "tool", "content": result})
    
    # 4. 继续循环
    iteration += 1
```

## 📊 数据库设计

### 核心表结构

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `users` | 用户表 | id, username, password |
| `conversation` | 会话表 | session_id, messages(缓存) |
| `messages` | 消息表 | conversation_id, role, content |
| `orders` | 订单表 | order_id, status, price |
| `tickets` | 工单表 | session_id, reason, status |

### 测试订单数据

| order_id | user_name | product_name | status | price |
|----------|-----------|--------------|--------|-------|
| ORD-001 | 张三 | 机械键盘 | 已发货 | 299.00 |
| ORD-002 | 李四 | 无线鼠标 | 已签收 | 99.00 |
| ORD-003 | 王五 | 4K显示器 | 处理中 | 1599.00 |

##  业务规则

### 退款业务规则

| 订单状态 | 是否可退款 | 提示信息 |
|---------|-----------|---------|
| 处理中 | ✅ 可以 | 直接退款 |
| 已发货 | ✅ 可以 | 等待收货后退款 |
| 已签收 | ⚠️ 有条件 | 需要先寄回商品 |
| 已退款 | ❌ 不可以 | 请勿重复申请 |

### 转人工触发条件

- 用户情绪激动（包含抱怨、愤怒词汇）
- 用户明确要求转人工
- 用户使用脏话
- 复杂投诉无法自动处理

## 🐛 常见问题

### 1. 密码字段长度不够

**错误：** `Data too long for column 'password'`

**解决：** 修改字段长度为255
```python
password: Mapped[str] = mapped_column(String(255), nullable=False)
```

### 2. Emoji 无法存储

**错误：** `Incorrect string value: '\xF0\x9F\x98\x8A'`

**解决：** 使用 utf8mb4 字符集
```sql
ALTER DATABASE customer_service_agent CHARACTER SET utf8mb4;
```

### 3. 外键找不到表

**错误：** `could not find table 'conversations'`

**解决：** 统一表名为单数
```python
ForeignKey("conversation.id", ondelete="CASCADE")
```

##  扩展开发

### 添加新工具

1. **在 `tools/order_tools.py` 中实现函数**

```python
async def check_product_detail(product_id: str):
    """查询产品详情"""
    async with AsyncSessionLocal() as session:
        # 查询逻辑
        return json.dumps({"status": "success", "data": {...}})
```

2. **在 `tools/agent_tools.py` 中注册**

```python
# 添加到映射表
TOOL_MAP["check_product_detail"] = check_product_detail

# 添加到工具描述
AGENT_TOOLS.append({
    "type": "function",
    "function": {
        "name": "check_product_detail",
        "description": "查询产品详细信息",
        "parameters": {...}
    }
})
```

## 📄 许可证

MIT License

## 👤 作者

**pppyyz1233**

- GitHub: [@pppyyz1233](https://github.com/pppyyz1233)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化异步Web框架
- [DeepSeek](https://deepseek.com/) - 强大的开源大语言模型
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL工具包

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
```


