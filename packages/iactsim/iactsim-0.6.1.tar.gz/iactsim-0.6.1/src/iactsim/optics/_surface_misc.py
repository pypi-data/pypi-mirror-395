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

from dataclasses import dataclass, field
from enum import Enum
import numpy as np

from ..visualization._iactsim_style import iactsim_style, MplInteractiveContext

class SurfaceType(Enum):
    """
    Enumeration representing the different types of optical surfaces.

    The directionality of reflection and sensitivity (e.g., "from above" or 
    "from below") is defined within the *local reference frame* of the surface at the point 
    of photon incidence. As a reference:

        - the front side of a surface with negative curvature is the convex side.
        - the front side of a surface with posistive curvature is the concave side.

    Attributes
    ----------
    REFLECTIVE : int
        Represents a reflective surface (both sides).
    REFLECTIVE_IN : int
        Represents a surface that is reflective on the front side. 
        In the surface's local reference frame, only photons arriving with a negative 
        z-component of their direction vector (i.e., coming "from the front", or 
        "from above" in the context of the local frame) are reflected. 
        The curvature of the surface does not affect this behavior.
    REFLECTIVE_OUT : int
        Represents a surface that is reflective on the back side. In the surface's 
        local reference frame, only photons arriving with a positive z-component of 
        their direction vector (i.e., coming "from the back", or "from below" in the 
        context of the local frame) are reflected. The curvature of the surface 
        does not affect this behavior.
    REFRACTIVE : int
        Represents a refractive surface. The refraction is the same on both sides.
    SENSITIVE : int
        Represents the focal plane surface where photons are detected. The sensitivity
        is the same on both sides.
    SENSITIVE_IN : int
        Represents a surface that is sensitive on the front side (as defined by the 
        local reference frame's positive z-axis). In the surface's local reference 
        frame, only photons arriving with a negative z-component of their direction 
        vector (i.e., coming "from the front", or "from above" in the context of the 
        local frame) are detected. The curvature of the surface does not affect 
        this behavior.
    SENSITIVE_OUT : int
        Represents a surface that is sensitive on the back side. In the surface's 
        local reference frame, only photons arriving with a positive z-component of 
        their direction vector (i.e., coming "from the back", or "from below" in the 
        context of the local frame) are detected. The curvature of the surface 
        does not affect this behavior.
    OPAQUE : int
        Represents a surface that blocks light.
    DUMMY : int
        Represents a surface that neither reflects nor refracts light. 
        It can be used to introduce artificial absorption or scattering effects, 
        serving as a means to model specific behaviors within the optical system.
    
    """
    REFLECTIVE = 0
    REFLECTIVE_IN = 1
    REFLECTIVE_OUT = 2
    REFRACTIVE = 3
    SENSITIVE = 4
    SENSITIVE_IN = 5
    SENSITIVE_OUT = 6
    OPAQUE = 7
    DUMMY = 8
    TEST_SENSITIVE = 9

class SurfaceShape(Enum):
    """
    Enumeration representing different types of surface shapes.

    This enum defines common surface shapes encountered in optical systems or
    other fields requiring precise geometrical definitions.

    """
    ASPHERICAL = 0
    """Represents an aspherical surface."""
    CYLINDRICAL = 1
    """Represents a cylindrical surface."""
    FLAT = 2
    """Represents a flat surface."""
    SPHERICAL = 3
    """Represents a spherical surface."""

class ApertureShape(Enum):
    """
    Enumeration representing the possible shapes of an aperture.

    Attributes
    ----------
    CIRCULAR : int
        Represents a circular aperture.
    HEXAGONAL : int
        Represents a hexagonal aperture.
    SQUARE : int
        Represents a square aperture.
    """
    CIRCULAR = 0
    HEXAGONAL = 1
    SQUARE = 2

@dataclass
class SurfaceEfficiency:
    """
    Represents surface transmittance/reflectance as a function of photon wavelength and incidence angle.
    """
    value: np.ndarray = field(default=None, metadata={'units': 'None'})
    """A numpy.ndarray of shape (n, m) or (n*m,) representing the transmittance/reflectance value (from 0 to 1).
    The value at wavelength[j] and incidence_angle[i] must correspond to:

        - value[i*n+j], if the array is flattened;
        - value[i,j], otherwise.
    
    """

    wavelength: np.ndarray = field(default=None, metadata={'units': 'nanometers'})
    """A NumPy ndarray of shape (n,) representing the wavelengths in nanometers."""

    incidence_angle: np.ndarray = field(default=None, metadata={'units': 'degrees'})
    """A NumPy ndarray of shape (m,) representing the incidence angles in degrees."""

    def __repr__(self):
        """Custom representation showing only whether fields are set."""
        field_info = []
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                field_info.append(f"{field_name}: not set")
            else:
                field_info.append(f"{field_name}: set")
        return f"SurfaceEfficiency({', '.join(field_info)})"

    @iactsim_style
    def plot(self, heatmap: bool | None = None):
        """Plot the efficiency curves.

        Parameters
        ----------
        heatmap : bool, optional
            Whether to plot a 2D heat map.  If `None` (default), a heatmap
            will be used when the number of wavelengths and incidence angles
            is large (greater than 11 for the smaller of the two dimensions).
            Otherwise, individual curves will be plotted.

        Returns
        -------
        matplotlib.figure.Figure, matplotlib.axes.Axes
            The matplotlib figure and axes object containing the plot.
        """
        if (self.incidence_angle is None and self.wavelength is None) or self.value is None:
            raise(RuntimeError("The surface efficiency has not been initialized properly."))
        
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()

        max_n_labels = 11

        plot_wavelength = self.wavelength is not None
        plot_incidence_angle = self.incidence_angle is not None

        n_wl = len(self.wavelength) if plot_wavelength else 1
        n_th = len(self.incidence_angle) if plot_incidence_angle else 1
        values = self.value.flatten()

        if heatmap is None:
            heatmap = False
            if n_th > 1 and n_wl > 1:
                if min(n_th, n_wl) > max_n_labels:
                    heatmap = True

        if not plot_wavelength or plot_incidence_angle:
            heatmap = False

        if not heatmap:
            curves = values.reshape((n_th, n_wl))
            if n_th <= n_wl:
                for i in range(n_th):
                    label = None
                    if self.incidence_angle is not None:
                        label = f'{self.incidence_angle[i]:.1f} $\\degree$'
                    plt.plot(self.wavelength, curves[i], label=label)
                plt.xlabel('Wavelength (nm)')
            else:
                for i in range(n_wl):
                    label = None
                    if self.wavelength is not None:
                        label = f'{self.wavelength[i]:.1f} nm'
                    plt.plot(self.incidence_angle, curves[:,i], label=label)
                plt.xlabel('Incidence angle ($\\degree$)')
            
            if min(n_th, n_wl) < max_n_labels and (plot_wavelength or plot_incidence_angle):
                plt.legend()
            
            plt.ylabel('Efficiency')
            ax.grid(which='both')
        else:
            contour = ax.contourf(self.wavelength, self.incidence_angle, self.value, levels=np.linspace(0,1,100))
            ax.set_xlabel("Wavelength (nm)")
            ax.set_ylabel("Incidence angle ($\\degree$)")
            fig.colorbar(contour, ax=ax, boundaries=[0,1])
        
        return fig, ax