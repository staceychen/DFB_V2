import csv

class Coordinates:
    
    def __init__(self):
        with open('location_data/merged_coordinates.csv', encoding = 'utf-8') as coordinate_data:
            reader = csv.DictReader(coordinate_data, delimiter = ',')
            
            self.coors_dict = {}
            for row in reader:
                airport = str(row['Airport Code'])
                coordinates = (float(row['Lat']), float(row['Lng']))
                self.coors_dict[airport] = coordinates
                
    def get_dictionary(self):
        return self.coors_dict
                