# urszi.py

A python script to simplify the **U**ninstall **R**ecompile **S**ign **Z**ipalign **I**nstall cycle when reverse engineering Android applications.
It checks if `debuggable=true` is present in AndroidManifest.xml, and sets it if it's not. The signing is done using the debug keystore.

## Prerequisites

* [apktool](https://ibotpeaches.github.io/Apktool/)
* python3

## Usage

* Decompile the target apk
* Modify it as you like
* `python3 urszi.py <decompiled_folder>`
* Open the modified app and try it out, attach a debugger to it to see your logs, etc.

## License

MIT