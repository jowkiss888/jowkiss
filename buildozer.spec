[app]
title = 扫码采集
package.name = samplerecord
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0

# --- 核心修复：锁定兼容的NDK和API版本 ---
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
# -----------------------------------------

android.manifest.extra = android:usesCleartextTraffic="true"
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
