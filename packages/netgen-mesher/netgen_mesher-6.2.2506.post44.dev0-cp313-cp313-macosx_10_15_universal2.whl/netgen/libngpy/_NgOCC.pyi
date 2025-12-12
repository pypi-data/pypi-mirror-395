"""
pybind NgOCC module
"""
from __future__ import annotations
import collections.abc
import netgen.libngpy._meshing
import numpy
import numpy.typing
import pyngcore.pyngcore
import typing
__all__ = ['ApproxParamType', 'ArcOfCircle', 'Axes', 'Axis', 'BSplineCurve', 'BezierCurve', 'BezierSurface', 'Box', 'COMPOUND', 'COMPSOLID', 'Circle', 'Compound', 'Cone', 'ConnectEdgesToWires', 'Cylinder', 'Dir', 'DirectionalInterval', 'EDGE', 'Edge', 'Ellipse', 'Ellipsoid', 'FACE', 'Face', 'From_PyOCC', 'Fuse', 'Geom2d_Curve', 'Geom_Surface', 'Glue', 'HalfSpace', 'ListOfShapes', 'LoadOCCGeometry', 'MakeFillet', 'MakePolygon', 'MakeThickSolid', 'OCCException', 'OCCGeometry', 'Pipe', 'PipeShell', 'Pnt', 'Prism', 'ResetGlobalShapeProperties', 'Revolve', 'SHAPE', 'SHELL', 'SOLID', 'Segment', 'Sew', 'ShapeContinuity', 'Solid', 'Sphere', 'SplineApproximation', 'SplineInterpolation', 'SplineSurfaceApproximation', 'SplineSurfaceInterpolation', 'TestXCAF', 'ThruSections', 'TopAbs_ShapeEnum', 'TopLoc_Location', 'TopoDS_Shape', 'VERTEX', 'Vec', 'Vertex', 'WIRE', 'Wire', 'WorkPlane', 'X', 'Y', 'Z', 'gp_Ax2', 'gp_Ax2d', 'gp_Dir', 'gp_Dir2d', 'gp_GTrsf', 'gp_Mat', 'gp_Pnt', 'gp_Pnt2d', 'gp_Trsf', 'gp_Vec', 'gp_Vec2d', 'occ_version']
class ApproxParamType:
    """
    Wrapper for Approx_ParametrizationType
    
    Members:
    
      Centripetal
    
      ChordLength
    
      IsoParametric
    """
    Centripetal: typing.ClassVar[ApproxParamType]  # value = <ApproxParamType.Centripetal: 1>
    ChordLength: typing.ClassVar[ApproxParamType]  # value = <ApproxParamType.ChordLength: 0>
    IsoParametric: typing.ClassVar[ApproxParamType]  # value = <ApproxParamType.IsoParametric: 2>
    __members__: typing.ClassVar[dict[str, ApproxParamType]]  # value = {'Centripetal': <ApproxParamType.Centripetal: 1>, 'ChordLength': <ApproxParamType.ChordLength: 0>, 'IsoParametric': <ApproxParamType.IsoParametric: 2>}
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
class Axes:
    """
    an OCC coordinate system in 3d
    """
    p: gp_Pnt
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, p: gp_Pnt = (0, 0, 0), n: gp_Dir = (0, 0, 1), h: gp_Dir = (1, 0, 0)) -> None:
        ...
    @typing.overload
    def __init__(self, axis: Axis) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: gp_Ax2) -> None:
        ...
class Axis:
    """
    an OCC axis in 3d
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, p: gp_Pnt, d: gp_Dir) -> None:
        ...
class Compound(TopoDS_Shape):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, shapes: collections.abc.Sequence[TopoDS_Shape], separate_layers: bool = False) -> None:
        ...
class DirectionalInterval:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __and__(self, arg0: DirectionalInterval) -> DirectionalInterval:
        ...
    def __gt__(self, arg0: typing.SupportsFloat) -> DirectionalInterval:
        ...
    def __lt__(self, arg0: typing.SupportsFloat) -> DirectionalInterval:
        ...
    def __str__(self) -> str:
        ...
class Edge(TopoDS_Shape):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Extend(self, point: gp_Pnt, continuity: typing.SupportsInt = 1, after: bool = True) -> Edge:
        ...
    def Split(self, *args) -> ...:
        """
        Splits edge at given parameters. Parameters can either be floating values in (0,1), then edge parametrization is used. Or it can be points, then the projection of these points are used for splitting the edge.
        """
    def Tangent(self, s: typing.SupportsFloat) -> gp_Vec:
        """
        tangent vector to curve at parameter 's'
        """
    def Value(self, s: typing.SupportsFloat) -> gp_Pnt:
        """
        evaluate curve for parameters 's'
        """
    @typing.overload
    def __init__(self, arg0: TopoDS_Shape) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ..., arg1: TopoDS_Face) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: Vertex, arg1: Vertex) -> None:
        ...
    @property
    def end(self) -> gp_Pnt:
        """
        end-point of curve
        """
    @property
    def end_tangent(self) -> gp_Vec:
        """
        tangent at end-point
        """
    @property
    def parameter_interval(self) -> tuple[float, float]:
        """
        parameter interval of curve
        """
    @property
    def partition(self) -> pyngcore.pyngcore.Array_D_S | None:
        ...
    @partition.setter
    def partition(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        ...
    @property
    def start(self) -> gp_Pnt:
        """
        start-point of curve
        """
    @property
    def start_tangent(self) -> gp_Vec:
        """
        tangent at start-point
        """
class Face(TopoDS_Shape):
    quad_dominated: bool | None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Extend(self, length: typing.SupportsFloat, continuity: typing.SupportsInt = 1, u_direction: bool = True, after: bool = True) -> Face:
        ...
    def ProjectWire(self, arg0: Wire) -> TopoDS_Shape:
        ...
    def WorkPlane(self) -> WorkPlane:
        ...
    @typing.overload
    def __init__(self, w: Wire) -> None:
        ...
    @typing.overload
    def __init__(self, f: Face, w: Wire) -> None:
        ...
    @typing.overload
    def __init__(self, f: Face, w: collections.abc.Sequence[Wire]) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: TopoDS_Shape) -> None:
        ...
    @property
    def surf(self) -> ...:
        ...
class Geom2d_Curve:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Edge(self) -> Edge:
        ...
    def Face(self) -> Face:
        ...
    def Trim(self, arg0: typing.SupportsFloat, arg1: typing.SupportsFloat) -> Geom2d_Curve:
        ...
    def Value(self, arg0: typing.SupportsFloat) -> gp_Pnt2d:
        ...
    def Wire(self) -> Wire:
        ...
    @property
    def end(self) -> gp_Pnt2d:
        ...
    @property
    def start(self) -> gp_Pnt2d:
        ...
class Geom_Surface:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def D1(self, arg0: typing.SupportsFloat, arg1: typing.SupportsFloat) -> tuple[gp_Pnt, gp_Vec, gp_Vec]:
        ...
    def Normal(self, arg0: typing.SupportsFloat, arg1: typing.SupportsFloat) -> gp_Dir:
        ...
    def Value(self, arg0: typing.SupportsFloat, arg1: typing.SupportsFloat) -> gp_Pnt:
        ...
class ListOfShapes:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Identify(self, other: ListOfShapes, name: str, type: netgen.libngpy._meshing.IdentificationType = ..., trafo: netgen.libngpy._NgOCC.gp_Trsf | netgen.libngpy._NgOCC.gp_GTrsf) -> None:
        """
        Identify shapes for periodic meshing
        """
    def Max(self, dir: gp_Vec) -> typing.Any:
        """
        returns shape where center of gravity is maximal in the direction 'dir'
        """
    def Min(self, dir: gp_Vec) -> typing.Any:
        """
        returns shape where center of gravity is minimal in the direction 'dir'
        """
    @typing.overload
    def Nearest(self, p: gp_Pnt) -> typing.Any:
        """
        returns shape nearest to point 'p'
        """
    @typing.overload
    def Nearest(self, p: gp_Pnt2d) -> typing.Any:
        """
        returns shape nearest to point 'p'
        """
    def Sorted(self, dir: gp_Vec) -> ListOfShapes:
        """
        returns list of shapes, where center of gravity is sorted in direction of 'dir'
        """
    @typing.overload
    def __add__(self, arg0: ListOfShapes) -> ListOfShapes:
        ...
    @typing.overload
    def __add__(self, arg0: list) -> ListOfShapes:
        ...
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> typing.Any:
        ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> ListOfShapes:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> ListOfShapes:
        """
        returns list of all shapes named 'name'
        """
    @typing.overload
    def __getitem__(self, arg0: DirectionalInterval) -> ListOfShapes:
        ...
    def __init__(self, arg0: collections.abc.Sequence[TopoDS_Shape]) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator[typing.Any]:
        ...
    def __len__(self) -> int:
        ...
    def __mul__(self, arg0: ListOfShapes) -> ListOfShapes:
        ...
    @property
    def col(self) -> None:
        """
        set col for all elements of list
        """
    @col.setter
    def col(self, arg1: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def edges(self) -> ListOfShapes:
        ...
    @property
    def faces(self) -> ListOfShapes:
        ...
    @property
    def hpref(self) -> None:
        """
        set hpref for all elements of list
        """
    @hpref.setter
    def hpref(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def maxh(self) -> None:
        """
        set maxh for all elements of list
        """
    @maxh.setter
    def maxh(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def name(self) -> None:
        """
        set name for all elements of list
        """
    @name.setter
    def name(self, arg1: str | None) -> None:
        ...
    @property
    def quad_dominated(self) -> None:
        ...
    @quad_dominated.setter
    def quad_dominated(self, arg1: bool | None) -> None:
        ...
    @property
    def shells(self) -> ListOfShapes:
        ...
    @property
    def solids(self) -> ListOfShapes:
        ...
    @property
    def vertices(self) -> ListOfShapes:
        ...
    @property
    def wires(self) -> ListOfShapes:
        ...
class OCCException(Exception):
    pass
class OCCGeometry(netgen.libngpy._meshing.NetgenGeometry):
    """
    Use LoadOCCGeometry to load the geometry from a *.step file.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Draw(self) -> None:
        ...
    def GenerateMesh(self, mp: netgen.libngpy._meshing.MeshingParameters = None, comm: pyngcore.pyngcore.MPI_Comm = ..., mesh: netgen.libngpy._meshing.Mesh = None, **kwargs) -> netgen.libngpy._meshing.Mesh:
        """
        Meshing Parameters
        -------------------
        
        maxh: float = 1e10
          Global upper bound for mesh size.
        
        grading: float = 0.3
          Mesh grading how fast the local mesh size can change.
        
        meshsizefilename: str = None
          Load meshsize from file. Can set local mesh size for points
          and along edges. File must have the format:
        
            nr_points
            x1, y1, z1, meshsize
            x2, y2, z2, meshsize
            ...
            xn, yn, zn, meshsize
        
            nr_edges
            x11, y11, z11, x12, y12, z12, meshsize
            ...
            xn1, yn1, zn1, xn2, yn2, zn2, meshsize
        
        segmentsperedge: float = 1.
          Minimal number of segments per edge.
        
        quad_dominated: bool = False
          Quad-dominated surface meshing.
        
        blockfill: bool = True
          Do fast blockfilling.
        
        filldist: float = 0.1
          Block fill up to distance
        
        delaunay: bool = True
          Use delaunay meshing.
        
        delaunay2d : bool = True
          Use delaunay meshing for 2d geometries.
        
        Optimization Parameters
        -----------------------
        
        optimize3d: str = "cmdmustm"
          3d optimization strategy:
            m .. move nodes
            M .. move nodes, cheap functional
            s .. swap faces
            c .. combine elements
            d .. divide elements
            p .. plot, no pause
            P .. plot, Pause
            h .. Histogramm, no pause
            H .. Histogramm, pause
        
        optsteps3d: int = 3
          Number of 3d optimization steps.
        
        optimize2d: str = "smcmSmcmSmcm"
          2d optimization strategy:
            s .. swap, opt 6 lines/node
            S .. swap, optimal elements
            m .. move nodes
            p .. plot, no pause
            P .. plot, pause
            c .. combine
        
        optsteps2d: int = 3
          Number of 2d optimization steps.
        
        elsizeweight: float = 0.2
          Weight of element size w.r.t. element shape in optimization.
        
        
        OCC Specific Meshing Parameters
        -------------------------------
        
        closeedgefac: Optional[float] = 2.
          Factor for meshing close edges, if None it is disabled.
        
        minedgelen: Optional[float] = 0.001
          Minimum edge length to be used for dividing edges to mesh points. If
          None this is disabled.
        """
    def Glue(self) -> None:
        ...
    def Heal(self, tolerance: typing.SupportsFloat = 0.001, fixsmalledges: bool = True, fixspotstripfaces: bool = True, sewfaces: bool = True, makesolids: bool = True, splitpartitions: bool = False) -> None:
        """
        Heal the OCCGeometry.
        """
    def SetFaceMeshsize(self, arg0: typing.SupportsInt, arg1: typing.SupportsFloat) -> None:
        """
        Set maximum meshsize for face fnr. Face numbers are 0 based.
        """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, shape: TopoDS_Shape, dim: typing.SupportsInt = 3, copy: bool = False) -> None:
        """
        Create Netgen OCCGeometry from existing TopoDS_Shape
        """
    @typing.overload
    def __init__(self, shape: collections.abc.Sequence[TopoDS_Shape]) -> None:
        """
        Create Netgen OCCGeometry from existing TopoDS_Shape
        """
    @typing.overload
    def __init__(self, filename: str, dim: typing.SupportsInt = 3) -> None:
        """
        Load OCC geometry from step, brep or iges file
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def _visualizationData(self) -> dict:
        ...
    @property
    def edges(self) -> ListOfShapes:
        """
        Get edges in order that they will be in the mesh
        """
    @property
    def faces(self) -> ListOfShapes:
        """
        Get faces in order that they will be in the mesh
        """
    @property
    def shape(self) -> TopoDS_Shape:
        ...
    @property
    def solids(self) -> ListOfShapes:
        """
        Get solids in order that they will be in the mesh
        """
    @property
    def vertices(self) -> ListOfShapes:
        """
        Get vertices in order that they will be in the mesh
        """
class ShapeContinuity:
    """
    Wrapper for OCC enum GeomAbs_Shape
    
    Members:
    
      C0
    
      C1
    
      C2
    
      C3
    
      CN
    
      G1
    
      G2
    """
    C0: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.C0: 0>
    C1: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.C1: 2>
    C2: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.C2: 4>
    C3: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.C3: 5>
    CN: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.CN: 6>
    G1: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.G1: 1>
    G2: typing.ClassVar[ShapeContinuity]  # value = <ShapeContinuity.G2: 3>
    __members__: typing.ClassVar[dict[str, ShapeContinuity]]  # value = {'C0': <ShapeContinuity.C0: 0>, 'C1': <ShapeContinuity.C1: 2>, 'C2': <ShapeContinuity.C2: 4>, 'C3': <ShapeContinuity.C3: 5>, 'CN': <ShapeContinuity.CN: 6>, 'G1': <ShapeContinuity.G1: 1>, 'G2': <ShapeContinuity.G2: 3>}
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
class Solid(TopoDS_Shape):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: TopoDS_Shape) -> None:
        """
        Create solid from shell. Shell must consist of topologically closed faces (share vertices and edges).
        """
class TopAbs_ShapeEnum:
    """
    Enumeration of all supported TopoDS_Shapes
    
    Members:
    
      COMPOUND
    
      COMPSOLID
    
      SOLID
    
      SHELL
    
      FACE
    
      WIRE
    
      EDGE
    
      VERTEX
    
      SHAPE
    """
    COMPOUND: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.COMPOUND: 0>
    COMPSOLID: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.COMPSOLID: 1>
    EDGE: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.EDGE: 6>
    FACE: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.FACE: 4>
    SHAPE: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.SHAPE: 8>
    SHELL: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.SHELL: 3>
    SOLID: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.SOLID: 2>
    VERTEX: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.VERTEX: 7>
    WIRE: typing.ClassVar[TopAbs_ShapeEnum]  # value = <TopAbs_ShapeEnum.WIRE: 5>
    __members__: typing.ClassVar[dict[str, TopAbs_ShapeEnum]]  # value = {'COMPOUND': <TopAbs_ShapeEnum.COMPOUND: 0>, 'COMPSOLID': <TopAbs_ShapeEnum.COMPSOLID: 1>, 'SOLID': <TopAbs_ShapeEnum.SOLID: 2>, 'SHELL': <TopAbs_ShapeEnum.SHELL: 3>, 'FACE': <TopAbs_ShapeEnum.FACE: 4>, 'WIRE': <TopAbs_ShapeEnum.WIRE: 5>, 'EDGE': <TopAbs_ShapeEnum.EDGE: 6>, 'VERTEX': <TopAbs_ShapeEnum.VERTEX: 7>, 'SHAPE': <TopAbs_ShapeEnum.SHAPE: 8>}
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
class TopLoc_Location:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Transformation(self) -> gp_Trsf:
        ...
    def __init__(self, arg0: gp_Trsf) -> None:
        ...
class TopoDS_Shape:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Distance(self, arg0: TopoDS_Shape) -> float:
        ...
    @typing.overload
    def Extrude(self, h: typing.SupportsFloat, dir: netgen.libngpy._NgOCC.gp_Vec | None = None, identify: bool = False, idtype: netgen.libngpy._meshing.IdentificationType = ..., idname: str = 'extrusion') -> TopoDS_Shape:
        """
        extrude shape to thickness 'h', shape must contain a plane surface, optionally give an extrusion direction
        """
    @typing.overload
    def Extrude(self, v: gp_Vec) -> TopoDS_Shape:
        """
        extrude shape by vector 'v'
        """
    def GenerateMesh(self, mp: netgen.libngpy._meshing.MeshingParameters = None, dim: typing.SupportsInt = 3, ngs_mesh: bool = True, **kwargs) -> typing.Any:
        ...
    def Identify(self, other: TopoDS_Shape, name: str, type: netgen.libngpy._meshing.IdentificationType = ..., trafo: netgen.libngpy._NgOCC.gp_Trsf | netgen.libngpy._NgOCC.gp_GTrsf | None = None) -> None:
        """
        Identify shapes for periodic meshing
        """
    def LimitTolerance(self, tmin: typing.SupportsFloat, tmax: typing.SupportsFloat = 0.0, type: TopAbs_ShapeEnum = ...) -> None:
        """
        limit tolerance of shape to range [tmin, tmax]
        """
    def Located(self, loc: TopLoc_Location) -> TopoDS_Shape:
        """
        copy shape and sets location of copy
        """
    def MakeChamfer(self, edges: collections.abc.Sequence[TopoDS_Shape], d: typing.SupportsFloat) -> TopoDS_Shape:
        """
        make symmetric chamfer for edges 'edges' of distrance 'd'
        """
    @typing.overload
    def MakeFillet(self, fillets: collections.abc.Sequence[tuple[TopoDS_Shape, typing.SupportsFloat]]) -> TopoDS_Shape:
        """
        make fillets for shapes of radius 'r'
        """
    @typing.overload
    def MakeFillet(self, edges: collections.abc.Sequence[TopoDS_Shape], r: typing.SupportsFloat) -> TopoDS_Shape:
        """
        make fillets for edges 'edges' of radius 'r'
        """
    def MakeThickSolid(self, facestoremove: collections.abc.Sequence[TopoDS_Shape], offset: typing.SupportsFloat, tol: typing.SupportsFloat, intersection: bool = False, joinType: str = 'arc', removeIntersectingEdges: bool = False) -> TopoDS_Shape:
        """
        makes shell-like solid from faces
        """
    def MakeTriangulation(self) -> None:
        ...
    @typing.overload
    def Mirror(self, axes: Axes) -> TopoDS_Shape:
        """
        copy shape, and mirror over XY - plane defined by 'axes'
        """
    @typing.overload
    def Mirror(self, axes: Axis) -> TopoDS_Shape:
        """
        copy shape, and rotate by 180 deg around axis 'axis'
        """
    def Move(self, v: gp_Vec) -> typing.Any:
        """
        copy shape, and translate copy by vector 'v'
        """
    def Offset(self, offset: typing.SupportsFloat, tol: typing.SupportsFloat, intersection: bool = False, joinType: str = 'arc', removeIntersectingEdges: bool = False, identification_name: str | None = None) -> TopoDS_Shape:
        """
        makes shell-like solid from faces
        """
    def Properties(self) -> tuple[typing.Any, typing.Any]:
        """
        returns tuple of shape properties, currently ('mass', 'center'
        """
    def Reversed(self) -> typing.Any:
        ...
    def Revolve(self, axis: Axis, ang: typing.SupportsFloat) -> TopoDS_Shape:
        """
        revolve shape around 'axis' by 'ang' degrees
        """
    def Rotate(self, axis: Axis, ang: typing.SupportsFloat) -> TopoDS_Shape:
        """
        copy shape, and rotet copy by 'ang' degrees around 'axis'
        """
    def Scale(self, p: gp_Pnt, s: typing.SupportsFloat) -> TopoDS_Shape:
        """
        copy shape, and scale copy by factor 's'
        """
    def SetTolerance(self, tol: typing.SupportsFloat, stype: TopAbs_ShapeEnum = ...) -> None:
        """
        set (enforce) tolerance of shape to 't'
        """
    def ShapeType(self) -> None:
        """
        deprecated, use 'shape.type' instead
        """
    def SubShapes(self, type: TopAbs_ShapeEnum) -> ...:
        """
        returns list of sub-shapes of type 'type'
        """
    def Triangulation(self) -> ...:
        ...
    def UnifySameDomain(self, unifyEdges: bool = True, unifyFaces: bool = True, concatBSplines: bool = True) -> TopoDS_Shape:
        ...
    def WriteBrep(self, filename: str, withTriangles: bool = True, withNormals: bool = False, version: typing.SupportsInt | None = None, binary: bool = False) -> None:
        """
        export shape in BREP - format
        """
    def WriteStep(self, filename: str) -> None:
        """
        export shape in STEP - format
        """
    def __add__(self, arg0: TopoDS_Shape) -> TopoDS_Shape:
        """
        fuses shapes
        """
    def __eq__(self, arg0: TopoDS_Shape) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __mul__(self, arg0: TopoDS_Shape) -> TopoDS_Shape:
        """
        common of shapes
        """
    def __radd__(self, arg0: typing.SupportsInt) -> TopoDS_Shape:
        """
        needed for Sum([shapes])
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: TopoDS_Shape) -> TopoDS_Shape:
        """
        cut of shapes
        """
    def _webgui_data(self) -> dict:
        ...
    def bc(self, name: str) -> TopoDS_Shape:
        """
        sets 'name' property for all faces of shape
        """
    def mat(self, name: str) -> TopoDS_Shape:
        """
        sets 'name' property to all solids of shape
        """
    @property
    def bounding_box(self) -> tuple:
        """
        returns bounding box (pmin, pmax)
        """
    @property
    def center(self) -> gp_Pnt:
        """
        returns center of gravity of shape
        """
    @property
    def col(self) -> typing.Any:
        """
        color of shape as RGB or RGBA - tuple
        """
    @col.setter
    def col(self, arg1: collections.abc.Sequence[typing.SupportsFloat] | None) -> None:
        ...
    @property
    def edges(self) -> ...:
        """
        returns all sub-shapes of type 'EDGE'
        """
    @property
    def faces(self) -> ...:
        """
        returns all sub-shapes of type 'FACE'
        """
    @property
    def hpref(self) -> float:
        """
        number of refinement levels for geometric refinement
        """
    @hpref.setter
    def hpref(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def inertia(self) -> gp_Mat:
        """
        returns matrix of inertia of shape
        """
    @property
    def layer(self) -> int:
        """
        layer of shape
        """
    @layer.setter
    def layer(self, arg1: typing.SupportsInt) -> None:
        ...
    @property
    def location(self) -> TopLoc_Location:
        """
        Location of shape
        """
    @location.setter
    def location(self, arg1: TopLoc_Location) -> None:
        ...
    @property
    def mass(self) -> float:
        """
        returns mass of shape, what is length, face, or volume
        """
    @property
    def maxh(self) -> float:
        """
        maximal mesh-size for shape
        """
    @maxh.setter
    def maxh(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def name(self) -> str | None:
        """
        'name' of shape
        """
    @name.setter
    def name(self, arg1: str | None) -> None:
        ...
    @property
    def shells(self) -> ...:
        """
        returns all sub-shapes of type 'SHELL'
        """
    @property
    def solids(self) -> ...:
        """
        returns all sub-shapes of type 'SOLID'
        """
    @property
    def type(self) -> TopAbs_ShapeEnum:
        """
        returns type of shape, i.e. 'EDGE', 'FACE', ...
        """
    @property
    def vertices(self) -> ...:
        """
        returns all sub-shapes of type 'VERTEX'
        """
    @property
    def wires(self) -> ...:
        """
        returns all sub-shapes of type 'WIRE'
        """
class Vertex(TopoDS_Shape):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, arg0: TopoDS_Shape) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: gp_Pnt) -> None:
        ...
    @property
    def p(self) -> gp_Pnt:
        """
        coordinates of vertex
        """
class Wire(TopoDS_Shape):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Offset(self, arg0: TopoDS_Face, arg1: typing.SupportsFloat, arg2: str, arg3: bool) -> TopoDS_Shape:
        ...
    @typing.overload
    def __init__(self, arg0: Edge) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: collections.abc.Sequence[TopoDS_Shape]) -> None:
        ...
class WorkPlane:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Arc(self, r: typing.SupportsFloat, ang: typing.SupportsFloat, name: str | None = None, maxh: typing.SupportsFloat | None = None) -> WorkPlane:
        """
        draw arc tangential to current pos/dir, of radius 'r' and angle 'ang', draw to the left/right if ang is positive/negative
        """
    def ArcTo(self, h: typing.SupportsFloat, v: typing.SupportsFloat, t: gp_Vec2d, name: str | None = None, maxh: typing.SupportsFloat | None = None) -> WorkPlane:
        ...
    @typing.overload
    def Circle(self, h: typing.SupportsFloat, v: typing.SupportsFloat, r: typing.SupportsFloat) -> WorkPlane:
        """
        draw circle with center (h,v) and radius 'r'
        """
    @typing.overload
    def Circle(self, r: typing.SupportsFloat) -> WorkPlane:
        """
        draw circle with center in current position
        """
    def Close(self, name: str | None = None) -> WorkPlane:
        """
        draw line to start point of wire, and finish wire
        """
    def Direction(self, dirh: typing.SupportsFloat, dirv: typing.SupportsFloat) -> WorkPlane:
        """
        reset direction to (dirh, dirv)
        """
    def Ellipse(self, major: typing.SupportsFloat, minor: typing.SupportsFloat) -> WorkPlane:
        """
        draw ellipse with current position as center
        """
    def Face(self) -> Face:
        """
        generate and return face of all wires, resets list of wires
        """
    def Finish(self) -> WorkPlane:
        """
        finish current wire without closing
        """
    def Last(self) -> netgen.libngpy._NgOCC.Wire | None:
        """
        (deprecated) returns current wire
        """
    @typing.overload
    def Line(self, l: typing.SupportsFloat, name: str | None = None) -> WorkPlane:
        ...
    @typing.overload
    def Line(self, dx: typing.SupportsFloat, dy: typing.SupportsFloat, name: str | None = None) -> WorkPlane:
        ...
    def LineTo(self, h: typing.SupportsFloat, v: typing.SupportsFloat, name: str | None = None) -> WorkPlane:
        """
        draw line to position (h,v)
        """
    def Move(self, l: typing.SupportsFloat) -> WorkPlane:
        """
        move 'l' from current position and direction, start new wire
        """
    def MoveTo(self, h: typing.SupportsFloat, v: typing.SupportsFloat) -> WorkPlane:
        """
        moveto (h,v), and start new wire
        """
    def NameVertex(self, name: str) -> WorkPlane:
        """
        name vertex at current position
        """
    def Offset(self, d: typing.SupportsFloat) -> WorkPlane:
        """
        replace current wire by offset curve of distance 'd'
        """
    def Rectangle(self, l: typing.SupportsFloat, w: typing.SupportsFloat, name: str | None = None) -> WorkPlane:
        """
        draw rectangle, with current position as corner, use current direction
        """
    def RectangleC(self, l: typing.SupportsFloat, w: typing.SupportsFloat, name: str | None = None) -> WorkPlane:
        """
        draw rectangle, with current position as center, use current direction
        """
    def Reverse(self) -> WorkPlane:
        """
        revert orientation of current wire
        """
    def Rotate(self, ang: typing.SupportsFloat) -> WorkPlane:
        """
        rotate current direction by 'ang' degrees
        """
    def Spline(self, points: collections.abc.Sequence[gp_Pnt2d], periodic: bool = False, tol: typing.SupportsFloat = 1e-08, tangents: collections.abc.Mapping[typing.SupportsInt, gp_Vec2d] = {}, start_from_localpos: bool = True, name: str | None = None) -> WorkPlane:
        """
        draw spline (default: starting from current position, which is implicitly added to given list of points), tangents can be specified for each point (0 refers to starting point)
        """
    def Wire(self) -> netgen.libngpy._NgOCC.Wire | None:
        """
        returns current wire
        """
    def Wires(self) -> ListOfShapes:
        """
        returns all wires
        """
    def __init__(self, axes: Axes = ..., pos: gp_Ax2d = ...) -> None:
        ...
    @property
    def cur_dir(self) -> gp_Vec2d:
        ...
    @property
    def cur_loc(self) -> gp_Pnt2d:
        ...
    @property
    def start_pnt(self) -> gp_Pnt2d:
        ...
class gp_Ax2:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, arg0: gp_Pnt, arg1: gp_Dir) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: gp_Ax3) -> None:
        ...
class gp_Ax2d:
    """
    2d OCC coordinate system
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, p: gp_Pnt2d = (0, 0), d: gp_Dir2d = ...) -> None:
        ...
class gp_Dir:
    """
    3d OCC direction
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, arg0: typing.SupportsInt) -> float:
        ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: gp_Vec) -> None:
        ...
    def __str__(self) -> str:
        ...
class gp_Dir2d:
    """
    2d OCC direction
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat) -> None:
        ...
class gp_GTrsf:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, arg0: TopoDS_Shape) -> TopoDS_Shape:
        ...
    def __init__(self, mat: collections.abc.Sequence[typing.SupportsFloat], vec: collections.abc.Sequence[typing.SupportsFloat] = [0.0, 0.0, 0.0]) -> None:
        ...
class gp_Mat:
    """
    3d OCC matrix
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, arg0: tuple[typing.SupportsInt, typing.SupportsInt]) -> float:
        ...
class gp_Pnt:
    """
    3d OCC point
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __add__(self, arg0: gp_Vec) -> gp_Pnt:
        ...
    def __getitem__(self, arg0: typing.SupportsInt) -> float:
        ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, arg0: gp_Pnt) -> gp_Vec:
        ...
    @typing.overload
    def __sub__(self, arg0: gp_Vec) -> gp_Pnt:
        ...
    @property
    def x(self) -> float:
        ...
    @x.setter
    def x(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def y(self) -> float:
        ...
    @y.setter
    def y(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def z(self) -> float:
        ...
    @z.setter
    def z(self, arg1: typing.SupportsFloat) -> None:
        ...
class gp_Pnt2d:
    """
    2d OCC point
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __add__(self, arg0: gp_Vec2d) -> gp_Pnt2d:
        ...
    @typing.overload
    def __init__(self, arg0: tuple[typing.SupportsFloat, typing.SupportsFloat]) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, arg0: gp_Pnt2d) -> gp_Vec2d:
        ...
    @typing.overload
    def __sub__(self, arg0: gp_Vec2d) -> gp_Pnt2d:
        ...
    @property
    def x(self) -> float:
        ...
    @x.setter
    def x(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def y(self) -> float:
        ...
    @y.setter
    def y(self, arg1: typing.SupportsFloat) -> None:
        ...
class gp_Trsf:
    @staticmethod
    def Mirror(arg0: Axis) -> gp_Trsf:
        ...
    @staticmethod
    @typing.overload
    def Rotation(arg0: Axis, arg1: typing.SupportsFloat) -> gp_Trsf:
        ...
    @staticmethod
    @typing.overload
    def Rotation(arg0: gp_Pnt, arg1: gp_Dir, arg2: typing.SupportsFloat) -> gp_Trsf:
        ...
    @staticmethod
    def Scale(arg0: gp_Pnt, arg1: typing.SupportsFloat) -> gp_Trsf:
        ...
    @staticmethod
    @typing.overload
    def Transformation(arg0: Axes) -> gp_Trsf:
        ...
    @staticmethod
    @typing.overload
    def Transformation(arg0: Axes, arg1: Axes) -> gp_Trsf:
        ...
    @staticmethod
    def Translation(arg0: gp_Vec) -> gp_Trsf:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Inverted(self) -> gp_Trsf:
        ...
    def SetMirror(self, arg0: Axis) -> gp_Trsf:
        ...
    def __call__(self, arg0: TopoDS_Shape) -> TopoDS_Shape:
        ...
    def __init__(self) -> None:
        ...
    def __mul__(self, arg0: gp_Trsf) -> gp_Trsf:
        ...
    def __str__(self) -> str:
        ...
class gp_Vec:
    """
    3d OCC vector
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Norm(self) -> float:
        ...
    def __add__(self, arg0: gp_Vec) -> gp_Vec:
        ...
    def __ge__(self, arg0: typing.SupportsFloat) -> ...:
        ...
    def __gt__(self, arg0: typing.SupportsFloat) -> ...:
        ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: gp_Dir) -> None:
        ...
    def __le__(self, arg0: typing.SupportsFloat) -> ...:
        ...
    def __lt__(self, arg0: typing.SupportsFloat) -> ...:
        ...
    def __mul__(self, arg0: gp_Vec) -> float:
        ...
    def __neg__(self) -> gp_Vec:
        ...
    def __repr__(self) -> str:
        ...
    def __rmul__(self, arg0: typing.SupportsFloat) -> gp_Vec:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: gp_Vec) -> gp_Vec:
        ...
    def __xor__(self, arg0: gp_Vec) -> gp_Vec:
        ...
    @property
    def x(self) -> float:
        ...
    @x.setter
    def x(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def y(self) -> float:
        ...
    @y.setter
    def y(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def z(self) -> float:
        ...
    @z.setter
    def z(self, arg1: typing.SupportsFloat) -> None:
        ...
class gp_Vec2d:
    """
    2d OCC vector
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __add__(self, arg0: gp_Vec2d) -> gp_Vec2d:
        ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat) -> None:
        ...
    def __neg__(self) -> gp_Vec2d:
        ...
    def __repr__(self: gp_Vec) -> str:
        ...
    def __rmul__(self, arg0: typing.SupportsFloat) -> gp_Vec2d:
        ...
    def __str__(self: gp_Vec) -> str:
        ...
    def __sub__(self, arg0: gp_Vec2d) -> gp_Vec2d:
        ...
    def __xor__(self, arg0: gp_Vec2d) -> float:
        ...
    @property
    def x(self) -> float:
        ...
    @x.setter
    def x(self, arg1: typing.SupportsFloat) -> None:
        ...
    @property
    def y(self) -> float:
        ...
    @y.setter
    def y(self, arg1: typing.SupportsFloat) -> None:
        ...
@typing.overload
def ArcOfCircle(p1: gp_Pnt, p2: gp_Pnt, p3: gp_Pnt) -> Edge:
    """
    create arc from p1 through p2 to p3
    """
@typing.overload
def ArcOfCircle(p1: gp_Pnt, v: gp_Vec, p2: gp_Pnt) -> Edge:
    """
    create arc from p1, with tangent vector v, to point p2
    """
def BSplineCurve(arg0: collections.abc.Sequence[gp_Pnt], arg1: typing.SupportsInt) -> Edge:
    ...
def BezierCurve(points: collections.abc.Sequence[gp_Pnt]) -> Edge:
    """
    create Bezier curve
    """
def BezierSurface(poles: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], weights: typing.Annotated[numpy.typing.ArrayLike, numpy.float64] | None = None, tol: typing.SupportsFloat = 1e-07) -> Face:
    """
    Creates a rational Bezier surface with the set of poles and the set of weights. The weights are defaulted to all being 1. If all the weights are identical the surface is considered as non rational. Raises ConstructionError if the number of poles in any direction is greater than MaxDegree + 1 or lower than 2 or CurvePoles and CurveWeights have not the same length or one weight value is lower or equal to Resolution. Returns an occ face with the given tolerance.
    """
def Box(p1: gp_Pnt, p2: gp_Pnt) -> Solid:
    """
    create box with opposite points 'p1' and 'p2'
    """
@typing.overload
def Circle(c: gp_Pnt2d, r: typing.SupportsFloat) -> Geom2d_Curve:
    """
    create 2d circle curve
    """
@typing.overload
def Circle(arg0: gp_Pnt, arg1: gp_Dir, arg2: typing.SupportsFloat) -> Edge:
    ...
def Cone(axis: gp_Ax2, r1: typing.SupportsFloat, r2: typing.SupportsFloat, h: typing.SupportsFloat, angle: typing.SupportsFloat) -> Solid:
    """
    create cone given by axis, radius at bottom (z=0) r1, radius at top (z=h) r2, height and angle
    """
def ConnectEdgesToWires(edges: collections.abc.Sequence[TopoDS_Shape], tol: typing.SupportsFloat = 1e-08, shared: bool = True) -> list[Wire]:
    ...
@typing.overload
def Cylinder(p: gp_Pnt, d: gp_Dir, r: typing.SupportsFloat, h: typing.SupportsFloat, bottom: str | None = None, top: str | None = None, mantle: str | None = None) -> typing.Any:
    """
    create cylinder with base point 'p', axis direction 'd', radius 'r', and height 'h'
    """
@typing.overload
def Cylinder(axis: gp_Ax2, r: typing.SupportsFloat, h: typing.SupportsFloat) -> Solid:
    """
    create cylinder given by axis, radius and height
    """
@typing.overload
def Dir(x: typing.SupportsFloat, y: typing.SupportsFloat) -> gp_Dir2d:
    """
    create 2d OCC direction
    """
@typing.overload
def Dir(x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> gp_Dir:
    """
    create 3d OCC direction
    """
@typing.overload
def Dir(d: collections.abc.Sequence[typing.SupportsFloat]) -> typing.Any:
    """
    create 2d or 3d OCC direction
    """
def Ellipse(axes: gp_Ax2d, major: typing.SupportsFloat, minor: typing.SupportsFloat) -> Geom2d_Curve:
    """
    create 2d ellipse curve
    """
def Ellipsoid(axes: Axes, r1: typing.SupportsFloat, r2: typing.SupportsFloat, r3: typing.SupportsFloat | None = None) -> TopoDS_Shape:
    """
    create ellipsoid with local coordinates given by axes, radi 'r1', 'r2', 'r3'
    """
def From_PyOCC(arg0: typing.Any) -> typing.Any:
    ...
def Fuse(arg0: collections.abc.Sequence[TopoDS_Shape]) -> TopoDS_Shape:
    ...
@typing.overload
def Glue(shapes: collections.abc.Sequence[TopoDS_Shape]) -> TopoDS_Shape:
    """
    glue together shapes of list
    """
@typing.overload
def Glue(shape: TopoDS_Shape) -> TopoDS_Shape:
    """
    glue together shapes from shape, typically a compound
    """
def HalfSpace(p: gp_Pnt, n: gp_Vec) -> TopoDS_Shape:
    """
    Create a half space threw point p normal to n
    """
def LoadOCCGeometry(arg0: os.PathLike | str | bytes) -> netgen.libngpy._meshing.NetgenGeometry:
    ...
def MakeFillet(arg0: TopoDS_Shape, arg1: collections.abc.Sequence[TopoDS_Shape], arg2: typing.SupportsFloat) -> TopoDS_Shape:
    """
    deprecated, use 'shape.MakeFillet'
    """
def MakePolygon(arg0: collections.abc.Sequence[Vertex]) -> Wire:
    ...
def MakeThickSolid(arg0: TopoDS_Shape, arg1: collections.abc.Sequence[TopoDS_Shape], arg2: typing.SupportsFloat, arg3: typing.SupportsFloat) -> TopoDS_Shape:
    """
    deprecated, use 'shape.MakeThickSolid'
    """
def Pipe(spine: Wire, profile: TopoDS_Shape, twist: tuple[gp_Pnt, typing.SupportsFloat] | None = None, auxspine: netgen.libngpy._NgOCC.Wire | None = None) -> TopoDS_Shape:
    ...
def PipeShell(spine: Wire, profile: netgen.libngpy._NgOCC.TopoDS_Shape | collections.abc.Sequence[TopoDS_Shape], auxspine: netgen.libngpy._NgOCC.Wire | None = None) -> TopoDS_Shape:
    ...
@typing.overload
def Pnt(x: typing.SupportsFloat, y: typing.SupportsFloat) -> gp_Pnt2d:
    """
    create 2d OCC point
    """
@typing.overload
def Pnt(x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> gp_Pnt:
    """
    create 3d OCC point
    """
@typing.overload
def Pnt(p: collections.abc.Sequence[typing.SupportsFloat]) -> typing.Any:
    """
    create 2d or 3d OCC point
    """
def Prism(face: TopoDS_Shape, v: gp_Vec) -> TopoDS_Shape:
    """
    extrude face along the vector 'v'
    """
def ResetGlobalShapeProperties() -> None:
    ...
def Revolve(arg0: TopoDS_Shape, arg1: Axis, arg2: typing.SupportsFloat) -> TopoDS_Shape:
    ...
@typing.overload
def Segment(p1: gp_Pnt2d, p2: gp_Pnt2d) -> Geom2d_Curve:
    """
    create 2d line curve
    """
@typing.overload
def Segment(arg0: gp_Pnt, arg1: gp_Pnt) -> Edge:
    ...
def Sew(faces: collections.abc.Sequence[TopoDS_Shape], tolerance: typing.SupportsFloat = 1e-06, non_manifold: bool = False) -> TopoDS_Shape:
    """
    Stitch a list of faces into one or more connected shells.
    
    Parameters
    ----------
    faces : list[TopoDS_Shape]
        Faces or other shapes to sew together.
    tolerance : float, default=1e-6
        Geometric tolerance for merging edges and vertices.
    non_manifold : bool, default=False
        If True, allows edges shared by more than two faces (may produce
        multiple shells). If False, creates only manifold shells suitable
        for solids.
    
    Returns
    -------
    TopoDS_Shape
        The sewed shape containing one or more shells.
    """
def Sphere(c: gp_Pnt, r: typing.SupportsFloat) -> Solid:
    """
    create sphere with center 'c' and radius 'r'
    """
@typing.overload
def SplineApproximation(points: collections.abc.Sequence[gp_Pnt2d], approx_type: ApproxParamType = ..., deg_min: typing.SupportsInt = 3, deg_max: typing.SupportsInt = 8, continuity: ShapeContinuity = ..., tol: typing.SupportsFloat = 1e-08) -> Geom2d_Curve:
    """
    Generate a piecewise continuous spline-curve approximating a list of points in 2d.
    
    Parameters
    ----------
    
    points : List|Tuple[gp_Pnt2d]
      List (or tuple) of gp_Pnt.
    
    approx_type : ApproxParamType
      Assumption on location of parameters wrt points.
    
    deg_min : int
      Minimum polynomial degree of splines
    
    deg_max : int
      Maximum polynomial degree of splines
    
    continuity : ShapeContinuity
      Continuity requirement on the approximating surface
    
    tol : float
      Tolerance for the distance from individual points to the approximating curve.
    """
@typing.overload
def SplineApproximation(points: collections.abc.Sequence[gp_Pnt], approx_type: ApproxParamType = ..., deg_min: typing.SupportsInt = 3, deg_max: typing.SupportsInt = 8, continuity: ShapeContinuity = ..., tol: typing.SupportsFloat = 1e-08) -> Edge:
    """
    Generate a piecewise continuous spline-curve approximating a list of points in 3d.
    
    Parameters
    ----------
    
    points : List[gp_Pnt] or Tuple[gp_Pnt]
      List (or tuple) of gp_Pnt.
    
    approx_type : ApproxParamType
      Assumption on location of parameters wrt points.
    
    deg_min : int
      Minimum polynomial degree of splines
    
    deg_max : int
      Maximum polynomial degree of splines
    
    continuity : ShapeContinuity
      Continuity requirement on the approximating surface
    
    tol : float
      Tolerance for the distance from individual points to the approximating curve.
    """
@typing.overload
def SplineInterpolation(points: collections.abc.Sequence[gp_Pnt2d], periodic: bool = False, tol: typing.SupportsFloat = 1e-08, tangents: collections.abc.Mapping[typing.SupportsInt, gp_Vec2d] = {}) -> Geom2d_Curve:
    """
    Generate a piecewise continuous spline-curve interpolating a list of points in 2d.
    
    Parameters
    ----------
    
    points : List|Tuple[gp_Pnt2d]
      List (or tuple) of gp_Pnt2d.
    
    periodic : bool
      Whether the result should be periodic
    
    tol : float
      Tolerance for the distance between points.
    
    tangents : Dict[int, gp_Vec2d]
      Tangent vectors for the points indicated by the key value (0-based).
    """
@typing.overload
def SplineInterpolation(points: collections.abc.Sequence[gp_Pnt], periodic: bool = False, tol: typing.SupportsFloat = 1e-08, tangents: collections.abc.Mapping[typing.SupportsInt, gp_Vec] = {}) -> Edge:
    """
    Generate a piecewise continuous spline-curve interpolating a list of points in 3d.
    
    Parameters
    ----------
    
    points : List|Tuple[gp_Pnt]
      List (or tuple) of gp_Pnt
    
    periodic : bool
      Whether the result should be periodic
    
    tol : float
      Tolerance for the distance between points.
    
    tangents : Dict[int, gp_Vec]
      Tangent vectors for the points indicated by the key value (0-based).
    """
def SplineSurfaceApproximation(points: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], approx_type: ApproxParamType = ..., deg_min: typing.SupportsInt = 3, deg_max: typing.SupportsInt = 8, continuity: ShapeContinuity = ..., tol: typing.SupportsFloat = 0.001, periodic: bool = False, degen_tol: typing.SupportsFloat = 1e-08) -> Face:
    """
    Generate a piecewise continuous spline-surface approximating an array of points.
    
    Parameters
    ----------
    
    points : np.ndarray
      Array of points coordinates. The first dimension corresponds to the first surface coordinate point
      index, the second dimension to the second surface coordinate point index. The third dimension refers to physical
      coordinates. Such an array can be generated with code like::
    
          px, py = np.meshgrid(*[np.linspace(0, 1, N)]*2)
          points = np.array([[(px[i,j], py[i,j], px[i,j]*py[i,j]**2) for j in range(N)] for i in range(N)])
    
    approx_type : ApproxParamType
      Assumption on location of parameters wrt points.
    
    deg_min : int
      Minimum polynomial degree of splines
    
    deg_max : int
      Maximum polynomial degree of splines
    
    continuity : ShapeContinuity
      Continuity requirement on the approximating surface
    
    tol : float
      Tolerance for the distance from individual points to the approximating surface.
    
    periodic : bool
      Whether the result should be periodic in the first surface parameter
    
    degen_tol : double
      Tolerance for resolution of degenerate edges
    """
def SplineSurfaceInterpolation(points: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], approx_type: ApproxParamType = ..., periodic: bool = False, degen_tol: typing.SupportsFloat = 1e-08) -> Face:
    """
    Generate a piecewise continuous spline-surface interpolating an array of points.
    
    Parameters
    ----------
    
    points : np.ndarray
      Array of points coordinates. The first dimension corresponds to the first surface coordinate point
      index, the second dimension to the second surface coordinate point index. The third dimension refers to physical
      coordinates. Such an array can be generated with code like::
    
          px, py = np.meshgrid(*[np.linspace(0, 1, N)]*2)
          points = np.array([[(px[i,j], py[i,j], px[i,j]*py[i,j]**2) for j in range(N)] for i in range(N)])
    
    approx_type : ApproxParamType
      Assumption on location of parameters wrt points.
    
    periodic : bool
      Whether the result should be periodic in the first surface parameter
    
    degen_tol : double
      Tolerance for resolution of degenerate edges
    """
def TestXCAF(shape: TopoDS_Shape = ...) -> None:
    ...
def ThruSections(wires: collections.abc.Sequence[TopoDS_Shape], solid: bool = True) -> TopoDS_Shape:
    """
    Building a loft. This is a shell or solid passing through a set of sections (wires). First and last sections may be vertices. See https://dev.opencascade.org/doc/refman/html/class_b_rep_offset_a_p_i___thru_sections.html#details
    """
@typing.overload
def Vec(x: typing.SupportsFloat, y: typing.SupportsFloat) -> gp_Vec2d:
    """
    create 2d OCC point
    """
@typing.overload
def Vec(x: typing.SupportsFloat, y: typing.SupportsFloat, z: typing.SupportsFloat) -> gp_Vec:
    """
    create 3d OCC point
    """
@typing.overload
def Vec(v: collections.abc.Sequence[typing.SupportsFloat]) -> typing.Any:
    """
    create 2d or 3d OCC vector
    """
COMPOUND: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.COMPOUND: 0>
COMPSOLID: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.COMPSOLID: 1>
EDGE: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.EDGE: 6>
FACE: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.FACE: 4>
SHAPE: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.SHAPE: 8>
SHELL: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.SHELL: 3>
SOLID: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.SOLID: 2>
VERTEX: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.VERTEX: 7>
WIRE: TopAbs_ShapeEnum  # value = <TopAbs_ShapeEnum.WIRE: 5>
X: gp_Vec  # value = (1, 0, 0)
Y: gp_Vec  # value = (0, 1, 0)
Z: gp_Vec  # value = (0, 0, 1)
occ_version: str = '7.8.1'
