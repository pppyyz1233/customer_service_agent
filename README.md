#  智能客服Agent系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange.svg)](https://deepseek.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-red.svg)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于 **RAG（检索增强生成）** 和 **Function Calling** 架构的企业级智能客服系统。系统能够理解用户意图、查询订单、跟踪物流、处理退款，并在必要时转接人工客服。

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

##  系统架构
