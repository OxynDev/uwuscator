import ast
from .utils import vars


class ImportTransformer(ast.NodeTransformer):

    def __init__(self, tree):
        self.imports = []
        self.new_tree = tree

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname:
                self.imports.append({"type": "Import", "name": alias.name, "node": node, "as": alias.asname})
            else:
                self.imports.append({"type": "Import", "name": alias.name, "node": node, "as": None})
            
    def visit_ImportFrom(self, node):
        modules = []
        for alias in node.names:
            if alias.asname:
                modules.append({"module": alias.name, "as": alias.asname})
            else:
                modules.append({"module": alias.name , "as": None})

        self.imports.append({"type": "ImportFrom", "name": node.module, "node": node, "module": modules})



class ImportRenameTransformer(ast.NodeTransformer):
    def __init__(self, tree, imports):
        self.imports = imports
        self.tree = tree

    def visit_Name(self, node):
        try:
            if isinstance(node.ctx, ast.Load):
                for i in self.imports:
                    if i['type'] == "Import":
                        if i['as'] == None:
                            if node.id == i['name']:
                                node.id = i['new_as']
                        else:
                            if node.id == i['as']:
                                node.id = i['new_as'] 
                    elif i['type'] == "ImportFrom":
                        if node.id == i['module']:
                            node.id = i['new_as']
        except:
            pass

        return node

class ImportManager:

    def __init__(self, tree):
        self.generator = vars.Variables()
        self.tree = tree

    def rename(self):

        visitor = ImportTransformer(self.tree)
        visitor.visit(self.tree)
        new_body = self.tree.body
        import_body = []
        new_imports = []
        
        for i in visitor.imports:

            if i['type'] == "Import":
                if not 'UwU_' in str(i.get('as')):
                    new_as = self.generator.random_string()
                else:
                    new_as = i['as']
                alias = ast.alias(name=i['name'], asname=new_as)
                new_import = ast.Import(names=[alias])
                import_body = import_body + [new_import]  
                import_data = i
                import_data['new_as'] = new_as
                new_imports.append(import_data)

            elif i['type'] == "ImportFrom":
                names = []
                for module in i['module']:
                    if not 'UwU_' in str(module.get('as')):
                        new_as = self.generator.random_string()
                    else:
                        new_as = module['as']
                    alias = ast.alias(name=module['module'], asname=new_as)
                    names.append(alias)
                    new_imports.append({'type': 'ImportFrom', 'name': i['name'], "node": i['node'], 'module': module['module'], 'as': module['as'], 'new_as': new_as})

                for name in names:
                    new_import = ast.ImportFrom(module=i['name'], names=[name], level=0)
                    import_body = import_body + [new_import]  

        self.tree.body = import_body + new_body
        ast.fix_missing_locations(new_import)

        ImportRenameTransformer(self.tree, new_imports).visit(self.tree)
        new_body = self.tree.body

        return self.tree, new_imports


