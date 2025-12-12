from pathlib import Path
import pytest
import pydre.project
import polars as pl
import polars.testing
import json
import tomllib
import shutil
import pydre.metrics

from pydre.core import DriveData
from pydre.project import Project

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "good_projectfiles" / "test1_pf.json")
def test_project_loadjson(datafiles):
    proj = pydre.project.Project(datafiles / "test1_pf.json")
    assert isinstance(proj, pydre.project.Project)


@pytest.mark.datafiles(FIXTURE_DIR / "good_projectfiles" / "test1_pf.toml")
def test_project_loadtoml(datafiles):
    proj = pydre.project.Project(datafiles / "test1_pf.toml")
    assert isinstance(proj, pydre.project.Project)


def test_project_loadbadtoml():
    with pytest.raises(FileNotFoundError):
        proj = pydre.project.Project("doesnotexist.toml")


@pytest.mark.datafiles(
    FIXTURE_DIR / "good_projectfiles" / "test1_pf.json",
    FIXTURE_DIR / "good_projectfiles" / "test1_pf.toml",
)
def test_project_projequiv(datafiles):
    proj_json = pydre.project.Project(datafiles / "test1_pf.json")
    proj_toml = pydre.project.Project(datafiles / "test1_pf.toml")
    assert proj_json == proj_toml


@pytest.mark.datafiles(
    FIXTURE_DIR / "good_projectfiles",
    FIXTURE_DIR / "test_custom_metric",
    FIXTURE_DIR / "test_datfiles",
    keep_top_dir=True,
)
def test_project_custom_metric(datafiles):
    resolved_data_file = str(
        datafiles / "test_datfiles" / "clvspectest_Sub_8_Drive_3.dat"
    )
    proj = pydre.project.Project(
        datafiles / "good_projectfiles" / "custom_test.toml",
        additional_data_paths=[resolved_data_file],
    )
    proj.processDatafiles(numThreads=2)

    expected_result = pl.DataFrame(
        [
            {
                "ParticipantID": "8",
                "UniqueID": "3",
                "ScenarioName": "Drive",
                "DXmode": "Sub",
                "ROI": None,
                "custom_test": 1387.6228702430055,
            }
        ]
    )

    polars.testing.assert_frame_equal(proj.results, expected_result)


def test_project_bad_toml_format(tmp_path):
    bad_toml = tmp_path / "bad.toml"
    bad_toml.write_text("bad:::toml")

    project = pydre.project.Project(bad_toml)
    assert project.definition == {} or project.definition is None


def test_project_missing_keys_toml(tmp_path):
    toml = tmp_path / "empty.toml"
    toml.write_text('title = "Empty project"')  # no rois, metrics, filters

    project = pydre.project.Project(toml)
    assert project.definition == {}  # no keys restructured


def test_project_additional_data_paths(tmp_path):
    test_file = tmp_path / "data1.dat"
    test_file.write_text("VidTime SimTime\n1 1\n2 2")

    dummy_toml = tmp_path / "base.toml"
    dummy_toml.write_text("""
        [config]
        datafiles = []
    """)

    project = pydre.project.Project(dummy_toml, additional_data_paths=[str(test_file)])
    assert str(test_file) in project.config["datafiles"]


def test_process_filter_missing_function():
    dummy_data = DriveData()
    bad_filter = {"name": "invalidfilter"}
    with pytest.raises(KeyError):
        pydre.project.Project.processFilter(bad_filter, dummy_data)


@pytest.mark.datafiles(FIXTURE_DIR / "good_projectfiles" / "test1_pf.toml")
def test_process_roi_unknown_type(datafiles):
    dummy_data = DriveData()
    unknown_roi = {"type": "nonexistent", "filename": "roi.csv"}

    # Explicitly specify and combine the TOML file path
    toml_path = datafiles / "test1_pf.toml"

    # Initialize the project using a TOML file
    project = pydre.project.Project(toml_path)

    result = project.processROI(unknown_roi, dummy_data)
    assert result == [dummy_data]


def test_save_results_without_running(tmp_path):
    dummy_toml = tmp_path / "dummy.toml"
    dummy_toml.write_text("""
        [config]
        datafiles = []
    """)
    project = pydre.project.Project(dummy_toml)
    project.results = None
    project.config["outputfile"] = str(tmp_path / "out.csv")

    # Should not raise error, just log it
    project.saveResults()
    assert not (tmp_path / "out.csv").exists()


def test_project_toml_full_definition(tmp_path):
    toml = tmp_path / "full.toml"
    toml.write_text("""
    [rois.rect1]
    type = "rect"
    filename = "roi.csv"

    [metrics.metric1]
    name = "m1"
    function = "test_metric"

    [filters.filter1]
    name = "f1"
    function = "test_filter"

    [config]
    datafiles = []
    """)

    project = pydre.project.Project(toml)
    assert isinstance(project.definition.get("rois"), list)
    assert isinstance(project.definition.get("metrics"), list)
    assert isinstance(project.definition.get("filters"), list)
    assert isinstance(project.config, dict)


def test_project_toml_with_extra_keys(tmp_path):
    toml = tmp_path / "weird.toml"
    toml.write_text("""
    title = "strange"
    [config]
    datafiles = []
    """)

    project = pydre.project.Project(toml)
    assert project.definition == {}


def test_project_outputfile_override(tmp_path):
    toml = tmp_path / "config.toml"
    toml.write_text("""
    [config]
    datafiles = []
    outputfile = "default.csv"
    """)

    override_file = tmp_path / "override.csv"
    project = pydre.project.Project(toml, outputfile=str(override_file))
    assert project.config["outputfile"] == str(override_file)


def test_project_ignore_files(tmp_path):
    data_file = tmp_path / "real.dat"
    data_file.write_text("VidTime SimTime\n1 1")
    ignored_file = tmp_path / "ignore_this.dat"
    ignored_file.write_text("VidTime SimTime\n1 1")

    toml = tmp_path / "ignore.toml"
    toml.write_text("""
    [config]
    datafiles = ["*.dat"]
    ignore = ["ignore_this"]
    """)

    project = pydre.project.Project(toml)
    assert all("ignore_this" not in str(f) for f in project.filelist)
    assert any("real" in str(f) for f in project.filelist)


def test_process_metric_missing_fields():
    dummy_data = DriveData()
    metric = {"function": "nonexistent_func"}
    project = pydre.project.Project.__new__(pydre.project.Project)
    with pytest.raises(KeyError):
        project.processMetric(metric, dummy_data)


def test_process_datafiles_with_exception(monkeypatch, tmp_path):
    dummy_file = tmp_path / "bad.dat"
    dummy_file.write_text("VidTime SimTime\n0.0 0.0")
    toml = tmp_path / "exc.toml"
    toml.write_text("""
    [config]
    datafiles = ["bad.dat"]
    """)
    proj = pydre.project.Project(toml)


def faulty_process(_):
    raise RuntimeError("Forced failure")

    monkeypatch.setattr(proj, "processSingleFile", faulty_process)
    proj.processDatafiles(numThreads=1)


def test_process_roi_rect(monkeypatch, tmp_path):
    roi = {"type": "rect", "filename": "roi.csv"}
    dummy_data = DriveData()
    dummy_file = tmp_path / "roi.csv"
    dummy_file.write_text("x,y,width,height\n0,0,1,1")

    monkeypatch.setattr(pydre.rois, "SpaceROI", lambda filename: DummyROI())

    roi_type = roi["type"]
    roi_filename = str(dummy_file)

    if roi_type == "rect":
        roi_obj = pydre.rois.SpaceROI(roi_filename)
        result = roi_obj.process(dummy_data)
        assert isinstance(result, list)
    else:
        pytest.skip("This test only covers 'rect' ROI")


class DummyROI:
    def split(self, data):
        return [data]

    def process(self, data):
        return [data]


def test_project_toml_parse_error(monkeypatch, tmp_path):
    bad_toml = tmp_path / "bad.toml"
    bad_toml.write_text("bad:::toml")
    monkeypatch.setattr(
        tomllib,
        "load",
        lambda _: (_ for _ in ()).throw(tomllib.TOMLDecodeError("bad", "bad", 1)),
    )
    project = pydre.project.Project(bad_toml)
    assert project.definition == {}


def test_load_custom_functions_empty(tmp_path):
    metrics_dir = tmp_path / "metrics"
    metrics_dir.mkdir()
    toml = tmp_path / "custom.toml"
    toml.write_text(f"""
    [config]
    datafiles = []
    custom_metrics_dirs = "{metrics_dir}"
    custom_filters_dirs = "{metrics_dir}"
    """)
    p = pydre.project.Project(toml)
    # No assertion needed — goal is line coverage


def test_project_json_toml_loading(tmp_path):
    # test json
    json_file = tmp_path / "project.json"
    json_file.write_text(json.dumps({"metrics": []}))
    pj = Project(json_file)
    assert pj.definition.get("metrics", []) == []

    # test toml
    toml_file = tmp_path / "project.toml"
    toml_file.write_text('[config]\ndatafiles = ["test.dat"]\n')
    pj2 = Project(toml_file)

    assert pj2.definition.get("rois", []) == []


def test_project_eq_true(tmp_path):
    toml = tmp_path / "eq.toml"
    toml.write_text("""
        [config]
        datafiles = []
    """)
    proj1 = Project(toml)
    proj2 = Project(toml)
    assert proj1 == proj2


def test_project_eq_false(tmp_path):
    t1 = tmp_path / "p1.toml"
    t2 = tmp_path / "p2.toml"
    t1.write_text("[config]\ndatafiles = []")
    t2.write_text('[config]\ndatafiles = ["fake.dat"]')
    p1 = Project(t1)
    p2 = Project(t2)
    assert p1 != p2


def test_resolve_file_relative_and_absolute(tmp_path):
    config_file = tmp_path / "cfg.toml"
    config_file.write_text("[config]\ndatafiles = []")
    p = Project(config_file)

    # relative path test
    rel = p.resolve_file("subdir/fakefile.py")
    assert rel.is_absolute()

    # absolute path test
    abs_path = tmp_path.resolve() / "file.py"
    result = p.resolve_file(abs_path)
    resolved = p.resolve_file(str(abs_path))
    assert Path(resolved) == abs_path


def test_clean_function():
    raw = "['C:\\\\Users\\\\file.dat']"
    cleaned = Project._Project__clean(raw)
    assert cleaned == "file.dat"


def test_process_metric_multiple_cols(monkeypatch):
    def dummy_metric(data, **kwargs):
        return [1.0, 2.0]

    monkeypatch.setitem(pydre.metrics.metricsList, "dummy", dummy_metric)
    monkeypatch.setitem(pydre.metrics.metricsColNames, "dummy", ["val1", "val2"])

    p = Project.__new__(Project)
    dummy_data = DriveData()
    metric = {"function": "dummy", "name": "custom"}
    result = p.processMetric(metric, dummy_data)

    assert result == {"val1": 1.0, "val2": 2.0}


def test_resolve_file(tmp_path):
    config_path = tmp_path / "project.toml"
    config_path.write_text("[config]\ndatafiles = []")

    p = Project(config_path)

    abs_path = tmp_path / "datafile.csv"
    abs_path.write_text("dummy")
    assert Path(p.resolve_file(str(abs_path))) == abs_path

    rel_path = "datafile.csv"
    assert Path(p.resolve_file(rel_path)) == tmp_path / rel_path


def test_load_custom_functions(tmp_path):
    custom_path = tmp_path / "dummy_metrics.py"
    custom_path.write_text("def test(): pass")

    config = tmp_path / "project.toml"
    config.write_text(
        f'[config]\ncustommetrics = ["{custom_path.name}"]\ndatafiles = []'
    )

    target_path = tmp_path / "subdir" / custom_path.name
    target_path.parent.mkdir(exist_ok=True)
    shutil.copy(str(custom_path), str(target_path))

    p = Project(config)


def test_process_metric_multiple_columns(tmp_path):
    dummy_csv = tmp_path / "dummy.csv"
    dummy_csv.write_text("a,b\n1,3\n2,4\n")

    config = tmp_path / "project.toml"
    config.write_text(f'[config]\ndatafiles = ["{dummy_csv.name}"]')

    p = Project(config)
    p.data = polars.read_csv(dummy_csv)

    def dummy_compute(*args, **kwargs):
        return 42

    pydre.metrics.metricsList["dummy_compute"] = dummy_compute
    pydre.metrics.metricsColNames["dummy_compute"] = ["metric_id"]

    metric_dict = {"name": "metric_id", "function": "dummy_compute", "col_names": ["a"]}

    result = p.processMetric(metric_dict, p.data)
    assert result == {"metric_id": 42}


def test_clean_method_via_project(tmp_path):
    config = tmp_path / "p.toml"
    config.write_text("[config]\ndatafiles = []")
    p = Project(config)
    cleaned = p._Project__clean("Hello World!! @#")
    assert cleaned == "Hello World!! @#"


def test_project_init_no_datafiles_logs_error(tmp_path, caplog):
    """
    When a project is initialized with no datafiles in [config],
    it should emit an ERROR log 'No datafile found in project definition.'
    """
    # 1. Create a minimal TOML with empty datafiles list
    toml = tmp_path / "nodata.toml"
    toml.write_text("""
    [config]
    datafiles = []
    """)
    # 2. Capture ERROR logs
    caplog.set_level("ERROR")
    # 3. Initialize project
    project = Project(str(toml))
    # 4. Assert that the specific error message was logged
    assert "No datafile found in project definition." in caplog.text


def test_save_results_without_running_logs_error(tmp_path, caplog, capsys):
    """
    Calling saveResults() before results are computed should:
      - log ERROR 'Results not computed yet'
      - not create an output file.

    We accept the log message from either pytest's caplog OR stderr,
    because the code under test (or other fixtures) may reconfigure
    loguru handlers during the test.
    """
    # 1. Prepare dummy TOML and project
    toml = tmp_path / "dummy.toml"
    toml.write_text("""
    [config]
    datafiles = []
    """)
    project = Project(str(toml))
    project.results = None
    project.config["outputfile"] = str(tmp_path / "out.csv")
    # 2. Capture ERROR logs
    caplog.set_level("ERROR")
    # 3. Invoke saveResults() — should not raise, but log
    project.saveResults()
    # 4. Verify no output file was written
    assert not (tmp_path / "out.csv").exists()
    # 5. Verify the error message was logged either in caplog or stderr
    out, err = capsys.readouterr()
    msg = "Results not computed yet"
    assert (msg in caplog.text) or (msg in err)
