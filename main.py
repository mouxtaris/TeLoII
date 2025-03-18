import dbConnect

trip = ['ibiza', 'den tha kanoume tipota', '2024-12-12', '2024-12-14', 500, 'polles']

dbConnect.crowdTrips(trip)

# trip_id` INT AUTO_INCREMENT PRIMARY KEY, `trip_name` VARCHAR(30) , `trip_desc` VARCHAR(300),"
#                    " `trip_start` DATE, `trip_end` DATE ,"
#                    " `trip_cost` INT(7), `trip_activities` VARCHAR(300))


