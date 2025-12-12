# kernel.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Callable, Generic, Mapping, Optional, TypeVar
import uuid

from .psi import PsiDefinition

T = TypeVar("T")

Metadata = Mapping[str, Any]
RunIdFactory = Callable[[], str]
NowProvider = Callable[[], datetime]
PerfCounterProvider = Callable[[], float]


@dataclass(frozen=True)
class ExecutionTrace(Generic[T]):
    """
    Immutable record of one kernel execution.

    Contract:
    - Never mutated after creation.
    - Field names and meanings are stable.
    """

    run_id: str
    psi: PsiDefinition

    started_at: datetime
    finished_at: datetime
    runtime_ms: float

    success: bool
    output: Optional[T]
    error: Optional[str]
    exception_type: Optional[str]
    exception_repr: Optional[str]

    metadata: Metadata = field(default_factory=dict)


class Kernel:
    """
    Minimal deterministic execution engine.

    Contract:
    - execute calls the task exactly once.
    - execute never raises, exceptions are captured in the trace.
    - Time is measured via a monotonic clock.
    - metadata is passed through and not interpreted.
    """

    def __init__(
        self,
        *,
        run_id_factory: Optional[RunIdFactory] = None,
        now_provider: Optional[NowProvider] = None,
        perf_counter_provider: Optional[PerfCounterProvider] = None,
    ) -> None:
        self._run_id_factory: RunIdFactory = (
            run_id_factory or (lambda: uuid.uuid4().hex)
        )
        self._now_provider: NowProvider = (
            now_provider or (lambda: datetime.now(timezone.utc))
        )
        self._perf_counter: PerfCounterProvider = perf_counter_provider or perf_counter

    def execute(
        self,
        *,
        psi: PsiDefinition,
        task: Callable[..., T],
        metadata: Optional[Metadata] = None,
        **kwargs: Any,
    ) -> ExecutionTrace[T]:
        """
        Execute task once and return a trace. Never raises.
        """
        started_at = self._now_provider()
        start = self._perf_counter()

        success = False
        output: Optional[T] = None
        error: Optional[str] = None
        exc_type: Optional[str] = None
        exc_repr: Optional[str] = None

        try:
            output = task(**kwargs)
            success = True
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
            exc_type = exc.__class__.__name__
            exc_repr = repr(exc)

        finished_at = self._now_provider()
        end = self._perf_counter()

        runtime_ms = max((end - start) * 1000.0, 0.0)
        run_id = self._run_id_factory()

        trace_metadata: dict[str, Any] = dict(metadata) if metadata is not None else {}

        return ExecutionTrace(
            run_id=run_id,
            psi=psi,
            started_at=started_at,
            finished_at=finished_at,
            runtime_ms=runtime_ms,
            success=success,
            output=output,
            error=error,
            exception_type=exc_type,
            exception_repr=exc_repr,
            metadata=trace_metadata,
        )
