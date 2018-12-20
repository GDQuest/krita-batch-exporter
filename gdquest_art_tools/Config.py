import re

config = {
    'outDir': 'export',
    'rootPat': r'^root',
    'sym': r'\W'
}  # yapf: disable
config['rootPat'] = re.compile(config['rootPat'])
config['sym'] = re.compile(config['sym'])

