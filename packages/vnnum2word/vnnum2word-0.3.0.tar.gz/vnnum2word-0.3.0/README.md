# vnnum2word

Convert numbers to words, with a focus on the Vietnamese language.

This project is inspired by [num2words](https://github.com/savoirfairelinux/num2words).

The original [num2words](https://github.com/savoirfairelinux/num2words) library formats numbers into floats with two decimal places. For example:

```python
from num2words import num2words
num2words(12.5, lang='vi')
# mười hai phẩy năm mươi
num2words(12.556, lang='vi')
# mười hai phẩy năm mươi sáu
```

However, in Vietnamese, these results are often inaccurate or unnatural.
This package fixes those issues and provides more accurate and natural outputs for Vietnamese numbers.

# Installation

```bash
pip install vnnum2word
```

# Usage

```python
from vnnum2word import convert_number, convert_string
convert_number(12.5)
# mười hai phẩy năm
convert_string("giải thưởng là 1000000 đồng")
# giải thưởng là một triệu đồng
convert_string("mã abc123def")
# mã abc một hai ba def
```

## Unittest

```bash
python -m unittest tests/number.py
python -m unittest tests/string.py
```