import base64


class Base64Tool:
    
    def encode(self, data, eval_var, decode_var):
        encoded_data = base64.b64encode(data.encode("utf8")).decode('utf8')
        return f"""{eval_var}("{eval_var}({decode_var}('{encoded_data}'))")"""
