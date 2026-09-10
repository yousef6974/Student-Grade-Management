import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import QSize


class StudentGradeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.students_data = []

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Student Grade Management System")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet(self.get_stylesheet())

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Title
        title_label = QLabel("Student Grade Management System")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Student Name Input
        name_layout = QHBoxLayout()
        name_label = QLabel("Student Name:")
        name_label.setMinimumWidth(100)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter student name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Score Input
        score_layout = QHBoxLayout()
        score_label = QLabel("Score (0-100):")
        score_label.setMinimumWidth(100)
        self.score_input = QLineEdit()
        self.score_input.setPlaceholderText("Enter score")
        score_layout.addWidget(score_label)
        score_layout.addWidget(self.score_input)
        main_layout.addLayout(score_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)
        self.add_button.setMinimumHeight(40)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_inputs)
        self.clear_button.setMinimumHeight(40)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        # Results Display
        results_label = QLabel("Results:")
        results_font = QFont()
        results_font.setBold(True)
        results_label.setFont(results_font)
        main_layout.addWidget(results_label)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(300)
        main_layout.addWidget(self.results_display)

        # Summary Layout
        summary_layout = QHBoxLayout()
        
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setMinimumHeight(40)
        
        self.reset_button = QPushButton("Reset All")
        self.reset_button.clicked.connect(self.reset_all)
        self.reset_button.setMinimumHeight(40)
        
        summary_layout.addWidget(self.export_button)
        summary_layout.addWidget(self.reset_button)
        main_layout.addLayout(summary_layout)

    def get_stylesheet(self):
        """Return custom stylesheet for the application"""
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                font-size: 11px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #0d47a1;
            }
            QLineEdit:focus {
                border: 2px solid #0d47a1;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-family: Courier;
                font-size: 10px;
            }
        """

    def calculate_grade(self, score):
        """Calculate grade based on score"""
        try:
            score = int(score)
            
            if score < 0 or score > 100:
                return None, "Invalid"
            elif 0 <= score < 50:
                return score, "F"
            elif 50 <= score < 60:
                return score, "D"
            elif 60 <= score < 70:
                return score, "C"
            elif 70 <= score < 80:
                return score, "C+"
            elif 80 <= score < 85:
                return score, "B"
            elif 85 <= score < 90:
                return score, "B+"
            elif 90 <= score < 95:
                return score, "A"
            elif 95 <= score <= 100:
                return score, "A+"
        except ValueError:
            return None, "Invalid"

    def add_student(self):
        """Add a new student and display results"""
        name = self.name_input.text().strip()
        score_text = self.score_input.text().strip()

        # Validation
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a student name.")
            return

        if not score_text:
            QMessageBox.warning(self, "Input Error", "Please enter a score.")
            return

        score, grade = self.calculate_grade(score_text)

        if grade == "Invalid":
            QMessageBox.warning(
                self, 
                "Invalid Score", 
                "Please enter a valid number between 0 and 100."
            )
            return

        # Add to data and display
        self.students_data.append({"name": name, "score": score, "grade": grade})
        self.update_results_display()
        self.clear_inputs()

    def update_results_display(self):
        """Update the results display area"""
        results_text = "Name\t\tScore\tGrade\n"
        results_text += "-" * 40 + "\n"

        for student in self.students_data:
            results_text += f"{student['name']:<20}\t{student['score']}\t{student['grade']}\n"

        if self.students_data:
            results_text += "-" * 40 + "\n"
            avg_score = sum(s['score'] for s in self.students_data) / len(self.students_data)
            results_text += f"Average Score: {avg_score:.2f}\n"
            results_text += f"Total Students: {len(self.students_data)}"

        self.results_display.setText(results_text)

    def clear_inputs(self):
        """Clear input fields"""
        self.name_input.clear()
        self.score_input.clear()
        self.name_input.setFocus()

    def reset_all(self):
        """Reset all data"""
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            "Are you sure you want to reset all data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.students_data = []
            self.results_display.clear()
            self.clear_inputs()

    def export_results(self):
        """Export results to a text file"""
        if not self.students_data:
            QMessageBox.warning(self, "No Data", "No student data to export.")
            return

        try:
            with open("student_grades.txt", "w") as file:
                file.write("Student Grade Management System - Results\n")
                file.write("=" * 50 + "\n\n")
                file.write("Name\t\tScore\tGrade\n")
                file.write("-" * 50 + "\n")

                for student in self.students_data:
                    file.write(f"{student['name']:<20}\t{student['score']}\t{student['grade']}\n")

                file.write("-" * 50 + "\n")
                avg_score = sum(s['score'] for s in self.students_data) / len(self.students_data)
                file.write(f"\nAverage Score: {avg_score:.2f}\n")
                file.write(f"Total Students: {len(self.students_data)}\n")

            QMessageBox.information(
                self,
                "Export Successful",
                "Results exported to 'student_grades.txt'"
            )
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting results: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = StudentGradeApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
