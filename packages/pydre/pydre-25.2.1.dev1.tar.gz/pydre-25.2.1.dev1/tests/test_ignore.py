from pathlib import Path
import pytest
import pydre.project


FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data"


@pytest.mark.datafiles(
    FIXTURE_DIR / "good_projectfiles",
    FIXTURE_DIR / "test_datfiles",
    keep_top_dir=True,
)
def test_ignore_1(datafiles):
    proj = pydre.project.Project(datafiles / "good_projectfiles" / "test_ignore_1.toml")
    assert isinstance(proj, pydre.project.Project)
    assert len(proj.filelist) == 8


@pytest.mark.datafiles(
    FIXTURE_DIR / "good_projectfiles", FIXTURE_DIR / "test_datfiles", keep_top_dir=True
)
def test_ignore_2(datafiles):
    proj = pydre.project.Project(datafiles / "good_projectfiles" / "test_ignore_2.toml")
    assert isinstance(proj, pydre.project.Project)
    assert len(proj.filelist) == 6
