from hecto.main import get_src


def test_get_src(mocker):
    mock_clone = mocker.patch("hecto.main.vcs.clone")
    src = get_src("https://github.com/jpsca/hecto.git#blueprint/new")
    mock_clone.assert_called_once_with("https://github.com/jpsca/hecto.git")
    assert str(src).endswith("/blueprint/new")
