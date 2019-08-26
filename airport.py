import requests
import csv
import json

class Airport:
    cnt = 0
    
    #constructor - make city default if not passed in
    def __init__(self, iata, flights, city = "", coordinates_dict = None):
        Airport.cnt += 1
        self.iata = iata
        self.flights = {}
        
        try:
            (lat, lng) = coordinates_dict[iata] 
            self.coordinates = (lat, lng)
            self.flights = flights
        except KeyError: 
            try:
                print("WARNING: Couldn't find " + str(iata) + " in the coordinates dictionary. Searching online with Bing...")
                response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + str(iata) +
                                    " Airport" + str(city) + "?",
                                    params={"include":"queryParse",
                                    "key":"AgUSM867a3r-7GFqCUQ81nvWLngFtrbanaBzA41qVEDoN-PFSEQiCTtx0eY9aJ--"})
            
                data = response.json()
                lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                
                #save it to the csv file and add it to the dictionary
                with open('location_data/merged_coordinates.csv', 'a', newline="\n", encoding='utf-8') as airport_coord:               
                    csv_writer = csv.writer(airport_coord, delimiter=',')
                    csv_writer.writerow([self.iata, city, lat, lng])
                
                coordinates_dict[self.iata] = (lat, lng)
                
                self.coordinates = (lat, lng)
                self.flights = flights
                
                
            except (json.decoder.JSONDecodeError, IndexError):
                try:
                    print("WARNING: Couldn't find " + str(iata) + " on Bing. Searching again without city information...")
                    #stacey's api key
                    response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + str(iata) + " Airport""?",
                                            params={"include":"queryParse",
                                            "key":"AgUSM867a3r-7GFqCUQ81nvWLngFtrbanaBzA41qVEDoN-PFSEQiCTtx0eY9aJ--"})
                    
                    data = response.json()
                    lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                    lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                    
                    #save it to the csv file and add it to the dictionary
                    with open('location_data/merged_coordinates.csv', 'a', newline="\n", encoding='utf-8') as airport_coord:               
                        csv_writer = csv.writer(airport_coord, delimiter=',')
                        csv_writer.writerow([self.iata, city, lat, lng])
                
                    coordinates_dict[self.iata] = (lat, lng)
                    
                    self.coordinates = (lat, lng)
                    self.flights = flights
                    
                    
                except:
                    raise ValueError("there was a problem getting the coordinate data of: " + str(iata) + " in " + str(city))

    #***METHODS***
    
    #set flight throws an exception if the given date is invalid
    def set_flight(self, date, airport):
        # return false if the date is invalid
        if not(len(str(date)) == 5 or len(str(date)) == 6) or (len(str(date)) == 6 and
                                                               int(str(date)[5]) > 2):
            raise ValueError("invalid date format - must be in the format YEARMONTH")
        
            
        #create new key if the date isn't here yet, otherwise add to the existing date set
        if date in self.flights:
            self.flights[date].add(airport)
        else:
            self.flights[date] = set()
            self.flights[date].add(airport)
        
    #has flight method returns true if there is a flight from this airport to the other airport
    #for the given date
    #note that airport is an airport object for the other airport
    def has_flight(self, date, other_airport):
        # return false if the date is invalid
        if not(len(str(date)) == 5 or len(str(date)) == 6) or (len(str(date)) == 6 and
                                                               int(str(date)[5]) > 2):
            raise ValueError("invalid date format - must be in the format YEARMONTH")
        
        #check to make sure that the date exists in airport flights
        if not date in self.flights:
            return False
        
        for destination in self.flights[date]:
            if other_airport.iata == destination:
                return True
            
        return False
    
    #equals method returns true if the other object is an airport with the same iata code
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.iata == other.iata
        else:
            return False
        
    #hash method to be able to use the airport object in sets - hash code will just be id and iata
    def __hash__(self):
        return hash(self.iata)