"""
Python bindings for the DSF library
"""
from __future__ import annotations
import typing
from . import mdt
from . import mobility
__all__: list[str] = ['AdjacencyMatrix', 'CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'LogLevel', 'Measurement', 'OFF', 'TRACE', 'WARN', 'get_log_level', 'mdt', 'mobility', 'set_log_level']
class AdjacencyMatrix:
    def __call__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> bool:
        """
        Description
        Get the link at the specified row and column.
        
        Args
          Id row: The row index of the element 
          Id col: The column index of the element 
        
        Returns
          bool: True if the link exists, false otherwise
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Description
        Construct a new
        
        Args
          std::string const & fileName: The name of the file containing the adjacency matrix 
        
        Returns
          void: No return value
        """
    @typing.overload
    def __init__(self, fileName: str) -> None:
        """
        Description
        Construct a new
        
        Args
          std::string const & fileName: The name of the file containing the adjacency matrix 
        
        Returns
          void: No return value
        """
    def clear(self) -> None:
        """
        Description
        Clear the adjacency matrix.
        
        Args
          None
        
        Returns
          void: No description
        """
    def clearCol(self, arg0: typing.SupportsInt) -> None:
        """
        Description
        Clear the column at the specified index. 
        The dimension of the matrix does not change.
        
        Args
          Id col: No description
        
        Returns
          void: No description
        """
    def clearRow(self, arg0: typing.SupportsInt) -> None:
        """
        Description
        Clear the row at the specified index. 
        The dimension of the matrix does not change.
        
        Args
          Id row: No description
        
        Returns
          void: No description
        """
    def contains(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> bool:
        """
        Description
        Check if the link row -> col exists in the adjacency matrix.
        
        Args
          Id row: The row index of the element 
          Id col: The column index of the element 
        
        Returns
          bool: True if the link exists, false otherwise
        """
    def elements(self) -> list[tuple[int, int]]:
        """
        Description
        Get a vector containing all the links in the adjacency matrix as pairs of nodes.
        
        Args
          None
        
        Returns
          std::vector< std::pair< Id, Id > >: A vector containing all the links in the adjacency matrix as pairs of nodes 
        """
    def empty(self) -> bool:
        """
        Description
        Check if the adjacency matrix is empty.
        
        Args
          None
        
        Returns
          bool: True if the adjacency matrix is empty, false otherwise 
        """
    def getCol(self, arg0: typing.SupportsInt) -> list[int]:
        """
        Description
        Get the column at the specified index.
        
        Args
          Id col: The column index 
        
        Returns
          std::vector< Id >: The column at the specified index 
        """
    def getInDegreeVector(self) -> list[int]:
        """
        Description
        Get the input degree vector of the adjacency matrix.
        
        Args
          None
        
        Returns
          std::vector< int >: The input degree vector of the adjacency matrix 
        """
    def getOutDegreeVector(self) -> list[int]:
        """
        Description
        Get the output degree vector of the adjacency matrix.
        
        Args
          None
        
        Returns
          std::vector< int >: The output degree vector of the adjacency matrix 
        """
    def getRow(self, arg0: typing.SupportsInt) -> list[int]:
        """
        Description
        Get the row at the specified index.
        
        Args
          Id row: The row index 
        
        Returns
          std::vector< Id >: The row at the specified index 
        """
    def insert(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> None:
        """
        Description
        Inserts the link row -> col in the adjacency matrix.
        
        Args
          Id row: The row index of the element 
          Id col: The column index of the element
        
        Returns
          void: No description
        """
    def n(self) -> int:
        """
        Description
        Get the number of nodes in the adjacency matrix.
        
        Args
          None
        
        Returns
          size_t: The number of nodes in the adjacency matrix 
        """
    def read(self, fileName: str) -> None:
        """
        Description
        Read the adjacency matrix from a binary file.
        
        Args
          std::string const & fileName: The name of the file containing the adjacency matrix 
        
        Returns
          void: No description
        """
    def save(self, fileName: str) -> None:
        """
        Description
        Write the adjacency matrix to a binary file.
        
        Args
          std::string const & fileName: The name of the file where the adjacency matrix will be written 
        
        Returns
          void: No description
        """
    def size(self) -> int:
        """
        Description
        Get the number of links in the adjacency matrix.
        
        Args
          None
        
        Returns
          size_t: The number of links in the adjacency matrix 
        """
class LogLevel:
    """
    Members:
    
      TRACE
    
      DEBUG
    
      INFO
    
      WARN
    
      ERROR
    
      CRITICAL
    
      OFF
    """
    CRITICAL: typing.ClassVar[LogLevel]  # value = <LogLevel.CRITICAL: 5>
    DEBUG: typing.ClassVar[LogLevel]  # value = <LogLevel.DEBUG: 1>
    ERROR: typing.ClassVar[LogLevel]  # value = <LogLevel.ERROR: 4>
    INFO: typing.ClassVar[LogLevel]  # value = <LogLevel.INFO: 2>
    OFF: typing.ClassVar[LogLevel]  # value = <LogLevel.OFF: 6>
    TRACE: typing.ClassVar[LogLevel]  # value = <LogLevel.TRACE: 0>
    WARN: typing.ClassVar[LogLevel]  # value = <LogLevel.WARN: 3>
    __members__: typing.ClassVar[dict[str, LogLevel]]  # value = {'TRACE': <LogLevel.TRACE: 0>, 'DEBUG': <LogLevel.DEBUG: 1>, 'INFO': <LogLevel.INFO: 2>, 'WARN': <LogLevel.WARN: 3>, 'ERROR': <LogLevel.ERROR: 4>, 'CRITICAL': <LogLevel.CRITICAL: 5>, 'OFF': <LogLevel.OFF: 6>}
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
class Measurement:
    def __init__(self, mean: typing.SupportsFloat, std: typing.SupportsFloat) -> None:
        """
        Description
        No description available.
        
        Args
          std::span< T > data: No description
        
        Returns
          void: No return value
        """
    @property
    def mean(self) -> float:
        """
        Description
        No description available.
        
        Args
          None
        
        Returns
          void: No return value
        """
    @mean.setter
    def mean(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def std(self) -> float:
        """
        Description
        No description available.
        
        Args
          None
        
        Returns
          void: No return value
        """
    @std.setter
    def std(self, arg0: typing.SupportsFloat) -> None:
        ...
def get_log_level() -> LogLevel:
    """
    Get the current global log level
    """
def set_log_level(level: LogLevel) -> None:
    """
    Set the global log level for spdlog
    """
CRITICAL: LogLevel  # value = <LogLevel.CRITICAL: 5>
DEBUG: LogLevel  # value = <LogLevel.DEBUG: 1>
ERROR: LogLevel  # value = <LogLevel.ERROR: 4>
INFO: LogLevel  # value = <LogLevel.INFO: 2>
OFF: LogLevel  # value = <LogLevel.OFF: 6>
TRACE: LogLevel  # value = <LogLevel.TRACE: 0>
WARN: LogLevel  # value = <LogLevel.WARN: 3>
__version__: str = '4.5.0'
