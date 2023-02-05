# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import manga

class Ui_MainWindow(object):
    manga_pesquisado = ''
    busca_realizada = False


    def CriarThread(self, _worker, retorno):
        thread = QThread()
        worker = _worker
        worker.moveToThread(thread)
        worker.finished.connect(retorno)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        return {'thread':thread, 'worker':worker}

    def BuscarAnime(self):
        def finalizar(resultado):
                if(resultado!={}):
                        self.manga_pesquisado = resultado
                        self.status_txt.setText(f"Mangá foi localizado!\n- {self.nome_txt.toPlainText()}\n- {resultado['url']}\n\n{resultado['data']['description']}")
                        self.busca_realizada = True
                else:
                        self.status_txt.setText("Opa... Eu não achei esse mangá!")
                self.BuscaWork['thread'].quit()

        self.nome_txt.setText(self.nome_txt.toPlainText().replace("\n", '').replace('\t', ''))
        self.capitulo_txt.setText(self.capitulo_txt.toPlainText().replace("\n", '').replace('\t', ''))

        if(self.nome_txt.toPlainText() == "" or self.capitulo_txt.toPlainText() == ""):
                self.status_txt.setText("Preencha todos os dados!")
                return 0
        if(self.capitulo_txt.toPlainText().isnumeric() == False):
                self.status_txt.setText("Apenas  numeros  no  campo  de  capitulos")
                return 0

        try:
                self.BuscaWork = self.CriarThread(
                        manga.Mangayabu(
                                self.nome_txt.toPlainText(),
                                self.capitulo_txt.toPlainText()
                        ),
                        finalizar
                )
                self.BuscaWork['thread'].started.connect(self.BuscaWork['worker'].Pesquisar_anime)
                self.BuscaWork['thread'].start()
        except Exception as erro:
                print(str(erro))

    def BaixarAnime(self):
        def finalizar():
                self.status_txt.setText("Download Concluído!")
                self.manga_pesquisado = ''
                self.busca_realizada = False
                self.nome_txt =''
                self.capitulo_txt=''

        if(self.busca_realizada == True):
                self.status_txt.setText("LEMBRE-SE DE REALIZAR UMA NOVA BUSCA PARA BAIXAR OUTROS CAPITULOS!")
                try:
                        self.DownloaddWork = self.CriarThread(
                                manga.Mangayabu(
                                        capitulo=self.manga_pesquisado['cap'],
                                        url=self.manga_pesquisado['url'],
                                        nome=self.manga_pesquisado['nome']),
                                finalizar
                        )
                        self.DownloaddWork['thread'].started.connect(self.DownloaddWork['worker'].Download)
                        self.DownloaddWork['thread'].start()
                except Exception as erro:
                        print(str(erro))
                self.DownloaddWork['thread'].start()
        else:
                self.status_txt.setText("Você ainda não realizou uma nova busca!")


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(563, 459)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(563, 459))
        MainWindow.setMaximumSize(QtCore.QSize(563, 459))
        MainWindow.setStyleSheet("background-color: rgb(40, 44, 52)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.finished = pyqtSignal()
        self.titulo = QtWidgets.QLabel(self.centralwidget)
        self.titulo.setGeometry(QtCore.QRect(170, 50, 291, 31))
        self.titulo.setStyleSheet("font-family: \"Exo 2 Black\";\n"
"font-size: 26px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"color: rgb(197, 168, 152);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;")
        self.titulo.setObjectName("titulo")
        self.btn_buscar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_buscar.setGeometry(QtCore.QRect(190, 230, 231, 23))
        self.btn_buscar.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"background-color: rgb(88, 70, 109);\n"
"color: rgb(255, 255, 255);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;\n"
"border-color: #00AA66;\n"
"border-style: solid;\n"
"border-radius: 5px;")
        self.btn_buscar.setObjectName("btn_buscar")
        self.btn_buscar.clicked.connect(self.BuscarAnime)
        self.btn_baixar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_baixar.setGeometry(QtCore.QRect(190, 260, 231, 23))
        self.btn_baixar.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"background-color: rgb(88, 70, 109);\n"
"color: rgb(255, 255, 255);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;\n"
"border-color: #00AA66;\n"
"border-style: solid;\n"
"border-radius: 5px;")
        self.btn_baixar.setObjectName("btn_baixar")
        self.btn_baixar.clicked.connect(self.BaixarAnime)
        self.todos_check = QtWidgets.QCheckBox(self.centralwidget)
        self.todos_check.setGeometry(QtCore.QRect(420, 200, 51, 16))
        self.todos_check.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 8px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"color: rgb(255, 255, 255);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;")
        self.todos_check.setObjectName("todos_check")
        self.servidores = QtWidgets.QLabel(self.centralwidget)
        self.servidores.setGeometry(QtCore.QRect(80, 431, 171, 20))
        self.servidores.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"letter-spacing: 0px;\n"
"word-spacing: 0px;\n"
"color: rgb(197, 168, 152);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;")
        self.servidores.setObjectName("servidores")
        self.nome_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.nome_txt.setGeometry(QtCore.QRect(200, 150, 211, 31))
        self.nome_txt.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"color: rgb(197, 168, 152);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;\n"
"border: 1px solid  rgb(88, 70, 109);\n"
"border-radius: 8px;\n"
"")
        self.nome_txt.setObjectName("nome_txt")
        self.barra_lateral = QtWidgets.QFrame(self.centralwidget)
        self.barra_lateral.setGeometry(QtCore.QRect(0, -10, 61, 471))
        self.barra_lateral.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.barra_lateral.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.barra_lateral.setFrameShadow(QtWidgets.QFrame.Raised)
        self.barra_lateral.setObjectName("barra_lateral")
        self.btn_main = QtWidgets.QPushButton(self.barra_lateral)
        self.btn_main.setGeometry(QtCore.QRect(0, 10, 61, 51))
        self.btn_main.setStyleSheet("image: url(:/icons/down_icon.png);\n"
"border-color: #00AA66;\n"
"border-style: solid;\n"
"border-radius: 5px;")
        self.btn_main.setText("")
        self.btn_main.setObjectName("btn_main")
        self.btn_ler = QtWidgets.QPushButton(self.barra_lateral)
        self.btn_ler.setGeometry(QtCore.QRect(0, 70, 61, 41))
        self.btn_ler.setStyleSheet("image: url(:/icons/book_icon.png);\n"
"border-color: #00AA66;\n"
"border-style: solid;\n"
"border-radius: 5px;\n"
"")
        self.btn_ler.setText("")
        self.btn_ler.setObjectName("btn_ler")
        self.capitulo_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.capitulo_txt.setGeometry(QtCore.QRect(200, 190, 211, 31))
        self.capitulo_txt.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"color: rgb(197, 168, 152);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;\n"
"border: 1px solid  rgb(88, 70, 109);\n"
"border-radius: 8px;")
        self.capitulo_txt.setObjectName("capitulo_txt")
        self.status_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.status_txt.setGeometry(QtCore.QRect(80, 330, 461, 91))
        self.status_txt.setStyleSheet("font-family: \'Noto Sans JP\', sans-serif;\n"
"font-size: 12px;\n"
"color: rgb(197, 168, 152);\n"
"font-weight: bold;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: uppercase;\n"
"border: 1px solid  rgb(88, 70, 109);\n"
"border-radius: 8px;\n"
"")
        self.status_txt.setReadOnly(True)
        self.status_txt.setObjectName("status_txt")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titulo.setText(_translate("MainWindow", "MANGÁ DOWNLOADER"))
        self.btn_buscar.setText(_translate("MainWindow", "Buscar"))
        self.btn_baixar.setText(_translate("MainWindow", "Baixar"))
        self.todos_check.setText(_translate("MainWindow", "Todos"))
        self.servidores.setText(_translate("MainWindow", "Servidores : Mangayabu"))
        self.nome_txt.setPlaceholderText(_translate("MainWindow", "NOME DO MANGÁ"))
        self.capitulo_txt.setPlaceholderText(_translate("MainWindow", "CApitulo"))
        self.status_txt.setPlaceholderText(_translate("MainWindow", "STATUS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
