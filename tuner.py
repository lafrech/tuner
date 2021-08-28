#!/usr/bin/env python

# ----------------------------------------------------------------------------
# tuner.py
# version 2.4
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jerome@jolimont.fr> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# Jérôme Lafréchoux
# ----------------------------------------------------------------------------

"""This module creates a keyboard emitting notes to tune a music instrument

Class Tuner creates a tuner : a keyboard and a few controls
"""

import os
import sys
from subprocess import Popen
from collections import deque
from signal import signal, SIGINT
import gettext

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject, Gdk  # noqa


class _Note:
    """Defines note names and frequencies

    notes is a table containing notes described by their frequence and their
    name in both french and english notation

    INDEX_FR_NAME, INDEX_EN_NAME and INDEX_FREQ are indexes to its columns
    """

    INDEX_FR_NAME, INDEX_EN_NAME, INDEX_FREQ = range(3)

    notes = [
        ["Do1", "C1", "32.7"],
        ["Do♯1", "C♯1", "34.65"],
        ["Ré1", "D1", "36.71"],
        ["Ré♯1", "D♯1", "38.89"],
        ["Mi1", "E1", "41.2"],
        ["Fa1", "F1", "43.65"],
        ["Fa♯1", "F♯1", "46.25"],
        ["Sol1", "G1", "49"],
        ["Sol♯1", "G♯1", "51.91"],
        ["La1", "A1", "55"],
        ["La♯1", "A♯1", "58.27"],
        ["Si1", "B1", "61.74"],
        ["Do2", "C2", "65.41"],
        ["Do♯2", "C♯2", "69.3"],
        ["Ré2", "D2", "73.42"],
        ["Ré♯2", "D♯2", "77.78"],
        ["Mi2", "E2", "82.41"],
        ["Fa2", "F2", "87.31"],
        ["Fa♯2", "F♯2", "92.5"],
        ["Sol2", "G2", "98"],
        ["Sol♯2", "G♯2", "103.83"],
        ["La2", "A2", "110"],
        ["La♯2", "A♯2", "116.54"],
        ["Si2", "B2", "123.47"],
        ["Do3", "C3", "130.81"],
        ["Do♯3", "C♯3", "138.59"],
        ["Ré3", "D3", "146.83"],
        ["Ré♯3", "D♯3", "155.56"],
        ["Mi3", "E3", "164.81"],
        ["Fa3", "F3", "174.61"],
        ["Fa♯3", "F♯3", "185"],
        ["Sol3", "G3", "196"],
        ["Sol♯3", "G♯3", "207.65"],
        ["La3", "A3", "220"],
        ["La♯3", "A♯3", "233.08"],
        ["Si3", "B3", "246.94"],
        ["Do4", "C4", "261.63"],
        ["Do♯4", "C♯4", "277.18"],
        ["Ré4", "D4", "293.66"],
        ["Ré♯4", "D♯4", "311.13"],
        ["Mi4", "E4", "329.63"],
        ["Fa4", "F4", "349.23"],
        ["Fa♯4", "F♯4", "369.99"],
        ["Sol4", "G4", "392"],
        ["Sol♯4", "G♯4", "415.3"],
        ["La4", "A4", "440"],
        ["La♯4", "A♯4", "466.16"],
        ["Si4", "B4", "493.88"],
        ["Do5", "C5", "523.25"],
        ["Do♯5", "C♯5", "554.37"],
        ["Ré5", "D5", "587.33"],
        ["Ré♯5", "D♯5", "622.25"],
        ["Mi5", "E5", "659.26"],
        ["Fa5", "F5", "698.46"],
        ["Fa♯5", "F5♯", "739.99"],
        ["Sol5", "G5", "783.99"],
        ["Sol♯5", "G5♯", "830.61"],
        ["La5", "A5", "880"],
        ["La♯5", "A♯5", "932.33"],
        ["Si5", "B5", "987.77"],
        ["Do6", "C6", "1046.5"],
        ["Do♯6", "C♯6", "1108.73"],
        ["Ré6", "D6", "1174.66"],
        ["Ré♯6", "D♯6", "1244.51"],
        ["Mi6", "E6", "1318.51"],
        ["Fa6", "F6", "1396.91"],
        ["Fa♯6", "F♯6", "1479.98"],
        ["Sol6", "G6", "1567.98"],
        ["Sol♯6", "G♯6", "1661.22"],
        ["La6", "A6", "1760"],
        ["La♯6", "A♯6", "1864.66"],
        ["Si6", "B6", "1975.53"],
        ["Do7", "C7", "2093"],
        ["Do♯7", "C♯7", "2217.46"],
        ["Ré7", "D7", "2349.32"],
        ["Ré♯7", "D♯7", "2489.02"],
        ["Mi7", "E7", "2637.02"],
        ["Fa7", "F7", "2793.83"],
        ["Fa♯7", "F♯7", "2959.96"],
        ["Sol7", "G7", "3135.96"],
        ["Sol♯7", "G♯7", "3322.44"],
        ["La7", "A7", "3520"],
        ["La♯7", "A♯7", "3729.31"],
        ["Si7", "B7", "3951.07"],
        ["Do8", "C8", "4186.01"],
    ]

    def __init__(self):
        pass


class _NoteSelectionDialog(Gtk.Dialog):
    """Custom frequency selector widget

    Allows the selection of a frequency from the notes table of class _Note
    Public method : get_index()
    """

    def __init__(self, title, index, notestyle_index):
        """Create and display a frequency selector.

        title is the window title to display,
        index is the index of the frequency to select as default,
        notestyle_index is the language column index in _Note.notes table.
        """
        # Set current index
        self._index = index

        # The selector is oriented high tones up / low tones down.
        # Translate the index to be selected.
        select = len(_Note.notes) - 1 - index

        # Notes
        store = Gtk.ListStore(str, str, str)
        for freq in _Note.notes:
            store.prepend(freq)

        # Window
        GObject.GObject.__init__(self)
        self.set_modal(True)
        self.set_title(title)
        self.set_size_request(150, 600)
        self.set_border_width(10)
        self.connect("key-press-event", self._key_pressed)
        # Position window under mouse cursor
        # TODO : replace with something better :
        # if keyboard used, the mouse could be anywhere
        self.set_position(Gtk.WindowPosition.MOUSE)

        # Treeview
        self._tree = Gtk.TreeView(store)
        self._tree.connect("button-press-event", self._double_click)
        # Select current freq
        self._tree.set_cursor(Gtk.TreePath(select), None, False)
        # Scroll to current freq
        self._tree.scroll_to_cell(select, use_align=True, row_align=0.5)

        # Name
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Note"))
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", notestyle_index)
        self._tree.append_column(column)

        # Freq
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Frequency"), renderer, text=2)
        self._tree.append_column(column)

        # Scroller
        scroll = Gtk.ScrolledWindow()
        scroll.add(self._tree)
        self.vbox.pack_start(scroll, True, True, 0)

        # Show all
        self._tree.show()
        scroll.show()
        self.show()

    def _key_pressed(self, widget, event):
        """Process keypress event."""
        # Get key name
        key = Gdk.keyval_name(event.keyval)

        if "Escape" == key:
            self.emit("response", Gtk.ResponseType.CANCEL)
        elif "Return" == key:
            self._note_selected()
        elif "Page_Up" == key:
            # Move one octave up
            # TODO : There should be a better way to do that.
            # Either with get/set cursor, or, even better, by setting
            # a Page_Up step
            model, treeiter = self._tree.get_selection().get_selected()
            index = model.get_path(treeiter).get_indices()[0] - 12
            if index < 0:
                index = 0
            self._tree.set_cursor(Gtk.TreePath(index), None, False)
            self._tree.scroll_to_cell(index, use_align=True, row_align=0.5)
            return True
        elif "Page_Down" == key:
            # Move one octave down
            model, treeiter = self._tree.get_selection().get_selected()
            index = model.get_path(treeiter).get_indices()[0] + 12
            if index > len(_Note.notes) - 1:
                index = len(_Note.notes) - 1
            self._tree.set_cursor(Gtk.TreePath(index), None, False)
            self._tree.scroll_to_cell(index, use_align=True, row_align=0.5)
            return True

    def _double_click(self, widget, event):
        """Process double-click event."""
        if event.button == 1 and event.type == Gdk.EventType._2BUTTON_PRESS:
            self._note_selected()

    def _note_selected(self):
        """Get row index of selection and emit response signal."""
        # Get selection
        select = self._tree.get_selection()
        model, treeiter = select.get_selected()
        if treeiter is not None:
            # Get index
            self._index = (
                len(_Note.notes)
                - 1
                - model.get_path(treeiter).get_indices()[0]
            )
            # Emit response signal
            self.emit("response", Gtk.ResponseType.OK)

    def get_index(self):
        """Return index of selected frequency's row in _Note.notes table."""
        return self._index


class _Key(Gtk.Box):
    """A key that can be laid out on a keyboard

    Each key consists of a button to play a sound, a button to select the
    frequency, and two buttons to tune up or down with a half tone step

    Public methods : adjust_freq(), get_freq(), get_index(), set_notestyle(),
    set_key_enabled()
    """

    __gsignals__ = {
        "play": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (str,)),
        "frequency-changed": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, index, notestyle, tuner):
        """Create a _Key

        index is the index of the note in _Note.notes,
        tuner is the Tuner keyboard in which the _Key is laid out.
        """
        self._index = index
        self._tuner = tuner
        self._notestyle = notestyle

        # Vertical box
        ##############
        GObject.GObject.__init__(
            self, spacing=5, orientation=Gtk.Orientation.VERTICAL)

        # Add play button
        self._play_button = Gtk.Button(stock=Gtk.STOCK_MEDIA_PLAY)
        # Hack to remove label from stock button
        # http://faq.pygtk.org/index.py?req=show&file=faq09.005.htp
        # TODO : Register new stock. Couldn't get that to work, yet.
        self._play_button.get_children()[0].get_children()[0].get_children()[
            1
        ].set_text("")
        self.pack_start(self._play_button, True, True, 0)
        self._play_button.show()

        # Add pick freq button
        self._pick_button = Gtk.Button()
        self.pack_start(self._pick_button, True, True, 0)
        self._pick_button.show()

        # Frequency label
        self._freq_label = Gtk.Label()
        self._freq_label.set_width_chars(10)
        self.pack_start(self._freq_label, False, False, 0)
        self._freq_label.show()

        # Add octave up arrow
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="8")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_oct_up = Gtk.Button()
        self._button_oct_up.add(hbox_arrow)
        self.pack_start(self._button_oct_up, False, True, 0)
        hbox_arrow.show()
        self._button_oct_up.show()

        # Add up arrow
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266F")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_up = Gtk.Button()
        self._button_up.add(hbox_arrow)
        self.pack_start(self._button_up, False, True, 0)
        hbox_arrow.show()
        self._button_up.show()

        # Add down arrow
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266D")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_down = Gtk.Button()
        self._button_down.add(hbox_arrow)
        self.pack_start(self._button_down, False, True, 0)
        hbox_arrow.show()
        self._button_down.show()

        # Add octave down arrow
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="8")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_oct_down = Gtk.Button()
        self._button_oct_down.add(hbox_arrow)
        self.pack_start(self._button_oct_down, False, True, 0)
        hbox_arrow.show()
        self._button_oct_down.show()

        # Connect handlers
        ##################
        self._play_button.connect("clicked", self._play)
        self._button_up.connect("clicked", self.adjust_freq, 1)
        self._button_down.connect("clicked", self.adjust_freq, -1)
        self._button_oct_up.connect("clicked", self.adjust_freq, 12)
        self._button_oct_down.connect("clicked", self.adjust_freq, -12)
        self._pick_button.connect("clicked", self._select_note)

        # Show all
        ##########
        self._set_label()
        self.show()

    def adjust_freq(self, widget=None, shift=0):
        """Adjust frequency by shifting frequency index.

        shift is a signed number of semitones to shift from.

        If highest or lowest freq reached, stop there silently.
        """
        if shift == 0:
            return

        index_max = len(_Note.notes) - 1

        while shift > 0 and self._index < index_max:
            # Increment index
            self._index = self._index + 1
            shift -= 1
            # If last index, disable increment button
            if self._index == index_max:
                self._button_up.set_sensitive(False)
                self._button_oct_up.set_sensitive(False)
            # Enable decrement button
            self._button_down.set_sensitive(True)
            self._button_oct_down.set_sensitive(True)

        while shift < 0 and self._index > 0:
            # Decrement index
            self._index = self._index - 1
            shift += 1
            # If first index, disable decrement button
            if self._index == 0:
                self._button_down.set_sensitive(False)
                self._button_oct_down.set_sensitive(False)
            # Enable increment button
            self._button_up.set_sensitive(True)
            self._button_oct_up.set_sensitive(True)

        # Refresh label
        self._set_label()

        # Tell Tuner a key was modified
        self.emit("frequency-changed")

    def _select_note(self, *args):
        """Select a note using the note selector widget."""

        # Create note selection dialog
        note_selector = _NoteSelectionDialog(
            _("Select note"), self._index, self._notestyle
        )
        # If new freq selected
        if note_selector.run() == Gtk.ResponseType.OK:
            # Get freq index from dialog
            self._index = note_selector.get_index()
            # Set label
            self._set_label()
            # Set buttons sensitivity accordingly
            if self._index == 0:
                self._button_up.set_sensitive(True)
                self._button_oct_up.set_sensitive(True)
                self._button_down.set_sensitive(False)
                self._button_oct_down.set_sensitive(False)
            elif self._index == (len(_Note.notes) - 1):
                self._button_up.set_sensitive(False)
                self._button_oct_up.set_sensitive(False)
                self._button_down.set_sensitive(True)
                self._button_oct_down.set_sensitive(True)
            else:
                self._button_up.set_sensitive(True)
                self._button_oct_up.set_sensitive(True)
                self._button_down.set_sensitive(True)
                self._button_oct_down.set_sensitive(True)
            self.emit("frequency-changed")

        # Destroy dialog
        note_selector.destroy()

    def get_freq(self):
        """Return current frequency value."""
        return _Note.notes[self._index][_Note.INDEX_FREQ]

    def get_index(self):
        """Return current frequency index."""
        return self._index

    def set_notestyle(self, notestyle):
        """Set _notesyle and refresh labels."""

        if notestyle is not None:
            self._notestyle = notestyle

        self._set_label()

    def _set_label(self):
        """Refresh note name and frequency value labels."""

        # Set button label
        self._pick_button.set_label(_Note.notes[self._index][self._notestyle])

        # Set freq label
        self._freq_label.set_text(_Note.notes[self._index][2] + " Hz")

    def set_key_enabled(self, enable):
        """Enable or disable play button.

        enable is a boolean. True means enable.
        """
        self._play_button.set_sensitive(enable)

    def _play(self, *args):
        """Order Tuner to play the note at self._index in _Note.notes."""

        self.emit("play", _Note.notes[self._index][_Note.INDEX_FREQ])


class Tuner:
    """Keyboard emitting notes to tune a music intrument such as a guitar.

    The layout of the keyboard can be modified : keys added or removed,
    key step tuning, global step tuning. French and english notestyle are
    supported. The length of each note is adjustable.

    Two backends are currently supported : beep and sox. The first uses the
    internal speaker, the latter the soundcard output.

    The key's notes are picked in _Note.notes table.
    """

    # Define backends
    _BEEP, _SOX_SINE, _SOX_PLUCK = range(3)

    def __init__(self, keys=None):
        """Initialize and display a keyboard

        keys is an optional array of frequency indexes
        """
        # I18n
        ######
        # Using local path
        local_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/locale"
        gettext.install("tuner", local_path)

        # Create empty if no key specified
        self._default_keys = keys or []

        # Variables
        ###########

        # Buttons and handlers
        self._buttons = []

        # Beep process
        self._beep_process = 0

        # Beep queue
        self._beep_queue = deque([])

        # Note playing token
        self._note_playing = False

        # Keys modified flag
        self._keys_modified_flag = False

        # Settings
        self._beep_length = 1
        self._notestyle = _Note.INDEX_FR_NAME
        self._backend = self._SOX_PLUCK

        # Create window
        ###############
        self._window = Gtk.Window()
        self._window.connect("destroy", self._close_request)
        signal(SIGINT, self._close_request)
        self._window.set_title(_("Tuner"))
        self._window.set_border_width(10)

        # Create vertical box and horizontal sub-boxes
        vbox = Gtk.Box(
            homogeneous=False, spacing=10, orientation=Gtk.Orientation.VERTICAL
        )
        hbox_controls = Gtk.ButtonBox()
        self._hbox_keys = Gtk.Box(homogeneous=True)
        hbox_settings = Gtk.Box(homogeneous=False, spacing=10)

        # Control horizontal box
        ########################

        hbox_controls.set_layout(Gtk.ButtonBoxStyle.START)

        # Reset keys modifications
        self._reset_button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        self._reset_button.set_sensitive(False)
        hbox_controls.add(self._reset_button)
        self._reset_button.connect("clicked", self._reset_keys)
        self._reset_button.show()

        # Remove key
        self._button_rem = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        hbox_controls.add(self._button_rem)
        self._button_rem.connect("clicked", self._rem_key)
        self._button_rem.show()

        # Add key
        self._button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        hbox_controls.add(self._button_add)
        self._button_add.connect("clicked", self._add_key)
        self._button_add.show()

        # Stop playback
        self._stop_playback_button = Gtk.Button(stock=Gtk.STOCK_MEDIA_STOP)
        self._stop_playback_button.set_sensitive(False)
        hbox_controls.add(self._stop_playback_button)
        hbox_controls.set_child_secondary(self._stop_playback_button, True)
        self._stop_playback_button.connect(
            "clicked", self._stop_playback_request)
        self._stop_playback_button.show()

        # Play all keys
        self._play_all_button = Gtk.Button(stock=Gtk.STOCK_MEDIA_PLAY)
        hbox_controls.add(self._play_all_button)
        hbox_controls.set_child_secondary(self._play_all_button, True)
        self._play_all_button.connect("clicked", self._play_all)
        self._play_all_button.show()

        # Keys horizontal box
        #####################

        # Add global incrementor / decrementor buttons
        vbox_inc_dec = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Octave decrement
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="8")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_oct_down = Gtk.Button()
        self._button_oct_down.add(hbox_arrow)
        vbox_inc_dec.pack_end(self._button_oct_down, False, True, 0)
        hbox_arrow.show()
        self._button_oct_down.show()

        # Semitone decrement
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266D")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_down = Gtk.Button()
        self._button_down.add(hbox_arrow)
        vbox_inc_dec.pack_end(self._button_down, False, True, 0)
        hbox_arrow.show()
        self._button_down.show()

        # Semitone increment
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266F")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_up = Gtk.Button()
        self._button_up.add(hbox_arrow)
        vbox_inc_dec.pack_end(self._button_up, False, True, 0)
        hbox_arrow.show()
        self._button_up.show()

        # Octave increment
        hbox_arrow = Gtk.Box()
        arrow = Gtk.Arrow(
            arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        hbox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="8")
        hbox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_oct_up = Gtk.Button()
        self._button_oct_up.add(hbox_arrow)
        vbox_inc_dec.pack_end(self._button_oct_up, False, True, 0)
        hbox_arrow.show()
        self._button_oct_up.show()

        vbox_inc_dec.show()
        self._hbox_keys.pack_start(vbox_inc_dec, True, True, 0)

        self._button_up.connect("clicked", self._adjust_freq, 1)
        self._button_down.connect("clicked", self._adjust_freq, -1)
        self._button_oct_up.connect("clicked", self._adjust_freq, 12)
        self._button_oct_down.connect("clicked", self._adjust_freq, -12)

        # Set default keys
        self._reset_keys()

        # Settings horizontal box
        #########################

        # Note style selector
        vbox_notestyle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label(label=_("Notestyle"))
        label.set_alignment(0, 1)
        vbox_notestyle.pack_start(label, False, True, 0)
        label.show()
        button = Gtk.RadioButton.new_with_label_from_widget(None, _("French"))
        button.connect("clicked", self._set_notestyle, _Note.INDEX_FR_NAME)
        vbox_notestyle.pack_start(button, False, True, 0)
        button.show()
        button = Gtk.RadioButton.new_with_label_from_widget(
            button, _("English"))
        button.connect("clicked", self._set_notestyle, _Note.INDEX_EN_NAME)
        vbox_notestyle.pack_start(button, False, True, 0)
        button.show()
        hbox_settings.pack_start(vbox_notestyle, False, True, 0)
        vbox_notestyle.show()

        # Separator
        separator = Gtk.VSeparator()
        hbox_settings.pack_start(separator, False, True, 0)
        separator.show()

        # Beep length
        vbox_beep_length = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label(label=_("Length (s)"))
        label.set_alignment(0, 1)
        vbox_beep_length.pack_start(label, False, True, 0)
        label.show()
        beep_length_adj = Gtk.Adjustment(
            value=self._beep_length,
            lower=1,
            upper=10,
            step_increment=1,
            page_increment=1,
            page_size=0,
        )
        beep_length_spin = Gtk.SpinButton(
            adjustment=beep_length_adj, climb_rate=0, digits=1
        )
        beep_length_adj.connect(
            "value_changed", self._set_beep_length, beep_length_spin
        )
        vbox_beep_length.pack_start(beep_length_spin, False, True, 0)
        beep_length_spin.show()
        hbox_settings.pack_start(vbox_beep_length, False, True, 0)
        vbox_beep_length.show()

        # Separator
        separator = Gtk.VSeparator()
        hbox_settings.pack_start(separator, False, True, 0)
        separator.show()

        # Backend selector
        vbox_backend = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label(label=_("Output"))
        label.set_alignment(0, 1)
        vbox_backend.pack_start(label, False, True, 0)
        label.show()
        button = Gtk.RadioButton.new_with_label_from_widget(
            None, "Sox (pluck)")
        button.connect("clicked", self._set_backend, self._SOX_PLUCK)
        vbox_backend.pack_start(button, False, True, 0)
        button.show()
        button = Gtk.RadioButton.new_with_label_from_widget(
            button, "Sox (sine)")
        button.connect("clicked", self._set_backend, self._SOX_SINE)
        vbox_backend.pack_start(button, False, True, 0)
        button.show()
        button = Gtk.RadioButton.new_with_label_from_widget(button, "Beep")
        button.connect("clicked", self._set_backend, self._BEEP)
        vbox_backend.pack_start(button, False, True, 0)
        button.show()
        hbox_settings.pack_start(vbox_backend, False, True, 0)
        vbox_backend.show()

        # Show everything
        #################
        vbox.pack_start(hbox_controls, True, True, 0)
        vbox.pack_start(self._hbox_keys, True, True, 0)
        vbox.pack_start(hbox_settings, True, True, 0)
        hbox_controls.show()
        self._hbox_keys.show()
        hbox_settings.show()
        vbox.show()
        self._window.add(vbox)
        self._window.show()

        # Poll note queue
        GObject.idle_add(self._play_note_from_queue)

    def _play_note(self, freq):
        """Play a note.

        freq is the frequency of the note to be played.
        """
        # Disable buttons while playing
        self._set_buttons_enabled(False)

        # Call external program (backend) to play the note
        try:
            if self._backend == self._BEEP:
                self._beep_process = Popen(
                    [
                        "beep",
                        "-f %s" % freq,
                        "-l %s" % (1000 * self._beep_length)
                    ]
                )
            elif self._backend == self._SOX_SINE:
                self._beep_process = Popen(
                    [
                        "play",
                        "-n",
                        "synth",
                        "1",
                        "sine",
                        "%s" % freq,
                        "repeat",
                        "%s" % (self._beep_length - 1),
                    ]
                )
            elif self._backend == self._SOX_PLUCK:
                self._beep_process = Popen(
                    [
                        "play",
                        "-n",
                        "synth",
                        "1",
                        "pluck",
                        "%s" % freq,
                        "repeat",
                        "%s" % (self._beep_length - 1),
                    ]
                )
        except OSError:
            self._missing_package_error(self._backend)
            self._set_buttons_enabled(True)

        # Set polling in idle to re-enable buttons when done
        else:
            self._note_playing = True
            GObject.idle_add(self._poll_beep_in_progress)

    def _stop_playback_request(self, *args):
        """Ask for playback stop in main loop to avoid race conditions."""
        GObject.idle_add(self._stop_playback)

    def _stop_playback(self):
        """Clear queue and interrupt playback. Called from main loop."""
        # Clear queue
        self._beep_queue.clear()
        # If process still alive (or zombie)
        if self._note_playing:
            # Terminate process (send SIGTERM signal)
            try:
                self._beep_process.terminate()
            except OSError:
                print(_("Could not terminate process."))

    def _missing_package_error(self, package):
        """Display dialog if a backend package is missing.

        package is an enum standing for the incriminated backend.
        """
        # Stop playback
        self._stop_playback_request()

        # Error message
        if package == self._BEEP:
            error_message = _("Oops! It seems beep is not installed.")
            error_message += "\n(http://johnath.com/beep/)\n"
        elif (package == self._SOX_SINE) or (package == self._SOX_PLUCK):
            error_message = _("Oops! It seems sox is not installed.")
            error_message += "\n(http://sox.sourceforge.net/)\n"
        error_message += _(
            "A package should be available for your distribution.")

        # CLI
        print(error_message)

        # GUI
        dialog = Gtk.Dialog(
            title=_("Missing program"),
            parent=None,
            flags=Gtk.DialogFlags.MODAL,
            buttons=(Gtk.STOCK_DIALOG_ERROR, Gtk.ResponseType.CLOSE),
        )
        label = Gtk.Label(label=error_message)
        dialog.vbox.pack_start(label, True, True, 0)
        label.show()
        response = dialog.run()
        if (
            Gtk.ResponseType.CLOSE == response
            or Gtk.ResponseType.DELETE_EVENT == response
        ):
            dialog.destroy()

    def _add_note_to_queue(self, widget, freq):
        """Add frequency to playback queue array.

        freq is the frequency of the note to add to the queue.
        """
        self._beep_queue.append(freq)

    def _play_note_from_queue(self):
        """Play first note from the queue

        This function is called from main loop.
        """
        # If no playback ongoing
        if not self._note_playing:
            # If queue not empty
            if self._beep_queue:
                # Play note from queue
                self._play_note(self._beep_queue.popleft())
        return True

    def _play_all(self, *args):
        """Add all notes on keyboard to queue."""
        for key in self._buttons:
            self._add_note_to_queue(None, key.get_freq())

    def _add_key(self, widget, index=None, reset=False):
        """Add a key on the rightmost part of the keyboard.

        If no freq specified, use same as rightmost key. If keyboard empty,
        start with default 110 Hz.

        index is the index of the freq the key should be created with.
        reset is set if the function is called by the reset() function, in
        which case the "keys modified" flag should not be set, to keep the
        reset button disabled.
        """
        if index is None:
            if len(self._buttons):
                index = self._buttons[-1].get_index()
            else:
                index = 21  # This is the index of 110 Hz in _Note.notes

        # Create new key
        key = _Key(index, self._notestyle, self)
        self._hbox_keys.pack_start(key, True, True, 0)
        self._buttons.append(key)
        key.connect("play", self._add_note_to_queue)
        key.connect("frequency-changed", self._keys_modified)

        # Refresh buttons and flags states
        self._button_rem.set_sensitive(True)
        if not reset:
            self._keys_modified()

    def _rem_key(self, widget=None, reset=False):
        """Remove rightmost key from the keyboard.

        reset is set if the function is called by the reset() function, in
        which case the "keys modified" flag should not be set, to keep the
        reset button disabled.
        """
        # Destroy key
        if len(self._buttons):
            self._buttons.pop().destroy()
        # If no key left, disable remove button
        if not len(self._buttons):
            self._button_rem.set_sensitive(False)
        # Refresh button and flags state
        if not reset:
            self._keys_modified()

    def _set_notestyle(self, widget, notestyle):
        """Set notestyle variable.

        notestyle is an enum standing for the notestyle's index in _Note.notes.
        """
        self._notestyle = notestyle
        for key in self._buttons:
            key.set_notestyle(notestyle)

    def _set_backend(self, widget, backend):
        """Set backend to use for playback.

        backend is an enum standing for the backend to use.
        """
        self._backend = backend

    def _set_beep_length(self, widget, beep_length_spin):
        """Set the length of the playback for each note.

        beep_length_spin is the spin button containing the length value,
        expressed in seconds.
        """
        self._beep_length = beep_length_spin.get_value()

    def _adjust_freq(self, widget=None, shift=0):
        """Adjust frequency of all keys.

        shift is a signed number of semitones to shift from.
        """
        for key in self._buttons:
            key.adjust_freq(shift=shift)
        self._keys_modified()

    def _set_buttons_enabled(self, enable):
        """Enable or disable buttons

        This function is called to disable play buttons and enable the stop
        button during playback.
        """
        # Enable / disable all keys on keyboard
        for key in self._buttons:
            key.set_key_enabled(enable)

        # Enable / disable play all button
        self._play_all_button.set_sensitive(enable)

        # Disable / enable stop playback button
        self._stop_playback_button.set_sensitive(not enable)

        # Enable / disable reset button if keys were modified
        if self._keys_modified_flag:
            self._reset_button.set_sensitive(enable)

    def _reset_keys(self, *args):
        """Reset keyboard to default configuration."""

        # Remove all keys
        for i in range(len(self._buttons)):
            self._rem_key(reset=True)

        # Set default keys
        for i in range(len(self._default_keys)):
            self._add_key(None, self._default_keys[i], reset=True)

        # Disable keys modified flag
        self._keys_modified_flag = False

        # Disable reset button
        self._reset_button.set_sensitive(False)

    def _keys_modified(self, *args):
        """Set _keys_modified_flag and enable reset button."""

        # When the keyboard is modified, set the flag...
        self._keys_modified_flag = True

        # ... and set reset button sensitive
        self._reset_button.set_sensitive(True)

    def _poll_beep_in_progress(self):
        """Unset _note_playing flag when playback is over.

        This function is called from main loop.
        """
        # Process still running -> return true to keep polling
        if self._beep_process.poll() is None:
            return True
        # If no more note in queue, enable buttons. Otherwise, don't.
        # (this avoids glitches when enabling/disabling instantly)
        if not self._beep_queue:
            self._set_buttons_enabled(True)
        self._note_playing = False
        return False

    def _close_request(self, *args):
        """Ask for application close in main loop to avoid race conditions."""
        GObject.idle_add(self._close)

    def _close(self):
        """Interrupt playback before closing application.

        This function is called from main loop.
        """
        # self._beep_process is not 0 : a subprocess was launched at some point
        if self._beep_process != 0:
            self._stop_playback()

        # Close application
        Gtk.main_quit()


if __name__ == "__main__":

    # Create Tuner with default guitar tuning (E, A, D, G, B, e).
    Tuner([16, 21, 26, 31, 35, 40])
    Gtk.main()
