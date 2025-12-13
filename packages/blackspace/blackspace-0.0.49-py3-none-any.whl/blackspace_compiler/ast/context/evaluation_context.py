from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable

from ..node import AstNode
from .function_registry import FunctionRegistry
from .issue_level import IssueLevel
from .label_registry import LabelRegistry


@dataclass
class Issue:
    level: IssueLevel
    node: AstNode
    message: str


@contextmanager
def increment_stack(context: EvaluationContext, by: int = 1):
    try:
        context._stack_offset += by
        yield
    finally:
        context._stack_offset -= by


@contextmanager
def reset_stack(context: EvaluationContext):
    try:
        original_offset = context._stack_offset
        context._stack_offset = 0
        yield
    finally:
        if context._stack_offset != 0:
            raise RuntimeError("Stack offset must be zero when exiting reset_stack context")
        context._stack_offset = original_offset


class EvaluationContext:
    def __init__(self) -> None:
        self.label_registry = LabelRegistry()
        self.function_registry = FunctionRegistry()

        self._issues: list[Issue] = []
        self._stack_offset = 0

    def register_issue(self, level: IssueLevel, node: AstNode, message: str) -> None:
        self._issues.append(Issue(level, node, message))

    def with_incremented_stack(self, fn: Callable[[EvaluationContext], str]) -> str:
        with increment_stack(self):
            return fn(self)

    @property
    def stack_offset(self) -> int:
        return self._stack_offset

    def print_issues(self, strict: bool = False) -> None:
        has_warnings = False
        has_errors = False

        for issue in self._issues:
            print(f"[{issue.level.name}] {issue.message} (at {issue.node})")

            if issue.level == IssueLevel.ERROR:
                has_errors = True
            elif issue.level == IssueLevel.WARNING:
                has_warnings = True

        if has_errors:
            raise RuntimeError("Compilation failed due to errors.")
        if strict and has_warnings:
            raise RuntimeError("Compilation failed due to warnings in strict mode.")
