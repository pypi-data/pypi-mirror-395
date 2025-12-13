# Copyright (C) 2024- Davide Mollica <davide.mollica@inaf.it>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of iactsim.
#
# iactsim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iactsim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iactsim.  If not, see <https://www.gnu.org/licenses/>.

import vtk
import math
import numpy as np

from ..optics._surface_misc import ApertureShape

def hexagonal_clipping(half_aperture, offset, structuredGrid, inside, input_connection=None):
    """Clip an hexagonal aspheric surface.

    Parameters
    ----------
    half_aperture : float
        Surface half aperture.
    offset : float, float
        Segment offset.
    structuredGrid : vtk.StructuredGrid
        The surface to clip.
    inside : bool
        Whether to keep the surface inside or outside the half aperture.
    input_connection : vtkClipDataSet, optional
        Apply the clipping to another clipped surface, by default None.

    Returns
    -------
    vtkClipDataSet
        Clipped surface.
    """
    hex_apothem = half_aperture
    booleanOp = vtk.vtkImplicitBoolean()
    booleanOp.SetOperationTypeToIntersection()
    num_sides = 6
    angle_step = 2.0 * math.pi / num_sides
    for i in range(num_sides):
        angle = i * angle_step + 0.5*angle_step
        nx_plane, ny_plane = math.cos(angle), math.sin(angle)
        ox_plane, oy_plane = hex_apothem * nx_plane, hex_apothem * ny_plane
        plane = vtk.vtkPlane()
        plane.SetOrigin(ox_plane+offset[0], oy_plane+offset[1], 0.0)
        plane.SetNormal(nx_plane, ny_plane, 0.0)
        booleanOp.AddFunction(plane)
    
    clipper = vtk.vtkClipDataSet()
    if input_connection is None:
        clipper.SetInputData(structuredGrid)
    else:
        clipper.SetInputConnection(input_connection.GetOutputPort())
    clipper.SetClipFunction(booleanOp)
    clipper.SetInsideOut(inside)
    clipper.SetValue(0.0)
    clipper.Update()
    return clipper

def square_clipping(half_aperture, offset, structuredGrid, inside, input_connection=None):
    """Clip a square aspheric surface.

    Parameters
    ----------
    half_aperture : float
        Surface half aperture.
    offset : float, float
        Segment offset.
    structuredGrid : vtk.StructuredGrid
        The surface to clip.
    inside : bool
        Whether to keep the surface inside or outside the half aperture.
    input_connection : vtkClipDataSet, optional
        Apply the clipping to another clipped surface, by default None.

    Returns
    -------
    vtkClipDataSet
        Clipped surface.
    """
    hex_apothem = half_aperture
    booleanOp = vtk.vtkImplicitBoolean()
    booleanOp.SetOperationTypeToIntersection()
    num_sides = 4
    angle_step = 2.0 * math.pi / num_sides
    for i in range(num_sides):
        angle = i * angle_step + angle_step
        nx_plane, ny_plane = math.cos(angle), math.sin(angle)
        ox_plane, oy_plane = hex_apothem * nx_plane, hex_apothem * ny_plane
        plane = vtk.vtkPlane()
        plane.SetOrigin(ox_plane+offset[0], oy_plane+offset[1], 0.0)
        plane.SetNormal(nx_plane, ny_plane, 0.0)
        booleanOp.AddFunction(plane)
    
    clipper = vtk.vtkClipDataSet()
    if input_connection is None:
        clipper.SetInputData(structuredGrid)
    else:
        clipper.SetInputConnection(input_connection.GetOutputPort())
    clipper.SetClipFunction(booleanOp)
    clipper.SetInsideOut(inside)
    clipper.SetValue(0.0)
    clipper.Update()
    return clipper

def circular_clipping(half_aperture, offset, structuredGrid, inside, input_connection=None):
    """Clip a circular aspheric surface.

    Parameters
    ----------
    half_aperture : float
        Surface half aperture.
    offset : float, float
        Segment offset.
    structuredGrid : vtk.StructuredGrid
        The surface to clip.
    inside : bool
        Whether to keep the surface inside or outside the half aperture.
    input_connection : vtkClipDataSet, optional
        Apply the clipping to another clipped surface, by default None.

    Returns
    -------
    vtkClipDataSet
        Clipped surface.
    """

    # Aperture clipping
    cylinder = vtk.vtkCylinder()
    cylinder.SetCenter(offset[0], offset[1], 0.0)
    cylinder.SetAxis(0.0, 0.0, 1.0)
    cylinder.SetRadius(half_aperture)

    # Create the clipper filter
    clipper = vtk.vtkClipDataSet()
    if input_connection is None:
        clipper.SetInputData(structuredGrid)
    else:
        clipper.SetInputConnection(input_connection.GetOutputPort())
    clipper.SetClipFunction(cylinder)
    clipper.SetInsideOut(inside)
    clipper.SetValue(0.0)
    clipper.GenerateClippedOutputOn()
    clipper.Update()
    return clipper

def create_aspheric_surface_actor(surface, res=None):
    """Create an actor for an aspheric surface.

    Parameters
    ----------
    surface : iactsim.optics.AsphericSurface
        The optical surface.
    res : float, optional
        Mesh resolution in mm, by default 10 mm.

    Returns
    -------
    vtkActor
        The surface actor.
    """
    if res is None:
        res = 10
    r_max = surface.half_aperture
    
    if surface.aperture_shape == ApertureShape.HEXAGONAL:
        r_max *= 1.1547
    
    if surface.aperture_shape == ApertureShape.SQUARE:
        r_max *= 1.4142
    
    # Meshgrid
    n = int(r_max/res)
    x_coords = np.linspace(surface.offset[0]-r_max, surface.offset[0]+r_max, n)
    y_coords = np.linspace(surface.offset[1]-r_max, surface.offset[1]+r_max, n)
    X, Y = np.meshgrid(x_coords, y_coords, indexing='xy')

    # Radius
    R = np.sqrt(X**2 + Y**2)

    # Z coordinates
    Z = surface.sagitta(R)

    # Populate vtkStructuredGrid
    points = vtk.vtkPoints()
    for j in range(n):
        for i in range(n):
            points.InsertNextPoint(X[j, i], Y[j, i], Z[j, i])
    structuredGrid = vtk.vtkStructuredGrid()
    structuredGrid.SetDimensions(n, n, 1)
    structuredGrid.SetPoints(points)

    if surface.aperture_shape == ApertureShape.HEXAGONAL:
        clipper = hexagonal_clipping(surface.half_aperture, surface.offset, structuredGrid, True)
    elif surface.aperture_shape == ApertureShape.CIRCULAR:
        clipper = circular_clipping(surface.half_aperture, surface.offset, structuredGrid, True)
    elif surface.aperture_shape == ApertureShape.SQUARE:
        clipper = square_clipping(surface.half_aperture, surface.offset, structuredGrid, True)
    else:
        raise(RuntimeError(f"Aperture shape '{surface.aperture_shape}' not supported."))

    if surface.central_hole_shape == ApertureShape.HEXAGONAL:
        clipper = hexagonal_clipping(surface.central_hole_half_aperture, surface.offset, structuredGrid, False, clipper)
    elif surface.central_hole_shape == ApertureShape.CIRCULAR:
        clipper = circular_clipping(surface.central_hole_half_aperture, surface.offset, structuredGrid, False, clipper)
    elif surface.central_hole_shape == ApertureShape.SQUARE:
        clipper = square_clipping(surface.central_hole_half_aperture, surface.offset, structuredGrid, False, clipper)
    else:
        raise(RuntimeError(f"Aperture shape '{surface.aperture_shape}' not supported."))
    
    transform_off = vtk.vtkTransform()
    transform_off.Translate(-surface.offset[0],-surface.offset[1],-surface.sagitta(math.sqrt(surface.offset[0]**2+surface.offset[1]**2)))
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetInputConnection(clipper.GetOutputPort())
    transformFilter.SetTransform(transform_off)
    transformFilter.Update()
    
    # Add Scalar Data
    # scalars = vtk.vtkDoubleArray()
    # scalars.SetName("Radius")
    # scalars.SetNumberOfTuples(nx * ny)
    # k = 0
    # for j in range(ny):
    #     for i in range(nx):
    #         scalars.SetValue(k, R[j,i])
    #         k += 1
    # structuredGrid.GetPointData().SetScalars(scalars)

    # # The output of the clipper is a vtkUnstructuredGrid
    # clipped_output = clipper.GetOutput()

    mapper = vtk.vtkDataSetMapper()
    if clipper is None:
        mapper.SetInputData(structuredGrid)
    else:
        # mapper.SetInputConnection(clipper.GetOutputPort())
        mapper.SetInputConnection(transformFilter.GetOutputPort())
    
    mapper.ScalarVisibilityOff()
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

def create_cylindric_surface_actor(surface, res=None):
    """create a VTK actor for a cylindrical surface.

    Parameters
    ----------
    surface : CylindricalSurface
        A cylindrical surface.
    res : float, optional
        Resolution (in mm) used to compute the number of facets, 60 facets are used.

    Returns
    -------
    vtk.vtkActor
        Actor representing the cylinder.
    """
    capping = surface.top and surface.bottom
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetCenter(0, 0, 0)
    cylinder.SetRadius(surface.radius)
    cylinder.SetHeight(surface.height)
    if res is not None:
        res = int(2*np.pi / (2*np.arcsin(res/2/surface.radius)))
    else:
        res = 60
    cylinder.SetResolution(res)
    cylinder.SetCapping(capping)
    cylinder.Update()

    appendFilter = None
    if surface.top != surface.bottom:
        capDisk = vtk.vtkDiskSource()
        capDisk.SetInnerRadius(0.0)
        capDisk.SetOuterRadius(cylinder.radius)
        capDisk.SetCircumferentialResolution(cylinder.resolution)
        capDisk.Update()
        transform_cap = vtk.vtkTransform()
        if surface.top:
            z = 0.5*cylinder.height
        else:
            z = -0.5*cylinder.height
        transform_cap.Translate(0, z, 0)
        transform_cap.RotateX(-90)
        transform_cap.Update()
        
        transform_filter_cap = vtk.vtkTransformPolyDataFilter()
        transform_filter_cap.SetInputConnection(capDisk.GetOutputPort())
        transform_filter_cap.SetTransform(transform_cap)
        transform_filter_cap.Update()

        appendFilter = vtk.vtkAppendPolyData()
        appendFilter.AddInputConnection(cylinder.GetOutputPort())
        appendFilter.AddInputConnection(transform_filter_cap.GetOutputPort())
        appendFilter.Update()
    
    transform_cyl = vtk.vtkTransform()
    transform_cyl.RotateX(90)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    if appendFilter is None:
        transformFilter.SetInputConnection(cylinder.GetOutputPort())
    else:
        transformFilter.SetInputConnection(appendFilter.GetOutputPort())
    transformFilter.SetTransform(transform_cyl)
    transformFilter.Update()
    
    cylinderMapper = vtk.vtkPolyDataMapper()
    cylinderMapper.SetInputData(transformFilter.GetOutput())
    
    actor = vtk.vtkActor()
    actor.SetMapper(cylinderMapper)
    
    return actor

def quit(render_window_interactor):
    render_window = render_window_interactor.GetRenderWindow()
    render_window.Finalize()
    render_window_interactor.TerminateApp()