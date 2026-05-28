# 创建 README.md 文件
@'
# 🤖 智能客服系统

基于 RAG（检索增强生成）架构的企业级智能客服助手。

## ✨ 功能特性

- 🔐 **用户管理**：注册、登录、Token 认证
- 💬 **智能问答**：基于 DeepSeek 大模型的语义理解
- 📄 **文档解析**：支持 PDF、Word 文档上传和解析
- 🎫 **工单管理**：创建、查询、处理客服工单
- 📦 **订单查询**：快速查询订单状态和详情
- 💾 **对话历史**：保存所有对话记录，支持多轮交互

## 🏗️ 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 | MySQL + SQLAlchemy |
| 向量数据库 | ChromaDB |
| AI 模型 | DeepSeek Chat + DashScope Embedding |
| 文档解析 | pdfplumber + python-docx |
| 认证方式 | JWT Token |

## 📁 项目结构
