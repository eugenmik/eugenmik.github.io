def _log(result):
    return result.stdout + result.stderr


def test_prod_build_clean(prod):
    dest, result = prod
    assert result.returncode == 0, _log(result)
    assert "WARN" not in _log(result), _log(result)
    assert "ERROR" not in _log(result), _log(result)
    assert (dest / "index.html").exists()


def test_drafts_build_clean(drafts):
    dest, result = drafts
    assert result.returncode == 0, _log(result)
    assert "WARN" not in _log(result), _log(result)
