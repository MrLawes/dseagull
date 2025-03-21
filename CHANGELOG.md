# Changelog

所有版本的更新记录和重要变更。

## 0.0.28 (2025-03-20)

### 新增

* 接口 500 异常的报错, 支持发送的钉钉. settings 配置 DJANGO_REQUEST_ERROR_WEBHOOK

## 0.0.27 (2025-02-05)

### 新增

* 增加中间件 BaseMiddleware, 用于基本的请求日志输出

## 0.0.19 (2025-02-13)

### 新增

* 提供新的 Command 命令: python manage.py startmodel -n Apple

## 0.0.15 (2025-02-12)

### 新增

* 提供基础模型 BaseModel
* 提供基础查询过滤对象 BaseFilterSet

## 0.0.12 (2025-02-05)

### 新增

* 增加中间件 LoggerMiddleware, 用于收集输出日志的字段,比如 ip, request_id 等

## 0.0.8 (2025-01-03)

### 新增

* 默认指定 TEST_REQUEST_DEFAULT_FORMAT 为 json
* 默认指定 DEFAULT_RENDERER_CLASSES 为 ('rest_framework.renderers.JSONRenderer',)

## 0.0.7 (2025-01-02)

### 新增

* 默认 REST_FRAMEWORK 配置支持 ordering; seach; filter

## 0.0.6 (2024-12-30)

### 新增

* 默认 OpenAPI 规范文档类为 rest_framework.schemas.coreapi.AutoSchema
* 默认每页 10 条数据

## 0.0.5 (2024-12-26)

### 新增

* 对称加密的 JWT 模块

## 0.0.4 (2024-12-24)

### 新增

* 默认统一的分页格式

## 0.0.3 (2024-12-12)

### 新增

* 在中文环境下, serializers.Field 的 required 提示:这个字段是必填项。 变为:{help_text}:这个字段是必填项。
* 在中文环境下, serializers.Field 的 null 提示:This field may not be null. 变为:{help_text}:不能为空。
* 在中文环境下, serializers.Field 的 blank 提示:This field may not be blank. 变为:{help_text}:不能为空白。
