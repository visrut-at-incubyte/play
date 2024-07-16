import ast
import os

def find_public_members(module_path):
    with open(module_path, 'r') as file:
        tree = ast.parse(file.read(), filename=module_path)
    
    public_members = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not node.name.startswith('_'):
                public_members.append(node.name)
    return public_members

def update_init_file(init_path, public_members):
    if not public_members:
        return

    with open(init_path, 'r') as file:
        lines = file.readlines()

    with open(init_path, 'w') as file:
        # Remove existing __all__ definition if any
        in_all_block = False
        for line in lines:
            if line.startswith('__all__'):
                in_all_block = True
            if in_all_block and line.strip().endswith(']'):
                in_all_block = False
                continue
            if not in_all_block:
                file.write(line)

        # Add the new __all__ definition
        file.write('\n\n__all__ = [\n')
        for member in public_members:
            file.write(f"    '{member}',\n")
        file.write(']\n')

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == '__init__.py':
                init_path = os.path.join(root, file)
                public_members = []
                for mod_file in os.listdir(root):
                    mod_path = os.path.join(root, mod_file)
                    if mod_file.endswith('.py') and mod_file != '__init__.py':
                        public_members.extend(find_public_members(mod_path))
                update_init_file(init_path, public_members)

if __name__ == '__main__':
    project_directory = 'src'
    process_directory(project_directory)
