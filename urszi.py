#!/usr/bin/python3

import argparse
import subprocess
from subprocess import CalledProcessError
import os
import pathlib
from pathlib import Path

#arg parsing
arg_parser = argparse.ArgumentParser( description = "Recompile, sign and zipalign app folder" )
arg_parser.add_argument( "source_folder" )
arguments = arg_parser.parse_args()

home = str(Path.home())
app_folder = arguments.source_folder
app_name = pathlib.PurePath(app_folder).name
adb_path = f'{home}/Library/Android/sdk/platform-tools/adb'

manifest = open(app_folder + "/AndroidManifest.xml", "r")
manifest_content = manifest.read()

#get package name
app_pkg_name = manifest_content.split('package="')[1].split('"')[0]

#fix debuggable attribute
if 'android:debuggable="true"' in manifest_content:
    print("Manifest already has debuggable attribue")
    manifest.close()
else:
    manifest.close()
    manifest = open(app_folder + "/AndroidManifest.xml", "w")
    print("Manifest needs debuggable fixup. Setting it to true...")
    manifest_content = manifest_content.replace('<application ', '<application android:debuggable="true" ')
    manifest.write(manifest_content)
    manifest.close()

recompiled_apk_name = "app-aligned.apk"

#pre-clean
try:
    os.remove(recompiled_apk_name)
except FileNotFoundError:
    pass


build_tools_path = f'{home}/Library/Android/sdk/build-tools'
built_apk_path = f'{app_folder}/dist/{app_name}.apk'
debug_keystore_path = f'{home}/.android/debug.keystore'

#execute 
try:
    subprocess.check_call([adb_path, "uninstall", app_pkg_name])
except CalledProcessError:
    pass

subprocess.check_call(["apktool", "b", "--use-aapt2", app_folder])
subprocess.run(["jarsigner", "-verbose", "-sigalg", "SHA1withRSA", "-digestalg", "SHA1", "-keystore", debug_keystore_path, built_apk_path, "androiddebugkey"], stdout=subprocess.PIPE, input='android', encoding='ascii')
zipalign_path = subprocess.check_output(["find", build_tools_path, "-name", "zipalign"], encoding='UTF-8')
zipalign_path = zipalign_path.split('\n')[0]
subprocess.check_call([zipalign_path, "-p", "4", built_apk_path, recompiled_apk_name])
subprocess.check_call([adb_path, "install", recompiled_apk_name])

