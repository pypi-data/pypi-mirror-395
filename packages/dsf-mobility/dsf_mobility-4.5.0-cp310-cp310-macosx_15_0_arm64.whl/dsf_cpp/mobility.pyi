"""
Bindings for mobility-related classes and functions, under the dsf::mobility C++ namespace.
"""
from __future__ import annotations
import collections.abc
import dsf_cpp
import typing
__all__: list[str] = ['DOUBLE_TAIL', 'Dynamics', 'Itinerary', 'LENGTH', 'PathCollection', 'PathWeight', 'RoadNetwork', 'SINGLE_TAIL', 'TRAVELTIME', 'TrafficLightOptimization', 'WEIGHT']
class Dynamics:
    def __init__(self, graph: RoadNetwork, useCache: bool = False, seed: typing.SupportsInt | None = None, alpha: typing.SupportsFloat = 0.0, weightFunction: PathWeight = ..., weightThreshold: typing.SupportsFloat | None = None) -> None:
        """
        Description
        Construct a new First Order
        
        Args
          RoadNetwork graph: The graph representing the network 
          bool useCache: If true, the cache is used (default is false) 
          std::optional< unsigned int > seed: The seed for the random number generator (default is std::nullopt) 
          double alpha: The minimum speed rate (default is 0) 
          PathWeight const weightFunction: The dsf::PathWeight function to use for the pathfinding (default is dsf::PathWeight::TRAVELTIME) 
          std::optional< double > weightTreshold: The weight threshold for the pathfinding (default is std::nullopt) 
        
        Returns
          void: No return value
        """
    @typing.overload
    def addAgentsRandomly(self, nAgents: typing.SupportsInt) -> None:
        """
        Description
        No description available.
        
        Args
          Size nAgents: No description
        
        Returns
          void: No description
        """
    @typing.overload
    def addAgentsRandomly(self, nAgents: typing.SupportsInt, src_weights: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat], dst_weights: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat]) -> None:
        """
        Description
        No description available.
        
        Args
          Size nAgents: No description
        
        Returns
          void: No description
        """
    def addAgentsUniformly(self, nAgents: typing.SupportsInt, itineraryId: typing.SupportsInt | None = None) -> None:
        """
        Description
        Add agents uniformly on the road network.
        
        Args
          Size nAgents: The number of agents to add 
          std::optional< Id > itineraryId: The id of the itinerary to use (default is std::nullopt) 
        
        Returns
          void: No description
        """
    @typing.overload
    def addRandomAgents(self, nAgents: typing.SupportsInt) -> None:
        """
        Description
        No description available.
        
        Args
          std::size_t nAgents: No description
        
        Returns
          void: No description
        """
    @typing.overload
    def addRandomAgents(self, nAgents: typing.SupportsInt, src_weights: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat]) -> None:
        """
        Description
        No description available.
        
        Args
          std::size_t nAgents: No description
        
        Returns
          void: No description
        """
    def datetime(self) -> str:
        """
        Description
        Get the current simulation time as formatted string (YYYY-MM-DD HH:MM:SS).
        
        Args
          None
        
        Returns
          auto: std::string, The current simulation time as formatted string 
        """
    def evolve(self, reinsert_agents: bool = False) -> None:
        """
        Description
        Evolve the simulation. 
        Evolve the simulation by moving the agents and updating the travel times. In particular:
        
        Args
          bool reinsert_agents: If true, the agents are reinserted in the simulation after they reach their destination 
        
        Returns
          void: No description
        """
    def graph(self) -> RoadNetwork:
        """
        Description
        Get the graph.
        
        Args
          None
        
        Returns
          const auto &: const network_t&, The graph 
        """
    def initTurnCounts(self) -> None:
        """
        Description
        Initialize the turn counts map.
        
        Args
          None
        
        Returns
          void: No description
        """
    def killStagnantAgents(self, timeToleranceFactor: typing.SupportsFloat = 3.0) -> None:
        """
        Description
        Set the time tolerance factor for killing stagnant agents. An agent will be considered stagnant if it has not moved for timeToleranceFactor * std::ceil(street_length / street_maxSpeed) time units.
        
        Args
          double timeToleranceFactor: The time tolerance factor 
        
        Returns
          void: No description
        """
    def meanTravelDistance(self, clearData: bool = False) -> dsf_cpp.Measurement:
        """
        Description
        Get the mean travel distance of the agents in
        
        Args
          bool clearData: If true, the travel distances are cleared after the computation 
        
        Returns
          Measurement: No description
        """
    def meanTravelSpeed(self, clearData: bool = False) -> dsf_cpp.Measurement:
        """
        Description
        Get the mean travel speed of the agents in
        
        Args
          bool clearData: If true, the travel times and distances are cleared after the computation 
        
        Returns
          Measurement: No description
        """
    def meanTravelTime(self, clearData: bool = False) -> dsf_cpp.Measurement:
        """
        Description
        Get the mean travel time of the agents in
        
        Args
          bool clearData: If true, the travel times are cleared after the computation 
        
        Returns
          Measurement: No description
        """
    def nAgents(self) -> int:
        """
        Description
        Get the number of agents currently in the simulation.
        
        Args
          None
        
        Returns
          Size: Size The number of agents 
        """
    def normalizedTurnCounts(self) -> dict:
        """
        Description
        Get the normalized turn counts of the agents.
        
        Args
          None
        
        Returns
          std::unordered_map< Id, std::unordered_map< Id, double > > const: const std::unordered_map<Id, std::unordered_map<Id, double>>& The normalized turn counts. The outer map's key is the street id, the inner map's key is the next street id and the value is the normalized number of counts 
        """
    def optimizeTrafficLights(self, optimizationType: TrafficLightOptimization = dsf_cpp.TrafficLightOptimization.DOUBLE_TAIL, logFile: str = '', threshold: typing.SupportsFloat = 0.0, ratio: typing.SupportsFloat = 1.3) -> None:
        """
        Description
        Optimize the traffic lights by changing the green and red times.
        
        Args
          TrafficLightOptimization optimizationType: TrafficLightOptimization, The type of optimization. Default is DOUBLE_TAIL 
          const std::string & logFile: The file into which write the logs (default is empty, meaning no logging) 
          double const percentage: double, the maximum amount (percentage) of the green time to change (default is 0.3) 
          double const threshold: double, The ratio between the self-density and neighbour density to trigger the non-local optimization (default is 1.3)
        
        Returns
          void: No description
        """
    def saveCoilCounts(self, filename: str, reset: bool = False, separator: str = ';') -> None:
        """
        Description
        Save the street input counts in csv format.
        
        Args
          const std::string & filename: The name of the file 
          bool reset: If true, the input counts are cleared after the computation
          char const separator: No description
        
        Returns
          void: No description
        """
    def saveMacroscopicObservables(self, filename: str, separator: str = ';') -> None:
        """
        Description
        Save the main macroscopic observables in csv format.
        
        Args
          std::string filename: The name of the file (default is "{datetime}_{simulation_name}_macroscopic_observables.csv") 
          char const separator: The separator character (default is ';')
        
        Returns
          void: No description
        """
    def saveStreetDensities(self, filename: str, normalized: bool = True, separator: str = ';') -> None:
        """
        Description
        Save the street densities in csv format.
        
        Args
          std::string filename: The name of the file (default is "{datetime}_{simulation_name}_street_densities.csv") 
          bool normalized: If true, the densities are normalized in [0, 1] 
          char const separator: No description
        
        Returns
          void: No description
        """
    def saveTravelData(self, filename: str, reset: bool = False) -> None:
        """
        Description
        Save the travel data of the agents in csv format. 
        The file contains the following columns:
        
        Args
          std::string filename: The name of the file (default is "{datetime}_{simulation_name}_travel_data.csv") 
          bool reset: If true, the travel speeds are cleared after the computation 
        
        Returns
          void: No description
        """
    def setDataUpdatePeriod(self, dataUpdatePeriod: typing.SupportsInt) -> None:
        """
        Description
        Set the data update period.
        
        Args
          delay_t dataUpdatePeriod: delay_t, The period
        
        Returns
          void: No description
        """
    @typing.overload
    def setDestinationNodes(self, destinationNodes: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Description
        Set the destination nodes.
        
        Args
          typename TContainer: No description
          TContainer const & destinationNodes: A container of destination nodes ids
        
        Returns
          void: No description
        """
    @typing.overload
    def setDestinationNodes(self, destinationNodes: typing.Annotated[numpy.typing.ArrayLike, numpy.uint64]) -> None:
        """
        Description
        Set the destination nodes.
        
        Args
          typename TContainer: No description
          TContainer const & destinationNodes: A container of destination nodes ids
        
        Returns
          void: No description
        """
    @typing.overload
    def setDestinationNodes(self, destinationNodes: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat]) -> None:
        """
        Description
        Set the destination nodes.
        
        Args
          typename TContainer: No description
          TContainer const & destinationNodes: A container of destination nodes ids
        
        Returns
          void: No description
        """
    def setErrorProbability(self, errorProbability: typing.SupportsFloat) -> None:
        """
        Description
        Set the error probability.
        
        Args
          double errorProbability: The error probability 
        
        Returns
          void: No description
        """
    def setForcePriorities(self: ..., forcePriorities: bool) -> None:
        """
        Description
        Set the force priorities flag.
        
        Args
          bool forcePriorities: The flag
        
        Returns
          void: No description
        """
    @typing.overload
    def setInitTime(self, timeEpoch: typing.SupportsInt) -> None:
        """
        Description
        Set the initial time as epoch time.
        
        Args
          std::time_t timeEpoch: The initial time as epoch time 
        
        Returns
          void: No description
        """
    @typing.overload
    def setInitTime(self, datetime: typing.Any) -> None:
        """
        Description
        Set the initial time as epoch time.
        
        Args
          std::time_t timeEpoch: The initial time as epoch time 
        
        Returns
          void: No description
        """
    def setMeanTravelDistance(self, meanDistance: typing.SupportsFloat) -> None:
        """
        Description
        Set the mean distance travelled by a random agent. The distance will be sampled from an exponential distribution with this mean.
        
        Args
          double const meanTravelDistance: The mean distance 
        
        Returns
          void: No description
        """
    def setMeanTravelTime(self, meanTravelTime: typing.SupportsInt) -> None:
        """
        Description
        Set the mean travel time for random agents. The travel time will be sampled from an exponential distribution with this mean.
        
        Args
          std::time_t const meanTravelTime: The mean travel time 
        
        Returns
          void: No description
        """
    def setName(self, name: str) -> None:
        """
        Description
        Set the name of the simulation.
        
        Args
          const std::string & name: The name of the simulation 
        
        Returns
          void: No description
        """
    @typing.overload
    def setOriginNodes(self, originNodes: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat]) -> None:
        """
        Description
        Set the origin nodes.
        
        Args
          std::unordered_map< Id, double > const & originNodes: The origin nodes 
        
        Returns
          void: No description
        """
    @typing.overload
    def setOriginNodes(self, originNodes: typing.Annotated[numpy.typing.ArrayLike, numpy.uint64]) -> None:
        """
        Description
        Set the origin nodes.
        
        Args
          std::unordered_map< Id, double > const & originNodes: The origin nodes 
        
        Returns
          void: No description
        """
    def setWeightFunction(self, weightFunction: PathWeight, weightThreshold: typing.SupportsFloat | None = None) -> None:
        ...
    def time(self) -> int:
        """
        Description
        Get the current simulation time as epoch time.
        
        Args
          None
        
        Returns
          auto: std::time_t, The current simulation time as epoch time 
        """
    def time_step(self) -> int:
        """
        Description
        Get the current simulation time-step.
        
        Args
          None
        
        Returns
          auto: std::time_t, The current simulation time-step 
        """
    def turnCounts(self) -> dict:
        """
        Description
        Get the turn counts of the agents.
        
        Args
          None
        
        Returns
          std::unordered_map< Id, std::unordered_map< Id, size_t > > const &: const std::unordered_map<Id, std::unordered_map<Id, size_t>>& The turn counts. The outer map's key is the street id, the inner map's key is the next street id and the value is the number of counts 
        """
    def updatePaths(self, throw_on_empty: bool = True) -> None:
        """
        Description
        Update the paths of the itineraries based on the given weight function.
        
        Args
          bool const throw_on_empty: If true, throws an exception if an itinerary has an empty path (default is true) If false, removes the itinerary with empty paths and the associated node from the origin/destination nodes 
        
        Returns
          void: No description
        """
class Itinerary:
    def __init__(self, id: typing.SupportsInt, destination: typing.SupportsInt) -> None:
        """
        Description
        No description available.
        
        Args
          const Itinerary &: No description
        
        Returns
          void: No return value
        """
    def destination(self) -> int:
        """
        Description
        Get the itinerary's destination.
        
        Args
          None
        
        Returns
          auto: Id, The itinerary's destination 
        """
    def id(self) -> int:
        """
        Description
        Get the itinerary's id.
        
        Args
          None
        
        Returns
          auto: Id, The itinerary's id 
        """
    def setPath(self, path: PathCollection) -> None:
        """
        Description
        Set the itinerary's path.
        
        Args
          PathCollection pathCollection: A 
        
        Returns
          void: No description
        """
class PathCollection:
    def __contains__(self, key: typing.SupportsInt) -> bool:
        """
        Check if a node id exists in the collection
        """
    def __getitem__(self, key: typing.SupportsInt) -> list[int]:
        """
        Get the next hops for a given node id
        """
    def __init__(self) -> None:
        """
        Create an empty PathCollection
        """
    def __len__(self) -> int:
        """
        Get the number of nodes in the collection
        """
    def __setitem__(self, key: typing.SupportsInt, value: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Set the next hops for a given node id
        """
    def explode(self, sourceId: typing.SupportsInt, targetId: typing.SupportsInt) -> list[list[int]]:
        """
        Description
        Explode all possible paths from sourceId to targetId.
        
        Args
          Id const sourceId: The starting point of the paths 
          Id const targetId: The end point of the paths 
        
        Returns
          std::list< std::vector< Id > >: A list of vectors, each vector representing a path from sourceId to targetId 
        """
    def items(self) -> dict:
        """
        Get all items (node id, next hops) in the collection
        """
    def keys(self) -> list[int]:
        """
        Get all node ids in the collection
        """
class PathWeight:
    """
    Members:
    
      LENGTH
    
      TRAVELTIME
    
      WEIGHT
    """
    LENGTH: typing.ClassVar[PathWeight]  # value = <PathWeight.LENGTH: 0>
    TRAVELTIME: typing.ClassVar[PathWeight]  # value = <PathWeight.TRAVELTIME: 1>
    WEIGHT: typing.ClassVar[PathWeight]  # value = <PathWeight.WEIGHT: 2>
    __members__: typing.ClassVar[dict[str, PathWeight]]  # value = {'LENGTH': <PathWeight.LENGTH: 0>, 'TRAVELTIME': <PathWeight.TRAVELTIME: 1>, 'WEIGHT': <PathWeight.WEIGHT: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class RoadNetwork:
    @typing.overload
    def __init__(self) -> None:
        """
        Description
        No description available.
        
        Args
          RoadNetwork &&: No description
        
        Returns
          void: No return value
        """
    @typing.overload
    def __init__(self, arg0: dsf_cpp.AdjacencyMatrix) -> None:
        """
        Description
        No description available.
        
        Args
          RoadNetwork &&: No description
        
        Returns
          void: No return value
        """
    def addCoil(self, streetId: typing.SupportsInt, name: str = '') -> None:
        """
        Description
        Add a coil (dsf::Counter sensor) on the street with streetId.
        
        Args
          Id streetId: The id of the street to add the coil to 
          std::string const & name: The coil name 
        
        Returns
          void: No description
        """
    def adjustNodeCapacities(self) -> None:
        """
        Description
        Adjust the nodes' transport capacity. 
        The nodes' capacity is adjusted using the graph's streets transport capacity, which may vary basing on the number of lanes. The node capacity will be set to the sum of the incoming streets' transport capacity.
        
        Args
          None
        
        Returns
          void: No description
        """
    def autoMapStreetLanes(self) -> None:
        """
        Description
        Automatically re-maps street lanes basing on network's topology. 
        For example, if one street has the right turn forbidden, then the right lane becomes a straight one
        
        Args
          None
        
        Returns
          void: No description
        """
    def capacity(self) -> int:
        """
        Description
        Get the maximum agent capacity.
        
        Args
          None
        
        Returns
          auto: unsigned long long The maximum agent capacity of the graph 
        """
    @typing.overload
    def importEdges(self, fileName: str) -> None:
        """
        Description
        Import the graph's streets from a file.
        
        Args
          typename... TArgs: No description
          const std::string & fileName: The name of the file to import the streets from.
          TArgs &&... args: No description
        
        Returns
          void: No description
        """
    @typing.overload
    def importEdges(self, fileName: str, separator: str) -> None:
        """
        Description
        Import the graph's streets from a file.
        
        Args
          typename... TArgs: No description
          const std::string & fileName: The name of the file to import the streets from.
          TArgs &&... args: No description
        
        Returns
          void: No description
        """
    @typing.overload
    def importEdges(self, fileName: str, bCreateInverse: bool) -> None:
        """
        Description
        Import the graph's streets from a file.
        
        Args
          typename... TArgs: No description
          const std::string & fileName: The name of the file to import the streets from.
          TArgs &&... args: No description
        
        Returns
          void: No description
        """
    def importNodeProperties(self, fileName: str, separator: str = ';') -> None:
        """
        Description
        Import the graph's nodes properties from a file.
        
        Args
          typename... TArgs: No description
          const std::string & fileName: The name of the file to import the nodes properties from.
          TArgs &&... args: No description
        
        Returns
          void: No description
        """
    def importTrafficLights(self, fileName: str) -> None:
        """
        Description
        Import the graph's traffic lights from a file.
        
        Args
          const std::string & fileName: The name of the file to import the traffic lights from.
        
        Returns
          void: No description
        """
    def initTrafficLights(self, minGreenTime: typing.SupportsInt = 30) -> None:
        """
        Description
        Initialize the traffic lights with random parameters.
        
        Args
          Delay const minGreenTime: The minimum green time for the traffic lights cycles (default is 30)
        
        Returns
          void: No description
        """
    def makeRoundabout(self, id: typing.SupportsInt) -> None:
        """
        Description
        Convert an existing node into a roundabout.
        
        Args
          Id nodeId: The id of the node to convert to a roundabout 
        
        Returns
          Roundabout: A reference to the roundabout 
        """
    def makeTrafficLight(self, id: typing.SupportsInt, cycleTime: typing.SupportsInt, counter: typing.SupportsInt) -> None:
        """
        Description
        Convert an existing node to a traffic light.
        
        Args
          Id const nodeId: The id of the node to convert to a traffic light 
          Delay const cycleTime: The traffic light's cycle time 
          Delay const counter: The traffic light's counter initial value. Default is 0 
        
        Returns
          TrafficLight: A reference to the traffic light 
        """
    def nCoils(self) -> int:
        """
        Description
        Get the graph's number of coil streets.
        
        Args
          None
        
        Returns
          Size: The number of coil streets 
        """
    def nEdges(self) -> int:
        """
        Description
        Get the number of edges.
        
        Args
          None
        
        Returns
          size_t: size_t The number of edges 
        """
    def nIntersections(self) -> int:
        """
        Description
        Get the graph's number of intersections.
        
        Args
          None
        
        Returns
          Size: The number of intersections 
        """
    def nNodes(self) -> int:
        """
        Description
        Get the number of nodes.
        
        Args
          None
        
        Returns
          size_t: size_t The number of nodes 
        """
    def nRoundabouts(self) -> int:
        """
        Description
        Get the graph's number of roundabouts.
        
        Args
          None
        
        Returns
          Size: The number of roundabouts 
        """
    def nTrafficLights(self) -> int:
        """
        Description
        Get the graph's number of traffic lights.
        
        Args
          None
        
        Returns
          Size: The number of traffic lights 
        """
    def setStreetStationaryWeights(self, weights: collections.abc.Mapping[typing.SupportsInt, typing.SupportsFloat]) -> None:
        """
        Description
        Set the streets' stationary weights.
        
        Args
          std::unordered_map< Id, double > const & streetWeights: A map where the key is the street id and the value is the street stationary weight. If a street id is not present in the map, its stationary weight is set to 1.0. 
        
        Returns
          void: No description
        """
    def shortestPath(self, sourceId: typing.SupportsInt, targetId: typing.SupportsInt, weightFunction: PathWeight = ..., threshold: typing.SupportsFloat = 1e-09) -> ...:
        """
        Find the shortest path between two nodes using Dijkstra's algorithm.
        
        Args:
            sourceId (int): The id of the source node
            targetId (int): The id of the target node
            weightFunction (PathWeight): The weight function to use (LENGTH, TRAVELTIME, or WEIGHT)
            threshold (float): A threshold value to consider alternative paths
        
        Returns:
            PathCollection: A map where each key is a node id and the value is a vector of next hop node ids toward the target
        """
class TrafficLightOptimization:
    """
    Members:
    
      SINGLE_TAIL
    
      DOUBLE_TAIL
    """
    DOUBLE_TAIL: typing.ClassVar[TrafficLightOptimization]  # value = <TrafficLightOptimization.DOUBLE_TAIL: 1>
    SINGLE_TAIL: typing.ClassVar[TrafficLightOptimization]  # value = <TrafficLightOptimization.SINGLE_TAIL: 0>
    __members__: typing.ClassVar[dict[str, TrafficLightOptimization]]  # value = {'SINGLE_TAIL': <TrafficLightOptimization.SINGLE_TAIL: 0>, 'DOUBLE_TAIL': <TrafficLightOptimization.DOUBLE_TAIL: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
DOUBLE_TAIL: TrafficLightOptimization  # value = <TrafficLightOptimization.DOUBLE_TAIL: 1>
LENGTH: PathWeight  # value = <PathWeight.LENGTH: 0>
SINGLE_TAIL: TrafficLightOptimization  # value = <TrafficLightOptimization.SINGLE_TAIL: 0>
TRAVELTIME: PathWeight  # value = <PathWeight.TRAVELTIME: 1>
WEIGHT: PathWeight  # value = <PathWeight.WEIGHT: 2>
