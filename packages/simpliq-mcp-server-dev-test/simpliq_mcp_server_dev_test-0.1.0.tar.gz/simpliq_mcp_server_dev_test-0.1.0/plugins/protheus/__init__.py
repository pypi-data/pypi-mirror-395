# -*- coding: utf-8 -*-
"""
Protheus TOTVS Semantic Mapping Plugin for SimpliQ MCP Server

This plugin provides automatic semantic mapping generation from
Protheus TOTVS data dictionary (SX2, SX3, SIX tables).

Author: SimpliQ Development Team
Date: 2025-11-18
"""

from .protheus_mapper import ProtheusMapperPlugin

__all__ = ['ProtheusMapperPlugin']
