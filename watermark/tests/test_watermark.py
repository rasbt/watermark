# -*- coding: utf-8 -*-

import watermark


def test_defaults():
    a = watermark.watermark()
    txt = a.split('\n')
    clean_txt = []
    for t in txt:
        t = t.strip()
        if t:
            t = t.split(':')[0]
            clean_txt.append(t.strip())
    clean_txt = set(clean_txt)

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
        'Architecture']

    for i in expected:
        assert i in clean_txt, print(f'{i} not in {clean_txt}')
