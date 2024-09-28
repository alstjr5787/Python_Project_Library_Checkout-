import os
import numpy as np
import requests
import example

import json
import sys
from datetime import datetime
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
import cv2

# 환경 변수 설정 mac M1
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')

from pyzbar.pyzbar import decode

class AddMemberForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원 추가")
        self.setGeometry(1050, 350, 400, 300)

        layout = QVBoxLayout()

        self.member_id_input = QLineEdit(self)
        self.member_id_input.setPlaceholderText("아이디")
        layout.addWidget(self.member_id_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("비밀번호")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("이름")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("전화번호")
        layout.addWidget(self.phone_input)

        self.submit_button = QPushButton("추가", self)
        self.submit_button.clicked.connect(self.add_member)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_member(self):
        member_id = self.member_id_input.text()
        password = self.password_input.text()
        name = self.name_input.text()
        phone = self.phone_input.text()

        data = {
            'member_id': member_id,
            'member_password': password,
            'name': name,
            'phone_number': phone
        }

        try:
            response = requests.post('http://domain.com/LibraryProject/signup.php', data=data)
            response_data = response.json()
            QMessageBox.information(self, "회원 추가", response_data['message'])
            if response_data['status'] == 'success':
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"서버와 연결할 수 없습니다: {str(e)}")


############################################################################ 회원등록



class SearchResultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.user_data = self.fetch_user_data()
        self.populate_user_table()

    def init_ui(self):
        layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        self.name_search_edit = QLineEdit(self)
        self.name_search_edit.setPlaceholderText('이름으로 검색')
        name_layout.addWidget(self.name_search_edit)

        self.search_by_name_button = QPushButton('검색', self)
        self.search_by_name_button.clicked.connect(self.filter_users_by_name)
        name_layout.addWidget(self.search_by_name_button)

        layout.addLayout(name_layout)

        self.user_table_widget = QTableWidget(self)
        self.user_table_widget.setColumnCount(4)
        self.user_table_widget.setHorizontalHeaderLabels(['선택', '아이디', '이름', '전화번호'])
        layout.addWidget(self.user_table_widget)

        self.select_button = QPushButton('선택', self)
        self.select_button.clicked.connect(self.select_users)
        layout.addWidget(self.select_button)

        self.setLayout(layout)
        self.setWindowTitle('회원 검색')
        self.resize(460, 400)

    def fetch_user_data(self):
        url = 'http://domain.com/LibraryProject/get_user.php'
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            QMessageBox.warning(self, '오류', '사용자 정보를 가져오는 데 실패했습니다.')
            return []

    def populate_user_table(self):
        self.user_table_widget.setRowCount(len(self.user_data))
        for row, user in enumerate(self.user_data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.user_table_widget.setItem(row, 0, checkbox_item)
            self.user_table_widget.setItem(row, 1, QTableWidgetItem(user['member_id']))
            self.user_table_widget.setItem(row, 2, QTableWidgetItem(user['name']))
            self.user_table_widget.setItem(row, 3, QTableWidgetItem(user['phone_number']))

    def filter_users_by_name(self):
        search_name = self.name_search_edit.text().strip().lower()
        filtered_data = [user for user in self.user_data if search_name in user['name'].lower()]

        self.user_table_widget.setRowCount(len(filtered_data))
        for row, user in enumerate(filtered_data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.user_table_widget.setItem(row, 0, checkbox_item)
            self.user_table_widget.setItem(row, 1, QTableWidgetItem(user['member_id']))
            self.user_table_widget.setItem(row, 2, QTableWidgetItem(user['name']))
            self.user_table_widget.setItem(row, 3, QTableWidgetItem(user['phone_number']))

    def select_users(self):
        selected_ids = []
        for row in range(self.user_table_widget.rowCount()):
            checkbox_item = self.user_table_widget.item(row, 0)
            if checkbox_item.checkState() == Qt.Checked:
                member_id = self.user_table_widget.item(row, 1).text()
                selected_ids.append(member_id)

        if selected_ids:
            if self.parent():
                self.parent().rent_quantity_edit.setText(", ".join(selected_ids))
            self.accept()
        else:
            QMessageBox.warning(self, '경고', '사용자를 선택하세요.')


class CameraThread(QThread):
    update_frame = pyqtSignal(QImage)
    barcode_detected = pyqtSignal(str)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        last_barcode = None

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            decoded_objects = decode(frame)

            # 바코드 주위에 박스
            for obj in decoded_objects:
                current_barcode = obj.data.decode('utf-8')
                if current_barcode != last_barcode:
                    last_barcode = current_barcode
                    self.barcode_detected.emit(current_barcode)

                points = obj.polygon
                if len(points) >= 4:
                    if len(points) == 4:
                        cv2.polylines(frame, [np.array(points)], isClosed=True, color=(0, 255, 0),
                                      thickness=4)
                    else:
                        hull = cv2.convexHull(np.array(points))
                        cv2.polylines(frame, [hull], isClosed=True, color=(0, 255, 0), thickness=4)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

            self.update_frame.emit(q_image)

        self.cap.release()


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("도서 관리 시스템")
        self.resize(1300, 600)

        button_group = QGroupBox("대출-반납")
        group_layout = QVBoxLayout()

        self.rent_button = QPushButton('대여하기', self)
        self.rent_button.clicked.connect(self.rent_book)

        self.return_button = QPushButton('반납하기', self)
        self.return_button.clicked.connect(self.return_book)

        group_layout.addWidget(self.rent_button)
        group_layout.addWidget(self.return_button)

        button_group.setLayout(group_layout)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.submit_button = QPushButton("회원 신규등록", self)
        self.submit_button.setFixedSize(120, 40)

        self.submit_button.clicked.connect(self.show_add_member_form)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("제목 또는 대출자 이름으로 검색")
        self.title_checkbox = QCheckBox("제목", self)
        self.name_checkbox = QCheckBox("대출자 이름", self)
        self.search_button_left = QPushButton("검색", self)
        self.search_button_left.clicked.connect(self.search_books)
        search_layout.addWidget(self.title_checkbox)
        search_layout.addWidget(self.name_checkbox)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button_left)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['책 제목', '저자', '대출자', '대출 일자', '반납 일자', '상태'])
        self.load_data()

        right_layout = QVBoxLayout()

        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText('제목')
        self.author_edit = QLineEdit(self)
        self.author_edit.setPlaceholderText('저자')
        self.isbn_edit = QLineEdit(self)
        self.isbn_edit.setPlaceholderText('ISBN')
        self.isbn_edit.setReadOnly(True)

        self.rent_quantity_edit = QLineEdit(self)
        self.rent_quantity_edit.setPlaceholderText('대여자 아이디')
        self.rent_quantity_edit.setReadOnly(True)

        self.search_button_right = QPushButton('검색', self)
        self.search_button_right.clicked.connect(self.search_renter)

        rent_layout = QHBoxLayout()

        rent_layout.addWidget(self.rent_quantity_edit)
        rent_layout.addWidget(self.search_button_right)

        self.copies_edit = QLineEdit(self)
        self.copies_edit.setPlaceholderText('대여 가능 수')

        self.add_button = QPushButton('책 추가하기', self)
        self.add_button.clicked.connect(self.add_book)

        right_layout.addWidget(self.title_edit)
        right_layout.addWidget(self.author_edit)
        right_layout.addWidget(self.isbn_edit)
        right_layout.addLayout(rent_layout)
        right_layout.addWidget(self.copies_edit)
        right_layout.addWidget(self.add_button)
        right_layout.addWidget(button_group)

        self.camera_window = QLabel(self)
        self.camera_window.setFixedSize(500, 500)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_layout.addItem(spacer)
        right_layout.addWidget(self.camera_window)

        left_layout.addWidget(self.submit_button)
        left_layout.addLayout(search_layout)
        left_layout.addWidget(self.table_widget)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.table_widget.setColumnWidth(0, 180)
        self.table_widget.setColumnWidth(1, 120)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 120)
        self.table_widget.setColumnWidth(4, 120)
        self.table_widget.setColumnWidth(5, 80)

        self.table_widget.setFixedSize(735, 600)

        self.camera_thread = CameraThread()
        self.camera_thread.update_frame.connect(self.update_video_frame)
        self.camera_thread.barcode_detected.connect(self.fetch_book_info)
        self.camera_thread.start()




    def load_data(self):
        response = requests.get("http://domain.com/LibraryProject/get_book.php")
        if response.status_code == 200:
            data = response.json()
            self.populate_table(data)

    def populate_table(self, data):
        self.table_widget.setRowCount(len(data))
        for row_index, book in enumerate(data):
            self.table_widget.setItem(row_index, 0, self.create_read_only_item(book.get("title", "")))
            self.table_widget.setItem(row_index, 1, self.create_read_only_item(book.get("author", "")))
            self.table_widget.setItem(row_index, 2, self.create_read_only_item(book.get("member_name", "")))
            self.table_widget.setItem(row_index, 3,
                                      self.create_read_only_item(self.format_date(book.get("loan_date", ""))))
            self.table_widget.setItem(row_index, 4,
                                      self.create_read_only_item(self.format_date(book.get("return_date", ""))))
            self.table_widget.setItem(row_index, 5, self.create_read_only_item(book.get("status", "")))

    def search_books(self):
        search_text = self.search_input.text().strip()
        title_search = self.title_checkbox.isChecked()
        name_search = self.name_checkbox.isChecked()
        response = requests.get("http://domain.com/LibraryProject/get_book.php")

        if response.status_code == 200:
            data = response.json()
            filtered_data = []

            for book in data:
                if (title_search and search_text.lower() in book.get("title", "").lower()) or \
                        (name_search and search_text.lower() in book.get("member_name", "").lower()):
                    filtered_data.append(book)

            self.populate_table(filtered_data)

    def fetch_book_info(self, current_barcode):
        response = requests.get(f'http://domain.com/LibraryProject/book_data.php?isbn={current_barcode}')
        book_info = response.json()

        if book_info['status'] == 'success':
            book = book_info['data']
            self.title_edit.setText(book['title'])
            self.author_edit.setText(book['author'])
            self.isbn_edit.setText(book['ISBN'])
            self.copies_edit.setText(str(book['available_copies']))
        else:
            self.isbn_edit.setText(current_barcode)
            self.show_message_box(current_barcode)

    def show_message_box(self, current_barcode):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("등록되지 않은 책")
        msg_box.setText("등록되지 않은 책입니다. 책을 추가하시겠습니까?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msg_box.exec_()
        if result == QMessageBox.Ok:
            self.isbn_edit.setText(current_barcode)

    def add_book(self):
        title = self.title_edit.text()
        author = self.author_edit.text()
        isbn = self.isbn_edit.text()
        if title and author and isbn:
            data = {
                'title': title,
                'author': author,
                'isbn': isbn,
                'total_copies': 1
            }
            response = requests.post('http://domain.com/LibraryProject/add_book.php', json=data)
            response_data = response.json()
            if response_data['status'] == 'success':
                self.load_data()
                QMessageBox.information(self, "성공", "책이 추가되었습니다.")
            else:
                QMessageBox.warning(self, "오류", "해당 책이 이미 등록되어 있습니다..")

    def format_date(self, date_string):
        if date_string:
            try:
                date_obj = datetime.strptime(date_string, "%Y-%m-%d")
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                return date_string
        return ""

    def create_read_only_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def update_video_frame(self, frame):
        scaled_frame = frame.scaled(self.camera_window.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.camera_window.setPixmap(QPixmap.fromImage(scaled_frame))

    def rent_book(self):
        member_id = self.rent_quantity_edit.text()
        book_title = self.title_edit.text()

        url = "http://domain.com/LibraryProject/add_rent.php"
        data = {
            'member_id': member_id,
            'book_title': book_title
        }
        try:
            response = requests.post(url, data=data)

            if response.status_code == 200:
                if "대여 정보가 추가되었습니다." in response.text:
                    QMessageBox.information(self, '대여 정보', '대여 정보가 성공적으로 추가되었습니다.')
                    self.rent_quantity_edit.clear()
                    self.refresh_table()
                elif "남은 재고가 없습니다" in response.text:
                    QMessageBox.warning(self, '대여 불가', '대여 불가: 남은 재고가 없습니다.')
                else:
                    QMessageBox.warning(self, '대여 정보', '대여 정보 추가에 실패했습니다.')
            else:
                QMessageBox.warning(self, '대여 정보', '대여를 실패했습니다.')

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, '대여 정보', f'서버와의 통신에 실패했습니다: {e}')
    def return_book(self):

        member_id = self.rent_quantity_edit.text()
        book_title = self.title_edit.text()

        url = "http://domain.com/LibraryProject/add_return.php"
        data = {
            'member_id': member_id,
            'book_title': book_title
        }

        try:
            response = requests.post(url, data=data)

            if response.status_code == 200:
                if "성공적으로 반납" in response.text:
                    QMessageBox.information(self, '반납 정보', '책이 성공적으로 반납되었습니다.')
                    self.rent_quantity_edit.clear()
                    self.refresh_table()
                elif "반납할 대여 기록을 찾을 수 없습니다" in response.text:
                    QMessageBox.warning(self, '반납 실패', '반납할 대여 기록을 찾을 수 없습니다.')
                else:
                    QMessageBox.warning(self, '반납 정보', '반납을 실패했습니다.')
            else:
                QMessageBox.warning(self, '반납 정보', '반납을 실패했습니다.')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, '반납 정보', f'서버와의 통신에 실패했습니다: {e}')

    def refresh_table(self):
        url = "http://domain.com/LibraryProject/get_book.php"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.populate_table(data)
            else:
                QMessageBox.warning(self, '대여 기록', '대여 기록을 가져오는 데 실패했습니다.')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, '대여 기록', f'서버와의 통신에 실패했습니다: {e}')

    def search_renter(self):

        self.search_result_dialog = SearchResultDialog(self)
        self.search_result_dialog.exec_()

    def show_add_member_form(self):
        self.add_member_form = AddMemberForm()
        self.add_member_form.setWindowTitle("회원 추가")
        self.add_member_form.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
