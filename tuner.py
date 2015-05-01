#!/usr/bin/env python
# -*- coding: UTF8 -*-

# tuner.py
# version 1.4

# ToDo
# reset keys
# menu deroulant choix freq
# kill beep si close
# alsaaudio
# play all
# i18n
# separer en modules

from gi.repository import Gtk, GObject
from subprocess import Popen

#########################################################################
# class Key 
#########################################################################
class Key(Gtk.VBox):

    keys = [["Do", "C", "32.7"], ["Do♯","C♯", "34.65"], ["Ré", "D", "36.71"],
            ["Ré♯","D♯", "38.89"], ["Mi", "E", "41.2"], ["Fa", "F", "43.65"],
            ["Fa♯","F♯", "46.25"], ["Sol", "G", "49"], ["Sol♯","G♯", "51.91"],
            ["La", "A", "55"], ["La♯","A♯", "58.27"], ["Si", "B", "61.74"],
            ["Do", "C", "65.41"], ["Do♯","C♯", "69.3"], ["Ré", "D", "73.42"],
            ["Ré♯","D♯", "77.78"], ["Mi", "E", "82.41"], ["Fa", "F", "87.31"],
            ["Fa♯","F♯", "92.5"], ["Sol", "G", "98"], ["Sol♯","G♯", "103.83"],
            ["La", "A", "110"], ["La♯","A♯", "116.54"], ["Si", "B", "123.47"],
            ["Do", "C", "130.81"], ["Do♯","C♯", "138.59"], ["Ré", "D", "146.83"],
            ["Ré♯","D♯", "155.56"], ["Mi", "E", "164.81"], ["Fa", "F", "174.61"],
            ["Fa♯","F♯", "185"], ["Sol", "G", "196"], ["Sol♯","G♯", "207.65"],
            ["La", "A", "220"], ["La♯","A♯", "233.08"], ["Si", "B", "246.94"],
            ["Do", "C", "261.63"], ["Do♯","C♯", "277.18"], ["Ré", "D", "293.66"],
            ["Ré♯","D♯", "311.13"], ["Mi", "E", "329.63"], ["Fa", "F", "349.23"],
            ["Fa♯","F♯", "369.99"], ["Sol", "G", "392"], ["Sol♯","G♯", "415.3"],
            ["La", "A", "440"], ["La♯","A♯", "466.16"], ["Si", "B", "493.88"],
            ["Do", "C", "523.25"], ["Do♯","C♯", "554.37"], ["Ré", "D", "587.33"],
            ["Ré♯","D♯", "622.25"], ["Mi", "E", "659.26"], ["Fa", "F", "698.46"],
            ["Fa♯","F♯", "739.99"], ["Sol", "G", "783.99"], ["Sol♯","G♯", "830.61"],
            ["La", "A", "880"], ["La♯","A♯", "932.33"], ["Si", "B", "987.77"],
            ["Do", "C", "1046.5"], ["Do♯","C♯", "1108.73"], ["Ré", "D", "1174.66"],
            ["Ré♯","D♯", "1244.51"], ["Mi", "E", "1318.51"], ["Fa", "F", "1396.91"],
            ["Fa♯","F♯", "1479.98"], ["Sol", "G", "1567.98"], ["Sol♯","G♯", "1661.22"],
            ["La", "A", "1760"], ["La♯","A♯", "1864.66"], ["Si", "B", "1975.53"],
            ["Do", "C", "2093"], ["Do♯","C♯", "2217.46"], ["Ré", "D", "2349.32"],
            ["Ré♯","D♯", "2489.02"], ["Mi", "E", "2637.02"], ["Fa", "F", "2793.83"],
            ["Fa♯","F♯", "2959.96"], ["Sol", "G", "3135.96"], ["Sol♯","G♯", "3322.44"],
            ["La", "A", "3520"], ["La♯","A♯", "3729.31"], ["Si", "B", "3951.07"],
            ["Do", "C", "4186.01"], ["Do♯","C♯", "4434.92"], ["Ré", "D", "4698.64"],
            ["Ré♯","D♯", "4978.03"], ["Mi", "E", "5274.04"], ["Fa", "F", "5587.65"],
            ["Fa♯","F♯", "5919.91"], ["Sol", "G", "6271.93"], ["Sol♯","G♯", "6644.88"],
            ["La", "A", "7040"], ["La♯","A♯", "7458.62"], ["Si", "B", "7902.13"]]


    #####################################################################
    # Increment freq
    #####################################################################
    def increment_freq(self, widget):
        if self._index < len(self.keys) - 1:
            self._index = self._index + 1
            freq = self.keys[self._index][2]
            self._button.disconnect(self._handler)
            self._handler = self._button.connect("clicked", self._accordeur.play_note, freq)
            self.set_label()
        if len(self.keys) - 1 == self._index :
            self._button_up.set_sensitive(False)
        self._button_down.set_sensitive(True)
        
    #####################################################################
    # Decrement freq
    #####################################################################
    def decrement_freq(self, widget):
        if self._index > 0:
            self._index = self._index - 1
            freq = self.keys[self._index][2]
            self._button.disconnect(self._handler)
            self._handler = self._button.connect("clicked", self._accordeur.play_note, freq)
            self.set_label()
        if 0 == self._index:
            self._button_down.set_sensitive(False)
        self._button_up.set_sensitive(True)
        
    #####################################################################
    # Set label
    #####################################################################
    def set_label(self):
        notestyle = self._accordeur.get_notestyle()
        if "French" == notestyle:
            label = self.keys[self._index][0]
        elif "English" == notestyle:
            label = self.keys[self._index][1]
        self._button.set_label(label)

    #####################################################################
    # Enable
    #####################################################################
    def enable(self):
        self._button.set_sensitive(True)

    #####################################################################
    # Disable
    #####################################################################
    def disable(self):
        self._button.set_sensitive(False)

    #####################################################################
    # Init
    #####################################################################
    def __init__(self, index, notestyle, accordeur):

        self._index = index
        self._accordeur = accordeur
        
        # Init VBox
        GObject.GObject.__init__(self, spacing=5)

        # Add up arrow
        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266F")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_up = Gtk.Button()
        self._button_up.add(HBox_arrow)
        self.pack_start(self._button_up, False, True, 0)
        HBox_arrow.show()
        self._button_up.show()

        # Add button
        self._button = Gtk.Button()
        self._button.set_size_request(40, 40)
        self.pack_start(self._button, True, True, 0)
        self._button.show()

        # Add down arrow
        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266D")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_down = Gtk.Button()
        self._button_down.add(HBox_arrow)
        self.pack_start(self._button_down, False, True, 0)
        HBox_arrow.show()
        self._button_down.show()

        # Add label
        self.set_label()

        # Connect handler
        self._handler = self._button.connect("clicked", accordeur.play_note, self.keys[index][2])
        self._button_up.connect("clicked", self.increment_freq)
        self._button_down.connect("clicked", self.decrement_freq)

        # Show
        self.show()

#########################################################################
# class Accordeur
#########################################################################
class Accordeur:

    #####################################################################
    # Play note
    #####################################################################
    def play_note(self, widget, freq):
        self._disable_buttons()
        beep_length_sec = 1000 * self._beep_length
        beep_freq = freq

        # Call beep external program
        try:
            self._beep_process = Popen(["beep","-f %s" % beep_freq, "-l %s" % beep_length_sec])
        except OSError:
            # Print message if beep is not installed
            # CLI
            print "Oops!  Apparemment, beep n'est pas installé. (http://johnath.com/beep/)"
            print "Un paquet est sans doute disponible pour votre distribution."
            # GUI
            dialog = Gtk.Dialog(title="beep n'est pas installé", \
                                parent=None, \
                                flags=Gtk.DialogFlags.MODAL, \
                                buttons=(Gtk.STOCK_DIALOG_ERROR, \
                                Gtk.ResponseType.CLOSE))
            error_message = "Oops!  Apparemment, beep n'est pas installé. " \
            + "(http://johnath.com/beep/)\n" \
            + "Un paquet est sans doute disponible pour votre distribution."
            label = Gtk.Label(label=error_message)
            dialog.vbox.pack_start(label, True, True, 0)
            label.show()
            response = dialog.run()
            if (Gtk.ResponseType.CLOSE == response or Gtk.ResponseType.DELETE_EVENT == response):
                dialog.destroy()

        # Set polling in idle to reconnect handles
        else:
            GObject.idle_add(self._poll_beep_in_progress)

    #####################################################################
    # Add key
    #####################################################################
    def _add_key(self, widget, hbox, index, notestyle):
        key = Key(index, notestyle, self)
        hbox.pack_start(key, True, True, 0)
        self._buttons.append(key)
        self._button_rem.set_sensitive(True)

    #####################################################################
    # Remove key
    #####################################################################
    def _rem_key(self, widget):
        if len(self._buttons):
            self._buttons.pop().destroy()
        if 0 == len(self._buttons):
            self._button_rem.set_sensitive(False)
        
    #####################################################################
    # Change note style
    #####################################################################
    def _change_notestyle(self, widget, notestyle):
        self._notestyle = notestyle
        for key in self._buttons:
            key.set_label()

    #####################################################################
    # Get note style
    #####################################################################
    def get_notestyle(self):
        return self._notestyle

    #####################################################################
    # Change beep length
    #####################################################################
    def _change_beep_length (self, widget, beep_length_spin):
        self._beep_length = beep_length_spin.get_value()

    #####################################################################
    # Tune up
    #####################################################################
    def _tune_up (self, widget):
        for key in self._buttons:
            key.increment_freq(None)

    #####################################################################
    # Tune down
    #####################################################################
    def _tune_down (self, widget):
        for key in self._buttons:
            key.decrement_freq(None)

    #####################################################################
    # Disable buttons
    #####################################################################
    def _disable_buttons(self):
        for key in self._buttons:
            key.disable()

    #####################################################################
    # Enable buttons
    #####################################################################
    def _enable_buttons(self):
        for key in self._buttons:
            key.enable()

    #####################################################################
    # Poll beep in progress
    #####################################################################
    def _poll_beep_in_progress (self):
        self._beep_process.poll()
        if (None == self._beep_process.returncode):
            return True
        self._enable_buttons()
        return False

    #####################################################################
    # Init
    #####################################################################
    def __init__(self):

        # Variables
        ###########

        # Buttons and handlers
        self._buttons = []

        # Declare beep process
        self._beep_process = 0

        # Settings
        self._beep_length = 1
        self._notestyle = "French"

        # Create window
        ###############
        self._window = Gtk.Window()
        self._window.connect("destroy", Gtk.main_quit)
        self._window.connect("destroy", Gtk.main_quit)
        self._window.set_title("Accordeur")
        self._window.set_border_width(10)

        # Create vertical box
        VBox = Gtk.VBox(homogeneous=False, spacing=10)

        # Keys horizontal box
        #####################
        HBox_keys = Gtk.HBox()

        # Add global incrementor / decrementor buttons
        VBox_inc_dec = Gtk.VBox()

        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266F")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_up = Gtk.Button()
        self._button_up.add(HBox_arrow)
        self._button_up.set_size_request(40, -1)
        VBox_inc_dec.pack_start(self._button_up, False, True, 0)
        HBox_arrow.show()
        self._button_up.show()
        
        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label=u"\u266D")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_down = Gtk.Button()
        self._button_down.add(HBox_arrow)
        self._button_down.set_size_request(40, -1)
        VBox_inc_dec.pack_end(self._button_down, False, True, 0)
        HBox_arrow.show()
        self._button_down.show()

        VBox_inc_dec.show()
        HBox_keys.pack_start(VBox_inc_dec, True, True, 0)

        self._button_up.connect("clicked", self._tune_up)
        self._button_down.connect("clicked", self._tune_down)

        # Add add / remove key buttons
        VBox_add_rem = Gtk.VBox()

        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="+")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_add = Gtk.Button()
        self._button_add.add(HBox_arrow)
        self._button_add.set_size_request(40, -1)
        VBox_add_rem.pack_start(self._button_add, False, True, 0)
        HBox_arrow.show()
        self._button_add.show()
        
        HBox_arrow = Gtk.HBox()
        arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.OUT)
        HBox_arrow.pack_start(arrow, True, True, 0)
        arrow.show()
        label = Gtk.Label(label="-")
        HBox_arrow.pack_start(label, True, True, 0)
        label.show()
        self._button_rem = Gtk.Button()
        self._button_rem.add(HBox_arrow)
        self._button_rem.set_size_request(40, -1)
        VBox_add_rem.pack_end(self._button_rem, False, True, 0)
        HBox_arrow.show()
        self._button_rem.show()

        VBox_add_rem.show()
        HBox_keys.pack_end(VBox_add_rem, True, True, 0)

        self._button_add.connect("clicked", self._add_key, HBox_keys, 33, self._notestyle)
        self._button_rem.connect("clicked", self._rem_key)

        # Add default keys
        nb_keys = 6
        default_key_indexes = [28, 33, 38, 43, 47, 52]
        for i in range (nb_keys):
            self._add_key(None, HBox_keys, default_key_indexes[i], self._notestyle)
 
        # Settings horizontal box
        #########################
        HBox_settings = Gtk.HBox(homogeneous=False, spacing=10)

        # Note style selector
        VBox_notestyle = Gtk.VBox()
        label = Gtk.Label(label="Notation")
        label.set_alignment(0,1)
        VBox_notestyle.pack_start(label, False, True, 0)
        label.show()
        button = Gtk.RadioButton.new_with_label_from_widget(None, "Française")
        button.connect("clicked", self._change_notestyle, "French")
        VBox_notestyle.pack_start(button, False, True, 0)
        button.show()
        button = Gtk.RadioButton.new_with_label_from_widget(button, "Anglaise")
        button.connect("clicked", self._change_notestyle, "English")
        VBox_notestyle.pack_start(button, False, True, 0)
        button.show()
        HBox_settings.pack_start(VBox_notestyle, False, True, 0)
        VBox_notestyle.show()

        # Separator
        separator = Gtk.VSeparator()
        HBox_settings.pack_start(separator, False, True, 0)
        separator.show()

        # Beep length
        VBox_beep_length= Gtk.VBox()
        label = Gtk.Label(label="Durée (s)")
        label.set_alignment(0,1)
        VBox_beep_length.pack_start(label, False, True, 0)
        label.show()
        beep_length_adj = Gtk.Adjustment(value=self._beep_length, \
                                         lower=1, \
                                         upper=10, \
                                         step_increment=0.5, \
                                         page_increment=1, \
                                         page_size=0)
        beep_length_spin = Gtk.SpinButton(adjustment=beep_length_adj, climb_rate=0, digits=1)
        beep_length_adj.connect("value_changed", self._change_beep_length, beep_length_spin)
        VBox_beep_length.pack_start(beep_length_spin, False, True, 0)
        beep_length_spin.show()
        HBox_settings.pack_start(VBox_beep_length, False, True, 0)
        VBox_beep_length.show()

        # Show everything
        #################
        VBox.pack_start(HBox_keys, True, True, 0)
        VBox.pack_start(HBox_settings, True, True, 0)
        HBox_keys.show()
        HBox_settings.show()
        VBox.show()
        self._window.add(VBox)
        self._window.show()

#########################################################################
# main
#########################################################################
def main():
    Gtk.main()
    return 0       

if __name__ == "__main__":
    Accordeur()
    main()

