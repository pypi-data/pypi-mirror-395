from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type as ClassType, Any, List, Optional, Union


@dataclass
class ControllerDef:
    name: str
    uses: List[QualifiedName]
    provides: List[QualifiedName]
    requires: List[QualifiedName]
    connections: List[Connection]
    machines: List[Union[StateMachineDef, StateMachineRef]]
    events: List[Event]
    operations: List[Operation]
    variables: List[Variable]
    parent: Any


@dataclass
class Connection:
    source: QualifiedName
    event_source: QualifiedName
    target: QualifiedName
    event_target: QualifiedName
    asynchronous: bool
    bidirectional: bool
    parent: Any


@dataclass
class StateMachineRef:
    name: str
    ref: QualifiedName
    parent: Any


@dataclass
class Operation:
    operation: Union[OperationRef, OperationDef]
    parent: Any


@dataclass
class OperationRef:
    name: str
    ref: QualifiedName
    parent: Any


@dataclass
class Variable:
    name: str
    type: Type
    parent: Any
    initial: Optional[Expression] = None
    modifier: Optional[VariableModifier] = None


@dataclass
class Expression:
    expression: Union[ForAll, Exists, LambdaExp, Iff]
    parent: Any


@dataclass
class ForAll:
    variables: List[Variable]
    predicate: Expression
    parent: Any
    suchthat: Optional[Expression]


@dataclass
class Exists:
    variables: List[Variable]
    unique: bool
    predicate: Expression
    parent: Any
    suchthat: Optional[Expression]


@dataclass
class LambdaExp:
    variables: List[Variable]
    predicate: Expression
    parent: Any
    suchthat: Optional[Expression]


@dataclass
class Iff:
    left: Implies
    right: List[Implies]
    parent: Any


@dataclass
class Implies:
    left: Or
    right: List[Or]
    parent: Any


@dataclass
class Or:
    left: And
    right: List[And]
    parent: Any


@dataclass
class And:
    left: Not
    right: List[Not]
    parent: Any


@dataclass
class Not:
    exp: Union[Not, Comp]
    parent: Any


@dataclass
class Comp:
    left: DefiniteDescription

    parent: Any
    comp: Optional[Comparison]  # TODO Unify these
    right: Optional[DefiniteDescription]  # TODO Unify these
    set: Optional[DefiniteDescription]  # TODO Unify these


@dataclass
class DefiniteDescription:
    variables: List[Variable]
    expression: Union[Expression, LetExpression]
    parent: Any
    suchthat: Optional[Expression]


@dataclass
class Comparison:
    operator: str
    right: DefiniteDescription
    parent: Any


@dataclass
class LetExpression:
    declarations: List[Declaration]
    expression: Union[LetExpression, IfExpression]
    parent: Any


@dataclass
class Declaration:
    name: str
    expression: Expression
    parent: Any


@dataclass
class IfExpression:
    condition: Expression
    ifexp: Expression
    elseexp: Expression
    expression: TypedExpression
    parent: Any


@dataclass
class TypedExpression:
    expression: PlusMinus

    parent: Any
    type: Optional[Type]


@dataclass
class PlusMinus:
    expression: MultDivMod
    right: List[MultDivMod]
    parent: Any


@dataclass
class MultDivMod:
    expression: CatExp
    right: List[CatExp]
    parent: Any


@dataclass
class CatExp:
    expression: Neg
    right: List[Neg]
    parent: Any


@dataclass
class Neg:
    expression: Union[Neg, Selection]
    parent: Any


@dataclass
class Selection:
    expression: ArrayExp
    member: List[QualifiedName]
    parent: Any


@dataclass
class ArrayExp:
    expression: CallExp
    parameters: List[Expression]
    parent: Any


@dataclass
class CallExp:
    expression: Atomic
    args: List[Expression]
    parent: Any


@dataclass
class Atomic:  # TODO Add subs
    value: Union[str, int, float, bool]
    parent: Any


@dataclass
class Node:  # TODO Add subs
    parent: Any


@dataclass
class Type:
    source: FunctionType
    target: Optional[Type] = None
    parent: Any = None

    def __repr__(self):
        if self.target:
            return f"{self.source} <-> {self.target}"
        return f"{self.source}"

@dataclass
class Field:
    name: str
    type: Type
    parent: Any


@dataclass
class RecordType:
    name: str
    fields: List[Field]
    parent: Any

@dataclass
class Parameter:
    name: str
    type: Type
    parent: Any

@dataclass
class Function:
    name: str
    parameters: List[Parameter]
    type: Type
    body: Body
    parent: Any


@dataclass
class Body:
    elements: List[BodyContent]
    parent: Any


@dataclass
class BodyContent:
    parent: Any


@dataclass
class Module:
    name: str
    connections: List[Connection]
    nodes: List[ConnectionNode]
    parent: Any


@dataclass
class VariableModifier:
    parent: Any


@dataclass
class Interface:
    name: str
    operations: List[OperationSig]
    events: List[Event]
    parent: Any
    clocks: List[Clock]
    variables: List[Variable]


@dataclass
class Clock:
    name: str


@dataclass
class OperationSig:
    name: str
    parameters: List[Parameter]
    terminates: bool
    parent: Any


@dataclass
class RoboticPlatformDef:
    name: str
    uses: List[QualifiedName]
    provides: List[QualifiedName]
    requires: List[QualifiedName]
    operations: List[OperationSig]
    events: List[Event]
    parent: Any
    variables: List[Variable]


@dataclass
class OperationDef:
    name: str
    parameters: List[Parameter]
    terminates: str
    preconditions: List[Expression]
    postconditions: List[Expression]
    uses: List[QualifiedName]
    provides: List[QualifiedName]
    variables: List[Variable]
    events: List[Event]
    nodes: List[Node]
    transitions: List[Transition]
    clock: List[Transition]
    parent: Any


@dataclass
class Package:
    name: QualifiedName
    imports: List[Import]
    controllers: List[ControllerDef]
    modules: List[Module]
    functions: List[Function]
    types: List[RecordType]
    machines: List[StateMachineDef]
    interfaces: List[Interface]
    robots: List[RoboticPlatformDef]
    operations: List[OperationDef]


@dataclass
class ConnectionNode:  # TODO add subs
    parent: Any


@dataclass
class QualifiedName:
    parts: List[str]
    parent: Any

    def __hash__(self):
        return hash(str(self.parts))

    def __repr__(self):
        return "::".join(self.parts)


@dataclass
class StateMachineDef:
    name: str
    uses: List[QualifiedName]
    provides: List[QualifiedName]
    requires: List[QualifiedName]
    events: List[Event]
    nodes: List[Node]
    transitions: List[Transition]
    clocks: List[Clock]
    parent: Any
    variables: List[Variable]


@dataclass
class Transition:
    name: str
    source: QualifiedName
    target: QualifiedName

    reset: List[ClockReset]

    parent: Any
    trigger: Optional[Trigger]
    deadline: Optional[Expression]
    condition: Optional[ConditionExpr]
    action: Optional[Statement]


@dataclass
class ConditionExpr:  # TODO
    parent: Any


@dataclass
class Statement:
    statements: List[EndStatement]
    parent: Any


@dataclass
class EndStatement:  # TODO
    parent: Any
    deadline: Optional[Expression]


@dataclass
class ClockReset:
    clock: QualifiedName
    parent: Any


@dataclass
class Trigger:
    trigger: Communication
    probability: Expression
    parent: Any


@dataclass
class CommunicationStmt:
    communication: Communication
    parent: Any


@dataclass
class Communication:
    event: QualifiedName
    source: QualifiedName
    predicate: List[Expression]
    type: Union[InputType, OutputType, SyncType]
    parent: Any


@dataclass
class InputType:
    parameter: QualifiedName
    parent: Any


@dataclass
class OutputType:
    value: CallExp
    parent: Any


@dataclass
class SyncType:
    value: CallExp
    parent: Any


@dataclass
class QualifiedNameWithWildcard:
    name: QualifiedName
    parent: Any

    def __hash__(self):
        return hash(str(self.name))

    def __repr__(self):
        return str(self.name) + "::*"


@dataclass
class Import:
    name: QualifiedNameWithWildcard
    parent: Any

    def __repr__(self):
        return str(self.name)


@dataclass
class FunctionType:
    source: ProductType
    parent: Any
    target: Optional[FunctionType]
    # added by processor
    source_chain: list = field(default_factory=list)
    final_target: Any = None

    def __repr__(self):
        if self.target:
            return f"{self.source} -> {self.target}"
        return f"{self.source}"


@dataclass
class SetType:
    domain: Type
    parent: Any


@dataclass
class AnyType:
    identifier: str
    parent: Any


@dataclass
class TypeRef:
    type: Union[SetType, SeqType, AnyType, Type, QualifiedName]
    parent: Any

    def __repr__(self):
        return f"{self.type}"


@dataclass
class VectorDef:
    base: Type
    size: int # TODO Add processor to set this to into from Atomic
    parent: Any


@dataclass
class MatrixDef:
    base: Type
    rows: Atomic
    columns: Atomic
    parent: Any


@dataclass
class VectorType:
    source: Union[VectorDef, MatrixDef, TypeRef]
    parent: Any

    def __repr__(self):
        return f"{self.source}"


@dataclass
class ProductType:
    types: List[Union[VectorType, TypeRef]]
    flat_types: List[VectorType] = field(default_factory=list)
    parent: Any = None

    def __repr__(self):
        if len(self.types) > 1:
            joined = "*".join(map(str, self.types))
            return f"{joined}"
        return f"{self.types[0]}"


@dataclass
class SeqType:
    domain: Type
    parent: Any

    def __repr__(self):
        return f"[{self.domain}]"


@dataclass
class Event:
    name: str
    broadcast: bool
    type: Type
    parent: Any

    def __repr__(self):
        return f"Event: {self.name} {self.broadcast, self.type}"


def all_concepts() -> List[ClassType]:
    import inspect
    return [
        obj for _, obj in globals().items()
        if inspect.isclass(obj) and obj.__module__ == __name__
    ]
