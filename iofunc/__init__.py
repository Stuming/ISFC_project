"""
This package provides function to load/save data(and others that related to data).

iofile:
  load and save brain imagine data.

create_label:
  provide different way to create label file.

"""

# module import
from .create_label import cl_index, cl_nsteps, cl_vertexes
from .iofile import load_imgfile, load_textfile, save_img
