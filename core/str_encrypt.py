import ast 
import base64 
import random
from cryptography.fernet import Fernet 

try: 
    from .utils import vars 
except ImportError: 
    from utils import vars 

class StringEncryption(ast.NodeTransformer): 
    def __init__(self, fernet, list_var, fernet_var, base64_var, builtins_dict): 
        self.builtins_dict = builtins_dict
        self.fernet = fernet 
        self.variable_mapping = {} 
        self.generator = vars.Variables() 
        self.strings = [] 
        self.list_var = list_var 
        self.fernet_var = fernet_var 
        self.base64_var = base64_var 

    def visit_Str(self, node): 
        enc_string = self.fernet.encrypt(node.s.encode()) 
        self.strings.append(enc_string) 
        index = len(self.strings) - 1
        string_decrypt = f"{self.fernet_var}.decrypt(" + self.list_var + f"[{index}]" + ").decode()" 
        base64_string = base64.b64encode(bytes(string_decrypt, encoding="utf8")).decode('ascii') 
        eval_var = random.choice(self.builtins_dict['eval'])
        args = [ast.Str(s=f'{eval_var}({self.base64_var}("{base64_string}"))'),] 
        return ast.Call( 
            func=ast.Name(id=eval_var), 
            args=args, 
            keywords=[], 
            ) 


    def visit_JoinedStr(self, node): 
        return node 

class StringManager: 
    def __init__(self, tree, fernet_var, base64_var, builtins_dict): 
        self.builtins_dict = builtins_dict
        self.generator = vars.Variables() 
        self.tree = tree 
        self.base64_var = base64_var 
        self.fernet_var = fernet_var 

    def encrypt(self): 
        self.list_var = self.generator.random_string() 
        self.fernet_object = self.generator.random_string() 
        key = Fernet.generate_key() 
        farent = Fernet(key) 
        
        
        renamer = StringEncryption(farent, self.list_var, self.fernet_object, self.base64_var, self.builtins_dict ) 
        self.tree = renamer.visit(self.tree) 

        init_code = ast.parse(f"{self.list_var}={str(renamer.strings)}\n" + f"{self.fernet_object}={self.fernet_var}({key})") 

        self.tree = ast.fix_missing_locations(self.tree) 
        return self.tree, init_code