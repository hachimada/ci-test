# tests/test_version.py
from pathlib import Path
import re
import toml
import pytest

# ----------------------------------------------------------------------
# 正規表現をコンパイル（X.Y.Z か X.Y.ZrcW にマッチ）
SEMVER_OR_RC_RE: re.Pattern[str] = re.compile(
    r"^(0|[1-9]\d*)"          # X
    r"\.(0|[1-9]\d*)"         # .Y
    r"\.(0|[1-9]\d*)"         # .Z
    r"(?:rc(0|[1-9]\d*))?$"   # optional rcW
)


@pytest.fixture(scope="session")
def project_version() -> str:
    """
    Return version defined in *pyproject.toml*.

    Returns
    -------
    str
        Version string under ``tool.poetry.version``.
    """
    project_root: Path = Path(__file__).resolve().parents[1]
    pyproject: dict = toml.load(project_root / "pyproject.toml")
    return pyproject["tool"]["poetry"]["version"]


def test_version_format(project_version: str) -> None:
    """
    Validate that the project version matches ``X.Y.Z`` or ``X.Y.ZrcW``.

    Parameters
    ----------
    project_version : str
        Version string provided by fixture.
    """
    # プロジェクトのバージョンが意図した形式かどうか確認
    assert SEMVER_OR_RC_RE.fullmatch(project_version), (
        f"Invalid version '{project_version}'. "
        "Use 'X.Y.Z' or 'X.Y.ZrcW' without a leading 'v'."
    )


# ----------------------------------------------------------------------
# 正規表現自体のユニットテスト（パラメタライズ）

@pytest.mark.parametrize(
    "version",
    [
        "0.0.0",
        "1.2.3",
        "10.20.30",
        "1.2.3rc1",
        "0.0.1rc10",
    ],
)
def test_regex_accepts_valid(version: str) -> None:
    """
    Ensure the regex accepts valid versions.

    Parameters
    ----------
    version : str
        Candidate version string expected to match.
    """
    # 正しい形式はマッチするはず
    assert SEMVER_OR_RC_RE.fullmatch(version) is not None, version


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3",      # 先頭に v
        "1.2",         # パッチ番号無し
        "1.2.3rc",     # rc だが数字が無い
        "1.2.3rc01",   # 先頭ゼロ
        "01.2.3",      # 先頭ゼロ
        "1.2.3dev1",   # dev 表記
        "1.2.3.post1", # post 表記
        "1.2.3b1",     # beta 表記
        "1.2.3rc-1",   # 不正文字
    ],
)
def test_regex_rejects_invalid(version: str) -> None:
    """
    Ensure the regex rejects invalid versions.

    Parameters
    ----------
    version : str
        Candidate version string expected *not* to match.
    """
    # 不正な形式はマッチしないはず
    assert SEMVER_OR_RC_RE.fullmatch(version) is None, version