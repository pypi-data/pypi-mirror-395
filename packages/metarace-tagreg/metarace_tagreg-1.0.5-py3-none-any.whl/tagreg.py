# SPDX-License-Identifier: MIT
"""tagreg

 Transponder reader and registration tool

"""
__version__ = '1.0.5'

import sys
import gi
import logging
import metarace
import os
import csv
from time import sleep
from metarace import tod
from metarace.jsonconfig import config
from metarace.riderdb import riderdb
from metarace.decoder.rrs import rrs
from metarace.decoder.rru import rru
from metarace.decoder.thbc import thbc

gi.require_version("GLib", "2.0")
from gi.repository import GLib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

PRGNAME = 'org._6_v.tagreg'
APPNAME = 'Tagreg'

_LOGLEVEL = logging.DEBUG
_log = logging.getLogger('tagreg')
_log.setLevel(_LOGLEVEL)

_DEFTYPE = 'rrs'
_DEFPORT = ''
_FAILTHRESH = 10
_CONFIGFILE = '.tagreg.json'


def addTextColumn(view,
                  label,
                  column,
                  expand=False,
                  calign=None,
                  width=None,
                  sort=None):
    """Create a tree view column and add to view"""
    r = Gtk.CellRendererText.new()
    r.set_property('editable', False)
    if calign is not None:
        r.set_property('xalign', calign)
    c = Gtk.TreeViewColumn(label, r, text=column)
    if width is not None:
        c.set_min_width(width)
    if sort is not None:
        c.set_sort_column_id(sort)
    c.set_expand(expand)
    view.append_column(c)
    return r


def addpage(nb, child, label):
    """Add a page to notebook with the text label provided"""
    l = Gtk.Label.new(label)
    l.set_single_line_mode(True)
    l.set_width_chars(12)
    l.show()
    child.show()
    nb.append_page(child, l)


def chooseCsvFile(title='',
                  mode=Gtk.FileChooserAction.OPEN,
                  parent=None,
                  path=None,
                  hintfile=None):
    """Open a native file chooser dialog to load/save a CSV file"""
    ret = None
    dialog = Gtk.FileChooserNative(title=title, modal=True)
    dialog.set_transient_for(parent)
    dialog.set_action(mode)
    filter = Gtk.FileFilter()
    filter.set_name('CSV Files')
    filter.add_mime_type('text/csv')
    filter.add_pattern('*.csv')
    dialog.add_filter(filter)
    filter = Gtk.FileFilter()
    filter.set_name('All Files')
    filter.add_pattern('*')
    dialog.add_filter(filter)
    if path is not None:
        dialog.set_current_folder(path)
    if hintfile:
        dialog.set_current_name(hintfile)
    response = dialog.run()
    if response == Gtk.ResponseType.ACCEPT:
        ret = dialog.get_filename()
    dialog.destroy()
    return ret


# Button indications
_button_images = {
    'idle': {
        'src': 'bg_idle.svg'
    },
    'activity': {
        'src': 'bg_armint.svg'
    },
    'ok': {
        'src': 'bg_armstart.svg'
    },
    'error': {
        'src': 'bg_armfin.svg'
    },
}


def _load_images(store):
    """Create image handles for the status button"""
    for b in store:
        img = store[b]
        with metarace.resource_file(img['src']) as fn:
            img['image'] = Gtk.Image.new_from_file(str(fn))


class statButton(Gtk.Button):

    def __init__(self):
        Gtk.Button.__init__(self)
        srcbuf = _button_images['idle']['image'].get_pixbuf()
        self.__curbg = 'idle'
        self.__image = Gtk.Image.new_from_pixbuf(srcbuf)
        self.__image.show()
        self.__label = Gtk.Label.new('--')
        self.__label.set_width_chars(12)
        self.__label.set_single_line_mode(True)
        self.__label.show()
        c = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        c.pack_start(self.__image, False, True, 0)
        c.pack_start(self.__label, True, True, 0)
        c.show()
        self.add(c)
        self.set_sensitive(False)
        self.set_can_focus(False)

    def update(self, bg=None, label=None):
        """Update button content"""
        if bg is not None and bg != self.__curbg and bg in _button_images:
            srcbuf = _button_images[bg]['image'].get_pixbuf()
            self.__image.set_from_pixbuf(srcbuf)
            self.__curbg = bg
        if label is not None:
            self.__label.set_text(label)


class textViewHandler(logging.Handler):
    """A class for displaying log messages in a GTK text view."""

    def __init__(self, log=None, view=None, scroll=None):
        self.log = log
        self.view = view
        self.scroll = scroll
        self.scroll_pending = False
        logging.Handler.__init__(self)

    def do_scroll(self):
        """Catch up end of scrolled window."""
        if self.scroll_pending:
            self.scroll.set_value(self.scroll.get_upper() -
                                  self.scroll.get_page_size())
            self.scroll_pending = False
        return False

    def append_log(self, msg):
        """Append msg to the text view."""
        atend = True
        if self.scroll and self.scroll.get_page_size() > 0:
            # Fudge a 'sticky' end of scroll mode... about a pagesz
            pagesz = self.scroll.get_page_size()
            if self.scroll.get_upper() - (self.scroll.get_value() + pagesz) > (
                    0.5 * pagesz):
                atend = False
        self.log.insert(self.log.get_end_iter(), msg.strip() + '\n')
        if atend:
            self.scroll_pending = True
            GLib.idle_add(self.do_scroll)
        return False

    def emit(self, record):
        """Emit log record to gtk main loop."""
        msg = self.format(record)
        GLib.idle_add(self.append_log, msg)


class logViewer(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)
        self.set_shadow_type(Gtk.ShadowType.IN)
        self._text = Gtk.TextView.new()
        self._text.set_left_margin(2)
        self._text.set_right_margin(2)
        self._text.set_cursor_visible(False)
        self._text.set_editable(False)
        self._text.set_monospace(True)
        self._text.show()
        self._buf = self._text.get_buffer()
        self.add(self._text)
        f = logging.Formatter('%(levelname)s: %(message)s')
        self._lh = textViewHandler(self._buf, self._text,
                                   self.get_vadjustment())
        self._lh.setFormatter(f)
        self._lh.setLevel(logging.INFO)
        logging.getLogger().addHandler(self._lh)


class registerBox(Gtk.Grid):

    def __init__(self, window, riderdb, tagmap):
        Gtk.Grid.__init__(self)
        self._window = window
        self._riderdb = riderdb
        self._tagmap = tagmap
        self.set_column_spacing(6)
        self.set_row_spacing(4)
        self.props.margin = 6
        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        row = 0
        for prompt in ('Number:', 'Series:', 'Transponder:', 'Auto Increment:',
                       'Follow Riders:', 'Rider List:'):
            l = Gtk.Label.new(prompt)
            l.set_halign(Gtk.Align.FILL)
            l.set_xalign(1.0)
            l.set_single_line_mode(True)
            l.show()
            self.attach(l, 0, row, 1, 1)
            row += 1
        self._numberEntry = Gtk.Entry.new()
        self._numberEntry.set_width_chars(4)
        self._numberEntry.set_tooltip_text('Rider number')
        self._numberEntry.show()
        self.attach(self._numberEntry, 1, 0, 1, 1)
        self._riderLabel = Gtk.Label.new('')
        self._riderLabel.set_single_line_mode(True)
        self._riderLabel.set_width_chars(24)
        self._riderLabel.set_halign(Gtk.Align.FILL)
        self._riderLabel.set_xalign(0.0)
        self._riderLabel.set_hexpand(True)
        self._riderLabel.show()
        self.attach(self._riderLabel, 2, 0, 2, 1)
        self._seriesEntry = Gtk.Entry.new()
        self._seriesEntry.set_width_chars(4)
        self._seriesEntry.set_tooltip_text('Optional rider number series')
        self._seriesEntry.show()
        self.attach(self._seriesEntry, 1, 1, 1, 1)
        self._refidEntry = Gtk.Entry.new()
        self._refidEntry.set_width_chars(8)
        self._refidEntry.set_tooltip_text('Transponder unique ID')
        self._refidEntry.show()
        self.attach(self._refidEntry, 1, 2, 2, 1)
        self._clearButton = Gtk.Button.new_with_label('Clear')
        self._clearButton.set_tooltip_text(
            'Clear transponder for this rider number')
        self._clearButton.show()
        self.attach(self._clearButton, 3, 2, 1, 1)
        self._incButton = Gtk.CheckButton.new_with_label('Yes')
        self._incButton.set_active(True)
        self._incButton.set_tooltip_text(
            'Automatically increment rider number after each scan')
        self._incButton.show()
        self.attach(self._incButton, 1, 3, 1, 1)
        self._followButton = Gtk.CheckButton.new_with_label('Yes')
        self._followButton.set_active(False)
        self._followButton.set_tooltip_text(
            'Choose next rider number in current series from riderlist')
        self._followButton.show()
        self.attach(self._followButton, 1, 4, 1, 1)
        self._resetButton = Gtk.Button.new_with_label('Reset')
        self._resetButton.set_tooltip_text(
            'Clear all riders and transponders from the current rider list')
        self._resetButton.show()
        self.attach(self._resetButton, 1, 5, 1, 1)
        self._importButton = Gtk.Button.new_with_label('Import')
        self._importButton.set_tooltip_text(
            'Import riders and transponders from CSV file')
        self._importButton.show()
        self.attach(self._importButton, 2, 5, 1, 1)
        self._exportButton = Gtk.Button.new_with_label('Export')
        self._exportButton.set_tooltip_text(
            'Export riders and transponders to CSV file')
        self._exportButton.show()
        self.attach(self._exportButton, 3, 5, 1, 1)

        # callbacks
        self._clearButton.connect('clicked', self._clearButton_clicked)
        self._resetButton.connect('clicked', self._resetButton_clicked)
        self._importButton.connect('clicked', self._importButton_clicked)
        self._exportButton.connect('clicked', self._exportButton_clicked)
        self._numberEntry.connect('changed', self._numberEntry_changed)
        self._numberEntry.connect('activate', self._numberEntry_activate)
        self._refidEntry.connect('activate', self._refidEntry_activate)
        self._seriesEntry.connect('changed', self._seriesEntry_changed)

    def _seriesEntry_changed(self, entry):
        """Update view if series is changed"""
        riderNo = self._numberEntry.get_text()
        if riderNo:
            self._numberEntry_changed(self._numberEntry)

    def _numberEntry_activate(self, entry):
        """Handle activate on rider number"""
        riderNo = self._numberEntry.get_text()
        series = self._seriesEntry.get_text()
        r = self._riderdb.get_rider(riderNo, series)
        if r is None:
            nr = self._riderdb.add_empty(riderNo, series)
            _log.debug('Added new rider entry: %r', nr)

    def _numberEntry_changed(self, entry):
        """Handle an update of the rider number"""
        riderNo = self._numberEntry.get_text()
        series = self._seriesEntry.get_text()
        r = self._riderdb.get_rider(riderNo, series)
        if r is not None:
            rv = []
            rname = r.fitname(16, True)
            if rname:
                rv.append(rname)
            if r['org'] and len(r['org']) < 5:
                rv.append('(' + r['org'] + ')')
            pcat = r.primary_cat()
            if pcat:
                rv.append(pcat)
            self._riderLabel.set_text(' '.join(rv))
            self._refidEntry.set_text(r['refid'])
        else:
            self._riderLabel.set_text('[new rider]')
            self._refidEntry.set_text('')

    def _refidEntry_activate(self, entry):
        """Update refid value"""
        riderNo = self._numberEntry.get_text()
        if riderNo:
            series = self._seriesEntry.get_text()
            refid = self._refidEntry.get_text()
            self._numberEntry_activate(self._numberEntry)
            r = self._riderdb.get_rider(riderNo, series)
            if r is not None:
                r['refid'] = refid
                _log.info('Assigned %s to rider %s', refid, riderNo)
                if self._incButton.get_active():
                    GLib.idle_add(self._incrementRider, self._refidEntry)
                else:
                    self._refidEntry.grab_focus()
            else:
                _log.warning('No rider to assign transponder')
        else:
            pass

    def timer(self, refid, riderid):
        """Handle a transponder read"""
        if refid:
            if riderid is not None:
                # transponder already assigned
                self._refidEntry.set_text(refid)
                self._numberEntry.set_text(riderid[0])
                self._seriesEntry.set_text(riderid[1])
            else:
                # transponder not yet assigned
                riderNo = self._numberEntry.get_text()
                if riderNo:
                    series = self._seriesEntry.get_text()
                    self._numberEntry_activate(self._numberEntry)
                    r = self._riderdb.get_rider(riderNo, series)
                    if r is not None:
                        if not r['refid']:
                            self._refidEntry.set_text(refid)
                            r['refid'] = refid
                            _log.info('Assigned %s to rider %s', refid,
                                      riderNo)
                            if self._incButton.get_active():
                                GLib.idle_add(self._incrementRider,
                                              self._numberEntry)
                            else:
                                self._numberEntry.grab_focus()
                        else:
                            _log.warning('Rider %s already assigned to %s',
                                         riderNo, r['refid'])
                else:
                    # nothing in rider number entry
                    self._refidEntry.set_text(refid)

    def _incrementRider(self, focusTo=None):
        """Update model to point to next rider number or entry"""
        riderNo = self._numberEntry.get_text()
        series = self._seriesEntry.get_text()
        if riderNo.isdigit():
            if self._followButton.get_active():
                nextRider = self._riderdb.next_rider(riderNo, series)
                if nextRider is not None:
                    self._numberEntry.set_text(nextRider[0])
                    self._numberEntry.activate()
                else:
                    _log.info('No more riders in current list')
            else:
                nextRider = int(riderNo) + 1
                self._numberEntry.set_text(str(nextRider))
                self._numberEntry.activate()
        if focusTo is not None:
            focusTo.grab_focus()
        return False

    def _clearButton_clicked(self, button):
        self._refidEntry.set_text('')
        self._refidEntry.activate()
        self._numberEntry.grab_focus()

    def _resetButton_clicked(self, button):
        self._riderdb.clear()
        self._numberEntry.set_text('')
        self._numberEntry.grab_focus()
        _log.info('Rider list cleared')

    def _importButton_clicked(self, button):
        csvfile = chooseCsvFile(title='Import Chipfile or Rider List',
                                parent=self._window,
                                path=os.getcwd())
        if csvfile is not None:
            try:
                self._riderdb.clear()
                self._riderdb.load(csvfile)
                riderCount = len(self._riderdb)
                if riderCount > 0:
                    _log.info('Loaded %d entries from %s', riderCount, csvfile)
                else:
                    _log.warning('No entries found in %s', csvfile)

            except Exception as e:
                _log.error('%s reading from csv %s: %s', e.__class__.__name__,
                           csvfile, e)
            self._numberEntry.grab_focus()

    def _exportButton_clicked(self, button):
        csvfile = chooseCsvFile(title='Export Chipfile or Rider List',
                                mode=Gtk.FileChooserAction.SAVE,
                                parent=self._window,
                                path=os.getcwd(),
                                hintfile='chipfile.csv')
        if csvfile is not None:
            try:
                count = self._riderdb.save_chipfile(csvfile)
                _log.info('Saved %d refids to %s', count, csvfile)

            except Exception as e:
                _log.error('%s writing chipfile csv %s: %s',
                           e.__class__.__name__, csvfile, e)
            self._numberEntry.grab_focus()


class tagreg(Gtk.Window):
    """Transponder reader and registration tool"""

    def __init__(self):
        _log.info('Tagreg - Init')
        Gtk.Window.__init__(self, title='Transponder Tool')

        # hardware
        self._decoder = None

        # runstate
        self._running = False
        self._failcount = 0
        self._riderdb = riderdb()
        self._tagmap = {}
        self._maptag = {}
        self._checkOut = {}
        self._checkIn = {}

        # content
        vb = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        vb.set_homogeneous(False)
        vb.show()
        self.add(vb)

        # decoder control bar
        db = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        db.set_homogeneous(False)
        db.show()
        self._decoderSelect = Gtk.ComboBoxText.new()
        self._decoderSelect.append('rrs', 'RR Decoder')
        self._decoderSelect.append('rru', 'RR USB Box')
        self._decoderSelect.append('thbc', 'Tag Heuer')
        self._decoderSelect.show()
        db.pack_start(self._decoderSelect, False, True, 2)
        self._decoderEntry = Gtk.Entry.new()
        self._decoderEntry.show()
        db.pack_start(self._decoderEntry, True, True, 2)
        self._decoderStat = statButton()
        self._decoderStat.show()
        db.pack_start(self._decoderStat, False, True, 2)
        vb.pack_start(db, False, True, 2)

        # mode select window
        self._modeBox = Gtk.Notebook.new()
        self._modeBox.set_size_request(-1, 300)
        # mode 1: register
        self._registerBox = registerBox(self, self._riderdb, self._tagmap)
        self._registerBox.show()
        addpage(self._modeBox, self._registerBox, 'Register')

        # mode 2: check out
        mb = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        mb.show()
        self._checkoutStore = Gtk.ListStore.new([str, str, str, str, str, str])
        self._checkoutView = Gtk.TreeView.new_with_model(self._checkoutStore)
        addTextColumn(self._checkoutView, 'Refid', 0, width=80, sort=0)
        addTextColumn(self._checkoutView, 'No.', 1, calign=1.0, sort=5)
        addTextColumn(self._checkoutView, 'Series', 2)
        addTextColumn(self._checkoutView, 'Name', 3, expand=True)
        addTextColumn(self._checkoutView, 'Cat', 4, width=60)
        self._checkoutView.show()
        cov = Gtk.ScrolledWindow.new()
        cov.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        cov.set_shadow_type(Gtk.ShadowType.IN)
        cov.add(self._checkoutView)
        cov.show()
        mb.pack_start(cov, True, True, 2)
        eb = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        eb.set_homogeneous(True)
        eb.show()
        self._coLabel = Gtk.Label.new('Total: 0')
        self._coLabel.show()
        eb.pack_start(self._coLabel, True, True, 2)
        self._coReset = Gtk.Button.new_with_label('Clear')
        self._coReset.set_tooltip_text('Clear all entries from check-out list')
        self._coReset.show()
        eb.pack_start(self._coReset, True, True, 2)
        self._coLoad = Gtk.Button.new_with_label('Load All')
        self._coLoad.set_tooltip_text(
            'Load all transponders from current rider list')
        self._coLoad.show()
        eb.pack_start(self._coLoad, True, True, 2)
        self._coExport = Gtk.Button.new_with_label('Export')
        self._coExport.set_tooltip_text('Save check-out list to CSV file')
        self._coExport.show()
        eb.pack_start(self._coExport, True, True, 2)
        mb.pack_start(eb, False, True, 2)
        addpage(self._modeBox, mb, 'Check-Out')

        # mode 3: check in
        mb = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        mb.show()
        self._checkinStore = Gtk.ListStore.new([str, str, str, str, str, str])
        self._checkinView = Gtk.TreeView.new_with_model(self._checkinStore)
        addTextColumn(self._checkinView, 'Refid', 0, width=80, sort=0)
        addTextColumn(self._checkinView, 'No.', 1, calign=1.0, sort=5)
        addTextColumn(self._checkinView, 'Series', 2)
        addTextColumn(self._checkinView, 'Name', 3, expand=True)
        addTextColumn(self._checkinView, 'Cat', 4, width=60)
        self._checkinView.show()
        cov = Gtk.ScrolledWindow.new()
        cov.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        cov.set_shadow_type(Gtk.ShadowType.IN)
        cov.add(self._checkinView)
        cov.show()
        mb.pack_start(cov, True, True, 2)
        eb = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        eb.set_homogeneous(True)
        eb.show()
        self._ciLabel = Gtk.Label.new('Total: 0')
        self._ciLabel.show()
        eb.pack_start(self._ciLabel, True, True, 2)
        self._ciCopy = Gtk.Button.new_with_label('Copy')
        self._ciCopy.set_tooltip_text('Copy from check-out to check-in')
        self._ciCopy.show()
        eb.pack_start(self._ciCopy, True, True, 2)
        self._ciClear = Gtk.Button.new_with_label('Clear All')
        self._ciClear.set_tooltip_text('Clear all entries from check-in list')
        self._ciClear.show()
        eb.pack_start(self._ciClear, True, True, 2)
        self._ciExport = Gtk.Button.new_with_label('Export')
        self._ciExport.set_tooltip_text('Save check-in list to CSV file')
        self._ciExport.show()
        eb.pack_start(self._ciExport, True, True, 2)
        mb.pack_start(eb, False, True, 2)
        addpage(self._modeBox, mb, 'Check-In')

        self._modeBox.show()
        vb.pack_start(self._modeBox, False, True, 2)

        # log window
        vs = logViewer()
        vs.set_size_request(-1, 180)
        vs.show()
        vb.pack_start(vs, True, True, 2)

        # callbacks
        self._riderdb.set_notify(self._rcb)
        self.connect('destroy', self._window_destroy)
        self._ciCopy.connect('clicked', self._ciCopy_clicked)
        self._ciClear.connect('clicked', self._ciClear_clicked)
        self._coReset.connect('clicked', self._coReset_clicked)
        self._coLoad.connect('clicked', self._coLoad_clicked)
        self._coExport.connect('clicked', self._coExport_clicked)
        self._ciExport.connect('clicked', self._ciExport_clicked)
        self._decoderSelect.connect('changed', self._decoderSelect_change)
        self._decoderEntry.connect('activate', self._decoderEntry_activate)
        self._decoderEntry.connect('changed', self._decoderEntry_change)

    def _ciClear_clicked(self, button):
        """Remove all entries from check-in"""
        self._checkinStore.clear()
        self._checkIn = {}
        self._checkinRider()

    def _ciCopy_clicked(self, button):
        """Copy entries from check-out to check-in"""
        self._checkinStore.clear()
        self._checkIn = {}
        for refid in self._checkOut:
            self._checkIn[refid] = self._checkOut[refid]
            self._checkinStore.append(self._checkOut[refid])
        self._checkinRider()

    def _coReset_clicked(self, button):
        """Clear all entries from checkout list"""
        self._checkoutStore.clear()
        self._checkOut = {}
        self._checkoutRider()

    def _coLoad_clicked(self, button):
        """Load all transponders into checkout"""
        self._checkoutStore.clear()
        self._checkOut = {}
        for refid in self._tagmap:
            self._checkoutRider(refid, self._tagmap[refid])

    def _coExport_clicked(self, button):
        """Write current check-out list to csv in order of view"""
        exportFile = chooseCsvFile(
            title='Save Check-Out Transponders to CSV File',
            mode=Gtk.FileChooserAction.SAVE,
            parent=self,
            path=os.getcwd(),
            hintfile='checkout.csv')
        if exportFile is not None:
            with metarace.savefile(exportFile) as f:
                cw = csv.writer(f)
                count = len(self._checkOut)
                _log.info('Saving %d entries from check-out to %s', count,
                          exportFile)
                cw.writerow(('refid', 'no', 'series', 'name', 'cat'))
                for r in self._checkoutStore:
                    cw.writerow(r[0:5])

    def _ciExport_clicked(self, button):
        """Write current check-in list to csv in order of view"""
        exportFile = chooseCsvFile(
            title='Save Check-In Transponders to CSV File',
            mode=Gtk.FileChooserAction.SAVE,
            parent=self,
            path=os.getcwd(),
            hintfile='checkin.csv')
        if exportFile is not None:
            with metarace.savefile(exportFile) as f:
                cw = csv.writer(f)
                count = len(self._checkinStore)
                _log.info('Saving %d entries from check-in to %s', count,
                          exportFile)
                cw.writerow(('refid', 'no', 'series', 'name', 'cat'))
                for r in self._checkinStore:
                    cw.writerow(r[0:5])

    def _decoderEntry_activate(self, entry):
        """Handle user update to decoder address"""
        GLib.idle_add(self._reconnect)

    def _decoderEntry_change(self, entry):
        GLib.idle_add(self._disconnect)

    def _decoderSelect_change(self, combo):
        """Handle change in decoderSelect"""
        GLib.idle_add(self._disconnect)
        self._decoderEntry.grab_focus()

    def _window_destroy(self, window):
        """Handle destroy signal."""
        self._running = False
        self.hide()
        self._saveconfig()
        # terminate decoder
        if self._decoder is not None:
            self._decoder.exit()
        Gtk.main_quit()

    def _rcb(self, rider):
        """Handle a change in the rider model"""
        if rider is not None:
            otag = None
            ntag = self._riderdb[rider]['refid'].lower()
            if rider in self._maptag:
                otag = self._maptag[rider]
                del (self._maptag[rider])
            if otag != ntag:
                if otag in self._tagmap:
                    del (self._tagmap[otag])
                if ntag:
                    self._maptag[rider] = ntag
                    self._tagmap[ntag] = rider
        else:
            # assume entire map has to be rebuilt
            self._tagmap = {}
            self._maptag = {}
            for r in self._riderdb:
                if r[1] != 'cat':
                    refid = self._riderdb[r]['refid'].lower()
                    if refid:
                        self._tagmap[refid] = r
                        self._maptag[r] = refid

    def _disconnect(self):
        """Disconnect current decoder and remove handler"""
        if self._decoder is not None:
            self._decoder.setcb()
            self._decoder.exit()
            self._decoder = None
        return False

    def _reconnect(self):
        """Try to reconnect with the current port specified"""
        _log.debug('_reconnect')
        newtype = self._decoderSelect.get_active_id()
        newport = self._decoderEntry.get_text()
        if not newport:
            newtype = None

        curtype = self._decoder.__class__.__name__
        if curtype != newtype:
            if self._decoder is not None:
                self._decoder.setcb()
                self._decoder.exit()
                self._decoder.join()
            self.decoder = None

            if newtype == 'rru':
                self._decoder = rru()
            elif newtype == 'rrs':
                self._decoder = rrs()
            elif newtype == 'thbc':
                self._decoder = thbc()
            else:
                self._decoder = None

            if self._decoder is not None:
                self._decoder.start()
                self._decoder.setcb(self._tcb)

        if newport and self._decoder is not None:
            self._decoder.setport(newport)
            self._decoder.clear()

        return False

    def _delCheckin(self, refid):
        """Scan list store and remove if found"""
        i = self._checkinStore.get_iter_first()
        while i is not None:
            if self._checkinStore.get_value(i, 0) == refid:
                break
            i = self._checkinStore.iter_next(i)
        if i is not None:
            self._checkinStore.remove(i)

    def _checkinRider(self, refid=None, riderid=None):
        """Remove this transponder from checkin"""
        if refid is not None:
            # riderid is ignored during check-in
            if refid in self._checkIn:
                if self._checkIn[refid] is not None:
                    self._delCheckin(refid)
                    self._checkIn[refid] = None
            else:
                _log.warning('Unallocated transponder: %s', refid)
        count = len(self._checkinStore)
        plural = 's'
        if count == 1:
            plural = ''
        self._ciLabel.set_text('Total: %d' % (count))

    def _checkoutRider(self, refid=None, riderid=None):
        """Add transponder or rider to checkout"""
        if refid is not None:
            riderno = ''
            series = ''
            name = ''
            cat = ''
            sort = 'ZZZZZZ.zzzz'
            if riderid is not None and riderid in self._riderdb:
                r = self._riderdb[riderid]
                riderno = r['no']
                series = r['series']
                sort = r.get_key()
                name = r.fitname(24, True)
                cat = r.primary_cat()
            if refid not in self._checkOut:
                # already in checkout list - ignore
                nr = [refid, riderno, series, name, cat, sort]
                self._checkOut[refid] = nr
                self._checkoutStore.append(nr)
        count = len(self._checkOut)
        plural = 's'
        if count == 1:
            plural = ''
        self._coLabel.set_text('Total: %d' % (count))

    def _timercb(self, event):
        """Handle timer message in mainloop"""
        refid = event.refid.lower()
        riderid = None
        if refid in self._tagmap:
            riderid = self._tagmap[refid]
        _log.info('Transponder: %s, Rider: %s', refid, riderid)
        curMode = self._modeBox.get_current_page()
        if curMode == 0:
            self._registerBox.timer(refid, riderid)
        elif curMode == 1:
            self._checkoutRider(refid, riderid)
        elif curMode == 2:
            self._checkinRider(refid, riderid)

    def _tcb(self, event):
        """Collect and process a timing event from attached decoder"""
        GLib.idle_add(self._timercb, event)
        return False

    def _timeout(self):
        """Check decoder state and update display status"""
        nt = tod.now()
        bg = 'idle'
        if self._decoder is not None:
            bg = 'ok'
            self._decoderStat.set_sensitive(True)
            if not self._decoder.connected():
                self._failcount += 1
                if self._failcount > _FAILTHRESH:
                    bg = 'activity'
                    self._reconnect()
                    self._failcount = 0
                else:
                    bg = 'error'
            else:
                self._failcount = 0
        else:
            self._decoderStat.set_sensitive(False)
            bg = 'idle'

        self._decoderStat.update(bg=bg, label=nt.meridiem())
        return True

    def run(self):
        _log.debug('run')
        self._loadconfig()
        self.show()
        GLib.idle_add(self._reconnect)
        GLib.timeout_add_seconds(1, self._timeout)

    def _loadconfig(self):
        """Check options and load state from current directory"""
        cr = config({
            'tagreg': {
                'decodertype': _DEFTYPE,
                'decoderport': _DEFPORT,
                'mode': 0,
                'checkout': {},
                'checkin': {}
            }
        })
        cr.add_section('tagreg')
        cr.merge(metarace.sysconf, 'tagreg')
        cr.load(_CONFIGFILE)

        self._decoderSelect.set_active_id(
            cr.get_str('tagreg', 'decodertype', _DEFTYPE))
        self._decoderEntry.set_text(
            cr.get_str('tagreg', 'decoderport', _DEFPORT))
        self._modeBox.set_current_page(cr.get_posint('tagreg', 'mode', 0))

        # load riders
        self._riderdb.load('riders.csv')
        riderCount = len(self._riderdb)
        if riderCount > 0:
            _log.info('Loaded %d entries from rider list', riderCount)

        # load check-out
        checkOut = cr.get('tagreg', 'checkout')
        if isinstance(checkOut, dict):
            for refid in checkOut:
                nr = checkOut[refid]
                if len(nr) == 6:
                    self._checkOut[refid] = checkOut[refid]
                    self._checkoutStore.append(checkOut[refid])
        self._checkoutRider()
        # check-in
        checkIn = cr.get('tagreg', 'checkin')
        if isinstance(checkIn, dict):
            for refid in checkIn:
                nr = checkIn[refid]
                if nr is not None and len(nr) == 6:
                    self._checkinStore.append(checkIn[refid])
                self._checkIn[refid] = checkIn[refid]
        self._checkinRider()

    def _saveconfig(self):
        """Save current setup to current directory"""
        self._riderdb.save('riders.csv')
        cw = config()
        cw.add_section('tagreg')
        cw.set('tagreg', 'decodertype', self._decoderSelect.get_active_id())
        cw.set('tagreg', 'decoderport', self._decoderEntry.get_text())
        cw.set('tagreg', 'mode', self._modeBox.get_current_page())
        cw.set('tagreg', 'checkout', self._checkOut)
        cw.set('tagreg', 'checkin', self._checkIn)
        with metarace.savefile(_CONFIGFILE) as f:
            cw.write(f)


def main():
    """Run the tagreg application"""
    chk = Gtk.init_check()
    if not chk[0]:
        print('Unable to init Gtk display')
        sys.exit(-1)

    ch = logging.StreamHandler()
    ch.setLevel(_LOGLEVEL)
    fh = logging.Formatter(metarace.LOGFORMAT)
    ch.setFormatter(fh)
    logging.getLogger().addHandler(ch)

    try:
        GLib.set_prgname(PRGNAME)
        GLib.set_application_name(APPNAME)
        Gtk.Window.set_default_icon_name(metarace.ICON)
    except Exception as e:
        _log.debug('%s setting property: %s', e.__class__.__name__, e)

    metarace.init()
    _load_images(_button_images)
    configpath = metarace.DATA_PATH
    if len(sys.argv) > 2:
        _log.error('Usage: tagreg [configdir]')
        sys.exit(1)
    elif len(sys.argv) == 2:
        configpath = sys.argv[1]
    configpath = metarace.config_path(configpath)
    if configpath is None:
        _log.error('Unable to open meet folder %r', sys.argv[1])
        sys.exit(1)
    lf = metarace.lockpath(configpath)
    if lf is None:
        _log.error('Unable to lock meet folder, already in use')
        sleep(2)
        sys.exit(1)
    _log.debug('Entering meet folder %r', configpath)
    os.chdir(configpath)
    app = tagreg()
    app.run()
    return Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
