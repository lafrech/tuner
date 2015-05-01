#!/usr/bin/env python
# -*- coding: UTF8 -*-

# tuner.py
# version 1.0

import pygtk
pygtk.require('2.0')
import gtk
from subprocess import call

#########################################################################
# class Accordeur
#########################################################################
class Accordeur:

    #####################################################################
    # Play the note
    #####################################################################
    def play_note(self, widget, freq):
        beep_length_sec = 1000 * self.beep_length
        beep_freq = freq * pow(2, self.tuning/6)
        try:
            call(["beep","-f %s" % beep_freq, "-l %s" % beep_length_sec])
        except OSError:
            print "Oops!  Apparemment, beep n'est pas installé. (http://johnath.com/beep/)"
            print "Un paquet est sans doute disponible pour votre distribution."

    #####################################################################
    # Create keys
    #####################################################################
    def add_keys(self, box):
        for key in range(len(self.keys)):
            button = gtk.Button()
            self.buttons.append(button)
            button.set_usize(40, 40)
            button.connect("clicked", self.play_note, self.keys[key][2])
            box.pack_start(button)
            button.show()

    #####################################################################
    # Set labels
    #####################################################################
    def set_key_labels(self):
        for key in range(len(self.keys)):
            if self.notestyle == "French":
                label = self.keys[key][0]
            elif self.notestyle == "English":
                label = self.keys[key][1]
            else:
                print "Note style %s does not exist, defaulting to english" % self.notestyle
                label = self.keys[key][1]
            self.buttons[key].set_label(label)

    #####################################################################
    # Toggle note style
    #####################################################################
    def toggle_notestyle(self, widget, data):
        self.notestyle = data
        self.set_key_labels()

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
    # Init
    #####################################################################
    def __init__(self):

        # Variables
        ###########

        # Buttons
        self.buttons = []
        # Keys
        self.keys = [["Mi", "E", 164.81],["La", "A", 220],["Ré", "D", 293.66],["Sol", "G", 392],["Si", "B", 493.88],["Mi", "E", 659.26]]

        # Settings
        self.notestyle = "French"
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
        self.set_key_labels()

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
        button.connect("clicked", self.toggle_notestyle, "French")
        VBox_notestyle.pack_start(button, expand=False)
        button.show()
        button = gtk.RadioButton(button, "Anglaise")
        button.connect("clicked", self.toggle_notestyle, "English")
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

