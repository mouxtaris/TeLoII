import mysql.connector

connection = mysql.connector.connect(
    host="sql7.freesqldatabase.com	",
    user="sql7767099	",
    passwd="cgpf79CiTP",
    database="sql7767099"
)
cursor = connection.cursor()
# cursor.close()

def dropTables():
    cursor.execute("DROP TABLE IF EXISTS buses, trips, bus_drivers, schedules")

# cursor.execute("CREATE TABLE `sql7767099`.`trips` ( `trip_name` VARCHAR(30) , `trip_desc` VARCHAR(300),"
#                " `trip_start` DATE, `trip_end` DATE , `trip_hotel` VARCHAR(20) ,"
#                " `trip_cost` INT(7), `trip_activities` VARCHAR(300))")

# cursor.execute("INSERT INTO `trips` (`trip_name`, `trip_desc`, `trip_start`, `trip_end`, `trip_hotel`, "
#                "`trip_cost`, `trip_activities`)"
#                " VALUES ('ibiza','nothing','2024/12/14', '2024/12/20', 'markiz', 500, 'polla')")
# connection.commit()

# cursor.execute("UPDATE `trips` SET `date` = DATE(`date`, '%d-%m-%Y')")

# cursor.execute("DELETE FROM trips WHERE trip_start = '0000-00-00'")
# connection.commit()

# print(cursor.fetchall())
# cursor.execute("DROP TABLE IF EXISTS trips")

# cursor.execute("ALTER TABLE `sql7767099`.`buses` ADD bus_id VARCHAR(7) FIRST")

# def crowdTrips(trips):
# connection.commit()
# def showTables():
#     cursor.execute("SHOW TABLES")
#     print(cursor.fetchall())


def createTables():
    # cursor.execute("CREATE TABLE `sql7767099`.`trips` (`trip_id` INT AUTO_INCREMENT PRIMARY KEY, `trip_name` VARCHAR(30) , `trip_desc` VARCHAR(300),"
    #                " `trip_start` DATE, `trip_end` DATE ,"
    #                " `trip_cost` INT(7), `trip_activities` VARCHAR(300))")
    # cursor.execute("CREATE TABLE `sql7767099`.`buses` (`bus_id` VARCHAR(8) PRIMARY KEY ,`model` VARCHAR(30), `bus_year` INT(7),`bus_km` INT(8), "
    #     "`service_cost` FLOAT(10,2), `service_time` INT(3), `operation_cost` FLOAT(10,2))")
    # cursor.execute(
    #     "CREATE TABLE `sql7767099`.`bus_drivers` (`driver_id` INT AUTO_INCREMENT PRIMARY KEY, `driver_name` VARCHAR(25), `driver_lname` VARCHAR(25),"
    #     " `availability` BOOLEAN, `driver_salary` FLOAT(8,2), `cost_perTrip` FLOAT(8,2),"
    #      "`driver_hours` FLOAT(5,1),`favoured_destinations` VARCHAR(10))")

    cursor.execute(
        "CREATE TABLE `sql7767099`.`trip_leaders` (`leader_id` INT(8) AUTO_INCREMENT PRIMARY KEY, `leader_name` VARCHAR(25), `leader_lname` VARCHAR(25),"
        " `experience` VARCHAR(100), `fav_destinations` VARCHAR(100), `availability` BOOLEAN,"
         "`cost_perTrip` FLOAT(8,2),`bonus` INT(10))")

    cursor.execute(
        "CREATE TABLE `sql7767099`.`employees` (`emp_id` INT AUTO_INCREMENT PRIMARY KEY, `emp_name` VARCHAR(25), `emp_lname` VARCHAR(25),"
        " `working_hours` FLOAT(8,2), `salary` FLOAT(8,2))")



# function to insert data into trips table
def crowdTrips(trip_values):
    query = """INSERT INTO `sql7767099`.`trips` 
                   (`trip_name`, `trip_desc`, `trip_start`, `trip_end`, `trip_cost`, `trip_activities`) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, trip_values)
    connection.commit()
    cursor.close()
    connection.close()

#show all data from trips table
def showTrips():
    query = """SELECT * FROM `sql7767099`.`trips`"""
    cursor.execute(query)
    trips = cursor.fetchall()
    for trip in trips:
        # Unpack trip values
        trip_id, trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities = trip

        # Format the dates as dd-mm-yyyy
        trip_start = trip_start.strftime("%d-%m-%Y")
        trip_end = trip_end.strftime("%d-%m-%Y")

        #create an array of trips


        # Print the formatted output
        print((trip_id, trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities))

    trips = []
    for trip in cursor.fetchall():
        trip_id, trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities = trip
        # Format dates to dd-mm-yyyy
        trip_start = trip_start.strftime("%d-%m-%Y")
        trip_end = trip_end.strftime("%d-%m-%Y")
        trips.append({
            "trip_id": trip_id,
            "trip_name": trip_name,
            "trip_desc": trip_desc,
            "trip_start": trip_start,
            "trip_end": trip_end,
            "trip_cost": trip_cost,
            "trip_activities": trip_activities
        })

    cursor.close()
    connection.close()


#display a single trip according to the trip_id
def displayTrip(trip_id):
    query = """SELECT * FROM `sql7767099`.`trips` WHERE trip_id = %s"""
    cursor.execute(query, (trip_id,))
    trip = cursor.fetchone()

    if trip:
        # Unpack the tuple
        trip_id, trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities = trip

        # Convert dates to dd-mm-yyyy format
        trip_start = trip_start.strftime("%d-%m-%Y")
        trip_end = trip_end.strftime("%d-%m-%Y")

        # Print formatted output
        print((trip_id, trip_name, trip_desc, trip_start, trip_end, trip_cost, trip_activities))
    else:
        print("Trip not found.")

    cursor.close()
    connection.close()




# function to insert data into buses table
def crowdBuses(bus_values):
    query = """INSERT INTO `sql7767099`.`buses` (bus_id, model, bus_year, bus_km, service_cost, service_time, operation_cost)
     VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, bus_values)
    connection.commit()
    cursor.close()
    connection.close()

def showBuses():
    query = """SELECT * FROM `sql7767099`.`buses`"""
    cursor.execute(query)
    buses = cursor.fetchall()
    for bus in buses:
        print(bus)

    busesArray = []
    cursor.execute("SELECT * FROM `buses`")
    for bus in cursor.fetchall():
        bus_id, model, bus_year, bus_km, service_cost, service_time, operation_cost = bus

        busesArray.append({
            "bus_id": bus_id,
            "model": model,
            "bus_year": bus_year,
            "bus_km": bus_km,
            "service_cost": service_cost,
            "service_time": service_time,
            "operation_cost": operation_cost
        })

        print(busesArray)

        cursor.close()
        connection.close()

def displayBus(bus_id):
    query = """SELECT * FROM `sql7767099`.`buses` WHERE bus_id = %s"""
    cursor.execute(query, (bus_id,))
    bus = cursor.fetchone()

    if bus:
        print(bus)
    else:
        print("Bus not found.")

    cursor.close()
    connection.close()

def crowdBusDrivers(busDriver_values):
    query = """INSERT INTO `sql7767099`.`bus_drivers` (driver_id, driver_name, driver_lname, availability, driver_salary,
     costperTrip, driver_hours, favoured_destinations)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, busDriver_values)
    connection.commit()
    cursor.close()
    connection.close()

def showBusDrivers():
    query = """SELECT * FROM `sql7767099`.`bus_drivers`"""
    cursor.execute(query)
    drivers = cursor.fetchall()
    for driver in drivers:
        print(driver)

    driversArray = []
    cursor.execute("SELECT * FROM `sql7767099`.`bus_drivers`")
    for driver in drivers:
        busDrivers = driver_id, driver_name, driver_lname, availability, driver_salary, costperTrip,
         driver_hours, favoured_destinations

        driversArray.append({
            "driver_id": driver_id,
            "driver_name": driver_name,
            "driver_lname": driver_lname,
            "availability": availability,
            "costperTrip" : costperTrip,
            "driver_salary": driver_salary,
            "driver_hours": driver_hours,
            "favoured_destinations": favoured_destinations
        })

        print(driversArray)

        cursor.close()
        connection.close()







