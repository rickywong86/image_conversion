from PyQt5.QtWidgets import qApp, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot, QSettings, QFileInfo
from os import path
from view.main_view_ui import Ui_MainWindow
from pathlib import Path
import os

not_saved_list = ['QLabel','QProgressBar']

# restore the saved settings
def restore(settings):
    finfo = QFileInfo(settings.fileName())

    if finfo.exists() and finfo.isFile():
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "" and mo.className() not in not_saved_list: # skip to reload property for certain widget
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)

# save the setting for all widget
def save(settings):
    for w in qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() != "" and mo.className() not in not_saved_list: # skip to reload property for certain widget
            for i in range(mo.propertyCount()):
                name = mo.property(i).name()
                settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))

class MainView(QMainWindow):
    # init the setting file
    settings = QSettings("gui.ini", QSettings.IniFormat)

    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # load saved settings
        restore(self.settings)
        self.default_model_value()

        print(self._model.file_type)
        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        self._ui.txtPath.mousePressEvent = self.open_dir_dialog
        # self._ui.txtPath.textChanged.connect(self.open_file_name_dialog)
 
        ####################################################################
        #   listen for model event signals
        ####################################################################
        # file name is updated 
        self._model.dir_changed.connect(self.on_dir_changed)
 
        self._ui.rdoJPG.toggled.connect(lambda: self._main_controller.file_type_changed("JPG"))
        self._ui.rdoPNG.toggled.connect(lambda: self._main_controller.file_type_changed("PNG"))
        self._model.file_type_changed.connect(self.on_file_type_changed)
 
        # connect button click action to controller
        self._ui.btnProcess.clicked.connect(lambda: self.on_btnProcess_click())

        # connect button click action to open directory
        self._ui.btnOpenConvertedDir.clicked.connect(lambda: self.on_btnOpenConvertedDir_click())
 
        self._main_controller.task_bar_message.connect(lambda: self.on_task_bar_message)

    # default model value
    def default_model_value(self):
        if self._model.dir == '':
            self._main_controller.dir_changed(self._ui.txtPath.text())
        if self._model.file_type == '':
            if self._ui.rdoJPG.isChecked():
                self._main_controller.file_type_changed("JPG")
            else :
                self._main_controller.file_type_changed("PNG")
        else:
            self._main_controller.file_type_changed("JPG")
        self.button_enable()

    def button_enable(self):
        # enable button
        valid_path = False
        if os.path.exists(self._model.dir):
            valid_path = True
            self._ui.btnProcess.setEnabled(True)
        else:
            self._ui.btnProcess.setEnabled(False)
            self.on_task_bar_message("red", "File path is not exists. (" + self._model.dir + ")" )
        if os.path.exists(self._model.converted_dir):
            self._ui.btnOpenConvertedDir.setEnabled(True)
        else:
            self._ui.btnOpenConvertedDir.setEnabled(False)
        
    # save setting after closed event
    def closeEvent(self, event):
        save(self.settings)
        QMainWindow.closeEvent(self, event)
  
    def on_dir_changed(self, name):
        # label color based on file_name
        # if the file name is empty them it means file is reseted
        # name = path.basename(name)
        name = name 
        self._ui.txtPath.setText(name)
        file_label_color = "green"
        self.button_enable()
        self.on_task_bar_message(file_label_color, "Successfully loaded {} file".format(name))
 
    def on_file_type_changed(self, type):
        # label color based on file_name
        # if the file name is empty them it means file is reseted
        type = type
        file_label_color = "purple"
        self.button_enable()
        self.on_task_bar_message(file_label_color, type)

# ------------------------------------------------------------------------------------------------------------
    def on_btnProcess_click(self):
        files = [f for f in os.listdir(self._model.dir) if f.endswith('.HEIC') or f.endswith('.heif')]
        cnt = 1
        # setting for loop to set value of progress bar 
        # print(str(files.__len__()))
        # print(files[1])
        for filename in files:
        # for i in range(files.__len__()):
            # filename = files[i]
            # slowing down the loop 
            # time.sleep(0.05) 
            file_label_color = "purple" 
            self.on_task_bar_message(file_label_color, "Processing file: " + filename)
            success, e = self._main_controller.btnProcess_clicked(filename)
            if success == False:
                file_label_color = "red" 
                self.on_task_bar_message(file_label_color, "Fail processing file: " + filename + " Exception: " + type(e).__name__)
            self._ui.progressBar.setValue(int(cnt/files.__len__()*100))
            cnt += 1 
        # self._main_controller.btnProcess_clicked("test")
        self.on_task_bar_message(file_label_color, "Process completed.")

    @pyqtSlot(str)
    def on_complete_file_changed(self, filename):
        print("run")
        # setting value to progress bar
        file_label_color = "purple" 
        self.on_task_bar_message(file_label_color, "Processing file: " + filename)
        # self._ui.progressBar.setValue(file_cnt) 
# --------------------------------------------------------------------------------------------------------------
    @pyqtSlot(str, str)
    def on_task_bar_message(self, color, message):
        self._ui.statusbar.show()
        self._ui.statusbar.showMessage(message)
        self._ui.statusbar.setStyleSheet('color: {}'.format(color))

    # Set one file
    def open_dir_dialog(self, value):
        # open window to select file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        dir = QFileDialog.getExistingDirectory(self, 'Select Folder')

        if dir:
            path = Path(dir)
            self._main_controller.dir_changed(str(path))

    def on_btnOpenConvertedDir_click(self):
        path = os.path.realpath(self._model.converted_dir)
        os.startfile(path)
