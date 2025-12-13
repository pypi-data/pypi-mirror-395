# h5tab - view tabular data stored as HDF5 datasets

This is a simple utility to display multiple HDF5 datasets as columns in a
table. This is useful when you need to look up elements with the same index
between different datasets.

## Usage

Run the script with the names of one or more HDF5 files as arguments.
```
h5tab.py filename ...
```
This brings up a tree view where you can select datasets to open. Clicking
a dataset toggles it between selected and not selected.

Once you've selected all of the datasets to open click the "Open
selected datasets" button at the bottom of the window. This opens a new
window with a table where the columns correspond to the selected datasets
and the rows are the dataset element index (in the first dimension in case
of multidimensional datasets).

In the case of compound data types, individual fields can be designated
as table columns.

Only the displayed portions of the datasets are read in, so very large
datasets can be viewed.

## Limitations

This is not a general purpose HDF5 file viewer.

  * Table rows always correspond to the first dimension so datasets with
    large dimensions other than the first can't be displayed
  * The program has no good way to display variable length datasets
  * The tree view can be slow for large numbers of datasets
