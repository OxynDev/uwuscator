from core.utils import vars, base64it

class BuiltinsManager:
    def __init__(self):
        self.generator = vars.Variables()
        self.base64it = base64it.Base64Tool()
        self.builtins_dict = {
            "eval": []
        }

    def gen_builtins(self, builtin_function, eval_var, decode_var):

        if not builtin_function in self.builtins_dict:
            self.builtins_dict[builtin_function] = []

        eval_base = self.generator.random_string([50,50])
        setcode = f"b='{eval_base}'"
        
        for i in range(10):
            self.builtins_dict[builtin_function].append(eval_base[:1:-1+(-i)])
            setcode += f";setattr(__builtins__,b[:1:-1+(-{i})],{builtin_function})"

        return self.base64it.encode(setcode, eval_var, decode_var)
    
