
[app]

title = MY Calculator
package.name = mycalculator
package.domain = org.mycalculator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/my_icon.png

[buildozer]

log_level = 2
warn_on_root = 1

[android]

android.api = 35
android.minapi = 23
android.archs = arm64-v8a
