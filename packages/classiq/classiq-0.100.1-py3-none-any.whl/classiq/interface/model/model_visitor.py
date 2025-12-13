from collections.abc import Collection

from pydantic import BaseModel

from classiq.interface.debug_info.debug_info import DebugInfoCollection
from classiq.interface.generator.visitor import RetType, Transformer, Visitor
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_statement import QuantumStatement


class ModelVisitor(Visitor):
    def visit_DebugInfoCollection(self, debug_info: DebugInfoCollection) -> None:
        return


class ModelStatementsVisitor(ModelVisitor):
    def visit_BaseModel(self, node: BaseModel) -> RetType | None:
        if isinstance(node, Model):
            return self.visit(node.functions)
        if isinstance(node, NativeFunctionDefinition):
            return self.visit(node.body)
        if isinstance(node, QuantumStatement):
            for block in node.blocks.values():
                self.visit(block)
            return None
        return super().visit_BaseModel(node)


class ModelTransformer(Transformer):
    def visit_DebugInfoCollection(
        self, debug_info: DebugInfoCollection
    ) -> DebugInfoCollection:
        return debug_info


class ModelStatementsTransformer(ModelTransformer):
    def visit_BaseModel(
        self, node: BaseModel, fields_to_skip: Collection[str] | None = None
    ) -> RetType:
        if isinstance(node, Model):
            new_functions = self.visit(node.functions)
            return node.model_copy(update=dict(functions=new_functions))
        if isinstance(node, NativeFunctionDefinition):
            new_body = self.visit(node.body)
            return node.model_copy(update=dict(body=new_body))
        if isinstance(node, QuantumStatement):
            new_blocks = {
                block_name: self.visit(block)
                for block_name, block in node.blocks.items()
            }
            return node.model_copy(update=new_blocks)
        return super().visit_BaseModel(node, fields_to_skip)
