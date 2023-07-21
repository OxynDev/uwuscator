from core import ren_import, ren_var, add_import, str_encrypt, com_obf, gen_builtins, ren_functions
import ast
import os

try:
    from core.utils import vars
except ImportError:
    from utils import vars

    



class Obfuscator:

    new_imports = None
    eval_var = None
    b64decode = None
    farent = None


    def __init__(self, debug: bool = False):
        self.debug = debug
        self.builtins_tool = gen_builtins.BuiltinsManager()
        self.generator = vars.Variables()
        self.code = self.load_code()
        self.tree = self.load_tree(self.code)
        self.imports_vars = {}

    def load_code(self):
        path_list = ['',r'\uwu-scator']
        for i in path_list:
            try:
                return open(os.getcwd() + i + r"\input.txt", "r").read()
            except FileNotFoundError:
                continue
        
        raise 'File not found'

    def load_tree(self, code):
        tree = ast.parse(code)
        return tree

    def tree_transform(self, tree):
        new_source_code = ast.unparse(tree)
        return new_source_code

    def rename_imports(self, tree):
        new_tree , new_imports = ren_import.ImportManager(tree).rename()
        return new_tree
    
    def rename_variables(self, tree):
        new_tree = ren_var.VarManager(tree).rename()
        return new_tree
    
    def add_library(self, tree, library, string):
        new_tree = add_import.ImportManager(tree, library, string).add()
        return new_tree

    def rename_builtins(self):
        builtins_list = [
            'eval',
            'print',
            'exec'
        ]
        builtins_code = ""

        for i in builtins_list:
            builtins_code += self.builtins_tool.gen_builtins(i, "exec", self.b64decode) + "\n"
        return builtins_code

    def encrypt_strings(self, tree):

        if self.debug:
            print("Farent: " + self.fernet)
            print("B64decode: " + self.b64decode)

        tree, encrypted_list = str_encrypt.StringManager(tree, self.fernet, self.b64decode, self.builtins_tool.builtins_dict).encrypt()
        tree = self.add_library(tree, "from cryptography.fernet import Fernet", self.fernet)
        tree = self.add_library(tree, "from base64 import b64decode", self.b64decode)
        tree = self.add_library(tree, "import ctypes", self.ctypes)
        tree = self.add_library(tree, "import threading", self.threading)

        self.imports_vars['Fernet'] = self.fernet
        self.imports_vars['b64decode'] = self.b64decode
        self.imports_vars['ctypes'] = self.ctypes
        self.imports_vars['threading'] = self.threading

        
        return tree, encrypted_list

    def compiler(self, tree, addon):

        marshal = self.generator.random_string()
        self.imports_vars['loads'] = marshal

        if self.debug:
            print("Marshal: " + marshal)

        compiler = com_obf.CompilerManager(tree, self.imports_vars, self.builtins_tool.builtins_dict)

        compiler.add_compiler(addon)
        self.tree = self.add_library(self.tree, "from marshal import loads", marshal)
        compiler.compile_functions(self.tree)
        return compiler.tree

    def rename_functions(self, tree):
        tree = ren_functions.FunctionManager(tree).rename()
        return tree


    def run(self):

        self.eval_var = self.generator.random_string()
        self.fernet = self.generator.random_string()
        self.b64decode = self.generator.random_string()
        self.threading = self.generator.random_string()
        self.ctypes = self.generator.random_string()

        if self.debug:
            print("Eval: " + self.eval_var)

        addon_code = self.rename_builtins()
        self.tree, encrypted_list = self.encrypt_strings(self.tree)
        self.tree = self.rename_functions(self.tree)
        self.tree = self.compiler(self.tree, ast.unparse(encrypted_list)+"\n"+addon_code)
        self.tree = self.rename_imports(self.tree)
        self.tree = self.rename_variables(self.tree)
        
        
        if self.debug:
            print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

        res = self.tree_transform(self.tree)
        return res



if __name__ == "__main__":
    res = Obfuscator(debug=False).run()
    open("out.py","w").write(res)