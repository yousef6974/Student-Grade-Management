import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)
from PySide6.QtCore import Qt


class StudentGradeManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Student Grade Management System")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet(self.get_stylesheet())

        # Main Widget
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Title
        title_label = QLabel("Student Grade Management System")
        title_label.setObjectName("title_label")
        main_layout.addWidget(title_label)

        # Table Subtitle
        results_label = QLabel("Grades Sheet:")
        results_label.setObjectName("results_label")
        main_layout.addWidget(results_label)

        # Excel Table Widget
        self.results_display = QTableWidget()
        self.results_display.setObjectName("results_display")
        self.results_display.setColumnCount(3)
        self.results_display.setHorizontalHeaderLabels(["Name", "Score", "Grade"])
        
        # Stretch columns to automatically fit the window width
        self.results_display.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
       # Set up initial rows and connect cell change listener
        self.results_display.setRowCount(10)
        self.results_display.cellChanged.connect(self.on_cell_changed)

        main_layout.addWidget(self.results_display)

        # Summary Buttons Layout
        summary_layout = QHBoxLayout()
        summary_layout.setObjectName("summary_layout")

        self.export_button = QPushButton("Export Results")
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self.export_results)

        self.reset_button = QPushButton("Reset All")
        self.reset_button.setObjectName("reset_button")
        self.reset_button.clicked.connect(self.reset_all)

        summary_layout.addWidget(self.export_button)
        summary_layout.addWidget(self.reset_button)
        main_layout.addLayout(summary_layout)

    def get_stylesheet(self):
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel#title_label {
            qproperty-alignment: 'AlignCenter';
            padding: 15px 0px;
            font-weight: bold;
            font-size: 24px;
            color: #gray;
        }
        QLabel#results_label {
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            padding-top: 10px;
        }
        QTableWidget {
            background-color: #ffffff;
            gridline-color: #d0d0d0;
            border: 1px solid #ababab;
            font-size: 14px;
            color: #333333;
        }
        QHeaderView::section {
            background-color: #f3f3f3;
            padding: 8px;
            border: 1px solid #d0d0d0;
            font-weight: bold;
            font-size: 13px;
            color: #444444;
        }
        QTableWidget::item {
            padding: 1px;
        }
        QTableWidget::item:selected {
            background-color: #e2f0d9;
            color: #000000;
        }
        QPushButton {
            padding: 8px 15px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 4px;
            border: 1px solid #ababab;
            background-color: #ffffff;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        QPushButton#export_button {
            background-color: #107c41;
            color: white;
            border: 1px solid #0e6c38;
        }
        QPushButton#export_button:hover {
            background-color: #0e6c38;
        }
        QPushButton#reset_button {
            background-color: #d9534f;
            color: white;
            border: 1px solid #d43f3a;
        }
        QPushButton#reset_button:hover {
            background-color: #c9302c;
        }
        """

    def calculate_grade(self, score):
        try:
            score = float(score)
            if score < 0 or score > 100:
                return None, "Invalid"
            elif 0 <= score < 50: return score, "F"
            elif 50 <= score < 60: return score, "D"
            elif 60 <= score < 70: return score, "C"
            elif 70 <= score < 80: return score, "C+"
            elif 80 <= score < 85: return score, "B"
            elif 85 <= score < 90: return score, "B+"
            elif 90 <= score < 95: return score, "A"
            elif 95 <= score <= 100: return score, "A+"
        except ValueError:
            return None, "Invalid"

    def on_cell_changed(self, row, column):
       # Auto-extend table: add a new row when the last row is modified
        if row == self.results_display.rowCount() - 1:
            self.results_display.blockSignals(True)
            self.results_display.insertRow(self.results_display.rowCount())
            self.results_display.blockSignals(False)

        # Auto-calculate grade upon updating the score column
        if column == 1:
            self.results_display.blockSignals(True)
            score_item = self.results_display.item(row, column)
            
            if score_item and score_item.text().strip():
                score_text = score_item.text().strip()
                score, grade = self.calculate_grade(score_text)
                
                if grade != "Invalid":
                    grade_item = QTableWidgetItem(grade)
                    # Prevent the user from manually editing the grade cell
                    grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                    self.results_display.setItem(row, 2, grade_item)
                else:
                    self.results_display.setItem(row, 2, QTableWidgetItem(""))
            else:
                self.results_display.setItem(row, 2, QTableWidgetItem(""))
                
            self.results_display.blockSignals(False)

    def reset_all(self):
        reply = QMessageBox.question(
            self, "Confirm Reset", "Are you sure you want to reset all data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.results_display.blockSignals(True)
           # Clear row count to prevent removing headers, then re-initialize with 10 blank rows 
            self.results_display.setRowCount(0)
            self.results_display.setRowCount(10)
            self.results_display.blockSignals(False)

    def export_results(self):
        # Pull data directly from table cells for export
        valid_students = []
        for row in range(self.results_display.rowCount()):
            name_item = self.results_display.item(row, 0)
            score_item = self.results_display.item(row, 1)
            grade_item = self.results_display.item(row, 2)
            
            name = name_item.text().strip() if name_item else ""
            score = score_item.text().strip() if score_item else ""
            grade = grade_item.text().strip() if grade_item else ""
            
            if name or score:  # Process only the rows populated by the user
                valid_students.append({"name": name, "score": score, "grade": grade})

        if not valid_students:
            QMessageBox.warning(self, "No Data", "No student data to export.")
            return

        try:
            with open("student_grades.txt", "w", encoding="utf-8") as file:
                file.write("Student Grade Management System - Results\n")
                file.write("=" * 50 + "\n\n")
                file.write(f"{'Name':<20}\t{'Score':<10}\t{'Grade':<10}\n")
                file.write("-" * 50 + "\n")
                
                for student in valid_students:
                    file.write(f"{student['name']:<20}\t{student['score']:<10}\t{student['grade']:<10}\n")
                    
            QMessageBox.information(self, "Success", "Results exported successfully to 'student_grades.txt'!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = StudentGradeManagementSystem()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
