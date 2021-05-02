Scripts:
===========================

**_single_line_equation.py_** script used to convert multiple line equations(generally written in format: /begin{} ---- /end{}) into a single line equation required by the im2markup model.

NOTE: source and destination need to modified as per one's system.
```
python single_line_equation.py 
```
**_SLE_latex2mml.py,  SLE_mathml_simplification.py, SLE_etreeParser.py_** used to render MathML from the LaTeX equations, for its simplification and rendering XML.etree.ElemnetTree
```
python SLE_latex2mml.py -src </path/to/arxiv/papers/>  -dst </path/to/destination/of/parsed_equations/>  -yr </path/to/year/folder/> -dir </path/to/specific/month/directory/>
```
```
python SLE_mathml_simplification.py -src </path/to/arxiv/papers/>  -dst </path/to/destination/of/parsed_equations/>  -yr </path/to/year/folder/> -dir </path/to/specific/month/directory/>
```
```
python SLE_etreeParser.py -src </path/to/arxiv/papers/>  -dst </path/to/destination/of/parsed_equations/>  -yr </path/to/year/folder/> -dir </path/to/specific/month/directory/>
```
