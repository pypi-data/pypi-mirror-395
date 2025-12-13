from typing import Set

_3D_MODEL_EXTENSIONS: Set[str] = {
    ".stl", ".obj", ".fbx", ".gltf", ".glb", ".3ds", ".max", ".blend",
}

def is_3d_model_file(filename: str) -> bool:
    """
    Checks if a filename has a common 3D model file extension.

    Args:
        filename: The filename to check.

    Returns:
        True if the filename has a 3D model extension, False otherwise.
    """
    return any(filename.lower().endswith(ext) for ext in _3D_MODEL_EXTENSIONS)