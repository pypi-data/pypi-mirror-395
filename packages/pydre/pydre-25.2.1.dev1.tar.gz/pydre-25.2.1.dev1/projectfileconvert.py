from loguru import logger
import json
import pathlib
import tomlkit


def convertProjToToml(proj: dict) -> tomlkit.TOMLDocument:
    new_proj = tomlkit.TOMLDocument()
    filters = proj.get("filters", [])
    rois = proj.get("rois", [])
    metrics = proj.get("metrics", [])

    if len(filters) > 0:
        filters_table = tomlkit.table(True)
        for filter in filters:
            name = filter.pop("name", None)
            f_tab = tomlkit.table()
            f_tab.update(filter)
            filters_table.add(name, f_tab)
        new_proj.add("filters", filters_table)

    if len(rois) > 0:
        rois_table = tomlkit.table(True)
        i = 1
        for roi in rois:
            name = f"roi{i}"
            i += 1
            r_tab = tomlkit.table()
            r_tab.update(roi)
            rois_table.add(name, r_tab)
        new_proj.add("rois", rois_table)

    if len(metrics) > 0:
        metrics_table = tomlkit.table(True)
        for metric in metrics:
            name = metric.pop("name", None)
            m_tab = tomlkit.table()
            m_tab.update(metric)
            metrics_table.add(name, m_tab)
        new_proj.add("metrics", metrics_table)
    return new_proj


def main():
    proj_dir = pathlib.Path("./project_files")
    old_proj_files = proj_dir.resolve().glob("*.json")
    for fn in old_proj_files:
        logger.info(f"Converting {fn}")
        with open(fn, "r") as fs:
            try:
                json_data = json.load(fs)
            except json.decoder.JSONDecodeError:
                logger.warning(f"Error decoding {fn}")
                continue
        new_proj = convertProjToToml(json_data)
        with open(fn.with_suffix(".toml"), "w") as fs:
            tomlkit.dump(new_proj, fs)


if __name__ == "__main__":
    main()
