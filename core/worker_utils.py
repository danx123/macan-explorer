# file: core/worker_utils.py

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool

class WorkerSignals(QObject):
    """
    Mendefinisikan sinyal yang tersedia dari Worker QRunnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    # Tambahkan sinyal progress jika dibutuhkan untuk QProgressBar,
    # namun _get_folder_size tidak mudah memberikan progress spesifik.
    progress = pyqtSignal(int, int) # value, max_value

class Worker(QRunnable):
    """
    Worker thread untuk menjalankan fungsi secara asinkron.
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        # Simpan fungsi dan argumen untuk dijalankan
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        """
        Inisialisasi eksekusi fungsi.
        """
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            # Tangkap semua exception dan kirimkan melalui sinyal error
            self.signals.error.emit((type(e), e, e.__traceback__))
        finally:
            # Pastikan sinyal finished selalu dipancarkan
            self.signals.finished.emit()