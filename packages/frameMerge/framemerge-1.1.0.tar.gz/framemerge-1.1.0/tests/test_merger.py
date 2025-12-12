import os
import tempfile

import h5py
import numpy as np
import pytest

from frameMerge.helpers import (
    _hadamard_encode_chunk_sq,
    _rolling_merge_sq,
    generate_s_matrix,
)
from frameMerge.merger import Merger


def create_test_hdf5(num_frames=6, shape=(2, 2), dtype=np.int32):
    tmpfile = tempfile.NamedTemporaryFile(suffix=".h5", delete=False)
    with h5py.File(tmpfile.name, "w") as f:
        entry = f.create_group("entry")
        data_grp = entry.create_group("data")
        dset = data_grp.create_dataset("data", shape=(num_frames, *shape), dtype=dtype)
        for i in range(num_frames):
            dset[i] = np.full(shape, i, dtype=dtype)
    return tmpfile.name


def test_generate_s_matrix():
    S = generate_s_matrix(3)
    assert S.shape == (3, 3)
    assert np.all((S == 0) | (S == 1))

    n = 3
    JN = np.ones((n, n))
    ST = S.T
    Sinv = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Sinv[i][j] = 2.0 * (2.0 * ST[i][j] - JN[i][j]) / (n + 1)

    identity = np.dot(S, Sinv)
    np.testing.assert_allclose(identity, np.eye(n), atol=1e-10)


def test_hadamard_encoding_patterns_differ():
    file_name = create_test_hdf5(num_frames=3, shape=(4, 4))

    merger = Merger(
        file_name=file_name,
        output_file="test_hadamard.h5",
        n_frames=3,
        n_merged_frames=3,
        data_location="entry/data",
        data_name="data",
        type="hadamard",
    )
    merger._open_and_load()

    S = generate_s_matrix(3)
    encoded = _hadamard_encode_chunk_sq(
        merger.data_array,
        merger.n_frames,
        merger.n_merged_frames,
        merger.frame_shape,
        S,
        merger.dtype,
    )

    assert encoded.shape == (3, 1, 4, 4)
    assert not np.array_equal(encoded[0, 0], encoded[1, 0])
    assert not np.array_equal(encoded[1, 0], encoded[2, 0])
    assert not np.array_equal(encoded[0, 0], encoded[2, 0])

    os.remove(file_name)


def test_hadamard_perfect_reconstruction():
    file_name = create_test_hdf5(num_frames=3, shape=(4, 4), dtype=np.float64)

    merger = Merger(
        file_name=file_name,
        output_file="test_hadamard.h5",
        n_frames=3,
        n_merged_frames=3,
        data_location="entry/data",
        data_name="data",
        type="hadamard",
    )
    merger._open_and_load()
    original_frames = merger.data_array.copy()

    S = generate_s_matrix(3)
    encoded = _hadamard_encode_chunk_sq(
        merger.data_array,
        merger.n_frames,
        merger.n_merged_frames,
        merger.frame_shape,
        S,
        dtype=np.float64,
    )

    n = 3
    JN = np.ones((n, n))
    ST = S.T
    Sinv = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Sinv[i][j] = 2.0 * (2.0 * ST[i][j] - JN[i][j]) / (n + 1)

    decoded = np.zeros_like(original_frames)
    for frame_idx in range(n):
        for pattern_idx in range(n):
            decoded[frame_idx] += Sinv[frame_idx, pattern_idx] * encoded[pattern_idx, 0]

    np.testing.assert_allclose(decoded, original_frames, rtol=1e-10, atol=1e-10)

    os.remove(file_name)


def test_hadamard_end_to_end(tmp_path):
    file_name = create_test_hdf5(num_frames=6, shape=(4, 4))
    output_file = tmp_path / "hadamard_merged.h5"

    merger = Merger(
        file_name=file_name,
        output_file=str(output_file),
        n_frames=6,
        n_merged_frames=3,
        data_location="entry/data",
        data_name="data",
        type="hadamard",
        n_workers=1,
    )
    merger.process(parallel=False)

    base_path = str(output_file).rsplit(".h5", 1)[0]
    file_110 = f"{base_path}_110.h5"
    file_101 = f"{base_path}_101.h5"
    file_011 = f"{base_path}_011.h5"

    assert os.path.exists(file_110), f"Expected {file_110}"
    assert os.path.exists(file_101), f"Expected {file_101}"
    assert os.path.exists(file_011), f"Expected {file_011}"

    with h5py.File(file_110, "r") as f:
        assert "entry/data/data" in f
        pattern0 = f["entry/data/data"][:]
        assert pattern0.shape[0] == 2  # 6 frames / 3 = 2 bunches
        assert f["entry/data"].attrs["encoding_type"] == "hadamard"

    with h5py.File(file_101, "r") as f:
        pattern1 = f["entry/data/data"][:]
        assert pattern1.shape[0] == 2

    with h5py.File(file_011, "r") as f:
        pattern2 = f["entry/data/data"][:]
        assert pattern2.shape[0] == 2

    assert not np.array_equal(pattern0, pattern1)
    assert not np.array_equal(pattern1, pattern2)
    assert not np.array_equal(pattern0, pattern2)

    os.remove(file_name)
    os.remove(file_110)
    os.remove(file_101)
    os.remove(file_011)


def test_invalid_n_merged_frames():
    file_name = create_test_hdf5(num_frames=6)

    with pytest.raises(ValueError, match="must be prime"):
        merger = Merger(
            file_name=file_name,
            output_file="test.h5",
            n_frames=6,
            n_merged_frames=4,
            type="hadamard",
        )
        merger.validate_inputs()

    with pytest.raises(ValueError, match="n ≡ 3"):
        merger = Merger(
            file_name=file_name,
            output_file="test.h5",
            n_frames=6,
            n_merged_frames=5,
            type="hadamard",
        )
        merger.validate_inputs()

    os.remove(file_name)


def test_rolling_merge_pattern_skip_1():
    file_name = create_test_hdf5(num_frames=6)
    merger = Merger(
        file_name=file_name,
        output_file="test_merged.h5",
        n_frames=6,
        n_merged_frames=3,
        skip_pattern=[1],
        data_location="entry/data",
        data_name="data",
        type="rolling",
    )
    merger._open_and_load()

    merged = _rolling_merge_sq(
        merger.data_array,
        merger.n_frames,
        merger.n_merged_frames,
        merger.frame_shape,
        merger.skip_pattern,
        merger.dtype,
    )

    expected_0 = merger.data_array[0] + merger.data_array[2]
    expected_1 = merger.data_array[3] + merger.data_array[5]

    np.testing.assert_array_equal(merged[0], expected_0)
    np.testing.assert_array_equal(merged[1], expected_1)

    os.remove(file_name)


def test_rolling_merge_pattern_skip_2():
    file_name = create_test_hdf5(num_frames=6)
    merger = Merger(
        file_name=file_name,
        output_file="test_merged.h5",
        n_frames=6,
        n_merged_frames=3,
        skip_pattern=[2],
        data_location="entry/data",
        data_name="data",
        type="rolling",
    )
    merger._open_and_load()

    merged = _rolling_merge_sq(
        merger.data_array,
        merger.n_frames,
        merger.n_merged_frames,
        merger.frame_shape,
        merger.skip_pattern,
        merger.dtype,
    )

    expected_0 = merger.data_array[0] + merger.data_array[1]
    expected_1 = merger.data_array[3] + merger.data_array[4]

    np.testing.assert_array_equal(merged[0], expected_0)
    np.testing.assert_array_equal(merged[1], expected_1)

    os.remove(file_name)


def test_rolling_end_to_end(tmp_path):
    file_name = create_test_hdf5(num_frames=6)
    output_file = tmp_path / "merged.h5"

    merger = Merger(
        file_name=file_name,
        output_file=str(output_file),
        n_frames=6,
        n_merged_frames=3,
        skip_pattern=[1],
        data_location="entry/data",
        data_name="data",
        type="rolling",
        n_workers=1,
    )
    merger.process(parallel=False)
    assert os.path.exists(output_file)

    with h5py.File(output_file, "r") as f:
        merged_data = f["entry/data/data"][:]
        assert merged_data.shape[0] == 2
        assert np.all(merged_data[0] == 0 + 2)
        assert np.all(merged_data[1] == 3 + 5)

    os.remove(file_name)
