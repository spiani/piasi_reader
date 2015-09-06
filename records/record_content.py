from sys import version_info

# Get python major version
py_version = int(version_info[0])

if py_version < 3:
    class uninterpreted_content(str):
        @property
        def interpreted(self):
            return False
else:
    class uninterpreted_content(bytes):
        @property
        def interpreted(self):
            return False

class interpreted_content(object):
    @property
    def interpreted(self):
        return True

