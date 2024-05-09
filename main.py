import os.path

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QCheckBox, QTreeView, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self.calculate_button.clicked.connect(self.calculate)
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_input)
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_date)
        self.save_button.hide()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

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
        row2.addLayout(column1, 30)
        column2.addWidget(self.canvas)
        row2.addLayout(column2, 70)
        master_layout.addLayout(row2)

        main_window.setLayout(master_layout)
        self.setCentralWidget(main_window)

    def calculate(self):
        try:
            init_invest = float(self.init_invest_lineedit.text())
            interest_rate = float(self.interest_rate_lineedit.text())
            num_of_years = int(self.num_of_years_lineedit.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid input Please Enter a valid number')
            return
        else:
            total = init_invest
            for year in range(1, num_of_years + 1):
                total += total * (interest_rate / 100)
                item_year = QStandardItem(str(year))
                item_total = QStandardItem(f'{total:.2f}')
                self.model.appendRow([item_year, item_total])

            self.figure.clear()
            ax = self.figure.subplots()
            years = list(range(1, num_of_years + 1))
            totals = [init_invest * (1 + interest_rate / 100) ** year for year in years]

            ax.plot(years, totals)
            ax.set_title("Interest Chart")
            ax.set_xlabel("Year")
            ax.set_ylabel("Total")
            self.canvas.draw()

            self.save_button.show()

    def reset_input(self):
        self.init_invest_lineedit.clear()
        self.interest_rate_lineedit.clear()
        self.num_of_years_lineedit.clear()
        self.model.clear()

        self.figure.clear()
        self.canvas.draw()

    def save_date(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Save directory')
        if dir_path:
            save_dir_path = os.path.join(dir_path, 'Saved')
            os.makedirs(save_dir_path, exist_ok=True)
            save_file_path = os.path.join(save_dir_path, 'result_finance.csv')
            with open(save_file_path, 'w') as file:
                file.write('Year,Total\n')
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write(f'{year},{total}\n')

            plt.savefig(os.path.join(save_dir_path, 'canvas.png'))
            QMessageBox.information(self, 'Save result', 'Results saved to your folder')
        else:
            QMessageBox.warning(self, 'Save result', 'Saved directory not selected')


if __name__ == '__main__':
    app = QApplication([])
    main_window = FinanceApp()
    main_window.show()
    app.exec()
