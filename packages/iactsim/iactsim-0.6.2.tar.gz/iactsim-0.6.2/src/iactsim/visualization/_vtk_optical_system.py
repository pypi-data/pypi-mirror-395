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

import numpy as np
import vtk

from ._vtk_utils import (
    create_aspheric_surface_actor,
    create_cylindric_surface_actor,
    quit
)

from ..optics._surface_misc import SurfaceType, SurfaceShape

from ..optics._cpu_transforms import local_to_telescope_rotation

from .._iact import IACT

from ..optics._optical_system import OpticalSystem


class VTKOpticalSystem():
    """Class to viasualize the geometry of an optical system.
    Each surface actor can be accessed from :py:attr:`actors` attribute after a :py:meth:`update` call.

    Parameters
    ----------
    optical_system : OpticalSystem or IACT
        Optical sistem for which visualize surfaces.

    Notes
    -----
    If you perform some operation on an actor, make sure to call :py:meth:`start_render` with ``update=False``, otherwise the actors will be replaced.
    
    """
    def __init__(self, optical_system):
        self.actors = {}
        """Dictionary of surface name: surface actor."""

        if issubclass(type(optical_system), OpticalSystem):
            self.os = optical_system
            self._rotation_matrix = np.eye(3)
            self._translation_vector = np.zeros(3)
        elif issubclass(type(optical_system), IACT):
            self.os = optical_system.optical_system
            self._rotation_matrix = local_to_telescope_rotation(*optical_system.pointing)
            self._translation_vector = optical_system.position
        else:
            raise(ValueError("optical system must be an instance of OpticalSystem or IACT."))

        """Optical system to be visualized."""
        
        self._default_surface_color = (0.7, 0.7, 0.75)

        self.surface_type_colors = {
            SurfaceType.REFRACTIVE: (0.6, 0.4, 1),
            SurfaceType.OPAQUE: (1, 0.3, 0.3)
        }
        """Dictionary to custumize surface colors based on surface type."""

        # Wireframe
        self.wireframe = False
        """Whether to use wireframe representation by default."""

        # Window size
        self.window_size = (1024,1024)
        """Window size in pixel."""

        self.resolution = 10. # mm
        """Objects mesh resolution (in mm)."""

        self._update()

        self._apply_global_transform()
    
    def _update(self):
        """Generate all surface actors.
        """
        self.actors = {}
        for s in self.os:
            if s._shape == SurfaceShape.ASPHERICAL:
                
                actor = create_aspheric_surface_actor(s, self.resolution)
            else:
                actor = create_cylindric_surface_actor(s, self.resolution)

            transform = vtk.vtkTransform()
            transform.Translate(*s.position)
            R = s.get_rotation_matrix()
            vtk_rotation_matrix = vtk.vtkMatrix4x4()
            for i in range(3):
                for j in range(3):
                    vtk_rotation_matrix.SetElement(i, j, R[j, i])
            transform.PreMultiply()
            transform.Concatenate(vtk_rotation_matrix)
            transform.Update()
            actor.SetUserTransform(transform)
            
            if self.wireframe:
                actor.GetProperty().SetRepresentationToWireframe()
            
            if s.type in self.surface_type_colors:
                color = self.surface_type_colors[s.type]
            else:
                color = self._default_surface_color

            actor.GetProperty().SetColor(*color)
            actor.GetProperty().SetAmbient(0.3)
            actor.GetProperty().SetDiffuse(0.5)
            actor.GetProperty().SetSpecular(0.2)
            actor.GetProperty().SetSpecularPower(10)
        
            self.actors[s.name] = actor
    
    def start_render(self):
        """Render the optical system geometry on a VTK window.

        Parameters
        ----------
        update : bool, optional
            Regenerate surface actors, by default True.
            Make sure to not re-generate actors if you have modified them.
        
        """
        # Rendering
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(0.1, 0.15, 0.25)

        for actor in self.actors.values():
            renderer.AddActor(actor)

        # Display instructions
        desc = [
            "Press: 'q' to exit",
            "Press: 'r' to reset the camera",
            "Press: 'x', 'y' or 'z' to align the up-vector to the desired axis",
            "Press: 'w', 's' or 'p' to switch to wireframe, surface or points representation",
        ]
        textActor = vtk.vtkTextActor()
        textActor.SetInput('\n'.join(desc))
        position_coordinate = textActor.GetPositionCoordinate()
        position_coordinate.SetCoordinateSystemToNormalizedViewport()
        position_coordinate.SetValue(0.01, 0.99)
        textActor.GetTextProperty().SetJustificationToLeft()
        textActor.GetTextProperty().SetVerticalJustificationToTop()
        textActor.GetTextProperty().SetFontSize(14)
        textActor.GetTextProperty().SetColor(vtk.vtkNamedColors().GetColor3d("Gold"))
        textActor.GetTextProperty().SetFontFamily(vtk.VTK_COURIER)
        renderer.AddActor2D(textActor)

        render_window = vtk.vtkRenderWindow()
        render_window.SetWindowName(self.os.name)
        render_window.AddRenderer(renderer)
        render_window.SetSize(*self.window_size)
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        # Camera
        cam_style = vtk.vtkInteractorStyleTrackballCamera()
        render_window_interactor.SetInteractorStyle(cam_style)

        # Axes
        axes = vtk.vtkAxesActor()
        widget = vtk.vtkOrientationMarkerWidget()
        rgba = [0] * 4
        vtk.vtkNamedColors().GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(render_window_interactor)
        widget.SetEnabled(1)
        widget.InteractiveOn()

        
        def perform_view_reset(up_vector):
            active_camera = renderer.GetActiveCamera()
            if not active_camera:
                return

            # Normalize up_vector
            norm_up = np.sqrt(sum(x*x for x in up_vector))
            if norm_up == 0: return
            target_up = [x/norm_up for x in up_vector]

            # Get current view plane normal
            vpn = active_camera.GetViewPlaneNormal()
            
            # Compute dot product
            dot = sum(vpn[i] * target_up[i] for i in range(3))
            
            # If dot product is near 1 or -1, vectors are parallel.
            # We must move the camera to avoid this.
            if abs(dot) > 0.95:
                fp = active_camera.GetFocalPoint()
                dist = active_camera.GetDistance()
                
                # Move camera to a perpendicular axis based on target UP
                if abs(target_up[2]) > 0.9: 
                    # Up is Z -> Move camera to look from Y
                    active_camera.SetPosition(fp[0], fp[1] - dist, fp[2])
                elif abs(target_up[1]) > 0.9:
                    # Up is Y -> Move camera to look from X
                    active_camera.SetPosition(fp[0] - dist, fp[1], fp[2])
                else:
                    # Up is X -> Move camera to look from Z
                    active_camera.SetPosition(fp[0], fp[1], fp[2] + dist)

                # Re-center view on object
                renderer.ResetCamera()

            active_camera.SetViewUp(*up_vector)
            # Orthogonalize ensures Up and direction are strictly 90 degrees
            active_camera.OrthogonalizeViewUp() 
            render_window.Render()

        def key_press_callback(caller, event):
            interactor = caller
            key_sym = interactor.GetKeySym()
            if key_sym and key_sym.lower() in 'r':
                renderer.ResetCamera()
            elif key_sym and key_sym.lower() == 'y':
                perform_view_reset((0,1,0))
            elif key_sym and key_sym.lower() == 'x':
                perform_view_reset((1,0,0))
            elif key_sym and key_sym.lower() == 'z':
                perform_view_reset((0,0,1))
            elif key_sym and key_sym.lower() == 'w':
                for actor in renderer.actors:
                    actor.GetProperty().SetRepresentationToWireframe()
                render_window.Render()
            elif key_sym and key_sym.lower() == 's':
                for actor in renderer.actors:
                    actor.GetProperty().SetRepresentationToSurface()
                render_window.Render()
            elif key_sym and key_sym.lower() == 'p':
                for actor in renderer.actors:
                    actor.GetProperty().SetRepresentationToPoints()
                render_window.Render()
            elif key_sym and key_sym.lower() == 'q':
                    quit(render_window_interactor)

        priority = 0.0
        render_window_interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, key_press_callback, priority)

        # Start
        render_window.Render()
        renderer.ResetCamera()
        render_window.Render()
        render_window_interactor.Initialize()
        render_window_interactor.Start()

        # Stop
        quit(render_window_interactor)

    def add_rays(self, start, stop, directions=None, length=None, opacity=0.5, point_size=1.0, show_rays=True, show_hits=True):
        """
        Draw rays from start to stop positions and highlight stop points.
        
        If a stop position is NaN (indicating a miss), the ray is skipped by default.
        If 'length' and 'directions' are provided, rays with NaN stops are drawn 
        starting from 'start' along 'direction' for 'length' units (without a hit dot).
        
        Parameters
        ----------
        start : ndarray
            (n, 3) array of starting coordinates (x, y, z).
        stop : ndarray
            (n, 3) array of stopping coordinates (x, y, z).
        directions : ndarray, optional
            (n, 3) array of direction vectors. Required if plotting NaN rays with fixed length.
        length : float, optional
            If provided, rays with NaN stop will be drawn with this length using the direction vector.
        opacity : float, optional
            Transparency of the rays from 0.0 (invisible) to 1.0 (opaque). Default is 0.5.
        point_size : float, optional
            Size of the hit points. Default is 1.0
        show_rays : bool, optional
            Whether to show rays or not. Default is True.
        show_hits : bool, optional
            Whether to show hits or not. Default is True.
        """

        if not show_hits and not show_rays:
            return
        
        # Rays
        points_rays = vtk.vtkPoints()
        lines_rays = vtk.vtkCellArray()
        
        # Hits
        points_dots = vtk.vtkPoints()
        verts_dots = vtk.vtkCellArray()
        
        n = start.shape[0]
        has_directions = directions is not None

        if start.shape != stop.shape or (has_directions and start.shape != directions.shape):
            raise ValueError("Start,  stop and directions must have the same shape.")

        # Check which rays have intersected a surface
        valid_stops = ~np.any(np.isnan(stop), axis=1)
        
        for i in range(n):
            current_start = start[i]
            current_stop = stop[i]
            
            is_valid_stop = valid_stops[i]
            
            final_stop = None
            draw_hit = False
            if is_valid_stop:
                # Draw from start to stop and add a hit
                final_stop = current_stop
                draw_hit = True
            elif length is not None and has_directions:
                # Draw fixed length ray if directions are available
                final_stop = current_start + directions[i] * length
                draw_hit = False
            else:
                # Ignore not intersected ray
                continue

            ## Ray logic
            id_start = points_rays.InsertNextPoint(current_start)
            id_stop_line = points_rays.InsertNextPoint(final_stop)
            
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, id_start)
            line.GetPointIds().SetId(1, id_stop_line)
            lines_rays.InsertNextCell(line)
            
            ## Hit logic
            if draw_hit:
                id_stop_dot = points_dots.InsertNextPoint(final_stop)
                verts_dots.InsertNextCell(1)
                verts_dots.InsertCellPoint(id_stop_dot)
            
        ## Rays actor
        if show_rays:
            raysPolyData = vtk.vtkPolyData()
            raysPolyData.SetPoints(points_rays)
            raysPolyData.SetLines(lines_rays)
            
            mapper_rays = vtk.vtkPolyDataMapper()
            mapper_rays.SetInputData(raysPolyData)
            
            actor_rays = vtk.vtkActor()
            actor_rays.SetMapper(mapper_rays)
            
            actor_rays.GetProperty().SetColor(0.0, 0.7, 1.0) # Electric blue
            actor_rays.GetProperty().SetLineWidth(1.0)
            actor_rays.GetProperty().SetOpacity(float(opacity))
            
            self.actors['rays_lines'] = actor_rays # Add rays to te actors list

        ## Hits actor
        if points_dots.GetNumberOfPoints() > 0 and show_hits:
            dotsPolyData = vtk.vtkPolyData()
            dotsPolyData.SetPoints(points_dots)
            dotsPolyData.SetVerts(verts_dots)
            
            mapper_dots = vtk.vtkPolyDataMapper()
            mapper_dots.SetInputData(dotsPolyData)
            
            actor_dots = vtk.vtkActor()
            actor_dots.SetMapper(mapper_dots)
            actor_dots.GetProperty().SetColor(1.0, 1.0, 0.0) # Yellow
            
            actor_dots.GetProperty().SetPointSize(point_size) 
            actor_dots.GetProperty().SetOpacity(1.0)
            
            self.actors['rays_dots'] = actor_dots

    def _apply_global_transform(self):
        """
        Apply a global rotation and translation to all current actors.
        
        Parameters
        ----------
        R : ndarray
            (3, 3) Rotation matrix. 
        t : ndarray or list
            (3,) Translation vector (x, y, z).
        """
        # Convert numpy array to vtkMatrix4x4
        vtk_R = vtk.vtkMatrix4x4()
        for i in range(3):
            for j in range(3):
                vtk_R.SetElement(i, j, self._rotation_matrix[i, j])

        # Iterate over all actors
        for actor in self.actors.values():
            
            # Get the existing transform
            transform = actor.GetUserTransform()
            if transform is None:
                transform = vtk.vtkTransform()
                transform.SetMatrix(actor.GetMatrix())
                actor.SetUserTransform(transform)
            
            # Apply transformations
            # PostMultiply ensures we are applying this to the "Global" world coordinates
            transform.PostMultiply()
            
            # Apply rotation
            transform.Concatenate(vtk_R)
            
            # Apply translation
            transform.Translate(*self._translation_vector)