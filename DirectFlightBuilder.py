import airport
import airport_set
import csv
import coordinates
import formulas


#create the global variable
organized_set = airport_set.Airport_Set()
iata_seen = set()
coordinates_dict = coordinates.Coordinates().get_dictionary()

def new_file():
    #write the header
    with open('outputs/flights.csv', 'w', newline="\n", encoding='utf-8-sig') as out_file:
        csv_writer = csv.writer(out_file, delimiter=',')
        header = ["location a name", "location b name", "location a radius", "location b radius", "location a airports", "location b airports", 
                  "flights", "location a coordinates", "location b coordinates"]
        for year in range(1990, 2019):
            for month in range(1, 13):
                date = int(str(year) + str(month))
                
                #data ends in August, 2018
                if date > 20188:
                    break
                header.append(str(date))
            

        csv_writer.writerow(header)
        
    #create the airport set
    global organized_set
    print("initializing dictionary of airport coordinates")
    global coordinates_dict
    print("number of total airports in dictionary: " + str(len(coordinates_dict)))
    print()

        

def pre_processing(i):
    global coordinates_dict
    global organized_set           
    global iata_seen 
    
    #start with the earliest flight data - parse through it
    
    name_d = str(i) + "_D"
    name_i = str(i) + "_I"
    

    with open('flight_data/' + name_d + '.csv', encoding='utf-8-sig') as dom_data:
        with open('flight_data/' + name_i + '.csv', encoding='utf-8-sig') as int_data:
            csv_reader_d = csv.DictReader(dom_data, delimiter=',')
            csv_reader_i = csv.DictReader(int_data, delimiter=',')
            for row in csv_reader_d:
                airport_iata = str(row['ORIGIN'])
                iata_seen.add(airport_iata)
                

                city = str(row['ORIGIN_CITY_NAME'])
                date = int(str(i) + row['MONTH'])
                

                dest = str(row['DEST'])
                ap = organized_set.locate_airport(airport_iata)
                
                
                #check if a given airport has been seen
                if not ap is None:
                    ap.set_flight(date, dest)
                else:
                    flights = {}
                    new_ap = airport.Airport(airport_iata, flights, city, coordinates_dict)
                    new_ap.set_flight(date, dest)
                    organized_set.place_airport(new_ap)
                

            for row in csv_reader_i:
                airport_iata = str(row['ORIGIN'])
                iata_seen.add(airport_iata)
                

                city = str(row['ORIGIN_CITY_NAME'])
                date = int(str(i) + row['MONTH'])
            

                dest = str(row['DEST'])
                ap = organized_set.locate_airport(airport_iata)
                

                #check if a given airport has been seen
                if not ap is None:
                    ap.set_flight(date, dest)
                else:
                    flights = {}
                    new_ap = airport.Airport(airport_iata, flights, city, coordinates_dict)
                    new_ap.set_flight(date, dest)
                    organized_set.place_airport(new_ap)
                    

def process_input_file(filename):
    print("processing "+filename)
    # open csv input
    with open('inputs/inputquery/'+filename, encoding = 'utf-8-sig') as input_data:
        csv_reader = csv.DictReader(input_data, delimiter=',')
        for row in csv_reader:
            # parse csv
            a = str(row['a'])
            b = str(row['b'])
            a_radius = int(row['a_radius'])
            b_radius = int(row['b_radius'])
            a_lat = float(row['a_lat'])
            a_lng = float(row['a_lng'])
            b_lat = float(row['b_lat'])
            b_lng = float(row['b_lng'])
            
            # call direct_flight_builder
            direct_flight_builder(a, (a_lat, a_lng), a_radius, b, (b_lat, b_lng), b_radius)
            
        

def direct_flight_builder(loc_a, coord_a, radius_a, loc_b, coord_b, radius_b):
    (lat1, lon1) = coord_a
    (lat2, lon2) = coord_b
    
    #ONLY DO THIS CALCULATION IF THE TWO LOCATIONS ARE MORE THAN N KM APART
    MINIMUM_DISTANCE = 100
    if formulas.haversine(lat1, lon1, lat2, lon2) < MINIMUM_DISTANCE:
        return
        
    
    # prepare the csv output
    with open('outputs/flights.csv', 'a', newline="\n", encoding='utf-8-sig') as out_file:
        # search through set of airports to get the set of airports within the radius for each location
        loc_a_airports = organized_set.get_subset(coord_a, radius_a)
        loc_b_airports = organized_set.get_subset(coord_b, radius_b)
        

        airports_a_list = []
        for close_airport in loc_a_airports:
            airports_a_list.append(str(close_airport.iata))
            

        airports_b_list = []
        for close_airport in loc_b_airports:
            airports_b_list.append(str(close_airport.iata))
        

        csv_writer = csv.writer(out_file, delimiter=',')
        

        #write the first several values
        date_list = [loc_a, loc_b, str(radius_a), str(radius_b), '; '.join(airports_a_list), '; '.join(airports_b_list), str(coord_a), str(coord_b)]
        

        #keep track of the flights themselves
        direct_flights_set = set()
        

        for year in range(1990, 2019):
            for month in range(1, 13):
                num_of_flights = 0
                date = int(str(year) + str(month))
                

                #data ends in August, 2018
                if date > 20188:
                    break
                    

                # check if there is a flight from some airport in a to some airport in b
                for airport_a in loc_a_airports:
                    for airport_b in loc_b_airports:
                        if (airport_a.has_flight(date, airport_b)):
                            num_of_flights += 1     
                            direct_flights_set.add(str(airport_a.iata) + "-" + str(airport_b.iata))
                date_list.append(str(num_of_flights))  
        date_list.insert(6, '; '.join(direct_flights_set))       
        csv_writer.writerow(date_list)
        


if __name__ == '__main__':
    pre_processing()
    

            

    direct_flight_builder("penn station, ny", (40.7506, -73.9935), 100, "london eye", (51.5033, -0.1195), 100)
    direct_flight_builder("sears tower, chicago", (41.8789, -87.6359), 100, "the louvre", (48.8606, 2.3376), 100)
    direct_flight_builder("hollywood sign, la", (34.1341, -118.3215), 100, "hong kong victoria harbour", (22.2795, 114.1648), 100)
    direct_flight_builder("golden gate bridge, sf", (37.8199, -122.4783), 100, "shanghai pearl tower", (31.2397, 121.4998), 100)
    direct_flight_builder("empire state building", (40.7484, -73.9857), 100, "cristo redentor, rio de janeiro", (-22.9519, -43.2105), 100)