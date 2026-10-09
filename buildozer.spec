[app]
title = ScanApp
package.name = scanapp
package.domain = org.scanapp
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.api = 30
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25c
android.ndk_path = /home/user/.buildozer/android/platform/android-ndk-r25c

[buildozer]
allow_root = 1
log_level = 2
