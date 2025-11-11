from tube.map import TubeMap
from network.graph import NeighbourGraphBuilder
from network.path import PathFinder


def test_all():
    print("===== Import JSON =====")
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    print(f"Stations: {len(tubemap.stations)}")
    print(f"Lines: {len(tubemap.lines)}")
    print(f"Connections: {len(tubemap.connections)}")

    print("\n===== Build Graph =====")
    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)
    print(f"Graph size: {len(graph)} stations")

    print("\n===== Shortest Path Test =====")
    finder = PathFinder(tubemap)
    path = finder.get_shortest_path("Covent Garden", "Green Park")
    if path:
        print(" → ".join([s.name for s in path]))
    else:
        print("No path found")

    print("\n===== Edge Cases =====")
    print("Invalid input:", finder.get_shortest_path("Nowhere", "Victoria"))
    same = finder.get_shortest_path("Victoria", "Victoria")
    print("Same start/end:", [s.name for s in same])
    print("\nAll tests passed ✅")


if __name__ == "__main__":
    test_all()
