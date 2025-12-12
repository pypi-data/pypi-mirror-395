import re
from copy import deepcopy

import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import savgol_filter
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform
import skrf as rf

def select_angles_maxvol(data_matrix, n_angles=4):
    """Select angles using Maximum Volume (MaxVol) algorithm

    This method selects rows that maximize the determinant of the submatrix,
    ensuring maximum linear independence.

    Args:
        data_matrix: Matrix where each row is an angle's features
        n_angles: Number of angles to select

    Returns:
        List of selected angle indices
    """
    n_total = data_matrix.shape[0]

    # Start with PCA to reduce dimensionality while preserving variance
    from sklearn.decomposition import PCA
    pca = PCA(n_components=min(n_angles, data_matrix.shape[0], data_matrix.shape[1]))
    data_reduced = pca.fit_transform(data_matrix)

    selected = []
    remaining = list(range(n_total))

    # Select first angle: the one with maximum norm in PCA space
    norms = np.linalg.norm(data_reduced, axis=1)
    first_idx = np.argmax(norms)
    selected.append(first_idx)
    remaining.remove(first_idx)

    # Iteratively select angles that maximize the volume
    for _ in range(n_angles - 1):
        max_vol = -1
        best_idx = None

        for idx in remaining:
            # Try adding this angle
            test_indices = selected + [idx]
            test_matrix = data_reduced[test_indices, :]

            # Calculate volume (absolute determinant if square, or based on singular values)
            if test_matrix.shape[0] <= test_matrix.shape[1]:
                vol = abs(np.linalg.det(test_matrix @ test_matrix.T))
            else:
                U, S, Vt = np.linalg.svd(test_matrix, full_matrices=False)
                vol = np.prod(S)

            if vol > max_vol:
                max_vol = vol
                best_idx = idx

        if best_idx is not None:
            selected.append(best_idx)
            remaining.remove(best_idx)

    return selected

def select_angles_greedy_distance(dist_matrix, n_angles=4, start_idx=None):
    """Select angles using greedy maximum distance algorithm

    Args:
        dist_matrix: Distance matrix between angles
        n_angles: Number of angles to select
        start_idx: Optional starting angle index

    Returns:
        List of selected angle indices
    """
    n_total = dist_matrix.shape[0]

    if start_idx is None:
        # Start with the angle that has maximum mean distance to all others
        mean_distances = np.mean(dist_matrix, axis=1)
        start_idx = np.argmax(mean_distances)

    selected = [start_idx]
    remaining = list(range(n_total))
    remaining.remove(start_idx)

    for _ in range(n_angles - 1):
        max_min_dist = -1
        best_idx = None

        for idx in remaining:
            # Find minimum distance to already selected angles
            min_dist = min([dist_matrix[idx, sel] for sel in selected])

            if min_dist > max_min_dist:
                max_min_dist = min_dist
                best_idx = idx

        if best_idx is not None:
            selected.append(best_idx)
            remaining.remove(best_idx)

    return selected

def select_angles_condition_number(data_matrix, n_angles=4):
    """Select angles to minimize condition number (maximize numerical stability)

    Args:
        data_matrix: Matrix where each row is an angle's features
        n_angles: Number of angles to select

    Returns:
        List of selected angle indices
    """
    n_total = data_matrix.shape[0]

    # Normalize data
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    data_norm = scaler.fit_transform(data_matrix.T).T

    selected = []
    remaining = list(range(n_total))

    # Start with angle having maximum norm
    norms = np.linalg.norm(data_norm, axis=1)
    first_idx = np.argmax(norms)
    selected.append(first_idx)
    remaining.remove(first_idx)

    # Select angles that minimize condition number
    for _ in range(n_angles - 1):
        best_cond = float('inf')
        best_idx = None

        for idx in remaining:
            test_indices = selected + [idx]
            test_matrix = data_norm[test_indices, :]

            # Calculate condition number
            try:
                U, S, Vt = np.linalg.svd(test_matrix, full_matrices=False)
                if S[-1] > 1e-10:  # Avoid division by zero
                    cond = S[0] / S[-1]
                else:
                    cond = float('inf')

                if cond < best_cond:
                    best_cond = cond
                    best_idx = idx
            except:
                continue

        if best_idx is not None:
            selected.append(best_idx)
            remaining.remove(best_idx)

    return selected

def calculate_selection_quality(selected_angles, data_matrix, dist_matrix):
    """Calculate quality metrics for selected angles

    Returns:
        dict: Dictionary with quality metrics
    """
    metrics = {}

    # 1. Mean pairwise distance
    pairwise_dists = []
    for i, idx1 in enumerate(selected_angles):
        for idx2 in selected_angles[i + 1:]:
            pairwise_dists.append(dist_matrix[idx1, idx2])
    metrics['mean_distance'] = np.mean(pairwise_dists)
    metrics['min_distance'] = np.min(pairwise_dists)

    # 2. Condition number
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    data_norm = scaler.fit_transform(data_matrix.T).T
    selected_data = data_norm[selected_angles, :]
    U, S, Vt = np.linalg.svd(selected_data, full_matrices=False)
    metrics['condition_number'] = S[0] / S[-1] if S[-1] > 1e-10 else float('inf')

    # 3. Determinant (volume)
    if selected_data.shape[0] <= selected_data.shape[1]:
        metrics['determinant'] = abs(np.linalg.det(selected_data @ selected_data.T))
    else:
        metrics['determinant'] = np.prod(S)

    # 4. Explained variance (PCA)
    from sklearn.decomposition import PCA
    pca_all = PCA(n_components=len(selected_angles))
    pca_all.fit(data_matrix)
    pca_selected = PCA(n_components=len(selected_angles))
    pca_selected.fit(selected_data)
    metrics['variance_ratio'] = np.sum(pca_selected.explained_variance_ratio_)

    return metrics


def smoothing(s_param, window_length, polyorder):
    """Apply Savitzky-Golay smoothing"""
    s_real = savgol_filter(np.real(s_param), window_length, polyorder)
    s_imag = savgol_filter(np.imag(s_param), window_length, polyorder)
    return s_real + 1j * s_imag


def extract_features(network):
    """Extract features from S-parameters"""
    s11_mag = np.abs(network.s[:, 0, 0])
    s11_phase = np.angle(network.s[:, 0, 0])
    s21_mag = np.abs(network.s[:, 1, 0])
    s21_phase = np.angle(network.s[:, 1, 0])

    features = np.concatenate([s11_mag, s11_phase, s21_mag, s21_phase])
    return features


def parse_s2p_filename(filename):
    """Extract angle from S2P filename

    Supports formats like:
    - angle_10_50.s2p (10.50°)
    - angle_-5_25.s2p (-5.25°)
    - angle_0_00.s2p (0.00°)

    Returns:
        float: angle in degrees, or None if parsing fails
    """
    # Pattern: angle_{int}_{dec}.s2p or angle_{-int}_{dec}.s2p
    pattern = r'.*?(-?\d+)-(\d+).*?\.s2p'
    match = re.search(pattern, filename)

    if match:
        int_part = int(match.group(1))
        dec_part = int(match.group(2))
        angle = int_part + dec_part / 100.0
        return angle

    return None


def find_angle_pairs(data_folder):
    """Automatically find S2P files and pair positive/negative angles

    Args:
        data_folder: Path to folder containing S2P files

    Returns:
        dict: {abs_angle: {'positive': angle, 'negative': angle, 'files': [pos_file, neg_file]}}
    """
    all_files = [f for f in os.listdir(data_folder) if f.endswith('.s2p')]

    angles_dict = {}
    angles = []
    for filename in all_files:
        angle = parse_s2p_filename(filename)
        if angle is not None:
            abs_angle = abs(angle)
            angles.append(abs_angle)
            if abs_angle not in angles_dict:
                angles_dict[abs_angle] = []
            angles_dict[abs_angle].append(filename)

    angles_dict = dict(sorted(angles_dict.items()))
    if 0 in angles_dict.keys():
        if len(angles_dict[0]) == 1:
            angles_dict[0].append(angles_dict[0][0])
    return angles_dict

def load_parameters(filepath1, filepath2, smoothing_window, smoothing_poly):
    mut1 = rf.Network(filepath1)
    mut2 = rf.Network(filepath2)
    _s21 = .25 * (mut1.s[:, 1, 0] + mut1.s[:, 0, 1] + mut2.s[:, 1, 0] + mut2.s[:, 0, 1])
    _s11 = .5 * (mut1.s[:, 0, 0] + mut2.s[:, 0, 0])
    _s22 = .5 * (mut1.s[:, 1, 1] + mut2.s[:, 1, 1])
    s = np.zeros_like(mut1.s, dtype=complex)
    s[:, 0, 0] = _s11
    s[:, 1, 0] = _s21
    s[:, 0, 1] = _s21
    s[:, 1, 1] = _s22
    s2 = deepcopy(s)
    s2[:, 0, 0] = smoothing(_s11, smoothing_window, smoothing_poly)
    s2[:, 1, 0] = smoothing(_s21, smoothing_window, smoothing_poly)
    s2[:, 0, 1] = smoothing(_s21, smoothing_window, smoothing_poly)
    s2[:, 1, 1] = smoothing(_s22, smoothing_window, smoothing_poly)
    return rf.Network(s=s, f=mut1.f, f_unit='Hz'), rf.Network(s=s2, f=mut1.f, f_unit='Hz')


def analyze_angle_independence(data_folder, n_angles_to_select=3,
                               use_pairs=True, smoothing_window=71, smoothing_poly=5):
    """Analyze information independence between angles with automatic file detection

    Args:
        data_folder: Path to folder containing S2P files
        n_angles_to_select: Number of angles to select
        use_pairs: If True, use both positive and negative angles; if False, use only positive
        smoothing_window: Window length for Savitzky-Golay filter
        smoothing_poly: Polynomial order for Savitzky-Golay filter

    Returns:
        tuple or None if no files found
    """

    print("=" * 70)
    print("AUTOMATIC ANGLE ANALYSIS")
    print("=" * 70)
    print(f"\nSearching for S2P files in: {os.path.abspath(data_folder)}")

    # Find angle pairs automatically
    angle_pairs = find_angle_pairs(data_folder)

    if len(angle_pairs) == 0:
        print(f"\nERROR: No S2P files found!")
        print(f"Expected filename pattern: xxx{{int}}-{{dec}}xxx.s2p")
        print(f"Examples: ang10-50.s2p")
        return None

    print(f"\nFound {len(angle_pairs)} angle pair(s):")

    print("\nLoading data with scikit-rf...")
    data_matrix = []
    valid_angles = []
    networks = []
    raw_networks = []

    # Load S2P files
    for abs_angle in sorted(angle_pairs.keys()):
        pair = angle_pairs[abs_angle]

        path1 = os.path.join(data_folder, pair[0])
        path2 = os.path.join(data_folder, pair[1])
        try:
            read_networks = load_parameters(path1, path2, smoothing_window, smoothing_poly)
            features = extract_features(read_networks[1])
            print(f"  ✓ Loaded: angle {abs_angle}° ({len(read_networks[0].f)} frequency points)")
            data_matrix.append(features)
            valid_angles.append(abs_angle)
            raw_networks.append(read_networks[0])
            networks.append(read_networks[1])
        except Exception as e:
            print(f"  ✗ Error reading {path1}: {e}")

    if n_angles_to_select == 1:
        s2p_raw_networks_array = [raw_networks[0]]
        s2p_networks_array = [networks[0]]
        return (0,), s2p_raw_networks_array, s2p_networks_array, np.array((1,)), (None, None, networks, None, angle_pairs)


    if len(data_matrix) == 0:
        print(f"\nERROR: No data could be loaded!")
        return None

    data_matrix = np.asarray(data_matrix)
    print(f"\n{'=' * 70}")
    print(f"Data loaded successfully:")
    print(f"  - Total angles: {len(valid_angles)}")
    print(f"  - Angle range: {min(valid_angles):.2f}° to {max(valid_angles):.2f}°")
    print(f"  - Feature dimensions: {data_matrix.shape}")
    print(f"  - Frequency range: {networks[0].f[0] / 1e9:.2f} - {networks[0].f[-1] / 1e9:.2f} GHz")
    print(f"{'=' * 70}")

    # Continue with correlation and selection analysis
    print("\n=== Calculating Correlation and Distance Matrices ===")
    corr_matrix = np.corrcoef(data_matrix)
    dist_matrix = 1 - np.abs(corr_matrix)

    # Method 1: MaxVol (Maximum Volume)
    print("\n=== METHOD 1: MaxVol (Maximum Volume) ===")
    selected_maxvol = select_angles_maxvol(data_matrix, n_angles_to_select)
    print("Selected angles:", [valid_angles[i] for i in selected_maxvol])
    metrics_maxvol = calculate_selection_quality(selected_maxvol, data_matrix, dist_matrix)

    # Method 2: Greedy Distance
    print("\n=== METHOD 2: Greedy Maximum Distance ===")
    selected_greedy = select_angles_greedy_distance(dist_matrix, n_angles_to_select)
    print("Selected angles:", [valid_angles[i] for i in selected_greedy])
    metrics_greedy = calculate_selection_quality(selected_greedy, data_matrix, dist_matrix)

    # Method 3: Condition Number Minimization
    print("\n=== METHOD 3: Minimum Condition Number ===")
    selected_condnum = select_angles_condition_number(data_matrix, n_angles_to_select)
    print("Selected angles:", [valid_angles[i] for i in selected_condnum])
    metrics_condnum = calculate_selection_quality(selected_condnum, data_matrix, dist_matrix)

    # Compare methods
    print("\n" + "=" * 70)
    print("COMPARISON OF SELECTION METHODS")
    print("=" * 70)

    methods = {
        'MaxVol': (selected_maxvol, metrics_maxvol),
        'Greedy Distance': (selected_greedy, metrics_greedy),
        'Min CondNum': (selected_condnum, metrics_condnum)
    }

    print(f"\n{'Method':<20} {'Mean Dist':<12} {'Min Dist':<12} {'Cond Num':<12} {'Det/Vol':<12}")
    print("-" * 70)
    for method_name, (sel, met) in methods.items():
        print(f"{method_name:<20} {met['mean_distance']:<12.4f} {met['min_distance']:<12.4f} "
              f"{met['condition_number']:<12.2f} {met['determinant']:<12.2e}")

    # Recommend best method
    print("\n" + "=" * 70)
    print("RECOMMENDATION")
    print("=" * 70)

    # Score each method
    scores = {}
    for method_name, (sel, met) in methods.items():
        score = (
                met['mean_distance'] * 2.0 +
                met['min_distance'] * 2.0 +
                (1.0 / met['condition_number'] if met['condition_number'] < 1e6 else 0) * 1.0
        )
        scores[method_name] = score

    best_method = max(scores, key=scores.get)
    best_selection, best_metrics = methods[best_method]

    # best_selection : indices des angles sélectionnés
    sub_dist = dist_matrix[np.ix_(best_selection, best_selection)]
    sub_networks = networks  # liste des réseaux S-parameters

    alpha = 0.5
    quality_signal = []

    for ii in best_selection:
        s21 = networks[ii].s[:, 1, 0]  # S21 pour cet angle
        # qualité = inverse de la variance absolue du signal
        quality_signal.append(1 / (np.std(np.abs(s21)) + 1e-12))

    quality_signal = np.array(quality_signal)
    quality_signal = (quality_signal - np.min(quality_signal)) / (np.ptp(quality_signal) + 1e-12)

    # indépendance
    mean_distances = np.mean(sub_dist, axis=1)
    mean_distances = (mean_distances - np.min(mean_distances)) / (np.ptp(mean_distances) + 1e-12)

    # combinaison
    weights = alpha * mean_distances + (1 - alpha) * quality_signal
    weights /= np.sum(weights)

    print(f"\nBest method: {best_method}")
    print(f"Selected angles: {[f'{valid_angles[i]:+.2f}°' for i in best_selection]}")
    print(f"\nQuality metrics:")
    print(f"  - Mean pairwise distance: {best_metrics['mean_distance']:.4f}")
    print(f"  - Minimum pairwise distance: {best_metrics['min_distance']:.4f}")
    print(f"  - Condition number: {best_metrics['condition_number']:.2f} "
          f"{'(excellent)' if best_metrics['condition_number'] < 10 else '(good)' if best_metrics['condition_number'] < 100 else '(acceptable)' if best_metrics['condition_number'] < 1000 else '(poor)'}")
    print(f"  - Determinant/Volume: {best_metrics['determinant']:.2e}")

    print("\nWeights for selected angles (relative independence):")
    for a, w in zip([valid_angles[i] for i in best_selection], weights):
        print(f"  Angle {a:+6.2f}°  →  weight = {w:.3f}")

    s2p_networks_array = []
    s2p_raw_networks_array = []
    for valid_angle in best_selection:
        s2p_raw_networks_array.append(raw_networks[valid_angle])
        s2p_networks_array.append(networks[valid_angle])
    return np.asarray(valid_angles)[best_selection], s2p_raw_networks_array, s2p_networks_array, weights, (valid_angles, dist_matrix, networks, methods, angle_pairs)

# Usage
if __name__ == "__main__":
    data_folder = "./s2p/pvc-air-pa6_sim/"
    filename_pattern = "pvc-air-pa6_ang{:02d}-{:02d}_000.s2p"

    angles_deg = np.linspace(0, 40, 41, endpoint=True)
    result = analyze_angle_independence(data_folder, angles_deg, filename_pattern=filename_pattern)

    if result is not None:
        best_sel, angles, dist_mat, networks, methods = result

        print("\n" + "=" * 70)
        print("FINAL RECOMMENDATION")
        print("=" * 70)
        print(f"\nOptimal angles for parameter estimation: {[angles[i] for i in best_sel]}")
        print("\nThese angles maximize information independence and numerical stability")
        print("for solving your 4-parameter inverse problem.")

    else:
        print("\nAnalysis aborted due to missing files.")

    plt.show()