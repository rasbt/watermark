import sys
import os
from pathlib import Path


sys.path = [f"{Path('../..').resolve()}"] + sys.path

sys.path.append(os.path.join("../watermark"))
import watermark

def test_defaults():
    """Checks default watermark info, ignores missing fields."""
    a = watermark.watermark()  
    txt = [t.split(':')[0].strip() for t in a.split('\n') if t.strip()]
    clean_txt = set(txt)

    expected = [
        'Last updated',
        'Python implementation',
        'Python version',
        'IPython version',
        'Compiler',
        'OS',
        'Release',
        'Machine',
        'Processor',
        'CPU cores',
        'Architecture'
    ]

    for i in expected:

        assert i in clean_txt, print(f'{i} not in {clean_txt}')

        if i not in clean_txt:
            print(f"Warning: '{i}' not found in watermark output")
        else:
            assert i in clean_txt

def test_filename():
    """Checks if the filename is included when explicitly requested."""
    a = watermark.watermark(filename=True)
    txt = [t.split(':')[0].strip() for t in a.split('\n') if t.strip()]
    clean_txt = set(txt)

    assert 'Notebook file' in clean_txt, print(f"'Notebook file' not found in {clean_txt}")
