import mysql.connector

connection = mysql.connector.connect(
    host="sql7.freesqldatabase.com	",
    user="sql7767099	",
    passwd="cgpf79CiTP",
    database="sql7767099"
)

cursor = connection.cursor()
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

# def crowdTrips(trips):

cursor.execute("CREATE TABLE `sql7767099`.`trips` ( `trip_name` VARCHAR(30) , `trip_desc` VARCHAR(300),"
               " `trip_start` DATE, `trip_end` DATE ,"
               " `trip_cost` INT(7), `trip_activities` VARCHAR(300))",)
cursor.execute("CREATE TABLE `sql7767099`.`buses` (`model` VARCHAR(30), `bus_year` INT(7),`bus_km` INT(8), "
               "`service_cost` FLOAT(10,2), `service_time` INT(3), `operation_cost` FLOAT(10,2))")


