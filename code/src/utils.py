import json
from pathlib import Path

import pandas as pd
import requests
<<<<<<< HEAD
=======
from bs4 import BeautifulSoup
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

from . import __file__ as pkg_init_name

HOME = Path(pkg_init_name).parent.parent.parent
DATA = HOME / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"
DATA_INTERIM = DATA / "interim"
MODELS = HOME / "models"
RESULTS = HOME / "results"
REG_DATA = MODELS / "reg_data"
CODE = HOME / "code"

ISOS = ["USA", "ITA", "FRA", "CHN", "KOR", "IRN"]
<<<<<<< HEAD
adm3_dir_fmt = "gadm36_{iso3}_{datestamp}.zip"
=======
adm3_dir_fmt = "gadm36_{iso3}.zip"
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

CUM_CASE_MIN_FILTER = 10
PROCESSED_DATA_ERROR_HANDLING = "raise"
PROCESSED_DATA_DATE_CUTOFF = False

COLORS = {"effect": "#27408B", "no_policy_growth_rate": "#8B0000"}

<<<<<<< HEAD
with open(CODE / "api_keys.json", "r") as f:
    API_KEYS = json.load(f)

=======
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

def zipify_path(path):
    return "zip://" + str(path)


<<<<<<< HEAD
def download_zip(url, out_path, overwrite=False):
=======
def download_file(url, out_path, overwrite=False):
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if (not out_path.exists()) or overwrite:
        r = requests.get(url, allow_redirects=True)
<<<<<<< HEAD
        with open(out_path, "wb") as f:
            f.write(r.content)
=======
        if Path(out_path).suffix in [".csv", ".txt"]:
            with open(out_path, "w") as f:
                f.write(r.text)
        else:
            with open(out_path, "wb") as f:
                f.write(r.content)
    return None


def get_scraped_text(url, out_path, overwrite=False):
    if (not out_path.exists()) or overwrite:
        with open(out_path, "w") as f:
            f.write(requests.get(url).text)
    with open(out_path, "r") as f:
        text = BeautifulSoup(f.read(), "lxml")
    return text
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51


def iso_to_dirname(iso3):
    mapping = {
        "FRA": "france",
        "ITA": "italy",
        "USA": "usa",
        "CHN": "china",
        "IRN": "iran",
        "KOR": "korea",
    }
    return mapping[iso3]


<<<<<<< HEAD
def get_adm_zip_path(iso3, datestamp):
    dirname = iso_to_dirname(iso3)
    assert (DATA_RAW / dirname).is_dir(), DATA_RAW / dirname
    return DATA_RAW / dirname / adm3_dir_fmt.format(iso3=iso3, datestamp=datestamp)
=======
def get_adm_zip_path(iso3):
    dirname = iso_to_dirname(iso3)
    assert (DATA_RAW / dirname).is_dir(), DATA_RAW / dirname
    return DATA_RAW / dirname / adm3_dir_fmt.format(iso3=iso3)
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51


def downcast_floats(ser):
    try:
        new_ser = ser.astype("int")
        if (new_ser == ser).all():
            return new_ser
        else:
            return ser
    except ValueError:
        return ser


def get_processed_fpath(iso3, adm_lvl):
    return DATA_PROCESSED / f"adm{adm_lvl}" / f"{iso3}_processed.csv"


def load_processed_data(iso3, adm_lvl):
    index_cols = [f"adm{i}_name" for i in range(adm_lvl + 1)] + ["date"]
    return pd.read_csv(
        get_processed_fpath(iso3, adm_lvl), index_col=index_cols, parse_dates=True
    ).sort_index()


def read_cases(fn, cases_drop=False):
    df_all = pd.read_csv(fn)
    if cases_drop:
        df_all = df_all.drop(columns="cases")
        df_all = df_all.rename(columns={"cases_drop": "cases"})
    df_cases = df_all.loc[:, ["date", "cases"]]
    df_cases.loc[:, "date_str"] = df_cases.loc[:, "date"]
    df_cases.loc[:, "date"] = pd.to_datetime(df_cases.loc[:, "date"])

    return df_cases


def load_all_cases_deaths(cases_drop=False):
    cases_dict = {}
    for i in ISOS:
        cases_data_fn = DATA_PROCESSED / "adm0" / f"{i}_cases_deaths.csv"
        cases = read_cases(cases_data_fn, cases_drop=cases_drop)
        cases_dict[iso_to_dirname(i)] = cases
    return cases_dict
