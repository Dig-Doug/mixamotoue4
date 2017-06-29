import math
import os
import bpy
import mocap
import sys


def clear_scene():
  # Delete all objects
  while len(bpy.data.objects) > 0:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)


def get_fcurve(armature, bone_name):
  result = None
  for fcurve in armature.animation_data.action.fcurves:
    fcurve_split = fcurve.data_path.split('"')
    if fcurve_split[1] == bone_name and fcurve_split[2] == "].location":
      result = fcurve
      break
  return result


def import_fbx(in_file):
  # Load fbx
  bpy.ops.import_scene.fbx(filepath=in_file)


def export_fbx(in_file, out_dir):
  # Export as fbx
  file_no_path = os.path.basename(in_file)
  in_filename, extension = os.path.splitext(file_no_path)
  out_filename = in_filename + "_root" + extension
  out_fullpath = os.path.join(out_dir, out_filename)
  print("Exporting to:", out_fullpath)
  bpy.ops.export_scene.fbx(filepath=out_fullpath,
                           axis_forward='-Y',
                           axis_up='Z')


def convert_mesh():
  # Get armature and make active object
  armature = bpy.data.objects['Armature']

  # Rename to root
  # armature.name = 'root'
  # Create the root bone
  bpy.ops.object.mode_set(mode="EDIT")
  for bone in armature.data.edit_bones:
    if bone.parent == None:
      hip_bone = bone
      break
  root_bone = armature.data.edit_bones.new('root')
  root_bone.tail = hip_bone.head
  hip_bone.parent = root_bone

  return armature

def convert_anim():
  # Get armature and make active object
  armature = bpy.data.objects['Armature']
  bpy.context.scene.objects.active = armature

  # Run fix bvh and undo X rotation
  mocap.mocap_tools.rotate_fix_armature(armature.data)
  armature.rotation_euler = (0, 0, 0)

  # Create the root bone
  bpy.ops.object.mode_set(mode="EDIT")
  for bone in armature.data.edit_bones:
    if bone.parent == None:
      hip_bone = bone
      break
  root_bone = armature.data.edit_bones.new('root')
  root_bone.tail = hip_bone.head
  hip_bone.parent = root_bone

  # Switch to pose editing
  bpy.ops.object.mode_set(mode="POSE")
  scene = bpy.context.scene
  anim_root_bone = armature.pose.bones['root']
  anim_hip_bone = armature.pose.bones[hip_bone.name]

  # Create a initial keyframe for root bone
  scene.frame_set(1)
  anim_root_bone.keyframe_insert(data_path='location')

  # Get keyframes in animation
  hip_fcurve = get_fcurve(armature, hip_bone.name)
  frame_indices = []
  for point in hip_fcurve.keyframe_points[1:]:
    frame_indices.append(point.co[0])
  # Modify all keyframes except first
  for index in frame_indices:
    scene.frame_set(index)

    # Add hip location data to root
    anim_root_bone.location = anim_hip_bone.location
    anim_root_bone.keyframe_insert(data_path='location')

    # Remove location keyframe from hip
    anim_hip_bone.keyframe_delete(data_path='location')

  return armature

def rename_bones(armature):
  bone_map = {
    'Root': 'root',
    'Hips': 'pelvis',
    'Spine': 'spine_01',
    'Spine1': 'spine_02',
    'Spine2': 'spine_03',
    'Neck': 'neck_01',
    'Head': 'head',
    # 'HeadTop_End': '',
    'LeftShoulder': 'clavicle_l',
    'LeftArm': 'upperarm_l',
    'LeftForeArm': 'lowerarm_l',
    'LeftHand': 'hand_l',
    'LeftHandThumb1': 'thumb_01_l',
    'LeftHandThumb2': 'thumb_02_l',
    'LeftHandThumb3': 'thumb_03_l',
    # 'LeftHandThumb4': '',
    'LeftHandIndex1': 'index_01_l',
    'LeftHandIndex2': 'index_02_l',
    'LeftHandIndex3': 'index_03_l',
    # 'LeftHandIndex4': '',
    'LeftHandMiddle1': 'middle_01_l',
    'LeftHandMiddle2': 'middle_02_l',
    'LeftHandMiddle3': 'middle_03_l',
    # 'LeftHandMiddle4': '',
    'LeftHandRing1': 'ring_01_l',
    'LeftHandRing2': 'ring_02_l',
    'LeftHandRing3': 'ring_03_l',
    # 'LeftHandRing4': '',
    'LeftHandPinky1': 'pinky_01_l',
    'LeftHandPinky2': 'pinky_02_l',
    'LeftHandPinky3': 'pinky_03_l',
    # 'LeftHandPinky4': '',
    'RightShoulder': 'clavicle_r',
    'RightArm': 'upperarm_r',
    'RightForeArm': 'lowerarm_r',
    'RightHand': 'hand_r',
    'RightHandThumb1': 'thumb_01_r',
    'RightHandThumb2': 'thumb_02_r',
    'RightHandThumb3': 'thumb_03_r',
    # 'RightHandThumb4': '',
    'RightHandIndex1': 'index_01_r',
    'RightHandIndex2': 'index_02_r',
    'RightHandIndex3': 'index_03_r',
    # 'RightHandIndex4': '',
    'RightHandMiddle1': 'middle_01_r',
    'RightHandMiddle2': 'middle_02_r',
    'RightHandMiddle3': 'middle_03_r',
    # 'RightHandMiddle4': '',
    'RightHandRing1': 'ring_01_r',
    'RightHandRing2': 'ring_02_r',
    'RightHandRing3': 'ring_03_r',
    # 'RightHandRing4': '',
    'RightHandPinky1': 'pinky_01_r',
    'RightHandPinky2': 'pinky_02_r',
    'RightHandPinky3': 'pinky_03_r',
    # 'RightHandPinky4': '',
    'LeftUpLeg': 'thigh_l',
    'LeftLeg': 'calf_l',
    'LeftFoot': 'foot_l',
    'LeftToeBase': 'ball_l',
    # 'LeftToe_End': '',
    'RightUpLeg': 'thigh_r',
    'RightLeg': 'calf_r',
    'RightFoot': 'foot_r',
    'RightToeBase': 'ball_r',
    # 'RightToe_End': '',
  }

  bpy.context.scene.objects.active = armature

  bpy.ops.object.mode_set(mode="EDIT")
  for bone in armature.data.edit_bones:
    bone_name = bone.name

    # Fix bones with name's like 'swat:Hips'
    if ':' in bone_name:
      bone_name = bone_name.split(':')[-1]

    if bone_name in bone_map:
      bone.name = bone_map[bone_name]


# Get command line args after '--'
argv = sys.argv
argv = argv[argv.index("--") + 1:]

# Mesh or animation
file_is_mesh = argv[0] == "mesh"
# File to convert
file = argv[1]
# Output directory
out_dir = argv[2]

print("Converting:", file)

clear_scene()
import_fbx(file)

armature = None
if file_is_mesh:
  armature = convert_mesh()
else:
  armature = convert_anim()

rename_bones(armature)

export_fbx(file, out_dir)
