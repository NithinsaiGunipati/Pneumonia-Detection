import warnings
from PIL import Image
warnings.filterwarnings('ignore')
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
from keras.preprocessing import image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QMovie

from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(695, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 701, 611))
        self.frame.setStyleSheet("background-color: #035874;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, -60, 541, 561))
        self.label.setText("")
        self.gif = QMovie("picture.gif")
        self.label.setMovie(self.gif)
        self.gif.start()
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(80, 430, 591, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(30, 530, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("patient.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      "border-radius: 10px;\n"
                                      " background-color:#DF582C;\n"
                                      "\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      " background-color: #7D93E0;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 530, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
                                        "border-radius: 10px;\n"
                                        " background-color:#DF582C;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        " background-color: #7D93E0;\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons
        self.pushButton.clicked.connect(self.upload_image)
        self.pushButton_2.clicked.connect(self.predict_result)

        # Load the model once at the start
        self.model = load_model('trained.h5')
        print(f"Model input shape: {self.model.input_shape}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PNEUMONIA Detection App"))
        self.label_2.setText(_translate("MainWindow", "Chest X-ray PNEUMONIA Detection"))
        self.pushButton.setText(_translate("MainWindow", "Upload Image"))
        self.pushButton_2.setText(_translate("MainWindow", "Predict"))

    def upload_image(self):
        # Open file dialog and select the image
        filename, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if filename:
            self.image_path = filename
            print(f"Selected image: {self.image_path}")

            try:
                # Load and preprocess the image
                img_file = image.load_img(self.image_path, target_size=(300, 300))  # Match model's input size
                img_array = image.img_to_array(img_file)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = preprocess_input(img_array)  # Normalize using model's preprocessing
                self.img_data = img_array

                # Debugging: Print preprocessed image shape
                print(f"Preprocessed image shape: {self.img_data.shape}")
                QMessageBox.information(None, "Image Upload", "Image uploaded and preprocessed successfully.", QMessageBox.Ok)
            except Exception as e:
                print(f"Error during image upload and preprocessing: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred: {e}", QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "No Image Selected", "Please select an image file.", QMessageBox.Ok)

    def predict_result(self):
        # Ensure an image is uploaded
        if hasattr(self, 'img_data'):
            try:
                # Debugging: Verify shapes
                print(f"Model input shape: {self.model.input_shape}")
                print(f"Image data shape: {self.img_data.shape}")

                # Perform prediction
                prediction = self.model.predict(self.img_data)
                print(f"Raw prediction result: {prediction}")

                # Interpret prediction
                if prediction[0][0] <= 0.5:
                    print("Result: Normal")
                    speak("Result is Normal")
                    QMessageBox.information(None, "Prediction Result", "The image is classified as Normal.", QMessageBox.Ok)
                else:
                    print("Result: Affected by Pneumonia")
                    speak("Result is Affected by Pneumonia")
                    QMessageBox.information(None, "Prediction Result", "The image is classified as Affected by Pneumonia.", QMessageBox.Ok)
            except Exception as e:
                print(f"Error during prediction: {e}")
                QMessageBox.critical(None, "Error", f"An error occurred: {e}", QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "No Image Uploaded", "Please upload an image before making a prediction.", QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
