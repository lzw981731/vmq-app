# V免签监控端 (Android) v3.0.0

一款轻量级、高性能的 Android 通知监听及状态回传工具，专为 **V免签 (V-MQ)** 标准版协议定制。通过监听系统通知，实现个人码收款的实时回调。

## ✨ 核心特性

- **协议深度兼容**：完美对齐 TP5 标准版 V免签路由（`/appHeart` 和 `/appPush`）。
- **签名算法优化**：精准对齐服务端 MD5 签名逻辑，解决因金额格式化导致的“签名校验不通过”问题。
- **环境自检系统**：一键检测“监听权限”与“心跳服务”状态，并在日志中实时反馈。
- **智能日志管理**：
  - 自动保留最新的 20 条记录。
  - 修复日志重复叠加 Bug。
  - 支持自动滚动与一键复制。
- **UI/UX 改进**：
  - **分色显示**：配置数值采用灰色区分，界面更专业。
  - **双通道手动配置**：地址与密钥分开输入，大幅降低填错概率。
  - **沉浸式适配**：支持 HTTP/HTTPS 自动识别，User-Agent 修正防止请求闪退。
- **点击跳转**：右下角内嵌 [vipkj.net](https://www.vipkj.net) 快捷跳转。

## 🚀 快速上手

### 1. 安装与配置
- 在 [Releases](../../actions) 页面下载最新的 APK 并安装。
- **扫码配置**：扫描服务端提供的配置二维码。
- **手动配置**：点击首页“手动配置”按钮，分别输入您的通知地址和通讯密钥。示例地址：`https://your-domain.com`。

### 2. 权限授予
- 启动后按提示授予 **“通知使用权”**。
- 建议将本 App 加入 **“电池优化白名单”**，以确保后台长期稳定运行。

### 3. 连接测试
- 点击 **“检测心跳”**：确认 App 与服务端通信正常。
- 点击 **“检测监听”**：模拟推送测试，检查监听服务是否存活。

## 🛠 技术参数

- **心跳路由**：`GET /appHeart?t={time}&sign={sign}`
- **推送路由**：`GET /appPush?t={time}&type={type}&price={price}&sign={sign}`
- **签名逻辑**：`md5(type + priceStr + t + transMemo + key)`
  - `priceStr`：动态格式化金额（自动去除末尾多余的 0）。
- **User-Agent**：`V-MQ-Monitor/3.0.0 (Android)`

## 📦 自动构建 (GitHub Actions)

本项目已配置完善的 CI/CD 工作流。您可以分叉 (Fork) 本仓库后，在 **Actions** 标签下手动触发构建：

1. 进入 GitHub 项目的 **Actions** 页面。
2. 选择 **Build Android APK** 工作流。
3. 点击 **Run workflow**。
4. 构建完成后，在运行记录的 **Artifacts** 处下载生成的 APK。

## 📝 开发者说明

- **开发环境**：Android Studio / Java 11 / Gradle 6.7.1
- **核心组件**：OkHttp3, ZXing (扫码)
- **适配方案**：本项目针对老旧 Android 编译插件在现代 CI 环境下的 `NumberFormatException` 报错做了特殊处理。

---

**By [vipkj.net](https://www.vipkj.net)** 
*让支付回调更简单、更稳健。*
