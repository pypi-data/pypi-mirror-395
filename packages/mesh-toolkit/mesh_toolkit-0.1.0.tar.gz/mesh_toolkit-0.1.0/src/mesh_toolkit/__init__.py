"""Mesh Toolkit - Python SDK for Meshy AI 3D generation API.

Usage:
    from mesh_toolkit import text3d, rigging, animate, retexture

    # Generate a model
    model = text3d.generate("a medieval sword")
    print(model.model_urls.glb)

    # Rig it for animation
    rigged = rigging.rig(model.id)

    # Apply an animation
    animated = animate.apply(rigged.id, animation_id=0)

    # Or retexture it
    retextured = retexture.apply(model.id, "golden with gems")
"""

from . import animate, base, retexture, rigging, text3d
from .base import MeshyAPIError, RateLimitError

__all__ = [
    # Errors
    "MeshyAPIError",
    "RateLimitError",
    # API modules
    "animate",
    "base",
    "retexture",
    "rigging",
    "text3d",
]
