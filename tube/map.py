class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances


    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be populated afresh with data from the JSON file. 
        Attribute values from previous imports should not be retained.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If the file does not exist, no attribute should be 
                populated and no error should be raised.

        Returns:
            None
        """
        import json
        from tube.components import Station, Line, Connection

        # Clear the previous imports 
        self.stations.clear()
        self.lines.clear()
        self.connections.clear()

        # Import data from "file.json"
        try:
            with open(filepath) as file:
             data = json.load(file)
        except FileNotFoundError:
            return


        def import_line(data):
            '''Creat Line instance based on data of lines, and put them into self.lines(dict)'''
            lines_list = data["lines"]
            for item in lines_list:
                self.lines[item["line"]] = Line(id=item["line"], name=item["name"])
            return self.lines
        
        self.lines = import_line(data)


        def trans_zone(zone):
            '''Transfer "zone" to the set form'''
            zone = float(zone)
            if zone.is_integer():
                return {int(zone)}
            else:
                return {int(zone), (int(zone) + 1)}


        def import_station(data):
            '''Creat Station insstance based on data of stations, \
                and put them into self.stations(dict)
            '''
            stations_list = data["stations"]
            for item in stations_list:
                self.stations[item["id"]] = Station(id=item["id"], 
                                                    name=item["name"], 
                                                    zones=trans_zone(item["zone"]))
            return self.stations
        
        self.stations = import_station(data)


        def import_connection(data):
            '''Creat connection insstance based on data of connections, \
                and put them into self.connections(list)
            '''
            connections_list = data["connections"]
            for item in connections_list:
                station1 = self.stations[item["station1"]]
                station2 = self.stations[item["station2"]]
                line = self.lines[item["line"]]
                self.connections.append(Connection(stations={station1, station2}, 
                                                   line=line, 
                                                   time=int(item["time"])))
            return self.connections
        
        self.connections = import_connection(data)

        return


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
