import marshal
import random
import ast
import ctypes

try:
    from .utils import vars
except ImportError:
    from utils import vars


class Encode:
    def __init__(self):
        self.random_var = random.randint(69,2115)

    def uwu_encode(self, opcodes):
        new_list = []
        for i in opcodes:
            if i == 0:
                if (len(new_list) % 2) > 0.5: new_list.append("OwO")
                else: new_list.append("UwU")
            else: new_list.append(i*self.random_var)
        return new_list

    def decode(self, opcodes):
        return [0 if i in ["UwU", "OwO"] else round(i/69) for i in opcodes]

    def return_decode(self, loads_var, decode_var):
        return f'{decode_var}=lambda o: {loads_var}(bytes([0 if i in ["UwU", "OwO"] else round(i/{self.random_var}) for i in o]))'

class CompilerManager:
    def __init__(self, tree,imports_vars, builtins_dict):

        self.builtins_dict = builtins_dict
        self.tree = tree
        self.encoder = Encode()
        self.generator = vars.Variables()
        self.imports_vars = imports_vars
        self.decode_var = self.generator.random_string()
    
    def compile_code(self, code, uwu_mode: bool = True):
        code_bytes = marshal.dumps(compile(code, "<string>", "exec"))
        code_ints = [int(byte) for byte in code_bytes]
        if uwu_mode == True:
            code_data = self.encoder.uwu_encode(code_ints)
            eval_var = random.choice(self.builtins_dict['eval'])
            return f"{eval_var}({self.decode_var}({code_data}))"
        elif uwu_mode == False:
            return code_ints
        
    def get_antidebug(self):
        crusher = """if ctypes.windll.kernel32.IsDebuggerPresent(): A=ctypes.POINTER(ctypes.c_int)();ctypes.windll.ntdll.RtlAdjustPrivilege(ctypes.c_uint(19),ctypes.c_uint(1),ctypes.c_uint(0),ctypes.byref(ctypes.c_int()));ctypes.windll.ntdll.NtRaiseHardError(ctypes.c_ulong(3221225595),ctypes.c_ulong(0),A,A,ctypes.c_uint(6),ctypes.byref(ctypes.c_uint()))"""
        crusher = crusher.replace("ctypes",self.imports_vars['ctypes'])
        return crusher
                    
    def add_compiler(self, add_code):
        #crusher_code = self.get_antidebug()
        # crusher_code + "\n" +
        code =  add_code + "\n" + self.encoder.return_decode(self.imports_vars['loads'], self.decode_var)

        compiler_bytes = self.compile_code(code,  False)
        compiler_code = f"eval({self.imports_vars['loads']}(bytes({compiler_bytes})))"
        compiler_tree = ast.parse(compiler_code)
        self.tree.body = compiler_tree.body + self.tree.body
        return self.tree

    def compile_functions(self, tree):
        
        compile = lambda code: self.compile_code(code, True)

        class FunctionVisitor(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name != "__init__":
                    function_node = compile(ast.parse(ast.unparse(node)))
                    return ast.parse(function_node)
                else:
                    return node
                
        visitor = FunctionVisitor()
        visitor.visit(tree)
        self.tree.body = tree.body
        return tree.body