# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-09

### Added

#### 核心功能
- ✨ 实现主客户端 `OomolConnectClient`
- ✨ 实现 Tasks API 客户端（核心模块）
- ✨ 实现 Flows API 客户端
- ✨ 实现 Blocks API 客户端
- ✨ 实现 Packages API 客户端

#### 智能轮询系统
- ✨ 实现指数退避轮询算法
- ✨ 实现固定间隔轮询模式
- ✨ 支持超时控制
- ✨ 支持进度回调
- ✨ 支持日志实时流式处理
- ✨ 自动去重日志（通过 lastLogId）

#### 任务管理
- ✨ `list()` - 列出所有任务
- ✨ `create()` - 创建任务（JSON 格式）
- ✨ `create_with_files()` - 创建任务（支持文件上传）
- ✨ `get()` - 获取任务详情
- ✨ `stop()` - 停止任务
- ✨ `get_logs()` - 获取任务日志
- ✨ `wait_for_completion()` - 智能轮询等待
- ✨ `create_and_wait()` - 创建并等待完成
- ✨ `run()` - 一步运行并获取结果（推荐方法）
- ✨ `run_with_files()` - 一步运行（含文件上传）

#### 文件上传
- ✨ 支持单文件上传
- ✨ 支持多文件批量上传
- ✨ 自动 FormData 处理

#### 输入值处理
- ✨ 支持对象格式输入（最简单）
- ✨ 支持数组格式输入
- ✨ 支持节点格式输入（多节点场景）
- ✨ 自动规范化输入值

#### 错误处理
- ✨ `OomolConnectError` - 基础错误类
- ✨ `ApiError` - HTTP API 错误
- ✨ `TaskFailedError` - 任务执行失败错误
- ✨ `TaskStoppedError` - 任务被停止错误
- ✨ `TimeoutError` - 轮询超时错误
- ✨ `InstallFailedError` - 包安装失败错误

#### 类型系统
- ✨ 完整的 TypedDict 类型定义
- ✨ Literal 类型用于字符串联合类型
- ✨ Enum 类型用于枚举
- ✨ 30+ 类型定义，支持完整的 IDE 自动补全

#### 包管理
- ✨ `list()` - 列出已安装包
- ✨ `install()` - 安装包
- ✨ `list_install_tasks()` - 列出安装任务
- ✨ `get_install_task()` - 获取安装任务详情
- ✨ `wait_for_install_completion()` - 轮询等待安装完成
- ✨ `install_and_wait()` - 安装并等待完成

#### 文档
- 📚 完整的 README.md（API 参考）
- 📚 QUICKSTART.md（快速入门指南）
- 📚 COMPARISON.md（TypeScript 版本对比）
- 📚 PROJECT_SUMMARY.md（项目总结）
- 📚 CONTRIBUTING.md（开发者指南）

#### 示例代码
- 📝 basic_usage.py - 基础使用示例
- 📝 advanced_usage.py - 高级使用示例

#### 测试
- ✅ 单元测试框架
- ✅ 工具函数测试
- ✅ pytest 配置

### Technical Details

#### 依赖项
- Python >= 3.8
- httpx >= 0.27.0（异步 HTTP 客户端）

#### 开发工具
- pytest >= 7.0.0（测试框架）
- pytest-asyncio >= 0.21.0（异步测试支持）
- mypy >= 1.0.0（类型检查）
- black >= 23.0.0（代码格式化）
- isort >= 5.12.0（导入排序）
- flake8 >= 6.0.0（代码检查）

#### 特性
- ✨ 完全异步设计（基于 asyncio）
- ✨ 支持异步上下文管理器
- ✨ 完整的类型注解（mypy 兼容）
- ✨ 100% API 对等 TypeScript 版本
- ✨ 连接池和资源自动管理
- ✨ 详细的错误信息和堆栈追踪

#### 代码质量
- 📊 1,304 行核心代码
- 📊 2,567 行总代码（含示例和测试）
- 📊 8 个核心模块
- 📊 30+ 类型定义
- 📊 20+ API 方法
- 📊 6 种错误类型

### Notes

这是 Oomol Connect SDK Python 版本的首个正式发布版本。

该 SDK 完全镜像了 TypeScript 版本的功能和 API 设计，提供了：
- 完整的 API 覆盖
- 智能轮询系统
- 类型安全
- 异步优先
- 文件上传支持
- 详细的错误处理
- 完善的文档

## [Unreleased]

### Planned
- 🔮 添加更多单元测试
- 🔮 添加集成测试
- 🔮 添加性能基准测试
- 🔮 支持 Python 3.13
- 🔮 添加更多示例代码

---

[1.0.0]: https://github.com/oomol/oomol-connect-sdk-py/releases/tag/v1.0.0
