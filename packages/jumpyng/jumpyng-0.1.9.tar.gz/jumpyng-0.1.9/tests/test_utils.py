import numpy as np
import pandas as pd
import pytest

import jumpyng.utils as utils
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Inject the expected statsmodels handles that the utils module references.
utils.sm = sm
utils.ols = ols


class _FakeSpine:
    def __init__(self):
        self.visible = True

    def set_visible(self, flag):
        self.visible = flag


class _FakeSpineCollection(list):
    def set_visible(self, flag):
        for spine in self:
            spine.set_visible(flag)


class _FakeSpines(dict):
    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            return _FakeSpineCollection([super().__getitem__(name) for name in item])
        return super().__getitem__(item)


class _FakeAxisTicks:
    def __init__(self):
        self.position = None
        self.visible = True

    def set_ticks_position(self, pos):
        self.position = pos

    def set_visible(self, flag):
        self.visible = flag


class _FakeAxes:
    def __init__(self):
        self.spines = _FakeSpines({key: _FakeSpine() for key in ("right", "top", "left", "bottom")})
        self.xaxis = _FakeAxisTicks()
        self.yaxis = _FakeAxisTicks()
        self._lines = []
        self._labels = {}
        self._limits = {}
        self._ticks = {}

    def plot(self, *args, **kwargs):
        self._lines.append(("plot", args, kwargs))
        return self._lines

    def vlines(self, *args, **kwargs):
        self._lines.append(("vlines", args, kwargs))

    def fill_between(self, *args, **kwargs):
        self._lines.append(("fill_between", args, kwargs))

    def legend(self, *args, **kwargs):
        self._labels["legend"] = (args, kwargs)

    def set_xlabel(self, label):
        self._labels["xlabel"] = label

    def set_ylabel(self, label):
        self._labels["ylabel"] = label

    def set_title(self, title):
        self._labels["title"] = title

    def set_xlim(self, *args, **kwargs):
        if args:
            self._limits["x"] = tuple(args)
        else:
            self._limits["x"] = kwargs

    def set_ylim(self, *args, **kwargs):
        if args:
            self._limits["y"] = tuple(args)
        else:
            self._limits["y"] = kwargs

    def errorbar(self, *args, **kwargs):
        self._lines.append(("errorbar", args, kwargs))

    def axis(self, params):
        self._limits["axis"] = tuple(params)

    def set_xticks(self, ticks):
        self._ticks["x"] = tuple(ticks)

    def set_yticks(self, ticks):
        self._ticks["y"] = tuple(ticks)

    def get_xaxis(self):
        return self.xaxis

    def get_yaxis(self):
        return self.yaxis

    def ravel(self):
        return np.array([self])


class _FakeFigure:
    def __init__(self, axes):
        self.axes = axes
        self.suptitle_text = ""

    def tight_layout(self):
        return None

    def suptitle(self, text):
        self.suptitle_text = text


def _fake_axes_grid(nrows, ncols):
    axes = np.empty((nrows, ncols), dtype=object)
    for i in range(nrows):
        for j in range(ncols):
            axes[i, j] = _FakeAxes()
    if nrows == 1 and ncols == 1:
        axes_out = axes[0, 0]
    elif nrows == 1 or ncols == 1:
        axes_out = axes.reshape(-1)
    else:
        axes_out = axes
    return _FakeFigure(axes), axes_out


class _FakePyplot:
    @staticmethod
    def subplots(nrows=1, ncols=1, **_):
        return _fake_axes_grid(nrows, ncols)

    @staticmethod
    def tight_layout():
        return None

    @staticmethod
    def close(_=None):
        return None

    @staticmethod
    def suptitle(*_, **__):
        return None


class _FakePdfPages:
    def __init__(self, path):
        self.path = path
        self.saved = []

    def savefig(self, fig):
        self.saved.append(fig)

    def close(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


utils.plt = _FakePyplot()
utils.PdfPages = _FakePdfPages


def test_file_search_helpers(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    (root / "sample.txt").write_text("hello")
    (root / "experiment_filtered.h5").write_text("x")
    (root / "report_filtered.h5").write_text("y")
    (root / "report_summary_filtered.h5").write_text("z")
    (root / "nested").mkdir()
    (root / "nested" / "2024_mouse_condition_TOP_0.avi").write_text("avi")

    txt_matches = utils.find("*.txt", str(root))
    assert str(root / "sample.txt") in txt_matches

    assert utils.findSingle("sample.txt", str(root)) == str(root / "sample.txt")
    assert utils.findSingle("missing.txt", str(root)) is None

    single = utils.findFileStrings(["experiment", "filtered"], str(root))
    assert single == str(root / "experiment_filtered.h5")

    multiple = utils.findFileStrings(["report", "filtered"], str(root))
    assert set(multiple) == {
        str(root / "report_filtered.h5"),
        str(root / "report_summary_filtered.h5"),
    }

    partial = utils.findSinglePartial(["2024", "condition"], str(root), suffix="TOP_0.avi")
    assert partial.endswith("TOP_0.avi")

    assert utils.findSinglePartial(["not-there"], str(root)) is None


def test_truncate_and_xy_axis():
    assert utils.truncate_float(3.14159, 2) == 3.14
    fig, ax = utils.plt.subplots(1, 1)
    result_ax = utils.xy_axis(ax)
    assert not result_ax.spines["right"].visible
    assert not result_ax.spines["top"].visible
    assert result_ax.yaxis.position == "left"
    assert result_ax.xaxis.position == "bottom"


def test_interpolate_movement_handles_nans():
    arr = np.array([0.0, np.nan, 6.0, np.nan, 10.0])
    interpolated = utils.interpolateMovement(arr)
    assert not np.isnan(interpolated).any()
    assert interpolated[-1] == pytest.approx(10.0)


def test_load_dlc_h5_functions(monkeypatch):
    columns = pd.MultiIndex.from_tuples(
        [
            ("scorer", "nose", "x"),
            ("scorer", "nose", "y"),
            ("scorer", "nose", "likelihood"),
        ]
    )
    base_df = pd.DataFrame([[1.0, 2.0, 0.9], [3.0, 4.0, 0.1]], columns=columns)

    filter_df = pd.DataFrame([[10.0, 12.0, 0.4], [10.0, 20.0, 0.8]], columns=columns)

    def fake_read_hdf(path):
        if "filter" in path:
            return filter_df.copy()
        return base_df.copy()

    monkeypatch.setattr(utils.pd, "read_hdf", fake_read_hdf)

    loaded = utils.load_dlc_h5("something.h5")
    assert list(loaded.columns) == ["nose x", "nose y", "nose likelihood"]

    filtered = utils.load_dlc_h5_filter("path_filter.h5", like_thresh=0.5, pix_per_cm=2.0)
    assert filtered["nose x"].iloc[0] == pytest.approx(5.0)
    assert filtered["nose y"].iloc[0] == pytest.approx(10.0)


def test_dlc_to_groupdf(monkeypatch, tmp_path):
    data = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "subject": ["A", "B"],
            "condition": ["control", "stim"],
            "trial_num": [1, 2],
        }
    )

    pts_columns = ["nose x", "nose y"]
    pts_df = pd.DataFrame({"nose x": [1.0, 2.0], "nose y": [3.0, 4.0]})

    orig_dataframe = utils.pd.DataFrame

    def df_factory(*args, **kwargs):
        df_obj = orig_dataframe(*args, **kwargs)
        if kwargs.get("columns") is not None and list(kwargs["columns"]) == pts_columns:
            return df_obj.astype(object)
        return df_obj

    def fake_find_file_strings(substrings, _):
        if "A_" in substrings:
            return ["loop_a.h5"]
        if "A" in substrings:
            return "initial_a.h5"
        if "B_" in substrings:
            return []
        return "initial_b.h5"

    read_calls = []

    def fake_read_hdf(path):
        read_calls.append(path)
        return pts_df.copy()

    saved_frames = []

    def fake_to_hdf(self, path, key):
        saved_frames.append((self.copy(), path, key))

    monkeypatch.setattr(utils, "findFileStrings", fake_find_file_strings)
    monkeypatch.setattr(utils.pd, "read_hdf", fake_read_hdf)
    monkeypatch.setattr(utils.pd.DataFrame, "to_hdf", fake_to_hdf, raising=False)
    monkeypatch.setattr(utils, "tqdm", lambda iterable, **_: iterable)
    monkeypatch.setattr(utils.pd, "DataFrame", df_factory)

    result = utils.dlc_to_groupdf(data.copy(), "experiment", tmp_path)

    assert "nose x" in result.columns
    assert isinstance(result.loc[0, "nose x"], np.ndarray)
    assert pd.isna(result.loc[1, "nose x"])
    assert saved_frames[0][1].endswith("dlc_df.h5")


def test_outcome_helpers():
    vec = np.array([0.1, 0.4, 0.9])
    assert utils.find_first(0.5, vec) == 1

    df = pd.DataFrame({"outcome": [0, 1, 2, 2], "extra": [1, 2, 3, 4]})
    failures = utils.aborts_as_failures(df)
    assert list(failures["outcome"]) == [0, 1, 0, 0]

    cleaned = utils.remove_aborts(df)
    assert 2 not in cleaned["outcome"].values
    assert len(cleaned) == 2


def test_video_helpers(monkeypatch):
    row = pd.Series({"date": "2024-01-01", "subject": "mouse", "condition": "ctrl", "trial_num": 3})

    monkeypatch.setattr(utils, "find", lambda name, path: [f"{path}/{name}"])
    vid_names = utils.get_vidname_from_row(row, "videos")
    assert vid_names[0].endswith(".avi")

    monkeypatch.setattr(utils, "find", lambda name, path: [f"{path}/{name}"])
    dlc_names = utils.get_dlcname_from_row(row, "videos")
    assert dlc_names[0].endswith("_filtered.h5")

    frame = utils.get_vid_frame("dummy.avi", 5)
    assert frame.shape == (2, 2, 3)

    gerbil_row = pd.Series(
        {"date": "2024-01-01", "subject": "g1", "condition": "ctrl", "sex": "M", "trial_num": 2}
    )
    monkeypatch.setattr(utils, "findSingle", lambda name, path: f"{path}/{name}")
    gerbil = utils.get_gerbil_vidname_from_row(gerbil_row, "gerbil_videos")
    assert gerbil.endswith(".avi")


def test_detect_video_syntax(monkeypatch):
    monkeypatch.setattr(
        utils,
        "find",
        lambda pattern, path: [f"{path}/2024_mouse_M_jumping_light_TOP_0.avi"],
    )
    syntax = utils._detect_video_syntax("experiment")
    assert "{sex}" in syntax

    monkeypatch.setattr(
        utils,
        "find",
        lambda pattern, path: [f"{path}/2024_mouse_light_TOP_0.avi"],
    )
    syntax_no_sex = utils._detect_video_syntax("experiment")
    assert "{sex}" not in syntax_no_sex

    monkeypatch.setattr(utils, "find", lambda pattern, path: [])
    with pytest.raises(FileNotFoundError):
        utils._detect_video_syntax("experiment")


def test_get_unambiguous_vidname_from_row(monkeypatch):
    row = pd.Series({"date": "2024", "subject": "mouse", "condition": "light", "trial_num": 2, "sex": "F"})

    monkeypatch.setattr(utils, "_detect_video_syntax", lambda path: "{date}_{subject}_{condition}_TOP_{trial}.avi")
    monkeypatch.setattr(utils, "findSinglePartial", lambda parts, path, suffix: "found_path.avi")

    result = utils.get_unambiguous_vidname_from_row(row, "experiment")
    assert result == "found_path.avi"


def test_time_helpers(tmp_path):
    csv_path = tmp_path / "timestamps.csv"
    csv_path.write_text("1\n2\n3\n")
    ts = utils.load_Bonsai_TS(str(csv_path))
    assert ts == [1, 2, 3]

    assert utils.hms_to_seconds("01:02:03.5") == pytest.approx(3723.5)


def test_calculate_firing_rates():
    spike_times = [0.1, 0.2, 0.3, 1.1, 1.2]
    event_times = [0.2, 1.2]
    centers, rates = utils.calculate_firing_rates(spike_times, event_times, window=(-0.2, 0.2), bin_size=0.1)

    assert centers.shape[0] == rates.shape[1]
    assert rates.shape[0] == 2


class DummyPdf:
    def __init__(self):
        self.calls = []

    def savefig(self, fig):
        self.calls.append(fig)


def test_plot_spike_and_rate(monkeypatch):
    pdf = DummyPdf()
    spike_times = [0.0, 0.05, 0.1, 1.0, 1.05, 1.1]
    event_times_1 = [0.0, 0.1]
    event_times_2 = [1.0]

    mean1, mean2 = utils.plot_spike_and_rate(
        spike_times,
        event_times_1,
        event_times_2,
        neuron_n="n1",
        window=(-0.2, 0.2),
        bin_size=0.05,
        pp=pdf,
    )

    assert mean1.shape == mean2.shape
    assert pdf.calls


def test_calculate_smoothed_firing_rates():
    spike_times = np.linspace(0, 1, 20)
    event_times = [0.2, 0.8]
    centers, rates = utils.calculate_smoothed_firing_rates(spike_times, event_times, window=(-0.5, 0.5), bin_size=0.1)

    assert rates.shape[0] == len(event_times)
    assert centers.shape[0] == rates.shape[1]


def test_calc_kde_psth_small_sample():
    spikeT = np.linspace(0, 0.01, 5)
    eventT = np.array([0.5])
    psth = utils.calc_kde_PSTH(spikeT, eventT, win=(-0.1, 0.1))
    assert np.allclose(psth, 0.0)


def test_calc_kde_psth_full_sample():
    spikeT = np.linspace(0, 1, 40)
    eventT = np.linspace(0.1, 0.9, 10)
    psth = utils.calc_kde_PSTH(spikeT, eventT, win=(-0.2, 0.2))
    assert psth.size > 0


def test_jump_peth(monkeypatch, tmp_path):
    call_counter = {"count": 0}

    def fake_plot_spike_and_rate(spike_times, success_times, abort_times, neuron_n, window, bin_size, pp):
        call_counter["count"] += 1
        return np.ones(5), np.zeros(5)

    def fake_find(pattern, path):
        if "ephys.bin" in pattern:
            return ["ephys.bin"]
        if "IMU.bin" in pattern:
            return ["imu.bin"]
        if "frame_nums.txt" in pattern:
            return ["frames.txt"]
        if "ephys_merge.json" in pattern:
            return ["merge.json"]
        return []

    def fake_json_load(_):
        return [
            {"event_type": "abort", "event_time_side": 0},
            {"event_type": "outcome", "event_time_side": 1},
            {"event_type": "abort", "event_time_side": 2},
            {"event_type": "outcome", "event_time_side": 3},
        ]

    phy_df = pd.DataFrame(
        {
            "group": ["good", "good"],
            "spikeT": [
                [0.1 * i for i in range(20)],
                [0.2 * i for i in range(20)],
            ],
        }
    )

    def fake_read_json(path):
        return phy_df.copy()

    saved = []

    def fake_to_hdf(self, path, key):
        saved.append((self.copy(), path, key))

    def fake_fromfile(file, dtype):
        n_channels = 8
        n_samples = 200
        data = np.zeros((n_channels, n_samples), dtype=np.int16)
        for idx in range(5, 125, 10):
            data[:, idx] = 6000
        return data.flatten(order="F")

    class FakeStat:
        def __init__(self, size):
            self.st_size = size

    class FakePath:
        def __init__(self, value):
            self.value = value

        def __truediv__(self, other):
            return FakePath(f"{self.value}/{other}")

        def stat(self):
            if "ephys.bin" in self.value:
                return FakeStat(128 * 20 * 2)
            if "imu.bin" in self.value:
                return FakeStat(8 * 200 * 2)
            return FakeStat(0)

        def __str__(self):
            return self.value

        def __fspath__(self):
            return self.value

    class DummyFile:
        def __init__(self, path):
            self.path = path

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, *_):
            return b""

    import builtins

    monkeypatch.setattr(utils, "plot_spike_and_rate", fake_plot_spike_and_rate)
    monkeypatch.setattr(utils, "find", fake_find)
    monkeypatch.setattr(utils.json, "load", fake_json_load)
    monkeypatch.setattr(utils.pd, "read_json", fake_read_json)
    monkeypatch.setattr(utils.pd.DataFrame, "to_hdf", fake_to_hdf, raising=False)
    monkeypatch.setattr(utils.np, "fromfile", fake_fromfile)
    monkeypatch.setattr(utils, "Path", FakePath)
    monkeypatch.setattr(builtins, "open", lambda *args, **kwargs: DummyFile(args[0]))

    utils.jump_peth(str(tmp_path), str(tmp_path))

    assert call_counter["count"] == 2
    assert saved and saved[0][1].endswith("jumping.h5")


def test_get_grating_preferences(monkeypatch, tmp_path):
    def fake_find(pattern, path):
        if "ephys_merge" in pattern:
            return ["merge.json"]
        if "frameTS" in pattern:
            return ["frameTS.csv"]
        if "stimRec" in pattern:
            return ["stimRec.csv"]
        if "Ephys_BonsaiBoardTS" in pattern:
            return ["bonsai.csv"]
        return []

    grat_phy = pd.DataFrame(
        {
            "group": ["good", "bad", "good"],
            "spikeT": [
                [0.1 * i for i in range(20)],
                [0.2 * i for i in range(20)],
                [0.15 * i for i in range(20)],
            ],
        }
    )

    csv_tables = {
        "frameTS.csv": pd.DataFrame({0: ["00:00:01.000", "00:00:02.000", "00:00:03.000", "00:00:04.000"]}),
        "stimRec.csv": pd.DataFrame(
            {
                "angle": [0, 0, 90, 90],
                "sf": [0.1, 0.2, 0.1, 0.2],
                "tf": [1, 2, 1, 2],
            }
        ),
        "bonsai.csv": pd.DataFrame({0: ["00:00:00.000"]}),
    }

    def fake_read_csv(path, **kwargs):
        from pathlib import Path as _Path

        name = _Path(str(path)).name
        return csv_tables[name].copy()

    def fake_read_json(path):
        return grat_phy.copy()

    def fake_smoothed(spike_times, event_times, window, bin_size, sigma=0.05):
        count = max(len(event_times), 1)
        centers = np.linspace(window[0], window[1], 40)
        if len(event_times) == 0:
            rates = np.zeros((0, centers.size))
        else:
            base = np.linspace(0, 4, centers.size)
            rates = np.vstack([base + idx for idx in range(count)])
        return centers[:-1], rates[:, :-1] if rates.size else rates

    saved = []

    def fake_to_hdf(self, path, key):
        saved.append((self.copy(), path, key))

    monkeypatch.setattr(utils, "find", fake_find)
    monkeypatch.setattr(utils.pd, "read_json", fake_read_json)
    monkeypatch.setattr(utils.pd, "read_csv", fake_read_csv)
    monkeypatch.setattr(utils, "calculate_smoothed_firing_rates", fake_smoothed)
    monkeypatch.setattr(utils.pd.DataFrame, "to_hdf", fake_to_hdf, raising=False)

    utils.get_grating_preferences(str(tmp_path), str(tmp_path))

    assert saved and saved[0][0].columns.isin(["pref_ori", "pref_sf", "pref_tf", "grat_peth", "grat_class"]).all()


def test_get_grat_pref(monkeypatch, tmp_path):
    def fake_find(pattern, path):
        if "ephys_merge" in pattern:
            return ["merge.json"]
        if "frameTS" in pattern:
            return ["frameTS.csv"]
        if "stimRec" in pattern:
            return ["stimRec.csv"]
        if "Ephys_BonsaiBoardTS" in pattern:
            return ["bonsai.csv"]
        return []

    grat_phy = pd.DataFrame(
        {
            "group": ["good", "good"],
            "spikeT": [
                [0.1 * i for i in range(30)],
                [0.2 * i for i in range(30)],
            ],
        }
    )

    csv_tables = {
        "frameTS.csv": pd.DataFrame({0: ["00:00:01.000", "00:00:02.000", "00:00:03.000", "00:00:04.000"]}),
        "stimRec.csv": pd.DataFrame(
            {
                "angle": [0, 0, 90, 90],
                "sf": [0.1, 0.2, 0.1, 0.2],
                "tf": [1, 2, 1, 2],
            }
        ),
        "bonsai.csv": pd.DataFrame({0: ["00:00:00.000"]}),
    }

    def fake_read_csv(path, **kwargs):
        from pathlib import Path as _Path

        name = _Path(str(path)).name
        return csv_tables[name].copy()

    def fake_read_json(path):
        return grat_phy.copy()

    def fake_calc_kde(spikeT, eventT, **kwargs):
        return np.linspace(0, 1, 1501)

    saved = []

    def fake_to_hdf(self, path, key):
        saved.append((self.copy(), path, key))

    monkeypatch.setattr(utils, "find", fake_find)
    monkeypatch.setattr(utils.pd, "read_json", fake_read_json)
    monkeypatch.setattr(utils.pd, "read_csv", fake_read_csv)
    monkeypatch.setattr(utils, "calc_kde_PSTH", fake_calc_kde)
    monkeypatch.setattr(utils.pd.DataFrame, "to_hdf", fake_to_hdf, raising=False)

    utils.get_grat_pref(str(tmp_path), str(tmp_path))

    assert saved and saved[0][0].columns.isin(["pref_tf", "pref_sf", "pref_ori", "vis_resp"]).all()


def test_plotting_helpers():
    rows = []
    subjects = ["s1", "s2"]
    distances = [10, 15, 20, 25]
    for condition in [0, 1]:
        for distance in distances:
            for subject in subjects:
                for platform in [1, 2, 3]:
                    for manip in [0, 1]:
                        rows.append(
                            {
                                "subject": subject,
                                "distance": distance,
                                "condition": condition,
                                "outcome": (distance + platform + manip + condition) % 3,
                                "platform_DLC": platform,
                                "Distance_Jumped": distance - 0.5 + 0.1 * platform + 0.2 * manip + condition,
                                "manip": manip,
                                "variable": distance / 10.0 + 0.05 * platform + 0.1 * manip + 0.1 * condition,
                            }
                        )

    df = pd.DataFrame(rows)

    fig_pf, axs_pf = utils.plt.subplots(1, 2)
    ax_result = utils.plot_performance_platforms(
        axs_pf,
        df,
        condition="condition",
        aborts=True,
        plt_min=10,
        plt_max=25,
        color_scheme=["red", "blue"],
        ls_list=["-", "--", ":"],
    )
    assert ax_result is not None

    fig_jp, axs_jp = utils.plt.subplots(1, 2)
    axs_return = utils.plot_jumpdist_platforms(
        axs_jp,
        df,
        condition="condition",
        plt_min=10,
        plt_max=25,
        color_scheme=["red", "blue"],
        ls_list=["-", "--", ":"],
    )
    assert axs_return is not None

    fig_var, ax_var = utils.plt.subplots(1, 1)
    ax_out = utils.plot_variable_vs_distance(
        ax_var,
        df,
        variable="variable",
        condition="condition",
        x_min=10,
        x_max=25,
        y_min=0,
        y_max=1.5,
        color_scheme=["red", "blue"],
        save_pdf=False,
        pp=None,
        suptitle="",
    )
    assert ax_out is not None

    fig_var_manip, axs_var_manip = utils.plt.subplots(1, 2)
    axs_vm = utils.plot_variable_vs_distance_manipulation(
        axs_var_manip,
        df,
        variable="variable",
        condition="condition",
        manipulation="manip",
        x_min=10,
        x_max=25,
        y_min=0,
        y_max=1.5,
        color_scheme=["red", "blue"],
        save_pdf=False,
        pp=None,
        suptitle="",
    )
    assert axs_vm is not None

    fig_var_manip2, axs_var_manip2 = utils.plt.subplots(1, 2)
    axs_vm2 = utils.plot_variable_vs_distance_manipulation(
        axs_var_manip2,
        df,
        variable="variable",
        condition="condition",
        manipulation="manip",
        aborts=True,
        plt_min=10,
        plt_max=25,
        color_scheme=["red", "blue"],
        ylabel="var",
    )
    assert axs_vm2 is not None

    fig_jm, axs_jm = utils.plt.subplots(1, 2)
    axs_jm_out = utils.plot_jumpdist_manipulation(
        axs_jm,
        df,
        condition="condition",
        manipulation="manip",
        plt_min=10,
        plt_max=25,
        color_scheme=["red", "blue"],
    )
    assert axs_jm_out is not None


def test_legacy_plot_variable_vs_distance_manipulation():
    from pathlib import Path

    legacy_rows = []
    for condition in [0, 1]:
        for distance in [10, 15, 20, 25]:
            for subject in ["s1", "s2"]:
                for manip in [0, 1]:
                    legacy_rows.append(
                        {
                            "subject": subject,
                            "distance": distance,
                            "condition": condition,
                            "manip": manip,
                            "variable": distance / 10.0 + 0.05 * manip + 0.1 * condition,
                        }
                    )

    df = pd.DataFrame(legacy_rows)

    source_lines = Path("jumpyng/utils.py").read_text().splitlines()
    start_idx = next(
        i
        for i, line in enumerate(source_lines)
        if line.strip().startswith("def plot_variable_vs_distance_manipulation(") and "x_min" in line
    )
    end_idx = next(
        i
        for i, line in enumerate(source_lines[start_idx + 1 :], start_idx + 1)
        if line.strip().startswith("def plot_variable_vs_distance_manipulation(")
    )
    func_source = "\n".join(source_lines[start_idx:end_idx])
    padded_source = "\n" * start_idx + func_source
    globals_dict = dict(utils.__dict__)
    exec(compile(padded_source, "jumpyng/utils.py", "exec"), globals_dict)
    legacy_func = globals_dict["plot_variable_vs_distance_manipulation"]

    fig, axs = utils.plt.subplots(1, 2)
    returned = legacy_func(
        axs,
        df,
        variable="variable",
        condition="condition",
        manipulation="manip",
        x_min=10,
        x_max=15,
        y_min=0.0,
        y_max=1.0,
        color_scheme=["red", "blue"],
        save_pdf=False,
        pp=None,
        suptitle="legacy",
    )
    assert returned is not None
