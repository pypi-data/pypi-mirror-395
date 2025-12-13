__author__ = "Justus Decker"
__copyright__ = "Copyright 2025, NiceCodingUtils by Justus Decker"
__license__ = "GPL V3"
__version__ = "1.0.0"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Production"

import os, ast

def file_write(filepath : str, data : str):
    """
    Writes to a file in `wb` mode
    """
    with open(filepath, 'wb') as f:
        f.write(data.encode())

# ignore-files
# ignore-methods
# ignore-functions
# ignore-classes

class AutoDocstring:
    """
    Gets all Docstrings contained in the `{current_folder}` & subdirectories and saves it to `{self.filepath}`.
    """
    METHOD = 'method'
    FUNCTION = 'function'
    
    def __init__(self, 
                 filepath: str,
                 ignored_filenames: list[str] = None,
                 ignored_methods: list[str] = None,
                 ignored_functions: list[str] = None,
                 ignored_classes: list[str] = None):
        
        if ignored_filenames is None: ignored_filenames = []
        if ignored_methods is None: ignored_methods = []
        if ignored_functions is None: ignored_functions = []
        if ignored_classes is None: ignored_classes = []
        
        self.ignored_filenames = ignored_filenames
        self.ignored_methods = ignored_methods
        self.ignored_functions = ignored_functions
        self.ignored_classes = ignored_classes
        
        self.filepath = filepath
        self.NUM_DOCS = 0
        self.NO_DOCS = 0
        self.DOCS = '# AutoDocstring by Justus Decker\n\n'
    
    def fnil(self, p: str, l: list[str]) -> bool:
        return os.path.basename(p).replace('.py','') in l
    
    def nnil(self, n: str, l: list[str]) -> bool:
        return n in l
    
    def doc(self, text: str):
        """ 
        Writes documentation into `self.DOCS`
        Adds a new-line each time
        """
        self.DOCS += text + '\n'
        
    def doc_inc(self, doc):
        self.NUM_DOCS += 1
        if doc is None:
            self.NO_DOCS += 1
            return False
        return True
    
    def doc_path(self, path: str, docs: str):
        if not self.doc_inc(docs): return
        self.doc(f'# {path}')
        self.doc(docs)
    
    def doc_class(self, _class: str, docs: str):
        if not self.doc_inc(docs): return
        self.doc(f'## {_class}')
        self.doc(docs)
        
    def doc_method(self, _class: str, method: str, docs: str):
        if not self.doc_inc(docs): return
        self.doc(f'### {_class} -> {method}')
        self.doc(docs)
    
    def doc_func(self, func: str, docs: str):
        if not self.doc_inc(docs): return
        self.doc(f'### {func}')
        self.doc(docs)
    
    @staticmethod
    def get_python_paths() -> list[str]:
        """
        Gets all the python files in the tree.
        """
        _ret = []
        for rel, _, files in os.walk('./'):
            for file in files:
                if file.endswith('.py'):
                    
                    p = os.path.join(rel, file).replace('\\','/')
                    _ret.append(p)
        return _ret
    
    def __class_fetch(self, obj, aw):
        """
        * Creates documentation for itself
        * Iterates over all methods in a class
            * Creating Documentation for the method
            * Set the method / function as flagged so it does not show up more than once.
        """
        blocked = False
        if not isinstance(obj, ast.ClassDef): return
        if self.nnil(obj.name, self.ignored_classes): # Blocks all methods of this class
            print(f'skipped class: {obj.name}, because of the ignored_classes')
            blocked = True
        if not blocked: 
            class_docs = ast.get_docstring(obj)
            self.doc_class(obj.name, class_docs)
        for func in obj.body:
            self.__funcmeth_fetch(func, aw, AutoDocstring.METHOD, obj, blocked)
                    
    def __funcmeth_fetch(self, obj, aw: list[int], type: str, _hClass = None, blocked = False):
        """
        Creates the documentation for a function / method.
        Only create the documentation in the case of:
        ```python
        if obj.lineno not in aw
        ``` 
        """
        if not isinstance(obj, ast.FunctionDef): return

        if blocked:
            print(f'skipped method: {obj.name}, because of the ignored_classes -> sub_methods')
            aw.append(obj.lineno)
            return
        docs = ast.get_docstring(obj)
        if type == 'function': 
            if obj.lineno in aw: return
            if self.nnil(obj.name, self.ignored_methods): # Blocks all methods of this class
                print(f'skipped function: {obj.name}, because of the ignored_functions')
                return
            self.doc_func(obj.name, docs)
        elif type == 'method':
            if self.nnil(obj.name, self.ignored_methods): # Blocks all methods of this class
                print(f'skipped method: {_hClass.name} -> {obj.name}, because of the ignored_methods')
                return
            self.doc_method(obj.name, _hClass.name, docs)
        aw.append(obj.lineno)
    def generate(self):
        """
        The Entry point for creating auto-docs.
        Creates a file automatically.
        """
        
        paths = AutoDocstring.get_python_paths()
        for path in paths:
            
            if self.fnil(path, self.ignored_filenames): 
                print(f'skipped path: {path}, because of the ignored_filenames')
                continue
            
            with open(path, 'rb') as file:
                data = file.read()
            tree = ast.parse(data)
            path_docs = ast.get_docstring(tree)
            self.doc_path(path, path_docs)
            already_written = []
            for n in ast.walk(tree):
                self.__class_fetch(n, already_written)
                self.__funcmeth_fetch(n, already_written, AutoDocstring.FUNCTION)
        file_write(self.filepath, self.DOCS)
        print(self.NO_DOCS / self.NUM_DOCS, self.NUM_DOCS, self.NO_DOCS)


if __name__ == '__main__':
    AutoDocstring("./docs/auto-docs.md",
                  ['__init__'],
                  ['__init__'],
                  [],
                  []
                  ).generate()