"""Dependency Injection framework for Funcy Bear."""

from funcy_bear.context.di.container import DeclarativeContainer
from funcy_bear.context.di.plugin_containers import LifecycleContainer, ToolContainer
from funcy_bear.context.di.plugins import Deleter, Factory, Getter, Setter, ToolContext, inject_tools
from funcy_bear.context.di.provides import Provide, Provider
from funcy_bear.context.di.resources import Resource, Singleton
from funcy_bear.context.di.wiring import inject, parse_params

__all__ = [
    "DeclarativeContainer",
    "Deleter",
    "Factory",
    "Getter",
    "LifecycleContainer",
    "Provide",
    "Provider",
    "Resource",
    "Setter",
    "Singleton",
    "ToolContainer",
    "ToolContext",
    "inject",
    "inject_tools",
    "parse_params",
]
