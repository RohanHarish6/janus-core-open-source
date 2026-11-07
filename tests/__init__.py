import sys, os, importlib.util

class DirectFileFinder:
    def find_spec(self, fullname, path, target=None):
        parts = fullname.split('.')
        base_name = parts[-1]
        search_paths = list(path) if path else list(sys.path)
        for p in search_paths:
            candidate = os.path.join(p, base_name + '.py')
            if os.path.exists(candidate):
                return importlib.util.spec_from_file_location(fullname, candidate)
        return None

if not any(isinstance(f, DirectFileFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, DirectFileFinder())

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
