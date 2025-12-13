Reference
=========

.. autosummary::
   :toctree: autosummary
   :template: module.rst
   :recursive:

    dachs


..
   # Generate a list of modules from the file names in src/dachs:
   for fn in $(ls -1 src/dachs/*.py); do echo -n "dachs.${$(basename $fn)%.py} "; done;

.. inheritance-diagram:: dachs.metaclasses dachs.reagent dachs.synthesis dachs.equipment
