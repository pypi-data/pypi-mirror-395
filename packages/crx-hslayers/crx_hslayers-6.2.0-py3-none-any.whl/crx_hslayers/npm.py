from pynpm import NPMPackage

def install():
    pkg = NPMPackage('static/package.json')
    pkg.install()