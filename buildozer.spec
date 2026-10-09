[app]
# 应用名称
title = 扫码采集

# 包名，必须全小写，且不能有空格
package.name = scanapp
package.domain = org.jowkiss

# 源文件目录
source.dir = .

# 包含的文件后缀
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 0.1

# --- 核心依赖（已移除 pymssql，添加了 requests 用于网络请求）---
requirements = python3,kivy==2.3.0

# 屏幕方向：竖屏
orientation = portrait

# 全屏设置（0表示保留状态栏，1表示全屏）
fullscreen = 0

# --- 关键权限：必须加上 INTERNET 权限，否则无法连接网络/数据库 ---
android.permissions = INTERNET

# --- Android API 和 NDK 版本 ---
android.api = 33
android.minapi = 21
android.ndk = 25b

# 打包的 CPU 架构（arm64-v8a 足以覆盖绝大多数现代手机，且能大幅缩短编译时间）
android.archs = arm64-v8a

# --- 极其关键：自动接受 SDK 许可，否则云端编译会卡死 ---
android.accept_sdk_license = True

[buildozer]
# 日志级别
log_level = 2
warn_on_root = 0