#!/usr/bin/python

import os
import subprocess
import sys
import glob

# Command to execute blender. On linux, this is probably just 'blender'
blender_command = "cd C:\\Program Files\\Blender Foundation\\Blender && blender"

# Path to conversion script
script_dir = os.path.dirname(os.path.abspath(__file__))
convert_script = os.path.join(script_dir, "convert_mixamo.py")

# Directory of source animation FBX files
anim_dir = "C:\\Users\\Doug\\Development\\grid\\mixamo\\animations"
# Directory to output converted animation FBX files
anim_out_dir = "C:\\Users\\Doug\\Development\\grid\\mixamo\\animations_root"
# Directory of source mesh FBX files
mesh_dir = "C:\\Users\\Doug\\Development\\grid\\mixamo\\meshes"
# Directory to output converted mesh FBX files
mesh_out_dir = "C:\\Users\\Doug\\Development\\grid\\mixamo\\meshes_root"


def run_blender_command(file_type, input_file, out_dir):
  command_args = [
    blender_command,
    '--background',
    '--python',
    convert_script,
    '--',
    file_type,
    input_file,
    out_dir
  ]
  command = ' '.join(command_args)
  status = os.system(command)
  if status != 0:
    print("Error: " + input_file)


# Convert all animation fbx files
print("Converting animations...")
for file in glob.glob(os.path.join(anim_dir, "*.fbx")):
  run_blender_command("anim", file, anim_out_dir)

# Convert all mesh fbx files
print("Converting meshes...")
for file in glob.glob(os.path.join(mesh_dir, "*.fbx")):
  run_blender_command("mesh", file, mesh_out_dir)
