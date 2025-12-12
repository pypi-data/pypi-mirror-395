from yklib_diff_getter import get_unified_diff, get_unified_diff_string


def test_get_unified_diff():
    text1 = "これはテストです。\n1行目\n2行目\n3行目"
    text2 = "これはテストです。\n1行目\n2行目（変更）\n4行目"
    expected_diff = [
        "--- 変更前\n",
        "+++ 変更後\n",
        "@@ -1,4 +1,4 @@\n",
        " これはテストです。",
        " 1行目",
        "-2行目",
        "-3行目",
        "+2行目（変更）",
        "+4行目",
    ]
    assert get_unified_diff(text1, text2) == expected_diff


def test_get_unified_diff_string():
    text1 = "これはテストです。\n1行目\n2行目\n3行目"
    text2 = "これはテストです。\n1行目\n2行目（変更）\n4行目"
    expected_diff_string = "--- 変更前\n\n+++ 変更後\n\n@@ -1,4 +1,4 @@\n\n これはテストです。\n 1行目\n-2行目\n-3行目\n+2行目（変更）\n+4行目"  # noqa: E501
    assert get_unified_diff_string(text1, text2) == expected_diff_string
