import pandas as pd
from services.utils.file_utils import detect_language, translate_header
import os
from core.config import TIMELINE_OPTION


def merge_rows(df: pd.DataFrame) -> pd.DataFrame:
    for i in range(len(df) - 1):
        if df.at[i, "Heading"] == "Y":
            for column in df.columns:
                if column not in [
                    "Heading",
                    "Ref#",
                    "Smart Area",
                    "Initiative Group",
                    "Initiative",
                ]:
                    if pd.isna(df.at[i, column]) or df.at[i, column] == "":
                        df.at[i, column] = df.at[i + 1, column]
                    else:
                        df.at[i, column] = (
                            f"**{df.at[i, column]}**\n{df.at[i + 1, column]}"
                        )
            df.at[i + 1, "Heading"] = "MERGED"
    df = df[df["Heading"] != "MERGED"].reset_index(drop=True)
    df["TempRef#"] = df["Ref#"].ffill().bfill()  # Ensure initial TempRef# assignment

    return df


def clean_group(group: any):
    for column in group.columns:
        if column not in ["Progress Update", "Status", "Title", "TempRef#"]:
            # group.loc[group.index[1:], column] = (
            # ""  # Clear all but the first row for each group
            # )
            group[column] = group[column].astype(str)
            group.loc[group.index[1:], column] = (
                ""  # Clear all but the first row for each group
            )
    return group


def process_csv(file_path: str, lang: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="utf-8")
    df["Language"] = lang
    language = detect_language(df)
    df = translate_header(df, language)

    # Combine 進度 & 時序
    df["Progress Update"] = df.apply(
        lambda row: (
            row["Progress Update"]
            if pd.isna(row["Timeline"]) or row["Timeline"] in TIMELINE_OPTION
            else f"{row['Progress Update']} ({row['Timeline']})"
        ),
        axis=1,
    )

    df["Status"] = df.apply(
        lambda row: (
            row["Timeline"] if row["Timeline"] in TIMELINE_OPTION else row["Status"]
        ),
        axis=1,
    )

    df = merge_rows(df)
    grouped = df.groupby("TempRef#")
    cleaned_df = grouped.apply(clean_group).reset_index(drop=True)

    cleaned_df["Initiative Group"] = cleaned_df.groupby("Ref#")[
        "Initiative Group"
    ].transform(lambda x: x.iloc[0])

    # Ensure TempRef# is propagated correctly
    cleaned_df["TempRef#"] = cleaned_df["TempRef#"].ffill().bfill()

    finalized_df = cleaned_df[
        [
            "Ref#",
            "Language",
            "Smart Area",
            "Initiative Group",
            "Initiative",
            "Progress Update",
            "Status",
            "TempRef#",
        ]
    ]

    return finalized_df


def combine_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Sort by TempRef#, Language, and OriginalOrder
    combined_df["OriginalOrder"] = combined_df.groupby("TempRef#").cumcount()
    combined_df.sort_values(by=["TempRef#", "OriginalOrder"], inplace=True)

    return combined_df


def clean_data_folder(folder_path):
    """Delete all files in the specified folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print("Deleted Files Successfully")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
