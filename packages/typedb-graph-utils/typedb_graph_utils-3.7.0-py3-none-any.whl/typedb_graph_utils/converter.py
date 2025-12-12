from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from typedb.analyze import Pipeline, Constraint
from typedb.driver import ConceptRow
from .data_constraint import (
    DataConstraint,
    Isa, Has, Links, Is, Is, Iid,
    Sub, Owns, Relates, Plays, Label, Kind, Value,
    Expression, FunctionCall, Comparison,
)

OutputType = TypeVar("OutputType")


class TypeDBAnswerConverter(ABC, Generic[OutputType]):
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def add_answer(self, answer_index: Optional[int], row: ConceptRow):
        involved_conjunctions = [self.pipeline.conjunction(i) for i in row.involved_conjunctions()]
        involved_constraints = [constraint for conjunction in involved_conjunctions for constraint in
                                conjunction.constraints()]
        data_constraints_with_none = [DataConstraint.of(self.pipeline, constraint, answer_index, row) for constraint in
                                      involved_constraints]
        data_constraints = [dc for dc in data_constraints_with_none if dc]
        for dc in data_constraints:
            self._add_constraint(dc)

    def _add_constraint(self, constraint: DataConstraint):
        if constraint.is_isa():
            self.add_isa(constraint.as_isa())
        elif constraint.is_has():
            self.add_has(constraint.as_has())
        elif constraint.is_links():
            self.add_links(constraint.as_links())
        elif constraint.is_sub():
            self.add_sub(constraint.as_sub())
        elif constraint.is_owns():
            self.add_owns(constraint.as_owns())
        elif constraint.is_relates():
            self.add_relates(constraint.as_relates())
        elif constraint.is_plays():
            self.add_plays(constraint.as_plays())
        elif constraint.is_function_call():
            self.add_function_call(constraint.as_function_call())
        elif constraint.is_expression():
            self.add_expression(constraint.as_expression())
        elif constraint.is_is():
            self.add_is(constraint.as_is())
        elif constraint.is_iid():
            self.add_iid(constraint.as_iid())
        elif constraint.is_comparison():
            self.add_comparison(constraint.as_comparison())
        elif constraint.is_kind_of():
            self.add_kind(constraint.as_kind())
        elif constraint.is_label():
            self.add_label(constraint.as_label())
        elif constraint.is_value():
            self.add_value(constraint.as_value())
        else:
            raise TypeError("Unsupported constraint variant: %s" % (type(constraint),))

    @abstractmethod
    def finish(self) -> OutputType:
        pass

    @abstractmethod
    def add_isa(self, isa: Isa):
        pass

    @abstractmethod
    def add_has(self, has: Has):
        pass

    @abstractmethod
    def add_links(self, links: Links):
        pass

    @abstractmethod
    def add_sub(self, sub: Sub):
        pass

    @abstractmethod
    def add_owns(self, owns: Owns):
        pass

    @abstractmethod
    def add_relates(self, relates: Relates):
        pass

    @abstractmethod
    def add_plays(self, plays: Plays):
        pass

    @abstractmethod
    def add_function_call(self, fc: FunctionCall):
        pass

    @abstractmethod
    def add_expression(self, expr: Expression):
        pass

    @abstractmethod
    def add_is(self, is_c: Is):
        pass

    @abstractmethod
    def add_iid(self, iid: Iid):
        pass

    @abstractmethod
    def add_comparison(self, comp: Comparison):
        pass

    @abstractmethod
    def add_kind(self, kind: Kind):
        pass

    @abstractmethod
    def add_label(self, label: Label):
        pass

    @abstractmethod
    def add_value(self, value: Value):
        pass
