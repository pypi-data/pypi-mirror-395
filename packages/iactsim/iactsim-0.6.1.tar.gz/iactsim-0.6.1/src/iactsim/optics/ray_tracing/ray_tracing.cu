// Copyright (C) 2024- Davide Mollica <davide.mollica@inaf.it>
// SPDX-License-Identifier: GPL-3.0-or-later
//
// This file is part of iactsim.
//
// iactsim is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// iactsim is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with iactsim.  If not, see <https://www.gnu.org/licenses/>.

//////////////////////////////////////////////////////////////////
//////////////////////////// Content /////////////////////////////
//                                                              //
////// Device functions                                         //
//                                                              //
// __device__ calculate_sag                                     //
// __device__ calculate_sag_derivative                          //
// __device__ compute_surface_normal                            //
// __device__ ray_aspheric_intersection_residual                //
// __device__ ray_aspheric_intersection_residual_derivative     //
// __device__ find_ray_aspheric_intersection                    //
// __device__ interp1d                                          //
// __device__ interp1d_text                                     //
// __device__ interp2d                                          //
// __device__ unregular_interp2d                                //
// __device__ reject_photon                                     //
// __device__ rotate                                            //
// __device__ rotate_back                                       //
// __device__ transform                                         //
// __device__ transform_back                                    //
// __device__ distance_to_aspherical_surface                    //
// __device__ distance_to_cylindrical_surface                   //
// __device__ next_surface                                      //
//                                                              //
////// Kernels                                                  //
//                                                              //
// __global__ trace                                             //
// __global__ trace_onto_sipm_modules                           //
// __global__ atmospheric_transmission                          //
// __global__ telescope_transform                               //
//                                                              //
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

#include <curand_kernel.h>

__constant__ float PI = 3.141592654f;
__constant__ float RAD2DEG = 57.29577951f;
__constant__ float C_LIGHT = 299.792458f; // speed of light in vacuum (mm/ns)
__constant__ float INV_C_LIGHT = 0.0033356409f; // invers speed of light in vacuum (ns/mm)

// Surface types
__constant__ int REFLECTIVE = 0;
__constant__ int REFLECTIVE_IN = 1;
__constant__ int REFLECTIVE_OUT = 2;
__constant__ int REFRACTIVE = 3;
__constant__ int SENSITIVE = 4;
__constant__ int SENSITIVE_IN = 5;
__constant__ int SENSITIVE_OUT = 6;
__constant__ int OPAQUE = 7;
__constant__ int DUMMY = 8;
__constant__ int TEST_SENSITIVE = 9;

// Surface shape
__constant__ int ASPHERICAL = 0;
__constant__ int CYLINDRICAL = 1;
__constant__ int FLAT = 2; // not yet used
__constant__ int SPHERICAL = 3; // not yet used

// Surface aperture shape
__constant__ int CIRCULAR = 0;
__constant__ int EXAGONAL = 1;
__constant__ int SQUARE = 2;

// Constants for sag calculation
__constant__ float CURVATURE_EPS = 1e-6f;
__constant__ float ERROR_VALUE = 1e9f;
__constant__ float R_EPS = 1e-6f;
__constant__ float DIST_EPS = 1e-9;

#define NUM_ASPHERIC_COEFFS 10 // Number of aspheric coefficients

// Constants for intersaction calculation
__constant__ int MAX_ITERATIONS = 30;
__constant__ float DERIVATIVE_EPS = 1e-9f;
__constant__ float ON_AXIS_EPS = 1e-9f;
__constant__ float TOLERANCE0 = 1e-4f; // 0.1 um
__constant__ float TOLERANCE1 = 1e-3f; // 1 um
__constant__ float TOLERANCE2 = 1e-2f; // 10 um
__constant__ float TOLERANCE3 = 1e-1f; // 100 um
__constant__ float TOLERANCE4 = 1.f; // 1 mm

// Material Indices
__constant__ int AIR = 0;
__constant__ int FUSED_SILICA = 1;

// NaN values
// TODO: use a more portable solution for NaNs generation 
__constant__ char type = '0';
extern "C"{

/**
 * @brief Calculates the sagitta of an aspheric optical surface.
 *
 * This function computes the sagitta of an aspheric surface defined by its curvature,
 * conic constant, and aspheric coefficients. It assumes a fixed maximum number
 * of aspheric coefficients, defined by the variable NUM_ASPHERIC_COEFFS.
 *
 * The sagitta equation is a combination of the conic section formula and a even polynomial
 * series representing the aspheric terms:
 *
 * sag = (c * r^2) / (1 + sqrt(1 - (1 + k) * c^2 * r^2)) + A_2 * r^2 + A_4 * r^4 + ...
 *
 * where:
 *   - c is the curvature (1/radius of curvature)
 *   - r is the radial distance from the optical axis
 *   - k is the conic constant
 *   - A_2, A_4, ... are the aspheric coefficients
 *
 * The aspheric coeafficients are the standard aspheric coefficients multiplied by the aperture: A_i = a_i * ra^(2i).
 * The function includes optimizations for special cases like flat surfaces, Fresnel
 * surfaces, and calculations near the optical axis.
 *
 * @param r The radial distance from the optical axis.
 * @param curvature The curvature of the surface (1/radius of curvature).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of aspheric coefficients. The array
 *                       is expected to have a size of at least NUM_ASPHERIC_COEFFS.
 *                       If a surface has fewer coefficients, the array must be
 *                       padded with zeros. The coefficients are ordered
 *                       corresponding to increasing even powers of the radial
 *                       distance (A_2, A_4, A_6, ...).
 * @param is_fresnel Boolean flag indicating whether the surface is a Fresnel surface.
 *                  If true, the sagitta is considered to be 0 (flat).
 * @param half_aperture The half-aperture of the surface.
 *
 * @return The calculated sagitta of the aspheric surface. If an error occurs (e.g.,
 *         negative argument under the square root), returns ERROR_VALUE.
 */
__device__ float 
calculate_sag(
    float r,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    bool is_fresnel,
    float half_aperture
)
{
    if ((fabsf(curvature) < CURVATURE_EPS) || (is_fresnel) || (fabsf(r) < R_EPS)) {
        return 0.f;
    }

    // Calculate normalized radius
    float normalized_radius = r / half_aperture;
    float normalized_radius_squared = normalized_radius * normalized_radius;
    
    // Calculate aspheric contribution
    float tot_aspher = 0.f;
    float rn = normalized_radius_squared;

    #pragma unroll
    for (int i = 0; i < NUM_ASPHERIC_COEFFS; i++) {
        tot_aspher += aspheric_coeffs[i] * rn;
        rn *= normalized_radius_squared;
    }

    float r_squared = r * r;
    float arg_sqrt = 1.f - (1.f + conic_constant) * curvature * curvature * r_squared;

    if (arg_sqrt < 0.f) {
        return ERROR_VALUE;
    }

    return curvature * r_squared / (1.f + sqrtf(arg_sqrt)) + tot_aspher;
}

/**
 * @brief Calculates the derivative of the sagitta of an aspheric surface with respect to the radial distance (r).
 *
 * This function computes the derivative of the sagitta (dsag/dr) for an aspheric
 * surface. The aspheric surface is defined by its curvature, conic constant,
 * and aspheric coefficients. It supports a fixed number of aspheric
 * coefficients (NUM_ASPHERIC_COEFFS).
 *
 * The sagitta equation is a combination of the conic section formula and a polynomial
 * series representing the aspheric terms:
 *
 * sagitta = (c * r^2) / (1 + sqrt(1 - (1 + k) * c^2 * r^2)) + A_2 * r^2 + A_4 * r^4 + ...
 *
 * and its derivative with respect to r is:
 *
 * dsag/dr = (c*r) / sqrt(1 - (1 + k) * c^2 * r^2) + 2*A_2 * r + 4*A_4 * r^3 + ...
 *
 * where:
 *   - c is the curvature (1/radius of curvature)
 *   - r is the radial distance from the optical axis
 *   - k is the conic constant
 *   - A_2, A_4, ... are the aspheric coefficients
 *
 * @param r The radial distance from the optical axis.
 * @param curvature The curvature of the surface (1/radius of curvature).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of aspheric coefficients.
 *                       The coefficients are ordered corresponding to
 *                       increasing even powers of the radial distance
 *                       (A_2, A_4, A_6, ...). The array must have a size
 *                       of at least NUM_ASPHERIC_COEFFS, padded with zeros
 *                       if necessary.
 * @param half_aperture The aperture radius of the surface.
 *
 * @return The calculated derivative of the sagitta (dsag/dr). If an error occurs
 *         (e.g., negative argument under the square root), returns ERROR_VALUE.
 */
__device__ float 
calculate_sag_derivative(
    float r,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    float half_aperture
)
{
    if ((fabsf(curvature) < CURVATURE_EPS) || (r < R_EPS)) {
        return 0.f;
    }

    // Calculate normalized radius
    float normalized_radius = r / half_aperture;
    float normalized_radius_squared = normalized_radius * normalized_radius;

    // Calculate aspheric contribution to the derivative
    float tot_aspher_deriv = 0.f;
    float rn = normalized_radius;

    #pragma unroll
    for (int i = 0; i < NUM_ASPHERIC_COEFFS; i++) {
        tot_aspher_deriv += (i + 1) * aspheric_coeffs[i] * rn;
        rn *= normalized_radius_squared;
    }
    tot_aspher_deriv *= 2.f;

    // Calculate the conic section part
    float r_squared = r * r;
    float c2 = curvature * curvature;
    float arg_sqrt = 1.f - (1.f + conic_constant) * c2 * r_squared;

    if (arg_sqrt < 0.f) {
        return ERROR_VALUE;
    }

    return curvature * r * rsqrtf(arg_sqrt) + tot_aspher_deriv / half_aperture;
}

/**
 * @brief Calculates the upward-pointing normal for an aspheric surface.
 *
 * This function computes the partial derivative of the saggita of a rotationally symmetric aspheric surface. 
 * The surface is defined by a conic constant, curvature, and aspheric coefficients.
 *
 * @param x The x-coordinate.
 * @param y The y-coordinate.
 * @param curvature The curvature (reciprocal of the radius of curvature) of the surface at the vertex.
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of 10 aspheric coefficients. The coefficients are assumed to be normalized by the half-aperture.
 * @param half_aperture The half-aperture used for normalizing aspheric coefficients.
 *
 * @return The upward-pointing normal direction vector (not normalized) the given (x, y) point.
 *         Returns a large value (1e9f) if the point lies outside the valid domain of the surface.
 */
__device__ float3 compute_surface_normal(
    float x,
    float y,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    float half_aperture
)
{
    float3 n = {0.f,0.f,1.f};

    // Flat surface
    if (fabsf(curvature) < CURVATURE_EPS) return n;

    // Square radius
    float r2 = x*x + y*y;
    float inv_half_aperture2 = 1.f / half_aperture / half_aperture;

    // Divide this result by half_aperture^2 since since ai = Ai*half_aperture^(2*(i+1))
    float normalized_r2 = r2 * inv_half_aperture2;
    float total_aspheric_term = 0.f;
    float pow_norm_r2 = inv_half_aperture2;

    #pragma unroll
    for (int i = 0; i < NUM_ASPHERIC_COEFFS; i++) {
        total_aspheric_term += 2.f * (i+1) * aspheric_coeffs[i] * pow_norm_r2;
        pow_norm_r2 *= normalized_r2;
    }

    float arg_sqrt = 1.f - (1.f + conic_constant) * curvature * curvature * r2;

    // This function is called after the intersection point has been founded
    // the point cannot be outside the surface domain

    float factor = curvature * rsqrtf(arg_sqrt);

    n.x = -fmaf(factor, x, total_aspheric_term*x);
    n.y = -fmaf(factor, y, total_aspheric_term*y);

    float inv_norm = rnorm3df(n.x,n.y,n.z);

    n.x *= inv_norm;
    n.y *= inv_norm;
    n.z *= inv_norm;

    return n;
}

/**
 * @brief Calculates the residual for finding the intersection of a ray with an
 *        aspheric surface.
 *
 * This function is designed to be used with an iterative root-finding algorithm
 * (e.g., Newton-Raphson, secant method) to find the intersection point of a
 * ray with an aspheric surface. It computes the difference between the z-coordinate
 * of a point on the ray and the sag of the aspheric surface at the corresponding
 * (x, y) coordinates.
 *
 * The ray is defined by its origin (p) and direction (v).
 * The aspheric surface is defined by its curvature, conic constant, aspheric
 * coefficients, Fresnel flag, and radius.
 *
 * @param distance_along_ray The parameter along the ray where the intersection
 *                        is being sought (the distance from p).
 * @param p A float3 representing the origin (starting point) of the ray.
 * @param v A float3 representing the direction vector of the ray.
 * @param curvature The curvature of the surface (1/radius of curvature).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of aspheric coefficients.
 * @param is_fresnel Boolean flag indicating whether the surface is a Fresnel
 *                  surface.
 * @param half_aperture The half-aperture of the surface.
 *
 * @return The residual value, which should be zero when the ray intersects
 *         the surface.
 */
__device__ float 
ray_aspheric_intersection_residual(
    float distance_along_ray,
    float3& p,
    float3& v,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    bool is_fresnel,
    float half_aperture
)
{
    float x = fmaf(v.x, distance_along_ray, p.x);
    float y = fmaf(v.y, distance_along_ray, p.y);
    float r = sqrtf(x * x + y * y);

    return calculate_sag(r, curvature, conic_constant, aspheric_coeffs, is_fresnel, half_aperture) - p.z - v.z * distance_along_ray;
}

/**
 * @brief Calculates the derivative of the ray-surface intersection residual with respect to the ray parameter.
 *
 * This function computes the derivative of the `ray_aspheric_intersection_residual` function with respect to the ray
 * parameter `distance_along_ray`. This derivative is used in the Newton-Raphson method
 * to find the intersection point of a ray with an aspheric surface.
 *
 * @param distance_along_ray The parameter along the ray where the intersection is being sought.
 * @param p A float3 representing the origin (starting point) of the ray.
 * @param v A float3 representing the direction vector of the ray.
 * @param curvature The curvature of the surface (1/radius of curvature).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of aspheric coefficients.
 * @param half_aperture The half-aperture of the surface.
 *
 * @return The calculated derivative of the ray-surface intersection residual.
 */
__device__ float 
ray_aspheric_intersection_residual_derivative(
    float distance_along_ray,
    float3& p,
    float3& v,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    float half_aperture
)
{
    float x = fmaf(v.x, distance_along_ray, p.x);
    float y = fmaf(v.y, distance_along_ray, p.y);
    float r = sqrtf(x * x + y * y);

    float dir_xy_mag_squared = fmaf(v.x, v.x, fmaf(v.y, v.y, 0.f));
    float dot_prod_origin_dir = fmaf(p.x, v.x, fmaf(p.y, v.y, 0.f));
    float r_derivative = fmaf(dir_xy_mag_squared, distance_along_ray, dot_prod_origin_dir) / r;

    return calculate_sag_derivative(r, curvature, conic_constant, aspheric_coeffs, half_aperture) * r_derivative - v.z;
}

/**
 * @brief Finds the intersection parameter of a ray with an aspheric surface using an iterative method.
 *
 * This function iteratively refines an initial guess for the parameter 't' along a ray
 * to find the intersection point with an aspheric surface. It uses a modified Newton-Raphson
 * method with the Kahan-Babushka-Neumaier (KBN) summation algorithm for improved numerical accuracy 
 * with float32.
 *
 * The ray is defined by its origin (p) and direction (v).
 * The aspheric surface is defined by its curvature, conic constant, aspheric coefficients,
 * Fresnel flag, and aperture radius.
 *
 * @param p A float3 representing the origin (starting point) of the ray.
 * @param v A float3 representing the direction vector of the ray.
 * @param initial_guess The initial guess for the intersection parameter 't'.
 * @param curvature The curvature of the surface (1/radius of curvature).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs Pointer to an array of aspheric coefficients.
 * @param is_fresnel Boolean flag indicating whether the surface is a Fresnel surface.
 * @param half_aperture The half-aperture of the surface.
 *
 * @return The calculated intersection parameter 't' along the ray. Returns ERROR_VALUE if
 *         the method fails to converge within MAX_ITERATIONS or if the derivative is too close to zero.
 */
__device__ float 
find_ray_aspheric_intersection(
    float3& p,
    float3& v,
    float initial_guess,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    bool is_fresnel,
    float half_aperture
)
{
    float t_change = ERROR_VALUE;
    float prev_t = initial_guess;
    float new_t, residual_derivative, residual;

    // Kahan-Babushka-Neumaier sum variables
    volatile float kbn_sum = prev_t;
    volatile float kbn_comp = 0.f;
    volatile float kbn_temp, kbn_input;

    // // Kahan sum variables
    // volatile float k_sum = prev_t;
    // volatile float k_y, k_t, k_input, k_temp;
    // volatile float k_c = 0.f;

    // Dynamic tolerance
    float tolerance = TOLERANCE0;
    
    // Start iteration
    int iteration = 0;
    while (fabsf(t_change) > tolerance) {
        if (iteration > 10) tolerance = TOLERANCE1;
        if (iteration > 15) tolerance = TOLERANCE2;
        if (iteration > 20) tolerance = TOLERANCE3;
        if (iteration > 25) tolerance = TOLERANCE4;
        if (iteration > MAX_ITERATIONS) {
            return ERROR_VALUE;
        }

        residual = ray_aspheric_intersection_residual(prev_t, p, v, curvature, conic_constant, aspheric_coeffs, is_fresnel, half_aperture);
        residual_derivative = ray_aspheric_intersection_residual_derivative(prev_t, p, v, curvature, conic_constant, aspheric_coeffs, half_aperture);

        if (fabsf(residual_derivative) < DERIVATIVE_EPS) {
            return ERROR_VALUE;
        }

        // // Simple Kahan sum
        // k_input = -residual / residual_derivative;
        // k_y = k_input - k_c;
        // k_t = k_sum + k_y;
        // k_temp = k_t - k_sum;
        // k_c = k_temp - k_y;
        // k_sum = k_t;
        // new_t = k_sum;

        // KBN summation for new_t = prev_t - residual / residual_derivative
        kbn_input = -residual / residual_derivative;
        kbn_temp = kbn_sum + kbn_input;
        if (fabsf(kbn_sum) >= fabsf(kbn_input)) {
            kbn_comp += (kbn_sum - kbn_temp) + kbn_input;
        } else {
            kbn_comp += (kbn_input - kbn_temp) + kbn_sum;
        }
        kbn_sum = kbn_temp;
        new_t = kbn_sum + kbn_comp;

        t_change = new_t - prev_t;
        prev_t = new_t;
        iteration++;
    }
    // if (iteration>25) printf("%d\n", iteration);
    return new_t;
}


/**
 * @brief Performs linear interpolation on a 1D dataset containing multiple curves.
 *
 * This function performs linear interpolation to estimate the value of a function at a given point `x0`,
 * based on a set of known data points (`xs`, `ys`) that represent multiple curves. The specific curve
 * to use for interpolation is defined by `start_x`, `start_y`, and `n_points`.
 *
 * @param x0 The x-coordinate at which to interpolate the value.
 * @param xs An array of x-coordinates of the known data points for multiple curves.
 *           The x-coordinates for each curve must be sorted in ascending order.
 * @param ys An array of y-coordinates (function values) corresponding to the `xs` values for multiple curves.
 * @param n_points The number of data points in the specific curve to be used for interpolation.
 * @param inv_dx The inverse of the spacing between consecutive x-coordinates in the curve (1 / (xs[i+1] - xs[i])).
 *               Assumes uniform spacing between points within each curve.
 * @param start_x The starting index in the `xs` array for the curve to be used.
 * @param start_y The starting index in the `ys` array for the curve to be used.
 *
 * @return The interpolated value at `x0`. Returns 0.f if `x0` is outside the range of the specified curve or if any error occurs.
 */
__device__ float 
interp1d(
    float x0,
    const float* xs,
    const float* ys,
    int n_points,
    float inv_dx,
    int start_x,
    int start_y
)
{
    // Distance the first input position
    float dx = x0 - xs[start_x];

    if (dx < 0.f) return 0.f;
    
    // Index of the nearest lower neighbor
    int xi = __float2int_rz(dx * inv_dx);

    if (xi>=n_points-1) return 0.f;

    // Values of the nearest neighbors
    float f0 = ys[start_y+xi];
    float f1 = ys[start_y+xi+1];

    // Calculate weights for linear interpolation
    float t = dx * inv_dx - truncf(dx * inv_dx);

    // Linear interpolation
    // See https://en.wikipedia.org/wiki/Linear_interpolation#Programming_language_support
    return fmaf(t, f1, fmaf(-t, f0, f0));
}

/**
 * @brief Performs bilinear interpolation on a 2D dataset containing multiple grids.
 *
 * This function performs bilinear interpolation to estimate the value of a function at a given point (`x1_0`, `x2_0`),
 * based on a set of known data points (`x1s`, `x2s`, `ys`) that represent multiple 2D grids. The specific grid
 * to use for interpolation is defined by `start_x1`, `start_x2`, `start_y`, `n`, and `m`.
 *
 * @param x1_0 The x1-coordinate at which to interpolate the value.
 * @param x2_0 The x2-coordinate at which to interpolate the value.
 * @param x1s An array of x1-coordinates of the known data points for multiple grids.
 *            The x1-coordinates for each grid must be sorted in ascending order and have uniform spacing.
 * @param x2s An array of x2-coordinates of the known data points for multiple grids.
 *            The x2-coordinates for each grid must be sorted in ascending order and have uniform spacing.
 * @param ys An array of y-values (function values) corresponding to the `x1s` and `x2s` values for multiple grids.
 * @param n The number of data points in the x1-direction for the specific grid to be used.
 * @param m The number of data points in the x2-direction for the specific grid to be used.
 * @param inv_dx1 The inverse of the spacing between consecutive x1-coordinates in the grid (1 / (x1s[i+1] - x1s[i])).
 * @param inv_dx2 The inverse of the spacing between consecutive x2-coordinates in the grid (1 / (x2s[i+1] - x2s[i])).
 * @param start_x1 The starting index in the `x1s` array for the grid to be used.
 * @param start_x2 The starting index in the `x2s` array for the grid to be used.
 * @param start_y The starting index in the `ys` array for the grid to be used.
 *
 * @return The interpolated value at (`x1_0`, `x2_0`). Returns 0.f if (`x1_0`, `x2_0`) is outside the range of the
 *         specified grid or if any error occurs.
 */
__device__ float 
interp2d(
    float x1_0, 
    float x2_0,
    const float* x1s,
    const float* x2s,
    const float* ys,
    int n,
    int m,
    float inv_dx1,
    float inv_dx2,
    int start_x1,
    int start_x2,
    int start_y)
{
    // Distance from x1_0 to the first x1-coordinate of the grid
    float dx1 = x1_0 - x1s[start_x1];
    // Distance from x2_0 to the first x2-coordinate of the grid
    float dx2 = x2_0 - x2s[start_x2];

    // If x1_0 or x2_0 is before the start of the grid, return 0.f
    if ((dx1 < 0.f) | (dx2 < 0.f)) return 0.f;

    // Index of the nearest lower neighbor to x1_0 within the grid
    int x1i = __float2int_rz(dx1 * inv_dx1);

    // Index of the nearest lower neighbor to x2_0 within the grid
    int x2i = __float2int_rz(dx2 * inv_dx2);

    // If x1_0 or x2_0 is beyond the end of the grid, return 0.f
    if ((x1i >= n - 1) | (x2i >= m - 1)) return 0.f;

    // Values of the four nearest neighbors
    float f00 = ys[start_y + x2i * n + x1i];
    float f01 = ys[start_y + (x2i + 1) * n + x1i];
    float f10 = ys[start_y + x2i * n + x1i + 1];
    float f11 = ys[start_y + (x2i + 1) * n + x1i + 1];

    // Calculate the interpolation weights (fractional parts of the distances)
    float t1 = dx1 * inv_dx1 - truncf(dx1 * inv_dx1);
    float t2 = dx2 * inv_dx2 - truncf(dx2 * inv_dx2);

    // Bilinear interpolation formula
    float res = f00 * (1.f - t1) * (1.f - t2) + f01 * (1.f - t1) * t2 + f10 * t1 * (1.f - t2) + f11 * t1 * t2;

    return res;
}

/**
 * @brief Performs bilinear interpolation on a 2D dataset containing multiple grids.
 *
 * This function performs bilinear interpolation to estimate the value of a function at a given point (`x1_0`, `x2_0`),
 * based on a set of known data points (`x1s`, `x2s`, `ys`) that represent multiple 2D grids. The specific grid
 * to use for interpolation is defined by `start_x1`, `start_x2`, `start_y`, `n`, and `m`.
 *
 * @param x1_0 The x1-coordinate at which to interpolate the value.
 * @param x2_0 The x2-coordinate at which to interpolate the value.
 * @param x1s An array of x1-coordinates of the known data points for multiple grids.
 *            The x1-coordinates for each grid must be sorted in ascending order.
 * @param x2s An array of x2-coordinates of the known data points for multiple grids.
 *            The x2-coordinates for each grid must be sorted in ascending order.
 * @param ys An array of y-values (function values) corresponding to the `x1s` and `x2s` values for multiple grids.
 * @param n The number of data points in the x1-direction for the specific grid to be used.
 * @param m The number of data points in the x2-direction for the specific grid to be used.
 * @param start_x1 The starting index in the `x1s` array for the grid to be used.
 * @param start_x2 The starting index in the `x2s` array for the grid to be used.
 * @param start_y The starting index in the `ys` array for the grid to be used.
 *
 * @return The interpolated value at (`x1_0`, `x2_0`). Returns 0.f if (`x1_0`, `x2_0`) is outside the range of the
 *         specified grid or if any error occurs.
 */
__device__ float 
unregular_interp2d(
    float x1_0, 
    float x2_0,
    const float* x1s,
    const float* x2s,
    const float* ys,
    int n,
    int m,
    int start_x1,
    int start_x2,
    int start_y)
{
    // Distance from x1_0 to the first x1-coordinate of the grid
    float dx1 = x1_0 - x1s[start_x1];

    // Distance from x2_0 to the first x2-coordinate of the grid
    float dx2 = x2_0 - x2s[start_x2];

    // If x1_0 or x2_0 is before the start of the grid, return 0.f
    if ((dx1 < 0.f) || (dx2 < 0.f)) return 0.f;

    // If x1_0 or x2_0 is after the end of the grid, return 0.f
    if ((x1_0 >= x1s[start_x1+n-1]) || (x2_0 >= x2s[start_x2+m-1])) return 0.f;

    // Index of the nearest lower neighbor to x1_0 within the grid
    int left = start_x1;
    int right = start_x1 + n - 1;
    int x1i, mid;
    while (left <= right) {
        mid = (left + right) >> 1;
        if ((x1_0 >= x1s[mid]) && (x1_0 < x1s[mid+1])) {
            x1i = mid;
            break;
        }
        else if (x1s[mid] < x1_0) {
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
    }

    // Index of the nearest lower neighbor to x2_0 within the grid
    left = start_x2;
    right = start_x2 + m - 1;
    int x2i;
    while (left <= right) {
        mid = (left + right) >> 1;
        if ((x2_0 >= x2s[mid]) && (x2_0 < x2s[mid+1])) {
            x2i = mid;
            break;
        }
        else if (x2s[mid] < x2_0) {
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
    }

    // Reciprocal of the local step
    float inv_dx1 = 1.f/(x1s[x1i+1]-x1s[x1i]);
    float inv_dx2 = 1.f/(x1s[x2i+1]-x2s[x2i]);

    // Values of the four nearest neighbors
    float f00 = ys[start_y + x2i * n + x1i];
    float f01 = ys[start_y + (x2i + 1) * n + x1i];
    float f10 = ys[start_y + x2i * n + x1i + 1];
    float f11 = ys[start_y + (x2i + 1) * n + x1i + 1];

    // Calculate the interpolation weights (fractional parts of the distances)
    float t1 = dx1 * inv_dx1 - truncf(dx1 * inv_dx1);
    float t2 = dx2 * inv_dx2 - truncf(dx2 * inv_dx2);

    // Bilinear interpolation formula
    float res = f00 * (1.f - t1) * (1.f - t2) + f01 * (1.f - t1) * t2 + f10 * t1 * (1.f - t2) + f11 * t1 * t2;

    return res;
}

/**
 * @brief Rejects a photon by setting its position, direction, wavelength, and time to NaN.
 *
 * This function is used to mark a photon as invalid or rejected. It achieves this by setting
 * all components of the photon position (`p`), direction (`v`), wavelength (`wl`), and time (`t`)
 * to `NaN` (Not a Number).
 *
 * @param p A float3 reference representing the photon position (x, y, z).
 * @param v A float3 reference representing the photon direction vector (vx, vy, vz).
 * @param wl A float reference representing the photon wavelength.
 * @param t A float reference representing the photon time.
 */
__device__ void 
reject_photon(
    float3& p, 
    float3& v, 
    float& wl, 
    float& t
) 
{
    p.x = nanf(&type);
    p.y = nanf(&type);
    p.z = nanf(&type);
    v.x = nanf(&type);
    v.y = nanf(&type);
    v.z = nanf(&type);
    wl = nanf(&type);
    t = nanf(&type);
}

/**
 * @brief Rotates a 3D vector using a rotation matrix.
 *
 * This function rotates the vector `v` using the provided 3x3 rotation matrix `r_mat`.
 * The rotation is performed in-place, modifying the original vector `v`.
 * The rotation matrix is assumed to be stored in row-major order:
 *
 *     | r_mat[0] r_mat[1] r_mat[2] |
 *     | r_mat[3] r_mat[4] r_mat[5] |
 *     | r_mat[6] r_mat[7] r_mat[8] |
 *
 * @param v A reference to a float3 representing the 3D vector to be rotated. This vector will be modified in-place.
 * @param r_mat A pointer to a 9-element array representing the 3x3 rotation matrix in row-major order.
 */
__device__ void 
rotate(
    float3& v,
    const float* r_mat
)
{
    float x = v.x;
    float y = v.y;
    float z = v.z;
    v.x = r_mat[0]*x + r_mat[1]*y + r_mat[2]*z;
    v.y = r_mat[3]*x + r_mat[4]*y + r_mat[5]*z;
    v.z = r_mat[6]*x + r_mat[7]*y + r_mat[8]*z;
}

/**
 * @brief Rotates a 3D vector using the inverse of a rotation matrix.
 *
 * This function rotates the vector `v` using the inverse (transpose) of the provided 3x3 rotation matrix `r_mat`.
 * The rotation is performed in-place, modifying the original vector `v`.
 * The rotation matrix is assumed to be stored in row-major order:
 *
 *     | r_mat[0] r_mat[1] r_mat[2] |
 *     | r_mat[3] r_mat[4] r_mat[5] |
 *     | r_mat[6] r_mat[7] r_mat[8] |
 *
 * @param v A reference to a float3 representing the 3D vector to be rotated. This vector will be modified in-place.
 * @param r_mat A pointer to a 9-element array representing the 3x3 rotation matrix in row-major order.
 */
__device__ void 
rotate_back(
    float3& v, 
    const float* r_mat
)
{
    float x = v.x;
    float y = v.y;
    float z = v.z;
    v.x = r_mat[0]*x + r_mat[3]*y + r_mat[6]*z;
    v.y = r_mat[1]*x + r_mat[4]*y + r_mat[7]*z;
    v.z = r_mat[2]*x + r_mat[5]*y + r_mat[8]*z;
}

/**
 * @brief Transforms a point and a direction vector into a new coordinate system.
 *
 * This function first translates the point `p` by subtracting the origin point `p0`, effectively
 * shifting the origin of the coordinate system. Then, it rotates both the translated point `p`
 * and the direction vector `v` using the provided rotation matrix `r_mat`. The transformations
 * are performed in-place, modifying the original `p` and `v`.
 *
 * The rotation matrix `r_mat` is assumed to be stored in row-major order:
 *
 *     | r_mat[0] r_mat[1] r_mat[2] |
 *     | r_mat[3] r_mat[4] r_mat[5] |
 *     | r_mat[6] r_mat[7] r_mat[8] |
 *
 * @param p A reference to a float3 representing the point to be transformed. This point will be modified in-place.
 * @param v A reference to a float3 representing the direction vector to be transformed. This vector will be modified in-place.
 * @param r_mat A pointer to a 9-element array representing the 3x3 rotation matrix in row-major order.
 * @param p0 A reference to a float3 representing the origin point of the original coordinate system.
 */
__device__ void 
transform(
    float3& p,
    float3& v,
    const float* r_mat,
    const float3& p0
)
{
    p.x -= p0.x;
    p.y -= p0.y;
    p.z -= p0.z;
    rotate(v, r_mat);
    rotate(p, r_mat);
}

/**
 * @brief Transforms a point and a direction vector back to the original coordinate system.
 *
 * This function first rotates both the point `p` and the direction vector `v` using the inverse
 * (transpose) of the provided rotation matrix `r_mat`. Then, it translates the rotated point `p`
 * by adding the origin point `p0`, effectively shifting the origin back to its original position.
 * The transformations are performed in-place, modifying the original `p` and `v`.
 *
 * The rotation matrix `r_mat` is assumed to be stored in row-major order:
 *
 *     | r_mat[0] r_mat[1] r_mat[2] |
 *     | r_mat[3] r_mat[4] r_mat[5] |
 *     | r_mat[6] r_mat[7] r_mat[8] |
 *
 * @param p A reference to a float3 representing the point to be transformed back. This point will be modified in-place.
 * @param v A reference to a float3 representing the direction vector to be transformed back. This vector will be modified in-place.
 * @param r_mat A pointer to a 9-element array representing the 3x3 rotation matrix in row-major order.
 * @param p0 A reference to a float3 representing the origin point of the original coordinate system.
 */
__device__ void 
transform_back(
    float3& p,
    float3& v,
    const float* r_mat,
    const float3& p0
)
{
    rotate_back(v, r_mat);
    rotate_back(p, r_mat);
    p.x += p0.x;
    p.y += p0.y;
    p.z += p0.z;
}

//TODO: use this
/**
 * @brief Calculates the intersection distance of a ray with a spherical surface.
 *
 * This function computes the intersection distance of a ray, defined by its origin `p` and direction `v`,
 * with a spherical surface defined by its curvature `c`. The sphere's center is assumed to be at (0, 0, 1/c).
 *
 * @param p A float3 reference representing the origin of the ray.
 * @param v A float3 reference representing the direction vector of the ray.
 * @param c The curvature of the spherical surface (1/radius).
 *
 * @return The distance from the ray origin to the intersection point. Returns ERROR_VALUE if there is no intersection.
 */
__device__ float 
calculate_spherical_intersection(
    float3& p,
    float3& v,
    float c
) 
{
    float radius = 1.f / c;
    float pv = p.x * v.x + p.y * v.y + (p.z - radius) * v.z;
    float r02 = p.x * p.x + p.y * p.y + (p.z - radius) * (p.z - radius);

    float determinant = pv * pv - r02 + radius * radius;
    if (determinant < 0.f) {
        return ERROR_VALUE;
    }
    
    return -pv - sqrtf(determinant);
}

//TODO: use this
/**
 * @brief Calculates the distance from a point to a spherical or flat surface along a given direction.
 *
 * This function computes the distance from a point `p` to a surface along the direction specified by `v`.
 * The surface can be either spherical (defined by curvature `c`) or flat (c close to 0 or `fresnel` flag set).
 * The point `p` is first translated by subtracting `axial_z` from its z-component.
 *
 * @param p A float3 reference representing the starting point (in/out parameter, z-component will be modified).
 * @param v A float3 reference representing the direction vector.
 * @param c The curvature of the surface (1/radius for spherical surfaces, ~0 for flat surfaces).
 * @param axial_z The z-coordinate of the surface's apex (for spherical surfaces) or the z-intercept (for flat surfaces).
 * @param fresnel A boolean flag indicating whether the surface is a Fresnel surface (treated as flat).
 *
 * @return The distance from the point `p` to the surface along the direction `v`. Returns ERROR_VALUE if there is no intersection.
 */
__device__ float 
calculate_distance_to_spheric_surface(
    float3 p,
    float3& v,
    float c,
    float axial_z,
    bool fresnel
) 
{
    // TODO: Transform here
    p.z -= axial_z;

    if ((fabsf(c) < CURVATURE_EPS) || (fresnel == true)) {
        if (fabsf(v.z) < ON_AXIS_EPS) {
            return ERROR_VALUE; // Ray perpendicular to optical axis
        }
        return -p.z / v.z;
    }
    return calculate_spherical_intersection(p, v, c);
}

/**
 * @brief Calculates the distance along a ray to an aspherical surface intersection, considering surface shape and aperture.
 *
 * This function computes the distance `t` along a ray (defined by origin `p` and direction `v`)
 * to a surface. The function also handles aperture checking for circular and hexagonal shapes.
 *
 * The ray is first transformed into the surface's local coordinate system using `transform`. Then, the intersection
 * distance `t` is calculated based on the surface type. Finally, an aperture check is performed if `aperture_shape`
 * is either `CIRCULAR`, `HEXAGONAL` or `SQUARE`. If the intersection point lies outside the defined aperture, `t` is set to a large value (1e9f).
 *
 * After the intersection and aperture checks, the ray is transformed back into the original coordinate system using `transform_back`.
 *
 * @param t The calculated distance along the ray to the surface (output parameter).
 *          Set to 1e9f if no valid intersection is found (outside aperture or ray misses surface).
 * @param p The starting point of the ray. It is both an input and output parameter.
 *                   Input: Ray origin in the global coordinate system.
 *                   Output: Ray origin transformed back into the global coordinate system after being temporarily transformed into the surface's local coordinate system.
 * @param v The direction vector of the ray. It is both an input and output parameter.
 *                      Input: Ray direction in the global coordinate system.
 *                      Output: Ray direction transformed back into the global coordinate system after being temporarily transformed into the surface's local coordinate system.
 * @param curvature The curvature of the surface (1/radius for spherical surfaces, 0 for flat surfaces).
 * @param conic_constant The conic constant of the surface.
 * @param aspheric_coeffs A pointer to an array of aspheric coefficients for the surface.
 * @param is_fresnel A boolean flag indicating whether the surface is a Fresnel surface (treated as flat).
 * @param outer_aperture The outer radius of the surface aperture.
 * @param inner_aperture The inner radius of the surface aperture.
 * @param aperture_shape An integer representing the shape of the aperture:
 *                       - 0 (CIRCULAR): Circular aperture.
 *                       - 1 (HEXAGONAL): Hexagonal aperture.
 *                       - 2 (SQUARE): Hexagonal aperture.
 *                       - Other values: No aperture check is performed.
 * @param surface_position A float3 representing the origin of the surface's local coordinate system in the global coordinate system.
 * @param rotation_matrix A pointer to a 9-element array representing the 3x3 rotation matrix to transform from the global
 *                       coordinate system to the surface's local coordinate system. The matrix is assumed to be stored in
 *                       row-major order:
 *
 *                           | rotation_matrix[0] rotation_matrix[1] rotation_matrix[2] |
 *                           | rotation_matrix[3] rotation_matrix[4] rotation_matrix[5] |
 *                           | rotation_matrix[6] rotation_matrix[7] rotation_matrix[8] |
 */
__device__ void 
distance_to_aspherical_surface(
    float& t,
    float3 p,
    float3 v,
    float2 offset,
    float curvature,
    float conic_constant,
    const float* aspheric_coeffs,
    bool is_fresnel,
    float outer_aperture,
    float inner_aperture,
    int aperture_shape,
    int central_hole_shape,
    float3 surface_position,
    float* rotation_matrix
)
{
    // Transform into the surface local reference frame 
    transform(p, v, rotation_matrix, surface_position);

    // Check if it is a segment
    float r_off = sqrtf(offset.x*offset.x + offset.y*offset.y);

    // Segment: move to the "mother surface" origin
    if (r_off > R_EPS) {
        float z0 = calculate_sag(
            r_off,
            curvature,
            conic_constant,
            aspheric_coeffs,
            is_fresnel,
            outer_aperture
        );
        p.x += offset.x;
        p.y += offset.y;
        p.z += z0;
    }

    // At this point the distance to the surface 
    // will be computed regardless if it is a segment
    // or a monolithic surface.
    // The segment is by default oriented like the
    // mother surface. A tilt angle represents only a deviation.

    float max_radius;
    if (aperture_shape == CIRCULAR) {
        max_radius = outer_aperture;
    }
    else if (aperture_shape == EXAGONAL) {
        max_radius = outer_aperture*1.15470053f;
    }
    else if (aperture_shape == SQUARE) {
        max_radius = outer_aperture*1.41421356f;
    }

    // Ray perpendicular to the optical axis
    //
    // TODO: cover this case
    // to do so we can try these:
    //
    //   1- two reference spheres that contain the aspheric surface
    //      1a - find the intersections (t1a,t1b) and (t2a,t2b) with the spheres
    //      2a - look for the aspheric intersections in the intervals above
    //
    //   2- a reference sphere that describes well the aspheric slope
    //      1a - find the intersections (t1,t2) with the spheres
    //      2a - look for the aspheric intersections in the interval above
    //
    // Not a main issue since ray tracing is often performed for small off axis angle (up to 6 degrees),
    // but maybe can be useful in some cases.
    //
    if (fabsf(v.z) < ON_AXIS_EPS) {
        t = ERROR_VALUE;
        return;
    }
    float inv_v2 = 1.f / v.z;

    // Intersection with the surface tangential plane
    float a = -p.z * inv_v2;

    // Flat or Fresnel surface
    if ((fabsf(curvature) < CURVATURE_EPS) || (is_fresnel == true)) {
        t = a;
    }
    // On-axis ray
    else if (1.f - fabsf(v.z) < ON_AXIS_EPS) {
        float r = sqrtf(p.x * p.x + p.y * p.y);
        float sag = calculate_sag(
            r,
            curvature,
            conic_constant,
            aspheric_coeffs,
            is_fresnel,
            max_radius
        );
        t = (sag - p.z) * inv_v2;
    }
    // Aspherical surface
    else {
        // float initial_guess;
        // float r = sqrtf(p.x * p.x + p.y * p.y);
        // float sag = calculate_sag(
        //     r,
        //     curvature,
        //     conic_constant,
        //     aspheric_coeffs,
        //     is_fresnel,
        //     max_radius
        // );
        // initial_guess = (0.5f*sag - p.z) * inv_v2;
        t = find_ray_aspheric_intersection(
            p,
            v,
            a,
            curvature,
            conic_constant,
            aspheric_coeffs,
            is_fresnel,
            max_radius
        );
    }

    // Move to the intersection
    // If the surface is a segment move back to its origin.
    float xa = fmaf(v.x, t, p.x) - offset.x;
    float ya = fmaf(v.y, t, p.y) - offset.y;

    // Aperture 
    bool inside_aperture = true;

    if (aperture_shape == CIRCULAR) {
        float r = sqrtf(xa*xa + ya*ya);
        inside_aperture = r < outer_aperture;
    }
    else if (aperture_shape == EXAGONAL) {
        float px = fabsf(xa);
        float py = fabsf(ya);
        // [inner exagon radius]/cos(30/180*pi)=[outer exagon radius]
        float r1 = outer_aperture*1.15470053f;
        float dprod1 = outer_aperture * r1 - 0.5f * r1 * py - outer_aperture * px;
        inside_aperture = ((py > outer_aperture) || (px > r1)) ? false : (dprod1 >= 0.f);

    }
    else if (aperture_shape == SQUARE) {
        bool in_inner_x  = (fabsf(xa) < outer_aperture);
        bool in_inner_y  = (fabsf(ya) < outer_aperture);
        inside_aperture = in_inner_x && in_inner_y;
    }

    if (!inside_aperture) {
        t = ERROR_VALUE;
        return;
    }

    // Central hole
    if (inner_aperture>0.f) {
        bool inside_hole = true;
    
        if (central_hole_shape == CIRCULAR) {
            float r = sqrtf(xa*xa + ya*ya);
            inside_hole = r < inner_aperture;
        }
        else if (central_hole_shape == EXAGONAL) {
            float px = fabsf(xa);
            float py = fabsf(ya);
            // [inner exagon radius]/cos(30/180*pi)=[outer exagon radius]
            float r1 = inner_aperture*1.15470053f;
            float dprod1 = inner_aperture * r1 - 0.5f * r1 * py - inner_aperture * px;
            inside_hole = ((py > inner_aperture) || (px > r1)) ? false : (dprod1 >= 0.f);

        }
        else if (central_hole_shape == SQUARE) {
            bool in_inner_x  = (fabsf(xa) < inner_aperture);
            bool in_inner_y  = (fabsf(ya) < inner_aperture);
            inside_hole = in_inner_x && in_inner_y;
        }

        if (inside_hole) {
            t = ERROR_VALUE;
            return;
        }
    }
}

/**
 * @brief Calculates the distance from a point to a cylindrical surface along a given direction.
 *
 * This function determines the distance `t` that a ray, starting at point `p` and traveling in 
 * direction `v`, must travel to intersect a cylindrical surface. The cylinder is defined by its 
 * `radius`, `height`, `surface_position` (the center of the cylinder
 * ), and a `rotation_matrix`
 * that orients it in 3D space.
 *
 * The function first transforms the ray into the cylinder's local coordinate system to simplify
 * the intersection calculation. It then solves the quadratic equation resulting from the 
 * intersection of a line and a cylinder. The function returns the smallest positive solution for `t`,
 * indicating the nearest intersection point. If no intersection occurs, or if the intersection 
 * point falls outside the cylinder's height, `t` is set to `ERROR_VALUE` (likely a predefined 
 * constant, e.g., -1.0f).
 *
 * @param t Output parameter. The calculated distance to the intersection point. Set to `ERROR_VALUE`
 *          if no intersection is found or if the intersection is outside the cylinder's height.
 * @param p The starting point of the ray (float3, likely a struct or class representing a 
 *          3D point with x, y, z coordinates).
 * @param v The direction vector of the ray (float3).
 * @param radius The radius of the cylinder.
 * @param height Half the total height of the cylinder (the cylinder extends from -height to +height along its local z-axis, centered at `surface_position`).
 * @param is_hollow Whether a ray can pass inside the cylinder curved surface.
 * @param surface_position The position of the **center** of the cylinder in the global 
 *                       coordinate system (float3).
 * @param rotation_matrix A pointer to a flattened 3x3 rotation matrix that transforms from the 
 *                        global coordinate system to the cylinder's local coordinate system.
 *
 * @note The function uses a small epsilon value `ON_AXIS_EPS` (likely a predefined constant) to handle 
 *       the special case where the ray is nearly parallel to the cylinder's axis.
 * @note The function assumes the cylinder's axis is aligned with the z-axis in its local coordinate system.
 * @note The `transform` and `transform_back` functions are assumed to be defined elsewhere and handle 
 *       the coordinate transformations between the global and local coordinate systems.
 */
__device__ void 
distance_to_cylindrical_surface(
    float& t,
    float3 p,
    float3 v,
    float radius,
    float height,
    bool top,
    bool bottom,
    float3 surface_position,
    float* rotation_matrix
)
{
    // Transform into the surface local reference frame
    transform(p, v, rotation_matrix, surface_position);

    float half_height = 0.5f*height;

    // Compute intersections with the top or bottom of the cylinder
    float t_flat;

    // Perpendicaular rays do not intersect with the base
    if (fabsf(v.z) < ON_AXIS_EPS) {
        t_flat = -ERROR_VALUE;
    }
    else {
        // Check if the ray reach the base planes
        float t_up = (half_height - p.z) / v.z;
        float t_down = (-half_height - p.z) / v.z;

        // The ray is going away
        if ((t_up < 0.f) && (t_down < 0.f)) {
            t = ERROR_VALUE;
            return;
        }

        // Check interestion with top and/or bottom as requested
        // TODO: use signbit
        if (top && bottom){
            t_flat = t_up*t_down < 0.f ? fmaxf(t_up,t_down) : fminf(t_up,t_down);
        }
        else if (top) {
            t_flat = t_up;
        }
        else {
            t_flat = t_down;
        }

        // Constrain on surface extent
        if (top || bottom) {
            float x_flat = fmaf(v.x, t_flat, p.x);
            float y_flat = fmaf(v.y, t_flat, p.y);
            float r_flat = sqrtf(x_flat*x_flat + y_flat*y_flat);
            if (r_flat > radius) {
                t_flat = -ERROR_VALUE;
            }
        }
    }
    
    // Compute intersections with the cylinder curved surface
    // On-axis ray do not intersect
    float t_cyl = -ERROR_VALUE;
    if (1.f - fabsf(v.z) > ON_AXIS_EPS) {
        float a = v.x*v.x + v.y*v.y;
        float b = -2.f * (p.x*v.x + p.y*v.y);
        float c = p.x*p.x + p.y*p.y - radius*radius;

        float delta = b*b - 4.f*a*c;

        // No intersaction with the reference cylinder
        if (delta >= 0.f) {
         
            float sqrt_delta = sqrtf(delta);

            float t1 = -0.5f*(-b - copysignf(sqrt_delta, b))/a;
            float t2 = c / a / t1;
            
            // TODO: use signbit
            t_cyl = t1*t2 < 0.f ? fmaxf(t1,t2) : fminf(t1,t2);

            // No positive intersaction with the reference cylinder
            if (t_cyl < 0.f) {
                t = ERROR_VALUE;
                return;
            }

            // Constrain on surface extent
            if (fabsf(p.z + t_cyl*v.z) > half_height)
                t_cyl = -ERROR_VALUE;
        }
    }

    // Now we have t_cyl and t_flat
    if (top || bottom) {
        if ((t_cyl < 0.f) && (t_flat<0.f)) {
            t = ERROR_VALUE;
        }
        else if (t_cyl < 0.f) {
            t = t_flat;
        }
        else {
            t = t_cyl*t_flat < 0.f ? fmaxf(t_cyl,t_flat) : fminf(t_cyl,t_flat);
        }
    }
    else {
        t = t_cyl < 0.f ? ERROR_VALUE : t_cyl;
    }
    
}

/**
 * @brief Represents an intersection between a ray and a surface.
 */
struct Intersection {
    int surface_index;  /**< Index of the intersected surface. */
    float distance;     /**< Distance along the ray to the intersection point. */
};

/**
 * @brief Finds the next surface that a ray intersects.
 *
 * This function iterates through a list of surfaces, starting from the `last_surface` + 1 index,
 * and calculates the intersection distance between the ray defined by origin `p` and
 * direction `v` and each surface. It returns an `Intersection` struct containing
 * the index of the closest intersected surface and the corresponding intersection distance.
 *
 * @param intersection An Intersection struct containing the index of the next intersected surface and the distance to it.
 *                     If no valid intersection is found, `intersection.surface_index` will be -1 and `intersection.distance` will be ERROR_VALUE.
 * @param last_surface The index of the last intersected surface.
 * @param p The origin of the ray. It is transformed in place during calculations.
 * @param v The direction of the ray (should be normalized). It is transformed in place during calculations.
 * @param curvatures Array of curvature values for each surface.
 * @param conic_constants Array of conic constant values for each surface.
 * @param aspheric_coeffs Array of aspheric coefficients for each surface. Each surface has 10 coefficients corresponding
 *                        to the even asphere equation: z = (c*r^2) / (1 + sqrt(1-(1+k)*c^2*r^2)) + A1*r^2 + A2*r^4 + A3*r^6 + ...
 * @param surface_flags Array of boolean flags for each surface, see `trace` kernel.
 * @param aperture_radii Array of aperture radii. Each surface has two values: outer radius and inner radius.
 * @param aperture_shapes Array of aperture and central hole shape identifiers for each surface (aperture_shapes[i*2] and aperture_shapes[i*2+1] respectively): 
 * 
 *                          - 0 (CIRCULAR): Circular aperture.
 *                          - 1 (HEXAGONAL): Hexagonal aperture (inradius).
 *                          - 3 (SQUARE): Hexagonal aperture.
 *                          - Other values: No aperture check is performed.
 * 
 * @param surface_positions Array of surface positions (center points).
 * @param surface_rotation_matrices Array of surface rotation matrices (3x3 matrices, stored in row-major order).
 *                                  Each surface has 9 elements representing its rotation matrix.
 * @param shapes Array of surface type identifiers
 * @param num_surfaces The total number of surfaces in the system.
 */
__device__ 
void next_surface(
    Intersection& intersection,
    int last_surface,
    float3 p,
    float3 v,
    const float2* offsets,
    const float* curvatures,
    const float* conic_constants, 
    const float* aspheric_coeffs,
    const bool* surface_flags, 
    const float* aperture_radii,
    const int* aperture_shapes,
    const float3* surface_positions,
    const float* surface_rotation_matrices,
    const int* shapes,
    int num_surfaces
)
{
    intersection.surface_index = -1;
    intersection.distance = ERROR_VALUE;

    float t, surface_rotation_matrix[9], aspheric_coefficients[10];
    for (int i = 0; i < num_surfaces; i++) {
        if (i == last_surface)
            continue;

        // Surface rotation
        for (int j = 0; j < 9; j++) {
            surface_rotation_matrix[j] = surface_rotation_matrices[i*9 + j];
        }

        // Find distance to the surface
        if (shapes[i] == CYLINDRICAL) {
            distance_to_cylindrical_surface(
                t,
                p,
                v,
                aperture_radii[i*2],
                aperture_radii[i*2+1],
                surface_flags[i*2],
                surface_flags[i*2+1],
                surface_positions[i],
                surface_rotation_matrix
            );
        }
        else {
            // Aspheric coefficients
            for (int j = 0; j < 10; j++) {
                aspheric_coefficients[j] = aspheric_coeffs[i * 10 + j];
            }
            distance_to_aspherical_surface(
                t,
                p,
                v,
                offsets[i],
                curvatures[i],
                conic_constants[i],
                aspheric_coefficients,
                surface_flags[i*2],
                aperture_radii[i*2],
                aperture_radii[i*2+1],
                aperture_shapes[i*2],
                aperture_shapes[i*2+1],
                surface_positions[i],
                surface_rotation_matrix
            );
        }

        // Check if it is a valid intersection (inside the aperture and positive distance)
        if ((t >= DIST_EPS) && (t < intersection.distance)) {
            intersection.distance = t;
            intersection.surface_index = i;
        }
    }
}

__device__ float interp1d_text(float x, float inv_dx, float start_x, cudaTextureObject_t& tex) {
    float u = (x-start_x)*inv_dx;
    return tex1D<float>(tex, u+0.5f);
}

/**
 * @brief The main ray tracing kernel.
 *
 * This kernel traces individual photons through an optical system, simulating their interactions with surfaces.
 * 
 * Values can represent different quantities depending on the surface type (e.g. aperture_sizes[i] defines the 
 * r_min and r_max aperture for an aspheric surface with circular aperture, but radius and height for a cylindrical surface).
 * 
 *
 * @param ps Array of photon positions (x, y, z).
 * @param vs Array of photon directions (normalized vectors, x, y, z).
 * @param wls Array of photon wavelengths (in desired units, e.g., nanometers).
 * @param times Array of photon times (time elapsed since the start of the trace).
 * @param weights Array of photon weights (initially 1 for each photon; can be reduced by transmission or absorption).
 * @param curvatures Array of surface curvature values for each surface.
 * @param conic_constants Array of surface conic constant values for each surface.
 * @param aspheric_coefficients Array of surface aspheric coefficients. Each surface has 10 coefficients corresponding
 *                              to the even asphere equation: :math:`z = (cr^2) / (1 + \sqrt{1-(1+k)c^2r^2}) \sum_{i=1}^n A_i r^{2i}`
 * @param surface_flags Array of boolean flags with different meaning for each surface type: (1) i-th aspheric surfaces: ``surface_flags[i]`` 
 *                      indicates whether the surface should be treated as a Fresnel surface; (2) i-th cylindrical surface: ``surface_flags[i]`` 
 *                      indicates whether the cylinder is hollow.
 * 
 * @param aperture_sizes Array of surface aperture sizes. Each surface has two values with different meaning for each surface type:
 *                       (1) i-th aspheric surface with circcular aperture: ``aperture_sizes[i+0]`` is the outer radius, and ``aperture_sizes[i+1]`` is the inner radius. 
 *                       (2) i-th aspheric surface with rectangular aperture: ``aperture_sizes[i+0]`` is the half-width in x, and ``aperture_sizes[i+1]`` is the half-width
 *                       in y. (3) i-th cylindrical surface: ``aperture_sizes[i+0]`` is the radius and ``aperture_sizes[i+1]`` is the height.
 * @param aperture_shapes Array of aperture and central hole shape identifiers for each surface (aperture_shapes[i*2] and aperture_shapes[i*2+1] respectively).
 * @param surface_positions Array of surface positions.
 * @param offsets Array of segment offsets. x and y coordinates for each surface.
 * @param surface_rotation_matrices Array of surface rotation matrices.
 * @param surface_types Array of surface type identifiers.
 * @param materials_before Array of material indices.
 * @param materials_after Array of material indices.
 * @param num_surfaces The total number of surfaces in the optical system.
 * @param telescope_rotation_matrix Rotation matrix of the telescope with respect to the global coordinate system.
 * @param telescope_position Position of the telescope with respect to the global coordinate system.
 * @param surface_scattering_dispersions Array of surface scattering sigmas in fraction of straight angle (i.e. degrees / 180).
 * @param transmission_curves Array of transmission curves.
 * @param transmission_curve_wavelengths Array of wavelengths for the transmission curves.
 * @param transmission_curve_angles Array of angles for the transmission curves (if applicable).
 * @param transmission_curve_dimensions Array of dimensions (number of wavelengths, number of angles) for each transmission curve.
 * @param inverse_curve_steps Array of inverse step sizes for wavelength and angle dimensions of transmission curves.
 * @param num_photons The total number of photons to trace.
 * @param refractive_index_textures
 * @param inv_dwl_refractive_index
 * @param start_wl_refractive_index
 * 
 */
__global__ 
void trace(
    float3* ps,
    float3* vs,
    float* wls,
    float* times,
    int* weights,
    const float* curvatures,
    const float* conic_constants,
    const float* aspheric_coefficients,
    const bool* surface_flags,
    const float* aperture_sizes,
    const int* aperture_shapes,
    const float3* surface_positions,
    const float2* offsets,
    const float* surface_rotation_matrices,
    const int* surface_types,
    const int* shapes,
    const int* materials_before,
    const int* materials_after,
    int num_surfaces,
    const float* telescope_rotation_matrix,
    const float3* telescope_position,
    const float* surface_scattering_dispersions,
    const float* transmission_curves,
    const float* transmission_curve_wavelengths,
    const float* transmission_curve_angles,
    const int* transmission_curve_dimensions,
    const float* inverse_curve_steps,
    const unsigned long long* refractive_index_textures, // one for each defined material
    const float* inv_dwl_refractive_index, // invers of the walength-spacing of each refractive index curve
    const float* start_wl_refractive_index, // start wavelength of each refractive index curva
    int num_photons
)
{
    // Photon index
    int k = blockIdx.x * blockDim.x + threadIdx.x;
    if (k >= num_photons) return;

    // Transform into telescope reference system
    transform(ps[k], vs[k], telescope_rotation_matrix, telescope_position[0]);

    int bounces_counter = 0;
    int current_surface = -1;
    Intersection intersection;

    while (true) {

        // Find the next_surface surface looking for the nearest surface along the ray path
        next_surface(
            intersection,
            current_surface,
            ps[k],
            vs[k],
            offsets,
            curvatures,
            conic_constants,
            aspheric_coefficients,
            surface_flags,
            aperture_sizes,
            aperture_shapes,
            surface_positions,
            surface_rotation_matrices,
            shapes,
            num_surfaces
        );
        
        int next_surface_index = intersection.surface_index;
        float next_surface_distance = intersection.distance;

        // Reject the photon in the following cases
        // - the surface is not found
        // - the surface is opaque
        if ((surface_types[next_surface_index]==OPAQUE) || (next_surface_index==-1) || bounces_counter>1000) {
            reject_photon(ps[k], vs[k], wls[k], times[k]);
            break;
        }

        bounces_counter += 1;

        // Next surface
        current_surface = next_surface_index;

        // Surface rotation (inside the telescope reference system)
        float surface_rotation_matrix[9];
        for (int j = 0; j < 9; j++) {
            surface_rotation_matrix[j] = surface_rotation_matrices[current_surface*9+j];
        }

        // After this call we are in the surface local coordinate system
        transform(ps[k], vs[k], surface_rotation_matrix, surface_positions[current_surface]);

        // Move to the found intersection
        ps[k].x = fmaf(vs[k].x, next_surface_distance, ps[k].x);
        ps[k].y = fmaf(vs[k].y, next_surface_distance, ps[k].y);
        ps[k].z = fmaf(vs[k].z, next_surface_distance, ps[k].z);
        
        int material_in, material_out;
        if (vs[k].z < 0.f) {
            material_in = materials_before[current_surface];
            material_out = materials_after[current_surface];
        }
        else {
            material_in = materials_after[current_surface];
            material_out = materials_before[current_surface];
        }

        // Get refractive index
        cudaTextureObject_t texture_ri_in = refractive_index_textures[material_in];
        float ri_in = interp1d_text(
            wls[k],
            inv_dwl_refractive_index[material_in],
            start_wl_refractive_index[material_in],
            texture_ri_in
        );
        
        // Update time
        times[k] += next_surface_distance * ri_in * INV_C_LIGHT;

        #ifdef STOP_SURFACE
        if (current_surface == STOP_SURFACE) {
            transform_back(ps[k], vs[k], surface_rotation_matrix, surface_positions[current_surface]);
            break;
        }
        #endif

        int surface_type = surface_types[current_surface];

        // On focal surface
        // Do not transform back to the telescope reference system since
        // ray-tracing into modules is done on the focal surface local system

        // Sensitive on both side
        if (surface_type == TEST_SENSITIVE) {
            transform_back(ps[k], vs[k], surface_rotation_matrix, surface_positions[current_surface]);
            break;
        }

        // Sensitive on both side
        if (surface_type == SENSITIVE) {
            break;
        }

        // Ray arriving on the
        //  convex side: if c<0
        //  concave side: if c>0 
        if (vs[k].z < 0.f) {
            // Photon has reached the a sensitive surface side
            if (surface_type == SENSITIVE_OUT)
                break;
            
            // Photon has reached an unsensitive surface side
            if ((surface_type == REFLECTIVE_IN) || (surface_type == SENSITIVE_IN)) {
                reject_photon(ps[k], vs[k], wls[k], times[k]);
                break;
            }
        }

        // Ray arriving on the
        //  concave side: if c<0
        //  convex side: if c>0
        if (vs[k].z > 0.f) {
            // Photon has reached a sensitive surface side
            if (surface_type == SENSITIVE_IN)
                break;
            
            // Photon has reached an unsensitive surface side
            if ((surface_type == REFLECTIVE_OUT) || (surface_type == SENSITIVE_OUT)) {
                reject_photon(ps[k], vs[k], wls[k], times[k]);
                break;
            }
        }

        // Aspheric coefficients to local memory
        float A[10];
        for (int j = 0; j < 10; j++) {
            A[j] = aspheric_coefficients[current_surface*10 + j];
        }

        // Surface normal (from the gradient)
        float3 surface_normal = compute_surface_normal(
            ps[k].x+offsets[current_surface].x,
            ps[k].y+offsets[current_surface].y,
            curvatures[current_surface],
            conic_constants[current_surface],
            A,
            aperture_sizes[current_surface*2]
        );

        // Cosine of the incidence angle on the surface
        float cosine_incident_angle = surface_normal.x*vs[k].x + surface_normal.y*vs[k].y + surface_normal.z*vs[k].z;
        
        curandStatePhilox4_32_10_t state;
        curand_init(clock64(), k, 0, &state);

        // Transmission
        int x1_size = transmission_curve_dimensions[current_surface*5 + 3];
        int x2_size = transmission_curve_dimensions[current_surface*5 + 4];

        if ((x1_size > 0) | (x2_size > 0)) {
            float transmission;

            // Wavelength dependance
            int start_x1 = transmission_curve_dimensions[current_surface*5+1];
            float inv_dx1 = inverse_curve_steps[current_surface*2];

            // Angular dependance
            int start_x2 = transmission_curve_dimensions[current_surface*5+2];
            float inv_dx2 = inverse_curve_steps[current_surface*2+1];

            int start_curve = transmission_curve_dimensions[current_surface*5];

            if (x2_size > 0) {
                float thetai = acosf(fabsf(cosine_incident_angle)) * RAD2DEG;
                // T(wl,theta)
                if (x1_size > 0) {
                    transmission = interp2d(wls[k], thetai, transmission_curve_wavelengths, transmission_curve_angles, transmission_curves,
                                           x1_size, x2_size, inv_dx1, inv_dx2, start_x1, start_x2, start_curve);
                }
                // T(theta)
                else {
                    transmission = interp1d(thetai, transmission_curve_angles, transmission_curves, x2_size, inv_dx2, start_x2, start_curve);
                }
            }
            else {
                // T(wl)
                transmission = interp1d(wls[k], transmission_curve_wavelengths, transmission_curves, x1_size, inv_dx1, start_x1, start_curve);
            }

            int bunch_size = weights[k];
            for (int bunch = 0; bunch < bunch_size; bunch++) {
                float u = curand_uniform(&state);
                if (u > transmission) weights[k] -= 1;
            }

            if (weights[k] < 1) {
                reject_photon(ps[k], vs[k], wls[k], times[k]);
                break;
            }
        }

        // Optical processes at the interface
        if (surface_type == REFRACTIVE)
        {
            cudaTextureObject_t texture_ri_out = refractive_index_textures[material_out];
            float ri_out = interp1d_text(
                wls[k],
                inv_dwl_refractive_index[material_out],
                start_wl_refractive_index[material_out],
                texture_ri_out
            );

            float refractive_index_ratio = ri_in / ri_out;
            float refractive_index_ratio2 = refractive_index_ratio * refractive_index_ratio;

            // Related to the normal part of the transmitted direction
            float sqrt_argument = 1.f - refractive_index_ratio2 * (1.f - cosine_incident_angle*cosine_incident_angle);

            // Kill photons that are internally reflected
            if (sqrt_argument <= 0.f) {
                reject_photon(ps[k], vs[k], wls[k], times[k]);
                break;
            }
            
            // Parallel + normal component (adjust for opposite i and n direction)
            float factor = refractive_index_ratio*fabsf(cosine_incident_angle) + copysignf(1.f, cosine_incident_angle)*sqrtf(sqrt_argument);

            vs[k].x = fmaf(refractive_index_ratio, vs[k].x, factor*surface_normal.x);
            vs[k].y = fmaf(refractive_index_ratio, vs[k].y, factor*surface_normal.y);
            vs[k].z = fmaf(refractive_index_ratio, vs[k].z, factor*surface_normal.z);
        }
        else if (surface_type != DUMMY) // i.e. reflective
        {
            float factor = -2.f * cosine_incident_angle;
            vs[k].x = fmaf(factor, surface_normal.x, vs[k].x);
            vs[k].y = fmaf(factor, surface_normal.y, vs[k].y);
            vs[k].z = fmaf(factor, surface_normal.z, vs[k].z);
        }

        // TODO: it would be better to define a __device__ function for this
        // Gaussian scattering
        if (surface_scattering_dispersions[current_surface] > 0.f) {
            // Scattered vector in the photon local system
            float scattering_angle = surface_scattering_dispersions[current_surface] * sqrtf(-2.f * __logf(curand_uniform(&state)));
            float scattering_azimuth = curand_uniform(&state) * 2.f;

            float sin_theta, cos_theta;
            sincospif(scattering_angle, &sin_theta, &cos_theta);
            float sin_phi, cos_phi;
            sincospif(scattering_azimuth, &sin_phi, &cos_phi);

            float3 v = {sin_theta*cos_phi, -sin_theta*sin_phi, cos_theta};

            // Rotate into the local surface system
            float invnorm = rsqrtf(v.x*v.x + v.y*v.y + v.z*v.z);
            float invden = invnorm / (1.f+vs[k].z);
            float rot[9] = {
                1.f+vs[k].z-vs[k].x*vs[k].x,            -vs[k].x*vs[k].y,                     vs[k].x+vs[k].x*vs[k].z,
                           -vs[k].x*vs[k].y, 1.f+vs[k].z-vs[k].y*vs[k].y,                     vs[k].y+vs[k].y*vs[k].z,
                   -vs[k].x-vs[k].x*vs[k].z,    -vs[k].y-vs[k].y*vs[k].z, 1.f+vs[k].z-vs[k].x*vs[k].x-vs[k].y*vs[k].y};
            vs[k].x = (rot[0]*v.x + rot[1]*v.y + rot[2]*v.z) * invden;
            vs[k].y = (rot[3]*v.x + rot[4]*v.y + rot[5]*v.z) * invden;
            vs[k].z = (rot[6]*v.x + rot[7]*v.y + rot[8]*v.z) * invden;
        }

        // Transform back to the telescope system and look for the next surface
        transform_back(ps[k], vs[k], surface_rotation_matrix, surface_positions[current_surface]);

    } // while
}

/**
 * @brief Simulates atmospheric transmission.
 *
 * This kernel function applies atmospheric transmission rejecting photons based on a 2D transmission curve (wavelength and emission altitude).
 *
 * @param ps Array of photon positions.
 * @param vs Array of photon directions.
 * @param wls Array of photon wavelengths.
 * @param ts Array of photon times.
 * @param weights Array of photon bunch size.
 * @param zems Array of photon zenith angles.
 * @param tr_curves Array containing the 2D transmission curve data.
 * @param tr_curve_wl Array of wavelength values for the transmission curve.
 * @param tr_curve_zem Array of emission altitude values for the transmission curve.
 * @param tr_curve_sizes Array containing the dimensions (x1_size, x2_size) of the 2D transmission curve.  `tr_curve_sizes[0]` is the wavelength size, and `tr_curve_sizes[1]` is the emission altitude size.
 * @param n_ph The total number of photons.
 * 
 */
__global__ void atmospheric_transmission(
    float3* ps,
    float3* vs,
    float* wls,
    float* ts,
    int* weights,
    const float* zems,
    const float* tr_curves,
    const float* tr_curve_wl,
    const float* tr_curve_zem,
    const int* tr_curve_sizes,
    int n_ph
)
{
    int k = blockIdx.x*blockDim.x + threadIdx.x;
    if (k >= n_ph) return;

    // Transmission interpolation
    int x1_size = tr_curve_sizes[0];
    int x2_size = tr_curve_sizes[1];

    // Only one 2D transmission
    int start_x1 = 0;
    int start_x2 = 0;
    int start_curve = 0;

    // tau(wl,zem) interpolate the optical depth curve 
    float tau = unregular_interp2d(
        wls[k],
        zems[k],
        tr_curve_wl,
        tr_curve_zem,
        tr_curves,
        x1_size,
        x2_size,
        start_x1,
        start_x2,
        start_curve
    );

    // Take into account zenith angle
    float transmission = expf(tau/vs[k].z);
    
    // Initialize generator
    curandStatePhilox4_32_10_t state;
    curand_init(clock64(), k, 0, &state);

    // Apply transmission to the bunch
    int bunch_size = weights[k];
    for (int bunch=0; bunch<bunch_size; bunch++) {
        float u = curand_uniform(&state);
        if (u > transmission) weights[k] -= 1;
    }
    
    if (weights[k] < 1) {
        reject_photon(ps[k], vs[k], wls[k], ts[k]);
    }
}

/**
 * @brief Transforms photon positions and directions based on a telescope position and orientation.
 *
 * This kernel performs a coordinate transformation on a set of photons, effectively simulating
 * the observation of those photons by a telescope located at a specific position and 
 * with a specific orientation.  The transformation consists of a translation and a rotation.
 * Is assumed that the altitude axis is not displaced with respect to the azimuth axis and intersect 
 * at the telescope origin.
 *
 * @param ps  An array of float3 representing the positions of the photons.  Modified in-place.
 * @param vs  An array of float3 representing the direction vectors of the photons. Modified in-place.
 * @param p0  A float3 representing the position of the telescope.
 * @param r_mat A float array representing the rotation matrix.
 * @param n_ph The number of photons to transform.
 */
__global__ void telescope_transform(float3* ps, float3* vs, float3 p0, float* r_mat, int n_ph)
{
    int i = blockIdx.x*blockDim.x + threadIdx.x;
    if (i >= n_ph) return;
    
    // Translate position
    ps[i].x -= p0.x;
    ps[i].y -= p0.y;
    ps[i].z -= p0.z;
    
    // Rotate position and direction
    rotate(ps[i], r_mat);
    rotate(vs[i], r_mat);
}

/**
 * @brief Traces photons onto SiPM modules.
 *
 * This kernel function simulates the propagation of photons from the focal plane surface and determines 
 * which pixel on a module each photon hits, taking into account the photon position, direction, 
 * wavelength, and time of arrival. It also incorporates the Photon Detection Efficiency (PDE) 
 * to probabilistically determine if a photon is detected.
 *
 * @param ps Input array of photon positions (x, y, z).
 * @param vs Input array of photon directions (vx, vy, vz).
 * @param wls Input array of photon wavelengths.
 * @param ts Input array of photon arrival times.
 * @param weights Input/output array of photon weights. 
 *                Input: Initial number of photons in the bunch.
 *                Output: Number of photons in the bunch after photon detection.
 * @param pixel_id Output array of pixel IDs for each photon. 
 *                 -1 indicates the photon was rejected or didn't hit a pixel.
 * @param n_ph Total number of photons to be traced.
 * @param modules_p Input array of module positions (x, y, z).
 * @param modules_r Input array of moduleS rotation matrices (3x3 matrices stored as 9 consecutive floats).
 * @param module_half_side Half-side of a square modules.
 * @param pixel_active_side Side length of the active area of a pixel.
 * @param pixels_sep Separation between the active areas of adjacent pixels.
 * @param n_pix_per_side Number of pixels per row/column in a moduleS.
 * @param n_module Number of modules in the system.
 * @param pde_wl Input array of wavelengths for the PDE curve.
 * @param pde_val Input array of PDE values corresponding to `pde_wl`.
 * @param pde_n_points Number of points in the PDE curve.
 * @param pde_inv_step Inverse step size for interpolating the PDE curve (0.0 if not using PDE).
 */
__global__ void trace_onto_sipm_modules(
    float3* ps,
    float3* vs,
    float* wls,
    float* ts,
    int* weights,
    int* pixel_id,
    int n_ph,
    const float3* modules_p,
    const float* modules_r,
    float module_half_side,
    float pixel_active_side, 
    float pixels_sep,
    int n_pix_per_side,
    int n_module,
    const float* pde_wl,
    const float* pde_val,
    int pde_n_points,
    float pde_inv_step,
    // Assuming focal plane is surrounded by a single material (i.e. air)
    const unsigned long long refractive_index_texture, // one for material around focal plane
    const float inv_dwl_refractive_index, // invers of the walength-spacing of refractive index curve
    const float start_wl_refractive_index // start wavelength of refractive index curve
)
{
    // Photon index
    int k = blockIdx.x*blockDim.x + threadIdx.x;
    if (k >= n_ph) return;
    
    if (isnan(ts[k])) {
        pixel_id[k] = -1;
        return;
    }

    // Find the module
    int module = -1;
    float min_dist = 1e9f;
    for (int i=0; i<n_module; i++) {
        // module position and orientation
        float3 module_p = modules_p[i];
        float module_r[9];
        for (int j=0; j<9; j++) {
            module_r[j] = modules_r[i*9 + j];
        }

        // Transform into module reference system
        transform(ps[k], vs[k], module_r, module_p);

        // Distance to module surface
        float d = -ps[k].z/vs[k].z;

        // Position on the module surface
        float dx = fabsf(vs[k].x*d);
        float dy = fabsf(vs[k].y*d);
        
        // Check if the ray hit the module and if it is the nearest module
        if ((min_dist > fabsf(d)) & (dx < module_half_side) & (dy < module_half_side)) {
            min_dist = fabsf(d);
            module = i;
        }

        // Transform into the focal surface reference system
        transform_back(ps[k], vs[k], module_r, module_p);
    }
    
    if (module == -1) {
        reject_photon(ps[k], vs[k], wls[k], ts[k]);
        pixel_id[k] = -1;
        return;
    }

    // Module position and orientation
    float3 module_p = modules_p[module];
    float module_r[9];
    for (int i=0; i<9; i++) {
        module_r[i] = modules_r[module*9 + i];
    }

    // Transform into module reference frame
    transform(ps[k], vs[k], module_r, module_p);

    // Distance to module plane
    float d_to_module = -ps[k].z/vs[k].z;
    
    // Move to module plane and update time
    ps[k].x += vs[k].x*d_to_module;
    ps[k].y += vs[k].y*d_to_module;
    ps[k].z += vs[k].z*d_to_module;

    cudaTextureObject_t texture_ri_out = refractive_index_texture;
    float ri_out = interp1d_text(
        wls[k],
        inv_dwl_refractive_index,
        start_wl_refractive_index,
        texture_ri_out
    );
    // TODO: check focal surface material_in and material_out
    ts[k] += d_to_module * INV_C_LIGHT * ri_out;
    
    // Check if the photon is outside the module
    float dx = abs(ps[k].x);
    float dy = abs(ps[k].y);
    if ((dx > module_half_side) | (dy > module_half_side)) {
        reject_photon(ps[k], vs[k], wls[k], ts[k]);
        pixel_id[k] = -1;
        return;
    }
    
    // Find the pixel
    float on_module_x = ps[k].x + module_half_side;
    float on_module_y = ps[k].y + module_half_side;
    float dpix = pixel_active_side + pixels_sep;
    float i = floorf(on_module_x / dpix);
    float j = floorf(on_module_y / dpix);

    // Check if the photon reaches the unactive region of the pixel
    float x0_right_pix = (i+1.f)*pixel_active_side + i*pixels_sep;
    float y0_up_pix = (j+1.f)*pixel_active_side + j*pixels_sep;
    if ((on_module_x > x0_right_pix) | (on_module_y > y0_up_pix)) {
        reject_photon(ps[k], vs[k], wls[k], ts[k]);
        pixel_id[k] = -1;
        return;
    }

    // Check if the photon is detected
    if (pde_inv_step > 0.f) {
        float this_pde = interp1d(wls[k], pde_wl, pde_val, pde_n_points, pde_inv_step, 0, 0);

        curandStatePhilox4_32_10_t state;
        curand_init(clock64(), k, 0, &state);

        int bunch_size = weights[k];
        for (int bunch_id=0; bunch_id<bunch_size; bunch_id++){
            float u = curand_uniform(&state);
            if (u > this_pde) weights[k] -= 1;
        }
        if (weights[k] < 1) {
            reject_photon(ps[k], vs[k], wls[k], ts[k]);
            pixel_id[k] = -1;
            return;
        }
    }
    
    // Get the pixel ID
    pixel_id[k] = static_cast<int>(module*n_pix_per_side*n_pix_per_side + j*n_pix_per_side + i);

    // Transform into the focal surface reference system
    transform_back(ps[k], vs[k], module_r, module_p);
}


/**
 * @brief Count all photons detected by each pixel. Can be divided in sub-events using :cpp:var:`event_mapping`.
 * 
 * @param weights Number of photons inside each bunch.
 * @param pixel_ids Pixel-id onto each bunch is arriving.
 * @param counters Incremental photon counter of each pixel for each event.
 * @param pix_counters Number of photons for each pixel of each event (n_events*n_pixels).
 * @param event_mapping Position of the first photon of each event inside ts and pixel_ids.
 * @param n_tot Total number of detected photons per event.
 * @param n_pixel Total number of pixels
 * @param n_events Total number of events
 */
__global__ void count_all_photons(const int* weights, const int* pixel_ids, int* counters, int* pix_counters, const int* event_mapping, int* n_tot, const int n_pixel, const int n_events)
{
    // Event index
    int thid = threadIdx.x;
    int event_id = blockIdx.x*blockDim.x + thid;
    if (event_id >= n_events) return;

    int start = event_mapping[event_id];
    int stop = event_mapping[event_id+1];

    __shared__ int shared_n_tot[1024];
    shared_n_tot[thid] = 0;
    
    for (int k=start; k<stop; ++k){
        int pixid = pixel_ids[k];
        if (pixid >= 0) {
            int index = event_id*(n_pixel+1) + pixid+1; // +1 since the first pix_counters value is 0 (to create a phs mapping with cumsum)
            counters[k] = pix_counters[index];
            pix_counters[index] += weights[k];
            shared_n_tot[thid] += weights[k];
            // n_tot[event_id+1] += weights[k];
        }
    }
    n_tot[event_id+1] = shared_n_tot[thid];
}

/**
 * @brief Generate the input for :py:class:`CherenkovCamera`. Can be divided in sub-events using :cpp:var:`event_mapping`.
 * 
 * @param phs Output array with arrival time of each detected photons per pixel.
 * @param mappings Output array with size `n_pixels+1` of first and last arrival time position inside phs for each pixel. E.g. pixel `n` arrival times: ```pes[mapping[n]:mapping[n+1]```.
 * @param ts Array of photon arrival times.
 * @param weights Number of photons inside each bunch.
 * @param pixel_ids Pixel identifier for each photon.
 * @param counters Incremental photon counter of each pixel for each event. Given by :func:`count_all_photons`.
 * @param pe_mapping Auxiliary array to keep track of the photon position inside phs. Is the cumsum of :cpp:var:`n_tot` given by :func:`count_all_photons`.
 * @param event_mapping Position of the first photon of each event inside :cpp:var:`ts` and :cpp:var:`pixel_ids`.
 * @param n_pixel Total number of pixels.
 * @param n_events Total number of events.
 *
 */
__global__ void camera_inputs(float* phs, const int* mappings, const float* ts, const int* weights, const int* pixel_ids, const int* counters, const int* pe_mapping, const int* event_mapping, const int n_pixel, const int n_events)
{
    int event_id = blockIdx.x*blockDim.x + threadIdx.x;
    if (event_id >= n_events) return;

    int pe_start = pe_mapping[event_id];
    int pe_stop = pe_mapping[event_id+1];
    if (pe_stop-pe_start == 0) return;

    int event_start = event_mapping[event_id];
    int event_stop = event_mapping[event_id+1];
    if (event_stop-event_start == 0) return;

    for (int k=event_start; k<event_stop; ++k){
        int pixid = pixel_ids[k];
        if (pixid < 0) continue;

        int index = mappings[event_id*(n_pixel+1) + pixid] + pe_start + counters[k];
        
        for (int i=0; i<weights[k]; ++i){
            phs[index+i] = ts[k];
        }
    }
}

} // extern C