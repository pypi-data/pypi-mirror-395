"""
Geode-Hybrid_Geosciences Python binding for Pillar
"""
from __future__ import annotations
import opengeode.bin.opengeode_py_basic
__all__: list[str] = ['HybridGeosciencesPillarLibrary', 'PillarStructuralModelBuilder', 'PillarStructuralModelBuilderResult', 'PillarStructuralModelInspectionResult', 'PillarStructuralModelOptions']
class HybridGeosciencesPillarLibrary:
    @staticmethod
    def initialize() -> None:
        ...
class PillarStructuralModelBuilder:
    def build(self, arg0: PillarStructuralModelOptions) -> PillarStructuralModelBuilderResult:
        ...
    def is_model_construction_possible(self) -> PillarStructuralModelInspectionResult:
        ...
class PillarStructuralModelBuilderResult:
    slice_collection_order: list[opengeode.bin.opengeode_py_basic.uuid]
class PillarStructuralModelInspectionResult:
    def string(self) -> str:
        ...
class PillarStructuralModelOptions:
    add_block_mesh: bool
