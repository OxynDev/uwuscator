import ast
try:
    from .utils import vars
except ImportError:
    from utils import vars


class VariableRenamer(ast.NodeTransformer):
    def __init__(self):
        self.variable_mapping = {}
        self.generator = vars.Variables()

    def visit_Name(self, node):
        if hasattr(node, 'ctx') and isinstance(node.ctx, ast.Store):
            old_name = node.id
            if old_name in self.variable_mapping.values():
                new_name = old_name
            else:
                new_name = self.generator.random_string()
                self.variable_mapping[old_name] = new_name
            node.id = new_name
        else:
            if node.id in self.variable_mapping:
                node.id = self.variable_mapping[node.id]
        return node

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Name):
            target_name = node.target.id
            if target_name in self.variable_mapping:
                node.target.id = self.variable_mapping[target_name]

        self.generic_visit(node)
        return node


class VarManager:
    def __init__(self, tree):
        self.generator = vars.Variables()
        self.tree = tree

    def rename(self):
        renamer = VariableRenamer()
        self.tree = renamer.visit(self.tree)
        return self.tree