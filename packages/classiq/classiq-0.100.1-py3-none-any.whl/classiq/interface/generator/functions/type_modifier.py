from classiq.interface.enum_utils import StrEnum


class TypeModifier(StrEnum):
    Const = "const"
    Mutable = "mutable"
    Inferred = "inferred"
