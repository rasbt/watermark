# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.join("../watermark"))

import watermark

def test_gpu_info():
    a = watermark.watermark(gpu=True)
    txt = a.split('\n')
    clean_txt = [t.strip() for t in txt if t.strip()]
    for t in txt:
        t = t.strip()
        if t:
            t = t.split(':')[0]
            clean_txt.append(t.strip())
    clean_txt = set(clean_txt)

    expected = [
        'GPU Info',
    ]

    for i in expected:
        assert any (i in line for line in clean_txt), f'{i} not found in {clean_txt}'