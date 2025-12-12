from pydre.project import Project

if __name__ == "__main__":
    proj = Project(r"tests/test_data/good_projectfiles/test_infer_schema.toml")
    result = proj.processDatafiles()
    print(result)
