# sqlite3_arabic_phonetic_fuzzy_trigram

This package provides an SQLite3 Python wrapper bundled
with [`sqlite3-arabic-phonetic-fuzzy-trigram/`](https://github.com/Greentech-Apps-Limited/sqlite3-arabic-phonetic-fuzzy-trigram/). It's a drop-in replacement
for the standard library's [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) module as the std one doesn't
support loading extension.

```
pip install sqlite3_arabic_phonetic_fuzzy_trigram
```

```python
import sqlite3_arabic_phonetic_fuzzy_trigram

# load the tokenizer
sqlite3_arabic_phonetic_fuzzy_trigram.load()

# has the same API as the default `sqlite3` module
conn = sqlite3_arabic_phonetic_fuzzy_trigram.connect(":memory:")
conn.execute("create table quran(sura, ayah, text)")

# and comes with the `sqlite3_arabic_phonetic_fuzzy_trigram`
cur = conn.execute("create table quran(sura, ayah, text, tokenize='arabic_phonetic_fuzzy_trigram')")
print(cur.fetchone())

conn.close()
```

## Installation

A binary package (wheel) is available for the following operating systems:

- Windows (64-bit)
- Linux (64-bit)
- macOS (both Intel and Apple processors)

```
pip install sqlite3_arabic_phonetic_fuzzy_trigram
```

## Building from source

For development purposes only.

Prepare source files:

```
make prepare-src
make download-sqlite
make download-sqlite3_arabic_phonetic_fuzzy_trigram
```

Build and test the package:

```
make clean
python setup.py build_ext -i
python -m test
python -m pip wheel . -w dist
```

## Credits

Based on the [pysqlite3](https://github.com/coleifer/pysqlite3) project. Available under the [Zlib license](LICENSE).
Packaging help from [sqlean.py](https://github.com/nalgeon/sqlean.py)


