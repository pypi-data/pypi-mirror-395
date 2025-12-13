#!/usr/bin/env python

#
# TODO:
#
# More sensible way to determine no. of rows
# Add attribute/info icons
#

# Avoid warnings if h5py has MPI support
try:
    import mpi4py
except ImportError:
    pass
else:
    mpi4py.rc.initialize = False

import h5py

import os.path
import sys

from tkinter import *
from idlelib.tree import TreeItem, TreeNode

import tkinter.font as tkFont

ITEM_TOP     = 0
ITEM_GROUP   = 1
ITEM_DATASET = 2
ITEM_ATTR    = 3
ITEM_DESCR   = 4

icon_images = None

# Nodes which are highlighted
selected_nodes = {}

# Format for displaying values
float_fmt = "%14.6e"
int_fmt   = "%d"

# Minimum column width
min_width = 16

# Maximum elements per row
max_elements = 6

# Maximum column width
max_width = max_elements * min_width

def get_shape(data):
    """Return shape of array or [1] if its a scalar"""
    if len(data.shape) > 0:
        return data.shape
    else:
        return [1]

def get_format(dtype):
    # Check for variable length data types
    if h5py.check_string_dtype(dtype) is not None:
        return "%s"
    elif h5py.check_vlen_dtype(dtype) is not None:
        dtype = h5py.check_vlen_dtype(dtype)
    # Choose format string depending on base type
    if dtype.kind == "i" or dtype.kind == "u":
        fmt = int_fmt
    elif dtype.kind == "f":
        fmt = float_fmt
    elif dtype.kind == "S" or dtype.kind == "U" or dtype.kind == "a":
        fmt = "%s"
    else:
        fmt = None
    return fmt

def get_width(dtype):
    if h5py.check_string_dtype(dtype) is not None or h5py.check_vlen_dtype(dtype) is not None:
        return max_width
    elif dtype.kind == "S" or dtype.kind == "U" or dtype.kind == "a":
        return min(max_width, max((dtype.itemsize, min_width)))
    else:
        return min_width

def is_too_big(shape):
    if len(shape) < 2:
        # 1D arrays are always ok
        return False
    elif len(shape) == 2:
        # 2D is ok if second dim is small
        return (shape[1] > max_elements)
    else:
        # Multidimensional array - check no. of elements
        i = shape[1]
        for j in shape[2:]:
            i *= j
        return (i > max_elements)

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def get_icons():
    # idlelib doesn't have appropriate icons for datasets/attributes
    # so encode some here (data strings are base64 encoded .gif files)
    dataset = PhotoImage(data=r'R0lGODlhEAANAPIEADAwMAD//8PDw9zc3P///6usr'+
                         r'QAAAAAAACH5BAEAAAUALAAAAAAQAA0AAAMqOLDcrSHKORe9'+
                         r'0uktuv/fIhBkaZKCCK6deL5ECrCsC5syvaq6BygbzSABADs=')
    node    = PhotoImage(data=r'R0lGODlhCwALAPECAAAAAH9/f////6usrSH5BAEAAA'+
                         r'MALAAAAAALAAsAAAIanI8Wy6wCowhPQjqCvdVivX3b1Elf0y'+
                         r'TqUAAAOw==')
    return {"data":dataset, "attr":node}

def value_to_text(value, fmt):
    """Write out a multidimensional array as text"""
    if isinstance(value, str):
        return value
    elif value.dtype.kind == "O" and value.shape == ():
        # Value is a single object reference
        return value_to_text(value[()], fmt)
    elif len(value.shape) > 0:
        # Value is an array, possibly of objects
        s = []
        for i in range(value.shape[0]):
            s.append(value_to_text(value[i,...], fmt))
        return "[" + (",".join(s)) + "]"
    else:
        # Value is a non-object scalar
        if fmt is None:
            return str(value)
        else:
            return fmt % value

def type_string(dtype):
    """Return a description of a HDF5 data type"""
    if h5py.check_string_dtype(dtype) is not None:
        return "vlen string"
    elif h5py.check_vlen_dtype(dtype) is not None:
        return "vlen "+str(h5py.check_vlen_dtype(dtype))
    else:
        return str(dtype)

class MyTreeNode(TreeNode):
    def __init__(self, canvas, parent, item):
        TreeNode.__init__(self, canvas, parent, item)
        self.item = item
    def select(self, event=None, value=None):
        if self.item.item_type == ITEM_DATASET:
            if value is None:
                self.selected = not(self.selected)
            else:
                self.selected = value
            self.canvas.delete(self.image_id)
            self.drawicon()
            self.drawtext()
            global selected_nodes
            my_id = (self.item.file.filename, self.item.path, self.item.field)
            if self.selected:
                selected_nodes[my_id] = self.item
            else:
                if my_id in selected_nodes:
                    del selected_nodes[my_id]
                
    def geticonimage(self, name):
        global icon_images
        if icon_images is None:
            icon_images = get_icons()
        if name in icon_images:
            return icon_images[name]
        else:
            return TreeNode.geticonimage(self, name)

class TopItem(TreeItem):
    """Top level tree widget item with one sub-item for each file"""
    def __init__(self):
        self.nodes = []
        self.item_type = ITEM_TOP
    def GetText(self):
        return "HDF5 files"
    def IsExpandable(self):
        return True
    def GetSubList(self):
        return self.nodes
    def add_child(self, child):
        self.nodes.append(child)
    
class AttrItem(TreeItem):
    """Tree widget item which represents a HDF5 attribute"""
    def __init__(self, name, value):
        self.name  = name
        self.value = value_to_text(value, None)
        self.item_type = ITEM_ATTR
    def GetText(self):
        return self.name + " = " + self.value
    def IsExpandable(self):
        return False
    def GetSubList(self):
        return []
    def GetIconName(self):
        return "attr"

class DescrItem(TreeItem):
    """Tree widget item which represents a description of a dataset"""
    def __init__(self, id, dtype, field):
        self.item_type = ITEM_DESCR
        self.text = "shape="+str(id.shape)+", dtype="+type_string(dtype)
        if field is None:
            # Don't show layout and chunks for dataset sub-fields
            plist = id.get_create_plist()
            if plist.get_layout() == h5py.h5d.CHUNKED:
                chunk = plist.get_chunk()
                self.text += ", chunks="+str(chunk)
            for i in range(plist.get_nfilters()):
                (code, flags, value, name) = plist.get_filter(i)
                self.text += ", "+str(name.decode())
    def GetText(self):
        return self.text
    def IsExpandable(self):
        return False
    def GetSubList(self):
        return []
    def GetIconName(self):
        return "attr"

#
# Use low level interface instead of instantiating h5py objects for every
# tree item in here to avoid performance issue with datasets with
# many chunks if using h5py < 2.0.
#
class HDF5Item(TreeItem):
    """Tree widget item which represents a HDF5 file, group or dataset"""
    def __init__(self, id, name="", file=None, is_file=False, parent_name="", field=None):
        self.id      = id
        self.file    = file
        self.is_file = is_file
        self.name    = name
        if field is None:
            self.path    = (parent_name+"/"+name).lstrip("/")
        else:
            self.path = parent_name
        self.field   = field if field is not None else ()
        if isinstance(self.id, h5py.h5d.DatasetID):
            self.item_type = ITEM_DATASET
        else:
            self.item_type = ITEM_GROUP
    def GetText(self):
        if self.is_file:
            return self.file.filename
        else:
            return self.name
    def IsExpandable(self):
        return True
    def GetSubList(self):
        sublist = []
        if isinstance(self.id, h5py.h5d.DatasetID):
            # This is a dataset or a sub-field of a dataset. Find its data type.
            dtype = self.id.get_type().dtype
            if self.field is not None:
                for f in self.field:
                    dtype = dtype[f]
            # Add its description to the tree.
            sublist.append(DescrItem(self.id, dtype, field=self.field))
            # Check for compound type and add sub fields
            if dtype.fields is not None:
                for field in dtype.fields:
                    sublist.append(HDF5Item(self.id, field, self.file,
                                            parent_name=self.path, field=self.field+(field,)))
        if isinstance(self.id, h5py.h5g.GroupID):
            # This is a group. Add its members to the tree.
            n = self.id.get_num_objs()
            for i in range(n):
                name = self.id.get_objname_by_idx(i)
                ot   = self.id.get_objtype_by_idx(i)
                if ot == h5py.h5g.DATASET:
                    subid = h5py.h5d.open(self.id, name)
                    sublist.append(HDF5Item(subid, name.decode(), self.file,
                                            parent_name=self.path)) 
                elif ot == h5py.h5g.GROUP:
                    subid = h5py.h5g.open(self.id, name)
                    sublist.append(HDF5Item(subid, name.decode(), self.file,
                                            parent_name=self.path))
                else:
                    # Unsupported object type
                    pass
        # Get number of attributes on this object
        try:
            nr_attrs = h5py.h5a.get_num_attrs(self.id)
        except ValueError:
            # Workaround for old HDF5 versions: need to open root group
            if self.is_file:
                nr_attrs = h5py.h5a.get_num_attrs(self.id["/"])
            else:
                raise
        # Add attributes of this object to the tree
        if nr_attrs > 0: 
            for name in self.get_data().attrs.keys():
                try:
                    value = self.get_data().attrs[name]
                except IOError as e:
                    pass
                else:
                    sublist.append(AttrItem(name, value))

        return sublist
    def GetIconName(self):
        if self.item_type == ITEM_DATASET:
            return "data"
        else:
            return "folder"
    def get_data(self):
        if len(self.path) > 0:
            return self.file[self.path]
        else:
            return self.file

class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

class DataWindow():
    def __init__(self, data):

        global windows_open
        windows_open += 1
        
        self.ids = data.keys()
        self.filenames = [id[0] for id in self.ids]
        self.names     = [id[1] for id in self.ids]
        self.fields    = [id[2] for id in self.ids]
        self.datasets  = [data[k].get_data() for k in self.ids]
        self.nrows_tot = max([get_shape(arr)[0] for arr in self.datasets])

        # Sort by file name
        #idx = argsort(self.filenames)
        sort_key = [fn + n for (fn,n) in zip(self.filenames, self.names)]
        idx = argsort(sort_key)
        self.names     = [self.names[i]     for i in idx]
        self.filenames = [self.filenames[i] for i in idx]
        self.datasets  = [self.datasets[i]  for i in idx]
        self.fields    = [self.fields[i]    for i in idx]

        # Figure out which columns need to show file names
        self.nspan = [1 for _ in range(len(self.names))]
        for i in range(len(self.names)-1):
            for j in range(i+1,len(self.names)):
                if self.filenames[i] == self.filenames[j]:
                    self.nspan[i] += 1
        for i in range(1, len(self.names)):
            if self.filenames[i] == self.filenames[i-1]:
                self.nspan[i] = 0
                    
        # Make top level window
        self.toplevel = Toplevel()
        self.toplevel.title("HDF5 data table")
        self.toplevel.grid_rowconfigure(0,weight=1)
        self.toplevel.grid_columnconfigure(0,weight=1)

        # Add label, entry and button for jumping to row
        lframe = Frame(self.toplevel)
        lframe.grid(row=2, column=0, sticky=E+W)
        lframe.columnconfigure(0, weight=0)
        lframe.columnconfigure(1, weight=0)
        lframe.columnconfigure(2, weight=1)
        self.label = Label(lframe, text="Find index: ")
        self.label.grid(row=2, column=0)
        self.entry = Entry(lframe)
        self.entry.grid(row=2, column=1)
        self.entry.bind("<Return>", self.on_return)

        # Add row count
        self.rowlabel = Label(lframe, text="Total rows: "+str(self.nrows_tot))
        self.rowlabel.grid(row=2, column=2, sticky=E)

        # Make vertical scroll bar
        self.vsbar = AutoScrollbar(self.toplevel, orient=VERTICAL,
                                   command=self.scrollbar_moved)
        self.vsbar.grid(row=0, column=1, sticky=N+S)

        # Make horizontal scroll bar
        hsbar = AutoScrollbar(self.toplevel, orient=HORIZONTAL)
        hsbar.grid(row=1, column=0, sticky=E+W)

        # Put a canvas in the window
        self.canvas = Canvas(self.toplevel, xscrollcommand=hsbar.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        hsbar.config(command=self.canvas.xview)                   

        # Put a frame in the canvas
        self.frame = Frame(self.canvas, bd=3, relief=SUNKEN)
        self.frame.rowconfigure(2,weight=1)

        # Calculate column widths
        self.widths = []
        for (name,dset,fname,fields) in zip(self.names,self.datasets,self.filenames,self.fields):
            dtype = dset.dtype
            for f in fields:
                dtype = dtype[f]
            width = get_width(dtype)
            if len(dset.shape) > 1:
                width += 3
                for s in dset.shape[1:]:
                    width *= s
            if is_too_big(dset.shape):
                width = min_width
            width = min((max_width, max(width, len(name))))
            self.widths.append(width)

        # Calculate file name widths
        self.fname_widths = []
        icol = 0
        for (width, nspan) in zip(self.widths, self.nspan):
            w = 0
            for i in range(nspan):
                w += self.widths[icol+i]
            self.fname_widths.append(w)
            icol += 1
            
        # Add text widgets with column headings and data columns
        font = tkFont.Font(family="courier", size=-16)
        self.title = []
        self.column = []
        self.fname  = []
        icol = 1
        self.index  = Text(self.frame, font=font, wrap=NONE,
                           width=12, bg="light cyan")
        self.index.grid(row=2, column=0, sticky=W+N+S)
        for (name,dset,fname,width,fw,fields) in zip(self.names,self.datasets,
                                                     self.filenames, self.widths,
                                                     self.fname_widths, self.fields):
            if len(fields) == 0:
                # Basic type - just display the dataset name
                display_name = name
            else:
                # Compound type - need to display the field name too
                display_name = "|".join((name,)+fields)

            self.title.append(Text(self.frame, font=font, wrap=NONE,
                                   width=width, height=1, bg="light yellow"))
            self.title[-1].insert("end", display_name+" ")
            self.title[-1].grid(row=1, column=icol,sticky=N+W)
            self.title[-1].config(state=DISABLED)
            self.column.append(Text(self.frame, font=font, wrap=NONE,
                                    width=width, bg="white", setgrid=1))
            self.column[-1].grid(row=2, column=icol, sticky=W+N+S)
            self.column[-1].config(state=DISABLED)

            # Add file name spanning columns from same file
            if self.nspan[icol-1] > 0:
                self.fname.append(Text(self.frame, font=font, wrap=NONE,
                                       height=1, width=fw))
                self.fname[-1].grid(row=0, column=icol, sticky=E+W,
                                    columnspan=self.nspan[icol-1])
                self.fname[-1].insert("end", fname)
                self.fname[-1].config(state=DISABLED)

            icol += 1

        self.win = self.canvas.create_window(0, 0, anchor=NW,
                                             window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Resize window if size of canvas changes
        self.canvas.bind( '<Configure>', self.on_resize)

        # Scrolling with keys/mouse wheel
        # TODO - see if there's a way to get events passed to the parent
        # frame instead of binding everything!
        self.bind_scrolling(self.canvas)
        self.bind_scrolling(self.frame)
        self.bind_scrolling(self.index)
        self.bind_scrolling(self.vsbar)
        self.bind_scrolling(self.entry)
        self.bind_scrolling(self.label)
        for c in self.column:
            self.bind_scrolling(c)
        for t in self.title:
            self.bind_scrolling(t)
        for f in self.fname:
            self.bind_scrolling(f)
            
        # Store height of one row of text
        for i in range(1000):
            self.index.insert("end", str(i)+"\n")
        height = self.index.winfo_height()
        nrows = int(self.index.index("@0,%d" % height).split(".")[0])
        self.row_height = int(height//nrows)

        # Set up initial content
        self.update_nrows()
        self.move_to_row(0)
        self.frame.focus_set()

        self.toplevel.protocol("WM_DELETE_WINDOW", self.destroy)

    def bind_scrolling(self, widget):
        widget.bind("<Prior>", self.pageup)
        widget.bind("<Next>",  self.pagedown)
        widget.bind("<Button-4>", self.pageup)
        widget.bind("<Button-5>", self.pagedown)

    def on_resize(self, event):
        # Resize the data window
        self.canvas.itemconfig(self.win, height=event.height)
        self.canvas.update_idletasks()
        self.update_nrows()
        # Resize text widgets
        #self.index.configure(height=self.nrows_display)
        #for c in self.column:
        #    c.configure(height=self.nrows_display)
        # Redraw values
        self.update_scroll_bar()
        self.update_data()

    def update_data(self):
        # Redraw array index
        self.index.config(state=NORMAL)
        self.index.delete(1.0, END)
        self.ilast = min(self.ifirst + self.nrows_display, self.nrows_tot)
        for i in range(self.ifirst, self.ilast):
            if i < self.ilast -1:
                self.index.insert("end", str(i)+"\n")
            else:
                self.index.insert("end", str(i))
        self.index.config(state=DISABLED)
        # Redraw columns
        for col, dat, fields in zip(self.column, self.datasets, self.fields):
            # Find data type of this column
            dtype = dat.dtype
            for f in fields:
                dtype = dtype[f]
            # Clear this column
            col.config(state=NORMAL)
            col.delete(1.0, END)
            # Check the data is something we can sensibly display
            if is_too_big(dat.shape):
                col.insert("end", "Unable to display!")
            else:
                # Check at least one value is to be displayed
                if len(dat.shape) == 0:
                    # Its a scalar, so only visible if scrolled up to the top
                    if self.ifirst == 0:
                        # Decide format to use
                        fmt = get_format(dat.dtype)
                        col.insert("end", value_to_text(dat[...], fmt)+"\n")
                else:
                    # Its an array
                    if self.ifirst < dat.shape[0] and self.ilast > self.ifirst:
                        ilast = min(self.ilast, dat.shape[0])
                        # Read the data
                        d = dat[self.ifirst:ilast, ...]
                        for f in fields:
                            d = d[f]
                        # Decide format to use
                        fmt = get_format(d.dtype)
                        # Add values to display
                        for i in range(d.shape[0]):
                            if i < d.shape[0] - 1:
                                col.insert("end", value_to_text(d[i,...],fmt)+
                                           "\n")
                            else:
                                col.insert("end", value_to_text(d[i,...],fmt))
  
            col.config(state=DISABLED)


    def update_scroll_bar(self):
        lo = float(self.ifirst) / float(self.nrows_tot)
        hi = float(self.ilast)  / float(self.nrows_tot)
        self.vsbar.set(lo, hi)

    def scrollbar_moved(self, action, *args):
        if action == "moveto":
            offset = float(args[0])
            i = int(offset * self.nrows_tot)
        elif action == "scroll":
            step = int(args[0])
            what = args[1]
            if what == "units":
                i = self.ifirst + step
            else:
                i = self.ifirst + step * self.nrows_display
        self.move_to_row(i)
    
    def on_return(self, event):
        try:
            i = int(self.entry.get())
        except ValueError:
            pass
        else:
            self.move_to_row(i)

    def move_to_row(self, i):
        self.ifirst = i
        if self.ifirst >= self.nrows_tot - self.nrows_display:
            self.ifirst = self.nrows_tot - self.nrows_display
        if self.ifirst < 0:
            self.ifirst = 0
        self.ilast = min((self.ifirst + self.nrows_display,
                          self.nrows_tot))
        self.update_scroll_bar()
        self.update_data()

    def pageup(self, event):
        self.move_to_row(self.ifirst - self.nrows_display)
        return "break"

    def pagedown(self, event):
        self.move_to_row(self.ifirst + self.nrows_display)
        return "break"

    def destroy(self, *args):
        global windows_open
        global root
        self.toplevel.destroy()
        windows_open -= 1
        if windows_open == 0:
            root.destroy()

    def update_nrows(self):
        n = ((self.index.winfo_height()-0.5*self.row_height)/
             self.row_height)
        n = max((0, n))
        self.nrows_display = int(n)
        
class BrowserWindow():
    def __init__(self, filenames):

        global windows_open
        windows_open += 1

        nloaded = 0

        self.windows = []

        self.toplevel = Toplevel()
        self.toplevel.title("HDF5 Browser")
        self.toplevel.config(bg="white")

        canvas = Canvas(self.toplevel)
        canvas.config(bg='white')
        canvas.grid(sticky=N+S+E+W)
        top_item = TopItem()
        top_node = MyTreeNode(canvas, None, top_item)

        vsbar = AutoScrollbar(self.toplevel)
        vsbar.config(command=canvas.yview)                   
        canvas.config(yscrollcommand=vsbar.set)              
        vsbar.grid(row=0, column=1, sticky=N+S)

        hsbar = AutoScrollbar(self.toplevel, orient=HORIZONTAL)
        hsbar.config(command=canvas.xview)                   
        canvas.config(xscrollcommand=hsbar.set)              
        hsbar.grid(row=1, column=0, sticky=E+W)
        canvas.bind('<4>', lambda event : canvas.yview('scroll', -1, 'units'))
        canvas.bind('<5>', lambda event : canvas.yview('scroll', 1, 'units'))

        self.toplevel.grid_rowconfigure(0, weight=1)
        self.toplevel.grid_columnconfigure(0, weight=1)
        
        for fname in sys.argv[1:]:
            try:
                f = h5py.File(fname, "r")
            except IOError:
                print("Unable to read file: ", fname)
                continue
            top_item.add_child(HDF5Item(f.id, file=f, is_file=True))
            nloaded += 1

        if nloaded == 0:
            raise IOError("No files loaded!")

        bframe = Frame(self.toplevel, relief="raised", borderwidth=2)
        bframe.grid(row=2, column=0, sticky=N+S+E+W)
        b1 = Button(bframe, text="Open selected datasets as table",
                    command=self.open_datasets)
        b1.grid(row=0, column=0)

        b2 = Button(bframe, text="Deselect all",
                    command=self.deselect_all)
        b2.grid(row=0, column=1)
        
        self.canvas   = canvas
        self.top_node = top_node
        self.top_item = top_item
        
        top_node.update()
        top_node.expand()

        self.toplevel.protocol("WM_DELETE_WINDOW", self.destroy)

    def open_datasets(self):
        if len(selected_nodes.keys()) > 0:
            self.windows.append(DataWindow(selected_nodes))

    def deselect_all(self):
        global selected_nodes
        self.top_node.deselecttree()
        selected_nodes = {}

    def destroy(self, *args):
        global windows_open
        global root
        self.toplevel.destroy()
        windows_open -= 1
        if windows_open == 0:
            root.destroy()

def main():
            
    global root
    global windows_open

    root = Tk()
    root.withdraw()
    
    windows_open = 0

    filenames = sys.argv[1:]
    mainwin = BrowserWindow(filenames)

    root.mainloop()
