import ast
from typing import Any, Dict, List, Optional, Set


class VariationTransformer(ast.NodeTransformer):
    """
    Transforms AST to replace destructive operations with VariationTensor equivalents
    """

    def __init__(self, mirages: List[Dict[str, Any]]) -> None:
        self.mirages = mirages
        self.mirage_nodes = {id(m["node"]): m for m in mirages}
        self.imports_added: Set[str] = set()

    def visit_Call(self, node: ast.Call) -> Any:
        """Transform destructive calls to VariationTensor equivalents"""
        if id(node) in self.mirage_nodes:
            mirage = self.mirage_nodes[id(node)]

            if mirage["type"] == "mean":
                return self._create_variation_tensor_collapse(node, "mean")
            elif mirage["type"] == "sum":
                return self._create_variation_tensor_ensemble_sum(node)
            elif mirage["type"] == "premature_discretization":
                return self._create_discretization_wrapper(node)

        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """Add VariationTensor import if needed"""
        if node.module == "__future__":
            return node

        # Add VariationTensor import
        if "VariationTensor" not in self.imports_added:
            self.imports_added.add("VariationTensor")
            variation_import = ast.ImportFrom(
                module="demyst.engine.variation_tensor",
                names=[ast.alias(name="VariationTensor", asname=None)],
                level=0,
            )
            return [variation_import, node]

        return node

    def visit_Module(self, node: ast.Module) -> Any:
        """Ensure VariationTensor import is added at the top"""
        self.generic_visit(node)

        # Add import if we transformed any nodes
        if self.imports_added and "VariationTensor" in self.imports_added:
            variation_import = ast.ImportFrom(
                module="demyst.engine.variation_tensor",
                names=[ast.alias(name="VariationTensor", asname=None)],
                level=0,
            )
            node.body.insert(0, variation_import)

        return node

    def _create_variation_tensor_collapse(self, node: ast.Call, operation: str) -> ast.Call:
        """Create VariationTensor(...).collapse() call"""
        # Extract arguments from original call
        args = [self.visit(arg) for arg in node.args]
        keywords = [self.visit(kw) for kw in node.keywords]

        # Create VariationTensor constructor
        variation_call = ast.Call(
            func=ast.Name(id="VariationTensor", ctx=ast.Load()), args=args, keywords=keywords
        )

        # Create collapse method call
        collapse_call = ast.Call(
            func=ast.Attribute(value=variation_call, attr="collapse", ctx=ast.Load()),
            args=[ast.Constant(value=operation)],
            keywords=[],
        )

        return collapse_call

    def _create_variation_tensor_ensemble_sum(self, node: ast.Call) -> ast.Call:
        """Create VariationTensor(...).ensemble_sum() call"""
        args = [self.visit(arg) for arg in node.args]
        keywords = [self.visit(kw) for kw in node.keywords]

        # Extract axis from keywords if present
        axis_arg = None
        new_keywords = []
        for kw in keywords:
            if kw.arg == "axis":
                axis_arg = kw.value
            else:
                new_keywords.append(kw)

        # Create VariationTensor constructor
        variation_call = ast.Call(
            func=ast.Name(id="VariationTensor", ctx=ast.Load()), args=args, keywords=new_keywords
        )

        # Create ensemble_sum method call
        ensemble_sum_call = ast.Call(
            func=ast.Attribute(value=variation_call, attr="ensemble_sum", ctx=ast.Load()),
            args=[axis_arg] if axis_arg else [],
            keywords=[],
        )

        return ensemble_sum_call

    def _create_discretization_wrapper(self, node: ast.Call) -> Any:
        """Wrap discretization in VariationTensor for metadata preservation"""
        # For now, just preserve the data before discretization
        # This is a more complex transformation that would need domain knowledge
        return self.generic_visit(node)
