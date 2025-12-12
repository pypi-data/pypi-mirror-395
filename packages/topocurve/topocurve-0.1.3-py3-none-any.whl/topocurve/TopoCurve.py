# topo_curve/topo_curve/topocurve.py
import os
import math
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import rasterio

from pyproj import Transformer
from scipy.fft import fft2, ifft2
from photutils.psf import TukeyWindow
from PIL import Image
from tifffile import TiffFile
from geotiff import GeoTiff
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

class TopoCurve():
    """
    A class for processing digital elevation models (DEM).

    Attributes:
        metadata (dict): Dictionary containing metadata extracted from the GeoTIFF file.
        z_array (numpy.ndarray): Array of elevation values.
        dimx (int): Number of pixels in the x-direction.
        dimy (int): Number of pixels in the y-direction.
        dx (float): Grid spacing.
        dx_dy (float): Grid spacing in both x and y directions.
    """

    def __init__(self, tiff_file):
        """
        Initializes the TopoCurve object.

        Args:
            tiff_file (str): Path to the GeoTIFF file.
        """
        tif = TiffFile(tiff_file)  # Open the GeoTIFF file

        # Ensure input file is of the right type and contains georeferencing information
        if not tif.is_geotiff:
            raise Exception("Not a GeoTIFF file.")
        if not tif.geotiff_metadata:
            raise Exception("Metadata missing.")

        # Store projection information
        self.metadata = {
            'GeogAngularUnitsGeoKey': tif.geotiff_metadata["GeogAngularUnitsGeoKey"],
            'GeogCitationGeoKey': tif.geotiff_metadata["GeogCitationGeoKey"],
            'GTCitationGeoKey': tif.geotiff_metadata["GTCitationGeoKey"],
            'GTModelTypeGeoKey': tif.geotiff_metadata["GTModelTypeGeoKey"],
            'GTRasterTypeGeoKey': tif.geotiff_metadata["GTRasterTypeGeoKey"],
            'KeyDirectoryVersion': tif.geotiff_metadata["KeyDirectoryVersion"],
            'KeyRevision': tif.geotiff_metadata["KeyRevision"],
            'KeyRevisionMinor': tif.geotiff_metadata["KeyRevisionMinor"],
            'ModelPixelScale': tif.geotiff_metadata["ModelPixelScale"],
            'ModelTiepoint': tif.geotiff_metadata["ModelTiepoint"],
            'ProjectedCSTypeGeoKey': tif.geotiff_metadata["ProjectedCSTypeGeoKey"],
            'ProjLinearUnitsGeoKey': tif.geotiff_metadata["ProjLinearUnitsGeoKey"],
        }

        crs = tif.geotiff_metadata["ProjectedCSTypeGeoKey"].value  # Get the coordinate reference system (CRS)

        # Pull out array of elevation values and store it as array within the DEM class
        gtiff = GeoTiff(tiff_file, crs_code=crs)
        self.z_array = gtiff.read()

        # Pull out dimensions of DEM grid
        self.dimx, self.dimy = gtiff.tif_shape

        # Assign grid spacing and check to ensure grid spacing is uniform in x and y directions
        self.dx = tif.geotiff_metadata["ModelPixelScale"]
        if abs(self.dx[1] - self.dx[0]) < 1e-3:
            self.dx_dy = self.dx[0]
        else:
            raise Exception("WARNING: Grid spacing is not uniform in x and y directions!")

    def CurveCalc(self, ZFilt, dx, dy, kt):
        """
        Calculates principal, mean, and Gaussian curvature maps for a surface Z(x,y).
        Compatible with MATLAB parity and right-handed normal orientation.

        Args:
            ZFilt (numpy.ndarray): 2D array of filtered elevation values (Z(x,y)).
            dx (float): Grid spacing in the x-direction.
            dy (float): Grid spacing in the y-direction.
            kt (float): Threshold value for removing small curvature noise.

        Returns:
            tuple: K1 (numpy.ndarray): Minimum principal curvature.
                   K2 (numpy.ndarray): Maximum principal curvature.
                   KM (numpy.ndarray): Mean curvature (average of K1 and K2).
                   KG (numpy.ndarray): Gaussian curvature (product of K1 and K2).
        """
        Z = ZFilt  # Input filtered surface

        # Compute first derivatives (∂Z/∂x and ∂Z/∂y)
        SZV, SZU = np.gradient(Z, dy, dx)

        # Define tangent vectors (right-handed parameterization basis)
        SXU = np.ones_like(Z)
        SXV = np.zeros_like(Z)
        SYU = np.zeros_like(Z)
        SYV = np.ones_like(Z)

        SU = np.stack((SXU, SYU, SZU), axis=2)  # Tangent in x (U)
        SV = np.stack((SXV, SYV, SZV), axis=2)  # Tangent in y (V)

        # Compute surface normal vector and ensure right-handedness
        CUV = np.cross(SU, SV, axis=2)
        AC = np.linalg.norm(CUV, axis=2)
        NX, NY, NZ = (CUV[..., 0] / AC, CUV[..., 1] / AC, CUV[..., 2] / AC)

        # Compute derivatives of the normal vector
        NXV, NXU = np.gradient(NX, dy, dx)
        NYV, NYU = np.gradient(NY, dy, dx)
        NZV, NZU = np.gradient(NZ, dy, dx)

        # Compute first fundamental form coefficients
        E = np.einsum('ijk,ijk->ij', SU, SU)
        F = np.einsum('ijk,ijk->ij', SU, SV)
        G = np.einsum('ijk,ijk->ij', SV, SV)

        # Compute second fundamental form coefficients
        NU = np.stack((NXU, NYU, NZU), axis=2)  # ∂N/∂u (x-direction)
        NV = np.stack((NXV, NYV, NZV), axis=2)  # ∂N/∂v (y-direction)

        e = -np.einsum('ijk,ijk->ij', NU, SU)
        f = -0.5 * (np.einsum('ijk,ijk->ij', NU, SV) + np.einsum('ijk,ijk->ij', NV, SU))
        g = -np.einsum('ijk,ijk->ij', NV, SV)

        # Solve for principal curvatures
        a = E * G - F**2
        b = -(g * E - 2 * f * F + e * G)
        c = e * g - f**2

        K2 = -(-b + np.sqrt(np.abs(b**2 - 4 * a * c))) / (2 * a)
        K1 = -(-b - np.sqrt(np.abs(b**2 - 4 * a * c))) / (2 * a)

        # Threshold small curvature values
        K1[np.abs(K1) <= kt] = 0
        K2[np.abs(K2) <= kt] = 0

        # Compute derived curvature metrics
        KM = 0.5 * (K1 + K2)  # Mean curvature
        KG = K1 * K2           # Gaussian curvature

        SMAP = np.empty_like(KG) * np.nan
        SDist = [[None] * 9, [None] * 9]

        tol = kt  # use kt also as classification tolerance

        # Perfect Saddles: KG < 0, KM ≈ 0
        in_ = np.where((KG < -tol) & (np.abs(KM) <= tol))
        SMAP[in_] = -4
        SDist[0][0] = ['Perfect Saddles']
        SDist[1][0] = np.size(in_) / np.size(SMAP)

        # Peaks: KG > 0, KM < 0
        in_ = np.where((KG > tol) & (KM < -tol))
        SMAP[in_] = -3
        SDist[0][1] = ['Peaks']
        SDist[1][1] = np.size(in_) / np.size(SMAP)

        # Antiformal Saddles: KG < 0, KM < 0
        in_ = np.where((KG < -tol) & (KM < -tol))
        SMAP[in_] = -2
        SDist[0][2] = ['Antiformal Saddles']
        SDist[1][2] = np.size(in_) / np.size(SMAP)

        # Antiforms: KG ≈ 0, KM < 0
        in_ = np.where((np.abs(KG) <= tol) & (KM < -tol))
        SMAP[in_] = -1
        SDist[0][3] = ['Antiforms']
        SDist[1][3] = np.size(in_) / np.size(SMAP)

        # Planes: KG ≈ 0, KM ≈ 0
        in_ = np.where((np.abs(KG) <= tol) & (np.abs(KM) <= tol))
        SMAP[in_] = 0
        SDist[0][4] = ['Planes']
        SDist[1][4] = np.size(in_) / np.size(SMAP)

        # Synforms: KG ≈ 0, KM > 0
        in_ = np.where((np.abs(KG) <= tol) & (KM > tol))
        SMAP[in_] = 1
        SDist[0][5] = ['Synforms']
        SDist[1][5] = np.size(in_) / np.size(SMAP)

        # Synformal Saddles: KG < 0, KM > 0
        in_ = np.where((KG < -tol) & (KM > tol))
        SMAP[in_] = 2
        SDist[0][6] = ['Synformal Saddles']
        SDist[1][6] = np.size(in_) / np.size(SMAP)

        # Basins: KG > 0, KM > 0
        in_ = np.where((KG > tol) & (KM > tol))
        SMAP[in_] = 3
        SDist[0][7] = ['Basins']
        SDist[1][7] = np.size(in_) / np.size(SMAP)

        # ----------
        CMAP = {
            'KG': KG,
            'KM': KM,
            'K1': K1,
            'K2': K2,
        }

        return K1, K2, KM, KG, SMAP, SDist, CMAP

    
    def get_latlon_extent(self, tiff_path):
        """
        Extracts geographic extent (lon/lat bounding box) from a DEM GeoTIFF.
        Returns:
            [lon_min, lon_max, lat_min, lat_max]
        """

        # Open the GeoTIFF
        with rasterio.open(tiff_path) as src:
            transform = src.transform
            width = src.width
            height = src.height
            crs_projected = src.crs

            # Upper-left corner
            X1, Y1 = transform * (0, 0)

            # Lower-right corner
            X2, Y2 = transform * (width, height)

        # Build transformer from DEM CRS → WGS84
        tf = Transformer.from_crs(crs_projected, "EPSG:4326", always_xy=True)

        # Convert corners to lon/lat
        lon_min, lat_max = tf.transform(X1, Y1)   # upper-left
        lon_max, lat_min = tf.transform(X2, Y2)   # lower-right

        return [lon_min, lon_max, lat_min, lat_max]

    
    def plot(self, array, title, cmap, cbar_label, filename, tiff_file,
             output_dir="../../reports/figures/"):
        """
        Generic plotting function for DEM, filtered DEM, curvature fields, etc.
        """

        os.makedirs(output_dir, exist_ok=True)

        # Get geographic extent
        extent = self.get_latlon_extent(tiff_file)

        plt.figure(figsize=(10, 6))
        plt.imshow(array, cmap=cmap, extent=extent, origin='upper')
        plt.colorbar(label=cbar_label)

        plt.title(title)
        plt.xlabel("Longitude (°W)")
        plt.ylabel("Latitude (°N)")

        # Tick formatting
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.5f'))
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.5f'))

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=300)
        plt.show()

        print(f"Saved: {filename}")


    def plot_smap(self, SMAP, tiff_file, title="Curvature Classification", output_dir="../../reports/figures/"):
        """
        Plot SMAP classification using your hillshade + curvature color rules,
        but without changing SMAP values themselves.
        """

        extent = self.get_latlon_extent(tiff_file)

        # Colors mapped to SMAP values
        color_list = {
            -3: (0.33, 0.00, 0.00, 1.0),   # Dome (deep maroon)
            -2: (0.95, 0.28, 0.26, 1.0),   # Antiformal Saddle (bright red)
            -1: (0.80, 0.20, 0.15, 1.0),   # Antiform (rust red)
            0: (1.00, 1.00, 1.00, 1.0),   # Plane (white)
            1: (0.55, 0.85, 0.90, 1.0),   # Synform (mid cyan)
            2: (0.78, 0.95, 0.98, 1.0),   # Synformal Saddle (cyan)
            3: (0.11, 0.30, 0.95, 1.0)    # Basin (deep blue)
        }

        # Build colormap and norm
        keys = sorted(color_list.keys())  # [-3,-2,-1,0,1,2,3]
        colors = [color_list[k] for k in keys]

        cmap = ListedColormap(colors)
        bounds = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        norm = BoundaryNorm(bounds, cmap.N)

        # Compute hillshade for base layer
        Z = self.z_array
        azimuth=315 
        altitude=45
        az = np.deg2rad(azimuth)
        alt = np.deg2rad(altitude)

        dy, dx = np.gradient(Z)
        slope = np.pi/2 - np.arctan(np.sqrt(dx*dx + dy*dy))
        aspect = np.arctan2(-dx, dy)

        shaded = (np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect))

        hillshade = (shaded - shaded.min()) / (shaded.max() - shaded.min())

        # Plot
        plt.figure(figsize=(10, 8))
        plt.imshow(hillshade, cmap="gray", extent=extent, origin="upper")
        plt.imshow(SMAP, cmap=cmap, norm=norm, alpha=0.55, extent=extent, origin="upper")

        plt.title(title)
        plt.xlabel("Longitude (°W)")
        plt.ylabel("Latitude (°N)")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.4f'))
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.4f'))

        # Legend
        labels = [
            "Dome (KG>0, KM<0)",
            "Antiformal Saddle (KG<0, KM<0)",
            "Antiform (KG≈0, KM<0)",
            "Plane (KG≈0, KM≈0)",
            "Synform (KG≈0, KM>0)",
            "Synformal Saddle (KG<0, KM>0)",
            "Basin (KG>0, KM>0)"
        ]

        patches = [Patch(color=colors[i], label=labels[i]) for i in range(7)]
        plt.legend(handles=patches, loc="lower right", fontsize=8, frameon=True)

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'smap.png'), dpi=300)
        plt.show()
