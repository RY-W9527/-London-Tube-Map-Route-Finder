from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
        # Feel free to add anything else needed here.
        
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use Dijkstra's algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: 
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        def get_station_by_name(tubemap, name):
            """Return the Station instance matching a given station name.
            Args:
                tubemap (TubeMap): map of the tube based on data(.json)
                name (str): name of the station
            Returns:
                station (Station)"""
            for station in tubemap.stations.values():
                if station.name == name: 
                    return station
            return None
        
        start_station = get_station_by_name(self.tubemap, start_station_name)
        end_station = get_station_by_name(self.tubemap, end_station_name)


        # Check if start_station_name or end_station_name does not exist.
        if not start_station or not end_station:
            return None

        # Check if start_station_name and end_station_name are the same.
        if start_station_name == end_station_name:
            return [start_station]
        
        # Dijkstras algorithm
        # Perform the initial setup for Dijkstra's algorithm
        time = {station_id: float("inf") for station_id in self.tubemap.stations}
        pre_station = {station_id: None for station_id in self.tubemap.stations}
        unvisited = set(self.tubemap.stations.keys())
        time[start_station.id] = 0

        # Main loop of Dijkstra's algorithm: update shortest paths iteratively
        while unvisited:
            point = min(unvisited, key=lambda station_id:time[station_id])
            unvisited.remove(point)

            # Break the loop when it reach the end_station.
            if point == end_station.id:
                break

            for neighbour_station_id, connections in self.graph[point].items():
                alt = time[point] + min(connection.time for connection in connections)
                if alt < time[neighbour_station_id]:
                    time[neighbour_station_id] = alt
                    pre_station[neighbour_station_id] = point
        
        # Reconstruct the path(list of station.id)
        shortest_path_id = []
        path_point = end_station.id
        while path_point is not None:
            shortest_path_id.append(path_point)
            path_point = pre_station[path_point]
        shortest_path_id.reverse()
        
        # Convert the list of station.id into Station instances
        shortest_path = []
        for id in shortest_path_id:
            shortest_path.append(self.tubemap.stations[id])
        
        return shortest_path


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
   
    assert stations is not None

    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
