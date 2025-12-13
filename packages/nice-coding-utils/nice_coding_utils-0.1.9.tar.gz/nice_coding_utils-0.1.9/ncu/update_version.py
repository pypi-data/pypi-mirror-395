
class UpdateVersion:
    """
    Updates the current project-version.
    
    Version-scheme:
    ```python
    "{major}.{minor}.{patch}"
    major : int
    minor : int
    patch : int
    ```
    
    Parameters:
    * **pathname**: default -> `./src/version.py`, this is the path of the file that contains the `varname` variable
    * **inc**: default -> `0.0.1` will be added to the current version
    * **varname**: default -> `__version__`, the variable name to overwrite

    Attributes:
    * **new_version**: (tuple[int, int, int] | None)
    * **old_version**: (tuple[int, int, int] | None)
    * **varname**: (str) -> look into parameters
    * **pathname**: (str) -> look into parameters
    * **inc**: (str) -> look into parameters
    """
    def __init__(self, pathname: str = './src/version.py', inc: str = '0.0.1', varname: str = '__version__'):
        self.pathname = pathname
        self.inc = inc
        self.varname = varname
        self.old_version, self.new_version = None, None
        self.__update_version()
        
    def __update_version(self):
        nmajor, nminor, npatch = map(int, self.inc.split('.'))
    
        text = ''
        blocked = False
        with open(self.pathname) as f:
            for line in f:
                if line.startswith(self.varname) and not blocked:
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    major, minor, patch = map(int, version.split('.'))
                    self.old_version = (major, minor, patch)
                    major += nmajor
                    minor += nminor
                    patch += npatch
                    version = f"{major}.{minor}.{patch}"
                    self.new_version = (major, minor, patch)
                    text += f'{self.varname} = "{version}"\n'
                    blocked = True
                else:
                    text += line
            
        with open(self.pathname, 'w') as fw:
            fw.write(text)