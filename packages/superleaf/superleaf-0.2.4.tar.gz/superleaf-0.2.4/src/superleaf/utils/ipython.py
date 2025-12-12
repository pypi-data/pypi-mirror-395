from IPython.extensions.autoreload import AutoreloadMagics
import pandas as pd


def autoreload():
    AutoreloadMagics().autoreload("3")


def show_all_columns():
    pd.set_option('display.max_columns', None)
