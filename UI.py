import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTextEdit, QDialog, QHBoxLayout, QScrollArea

from scipy.sparse import load_npz

# Load the sparse matrix
sparse_matrix = load_npz("sparse_matrix.npz")

class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #666666;
            }
        """)

class ProductModifyDialog(QDialog):
    def __init__(self, product_id):
        super().__init__()
        self.setWindowTitle("Modify Pin Codes")
        self.setMinimumSize(300, 200)
        self.setStyleSheet("background-color: #ffe5b4;")

        self.product_id = product_id

        self.label_search = QLabel(f"Product ID: {product_id}", self)
        self.label_pincode = QLabel("Pin Code:", self)
        self.entry_pincode = QLineEdit(self)
        self.add_pincode_button = CustomButton("Add Pin Code")
        self.remove_pincode_button = CustomButton("Remove Pin Code")
        self.result_text = QTextEdit(self)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_search)
        layout.addWidget(self.label_pincode)
        layout.addWidget(self.entry_pincode)
        layout.addWidget(self.add_pincode_button)
        layout.addWidget(self.remove_pincode_button)
        layout.addWidget(self.result_text)

        self.add_pincode_button.clicked.connect(self.add_pincode)
        self.remove_pincode_button.clicked.connect(self.remove_pincode)

        self.result_text.setStyleSheet("""
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #333333;
            border-radius: 10px;
            padding: 10px;
        """)

    def add_pincode(self):
        try:
            pincode = int(self.entry_pincode.text())
            if 0 <= pincode < sparse_matrix.shape[1]:
                sparse_matrix[self.product_id, pincode] = 1
                self.result_text.setPlainText(f"Pincode {pincode} added for Product {self.product_id}")
                return
            QMessageBox.critical(self, "Error", "Invalid pincode")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for the pincode")

    def remove_pincode(self):
        try:
            pincode = int(self.entry_pincode.text())
            if 0 <= pincode < sparse_matrix.shape[1]:
                if sparse_matrix[self.product_id, pincode] == 1:
                    sparse_matrix[self.product_id, pincode] = 0
                    self.result_text.setPlainText(f"Pincode {pincode} removed for Product {self.product_id}")
                else:
                    QMessageBox.critical(self, "Error", f"Pincode {pincode} is not associated with Product {self.product_id}")
                return
            QMessageBox.critical(self, "Error", "Invalid pincode")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for the pincode")

class ProductSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Search")
        self.setMinimumSize(400, 400)
        self.setStyleSheet("background-color: #ffe5b4;")

        self.label_search = QLabel("Search by Product ID:", self)
        self.entry_search = QLineEdit(self)
        self.search_button = CustomButton("Search")
        self.modify_button = CustomButton("Modify")
        self.close_button = CustomButton("Close")
        self.result_text = QTextEdit(self)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_search)
        layout.addWidget(self.entry_search)
        layout.addWidget(self.search_button)
        layout.addWidget(self.modify_button)
        layout.addWidget(self.result_text)
        layout.addWidget(self.close_button)

        self.search_button.clicked.connect(self.search_product)
        self.modify_button.clicked.connect(self.modify_product)
        self.close_button.clicked.connect(self.close)

        self.result_text.setStyleSheet("""
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #333333;
            border-radius: 10px;
            padding: 10px;
        """)

    def search_product(self):
        try:
            product_id = int(self.entry_search.text())
            if 0 <= product_id < sparse_matrix.shape[0]:
                pincodes = sparse_matrix.getrow(product_id).indices
                self.result_text.setPlainText(f"Pincodes for Product {product_id}:\n{', '.join(map(str, pincodes))}")
                return
            QMessageBox.critical(self, "Error", "Invalid product ID")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for the product ID")

    def modify_product(self):
        try:
            product_id = int(self.entry_search.text())
            if 0 <= product_id < sparse_matrix.shape[0]:
                dialog = ProductModifyDialog(product_id)
                dialog.exec_()
                return
            QMessageBox.critical(self, "Error", "Invalid product ID")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for the product ID")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductSearchApp()
    window.show()
    sys.exit(app.exec_())
