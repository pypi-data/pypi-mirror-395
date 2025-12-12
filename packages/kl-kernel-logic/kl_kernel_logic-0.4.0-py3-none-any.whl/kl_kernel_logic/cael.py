# cael.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, List, Mapping, Optional, Sequence, Tuple, TypeVar

from .psi import PsiDefinition
from .kernel import Kernel, ExecutionTrace

T = TypeVar("T")


@dataclass(frozen=True)
class CaelResult(Generic[T]):
    """
    Aggregated result of a CAEL pipeline.

    Contract:
    - traces: ordered list of ExecutionTrace objects (one per step)
    - success: False if any step fails
    - final_output: output of the last successful step or None
    """

    traces: List[ExecutionTrace[Any]]
    final_output: Optional[T]
    success: bool


class CAEL:
    """
    Composable Atomic Execution Layer.

    Responsibilities:
    - execute a sequence of steps via a single Kernel instance
    - each step is defined as (psi, task, kwargs)
    - no governance, routing or retry logic
    """

    def __init__(self, kernel: Kernel) -> None:
        self._kernel = kernel

    def run(
        self,
        steps: Sequence[
            Tuple[
                PsiDefinition,
                Callable[..., Any],
                Mapping[str, Any],  # kwargs for the task
            ]
        ],
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> CaelResult[Any]:
        """
        Execute all steps in order using the kernel.

        Each step:
        - uses its PsiDefinition
        - calls task(**kwargs)
        - generates an ExecutionTrace through Kernel.execute
        """
        traces: List[ExecutionTrace[Any]] = []
        last_output: Any = None
        pipeline_success = True

        for psi, task, kwargs in steps:
            trace = self._kernel.execute(
                psi=psi,
                task=task,
                metadata=metadata,
                **dict(kwargs),
            )
            traces.append(trace)

            if not trace.success:
                pipeline_success = False
                last_output = None
                break

            last_output = trace.output

        return CaelResult(
            traces=traces,
            final_output=last_output,
            success=pipeline_success,
        )
