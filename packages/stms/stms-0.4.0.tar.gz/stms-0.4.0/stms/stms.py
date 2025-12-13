# SPATIOTEMPORAL FILLING - MULTISTEP SMOOTHING DATA RECONSTRUCTION
# Author: Bayu Suseno <bayu.suseno@outlook.com>

import numpy as np
from pygam import LinearGAM, s
from tqdm.auto import tqdm
import math
import time
from numba import njit

@njit(cache=True)
def best_window_corr(
    vi_target,
    cloud_target,
    vi_cand,
    cloud_cand,
    threshold_cloudy,
    step_min,
    step_max
):
    n_t = vi_target.shape[0]
    n_c = vi_cand.shape[0]

    if n_c < n_t:
        dummy_vi = np.zeros(n_t, dtype=np.float64)
        dummy_mask = np.zeros(n_t, dtype=np.bool_)
        return -1.0, dummy_vi, dummy_mask, dummy_mask

    filter_target_hi = cloud_target > threshold_cloudy
    filter_target_lo = cloud_target <= threshold_cloudy

    best_corr = -1.0
    best_start = 0

    first_row = 0
    end_row = n_t

    while end_row <= n_c:
        filter_hi = filter_target_hi * (cloud_cand[first_row:end_row] > threshold_cloudy)
        filter_pred = filter_target_lo * (cloud_cand[first_row:end_row] > threshold_cloudy)

        if np.sum(filter_hi) >= np.sum(filter_target_hi) / 2 and np.sum(filter_pred) > 0:
            x = vi_target[filter_hi]
            y = vi_cand[first_row:end_row][filter_hi]

            mx = np.mean(x)
            my = np.mean(y)
            num = 0.0
            denx = 0.0
            deny = 0.0

            for k in range(x.shape[0]):
                dx = x[k] - mx
                dy = y[k] - my
                num += dx * dy
                denx += dx * dx
                deny += dy * dy

            if denx > 0 and deny > 0:
                corr = num / np.sqrt(denx * deny)
            else:
                corr = 0.0

            if corr > best_corr:
                best_corr = corr
                best_start = first_row

        # adaptive step
        corr_use = max(0.0, min(1.0, best_corr))
        step = int(step_max - corr_use * (step_max - step_min))
        if step < step_min:
            step = step_min
        if step > step_max:
            step = step_max

        first_row += step
        end_row += step

    best_end = best_start + n_t

    return (
        best_corr,
        vi_cand[best_start:best_end],
        filter_target_hi * (cloud_cand[best_start:best_end] > threshold_cloudy),
        filter_target_lo * (cloud_cand[best_start:best_end] > threshold_cloudy),
    )



@njit
def _compute_distance_norm(loc_lat, loc_lon, lat_all, lon_all):
    """
    Numba-accelerated: compute normalized inverse distance from (loc_lat, loc_lon)
    to each (lat_all[i], lon_all[i]).
    """
    n = lat_all.shape[0]
    dist = np.empty(n, np.float64)

    for i in range(n):
        dlat = loc_lat - lat_all[i]
        dlon = loc_lon - lon_all[i]
        d = math.sqrt(dlat * dlat + dlon * dlon)
        if d == 0.0:
            d = 1e-7
        dist[i] = d

    inv = 1.0 / dist
    inv_min = inv[0]
    inv_max = inv[0]
    for i in range(1, n):
        if inv[i] < inv_min:
            inv_min = inv[i]
        if inv[i] > inv_max:
            inv_max = inv[i]

    denom = inv_max - inv_min
    out = np.empty(n, np.float64)

    if denom <= 0:
        for i in range(n):
            out[i] = 1.0
    else:
        for i in range(n):
            v = (inv[i] - inv_min) / denom
            if v <= 0.0:
                v = 1e-7
            out[i] = abs(v)

    return out

#@njit
def find_intervals_one_series(filter_cloud, n_consecutive, n_tail):
    starts = []
    ends = []
    cons_temp = 0
    cons_max = 0
    n = len(filter_cloud)
    for j in range(n):
        if filter_cloud[j] and j < n - 1:
            cons_temp += 1
        elif filter_cloud[j] and j == n - 1:
            cons_max = cons_temp + 1
            cons_temp = 0
            if cons_max >= n_consecutive:
                start_idx = max(0, j - cons_max - n_tail + 1)
                end_idx = min(n, j + n_tail + 1)
                starts.append(start_idx)
                ends.append(end_idx)
        else:
            cons_max = cons_temp
            cons_temp = 0
            if cons_max >= n_consecutive:
                start_idx = max(0, j - cons_max - n_tail + 1)
                end_idx = min(n, j + n_tail + 1)
                starts.append(start_idx)
                ends.append(end_idx)
    return np.array(starts), np.array(ends)

@njit
def _build_poly3_design(x):
    """
    Build design matrix for cubic polynomial:
    columns = [1, x, x^2, x^3]
    """
    n = x.shape[0]
    X = np.empty((n, 4), dtype=np.float64)
    for i in range(n):
        xi = x[i]
        X[i, 0] = 1.0
        X[i, 1] = xi
        X[i, 2] = xi * xi
        X[i, 3] = xi * xi * xi
    return X


@njit
def _poly3_fit_numba(x, y):
    """
    Ordinary least squares cubic regression using the normal equations:
    beta = (X^T X)^(-1) X^T y
    """
    X = _build_poly3_design(x)
    XtX = X.T @ X
    Xty = X.T @ y

    eps = 1e-7
    for d in range(4):
        XtX[d, d] += eps

    beta = np.linalg.solve(XtX, Xty)
    return beta  


@njit
def _poly3_predict_numba(x, beta):
    """
    Evaluate cubic polynomial with coefficients beta on x.
    beta = [b0, b1, b2, b3]
    """
    n = x.shape[0]
    y_pred = np.empty(n, dtype=np.float64)
    b0, b1, b2, b3 = beta[0], beta[1], beta[2], beta[3]
    for i in range(n):
        xi = x[i]
        y_pred[i] = b0 + b1 * xi + b2 * xi * xi + b3 * xi * xi * xi
    return y_pred


def update_cloud_and_vi(
    vi_values,
    vi_smooth,
    cloud_init_sample,
    cloud_values,
    threshold,
    vi_min,
    vi_max,
):
    """
    Update vi_values and cloud_values for a single smoothing threshold.
    Returns (vi_values_new, cloud_values_new, ok_flag).
    ok_flag=False means "stop smoothing for this series".
    """
    vi_s = vi_smooth.copy()

    if vi_max is not None:
        vi_s[vi_s > vi_max] = vi_max
    if vi_min is not None:
        vi_s[vi_s < vi_min] = vi_min

    vi_diff = vi_s - vi_values
    diff_min = np.min(vi_diff)
    diff_max = np.max(vi_diff)
    diff_range = diff_max - diff_min

    if diff_range == 0 or not np.isfinite(diff_range):
        return vi_values, cloud_values, False

    cloud_new = np.abs((vi_diff - diff_min) / diff_range)
    cloud_new[cloud_new == 0] = 1e-7

    mask_hi = (cloud_init_sample > threshold) & (cloud_new <= cloud_init_sample)
    mask_lo = (cloud_init_sample <= threshold) & (cloud_new > cloud_init_sample)
    cloud_new[mask_hi] = cloud_init_sample[mask_hi]
    cloud_new[mask_lo] = cloud_init_sample[mask_lo]

    vi_new = vi_values.copy()
    mask_replace = (cloud_init_sample <= threshold)
    vi_new[mask_replace] = vi_s[mask_replace]

    return vi_new, cloud_new, True


def poly3_fit_and_predict(x_full, x_fit, y_fit):
    """
    Safe cubic polynomial fit with automatic fallback to linear.
    """
    x_fit = np.asarray(x_fit, dtype=np.float64)
    y_fit = np.asarray(y_fit, dtype=np.float64)
    x_full = np.asarray(x_full, dtype=np.float64)

    if x_fit.size < 6 or np.std(x_fit) < 1e-6:
        # Fallback to linear
        coef = np.polyfit(x_fit, y_fit, 1)
        y_pred = np.polyval(coef, x_full)
        return coef, y_pred

    beta = _poly3_fit_numba(x_fit, y_fit)
    y_pred = _poly3_predict_numba(x_full, beta)

    return beta, y_pred


class stms:
    """
    Spatiotemporal Filling - Multistep Smoothing (STMS) for reconstructing
    satellite-derived vegetation index (VI) time series data in cloud-prone regions.
    
    This class performs:
    - Automatic detection of long cloudy gaps in VI time series.
    - Spatiotemporal filling using nearby spatial samples with high temporal
      similarity and low cloud contamination.
    - Iterative multistep temporal smoothing using Generalized Additive Models (GAM)
      with adaptive quality reweighting.
    - Optional value clipping for any vegetation index (NDVI, EVI, NDRE, etc.).
    
    STMS is fully data-agnostic and supports any vegetation index or environmental
    time series with spatial coordinates and quality weights.
    
    Parameters
    ----------
    n_spline : int, default=20
        Number of spline basis functions used in GAM smoothing.
    
    smoothing_min : float, default=0.1
        Minimum quality threshold used in the first smoothing iteration.
    
    smoothing_max : float, default=1.0
        Maximum quality threshold used in the final smoothing iteration.
    
    smoothing_steps : int, default=6
        Total number of smoothing iterations. The thresholds between
        `smoothing_min` and `smoothing_max` are generated automatically
        using either linear or geometric spacing.
    
    smoothing_strategy : {"linear", "geometric"}, default="geometric"
        Strategy used to generate the sequence of smoothing thresholds.
        - "linear"  : equally spaced thresholds
        - "geometric": multiplicative spacing (faster early refinement)
    
    lamdas : array-like
        Regularization parameters tested during GAM grid search.
    
    vi_max : float or None, default=None
        Optional maximum allowable value for VI predictions.
        If None, no upper clipping is applied.
    
    vi_min : float or None, default=None
        Optional minimum allowable value for VI predictions.
        If None, no lower clipping is applied.
    
    n_consecutive : int, default=7
        Minimum number of consecutive cloudy observations required to trigger
        spatiotemporal reconstruction.
    
    n_tail : int, default=24
        Padding length (in time steps) added before and after a detected cloudy gap.
    
    threshold_cloudy : float, default=0.1
        Quality threshold below which an observation is considered contaminated
        (e.g., cloudy).
    
    threshold_corr : float, default=0.9
        Minimum Pearson correlation required for a candidate series to be accepted
        as a spatial donor.
    
    n_candidate : int or None, default=None
        Maximum number of spatial donor series used per gap (global cap).
        If None, all accepted candidates are used.
    
    n_candidate_nested : int or None, default=None
        Maximum number of accepted candidates per nested group
        (e.g., per field or administrative unit). Only active if `id_nested` is given.
    
    candidate_sampling : {"distance", "random"}, default="distance"
        Strategy used to order candidate donors:
        - "distance": nearest neighbors first
        - "random"  : random order (optionally stratified by nested groups)
    
    max_candidate_pool : int or None, default=None
        Maximum number of candidate series that are *tested* during
        spatiotemporal filling. If None, all series are tested.
    
    step_min : int, default=1
        Minimum step size of the sliding window used for candidate correlation search
        (fine search).
    
    step_max : int, default=6
        Maximum step size of the sliding window used for candidate correlation search
        (coarse search).
    
    Notes
    -----
    - Spatiotemporal reconstruction is accelerated using Numba for:
      distance computation, correlation search, and polynomial regression.
    - Multistep smoothing relies on GAM and cannot be fully JIT-compiled,
      but its iteration count is controlled by `smoothing_steps` for efficiency.
    - Optional `target_ids` allow partial reconstruction of selected subsegments only.
    """


    def __init__(
        self,
        n_spline=20,
        smoothing_min=0.05,
        smoothing_max=1.0,
        smoothing_steps=6,              
        smoothing_mode="geometric",
        lamdas=np.logspace(-3, 2, 30),
        vi_max=None,             
        vi_min=None,             
        n_consecutive=7,
        n_tail=24,
        threshold_cloudy=0.1,
        threshold_corr=0.9,
        n_candidate=None,            
        n_candidate_nested=None,     
        candidate_sampling="distance",
        max_candidate_pool=None,     
        step_min=1,                  
        step_max=6,                  
    ):
        self.n_spline = n_spline
        self.smoothing_min = smoothing_min
        self.smoothing_max = smoothing_max
        self.smoothing_steps = smoothing_steps
        self.smoothing_mode = smoothing_mode
        self.lamdas = lamdas
        self.vi_max = vi_max
        self.vi_min = vi_min
        self.n_consecutive = n_consecutive
        self.n_tail = n_tail
        self.threshold_cloudy = threshold_cloudy
        self.threshold_corr = threshold_corr
        self.n_candidate = n_candidate
        self.n_candidate_nested = n_candidate_nested
        self.candidate_sampling = candidate_sampling
        self.max_candidate_pool = max_candidate_pool
        self.step_min = step_min
        self.step_max = step_max

    # ------------------------------------------------------------------
    # spatiotemporal_filling
    # ------------------------------------------------------------------
    def spatiotemporal_filling(
        self,
        id_sample,
        days_data,
        vi_data,
        long_data,
        lati_data,
        cloud_data,
        id_nested=None,
        candidate_sampling=None,
        max_candidate_pool=None,
        target_ids=None,
    ):
        """
        Reconstructs VI values in intervals with prolonged cloudy conditions by using nearby
        samples with similar temporal patterns.
        """
        vi_raw = vi_data.copy()
    
        # Unique IDs for all time series
        idsamp_unique = np.unique(id_sample)
    
        id_start = {}
        id_end = {}
        for sid in idsamp_unique:
            mask = (id_sample == sid)
            idx = np.where(mask)[0]
            id_start[sid] = idx[0]
            id_end[sid] = idx[-1] + 1

        if target_ids is None:
            idsamp_target = idsamp_unique
        else:
            target_ids = np.asarray(target_ids)
            target_set = set(target_ids)
            idsamp_target = np.array([sid for sid in idsamp_unique if sid in target_set])
    
        if candidate_sampling is None:
            candidate_sampling = self.candidate_sampling
        if max_candidate_pool is None:
            max_candidate_pool = self.max_candidate_pool
    
        nested_by_id = None
        if id_nested is not None:
            nested_by_id = {}
            for sid in idsamp_unique:
                nested_by_id[sid] = id_nested[id_sample == sid][0]
    
        lat_by_id = {}
        lon_by_id = {}
        for sid in idsamp_unique:
            mask = (id_sample == sid)
            lat_by_id[sid] = lati_data[mask][0]
            lon_by_id[sid] = long_data[mask][0]
        
        lat_all_vector = np.empty(len(idsamp_unique), dtype=np.float64)
        lon_all_vector = np.empty(len(idsamp_unique), dtype=np.float64)
        for idx, sid in enumerate(idsamp_unique):
            lat_all_vector[idx] = lat_by_id[sid]
            lon_all_vector[idx] = lon_by_id[sid]

    
        # ------------------------------------------------------------------
        # STEP 1. Finding series with consecutive cloudy condition
        # ------------------------------------------------------------------
        id_gap_list = []
        days_gap_list = []
        long_gap_list = []
        lati_gap_list = []
        vi_gap_list = []
        cloud_gap_list = []
    
        for i in tqdm(idsamp_target, desc="STEP 1. Gap Detection"):
            time.sleep(0.1)
            mask = (id_sample == i)
            id_values = id_sample[mask]
            days_values = days_data[mask]
            long_values = long_data[mask]
            lati_values = lati_data[mask]
            vi_values = vi_data[mask]
            cloud_values = cloud_data[mask]
    
            filter_cloud = (cloud_values <= self.threshold_cloudy)
            cons_temp = 0
            cons_max = 0
            for j in range(len(filter_cloud)):
                if filter_cloud[j]:
                    cons_temp += 1
                else:
                    cons_temp = 0
                if cons_temp > cons_max:
                    cons_max = cons_temp
    
            if cons_max >= self.n_consecutive:
                id_gap_list.append(id_values)
                days_gap_list.append(days_values)
                long_gap_list.append(long_values)
                lati_gap_list.append(lati_values)
                vi_gap_list.append(vi_values)
                cloud_gap_list.append(cloud_values)

        if len(id_gap_list) > 0:
            id_gap = np.concatenate(id_gap_list)
            days_gap = np.concatenate(days_gap_list)
            long_gap = np.concatenate(long_gap_list)
            lati_gap = np.concatenate(lati_gap_list)
            vi_gap = np.concatenate(vi_gap_list)
            cloud_gap = np.concatenate(cloud_gap_list)
        else:
            return vi_data
            
        # STEP 2. Creating target interval
        unique_ids_with_gap = np.unique(id_gap)
        
        count = 1
        unique_int = np.empty(0, dtype=int)
        id_int = np.empty(0, dtype=object)
        days_int = np.empty(0, dtype=int)
        long_int = np.empty(0, dtype=float)
        lati_int = np.empty(0, dtype=float)
        vi_int = np.empty(0, dtype=float)
        cloud_int = np.empty(0, dtype=float)
        
        # ------------------------------------------------------------------
        # STEP 2. Creating target interval
        # ------------------------------------------------------------------
        id_int_list = []
        unique_int_list = []
        days_int_list = []
        long_int_list = []
        lati_int_list = []
        vi_int_list = []
        cloud_int_list = []

        for sid in tqdm(unique_ids_with_gap, desc="STEP 2. Target Interval Construction"):
            mask = (id_gap == sid)
            id_values = id_gap[mask]
            days_values = days_gap[mask]
            long_values = long_gap[mask]
            lati_values = lati_gap[mask]
            vi_values = vi_gap[mask]
            cloud_values = cloud_gap[mask]
            filter_cloud = (cloud_values <= self.threshold_cloudy)

            starts, ends = find_intervals_one_series(
                filter_cloud.astype(np.bool_),
                self.n_consecutive,
                self.n_tail,
            )

            for s_idx, e_idx in zip(starts, ends):
                id_temp = id_values[s_idx:e_idx]
                days_temp = days_values[s_idx:e_idx]
                long_temp = long_values[s_idx:e_idx]
                lati_temp = lati_values[s_idx:e_idx]
                vi_temp = vi_values[s_idx:e_idx]
                cloud_temp = cloud_values[s_idx:e_idx]

                unique_temp = np.full(id_temp.shape[0], count, dtype=int)
                count += 1

                id_int_list.append(id_temp)
                unique_int_list.append(unique_temp)
                days_int_list.append(days_temp)
                long_int_list.append(long_temp)
                lati_int_list.append(lati_temp)
                vi_int_list.append(vi_temp)
                cloud_int_list.append(cloud_temp)

        if len(id_int_list) == 0:
            # no intervals to reconstruct
            print("\nNo target intervals found. Returning original vi_data.")
            return vi_data

        id_int = np.concatenate(id_int_list)
        unique_int = np.concatenate(unique_int_list)
        days_int = np.concatenate(days_int_list)
        long_int = np.concatenate(long_int_list)
        lati_int = np.concatenate(lati_int_list)
        vi_int = np.concatenate(vi_int_list)
        cloud_int = np.concatenate(cloud_int_list)

        n_intervals = len(np.unique(unique_int))
        
        # ------------------------------------------------------------------
        # STEP 3. Spatiotemporal filling
        # ------------------------------------------------------------------
        unique_intervals = np.unique(unique_int)
        for uid in tqdm(unique_intervals, desc="STEP 3. Spatiotemporal filling"):
            mask_int = (unique_int == uid)
            id_target = id_int[mask_int]
            days_target = days_int[mask_int]
            long_target = long_int[mask_int]
            lati_target = lati_int[mask_int]
            vi_target = vi_int[mask_int]
            cloud_target = cloud_int[mask_int]

            vi_cand_pred_all = np.empty(0, dtype=float)
            weight_cand_pred_all = np.empty(0, dtype=float)
            distance_cand_all = np.empty(0, dtype=float)
            corr_cand_all = np.empty(0, dtype=float)
            vi_cand_all = np.empty(0, dtype=float)
            filter_cand_all = np.empty(0, dtype=int)
            filterpred_cand_all = np.empty(0, dtype=int)

            loc_lat = float(lati_target[0])
            loc_lon = float(long_target[0])
            filter_target_lo = (cloud_target <= self.threshold_cloudy)
            filter_target_hi = (cloud_target > self.threshold_cloudy)

            distance_norm = _compute_distance_norm(
                loc_lat,
                loc_lon,
                lat_all_vector,
                lon_all_vector,
            )

            index_distance = np.argsort(distance_norm)
            base_ids = idsamp_unique[index_distance]
            base_ids = base_ids[base_ids != id_target[0]]

            if candidate_sampling == "random":
                if nested_by_id is not None:
                    groups = {}
                    seg_order = []
                    for sid in base_ids:
                        seg = nested_by_id[sid]
                        if seg not in groups:
                            groups[seg] = []
                            seg_order.append(seg)
                        groups[seg].append(sid)
                    cand_list = []
                    for seg in seg_order:
                        arr = np.array(groups[seg])
                        arr = np.random.permutation(arr)
                        cand_list.append(arr)
                    if len(cand_list) > 0:
                        cand_ids = np.concatenate(cand_list)
                    else:
                        cand_ids = np.array([], dtype=base_ids.dtype)
                else:
                    cand_ids = np.random.permutation(base_ids)
            else:
                cand_ids = base_ids

            if (max_candidate_pool is not None) and (len(cand_ids) > max_candidate_pool):
                cand_ids = cand_ids[:max_candidate_pool]

            nested_counts = {}  

            for k in cand_ids:
                if (nested_by_id is not None) and (self.n_candidate_nested is not None):
                    seg_k = nested_by_id[k]
                    if nested_counts.get(seg_k, 0) >= self.n_candidate_nested:
                        continue

                mask_cand = (id_sample == k)
                vi_cand = vi_raw[mask_cand]
                cloud_cand = cloud_data[mask_cand]

                distance_cand = distance_norm[idsamp_unique == k]

                best_corr, vi_cand_temp, filter_temp, filter_pred_temp = best_window_corr(
                    vi_target.astype(np.float64),
                    cloud_target.astype(np.float64),
                    vi_cand.astype(np.float64),
                    cloud_cand.astype(np.float64),
                    self.threshold_cloudy,
                    self.step_min,
                    self.step_max,
                )

                if best_corr >= self.threshold_corr:
                    distance_cand_all = np.append(distance_cand_all, distance_cand)
                    corr_cand_all = np.append(corr_cand_all, best_corr)
                    vi_cand_all = np.append(vi_cand_all, vi_cand_temp)
                    filter_cand_all = np.append(filter_cand_all, filter_temp.astype(int))
                    filterpred_cand_all = np.append(filterpred_cand_all, filter_pred_temp.astype(int))

                    if (nested_by_id is not None) and (self.n_candidate_nested is not None):
                        seg_k = nested_by_id[k]
                        nested_counts[seg_k] = nested_counts.get(seg_k, 0) + 1

                if (self.n_candidate is not None) and (len(corr_cand_all) == self.n_candidate):
                    break

            n_cand = len(corr_cand_all)
            if n_cand > 0:
                L = len(vi_target)
                vi_cand_pred_all = np.empty(n_cand * L, dtype=float)
                weight_cand_pred_all = np.empty(n_cand * L, dtype=float)

                for idx_cand in range(n_cand):
                    distance_cand_temp = distance_cand_all[idx_cand]
                    corr_cand_temp = corr_cand_all[idx_cand]

                    start = idx_cand * L
                    end = (idx_cand + 1) * L

                    vi_cand_temp = vi_cand_all[start:end]
                    filter_cand_temp = filter_cand_all[start:end]
                    filterpred_cand_temp = filterpred_cand_all[start:end]

                    x_fit = vi_cand_temp[filter_cand_temp == 1]
                    y_fit = vi_target[filter_cand_temp == 1]

                    _, vi_cand_pred = poly3_fit_and_predict(
                        x_full=vi_cand_temp,
                        x_fit=x_fit,
                        y_fit=y_fit,
                    )

                    if self.vi_max is not None:
                        vi_cand_pred[vi_cand_pred > self.vi_max] = self.vi_max
                    if self.vi_min is not None:
                        vi_cand_pred[vi_cand_pred < self.vi_min] = self.vi_min

                    vi_cand_pred[filterpred_cand_temp == 0] = 0.0

                    vi_cand_pred_fin = vi_cand_pred * corr_cand_temp * distance_cand_temp
                    weight_cand_pred = filterpred_cand_temp * corr_cand_temp * distance_cand_temp
                    weight_cand_pred[filterpred_cand_temp == 0] = 0.0

                    vi_cand_pred_all[start:end] = vi_cand_pred_fin
                    weight_cand_pred_all[start:end] = weight_cand_pred

                vi_pred_sum = np.nansum(
                    np.split(vi_cand_pred_all, n_cand),
                    axis=0,
                )
                filterpred_sum = np.nansum(
                    np.split(filterpred_cand_all, n_cand),
                    axis=0,
                )
                weight_pred_sum = np.nansum(
                    np.split(weight_cand_pred_all, n_cand),
                    axis=0,
                )

                vi_pred_fin = np.divide(
                    vi_pred_sum,
                    weight_pred_sum,
                    out=vi_target.copy(),
                    where=weight_pred_sum > 0,
                )

                if (self.vi_max is not None) or (self.vi_min is not None):
                    bad_mask = np.zeros_like(vi_pred_fin, dtype=bool)
                    if self.vi_max is not None:
                        bad_mask |= vi_pred_fin > self.vi_max
                    if self.vi_min is not None:
                        bad_mask |= vi_pred_fin < self.vi_min
                    vi_pred_fin[bad_mask] = vi_target[bad_mask]

                for m in days_target[filterpred_sum > 0]:
                    vi_data[
                        (id_sample == id_target[0]) & (days_data == m)
                    ] = vi_pred_fin[days_target == m]

        return vi_data



    # ------------------------------------------------------------------
    # multistep_smoothing
    # ------------------------------------------------------------------
    def multistep_smoothing(self, id_sample, days_data, vi_data, cloud_data, target_ids=None):
        """
        Applies iterative GAM-based smoothing on each time series.

        Uses a sequence of cloud thresholds between smoothing_min and smoothing_max.
        The number of steps is controlled by `self.smoothing_steps`, and the spacing
        can be 'linear' or 'geometric'.
        """
        idsamp_unique = np.unique(id_sample)

        if target_ids is None:
            idsamp_target = idsamp_unique
        else:
            target_ids = np.asarray(target_ids)
            target_set = set(target_ids)
            idsamp_target = np.array([sid for sid in idsamp_unique if sid in target_set])

        if self.smoothing_steps <= 1:
            thresholds = np.array([self.smoothing_max], dtype=float)
        else:
            if self.smoothing_mode == "geometric":
                start = max(self.smoothing_min, 1e-3)
                stop = max(self.smoothing_max, start + 1e-3)
                thresholds = np.geomspace(start, stop, self.smoothing_steps)
            else:
                thresholds = np.linspace(self.smoothing_min, self.smoothing_max, self.smoothing_steps)

        cloud_init = cloud_data.copy()

        for i in tqdm(idsamp_target, desc="Multistep Temporal Smoothing"):
            mask = (id_sample == i)
            days_values = days_data[mask]
            vi_values = vi_data[mask]
            cloud_init_sample = cloud_init[mask]
            cloud_values = cloud_data[mask]

            if len(np.unique(days_values)) < 5:
                continue
            if np.nanstd(vi_values) == 0:
                continue

            cloud_values = np.asarray(cloud_values, dtype=float)
            cloud_values[cloud_values <= 0] = 1e-6
            X = days_values.reshape(-1, 1)

            for thr in thresholds:
                try:
                    gam = LinearGAM(s(0), n_splines=self.n_spline)
                    gam = gam.gridsearch(
                        X,
                        vi_values,
                        weights=cloud_values,
                        lam=self.lamdas,
                        objective="GCV",
                        progress=False,
                    )
                    vi_smooth = gam.predict(days_values)
                except LinAlgError:
                    print(f"GAM failed for id {i} (skipping this series)")
                    break

                vi_values, cloud_values, ok = update_cloud_and_vi(
                    vi_values, vi_smooth,
                    cloud_init_sample, cloud_values,
                    thr, self.vi_min, self.vi_max
                )
                if not ok:
                    break

            vi_data[mask] = vi_values

        return vi_data

