#****************************************************************************
#* native.py
#*
#* Copyright 2024 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#****************************************************************************
"""
Native library wrapper for svdep.
Attempts to load the native shared library and provides Python bindings.
"""

import ctypes
import json
import os
import sys
from typing import List, Optional

from .file_collection import FileCollection

# Try to load the native library
_lib = None
_lib_path = None

def _find_native_library() -> Optional[str]:
    """Find the native svdep library."""
    # Determine library name based on platform
    if sys.platform == 'win32':
        lib_name = 'svdep.dll'
    elif sys.platform == 'darwin':
        lib_name = 'libsvdep.dylib'
    else:
        lib_name = 'libsvdep.so'
    
    # Search paths
    search_paths = []
    
    # Check relative to this module
    module_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths.append(module_dir)
    search_paths.append(os.path.join(module_dir, '..', '..', '..', 'cpp', 'build'))
    search_paths.append(os.path.join(module_dir, '..', '..', '..', 'cpp', 'build', 'lib'))
    
    # Check standard library paths
    if 'LD_LIBRARY_PATH' in os.environ:
        search_paths.extend(os.environ['LD_LIBRARY_PATH'].split(os.pathsep))
    if 'DYLD_LIBRARY_PATH' in os.environ:
        search_paths.extend(os.environ['DYLD_LIBRARY_PATH'].split(os.pathsep))
    if 'PATH' in os.environ and sys.platform == 'win32':
        search_paths.extend(os.environ['PATH'].split(os.pathsep))
    
    # Standard system paths
    search_paths.extend(['/usr/local/lib', '/usr/lib'])
    
    for path in search_paths:
        full_path = os.path.join(path, lib_name)
        if os.path.isfile(full_path):
            return full_path
    
    return None

def _load_native_library():
    """Load the native library and setup function signatures."""
    global _lib, _lib_path
    
    _lib_path = _find_native_library()
    if _lib_path is None:
        return False
    
    try:
        _lib = ctypes.CDLL(_lib_path)
    except OSError:
        return False
    
    # Define function signatures
    # svdep_t svdep_create(void)
    _lib.svdep_create.restype = ctypes.c_void_p
    _lib.svdep_create.argtypes = []
    
    # void svdep_destroy(svdep_t ctx)
    _lib.svdep_destroy.restype = None
    _lib.svdep_destroy.argtypes = [ctypes.c_void_p]
    
    # int svdep_add_incdir(svdep_t ctx, const char *path)
    _lib.svdep_add_incdir.restype = ctypes.c_int
    _lib.svdep_add_incdir.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    
    # int svdep_add_root_file(svdep_t ctx, const char *path)
    _lib.svdep_add_root_file.restype = ctypes.c_int
    _lib.svdep_add_root_file.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    
    # int svdep_build(svdep_t ctx)
    _lib.svdep_build.restype = ctypes.c_int
    _lib.svdep_build.argtypes = [ctypes.c_void_p]
    
    # const char *svdep_get_json(svdep_t ctx)
    _lib.svdep_get_json.restype = ctypes.c_char_p
    _lib.svdep_get_json.argtypes = [ctypes.c_void_p]
    
    # int svdep_load_json(svdep_t ctx, const char *json)
    _lib.svdep_load_json.restype = ctypes.c_int
    _lib.svdep_load_json.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    
    # int svdep_check_up_to_date(svdep_t ctx, double last_timestamp)
    _lib.svdep_check_up_to_date.restype = ctypes.c_int
    _lib.svdep_check_up_to_date.argtypes = [ctypes.c_void_p, ctypes.c_double]
    
    # const char *svdep_get_error(svdep_t ctx)
    _lib.svdep_get_error.restype = ctypes.c_char_p
    _lib.svdep_get_error.argtypes = [ctypes.c_void_p]
    
    return True

# Try to load on import
_native_available = _load_native_library()

def is_native_available() -> bool:
    """Check if the native library is available."""
    return _native_available

def get_native_library_path() -> Optional[str]:
    """Get the path to the loaded native library."""
    return _lib_path


class NativeTaskBuildFileCollection:
    """Native implementation of TaskBuildFileCollection."""
    
    def __init__(self, root_paths: List[str], incdirs: List[str] = None):
        self.root_paths = root_paths
        self.incdirs = incdirs if incdirs is not None else []
        self._ctx = None
    
    def build(self) -> FileCollection:
        if not _native_available:
            raise RuntimeError("Native library not available")
        
        self._ctx = _lib.svdep_create()
        if not self._ctx:
            raise RuntimeError("Failed to create svdep context")
        
        try:
            # Add include directories
            for incdir in self.incdirs:
                result = _lib.svdep_add_incdir(self._ctx, incdir.encode('utf-8'))
                if result != 0:
                    error = _lib.svdep_get_error(self._ctx)
                    raise RuntimeError(f"Failed to add incdir: {error.decode('utf-8') if error else 'unknown error'}")
            
            # Add root files
            for path in self.root_paths:
                result = _lib.svdep_add_root_file(self._ctx, path.encode('utf-8'))
                if result != 0:
                    error = _lib.svdep_get_error(self._ctx)
                    raise RuntimeError(f"Failed to add root file: {error.decode('utf-8') if error else 'unknown error'}")
            
            # Build
            result = _lib.svdep_build(self._ctx)
            if result != 0:
                error = _lib.svdep_get_error(self._ctx)
                raise RuntimeError(f"Build failed: {error.decode('utf-8') if error else 'unknown error'}")
            
            # Get JSON result
            json_str = _lib.svdep_get_json(self._ctx)
            if not json_str:
                error = _lib.svdep_get_error(self._ctx)
                raise RuntimeError(f"Failed to get JSON: {error.decode('utf-8') if error else 'unknown error'}")
            
            # Parse JSON and create FileCollection
            data = json.loads(json_str.decode('utf-8'))
            return FileCollection.from_dict(data)
        
        finally:
            if self._ctx:
                _lib.svdep_destroy(self._ctx)
                self._ctx = None


class NativeTaskCheckUpToDate:
    """Native implementation of TaskCheckUpToDate."""
    
    def __init__(self, root_files: List[str], incdirs: List[str] = None):
        self.root_files = root_files
        self.incdirs = incdirs if incdirs is not None else []
        self._ctx = None
    
    def check(self, info: FileCollection, timestamp: float) -> bool:
        if not _native_available:
            raise RuntimeError("Native library not available")
        
        self._ctx = _lib.svdep_create()
        if not self._ctx:
            raise RuntimeError("Failed to create svdep context")
        
        try:
            # Load the file collection as JSON
            json_str = json.dumps(info.to_dict())
            result = _lib.svdep_load_json(self._ctx, json_str.encode('utf-8'))
            if result != 0:
                error = _lib.svdep_get_error(self._ctx)
                raise RuntimeError(f"Failed to load JSON: {error.decode('utf-8') if error else 'unknown error'}")
            
            # Check if up to date
            result = _lib.svdep_check_up_to_date(self._ctx, timestamp)
            if result == -1:
                error = _lib.svdep_get_error(self._ctx)
                raise RuntimeError(f"Check failed: {error.decode('utf-8') if error else 'unknown error'}")
            
            return result == 1
        
        finally:
            if self._ctx:
                _lib.svdep_destroy(self._ctx)
                self._ctx = None
