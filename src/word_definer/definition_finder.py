
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, QTimer, pyqtSignal, pyqtSlot
from API.google_trans_API import GoogleTranslate

class DefinitionFinder:
    """
   This class is responible for finding the definition of a word
   whether using the google translate API or the database lookup 
    """
    def __init__(self):
        pass
    
    def lookup(self, selection):
        pass
class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    progress
        int progress complete,from 0-100
    """
    # progress = pyqtSignal(str, int)
    finished = pyqtSignal(str)

class GoogleTranslateWorker(QRunnable):
    def __init__(self,search_term):
        super().__init__()
        self.google_trans_API = GoogleTranslate()
        self.signals = WorkerSignals()
        self.search_term = search_term

    @pyqtSlot()
    def run(self):
        answer = self.google_trans_API.translate(self.search_term)
        self.signals.finished.emit(answer)
class DatabaseLookupWorker(QRunnable):
    def __init__(self,search_term):
        super().__init__()
        pass 

    @pyqtSlot()
    def run(self):
        pass
        # self.signals.finished.emit(answer)

