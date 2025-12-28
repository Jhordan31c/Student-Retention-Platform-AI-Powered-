"""Core module exports"""
from app.core.config import settings
from app.core.lifespan import lifespan, MLModels

__all__ = ["settings", "lifespan", "MLModels"]