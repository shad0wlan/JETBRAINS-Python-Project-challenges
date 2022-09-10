# write your code here
import _ast
from collections import defaultdict
from pathlib import Path
import re
import argparse
import os
import ast


class CodeAnalyzer:
    def __init__(self, file_to_process):
        self.check_existence = Path(file_to_process)
        self.valid_path = False
        if self.check_existence.is_file():
            self.valid_path = True
            self.file = file_to_process
            self.file_data = defaultdict(str)
            self.functions = defaultdict(dict)
            self.base_variables = defaultdict(dict)
            self.classes = defaultdict(dict)
            self.tree_walk = None
            with open(self.file) as f:
                for index, line in enumerate(f):
                    self.file_data[index + 1] = line
            with open(self.file) as f:
                r = f.read()
                tree = ast.parse(r)
                self.tree_walk = ast.walk(tree)
            self.problems = defaultdict(dict)
        else:
            print("Path Does not exist")

    def check_lines_length(self, file_data: dict):
        problems_count = 0
        for line, data in file_data.items():
            if len(data.strip()) > 79:
                self.problems[line]['S001'] = 'Too long'
                problems_count += 1
        if problems_count > 0:
            return True
        else:
            return False

    def check_indent(self, file_data: dict):
        problems_count = 0
        for line, data in file_data.items():
            if data.startswith(" "):
                spaces = re.search(r"^ +", data).group()
                if len(spaces) % 4 != 0:
                    self.problems[line]['S002'] = 'Indentation is not a multiple of four'
                problems_count += 1
        if problems_count > 0:
            return True
        else:
            return False

    def check_semicolon(self, file_data: dict):
        problems_count = 0
        for line, data in file_data.items():
            if ";" in data:
                string_template = re.search(r"(\'|\").*(\'|\")", data)
                if string_template and ";" in string_template.group() and not data.endswith(";"):
                    continue
                elif string_template and "#" in data and data.index(";") > data.index("#") or data.startswith("#"):
                    continue
                else:
                    self.problems[line]['S003'] = 'Unnecessary semicolon'
                problems_count += 1
        if problems_count > 0:
            return True
        else:
            return False

    def nodes_build(self):
        for node in self.tree_walk:
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_arguments = [j.arg for j in node.args.args]
                function_defaults = [True for j in node.args.defaults if
                                     isinstance(j, (_ast.List, _ast.Set, _ast.Dict))]
                self.functions[node.lineno] = \
                    {'name': function_name,
                     'args': function_arguments,
                     'mutable': function_defaults,
                     }
                for b in node.body:
                    if isinstance(b, ast.Assign):
                        if not isinstance(b.targets[0], ast.Tuple):
                            if not isinstance(b.targets[0], ast.Attribute):
                                self.functions[b.lineno] = {'variable': b.targets[0].id}
                        else:
                            for name in b.targets:
                                for n in name.elts:
                                    self.functions[b.lineno]['variable'].append(n.id)

            elif isinstance(node, _ast.Module):
                for b in node.body:
                    if isinstance(b, _ast.Assign):
                        self.base_variables[b.lineno]['variable'] = []
                        if not isinstance(b.targets[0], ast.Tuple):
                            self.base_variables[b.lineno] = {'variable': b.targets[0].id}
                        else:
                            for name in b.targets:
                                for n in name.elts:
                                    self.base_variables[b.lineno]['variable'].append(n.id)

            elif isinstance(node, _ast.ClassDef):
                for b in node.body:
                    if isinstance(b, _ast.Assign):
                        if not isinstance(b.targets[0], ast.Tuple):
                            self.classes[b.lineno] = {'variable': b.targets[0].id}
                        else:
                            for name in b.targets:
                                for n in name.elts:
                                    self.classes[b.lineno]['variable'].append(n.id)

                self.classes[node.lineno] = {'name': node.name, 'base': node.bases[0].id if node.bases else ''}

    def check_inline_comment(self, file_data: dict):
        problems_count = 0
        for line, data in file_data.items():
            if "#" in data and not data.strip().startswith("#"):
                inline = re.search(r"\s\s#", data)
                if inline is None:
                    self.problems[line]['S004'] = 'At least two spaces required before inline comments'
                problems_count += 1
        if problems_count > 0:
            return True
        else:
            return False

    def check_todo(self, file_data: dict):
        problems_count = 0
        for line, data in file_data.items():
            if "#" in data and "todo" in data.lower():
                if data.index("#") < data.lower().index("todo"):
                    self.problems[line]['S005'] = 'TODO found'
                problems_count += 1
        if problems_count > 0:
            return True
        else:
            return False

    def check_new_lines(self, file_data: dict):
        problems_count = 0
        counter = 0
        for line, data in file_data.items():
            if data == "\n":
                counter += 1
                continue
            if data != "\n" and (counter == 2 or counter == 1):
                counter = 0
                continue
            if counter == 3:
                self.problems[line]['S006'] = 'More than two blank lines used before this line'
                counter = 0
                problems_count += 1
                continue
        if problems_count > 0:
            return True
        else:
            return False

    def check_classes(self):
        name_template = r'[A-Z][a-z]*[A-Z]?[a-z]*'
        variable_name_template = r'([A-Z_0-9])+|([a-z0-9_\.])+'
        for i, j in self.file_data.items():
            if "class" in j:
                if j.count(" ") != 1:
                    self.problems[i]['S007'] = "Too many spaces after 'class'"
        for i, j in self.classes.items():
            name = self.classes[i].get('name')
            base_class = self.classes[i].get('base')
            variable_names = self.classes[i].get('variable')
            if name is not None:
                if not re.fullmatch(name_template, name):
                    self.problems[i]['S008'] = f"Class name '{name}' should be written in CamelCase"
            if base_class:
                if not re.fullmatch(name_template, base_class):
                    self.problems[i]['S011'] = f"Class '{base_class}' should be written in CamelCase"
            if variable_names is not None:
                if not re.fullmatch(variable_name_template, variable_names):
                    self.problems[i]['S011'] = f"Variable '{variable_names}' should be written in snake_case"

    def check_functions(self):
        name_template = r'([a-z0-9_])+'
        variable_name_template = r'([a-z0-9_\.])+'
        for i, j in self.file_data.items():
            if "def" in j:
                name = j.lstrip()[: j.index("(")]
                if name.count(" ") != 1:
                    self.problems[i]['S007'] = "Too many spaces after 'def'"
        for i, j in self.functions.items():
            name = self.functions[i].get('name')
            arguments = self.functions[i].get('args')
            variable_names = self.functions[i].get('variable')
            mutability = self.functions[i].get('mutable')
            if name is not None:
                if not re.fullmatch(name_template, name):
                    self.problems[i]['S009'] = f"Function '{name}' should be written in snake_case"
            if arguments is not None:
                for arg in arguments:
                    if not re.fullmatch(variable_name_template, arg):
                        self.problems[i]['S010'] = f"Argument name '{arg}' should be written in snake_case"
            if variable_names is not None:
                if not re.fullmatch(variable_name_template, variable_names):
                    self.problems[i]['S011'] = f"Variable '{variable_names}' should be written in snake_case"
            if mutability:
                self.problems[i]['S012'] = "The default argument value is mutable."

    def check_mod_vars(self):
        variable_name_template = r'([A-Z_0-9])+|([a-z0-9_\.])+'
        for i, j in self.base_variables.items():
            name = self.base_variables[i].get('variable')
            if name is not None:
                if not re.fullmatch(variable_name_template, name):
                    self.problems[i]['S011'] = f"Variable '{name}' should be written in snake_case"


    def pep_checks_wrapper(self, file_data: dict):
        self.nodes_build()
        self.check_lines_length(file_data)
        self.check_indent(file_data)
        self.check_semicolon(file_data)
        self.check_inline_comment(file_data)
        self.check_todo(file_data)
        self.check_new_lines(file_data)
        self.check_classes()
        self.check_functions()
        self.check_mod_vars()

    def __str__(self):
        problems_found = []
        if len(self.problems) > 0:
            for key, value in sorted(self.problems.items(), key=lambda x: x[0]):
                for v in value:
                    problems_found.append(f'{self.check_existence}: Line {key}: {v} {value[v]}')
            return "\n".join(problems_found)
        else:
            return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_scan", help="Enter a valid path to scan python files for PEP8 style errors", type=str)
    args = parser.parse_args()
    if args.path_to_scan:
        path = Path(args.path_to_scan)
        if path.name.endswith(".py"):
            file_to_scan = args.path_to_scan
            analyzer = CodeAnalyzer(file_to_scan)
            analyzer.pep_checks_wrapper(analyzer.file_data)
            print(analyzer)

        elif path.is_dir():
            directory = args.path_to_scan + "/"
            list_files = sorted(os.listdir(args.path_to_scan))
            for file in list_files:
                if file.endswith("py"):
                    file_to_scan = directory + file
                    analyzer = CodeAnalyzer(file_to_scan)
                    analyzer.pep_checks_wrapper(analyzer.file_data)
                    print(analyzer)
