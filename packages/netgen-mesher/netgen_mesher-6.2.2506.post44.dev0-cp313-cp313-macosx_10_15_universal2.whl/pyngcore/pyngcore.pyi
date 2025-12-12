from __future__ import annotations
import collections.abc
import typing
__all__ = ['AddConsoleSink', 'AddFileSink', 'Array_D_S', 'Array_F_S', 'Array_I_S', 'Array_S_S', 'Array_U_S', 'Array_a_S', 'Array_h_S', 'Array_s_S', 'Array_t_S', 'Array_y_S', 'BitArray', 'ClearLoggingSinks', 'Flags', 'FlatArray_D_S', 'FlatArray_F_S', 'FlatArray_I_S', 'FlatArray_S_S', 'FlatArray_U_S', 'FlatArray_a_S', 'FlatArray_h_S', 'FlatArray_s_S', 'FlatArray_t_S', 'FlatArray_y_S', 'FlushOnLoggingLevel', 'GetTotalMemory', 'InitMPI', 'LOG_LEVEL', 'MPI_Comm', 'PajeTrace', 'ResetTimers', 'RunWithTaskManager', 'SetLoggingLevel', 'SetNumThreads', 'SuspendTaskManager', 'Table_I', 'TaskManager', 'Timer', 'Timers']
class Array_D_S(FlatArray_D_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_F_S(FlatArray_F_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_I_S(FlatArray_I_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_S_S(FlatArray_S_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_U_S(FlatArray_U_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
class Array_a_S(FlatArray_a_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
class Array_h_S(FlatArray_h_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_s_S(FlatArray_s_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Array_t_S(FlatArray_t_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
class Array_y_S(FlatArray_y_S):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[typing.SupportsInt]) -> None:
        """
        Makes array with given list of elements
        """
class BitArray:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def Clear(self) -> None:
        """
        Clear all bits
        """
    @typing.overload
    def Clear(self, i: typing.SupportsInt) -> None:
        """
        Clear bit at given position
        """
    def NumSet(self) -> int:
        ...
    @typing.overload
    def Set(self) -> None:
        """
        Set all bits
        """
    @typing.overload
    def Set(self, i: typing.SupportsInt) -> None:
        """
        Set bit at given position
        """
    def __and__(self, arg0: BitArray) -> BitArray:
        ...
    def __getitem__(self, pos: typing.SupportsInt) -> bool:
        """
        Returns bit from given position
        """
    def __getstate__(self) -> tuple:
        ...
    def __iand__(self, arg0: BitArray) -> BitArray:
        ...
    @typing.overload
    def __init__(self, n: typing.SupportsInt) -> None:
        ...
    @typing.overload
    def __init__(self, ba: BitArray) -> None:
        ...
    @typing.overload
    def __init__(self, vec: collections.abc.Sequence[bool]) -> None:
        ...
    def __invert__(self) -> BitArray:
        ...
    def __ior__(self, arg0: BitArray) -> BitArray:
        ...
    def __len__(self) -> int:
        ...
    def __or__(self, arg0: BitArray) -> BitArray:
        ...
    @typing.overload
    def __setitem__(self, pos: typing.SupportsInt, value: bool) -> None:
        """
        Clear/Set bit at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: bool) -> None:
        """
        Clear/Set bit at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, ba: BitArray) -> None:
        """
        copy BitArray
        """
    @typing.overload
    def __setitem__(self, range: ..., value: bool) -> None:
        """
        Set value for range of indices
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
class Flags:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def Set(self, aflag: dict) -> Flags:
        """
        Set the flags by given dict
        """
    @typing.overload
    def Set(self, akey: str, value: typing.Any) -> Flags:
        """
        Set flag by given value.
        """
    def ToDict(self) -> dict:
        ...
    def __getitem__(self, name: str) -> typing.Any:
        """
        Return flag by given name
        """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: dict) -> None:
        """
        Create flags from dict
        """
    @typing.overload
    def __init__(self, **kwargs) -> None:
        """
        Create flags from kwargs
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    def items(self) -> typing.Any:
        ...
    def keys(self) -> list:
        ...
class FlatArray_D_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> float:
        ...
    def __iter__(self) -> collections.abc.Iterator[float]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsFloat) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_F_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> float:
        ...
    def __iter__(self) -> collections.abc.Iterator[float]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsFloat) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_I_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_S_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_U_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_a_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_h_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_s_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_t_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class FlatArray_y_S:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: typing.SupportsInt) -> int:
        ...
    def __iter__(self) -> collections.abc.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
class LOG_LEVEL:
    """
    Logging level
    
    Members:
    
      Trace
    
      Debug
    
      Info
    
      Warn
    
      Error
    
      Critical
    
      Off
    """
    Critical: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Critical: 5>
    Debug: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Debug: 1>
    Error: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Error: 4>
    Info: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Info: 2>
    Off: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Off: 6>
    Trace: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Trace: 0>
    Warn: typing.ClassVar[LOG_LEVEL]  # value = <LOG_LEVEL.Warn: 3>
    __members__: typing.ClassVar[dict[str, LOG_LEVEL]]  # value = {'Trace': <LOG_LEVEL.Trace: 0>, 'Debug': <LOG_LEVEL.Debug: 1>, 'Info': <LOG_LEVEL.Info: 2>, 'Warn': <LOG_LEVEL.Warn: 3>, 'Error': <LOG_LEVEL.Error: 4>, 'Critical': <LOG_LEVEL.Critical: 5>, 'Off': <LOG_LEVEL.Off: 6>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
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
class MPI_Comm:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Barrier(self) -> None:
        ...
    @typing.overload
    def Max(self, arg0: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def Max(self, arg0: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def Max(self, arg0: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def Min(self, arg0: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def Min(self, arg0: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def Min(self, arg0: typing.SupportsInt) -> int:
        ...
    def SubComm(self, procs: collections.abc.Sequence[typing.SupportsInt]) -> MPI_Comm:
        ...
    @typing.overload
    def Sum(self, arg0: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def Sum(self, arg0: typing.SupportsInt) -> int:
        ...
    @typing.overload
    def Sum(self, arg0: typing.SupportsInt) -> int:
        ...
    def WTime(self) -> float:
        ...
    def __init__(self, arg0: mpi4py_comm) -> None:
        ...
    @property
    def mpi4py(self) -> typing.Any:
        ...
    @property
    def rank(self) -> int:
        ...
    @property
    def size(self) -> int:
        ...
class PajeTrace:
    @staticmethod
    def SetMaxTracefileSize(arg0: typing.SupportsInt) -> None:
        ...
    @staticmethod
    def SetTraceThreadCounter(arg0: bool) -> None:
        ...
    @staticmethod
    def SetTraceThreads(arg0: bool) -> None:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __enter__(self) -> None:
        ...
    def __exit__(self, *args) -> None:
        ...
    def __init__(self, filename: str = 'ng.trace', size: typing.SupportsInt = 1000, threads: bool = True, thread_counter: bool = False, memory: bool = True) -> None:
        """
        size in Megabytes
        """
class SuspendTaskManager:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __enter__(self) -> SuspendTaskManager:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> bool:
        ...
    def __init__(self, sleep_usecs: typing.SupportsInt = 1000) -> None:
        """
        sleep_usecs : int
            number of microseconds the worker threads sleep
        """
class Table_I:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, arg0: typing.SupportsInt) -> FlatArray_I_S:
        ...
    def __init__(self, blocks: list) -> None:
        """
        a list of lists
        """
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class TaskManager:
    @staticmethod
    def __timing__() -> list[tuple[str, float]]:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __enter__(self) -> None:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, pajetrace: typing.SupportsInt) -> None:
        """
        Run paje-tracer, specify buffersize in bytes
        """
class Timer:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Start(self) -> None:
        """
        start timer
        """
    def Stop(self) -> None:
        """
        stop timer
        """
    def __enter__(self) -> None:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    def __init__(self, arg0: str) -> None:
        ...
    @property
    def time(self) -> float:
        """
        returns time
        """
class _NG_MPI_Comm:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
def AddConsoleSink(level: LOG_LEVEL, logger: str = '') -> None:
    """
    Add console output for specific logger or all if none given
    """
def AddFileSink(filename: str, level: LOG_LEVEL, logger: str = '') -> None:
    """
    Add File sink, either only to logger specified or globally to all loggers
    """
def ClearLoggingSinks(logger: str = '') -> None:
    """
    Clear sinks of specific logger, or all if none given
    """
def FlushOnLoggingLevel(level: LOG_LEVEL, logger: str = '') -> None:
    """
    Flush every message with level at least `level` for specific logger or all loggers if none given.
    """
def GetTotalMemory() -> int:
    ...
def InitMPI(mpi_library_path: os.PathLike | str | bytes | None = None) -> None:
    ...
def ResetTimers() -> None:
    ...
def RunWithTaskManager(lam: typing.Any) -> None:
    """
    Parameters:
    
    lam : object
      input function
    """
def SetLoggingLevel(level: LOG_LEVEL, logger: str = '') -> None:
    """
    Set logging level, if name is given only to the specific logger, else set the global logging level
    """
def SetNumThreads(threads: typing.SupportsInt) -> None:
    """
    Set number of threads
    
    Parameters:
    
    threads : int
      input number of threads
    """
def Timers() -> list:
    """
    Returns list of timers
    """
