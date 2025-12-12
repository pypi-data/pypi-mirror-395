
from .file_collection import FileCollection
from .native import is_native_available, get_native_library_path

# Import pure-Python implementations
from .task_check_up_to_date import TaskCheckUpToDate as _PythonTaskCheckUpToDate
from .task_build_file_collection import TaskBuildFileCollection as _PythonTaskBuildFileCollection

# Use native implementations if available, otherwise fall back to pure-Python
if is_native_available():
    from .native import NativeTaskCheckUpToDate as TaskCheckUpToDate
    from .native import NativeTaskBuildFileCollection as TaskBuildFileCollection
else:
    TaskCheckUpToDate = _PythonTaskCheckUpToDate
    TaskBuildFileCollection = _PythonTaskBuildFileCollection