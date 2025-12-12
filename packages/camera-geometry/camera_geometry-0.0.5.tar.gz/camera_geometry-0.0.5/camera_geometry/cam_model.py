from __future__ import annotations

import json
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np


class LineSample:
    """Represents a sampled warped vertical line.

    Attributes:
        midscreen_x: optional x coordinate where the sample crosses image midline.
        points: list of (x, y) tuples sampled along the line.
    """

    def __init__(self, midscreen_x: float | None = None, points: Sequence[Tuple[int, int]] | None = None):
        self.midscreen_x = None if midscreen_x is None else float(midscreen_x)
        self.points = [] if points is None else [(int(x), int(y)) for x, y in points]


def fit_line_models(samples: Sequence[LineSample], deg_y: int = 5, deg_m: int = 3) -> Dict[str, Any]:
    mids: List[float] = []
    coeffs: List[np.ndarray] = []

    for s in samples:
        if s.midscreen_x is None:
            continue
        pts = s.points
        if len(pts) < 2:
            continue
        ys = np.array([p[1] for p in pts], dtype=float)
        xs = np.array([p[0] for p in pts], dtype=float)
        eff_deg_y = min(deg_y, max(1, len(xs) - 1))
        try:
            c = np.polyfit(ys, xs, eff_deg_y)
        except Exception:
            continue
        if len(c) < deg_y + 1:
            pad = np.zeros((deg_y + 1 - len(c),), dtype=float)
            c = np.concatenate([pad, c])
        coeffs.append(c)
        mids.append(float(s.midscreen_x))

    if len(coeffs) == 0:
        raise ValueError("No usable samples with midscreen_x found")

    coeffs_arr = np.vstack(coeffs)
    mids_arr = np.array(mids, dtype=float)

    coef_funcs: List[List[float]] = []
    for j in range(coeffs_arr.shape[1]):
        yvals = coeffs_arr[:, j]
        c = np.polyfit(mids_arr, yvals, deg_m)
        coef_funcs.append(c.tolist())

    return {"deg_y": deg_y, "deg_m": deg_m, "coef_funcs": coef_funcs}


def save_model(model: Dict[str, Any], path: str) -> None:
    with open(path, "w") as f:
        json.dump(model, f, indent=2)


def load_model(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def generate_line_from_model(midscreen_x: float, y_values: np.ndarray, model: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    coef_funcs = np.array(model["coef_funcs"], dtype=float)
    coeffs = [np.polyval(coef_funcs[j], midscreen_x) for j in range(coef_funcs.shape[0])]
    xs = np.polyval(coeffs, y_values)
    return np.asarray(xs, dtype=float), np.asarray(coeffs, dtype=float)


def _coeffs_for_mids_x(coef_funcs: np.ndarray, mids_x: float) -> List[float]:
    return [np.polyval(coef_funcs[j], mids_x) for j in range(coef_funcs.shape[0])]


def pix_to_elevation_angle(x, y, model: Dict[str, Any], camera_fov_deg: float, im_width: int, img_height: int) -> float:
    x = float(x)
    y = float(y)
    im_w = float(im_width)
    im_h = float(img_height)

    if not isinstance(model, dict) or "coef_funcs" not in model:
        raise ValueError('model must be a dict containing "coef_funcs"')

    coef_funcs = np.array(model["coef_funcs"], dtype=float)
    deg_y = int(model.get("deg_y", coef_funcs.shape[0] - 1))

    poly_in_n = [np.poly1d(coef_funcs[j]) for j in range(coef_funcs.shape[0])]

    x_pows = [(x ** (deg_y - j)) for j in range(len(poly_in_n))]
    H = np.poly1d([0.0])
    for j, polyn in enumerate(poly_in_n):
        H = H + polyn * x_pows[j]
    H = H - y

    n_param = None
    try:
        roots_n = np.roots(H.coeffs)
        real_ns = [float(np.real(r)) for r in roots_n if np.isreal(r) and -1e-6 <= float(np.real(r)) <= im_h + 1e-6]
        if real_ns:
            center_n = im_h / 2.0
            n_param = float(min(real_ns, key=lambda v: abs(v - center_n)))
    except Exception:
        n_param = None

    if n_param is None:
        grid = np.linspace(0.0, im_h - 1.0, 1001)
        vals = np.zeros_like(grid)
        for j, polyn in enumerate(poly_in_n):
            vals += polyn(grid) * x_pows[j]
        idx = int(np.argmin(np.abs(vals - y)))
        n_param = float(grid[idx])

    center_x = im_w / 2.0
    y_at_center = sum(np.polyval(coef_funcs[j], n_param) * (center_x ** (deg_y - j)) for j in range(len(coef_funcs)))

    def _find_mids_x_for_vertical(x0: float, y0: float) -> float | None:
        poly_in_m = [np.poly1d(coef_funcs[j]) for j in range(coef_funcs.shape[0])]
        y_pows = [(y0 ** (deg_y - j)) for j in range(len(poly_in_m))]
        p_m = np.poly1d([0.0])
        for j, polyj in enumerate(poly_in_m):
            p_m = p_m + polyj * y_pows[j]
        q = p_m - x0
        if np.allclose(q.coeffs, 0):
            return None
        try:
            roots = np.roots(q.coeffs)
            real_roots = [float(np.real(r)) for r in roots if np.isreal(r) and -1e-6 <= float(np.real(r)) <= im_w + 1e-6]
            if real_roots:
                center = im_w / 2.0
                return float(min(real_roots, key=lambda r: abs(r - center)))
        except Exception:
            pass
        grid = np.linspace(0.0, im_w - 1.0, 1001)
        vals = np.zeros_like(grid)
        for j, polyj in enumerate(poly_in_m):
            vals += polyj(grid) * y_pows[j]
        idx = int(np.argmin(np.abs(vals - x0)))
        return float(grid[idx])

    def _elevation_for_vertical_point(x0: float, y0: float) -> float:
        mids_x = _find_mids_x_for_vertical(x0, y0)
        if mids_x is None:
            frac = ((im_h / 2.0) - y0) / (im_h / 2.0)
            ang = frac * float(camera_fov_deg)
            return float(max(-abs(camera_fov_deg), min(abs(camera_fov_deg), ang)))
        ys_full = np.arange(0, int(im_h))
        coeffs_y = _coeffs_for_mids_x(coef_funcs, mids_x)
        xs_full = np.polyval(coeffs_y, ys_full)
        pts = np.stack([xs_full, ys_full], axis=1)
        deltas = np.diff(pts, axis=0)
        seg_dists = np.sqrt((deltas ** 2).sum(axis=1))
        cum = np.concatenate(([0.0], np.cumsum(seg_dists)))
        idx_mid = int(np.argmin(np.abs(ys_full - (im_h / 2.0))))
        idx_pix = int(np.argmin(np.abs(ys_full - y0)))
        total_top = float(cum[idx_mid])
        if total_top <= 1e-9:
            frac = ((im_h / 2.0) - y0) / (im_h / 2.0)
        else:
            dist_pix = abs(cum[idx_mid] - cum[idx_pix])
            frac = dist_pix / total_top
            if idx_pix > idx_mid:
                frac = -frac
        ang = frac * float(camera_fov_deg)
        ang = max(-abs(camera_fov_deg), min(abs(camera_fov_deg), ang))
        return float(ang)

    elev = _elevation_for_vertical_point(center_x, y_at_center)
    return float(elev) / 2.0


def pixels_along_model_line(model: Dict[str, Any], azimuth_deg: float, im_width: int, im_height: int, camera_fov_deg: float) -> np.ndarray:
    center_x = float(im_width) / 2.0
    mids_x = center_x + (float(azimuth_deg) / float(camera_fov_deg)) * center_x
    ys = np.arange(0, int(im_height))
    xs, _ = generate_line_from_model(float(mids_x), ys, model)
    pts = np.vstack([xs, ys]).T
    pts[:, 0] = np.clip(np.round(pts[:, 0]).astype(int), 0, int(im_width) - 1)
    pts[:, 1] = np.clip(np.round(pts[:, 1]).astype(int), 0, int(im_height) - 1)
    uniq = [tuple(pts[0].tolist())]
    for p in pts[1:]:
        t = (int(p[0]), int(p[1]))
        if t != uniq[-1]:
            uniq.append(t)
    return np.asarray(uniq, dtype=int)
