import pandas


def __keep_text_from(
    data: pandas.DataFrame, lowest_conf: float = 20.0
) -> pandas.DataFrame:
    """
    Remove tokens lower than the lowest_conf from the dataframe returned from Tesseract.

    Returns filtered dataframe.
    """
    data = data.drop(data[data.conf <= lowest_conf].index)
    return data


def correct_text(dataframe):
    # NOT FINISHED, i just filter out all low-confident predictions
    dataframe = __keep_text_from(dataframe)
    return dataframe


def get_text(dataframe):
    """Concatenate all text in the dataframe"""
    return " ".join(dataframe["text"])
