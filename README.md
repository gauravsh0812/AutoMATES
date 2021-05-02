AutoMATES(Automated Model Assembly from Text, Equations, and Software) 
============================================================================================================================
The AutoMATES project aims to build technology to construct and curate semantically-rich representations of scientific models by integrating three different sources of information using AI/ML, NLP. More detail about the project can be found at https://ml4ai.github.io/automates/

# Prerequisite 
Python 3

chardet(to get equation's encoding type)

pandas

Node.js

pdflatex

pdf2image

Texlive(or any other to view TeX files)

# Usage
This repository consist of _Data Engineering and Preprocessing_ scripts used to construct dataset from scartch.

_**automates_scripts**_ folder contain scripts to build dataset.

**_SLE_** contain scripts to create dataset having single lined equations required at the later stages of the project(while working with Torch(Lua) model of im2markup: https://github.com/harvardnlp/im2markup)

**_Log_problem_scripts_** contain scripts to get insight of various errors I have got during the experimentation.

**_modified_image2markup_** contain modified im2markup preprocessing scripts to make them workable with my dataset.  

**_Docker_** contain DockerFile to create Docker Image to run im2markup model smoothly on any machine.

## Further details can be found under respective folder's README.md
