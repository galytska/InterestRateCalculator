from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QCheckBox, QTreeView, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QStandardItemModel


class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        main_window = QWidget()
        self.resize(800, 600)
        self.setWindowTitle('Interest Rate Calculator')

        self.interest_rate_lineedit = QLineEdit()
        self.init_invest_lineedit = QLineEdit()
        self.num_of_years_lineedit = QLineEdit()
        self.dar_mode_checkbox = QCheckBox('Dark Mode')
        self.model = QStandardItemModel()
        self.year_total_treeview = QTreeView()
        self.year_total_treeview.setModel(self.model)
        self.calculate_button = QPushButton('Calculate')
        self.reset_button = QPushButton('Reset')
        self.save_button = QPushButton('Save')
        self.figure = QLabel('------Here wille the plot------')

        master_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()

        row1.addWidget(QLabel('Interest Rate (%):'))
        row1.addWidget(self.interest_rate_lineedit)
        row1.addWidget(QLabel('Initial Investment ($):'))
        row1.addWidget(self.init_invest_lineedit)
        row1.addWidget(QLabel('Number of Years:'))
        row1.addWidget(self.num_of_years_lineedit)
        row1.addWidget(self.dar_mode_checkbox)
        master_layout.addLayout(row1)

        column1.addWidget(self.year_total_treeview)
        column1.addWidget(self.calculate_button)
        column1.addWidget(self.reset_button)
        column1.addWidget(self.save_button)
        row2.addLayout(column1, 20)
        column2.addWidget(self.figure)
        row2.addLayout(column2, 80)
        master_layout.addLayout(row2)

        main_window.setLayout(master_layout)
        self.setCentralWidget(main_window)


if __name__ == '__main__':
    app = QApplication([])
    main_window = FinanceApp()
    main_window.show()
    app.exec()
