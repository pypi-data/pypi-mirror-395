import numpy as np
import pandas as pd
import geopy.distance
import alphashape

from types import SimpleNamespace
from scipy.stats import gaussian_kde, kurtosis, skew as skewness
from sklearn.cluster import DBSCAN
from skimage.morphology import skeletonize
from shapely.geometry import Polygon, MultiPolygon
from scipy.spatial import ConvexHull

from .geometry import surface_area_on_the_ellipsoid, ellipse


class Front():
    """
    Representation of an individual front.

    Parameters
    ----------
    label : int
        Front identifier.
    pixels : int
        Number of pixels per front.
    longitude : array-like
        Longitudes of the front pixels.
    latitude : array-like
        Latitudes of the front pixels.
    gm : array-like
        Gradient magnitude values.
    epsx : float
        Maximum distance between two samples in longitude.
    epsy : float
        Maximum distance between two samples in latitude.
    nstd : float
        Number of standard deviations for ellipse estimation.
    """
    def __init__(self, label, pixels, longitude, latitude, gm, epsx, epsy, nstd):
        self.label = label
        self.pixels = pixels
        self.longitude = np.array(longitude)
        self.latitude = np.array(latitude)
        self.gm = np.array(gm)
        self.epsx = epsx
        self.epsy = epsy
        self.nstd = nstd

    def metrics(self):
        """Compute area, ellipse and skeleton metrics for the front."""
        self._area()
        self.front_ellipse()
        self._skeleton()
    
    def _area(self):
        """Compute the approximate area covered by the front in km²."""
        area = 0
        for k in range(self.pixels):
            area += surface_area_on_the_ellipsoid(self.latitude[k], self.latitude[k]+self.epsy, self.longitude[k], self.longitude[k]+self.epsx)
        self.area = area

    def contouring(self, alpha=None):
        """
        Compute alpha-shape contour of the front.

        Parameters
        ----------
        alpha : float, optional
            Alpha value for shape generation. If None, defaults to `1/epsx`.
        """
        self.contours = []
        coords = np.column_stack((self.longitude, self.latitude))

        if alpha == None:
            alpha = 1/self.epsx;

        try:
            alpha_shape = alphashape.alphashape(coords, alpha)
            if alpha_shape and alpha_shape.is_valid:
                self.contours = []
                if isinstance(alpha_shape, Polygon):
                    self.contours.append(alpha_shape)
                elif isinstance(alpha_shape, MultiPolygon):
                    for polygon in alpha_shape.geoms:
                        self.contours.append(polygon)
        except:
            pass

    def front_ellipse(self):
        """Compute the ellipse parameters describing the front."""
        x_mean = np.mean(self.longitude)
        y_mean = np.mean(self.latitude)
        cov = np.cov(self.longitude, self.latitude)

        centre, size, angle, eccentricity, e = ellipse(cov, (x_mean, y_mean), nstd=self.nstd)
        self.ellipse = FrontEllipse(self.longitude, self.latitude, centre, size, angle, eccentricity, e)

        points1 = [(self.ellipse.centre[0]+self.ellipse.size[0]/2*np.cos(np.radians(self.ellipse.angle)), self.ellipse.centre[1]+self.ellipse.size[0]/2*np.sin(np.radians(self.ellipse.angle))), (self.ellipse.centre[0]+self.ellipse.size[0]/2*np.cos(np.radians(self.ellipse.angle + 180)), self.ellipse.centre[1]+self.ellipse.size[0]/2*np.sin(np.radians(self.ellipse.angle + 180)))]
        points2 = [(self.ellipse.centre[0]+self.ellipse.size[1]/2*np.cos(np.radians(self.ellipse.angle+90)), self.ellipse.centre[1]+self.ellipse.size[1]/2*np.sin(np.radians(self.ellipse.angle+90))), (self.ellipse.centre[0]+self.ellipse.size[1]/2*np.cos(np.radians(self.ellipse.angle + 270)), self.ellipse.centre[1]+self.ellipse.size[1]/2*np.sin(np.radians(self.ellipse.angle + 270)))]

        try:
            length = geopy.distance.geodesic(points1[0][::-1], points1[1][::-1]).km
            width = geopy.distance.geodesic(points2[0][::-1], points2[1][::-1]).km
        except:
            length = width = -1
        self.length, self.width = length, width

    def _skeleton(self):
        """
        Build a skeletonized representation of the front from its pixel coordinates.

        Attributes
        ----------
        skeleton : FrontSkeleton
            Object containing the skeleton grid and its geodesic length.
        """
        min_lon = self.longitude.min()
        min_lat = self.latitude.min()
        grid_longitude = np.arange(min_lon, self.longitude.max()+self.epsx, self.epsx)
        grid_latitude = np.arange(min_lat, self.latitude.max()+self.epsy, self.epsy)

        x = ((self.longitude - min_lon) / self.epsx).astype(int)
        y = ((self.latitude - min_lat) / self.epsy).astype(int)
        grid = np.zeros((grid_latitude.shape[0], grid_longitude.shape[0])).astype(float)
        grid[y, x] = 1
        grid[grid == 0] = np.nan

        self.skeleton = FrontSkeleton(grid_latitude, grid_longitude, grid)

    def rotate_front(self, angle=None):
        """
        Rotate the front around its ellipse center.

        Parameters
        ----------
        angle : float, optional
            Rotation angle in degrees. Defaults to 0.
        """
        if angle == None:
            angle = 0

        degrees = -1 * self.ellipse.angle + angle
        angle = np.radians(degrees)
        
        xy = np.hstack((self.longitude.reshape(self.longitude.shape[0], 1), self.latitude.reshape(self.latitude.shape[0], 1)))
        ox, oy = self.ellipse.centre

        rotated_points = []
        for k in range(len(xy)):
            px, py = xy[k][0], xy[k][1]
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            rotated_points.append([qx,qy])

        xy = np.array(rotated_points)
        self.longitude = xy[:,0]
        self.latitude = xy[:,1]
        self.front_ellipse()
    
    def get_greatest_distance(self):
        """
        Compute the greatest geodesic distance between any two pixels using the convex hull of the front.

        Returns
        -------
        tuple
            (distance in km, coord1, coord2)
        """
        points = np.column_stack((self.longitude, self.latitude))

        hull = ConvexHull(points)
        hull_points = points[hull.vertices]

        max_dist = 0
        coord1, coord2 = None, None

        h = len(hull_points)
        for i in range(h):
            for j in range(i+1, h):
                c1 = (hull_points[i,1], hull_points[i,0])
                c2 = (hull_points[j,1], hull_points[j,0])
                dist = geopy.distance.geodesic(c1, c2).kilometers
                if dist > max_dist:
                    max_dist = dist
                    coord1, coord2 = [c1[1], c1[0]], [c2[1], c2[0]]

        return max_dist, coord1, coord2

    def get_gm_description(self, verbose=True):
        """
        Get descriptive statistics of the gradient magnitude.

        Parameters
        ----------
        verbose : bool, default=True
            If True, print the description.

        Returns
        -------
        dict
            Dictionary with statistics (mean, std, min, percentiles, max).
        """
        description = {
            "pixels": self.gm.size,
            "mean": np.nanmean(self.gm),
            "std": np.nanstd(self.gm),
            "min": np.nanmin(self.gm),
            "25%": np.nanpercentile(self.gm, 25),
            "50%": np.nanmedian(self.gm),
            "75%": np.nanpercentile(self.gm, 75),
            "max": np.nanmax(self.gm),
        }

        if verbose:
           for k, v in description.items():
                print(f"{k:>6}: {int(v) if k == 'pixels' else f'{v:.4f}'}")

        return description

class FrontEllipse():
    """
    Representation of a frontal ellipse with statistical descriptors.

    Parameters
    ----------
    longitude : array-like
        Longitudes of the front points.
    latitude : array-like
        Latitudes of the front points.
    centre : tuple
        Ellipse center (x, y).
    size : list
        Ellipse width and height.
    angle : float
        Ellipse rotation angle in degrees.
    eccentricity : float
        Ellipse eccentricity.
    e : matplotlib.patches.Ellipse
        Matplotlib ellipse object.
    x_pdf : 
    y_pdf : 
    """
    def __init__(self, longitude, latitude, centre, size, angle, eccentricity, e):
        self.centre = centre
        self.size = size
        self.angle = angle
        self.eccentricity = eccentricity
        self.e = e
        self.x_pdf = self.pdf(longitude)
        self.y_pdf = self.pdf(latitude)

    def pdf(self, data):
        """
        Estimate the probability density function of a dataset using KDE.

        Parameters
        ----------
        data : array-like
            Input values.

        Returns
        -------
        SimpleNamespace
            Object with attributes:
            - pdf : callable or None
            - pdf_values : array or None
            - data_values : array
            - kurt : float
            - skew : float
        """
        data_values = np.linspace(min(data), max(data), 1000)
        if np.unique(data).size < 2:
            return SimpleNamespace(
                pdf = None,
                pdf_values = None,
                data_values = data_values,
                kurt = kurtosis(data, fisher=True),
                skew = skewness(data)
            )

        kde = gaussian_kde(data)
        return SimpleNamespace(
            pdf = kde,
            pdf_values = kde(data_values),
            data_values = data_values,
            kurt = kurtosis(data, fisher=True),
            skew = skewness(data)
        )

class FrontSkeleton():
    """
    Skeletonized representation of a front.

    Parameters
    ----------
    latitude : array-like
        Latitude grid values.
    longitude : array-like
        Longitude grid values.
    grid : ndarray
        Binary grid of the front.

    Attributes
    ----------
    skeleton : ndarray
        Skeletonized grid (NaN where no skeleton exists).
    length : float
        Geodesic length of the skeleton in kilometers.
    """
    def __init__(self, latitude, longitude, grid):
        self.latitude = latitude
        self.longitude = longitude
        self.grid = grid
        self.skeleton = skeletonize(grid).astype(float)
        self.skeleton[self.skeleton == 0] = np.nan
        self._length()

    def _length(self):
        """Compute the geodesic length of the skeleton."""
        length = 0
        for x in range(self.longitude.shape[0]-1):
            for y in range(self.latitude.shape[0]):
                if self.skeleton[y,x] == 1:
                    coord1 = (self.latitude[y], self.longitude[x])
                    coord2 = (self.latitude[y], self.longitude[x+1])
                    length += geopy.distance.geodesic(coord1, coord2).kilometers
        self.length = length

class FrontTracker():
    """
    Main class for identifying and tracking oceanic fronts over time.

    Attributes
    ----------
    fronts : dict
        Dictionary of identified `Front` objects, indexed by label.
    data : pandas.DataFrame
        Tabular data of all detected front pixels with columns:
        `time`, `longitude`, `latitude`, `gm`, `labels`.
    data_labels : pandas.DataFrame
        DataFrame mapping each front label to its next label in the tracking path.
    epsx : float
        Grid resolution in longitude (degrees).
    epsy : float
        Grid resolution in latitude (degrees).
    eps : float
        Neighborhood distance used in DBSCAN clustering.
    nstd : float
        Number of standard deviations for ellipse estimation.
    """
    def __init__(self):
        self.fronts = {}

    def identify_fronts(self, time, longitudes, latitudes, grid, treshold=0.05, eps=None, nstd=2):
        """
        Identify fronts from gradient magnitude grids using DBSCAN clustering.

        Parameters
        ----------
        time : array-like
            Sequence of timestamps corresponding to the grid.
        longitudes : array-like
            Array of geodesic longitudes.
        latitudes : array-like
            Array of geodesic latitudes.
        grid : ndarray
            3D array of gradient magnitude values (time, lat, lon).
        treshold : float, default=0.05
            Threshold to binarize the gradient magnitude field.
        eps : float, optional
            Maximum distance between two samples for DBSCAN. If None,
            it is estimated automatically from grid resolution.
        nstd : float, default=2
            Number of standard deviations for ellipse estimation.
        """
        if eps == None:
            self.epsx = (longitudes[1]-longitudes[0])
            self.epsy = (latitudes[1]-latitudes[0])
            self.eps = self.epsx if self.epsx > self.epsy else self.epsy
            self.eps = self.eps*1.5
        else:
            self.epsx = self.epsy = eps

        self.nstd = nstd;
        self.fronts = {}
        label_max = 0

        binary_gm = np.copy(grid)
        binary_gm[binary_gm < treshold] = 0
        binary_gm[np.isnan(binary_gm)] = 0
        binary_gm[binary_gm >= treshold] = 1

        for k in range(len(time)):
            xy, gm = self.get_frontal_pixels(longitudes, latitudes, binary_gm[k], grid[k])
            labels = self.get_clusters(xy)

            df = pd.DataFrame({"time": time[k], "longitude": xy[:,0], "latitude": xy[:,1], "gm": gm, "labels": label_max+labels})
            df_grouped = df.groupby("labels").count().reset_index()
            label_max = df.labels.max()+1
            
            for k in range(df_grouped.shape[0]):
                _df = df[df.labels == df_grouped.labels[k]].reset_index(drop=True)
                self.fronts[df_grouped.labels[k]] = Front(df_grouped.labels[k], df_grouped.longitude[k], _df.longitude.values, _df.latitude.values, _df.gm.values, self.epsx, self.epsy, self.nstd)

            if hasattr(self, 'data'):
                self.data = pd.concat([self.data, df], ignore_index=True)
            else: self.data = df

    def get_frontal_pixels(self, x, y, grid, grid_gm):
        """
        Extract pixels corresponding to frontal zone.

        Parameters
        ----------
        x : array-like
            Longitudes.
        y : array-like
            Latitudes.
        grid : 2D ndarray
            Binary grid (1 = front, 0 = background).
        grid_gm : 2D ndarray
            Gradient magnitude values corresponding to the grid.

        Returns
        -------
        xy : ndarray of shape (n, 2)
            Array of (longitude, latitude) coordinates of frontal pixels.
        gm : ndarray
            Gradient magnitude values at the extracted pixels.
        """
        xy, gm = [], []
        for i in range(len(x)):
            for j in range(len(y)):
                if (grid[j,i] != 0) & (~np.isnan(grid[j,i])):
                    xy.append([x[i],y[j]])
                    gm.append(grid_gm[j,i])
        return np.array(xy), np.array(gm)

    def get_clusters(self, X):
        """
        Cluster frontal pixels using DBSCAN.

        Parameters
        ----------
        X : ndarray of shape (n, 2)
            Array of (longitude, latitude) coordinates of frontal pixels.

        Returns
        -------
        labels : ndarray of shape (n,)
            Cluster labels for each pixel.
        """
        return DBSCAN(self.eps, min_samples=1).fit(X).labels_

    def get_frontal_path(self, start_label):
        """
        Compute the sequence of connected fronts starting from a given label.

        Parameters
        ----------
        start_label : int
            Label of the starting front.

        Returns
        -------
        path : list of int
            Sequence of connected front labels.
        """
        path = [start_label]
        current_label = start_label

        while True:
            row = self.data_labels.loc[self.data_labels['labels'] == current_label]
            if row.empty:
                break
            
            next_label = row.iloc[0]['next_labels']

            if pd.isnull(next_label) or next_label is None:
                break
            
            path.append(next_label)
            current_label = next_label
        
        return path

    def track(self):
        """
        Track fronts over time based on pixel overlap.
        """
        self.data['time'] = pd.to_datetime(self.data['time'])
        dias = sorted(self.data['time'].unique())
        tracking = {}

        for t in range(len(dias) - 1):
            dia_t = dias[t]
            dia_tp1 = dias[t + 1]

            frentes_t = self.data[self.data['time'] == dia_t].groupby('labels')
            frentes_tp1 = self.data[self.data['time'] == dia_tp1].groupby('labels')

            usados_tp1 = set()

            for label_t, grupo_t in frentes_t:
                coords_t = set(map(tuple, grupo_t[['latitude', 'longitude']].to_numpy()))
                mejor_label = None
                mejor_overlap = 0

                for label_tp1, grupo_tp1 in frentes_tp1:
                    if label_tp1 in usados_tp1:
                        continue
                    coords_tp1 = set(map(tuple, grupo_tp1[['latitude', 'longitude']].to_numpy()))
                    overlap = len(coords_t & coords_tp1)  # intersección

                    if overlap > mejor_overlap:
                        mejor_overlap = overlap
                        mejor_label = label_tp1

                if mejor_label is not None and mejor_overlap > 0:
                    tracking[(dia_t, label_t)] = (dia_tp1, mejor_label)
                    usados_tp1.add(mejor_label)

        self.data['next_labels'] = None
        for (dia_t, label_t), (dia_tp1, mejor_label) in tracking.items():
            self.data.loc[(self.data['time'] == dia_t) & (self.data['labels'] == label_t), 'next_labels'] = mejor_label

        self.data_labels = self.data[['labels', 'next_labels']].drop_duplicates()
