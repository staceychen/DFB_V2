import airport
import formulas

class Airport_Set:
    #constructor will only initialize all 72 airport sets
    def __init__(self):
        #organized in 6 x 12 grid according to this diagram http://www.satsig.net/world105.gif
        #total of 72 sets - with names following the position of a matrix - upper left corner is 1,1
        self.sets = {}
        self.airports = {}
        
        for i in range(72):
            row = int(i / 12) + 1
            column = (i % 12) + 1
            
            key = self.__get_key(row, column)
            
            self.sets[key] = set()
            
            
    #this method will place a airport into the correct set - input MUST be an airport
    def place_airport(self, port):
        #check that the input is an instance of an airport
        if not isinstance(port, airport.Airport):
            raise ValueError("the input to place_airport must be an airport")
        
        (row, column) = self.__get_row_and_column(port.coordinates)
        key = self.__get_key(row, column)
        
        #add the port to the corresponding airport set
        self.sets[key].add(port)
        
        self.airports[port.iata] = port
        
            
    #this helper method determines the row and column of the set given coordinates
    def __get_row_and_column(self, coordinates):
        (lat, lng) = coordinates
        
        row = 0
        if lat > 60:
            row = 1
        elif lat > 30:
            row = 2
        elif lat > 0:
            row = 3
        elif lat > -30:
            row = 4
        elif lat > -60:
            row = 5
        else:
            row = 6
            
        column = 0
        if lng < -150:
            column = 1
        elif lng < -120:
            column = 2
        elif lng < -90:
            column = 3
        elif lng < -60:
            column = 4
        elif lng < -30:
            column = 5
        elif lng < -0:
            column = 6
        elif lng < 30:
            column = 7
        elif lng < 60:
            column = 8
        elif lng < 90:
            column = 9
        elif lng < 120:
            column = 10
        elif lng < 150:
            column = 11
        else:
            column = 12
            
        return (row, column)
    
    
    #this helper method will return the key to get the corresponding set given row and column
    def __get_key(self, row, column):
        return "area_" + str(row) + "_" + str(column)
    
    
    #this method will get the airport set that contains the given coordinates. If the coordinates 
    #and the radius encompasses multiple sets, then the union of the relevant sets will be returned
    #coordinates are an integer tuple, radius is a integer
    
    def get_subset(self, coordinates, radius):
        (lat, lng) = coordinates
        
        #check that the coordinates exist
        if (abs(lat) > 90 or abs(lng > 180)):
            raise ValueError("get_subset: the coordinates are invalid")
        
        #determine the row and column associated with the coordinates
        (row, column) = self.__get_row_and_column(coordinates)
        key = self.__get_key(row, column)
        
        #create the set of airports - give it the airports in the same box as coordinate
        close_airports = self.sets[key]
        
        #the formula assumes units in kilometers!
        dlat = formulas.change_in_latitude(radius)
        
        #check the corners of the radius bounding box
        latHigh = lat + dlat
        latLow = lat - dlat
        
        dlngHigh = formulas.change_in_longitude(latHigh, radius)
        dlngLow = formulas.change_in_longitude(latLow, radius)
        
        (row_u_l, column_u_l) = self.__get_row_and_column((latHigh, lng - dlngHigh))
        (row_l_r, column_l_r) = self.__get_row_and_column((latLow, lng + dlngLow))
        
        # union all airports encompassed by bounding box - from upper left corner to lower right
        drow = row_l_r - row_u_l
        dcolumn = column_l_r - column_u_l
        
        for i in range(drow + 1):
            for j in range(dcolumn + 1):
                temp_key = self.__get_key(row_u_l + i, column_u_l + j)
                close_airports.update(self.sets[temp_key])
        
        # the actual set of airports within the radius
        airportSet = set()
        
        for airport in close_airports:
            airportCoord = airport.coordinates
            dist = formulas.haversine(coordinates[0], coordinates[1], airportCoord[0], airportCoord[1])
            if dist <= radius:
                airportSet.add(airport)
            
        return airportSet
    
    
        
    #returns the airport with the iata code provided
    def locate_airport(self, iataCode):
        if iataCode in self.airports:
            return self.airports[iataCode]
        else:
            return None
    
    #returns the grid coordinates of a provided airport, if not found, returns "not found"
    def get_grid_coor(self, iataCode):
        for key, airports in self.sets.items():
                for airport in airports:
                    if airport.iata == iataCode:
                        return key
        return "not found"
            
    