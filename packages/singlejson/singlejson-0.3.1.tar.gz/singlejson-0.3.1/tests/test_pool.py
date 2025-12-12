from singlejson.pool import load, sync
from singlejson.fileutils import JSONFile


def test_pool(tmp_path):
    path = tmp_path.joinpath("test.json").__str__()
    jsonfile = load(path, default={"test": "successful", "other_types": [True, 1, {}]})
    assert jsonfile.json["test"] == "successful", "should be successful"
    jsonfile.json["test"] = "unsuccessful"
    assert load(path).json["test"] == "unsuccessful", \
        "should be unsuccessful since it should access the local copy."
    assert JSONFile(path, default={"test": "unsuccessful"}).json["test"] == "successful", \
        "should be successful since changes to pool should not have been saved."
    sync()
    assert JSONFile(path, default={"test": "successful"}).json["test"] == "unsuccessful", \
        "should be unsuccessful since changes to pool should have been saved."
