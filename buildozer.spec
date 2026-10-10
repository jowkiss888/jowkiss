[app]
title = 扫码采集
package.name = samplerecord
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttc,ttf
source.include_patterns = fonts/*.ttc
version = 0.1
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,openssl
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.manifest.extra = android:usesCleartextTraffic="true"
