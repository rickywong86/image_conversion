from PyQt5.QtCore import QObject, pyqtSignal
import os


class Model(QObject):
    dir_changed = pyqtSignal(str)
    file_type_changed = pyqtSignal(str)
    # on_complete_file_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._dir = ''
        self._file_type = ''
        self._converted_dir = ''

    @property
    def dir(self):
        return self._dir
    
    @property
    def converted_dir(self):
        return self._converted_dir

    @dir.setter
    def dir(self, value):
        self._dir = value
        self._converted_dir = os.path.join(value, "converted")
        # update in model is reflected in view by sending a signal to view
        self.dir_changed.emit(value)

    @property
    def file_type(self):
        return self._file_type
    
    @file_type.setter
    def file_type(self, value):
        self._file_type = value
        self.file_type_changed.emit(value)

    # @property
    # def complete_file(self):
    #     return self.dir

    # @complete_file.setter
    # def complete_file(self, value):
    #     self._complete_file = value
    #     self.on_complete_file_changed.emit(value)
