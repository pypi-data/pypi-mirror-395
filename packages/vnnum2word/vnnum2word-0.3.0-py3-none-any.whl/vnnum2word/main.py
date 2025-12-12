
from __future__ import unicode_literals

import re

to_19 = (
    u"không",
    u"một",
    u"hai",
    u"ba",
    u"bốn",
    u"năm",
    u"sáu",
    u"bảy",
    u"tám",
    u"chín",
    u"mười",
    u"mười một",
    u"mười hai",
    u"mười ba",
    u"mười bốn",
    u"mười lăm",
    u"mười sáu",
    u"mười bảy",
    u"mười tám",
    u"mười chín",
)
tens = (u"hai mươi", u"ba mươi", u"bốn mươi", u"năm mươi",
        u"sáu mươi", u"bảy mươi", u"tám mươi", u"chín mươi")
denom = (
    "",
    u"nghìn",
    u"triệu",
    u"tỷ",
    u"nghìn tỷ",
    u"trăm nghìn tỷ",
    "Quintillion",
    "Sextillion",
    "Septillion",
    "Octillion",
    "Nonillion",
    "Decillion",
    "Undecillion",
    "Duodecillion",
    "Tredecillion",
    "Quattuordecillion",
    "Sexdecillion",
    "Septendecillion",
    "Octodecillion",
    "Novemdecillion",
    "Vigintillion",
)


def convert_nn(val):
    if val < 20:
        return to_19[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
        if dval + 10 > val:
            if val % 10:
                a = u"lăm"
                if to_19[val % 10] == u"một":
                    a = u"mốt"
                else:
                    a = to_19[val % 10]
                if to_19[val % 10] == u"năm":
                    a = u"lăm"
                return dcap + " " + a
            return dcap


def convert_nnn(val):
    word = ""
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        word = to_19[rem] + u" trăm"
        if mod > 0:
            word = word + " "
    if mod > 0 and mod < 10:
        if mod == 5:
            word = word != "" and word + u"lẻ năm" or word + u"năm"
        else:
            word = word != "" and word + u"lẻ " + \
                convert_nn(mod) or word + convert_nn(mod)
    if mod >= 10:
        word = word + convert_nn(mod)
    return word


def vietnam_number(val):
    if val < 100:
        return convert_nn(val)
    if val < 1000:
        return convert_nnn(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
        if dval > val:
            mod = 1000 ** didx
            lval = val // mod
            r = val - (lval * mod)

            ret = convert_nnn(lval) + u" " + denom[didx]
            if 99 >= r > 0:
                ret = convert_nnn(lval) + u" " + denom[didx] + u" lẻ"
            if r > 0:
                ret = ret + " " + vietnam_number(r)
            return ret


def convert_number(number):
    """
    Chuyển số (có thể có phần thập phân) sang chữ tiếng Việt.

    Quy ước phần thập phân:
    - Nếu có 1 hoặc 2 chữ số: coi cả phần thập phân là một số nguyên rồi đọc bình thường.
      Ví dụ: 3.1  -> "ba phẩy một"
              3.14 -> "ba phẩy mười bốn"
    - Nếu có từ 3 chữ số trở lên: đọc từng chữ số một.
      Ví dụ: 3.141 -> "ba phẩy một bốn một"
    """

    s = str(number)

    # Không có dấu thập phân -> chỉ đọc phần nguyên
    if "." not in s:
        return vietnam_number(int(s))

    int_part, frac_part = s.split(".", 1)

    # Bỏ các số 0 ở cuối phần thập phân (nếu có) để tránh đọc "không" dư
    frac_part = frac_part.rstrip("0")

    start_word = vietnam_number(int(int_part))
    if not frac_part:
        # Không còn phần thập phân có ý nghĩa
        return start_word

    # 1 hoặc 2 chữ số: coi là một số nguyên
    if len(frac_part) <= 2:
        end_word = vietnam_number(int(frac_part))
    else:
        # Từ 3 chữ số trở lên: đọc từng chữ số
        digit_words = [to_19[int(ch)] for ch in frac_part]
        end_word = " ".join(digit_words)

    return start_word + " phẩy " + end_word


def convert_string(text, converter=None):
    """
    Chuyển tất cả số trong chuỗi sang phiên âm tiếng Việt.

    Ví dụ:
        "anh có 123 đồng" -> "anh có một trăm hai mươi ba đồng"
    """

    def _replace(match):
        num_str = match.group(0)

        s = match.string
        start, end = match.start(), match.end()
        # Kiểm tra xem số có dính liền với chữ hai bên không
        left_adjacent = start > 0 and not s[start - 1].isspace()
        right_adjacent = end < len(s) and not s[end].isspace()

        # Nếu số gắn liền với chữ (ví dụ: "abc123def", "sp001")
        # thì đọc TỪNG CHỮ SỐ
        if left_adjacent or right_adjacent:
            digit_words = [to_19[int(ch)] for ch in num_str if ch.isdigit()]
            word = " ".join(digit_words)
        else:
            # Ngược lại, đọc theo quy tắc số nguyên / số thập phân bình thường
            if "," in num_str:
                # Nếu có dấu phẩy, coi đây là số thập phân với dấu thập phân là ","
                try:
                    # Đổi "," thành "." để tận dụng convert_number hiện tại
                    num = float(num_str.replace(",", "."))
                except ValueError:
                    return num_str
                word = convert_number(num)
            else:
                # Ngược lại, xử lý như số nguyên bình thường
                try:
                    num = int(num_str)
                except ValueError:
                    # Nếu vì lý do gì đó không parse được thì trả lại chuỗi gốc
                    return num_str
                word = vietnam_number(num)

        # Thêm khoảng trắng nếu số dính liền với chữ (ví dụ: "abc123def")
        prefix = ""
        suffix = ""

        if left_adjacent:
            prefix = " "
        if right_adjacent:
            suffix = " "

        return prefix + word + suffix

    # Tìm tất cả các cụm số: hoặc số nguyên (\d+), hoặc số thập phân có dấu phẩy (\d+,\d+)
    pattern = r"\d+,\d+|\d+"
    return re.sub(pattern, _replace, text)
