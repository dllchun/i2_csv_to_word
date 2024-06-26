import pandas as pd
from docx.enum.section import WD_ORIENTATION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re


def detect_language(df: pd.DataFrame) -> str:
    if "參考#" in df.columns:
        return "TC"
    elif "Ref#" in df.columns:
        return "EN"
    elif "参考#" in df.columns:
        return "SC"
    else:
        raise ValueError("Unknown language for the CSV file headers")


def translate_header(df: pd.DataFrame, language: str) -> pd.DataFrame:
    if language == "TC":
        df = df.rename(
            columns={
                "SM_Ref": "SM_Ref#",
                "參考#": "Ref#",
                "智慧範疇": "Smart Area",
                "措施組合": "Initiative Group",
                "措施": "Initiative",
                "進度": "Progress Update",
                "狀況": "Status",
                "時序": "Timeline",
                "標題": "Heading",
                "新措施": "New Initiative",
                "標題值": "Heading Value",
                "排序": "Sorting Order",
            }
        )
    elif language == "EN":
        df = df.rename(
            columns={
                "SM_Ref": "SM_Ref#",
                "Ref#": "Ref#",
                "Smart Area": "Smart Area",
                "Initiative Group": "Initiative Group",
                "Initiative": "Initiative",
                "Progress Update": "Progress Update",
                "Status": "Status",
                "Timeline": "Timeline",
                "Heading": "Heading",
                "New Initiative": "New Initiative",
                "Heading Value": "Heading Value",
                "Sorting Order": "Sorting Order",
            }
        )
    elif language == "SC":
        df = df.rename(
            columns={
                "SM_Ref": "SM_Ref#",
                "参考#": "Ref#",
                "智慧范畴": "Smart Area",
                "措施组合": "Initiative Group",
                "措施": "Initiative",
                "进度": "Progress Update",
                "状况": "Status",
                "时序": "Timeline",
                "标题": "Heading",
                "新措施": "New Initiative",
                "标题值": "Heading Value",
                "排序": "Sorting Order",
            }
        )

    return df


# Word Related
def set_table_borders(table):
    tbl = table._tbl  # Get the table's XML element
    tbl_pr = tbl.tblPr  # Get the table properties element

    # Create a table borders element
    tbl_borders = OxmlElement("w:tblBorders")

    # Define border styles
    borders = {
        "top": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
        "left": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
        "bottom": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
        "right": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
        "insideH": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
        "insideV": {"sz": 12, "val": "single", "color": "000000", "space": "0"},
    }

    # Create and append border elements
    for border_name, border_attrs in borders.items():
        border = OxmlElement(f"w:{border_name}")
        for attr_name, attr_value in border_attrs.items():
            border.set(qn(f"w:{attr_name}"), str(attr_value))
        tbl_borders.append(border)

    tbl_pr.append(tbl_borders)


def add_bold_text(paragraph, text):
    parts = re.split(r"(\*\*.*?\*\*)", text)  # Split text by bold markers
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])  # Remove the ** markers
            run.bold = True
            run.underline = True

        else:
            paragraph.add_run(part)
