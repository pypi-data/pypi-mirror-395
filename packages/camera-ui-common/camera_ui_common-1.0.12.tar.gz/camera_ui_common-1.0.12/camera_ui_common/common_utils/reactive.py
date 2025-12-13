"""Reactive property utilities."""

from __future__ import annotations

from copy import deepcopy
from typing import Generic, TypeVar, cast

from camera_ui_sdk import HybridObservable
from reactivex import operators as ops
from reactivex.subject import BehaviorSubject

T = TypeVar("T")


class ReactiveProperty(Generic[T]):
    """A reactive property that wraps a BehaviorSubject with observable access."""

    __subject: BehaviorSubject[T]
    observable: HybridObservable[T]

    def __init__(
        self, initial_value: T | BehaviorSubject[T], observable: HybridObservable[T] | None = None
    ) -> None:
        if isinstance(initial_value, BehaviorSubject):
            self.__subject = cast(BehaviorSubject[T], initial_value)
        else:
            self.__subject = BehaviorSubject(initial_value)

        self.observable = observable or self.__create_state_observable(self.__subject)

    @property
    def value(self) -> T:
        val = self.__subject.value

        if isinstance(val, dict | list) or hasattr(val, "__dict__"):
            return deepcopy(val)  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]

        return val

    def next(self, value: T) -> None:
        self.__subject.on_next(value)

    def complete(self) -> None:
        self.__subject.on_completed()

    def __create_state_observable(self, state_subject: BehaviorSubject[T]) -> HybridObservable[T]:
        return HybridObservable(state_subject.pipe(ops.distinct_until_changed(), ops.share()))
