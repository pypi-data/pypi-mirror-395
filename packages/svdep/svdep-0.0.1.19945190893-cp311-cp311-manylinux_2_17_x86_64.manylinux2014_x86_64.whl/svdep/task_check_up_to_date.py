#****************************************************************************
#* task_compute_file_deps.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
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
#* Created on:
#*     Author: 
#*
#****************************************************************************
import os
from typing import List
from .file_collection import FileCollection
from .file_info import FileInfo
from .file_deps_report import FileDepsReport

class TaskCheckUpToDate(object):

    def __init__(self, root_files, incdirs=[]):
        self.root_files = root_files
        self.incdirs = incdirs
        pass

    def check(self, info : FileCollection, timestamp : int) -> bool:
        ret = True

        ret &= (len(info.root_files) == len(self.root_files))

        if ret:
            for i in range(len(info.root_files)):
                ret &= info.root_files[i].name == self.root_files[i]

                if ret:
                    ret &= (os.path.getmtime(self.root_files[i]) <= timestamp)

                    if ret:
                        # Check included files
                        for inc_f in info.root_files[i].includes:
                            ret &= self._checkInclude(info, info.file_info[inc_f], timestamp)

                            if not ret:
                                break
                
                if not ret:
                    break

        return ret
    
    def _checkInclude(self, info : FileCollection, inc : FileInfo, timestamp):
        if inc.checked:
            return True
        else:
            ret = (os.path.getmtime(inc.name) <= timestamp)

            if ret:
                for si in inc.includes:
                    sub_inc = info.file_info[si]
                    ret &= self._checkInclude(info, sub_inc, timestamp)

                    if not ret:
                        break

            inc.checked = True
            return ret




