import sys
import random
from PyQt6.QtWidgets import (QComboBox,QScrollArea,QGridLayout,QTableWidget,QTableWidgetItem,
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt,QDate
import requests
main_user = ''
select_movie = ''
session = ''
class CinemaLoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinema Application")
        self.setFixedSize(600, 400)

        # Колдонуучуларды жүктөө

        # Background image
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("image.png"))
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)

        # Central widget
        self.central_widget = QWidget(self)
        self.central_widget.setGeometry(150, 50, 300, 300)

        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username label
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)

        # Password label
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #4C5563; color: white;")
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet("background-color: #4C5563; color: white;")
        self.signup_button.clicked.connect(self.open_signup_window)
        button_layout.addWidget(self.signup_button)

        layout.addLayout(button_layout)

    # def load_users(self):
    #     """Кошулган адамдарды файлдан жүктөө"""
    #     users = {}
    #     try:
    #         with open("users.txt", "r") as file:
    #             for line in file:
    #                 username, password = line.strip().split(",")
    #                 users[username] = password
    #     except FileNotFoundError:
    #         pass
    #     return users

    # def save_users(self):
    #     """Кошулган адамдарды файлга сактоо"""
    #     with open("users.txt", "w") as file:
    #         for username, password in self.users.items():
    #             file.write(f"{username},{password}\n")

    def login(self):
        """Кирип жаткан адамды текшерип жана кинолор жайгашкан бетке отуу"""
        global main_user
        username = self.username_input.text()
        password = self.password_input.text()

        response = requests.get('http://kutmanata.pythonanywhere.com/get_user', params={'user':username, 'password':password})
        if response.json()==True:
            response = requests.get('http://kutmanata.pythonanywhere.com/check_password', params={'user':username, 'password':password})
            if response.json()==True:
                main_user = username
                self.open_movies_page()
        else:
            QMessageBox.critical(self, 'Error', 'User not found')

    def open_movies_page(self):
        """Кинолор жайгашкан бетке кируу(отуу)"""
        self.movies_page = CinemaApp()
        self.movies_page.show()
        self.close()

    def open_signup_window(self):
        """Sign Up окносун ачуу"""
        self.signup_window = SignUpWindow( self)
        self.signup_window.show()

class SignUpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setFixedSize(400, 400)

        # Фонду кошуу
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("image 1.png"))  # озумдун суротумду коюуу
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 400, 400)

        # Layout түзүү
        layout = QVBoxLayout()

        # Username текстинин стили
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)

        # Password текстинин стили
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Verify Password текстинин стили
        self.verify_password_label = QLabel("Verify Password:")
        self.verify_password_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.verify_password_label)

        self.verify_password_input = QLineEdit()
        self.verify_password_input.setPlaceholderText("Re-enter your password")
        self.verify_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.verify_password_input)

        # CAPTCHA текстинин стили
        self.captcha_label = QLabel()
        self.update_captcha()
        self.captcha_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.captcha_label)

        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Enter CAPTCHA")
        layout.addWidget(self.captcha_input)

        # Signup кнопкасы
        self.register_button = QPushButton("Registered")
        self.register_button.setStyleSheet("background-color: #4C5563; color: white; font-size: 16px; font-weight: bold;")
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def update_captcha(self):
        """CAPTCHA алмаштыруу(алмашып туруу учун)"""
        self.current_captcha = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=5))
        self.captcha_label.setText(f"CAPTCHA: {self.current_captcha}")
    
    def register_user(self):
        """Жаңы кирген адамды кошуу(катоо)"""
        username = self.username_input.text()
        password = self.password_input.text()
        verify_password = self.verify_password_input.text()
        captcha = self.captcha_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields must be filled")
            return

        if password != verify_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        if captcha != self.current_captcha:
            QMessageBox.warning(self, "Error", "Incorrect CAPTCHA")
            self.update_captcha()
            return

        response = requests.get('http://kutmanata.pythonanywhere.com/get_user', params={'user':username})
        if response.json()==False:
            requests.get('http://kutmanata.pythonanywhere.com/add_user', params={'user':username, 'password':password})
            self.parent().show()  # CinemaLoginApp терезесин көрсөтүү
            self.close()  # SignUp терезесин жапуу
        else:
            QMessageBox.critical(self, 'Error', 'User already exist')
            

        # Login бетине өтүү (билдирүүсүз)


class CinemaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinema App")
        self.setFixedSize(1000, 750)

        # Задний фон
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("image 8.png"))
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Movie Title
        self.title_label = QLabel("Movies", self)
        self.title_label.setStyleSheet("color: white; font-size: 60px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setGeometry(400, 20, 224, 50)

        # Кино жана сеанстар жайгашкан коллонкалар
        self.movies_and_sessions = QWidget(self)
        self.movies_and_sessions.setGeometry(150, 100, 700, 400)
        layout = QHBoxLayout(self.movies_and_sessions)

        # Сол колонка: кинолордун аттары (скролл менен жылдырып коро беребиз)
        self.movies_scroll = QScrollArea(self)
        self.movies_scroll.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.movies_scroll.setWidgetResizable(True)

        self.movies_widget = QWidget()

        self.load_movies()
        # self.movie_data = requests.get('http://kutmanata.pythonanywhere.com/get_movies').json()
        # self.movie_labels = []
        # for movie in self.movie_data.keys():
        #     movie_label = QPushButton(movie)
        #     movie_label.setStyleSheet("color:black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")
        #     movie_label.clicked.connect(lambda checked, m=movie: self.show_sessions(m))
        #     self.movie_labels.append(movie_label)
        #     self.movies_list.addWidget(movie_label)
        # self.movies_widget.setLayout(self.movies_list)
        # self.movies_scroll.setWidget(self.movies_widget)

        # Он колонка: сеанстар (скролл менен жылдырып коро беребиз)
        self.sessions_scroll = QScrollArea(self)
        self.sessions_scroll.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.sessions_scroll.setWidgetResizable(True)

        self.sessions_widget = QWidget()
        self.sessions_list = QVBoxLayout(self.sessions_widget)
        self.session_labels = []
        self.selected_movie = None
        self.sessions_widget.setLayout(self.sessions_list)
        self.sessions_scroll.setWidget(self.sessions_widget)

        layout.addWidget(self.movies_scroll)
        layout.addWidget(self.sessions_scroll)

        # кнопкалар жонундо
        self.buy_button = QPushButton("Buy", self)
        self.buy_button.setGeometry(200, 550, 120, 50)
        self.buy_button.setStyleSheet("background-color: #908960; color: black; font-size: 16px; font-weight: bold;")
        self.buy_button.clicked.connect(self.open_buy_window)

        self.movie_info_button = QPushButton("Movie Info", self)
        self.movie_info_button.setGeometry(370, 600, 120, 50)
        self.movie_info_button.setStyleSheet("background-color: #908960; color: black; font-size: 16px; font-weight: bold;")
        self.movie_info_button.clicked.connect(self.open_movie_info_window)

        self.history_button = QPushButton("History", self)
        self.history_button.setGeometry(540, 550, 120, 50)
        self.history_button.setStyleSheet("background-color: #908960; color: black; font-size: 16px; font-weight: bold;")
        self.history_button.clicked.connect(self.open_history_window)

        self.add_button = QPushButton("Add+", self)
        self.add_button.setGeometry(710, 600, 120, 50)
        self.add_button.setStyleSheet("background-color: #908960; color: black; font-size: 16px; font-weight: bold;")
        self.add_button.clicked.connect(self.open_add_window)

        self.selected_movie = None
        self.selected_session = None
        self.history = requests.get('http://kutmanata.pythonanywhere.com/get_history').json()

    def load_movies(self):
        """
        Загружает данные о фильмах с сервера и обновляет кнопки.
        """
        self.movie_data = requests.get('http://kutmanata.pythonanywhere.com/get_movies').json()
        
        # Очистка существующего макета
        if hasattr(self, 'movies_list'):
            self.clear_layout(self.movies_list)
        else:
            self.movies_list = QVBoxLayout()  # Создаем макет, если его еще нет

        self.movie_labels = []  # Список для хранения кнопок

        # Добавление новых кнопок
        for movie in self.movie_data.keys():
            movie_label = QPushButton(movie)
            movie_label.setStyleSheet("color:black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")
            movie_label.clicked.connect(lambda checked, m=movie: self.show_sessions(m))
            self.movie_labels.append(movie_label)
            self.movies_list.addWidget(movie_label)
        
        # Установка обновленного макета
        self.movies_widget.setLayout(self.movies_list)
        self.movies_scroll.setWidget(self.movies_widget)

    def clear_layout(self, layout):
        """
        Очищает все виджеты из переданного QLayout.
        """
        if layout is not None:
            while layout.count():  # Проход по всем элементам макета
                item = layout.takeAt(0)  # Удаляет элемент из макета
                widget = item.widget()   # Получает виджет из элемента
                if widget is not None:
                    widget.deleteLater()  # Удаляет виджет корректно




    def show_sessions(self, movie):
        global select_movie
        select_movie = movie
        """Кинону тандаганда сеанстар ачылат . кайсыл кинонуку кайсыл болсо."""
        self.selected_movie = movie
        for label in self.session_labels:
            label.setParent(None)
        self.session_labels.clear()

        # Получаем список фильмов с сеансами
        movies_data = requests.get('http://kutmanata.pythonanywhere.com/get_movies').json()
        
        # Ищем фильм в полученных данных
        if movie in movies_data:  # Если фильм найден
            movie_sessions = movies_data[movie]
            
            # Перебираем сеансы для этого фильма
            for session_time, booked_seats in movie_sessions.items():
                session_label = QPushButton(f"{session_time}")
                session_label.setStyleSheet("color: black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")
                
                # Передаем session_time в лямбда-функцию
                session_label.clicked.connect(lambda checked, s=session_time: self.select_date(s))
                self.session_labels.append(session_label)
                self.sessions_list.addWidget(session_label)


    def select_date(self, date):
        global session
        session = date
        self.selected_session = date
    def open_buy_window(self, session):
        # Получаем забронированные места для выбранного фильма и сеанса
        booked = requests.get('http://kutmanata.pythonanywhere.com/get_seance_booked', params={"movie": select_movie, "date": self.selected_session}).json()
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Buy Ticket")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)
        client_label = QLabel(f"Client Name: {main_user}")
        self.client_input = QLineEdit()
        layout.addWidget(client_label)

        seat_layout = QGridLayout()
        self.seats = {}

        # Отображаем кнопки для мест
        for row in range(5):
            for col in range(9):
                seat_id = f"{chr(65+row)}{col+1}"  # Создаем уникальный идентификатор для места
                seat = QPushButton(seat_id)
                seat.setStyleSheet("background-color: white; color: black;")

                # Если место забронировано, делаем его некликабельным
                if seat_id in booked:
                    seat.setStyleSheet("background-color: gray; color: black;")
                    seat.setEnabled(False)

                seat.clicked.connect(lambda checked, btn=seat: self.toggle_seat(btn))
                self.seats[seat_id] = seat
                seat_layout.addWidget(seat, row, col)
        
        layout.addLayout(seat_layout)

        buy_button = QPushButton("Buy")
        buy_button.clicked.connect(lambda: self.confirm_purchase(dialog))
        layout.addWidget(buy_button)

        dialog.setLayout(layout)
        dialog.exec()

    def make_button_unclickable(self, btn):
        btn.setStyleSheet("background-color: gray; color: black;")
        btn.setEnabled(False)

    def toggle_seat(self, btn):
        if btn.styleSheet() == "background-color: white; color: black;":
            btn.setStyleSheet("background-color: red; color: white;")
        else:
            btn.setStyleSheet("background-color: white; color: black;")

    def confirm_purchase(self, dialog):
        purchased = [seat for seat, btn in self.seats.items() if btn.styleSheet() == "background-color: red; color: white;"]
        text = ",".join(purchased)
        print(purchased, text)
        if purchased:
            requests.get('http://kutmanata.pythonanywhere.com/booking_seats', params={'movie':select_movie, 'date':session, 'seats':text})
            requests.get('http://kutmanata.pythonanywhere.com/add_history', params={'client':main_user, 'movie':self.selected_movie, 'session':self.selected_session, 'seats':','.join(purchased), 'date':QDate.currentDate().toString("dd/MM/yyyy")})

                
            #     {
            #     "client": main_user,
            #     "movie": self.selected_movie,
            #     "session": self.selected_session,
            #     "seats": purchased,
            #     "date": QDate.currentDate().toString("dd/MM/yyyy"),
            # }

            dialog.accept()
            self.history = requests.get('http://kutmanata.pythonanywhere.com/get_history').json()
        else:
            QMessageBox.warning(self, "Error", "No seats selected!")

    def open_history_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("History")
        dialog.setFixedSize(600, 400)

        layout = QVBoxLayout(dialog)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search Client:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Client", "Movie", "Session", "Seats", "Date"])
        self.update_history_table()

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        dialog.setLayout(layout)

        dialog.exec()

    def update_history_table(self):
        self.table.setRowCount(len(self.history))
        for row, record in enumerate(self.history):
            self.table.setItem(row, 0, QTableWidgetItem(record["client"]))
            self.table.setItem(row, 1, QTableWidgetItem(record["movie"]))
            self.table.setItem(row, 2, QTableWidgetItem(record["session"]))
            self.table.setItem(row, 3, QTableWidgetItem(", ".join(record["seats"])))
            self.table.setItem(row, 4, QTableWidgetItem(record["date"]))

    def filter_history(self):
        search_text = self.search_input.text().lower()
        filtered_data = [
            record for record in self.history if search_text in record["client"].lower()
        ]
        self.table.setRowCount(len(filtered_data))
        for row, record in enumerate(filtered_data):
            self.table.setItem(row, 0, QTableWidgetItem(record["client"]))
            self.table.setItem(row, 1, QTableWidgetItem(record["movie"]))
            self.table.setItem(row, 2, QTableWidgetItem(record["session"]))
            self.table.setItem(row, 3, QTableWidgetItem(", ".join(record["seats"])))
            self.table.setItem(row, 4, QTableWidgetItem(record["date"]))

    def open_movie_info_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Movie Info")
        dialog.setFixedSize(600, 400)

        layout = QVBoxLayout(dialog)

        self.movie_info_table = QTableWidget()
        self.movie_info_table.setColumnCount(3)
        self.movie_info_table.setHorizontalHeaderLabels(["Movie", "Session", "Clients"])
        self.update_movie_info_table()

        layout.addWidget(self.movie_info_table)
        dialog.setLayout(layout)
        dialog.exec()

    def update_movie_info_table(self):
        self.movie_info_table.setRowCount(len(requests.get('http://kutmanata.pythonanywhere.com/get_movies').json()))
        for row, (movie, data) in enumerate(self.movie_data.items()):
            self.movie_info_table.setItem(row, 0, QTableWidgetItem(movie))
            self.movie_info_table.setItem(row, 1, QTableWidgetItem(", ".join(data["sessions"])))
            self.movie_info_table.setItem(row, 2, QTableWidgetItem(str(data["people"])))

    def open_add_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Movie")
        dialog.setFixedSize(500, 300)

        layout = QVBoxLayout(dialog)

        movie_label = QLabel("Movie Name:")
        self.movie_input = QLineEdit()
        layout.addWidget(movie_label)
        layout.addWidget(self.movie_input)

        session_label = QLabel("Sessions (comma separated):")
        self.session_input = QLineEdit()
        layout.addWidget(session_label)
        layout.addWidget(self.session_input)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_movie)
        layout.addWidget(add_button)

        dialog.setLayout(layout)
        dialog.exec()

    def add_movie(self):
        movie = self.movie_input.text()
        sessions = self.session_input.text()
        if movie and sessions:
            sessions = sessions.split(",")
            requests.get('http://kutmanata.pythonanywhere.com/add_movie', params={'movie':movie, 'date':sessions})
        self.load_movies()

    # def update_movies_list(self):
    #     self.movie_labels.clear()
    #     for movie in self.movie_data.keys():
    #         movie_label = QPushButton(movie)
    #         movie_label.setStyleSheet("color:black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")
    #         movie_label.clicked.connect(lambda checked, m=movie: self.show_sessions(m))
    #         self.movie_labels.append(movie_label)
    #         self.movies_list.addWidget(movie_label)
    def open_movie_info_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Movie Info")
        dialog.setFixedSize(600, 500)

        layout = QVBoxLayout(dialog)

        # Movie Selection Dropdown
        movie_label = QLabel("Select Movie:")
        self.movie_dropdown = QComboBox()
        self.movie_dropdown.addItems(self.movie_data.keys())
        self.movie_dropdown.currentTextChanged.connect(self.update_session_dropdown)

        # Session Selection Dropdown
        session_label = QLabel("Select Session:")
        self.session_dropdown = QComboBox()
        self.update_session_dropdown() 

        # Movie Info Table
        self.movie_info_table = QTableWidget()
        self.movie_info_table.setColumnCount(3)
        self.movie_info_table.setHorizontalHeaderLabels(["Client", "Seats", "Date"])

        # Update Button
        update_button = QPushButton("Show Info")
        update_button.clicked.connect(self.update_movie_info_table)

        # Add widgets to layout
        layout.addWidget(movie_label)
        layout.addWidget(self.movie_dropdown)
        layout.addWidget(session_label)
        layout.addWidget(self.session_dropdown)
        layout.addWidget(update_button)
        layout.addWidget(self.movie_info_table)

        dialog.setLayout(layout)
        dialog.exec()

    def update_session_dropdown(self):
       
        selected_movie = self.movie_dropdown.currentText()
        self.session_dropdown.clear()
        if selected_movie in self.movie_data:
            self.session_dropdown.addItems(self.movie_data[selected_movie])

    def update_movie_info_table(self):
       
        selected_movie = self.movie_dropdown.currentText()
        selected_session = self.session_dropdown.currentText()

        if not selected_movie or not selected_session:
            QMessageBox.warning(self, "Error", "Please select both a movie and a session.")
            return

        # Filter history for selected movie and session
        filtered_history = [
            record for record in requests.get('http://kutmanata.pythonanywhere.com/get_history').json()
            if record["movie"] == selected_movie and record["session"] == selected_session
        ]

        self.movie_info_table.setRowCount(len(filtered_history))
        for row, record in enumerate(filtered_history):
            self.movie_info_table.setItem(row, 0, QTableWidgetItem(record["client"]))
            self.movie_info_table.setItem(row, 1, QTableWidgetItem(", ".join(record["seats"])))
            self.movie_info_table.setItem(row, 2, QTableWidgetItem(record["date"]))

    # def show_sessions(self, movie):
 
    #     self.selected_movie = movie
    #     for label in self.session_labels:
    #         label.setParent(None)
    #     self.session_labels.clear()

    #     for session in self.movie_data[movie]:
    #         session_label = QPushButton(session)
    #         session_label.setStyleSheet("color: black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")
    #         session_label.clicked.connect(lambda checked, s=session: self.select_date(s))
    #         self.session_labels.append(session_label)
    #         self.sessions_list.addWidget(session_label)

    #     # тандалган кинолорду корсотуу
    #     for label in self.movie_labels:
    #         if label.text() == movie:
    #             label.setStyleSheet("color: white; font-size: 20px; padding: 10px; background-color: #5F9F60; margin-bottom: 10px;")
    #         else:
    #             label.setStyleSheet("color:black; font-size: 20px; padding: 10px; background-color: #908960; margin-bottom: 10px;")

if __name__ == "__main__":
    app = QApplication([])
    window = CinemaLoginApp()
    window.show()
    app.exec()

