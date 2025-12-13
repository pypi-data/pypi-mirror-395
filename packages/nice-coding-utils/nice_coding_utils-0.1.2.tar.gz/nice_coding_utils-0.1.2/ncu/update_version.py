
class UpdateVersion:
    def __init__(self, pathname: str = './src/version.py', inc: str = '0.0.1', varname: str = '__version__'):
        self.pathname = pathname
        self.inc = inc
        self.varname = varname
    def update_version(self): 
        nmajor, nminor, npatch = map(int, self.inc.split('.'))
    
        text = ''
        with open(self.pathname) as f:
            for line in f:
                if line.startswith(self.varname):
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    major, minor, patch = map(int, version.split('.'))
                    major += nmajor
                    minor += nminor
                    patch += npatch
                    version = f"{major}.{minor}.{patch}"
                    text += f'{self.varname} = "{version}"\n'
                else:
                    text += line
            
        with open(self.pathname, 'w') as fw:
            fw.write(text)