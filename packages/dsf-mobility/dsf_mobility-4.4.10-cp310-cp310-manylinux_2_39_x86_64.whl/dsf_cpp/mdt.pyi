"""
Bindings for movement data tools (MDT) related classes and functions, under the dsf::mdt C++ namespace.
"""
from __future__ import annotations
import collections.abc
import typing
__all__: list[str] = ['TrajectoryCollection']
class TrajectoryCollection:
    @typing.overload
    def __init__(self, fileName: str, column_mapping: collections.abc.Mapping[str, str] = {}, separator: str = ';', bbox: typing.Annotated[collections.abc.Sequence[typing.SupportsFloat], "FixedSize(4)"] = [0.0, 0.0, 0.0, 0.0]) -> None:
        """
        Description
        Construct a
        
        Args
          std::string const & fileName: The path to the CSV file. 
          std::unordered_map< std::string, std::string > const & column_mapping: A mapping of column names. 
          char const sep: The character used to separate values in the CSV file. 
          std::array< double, 4 > const & bbox: Optional bounding box [minX, minY, maxX, maxY] to limit the area of interest. Default is empty (no bounding box). 
        
        Returns
          void: No return value
        """
    @typing.overload
    def __init__(self, df: typing.Any) -> None:
        """
        Constructor that builds a TrajectoryCollection from a pandas or polars DataFrame.
        
        Args:
        	df (pandas.DataFrame | polars.DataFrame): Input DataFrame. Must contain the following columns:
        		'uid' (identifier), 'timestamp' (epoch seconds), 'lat' (latitude),
        		'lon' (longitude). The constructor will call ``df.columns`` and
        		``df.to_numpy()`` internally. All cell values are converted to strings
        		when building the underlying C++ data structure.
        
        Returns:
        	dsf.mdt.TrajectoryCollection: A new TrajectoryCollection constructed from
        	the provided DataFrame.
        """
    def filter(self, cluster_radius_km: typing.SupportsFloat, max_speed_kph: typing.SupportsFloat = 150.0, min_points_per_trajectory: typing.SupportsInt = 2, min_duration_min: typing.SupportsInt | None = None) -> None:
        """
        Description
        Filter all point trajectories to identify stop points based on clustering and speed criteria.
        
        Args
          double const cluster_radius_km: The radius (in kilometers) to use for clustering points. 
          double const max_speed_kph: The max allowed speed (in km/h) to consider a cluster as a stop point. Default is 150.0 km/h. 
          std::size_t const min_points_per_trajectory: The minimum number of points required for a trajectory to be considered valid. Default is 2. 
          std::optional< std::time_t > const min_duration_min: The minimum duration (in minutes) for a cluster to be considered a stop point. If stops are detected, trajectories may be split into multiple segments. 
        
        Returns
          void: No description
        """
    def to_csv(self, fileName: str, sep: str = ';') -> None:
        """
        Description
        Export clustered trajectories to a CSV file with columns 'uid', 'trajectory_id', 'lon', 'lat', 'timestamp_in', 'timestamp_out'.
        
        Args
          std::string const & fileName: The path to the output CSV file. 
          char const sep: The character used to separate values in the CSV file. 
        
        Returns
          void: No description
        """
    def to_pandas(self) -> typing.Any:
        """
        Convert the TrajectoryCollection to a pandas DataFrame.
        
        Returns:
        	pandas.DataFrame: DataFrame containing the trajectory data with columns 'uid', 'trajectory_id', 'lon', 'lat', 'timestamp_in', and 'timestamp_out'.
        """
    def to_polars(self) -> typing.Any:
        """
        Convert the TrajectoryCollection to a polars DataFrame.
        
        Returns:
        	polars.DataFrame: DataFrame containing the trajectory data with columns 'uid', 'trajectory_id', 'lon', 'lat', 'timestamp_in', and 'timestamp_out'.
        """
