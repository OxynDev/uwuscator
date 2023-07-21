import ast
try:
    from .utils import vars
except ImportError:
    from utils import vars


class RandomizeFuncNames(ast.NodeTransformer):
    def __init__(self):
        super(RandomizeFuncNames, self).__init__()
        self.func_name_mapping = {}
        self.generator = vars.Variables()

    def visit_FunctionDef(self, node):
        blacklist = ['__init__', '__enter__', '__exit__', '__call__']
        if node.name not in blacklist:
            random_name = self.generator.random_string()
            self.func_name_mapping[node.name] = random_name
            node.name = random_name
            return self.generic_visit(node)
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            original_func_name = node.func.id
            if original_func_name in self.func_name_mapping:
                random_name = self.func_name_mapping[original_func_name]
                node.func.id = random_name
        elif isinstance(node.func, ast.Attribute):
            original_func_name = node.func.attr
            if original_func_name in self.func_name_mapping:
                random_name = self.func_name_mapping[original_func_name]
                node.func.attr = random_name
        return self.generic_visit(node)


class FunctionManager:
    def __init__(self, tree):
        self.tree = tree

    def rename(self):
        renamer = RandomizeFuncNames()
        self.tree = renamer.visit(self.tree)
        return self.tree
