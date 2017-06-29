# Mixamo to UE4
A blender script that adds root bones to FBX files from Mixamo for use in Unreal Engine 4 with root motion.

Automates the approach described in this [tutorial](https://www.youtube.com/watch?v=AYlonUyPong).

This script also renames bones to match the UE4 naming conventions.

## Usage
To run `convert_mixamo.py` in blender, use the following command:
```bash
# Command syntax:
blender --background --python <path to convert_mixamo> -- <mesh or anim> <path to input file> <path to out dir>
# Example:
blender --background --python "path/to/convert_mixamo.py" -- mesh mychar.fbx converted
```

The `run_batch.py` script is an example of how to convert a folder full of meshes and animations.

## Contributing
Bug fixes, documentation improvements, etc. are welcome :)
