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

from ._vtk_utils import (
    create_aspheric_surface_actor,
    create_cylindric_surface_actor,
    quit
)

from ..optics._surface_misc import SurfaceType, SurfaceShape

class VTKOpticalSystem():
    """Class to viasualize the geometry of an optical system.
    Each surface actor can be accessed from :py:attr:`actors` attribute after a :py:meth:`update` call.

    Parameters
    ----------
    optical_system : OpticalSystem
        Optical sistem for which visualize surfaces.

    Notes
    -----
    If you perform some operation on an actor, make sure to call :py:meth:`start_render` with ``update=False``, otherwise the actors will be replaced.
    
    """
    def __init__(self, optical_system):
        self.actors = {}
        """Dictionary of surface name: surface actor."""

        self.os = optical_system
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
    
    def update(self):
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
    
    def start_render(self, update=True):
        """Render the optical system geometry on a VTK window.

        Parameters
        ----------
        update : bool, optional
            Regenerate surface actors, by default True.
            Make sure to not re-generate actors if you have modified them.
        
        """
        if update:
            self.update()

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
            if active_camera:
                active_camera.SetViewUp(*up_vector)
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