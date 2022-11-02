import re
from collections import Counter
from typing import Optional
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import webtext

# nltk.download("webtext")
# nltk.download("punkt)
# nltk.download('stopwords')


stopwords = set(nltk.corpus.stopwords.words("english"))
additional_stopwords = {"a", "i", "yet", "if", "bit"}
stopwords.update(additional_stopwords)


def get_data() -> pd.DataFrame:

    # Make sure to run nltk.download if you have not done so already
    raw_sentences = re.split("\n", webtext.raw("wine.txt"))

    df = pd.DataFrame(data=raw_sentences, columns=["reviews"])
    df["stars"] = df["reviews"].apply(lambda x: x.rsplit(" ")[-1])

    return df


def clean_data(df: pd.DataFrame = None) -> pd.DataFrame:

    if df is None:
        df = get_data()

    # After inspecting data in Excel we decide to clean it as following:

    # Make reviews lowercase
    df["reviews"] = df["reviews"].apply(lambda x: x.lower())

    # Remove the part of review extracted as stars from the reviews text
    df["reviews"] = df["reviews"].apply(lambda x: x.replace(x.rsplit(" ")[-1], ""))

    # Clean up stars column of any captured words
    df["stars"] = df["stars"].apply(
        lambda x: "".join([c for c in x if c in ["*", "(", ")"]])
    )

    # Remove records with no stars
    df["valid"] = df["stars"].apply(lambda x: True if x.find("*") > -1 else False)

    df = df.loc[df["valid"]]

    # Remove records where review is less than 10 chars long
    df = df.loc[df["reviews"].str.len() > 10]

    # Map stars to the number
    df["stars_num"] = df["stars"].apply(
        lambda x: len(x) - 3 + 0.5 if x.find("(") > -1 else len(x)
    )

    return df[["reviews", "stars", "stars_num"]]


def tokenize(df: pd.DataFrame = None) -> pd.DataFrame:

    if df is None:
        df = clean_data(get_data())

    # Add a column with tokenized reviews where we remove punctuations
    # Also remove stop words that are defined globally
    # Because we cannot display a list in a dataframe we return tokens as string
    df["tokens"] = df["reviews"].apply(
        lambda x: ", ".join(
            [w for w in word_tokenize(x) if w.isalpha() and w not in stopwords]
        )
    )

    return df


def get_word_freq(df: pd.DataFrame, stars_filter: Optional[int] = 5) -> dict:

    # Filter the dataframe on the stars ensuring we have passed a good value
    if stars_filter in Counter(df["stars_num"]).keys():
        df_filtered = df.loc[df["stars_num"] == stars_filter]

        cnt = Counter()
        df_filtered["tokens"].apply(lambda x: cnt.update(x.split(", ")))

        return dict(cnt.most_common())
    else:
        return dict()
