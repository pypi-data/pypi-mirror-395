"""
Graphical user interface (GUI) utilities & helpers
"""
import matplotlib as mpl
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from zdev.plot import axxess


# INTERNAL PARAMETERS & DEFAULTS
_ATTR_DATA = ('text',)
_ATTR_SIZE = ('geometry', 'sizePolicy', 'minimumSize', 'maximumSize', 'baseSize') # QWidget
_ATTR_BEHAVIOUR = (
    # QAbstractItemView
    'selectionMode', 'autoScroll', 'verticalScrollMode', 'horizontalScrollMode',
    # Note: The following will be handeled in a defined way:
    #       'dragDropOverwriteMode', 'defaultDropAction', 'dragEnabled', 'dragDropMode',
    # QAbstractScrollArea
    'sizeAdjustPolicy', 'verticalScrollBarPolicy', 'horizontalScrollBarPolicy',
    # QListView
    'layoutMode', 'resizeMode', 'viewMode', 'batchSize', 'isWrapping', 'wordWrap', 'selectionRectVisible',
    # QListWidget
    'sortingEnabled',
    )
_ATTR_VISUALS = (
    # QWidget (cont'd)
    'enabled', 'focusPolicy', 'font', 'palette', 'locale', 'layoutDirection', 'styleSheet',
    'autoFillBackground', 'toolTip', 'toolTipDuration', 'statusTip', 'whatsThis',
    # QFrame
    'frameShape', 'frameShadow', 'lineWidth', 'midLineWidth',
    # # QAbstractItemView
    'alternatingRowColors', 'showDropIndicator',
    )

# Note: If a QListWidget is set to do 'dragDropMode=InternalMove' in QDesigner, it CANNOT be
#       used with these 'drag & drop' versions!


#-----------------------------------------------------------------------------------------------


class QLabel_drop(QLabel):
    """ Drop version of builtin 'QLabel' widget. """

    def __init__(self, text=None, drop_func=None):
        super().__init__()
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)  #### FIXME: n/a, drag is NOT supported by base class!
        if (text):
            self.setText(text)
        else:
            self.setText('[label]')
        self.drop_func = drop_func
        return

    def dragEnterEvent(self, event):
        """ Checks if incoming MIME data can be used (or not). """
        mimeData = event.mimeData()
        if (('application/x-qabstractitemmodeldatalist' in mimeData.formats()) or
            ('text/plain' in mimeData.formats())):
            event.accept()
        else:
            event.ignore()
        return

    def dropEvent(self, event):
        """ Consumes incoming MIME data and performs acc. action. """
        mimeData = event.mimeData()
        str_data = drop_data2str(mimeData)
        if (self.drop_func):
            self.drop_func(str_data)
        else:
            self.setText(str_data)
        return

    # def dragMoveEvent(self, event): #### FIXME: n/a, drag is NOT supported by base class!
    #      mimeData = event.mimeData()
    #      val = self.getText()
    #      print(f"The label says -> {val}!")
    #      mimeData.setText( val )
    #      return

    # Note: Solution could be adjusted to "move" operation (if desired) acc. to:
    # [ https://stackoverflow.com/questions/22774168/how-to-drag-and-drop-from-listwidget-onto-combobox ]


#-----------------------------------------------------------------------------------------------


class QListWidget_drag(QListWidget):
    """ Drag&drop version of builtin 'QListWidget' widget. """

    def __init__(self, drop_func=None):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(False) # FIXME: Set to 'True' if "determine index 'n'" issue solved!
        self.drop_func = drop_func


    def dragMoveEvent(self, event):
        """ Sets MIME data once dragging is started. """
        mimeData = event.mimeData()
        vals = self.selectedItems()
        if (len(vals) == 1):
            sel_str = vals[0].text()
        else: # concatenate strings
            sel_all = [item.text() for item in vals]
            sel_str = ', '.join(sel_all)
        mimeData.setText( sel_str )


    def dragEnterEvent(self, event):
        """ Checks if incoming MIME data can be used (or not). """
        mimeData = event.mimeData()
        if (('application/x-qabstractitemmodeldatalist' in mimeData.formats()) or
            ('text/plain' in mimeData.formats())):
            event.accept()
        else:
            event.ignore()
        return


    def dropEvent(self, event):
        """ Consumes incoming MIME data and performs acc. action. """
        if (self.dragDropMode() == QAbstractItemView.InternalMove):
            pass # FIXME!
        else:
            mimeData = event.mimeData()
            str_data = drop_data2str(mimeData)
            if (self.drop_func):
                self.drop_func(str_data)
            else:
                new_item = QListWidgetItem(str_data[0]) # FIXME!
                # self.addItem( new_item )      # adds @ end
                # self.insertItem(n, new_item)  # FIXME: how to determine index 'n' to place?

                # print(new_item.text())

                #### FIXME: how to determine index 'n' to place?
                # print(f"now @ {event.pos()}")
                # print(f"...and self pos is {self.pos()}")
                # print(f"...and self size is {self.size()}")
                # print(f"...and point size {self.font().pointSize()}")
                # QS = self.size()
                # H = QS.height()
                # EP = event.pos()
                # eh = EP.y()
                # ehip = eh / self.font().pointSize()
                # print
                # print(ehip)

                # self.items()
                # for n in range(len(self)):
                #     # self.itemAt(n).pos()
                #     self.item(n)

                # selected: self.currentRow()

            return


#-----------------------------------------------------------------------------------------------


class QFigure_drop(FigureCanvasQTAgg):
    """ Manage plots for PyQt GUIs (based on 'FigureCanvasQTAgg'). """

    def __init__(self, drop_func=None): ####, num_plots=1, layout_type='vertical'):
        """ Initialises a 'QFigure' object. """
        super().__init__( mpl.figure.Figure() )
        # self.axes = self.figure.axes
        self.axes_now = None
        self.setAcceptDrops(True)
        self.drop_func = drop_func
        self._dummymodel = QStandardItemModel(self)
        return

    # def draw(self):
    #     """ Exposes 'draw' to class object. """
    #     self.canvas.draw()
    #     return


    def addAxes(self):
        """ Adds another axes to the figure. """
        _, self.axes_now = axxess(self.figure, newplot=True)
        self.draw()
        return


    def deleteAxes(self, idx=None):
        """ Deletes axes w/ 'idx' from the figure (default: last index). """
        if (len(self.figure.axes)):
            self.figure.axes[-1].remove()
            if (len(self.figure.axes)):
                self.figure.axes[-1].remove()
                self.axes_now = self.addAxes()
        else:
            self.axes_now = None
        self.draw()
        return
        # Note: The above "trick" to remove 2 axes, then add 1 again is used to properly exploit
        # the available size of the figure area!


    def dragEnterEvent(self, event):
        """ Checks if incoming MIME data can be used (or not). """
        mimeData = event.mimeData()
        if (('application/x-qabstractitemmodeldatalist' in mimeData.formats()) or
            ('text/plain' in mimeData.formats())):
            event.accept()
        else:
            event.ignore()
        return


    def dropEvent(self, event):
        """ Consumes incoming MIME data and performs acc. action. """
        mimeData = event.mimeData()
        str_data = drop_data2str(mimeData)

        #### FIXME: if desired (switch!!!) -> detect vertical position of drop
        ####        --> comm this normalized to drop_func as float? (0.78)
        ####            drop func will select "proper" axes

        if (self.drop_func):
            self.drop_func(str_data)
        else:
            self.testplot()
        return

    def testplot(self):
        """ check it out """
        print(">>>>>>>  INSIDE testplot() <<<<<<<<<<")
        fh = self.figure
        print(f"FIG = {fh}")
        # print("...but we'll make it a-new!! ;)")
        # fh, ax = axxess()
        # self.figure = fh # set it
        _, ax = axxess(fh, newplot=True)
        print(f"AXES = {ax}")
        ax.plot([1,2,-3,4,-5,6,7,-16])
        print(f"plotted sth!")

        self.draw()
        return



# class GuiCanvas():
#     """ Manage plots for PyQt GUIs (based on 'FigureCanvasQTAgg'). """

#     def __init__(self, num_plots=1, layout_type='vertical'):
#         """ Initialises a 'GuiCanvas' object.

#         Args:
#             num_plots (int, optional): Number of subplots / axes to start with. Defaults to 1.
#                 Note that additional subplots can be added dynamically later on.
#             layout_type (str, optional): Type of subplot layout. Defaults to 'vertical'.

#         Returns:
#             --
#         """

#         # attributes
#         self.layout_type = layout_type

#         # members
#         self.fig = mpl.figure.Figure()
#         if (self.layout_type == 'vertical'):
#             self.fig.subplots(num_plots,1)
#         else: # 'horizontal'
#             self.fig.subplots(1,num_plots)
#         self.axes = self.fig.get_axes()
#         self.canvas = FigureCanvasQTAgg( self.fig )

#         return

#     def add_plot(self):
#         """ Adds another axes object acc. to layout type. """
#         M, N = self.axes[-1].get_subplotspec().get_geometry()[0:2]
#         # TODO: check on layout type & change accordingly?
#         for sp, ax in enumerate(self.axes, start=1):
#             ax.change_geometry(M+1,1,sp)
#         self.fig.add_subplot(M+1, N, M+1)
#         self.axes = self.fig.get_axes()
#         return self.axes[-1]

#     def draw(self):
#         """ Exposes 'draw' to class object. """
#         self.canvas.draw()
#         return

#     def close(self):
#         """ Closes 'GuiCanvas' object. """
#         del self.fig
#         return


#-----------------------------------------------------------------------------------------------
# MODULE FUNCTIONS
#-----------------------------------------------------------------------------------------------

def drop_data2str(mimeData):
    """ Extracts text from MIME data as single string (i.e. concatenate list if necessary). """
    dummy = QStandardItemModel()
    if (mimeData.hasFormat('application/x-qabstractitemmodeldatalist')):
        dummy.setRowCount(0)
        dummy.dropMimeData(mimeData, Qt.CopyAction, 0, 0, QModelIndex())
        msg = []
        for idx in range(dummy.rowCount()):
            item = dummy.item(idx, 0)
            msg.append(item.text())
        if (len(msg) > 1):
            text_str = ', '.join(msg)
        else:
            text_str = msg[0]
    elif (mimeData.hasFormat('text/plain')):
        text_str = mimeData.text()
    return text_str


def copy_attributes(wg1, wg2):
    """ Copies attributes (e.g. size policies) of QWidget 'wg1' onto QWidget 'wg2'. """
    for item in (_ATTR_DATA + _ATTR_SIZE + _ATTR_BEHAVIOUR + _ATTR_VISUALS):
        setItem = f"set{item[0].upper()}{item[1:]}"
        if ((item in dir(wg1)) and (setItem in dir (wg2))):
            eval(f"wg2.{setItem}( wg1.{item}() )")
    return



################################################################################################
# EXPLANATION / Overview over Methods
################################################################################################
# dragLeaveEvent() --> define in "FROM" widget
# dragMoveEvent()  --> define for main widget / exec loop?
# dragEnterEvent() --> define in "TO" widget
# dropEvent()      --> define in "TO" widget / i.e. what to do actually? ;)
