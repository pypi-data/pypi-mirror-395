#****************************************************************************
#* file_collection_info.py
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
import dataclasses as dc
from typing import Dict, List
from .file_info import FileInfo

@dc.dataclass
class FileCollection(object):
    root_files : List = dc.field(default_factory=list)
    file_info : Dict[str, object] = dc.field(default_factory=dict)

    def to_dict(self):
        ret = {}
        ret["root_files"] = []
        for file in self.root_files:
            ret["root_files"].append(file.to_dict())
        ret["file_info"] = {}
        for path in self.file_info.keys():
            ret["file_info"][path] = self.file_info[path].to_dict()
        return ret
    
    @classmethod
    def from_dict(cls, d):
        ret = FileCollection()
        for file in d["root_files"]:
            ret.root_files.append(FileInfo.from_dict(file))
        for path in d["file_info"].keys():
            ret.file_info[path] = FileInfo.from_dict(d["file_info"][path])
        return ret


