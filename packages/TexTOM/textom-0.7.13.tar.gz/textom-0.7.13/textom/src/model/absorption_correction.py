from scipy.ndimage import map_coordinates
from numba import njit, prange
import numpy as np

from textom.src.model import rotation as rot
from textom.src.model.model_textom import model_textom

from textom.input import geometry as geo
def all_paths( mod:model_textom ):
    
    for g in range(mod.Gs.shape[0]):
        beam_direction = geo.beam_direction @ rot.MatrixfromOTP(mod.Gs[g,0],mod.Gs[g,1],mod.Gs[g,2])
        detector_direction_origin = geo.detector_direction_origin @ rot.MatrixfromOTP(mod.Gs[g,0],mod.Gs[g,1],mod.Gs[g,2])
        detector_direction_positive_90 = geo.detector_direction_positive_90 @ rot.MatrixfromOTP(mod.Gs[g,0],mod.Gs[g,1],mod.Gs[g,2])

        mod.x_p
        

def integrate_mu(mu, point_start, point_end, step):
    direction = point_end - point_start
    length = np.linalg.norm(direction)
    direction = direction / length
    t_vals = np.arange(0, length/step, step)
    points = point_start[:, None] + direction[:, None] * t_vals
    mu_vals = map_coordinates(mu, points, order=1, mode='nearest')
    return np.sum(mu_vals) * step

@njit(parallel=True)
def integrate_detector_pixel(tomogram, beam_dir, two_theta, chi, stepsize):
    nx, ny, nz = tomogram.shape
    kf = np.array([ # this needs to be adapted to beam_dir (actually instead of beam_dir, i need the sample orientation as input and then i back-rotate both k_0 and k_scattered)
        np.sin(two_theta) * np.cos(chi),
        np.sin(two_theta) * np.sin(chi),
        np.cos(two_theta)
    ])
    transmission = np.zeros(tomogram.size)
    idx = 0
    for ix in prange(nx): # here i need to apply the scanmask
        for iy in range(ny):
            for iz in range(nz):
                point = np.array([ix, iy, iz])
                A_in = integrate_along_vector(tomogram, point - 100*beam_dir, point, stepsize)
                A_out = integrate_along_vector(tomogram, point, point + 100*kf, stepsize)
                transmission[idx] = np.exp(-(A_in + A_out))
                idx += 1
    return np.sum(transmission)
'''
basically need to do this:
for s along primary beam:
    point = beam_origin + s*beam_dir
    A_in = integral of μ from beam start to point
    A_out = integral over cone paths from point to detector pixel
    contribution = exp(-A_in - A_out)
    accumulate
'''

@njit
def integrate_along_vector(array_3d, point_start, point_end, stepsize):
    """
    Numerically integrates values from a 3D array along a straight path
    between two points using trilinear interpolation.

    Parameters
    ----------
    array_3d : 3D numpy array
        Field of absorption coefficients or scalar values on a regular grid.
    point_start : array-like of float (3,)
        Starting point of the integration path, in voxel coordinates.
    point_end : array-like of float (3,)
        Ending point of the integration path, in voxel coordinates.
    stepsize : float
        Distance between consecutive interpolation samples (in voxel units).

    Returns
    -------
    float
        Approximate line integral of array_3d along the path.
    """
    # Direction vector and total path length
    direction = point_end - point_start
    length = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    inv_len = 1.0 / length
    dx, dy, dz = direction * inv_len

    n_steps = int(length / stepsize)

    nx, ny, nz = array_3d.shape
    ox, oy, oz = point_start
    integral = 0.0

    for s in range(n_steps):
        # Current position along the path
        x = ox + dx * s * stepsize
        y = oy + dy * s * stepsize
        z = oz + dz * s * stepsize

        # Integer voxel indices
        ix, iy, iz = int(x), int(y), int(z)

        # Skip points outside valid interpolation range
        if 0 <= ix < nx-1 and 0 <= iy < ny-1 and 0 <= iz < nz-1:
            # Fractional offsets within voxel
            fx, fy, fz = x - ix, y - iy, z - iz

            # Trilinear interpolation
            c000 = array_3d[ix, iy, iz]
            c100 = array_3d[ix+1, iy, iz]
            c010 = array_3d[ix, iy+1, iz]
            c001 = array_3d[ix, iy, iz+1]
            c110 = array_3d[ix+1, iy+1, iz]
            c101 = array_3d[ix+1, iy, iz+1]
            c011 = array_3d[ix, iy+1, iz+1]
            c111 = array_3d[ix+1, iy+1, iz+1]

            c00 = c000*(1-fx) + c100*fx
            c01 = c001*(1-fx) + c101*fx
            c10 = c010*(1-fx) + c110*fx
            c11 = c011*(1-fx) + c111*fx
            c0 = c00*(1-fy) + c10*fy
            c1 = c01*(1-fy) + c11*fy
            interpolated_value = c0*(1-fz) + c1*fz

            # Accumulate integral
            integral += interpolated_value

    # Scale by step size to approximate continuous integral
    return integral * stepsize