import sys
import mysql.connector
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton,
                             QMessageBox, QDateEdit, QFormLayout, QTabWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TransportManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transport Management System")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget and tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create Trips Tab
        self.trips_tab = QWidget()
        self.setup_trips_tab()
        self.tab_widget.addTab(self.trips_tab, "Trips")

        # Create Buses Tab
        self.buses_tab = QWidget()
        self.setup_buses_tab()
        self.tab_widget.addTab(self.buses_tab, "Buses")

        # Create tables if not exist
        self.create_tables()

    def setup_trips_tab(self):
        """Set up the trips tab layout"""
        trips_layout = QHBoxLayout()
        self.trips_tab.setLayout(trips_layout)

        # Left side - Trip Input Form
        input_widget = QWidget()
        input_layout = QFormLayout()
        input_widget.setLayout(input_layout)

        # Trip input fields
        self.trip_name_input = QLineEdit()
        self.trip_desc_input = QLineEdit()
        self.trip_start_input = QDateEdit()
        self.trip_start_input.setCalendarPopup(True)
        self.trip_end_input = QDateEdit()
        self.trip_end_input.setCalendarPopup(True)
        self.trip_cost_input = QLineEdit()
        self.trip_activities_input = QLineEdit()

        # Add input fields to layout
        input_layout.addRow("Trip Name:", self.trip_name_input)
        input_layout.addRow("Description:", self.trip_desc_input)
        input_layout.addRow("Start Date:", self.trip_start_input)
        input_layout.addRow("End Date:", self.trip_end_input)
        input_layout.addRow("Cost:", self.trip_cost_input)
        input_layout.addRow("Activities:", self.trip_activities_input)

        # Add Trip Button
        add_trip_btn = QPushButton("Add Trip")
        add_trip_btn.clicked.connect(self.add_trip)
        input_layout.addRow(add_trip_btn)

        #Add Export Button
        export_trip_btn = QPushButton("Export Trip")
        export_trip_btn.clicked.connect(self.export_trip)
        input_layout.addRow(export_trip_btn)

        # Right side - Trips Table
        self.trips_table = QTableWidget()
        self.trips_table.setColumnCount(7)
        self.trips_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Description", "Start Date", "End Date", "Cost", "Activities"]
        )
        self.trips_table.horizontalHeader().setStretchLastSection(True)

        # Layouts
        trips_layout.addWidget(input_widget, 1)
        trips_layout.addWidget(self.trips_table, 2)

    def setup_buses_tab(self):
        """Set up the buses tab layout"""
        buses_layout = QHBoxLayout()
        self.buses_tab.setLayout(buses_layout)

        # Left side - Bus Input Form
        input_widget = QWidget()
        input_layout = QFormLayout()
        input_widget.setLayout(input_layout)

        # Bus input fields
        self.bus_id_input = QLineEdit()
        self.bus_model_input = QLineEdit()
        self.bus_year_input = QLineEdit()
        self.bus_km_input = QLineEdit()
        self.service_cost_input = QLineEdit()
        self.service_time_input = QLineEdit()
        self.operation_cost_input = QLineEdit()

        # Add input fields to layout
        input_layout.addRow("Bus ID:", self.bus_id_input)
        input_layout.addRow("Model:", self.bus_model_input)
        input_layout.addRow("Year:", self.bus_year_input)
        input_layout.addRow("Kilometers:", self.bus_km_input)
        input_layout.addRow("Service Cost:", self.service_cost_input)
        input_layout.addRow("Service Time:", self.service_time_input)
        input_layout.addRow("Operation Cost:", self.operation_cost_input)

        # Add Bus Button
        add_bus_btn = QPushButton("Add Bus")
        add_bus_btn.clicked.connect(self.add_bus)
        input_layout.addRow(add_bus_btn)

        # Right side - Buses Table
        self.buses_table = QTableWidget()
        self.buses_table.setColumnCount(7)
        self.buses_table.setHorizontalHeaderLabels(
            ["Bus ID", "Model", "Year", "Kilometers", "Service Cost", "Service Time", "Operation Cost"]
        )
        self.buses_table.horizontalHeader().setStretchLastSection(True)

        # Layouts
        buses_layout.addWidget(input_widget, 1)
        buses_layout.addWidget(self.buses_table, 2)

    def get_database_connection(self):
        """Establish database connection"""
        try:
            connection = mysql.connector.connect(
                host="sql7.freesqldatabase.com",
                user="sql7767099",
                passwd="cgpf79CiTP",
                database="sql7767099"
            )
            return connection
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not connect to database: {str(e)}")
            return None

    def create_tables(self):
        """Create tables if they don't exist"""
        connection = self.get_database_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            # Create trips table if not exists
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                trip_id INT AUTO_INCREMENT PRIMARY KEY,
                trip_name VARCHAR(30),
                trip_desc VARCHAR(300),
                trip_start DATE,
                trip_end DATE,
                trip_cost INT(7),
                trip_activities VARCHAR(300)
            )
            """)

            # Create buses table if not exists
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS buses (
                bus_id VARCHAR(8) PRIMARY KEY,
                model VARCHAR(30),
                bus_year INT(7),
                bus_km INT(8),
                service_cost FLOAT(10,2),
                service_time INT(3),
                operation_cost FLOAT(10,2)
            )
            """)

            connection.commit()
            cursor.close()
            connection.close()

            # Load initial data
            self.load_trips()
            self.load_buses()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Table Creation Error", f"Could not create tables: {str(e)}")

    def load_trips(self):
        """Load trips from database into table"""
        connection = self.get_database_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM trips")
            trips = cursor.fetchall()

            # Clear existing table rows
            self.trips_table.setRowCount(0)

            # Populate table
            for row_num, trip in enumerate(trips):
                self.trips_table.insertRow(row_num)
                for col_num, value in enumerate(trip):
                    # Convert date objects to string
                    if isinstance(value, (QDate, datetime.date)):
                        value = value.strftime("%d-%m-%Y")

                    item = QTableWidgetItem(str(value))
                    self.trips_table.setItem(row_num, col_num, item)

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Could not load trips: {str(e)}")

    def load_buses(self):
        """Load buses from database into table"""
        connection = self.get_database_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM buses")
            buses = cursor.fetchall()

            # Clear existing table rows
            self.buses_table.setRowCount(0)

            # Populate table
            for row_num, bus in enumerate(buses):
                self.buses_table.insertRow(row_num)
                for col_num, value in enumerate(bus):
                    item = QTableWidgetItem(str(value))
                    self.buses_table.setItem(row_num, col_num, item)

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Could not load buses: {str(e)}")

    def add_trip(self):
        """Add a new trip to the database"""
        # Validate inputs
        name = self.trip_name_input.text()
        desc = self.trip_desc_input.text()
        start_date = self.trip_start_input.date().toString("yyyy-MM-dd")
        end_date = self.trip_end_input.date().toString("yyyy-MM-dd")

        try:
            cost = int(self.trip_cost_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Cost must be a number")
            return

        activities = self.trip_activities_input.text()

        # Validate required fields
        if not all([name, desc, start_date, end_date, activities]):
            QMessageBox.warning(self, "Missing Information", "Please fill all fields")
            return

        connection = self.get_database_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """INSERT INTO trips 
                       (trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (name, desc, start_date, end_date, cost, activities)

            cursor.execute(query, values)
            connection.commit()

            # Clear input fields
            self.trip_name_input.clear()
            self.trip_desc_input.clear()
            self.trip_cost_input.clear()
            self.trip_activities_input.clear()

            # Reload trips
            self.load_trips()

            QMessageBox.information(self, "Success", "Trip added successfully!")

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not add trip: {str(e)}")

    def add_bus(self):
        """Add a new bus to the database"""
        # Validate inputs
        bus_id = self.bus_id_input.text()
        model = self.bus_model_input.text()

        try:
            bus_year = int(self.bus_year_input.text())
            bus_km = int(self.bus_km_input.text())
            service_cost = float(self.service_cost_input.text())
            service_time = int(self.service_time_input.text())
            operation_cost = float(self.operation_cost_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers")
            return

        # Validate required fields
        if not all([bus_id, model]):
            QMessageBox.warning(self, "Missing Information", "Please fill all fields")
            return

        connection = self.get_database_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """INSERT INTO buses 
                       (bus_id, model, bus_year, bus_km, service_cost, service_time, operation_cost) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (bus_id, model, bus_year, bus_km, service_cost, service_time, operation_cost)

            cursor.execute(query, values)
            connection.commit()

            # Clear input fields
            self.bus_id_input.clear()
            self.bus_model_input.clear()
            self.bus_year_input.clear()
            self.bus_km_input.clear()
            self.service_cost_input.clear()
            self.service_time_input.clear()
            self.operation_cost_input.clear()

            # Reload buses
            self.load_buses()

            QMessageBox.information(self, "Success", "Bus added successfully!")

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not add bus: {str(e)}")

    def export_trip(self):
        #Ελέγχει αν έχει επιλεχθεί κάποιο Trip
            selected_row = self.trips_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "No Selection", "Please select a trip to export.")
                return

            trip_data = []
            headers = ["Name", "Description", "Start Date", "End Date", "Cost", "Activities"]

            for col in range(self.trips_table.columnCount()):
                item = self.trips_table.item(selected_row, col)
                trip_data.append(item.text() if item else "")
            #Αποθήκευσει pdf
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Trip", "", "PDF Files (*.pdf);;All Files (*)",
                                                       options=options)
            #Δημιουργεί το PDF
            if file_path:
                try:
                    c = canvas.Canvas(file_path, pagesize=letter)
                    c.setFont("Helvetica", 12)
                    c.drawString(100, 750, "Trip Export")
                    c.line(100, 745, 500, 745)  # Διαχωριστική γραμμή

                    y_position = 720
                    for header, value in zip(headers, trip_data):
                        c.drawString(100, y_position, f"{header}: {value}")
                        y_position -= 20  # Μετακίνηση προς τα κάτω

                    c.save()
                    QMessageBox.information(self, "Export Successful", f"Trip exported to {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Export Failed", f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TransportManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()