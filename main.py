# Importe a classe do mapa que criamos (ajuste o nome do arquivo se você salvou diferente)
from View.login_view import LoginView
from View.main_window import MainWindow
from View.main_window_worker import MainWindowWorker
from database import init_db

def on_login(worker):
    login_window.withdraw()
    if worker.role == "admin":
        MainWindow(login_window)
    else:
        MainWindowWorker(login_window)

if __name__ == "__main__":
    init_db()
    login_window = LoginView(on_login=on_login)
    login_window.mainloop()