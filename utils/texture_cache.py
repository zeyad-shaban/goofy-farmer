"""Texture caching system for item icons."""

from typing import Dict, Optional
from OpenGL.GL import *
import pygame


class TextureCache:
    """Cache and manage textures for items."""
    
    _cache: Dict[str, int] = {}
    
    @classmethod
    def get_texture(cls, texture_path: str) -> Optional[int]:
        """Load and cache a texture, return texture ID."""
        # Return cached texture if available
        if texture_path in cls._cache:
            return cls._cache[texture_path]
        
        try:
            # Load image
            image = pygame.image.load(texture_path)
            image_data = pygame.image.tostring(image, "RGBA", True)
            
            # Create OpenGL texture
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA,
                image.get_width(), image.get_height(),
                0, GL_RGBA, GL_UNSIGNED_BYTE, image_data
            )
            glBindTexture(GL_TEXTURE_2D, 0)
            
            # Cache it
            cls._cache[texture_path] = texture_id
            return texture_id
        except Exception as e:
            print(f"Failed to load texture {texture_path}: {e}")
            return None
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached textures."""
        for texture_id in cls._cache.values():
            glDeleteTextures([texture_id])
        cls._cache.clear()
