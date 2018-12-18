import re


config = {'outDir': 'export',
          'rootPat': r'^root',
          'supportedExtensions': ['png', 'jpg', 'jpeg']}
config['rootPat'] = re.compile(config['rootPat'])

