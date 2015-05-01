#!/usr/bin/env python
# -*- coding: UTF8 -*-

# tuner.py
# version 1.2

import pygtk
pygtk.require('2.0')
import gtk, gobject
from subprocess import Popen

#########################################################################
# class Accordeur
#########################################################################
class Accordeur:

    #####################################################################
    # Play the note
    #####################################################################
    def play_note(self, widget, freq):
        self.disable_buttons()
        beep_length_sec = 1000 * self.beep_length
        beep_freq = freq * pow(2, self.tuning/6)

        # Call beep external program
        try:
            self.beep_process = Popen(["beep","-f %s" % beep_freq, "-l %s" % beep_length_sec])
        except OSError:
            # Print message if beep is not installed
            # CLI
            print "Oops!  Apparemment, beep n'est pas installé. (http://johnath.com/beep/)"
            print "Un paquet est sans doute disponible pour votre distribution."
            # GUI
            dialog = gtk.Dialog(title="beep n'est pas installé", parent=None, flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_DIALOG_ERROR, gtk.RESPONSE_CLOSE))
            error_message = "Oops!  Apparemment, beep n'est pas installé. " \
            + "(http://johnath.com/beep/)\n" \
            + "Un paquet est sans doute disponible pour votre distribution."
            label = gtk.Label(error_message)
            dialog.vbox.pack_start(label, True, True, 0)
            label.show()
            response = dialog.run()
            if (gtk.RESPONSE_CLOSE == response or gtk.RESPONSE_DELETE_EVENT == response):
                dialog.destroy()

        # Set polling in idle to reconnect handles
        else:
            gobject.idle_add(self.poll_beep_in_progress)

    #####################################################################
    # Create keys
    #####################################################################
    def add_keys(self, box):
        for key in range(len(self.keys)):
            button = gtk.Button()
            button.connect("clicked", self.play_note, self.keys[key][2])
            button.set_usize(40, 40)
            box.pack_start(button)
            button.show()
            self.buttons.append(button)

    #####################################################################
    # Set labels
    #####################################################################
    def set_key_labels(self, notestyle):
        for key in range(len(self.keys)):
            if notestyle == "French":
                label = self.keys[key][0]
            elif notestyle == "English":
                label = self.keys[key][1]
            else:
                print "Note style %s does not exist, defaulting to english" \
                % notestyle
                label = self.keys[key][1]
            self.buttons[key].set_label(label)

    #####################################################################
    # Toggle note style
    #####################################################################
    def change_notestyle(self, widget, notestyle):
        self.set_key_labels(notestyle)

    #####################################################################
    # Change beep length
    #####################################################################
    def change_beep_length (self, widget, beep_length_spin):
        self.beep_length = beep_length_spin.get_value()

    #####################################################################
    # Change tuning
    #####################################################################
    def change_tuning (self, widget, tuning_spin):
        self.tuning = tuning_spin.get_value()

    #####################################################################
    # Disable buttons
    #####################################################################
    def disable_buttons(self):
        for key in range(len(self.buttons)):
            self.buttons[key].set_sensitive(False)

    #####################################################################
    # Enable buttons
    #####################################################################
    def enable_buttons(self):
        for key in range(len(self.buttons)):
            self.buttons[key].set_sensitive(True)

    #####################################################################
    # Poll beep in progress
    #####################################################################
    def poll_beep_in_progress (self):
        self.beep_process.poll()
        if (None == self.beep_process.returncode):
            return True
        self.enable_buttons()
        return False

    #####################################################################
    # Init
    #####################################################################
    def __init__(self):

        # Variables
        ###########

        # Buttons and handlers
        self.buttons = []
        # Keys
        self.keys = [["Mi", "E", 164.81],
                     ["La", "A", 220],
                     ["Ré", "D", 293.66],
                     ["Sol", "G", 392],
                     ["Si", "B", 493.88],
                     ["Mi", "E", 659.26]]

        self.beep_process = 0

        # Settings
        self.beep_length = 1
        self.tuning = 0

        # Create window
        ###############
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_title("Accordeur")
        self.window.set_border_width(10)

        # Create vertical box
        VBox = gtk.VBox(homogeneous=False, spacing=10)

        # Keys horizontal box
        #####################
        HBox_keys = gtk.HBox()
        self.add_keys(HBox_keys)
        self.set_key_labels("French")

        # Settings horizontal box
        #########################
        HBox_settings = gtk.HBox(homogeneous=False, spacing=10)

        # Note style selector
        VBox_notestyle = gtk.VBox()
        label = gtk.Label("Notation")
        label.set_alignment(0,1)
        VBox_notestyle.pack_start(label, expand=False)
        label.show()
        button = gtk.RadioButton(None, "Française")
        button.connect("clicked", self.change_notestyle, "French")
        VBox_notestyle.pack_start(button, expand=False)
        button.show()
        button = gtk.RadioButton(button, "Anglaise")
        button.connect("clicked", self.change_notestyle, "English")
        VBox_notestyle.pack_start(button, expand=False)
        button.show()
        HBox_settings.pack_start(VBox_notestyle, expand=False)
        VBox_notestyle.show()

        # Separator
        separator = gtk.VSeparator()
        HBox_settings.pack_start(separator, expand=False)
        separator.show()

        # Beep length
        VBox_beep_length= gtk.VBox()
        label = gtk.Label("Durée (s)")
        label.set_alignment(0,1)
        VBox_beep_length.pack_start(label, expand=False)
        label.show()
        beep_length_adj = gtk.Adjustment(value=self.beep_length, lower=1, upper=10, step_incr=0.5, page_incr=1, page_size=0)
        beep_length_spin = gtk.SpinButton(adjustment=beep_length_adj, climb_rate=0, digits=1)
        beep_length_adj.connect("value_changed", self.change_beep_length, beep_length_spin)
        VBox_beep_length.pack_start(beep_length_spin, expand=False)
        beep_length_spin.show()
        HBox_settings.pack_start(VBox_beep_length, expand=False)
        VBox_beep_length.show()

        # Separator
        separator = gtk.VSeparator()
        HBox_settings.pack_start(separator, expand=False)
        separator.show()

        # Tuning
        VBox_tuning= gtk.VBox()
        label = gtk.Label("Altération (tons)")
        label.set_alignment(0,1)
        VBox_tuning.pack_start(label, expand=False)
        label.show()
        label = gtk.Label(u"\u266F")
        label.set_alignment(1,0)
        VBox_tuning.pack_start(label, expand=False)
        label.show()
        tuning_adj = gtk.Adjustment(value=self.tuning, lower=-10, upper=10, step_incr=0.5, page_incr=1, page_size=0)
        tuning_spin = gtk.SpinButton(adjustment=tuning_adj, climb_rate=0, digits=1)
        tuning_adj.connect("value_changed", self.change_tuning, tuning_spin)
        VBox_tuning.pack_start(tuning_spin, expand=False)
        tuning_spin.show()
        label = gtk.Label(u"\u266D")
        label.set_alignment(1,0)
        VBox_tuning.pack_start(label, expand=False)
        label.show()
        HBox_settings.pack_start(VBox_tuning, expand=False)
        VBox_tuning.show()

        # Show everything
        #################
        VBox.pack_start(HBox_keys)
        VBox.pack_start(HBox_settings)
        HBox_keys.show()
        HBox_settings.show()
        VBox.show()
        self.window.add(VBox)
        self.window.show()

#########################################################################
# main
#########################################################################
def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    Accordeur()
    main()

