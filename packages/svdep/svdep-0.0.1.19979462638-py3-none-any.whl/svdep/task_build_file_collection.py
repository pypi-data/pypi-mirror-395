import os
import dataclasses as dc
import logging
from typing import ClassVar, Dict, List
from .file_collection import FileCollection
from .file_info import FileInfo
from .svpp_lexer import mk_lexer

@dc.dataclass
class TaskBuildFileCollection(object):
    root_paths : List[str]
    incdirs : List[str] = dc.field(default_factory=list)
    collection : FileCollection = None
    depth : int = 0
    inc_m : Dict[str,str] = dc.field(default_factory=dict)

    _log : ClassVar = logging.getLogger("TaskBuildFileCollection")

    def build(self) -> FileCollection:
        self.collection = FileCollection()

        for path in self.root_paths:
            if os.path.isfile(path):
                path_dir = os.path.dirname(path)
                if path_dir not in self.incdirs:
                    self.incdirs.append(path_dir)
                info = self._buildFileInfo(path)
                self.collection.root_files.append(info)            
            else:
                raise Exception("File %s doesn't exist" % path)

        return self.collection
    
    def _buildFileInfo(self, path):
        self._log.debug("buildFileInfo: %s" % path)
        if path in self.collection.file_info.keys():
            ret = self.collection.file_info[path]
        else:
            ret = FileInfo(
                path,
                os.path.getmtime(path))

            self.collection.file_info[path] = ret

            # Now, need to process the file content
            with open(path, "r") as fp:
                lexer = mk_lexer(debug=False)
                lexer.input(fp.read())

            while tok:=lexer.token():
#                print("tok: %s" % str(tok))
                if tok.type == "DIRECTIVE" and tok.value == "include":
                    name_t = lexer.token()
                    self._log.debug("name_t: %s" % name_t.value)

                    inc_path = None
                    if name_t.value in self.inc_m.keys():
                        # Already did the searching
                        inc_path = self.inc_m[name_t.value]
                    else:
                        for incdir in self.incdirs:
                            if os.path.isfile(os.path.join(incdir, name_t.value)):
                                inc_path = os.path.join(incdir, name_t.value)
                                self.inc_m[name_t.value] = inc_path
                                break
                    if inc_path is not None:
                        path_dir = os.path.dirname(name_t.value)
                        if path_dir not in self.incdirs:
                            self.incdirs.append(path_dir)
                        inc = self._buildFileInfo(inc_path)
                        ret.includes.append(inc.name)
                    else:
                        self._log.critical("Failed to find include %s" % name_t.value)

        return ret
        
