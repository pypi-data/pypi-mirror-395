from singlejson.fileutils import prepare, JSONFile


def test_prepare_file(tmp_path):
    path = tmp_path.joinpath("testdir/test.json").__str__()
    prepare(path, default="test")
    with open(path, "r") as readable:
        assert readable.read().strip() == "test", "should be test"
    prepare(path, default="no_overwrite")
    with open(path, "r") as readable:
        assert readable.read().strip() == "test", "should still be test"


def test_json_file(tmp_path):
    file = JSONFile(tmp_path.joinpath("test.json").__str__(), {"test": "successful", "other_types": [True, 1, {}]})
    file.json["test"] = "unsuccessful"
    local_file = JSONFile(tmp_path.joinpath("test.json").__str__())
    assert local_file.json["test"] == "successful", "should be successful, change should not have been saved"
    file.save()
    assert local_file.json["test"] == "successful", "should be successful, change should not have been loaded"
    local_file.reload()
    assert local_file.json["test"] == "unsuccessful", "should be unsuccessful, change should have been loaded"
    assert local_file.json["other_types"] == [True, 1, {}], "other types should be saved properly"
