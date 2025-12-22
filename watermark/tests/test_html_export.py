# -*- coding: utf-8 -*-
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import unittest

def test_html_output_presence():
    
    nb = nbformat.v4.new_notebook()
    
    code = "%load_ext watermark\n%watermark"
    nb.cells.append(nbformat.v4.new_code_cell(code))
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    try:
        ep.preprocess(nb, {'metadata': {'path': '.'}})
        
        cell_output = nb.cells[0].outputs[0].text
        
        assert 'Python implementation' in cell_output
        assert 'IPython version' in cell_output
        print("\n HTML Output Test Passed!")
        
    except Exception as e:
        print(f"\n Test failed due to: {e}")
        raise e

if __name__ == "__main__":
    test_html_output_presence()