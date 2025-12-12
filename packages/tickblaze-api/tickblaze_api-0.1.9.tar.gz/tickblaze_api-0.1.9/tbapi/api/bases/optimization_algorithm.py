






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import OptimizationAlgorithm as _OptimizationAlgorithm
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.script import Script
if TYPE_CHECKING:
    from tbapi.api.bases.optimization_vector import OptimizationVector

@tb_interface(_OptimizationAlgorithm)
class OptimizationAlgorithm(Script):

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for OptimizationAlgorithm. Use overloads for IDE type hints."""
        return OptimizationAlgorithm(*args, **kwargs)

    @property
    def max_optimizations(self) -> int:
        """The number of optimization vectors that the algorithm will select and run if the optimization process runs to completion."""
        val = self._value.MaxOptimizations
        return val
    @property
    def optimization_parameters(self) -> IReadOnlyList:
        val = self._value.OptimizationParameters
        return val
    @optimization_parameters.setter
    def optimization_parameters(self, val: IReadOnlyList):
        tmp = self._value
        tmp.OptimizationParameters = val
        self._value = tmp
    @property
    def vectors(self) -> IReadOnlyList:
        val = self._value.Vectors
        return val
    @vectors.setter
    def vectors(self, val: IReadOnlyList):
        tmp = self._value
        tmp.Vectors = val
        self._value = tmp

    @abstractmethod
    def get_next_vectors_to_run(self, max_count: int) -> list[OptimizationVector]:
        result = self._value.GetNextVectorsToRun(max_count)
        return result
  
    def on_vector_processed(self, vector: OptimizationVector) -> None:
        result = self._value.OnVectorProcessed(vector._value)
        return result
  


