from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PIL import Image
from pillow_heif import register_heif_opener
import os

class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)
    # on_complete_file_changed = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot(str)
    def dir_changed(self, name):
        # update model
        self._model.dir = name

    @pyqtSlot(str)
    def file_type_changed(self, type):
        # update model
        self._model.file_type = type

    @pyqtSlot(str)
    def btnProcess_clicked(self, filename):
        # time.sleep(0.05)
        # print(str(file_cnt))
        # self.on_complete_file_changed.emit(filename, file_cnt)
        # self._model.complete_file = filename
        
        # self.task_bar_message.emit("green", filename)
        
        convert_dir_path = os.path.join(self._model.dir, "converted")
        if os.path.exists(convert_dir_path) == False:
            convert_dir = os.mkdir(convert_dir_path)
        else :
            convert_dir = convert_dir_path

        register_heif_opener()
        success = True
        _e = None
        try:
            image = Image.open(os.path.join(self._model.dir, filename))
            image.convert('RGB').save(os.path.join(convert_dir, os.path.splitext(filename)[0] + '.' + self._model.file_type))
        except Exception as e:
            print(e)
            _e = e
            success = False
        return (success, _e)
        
