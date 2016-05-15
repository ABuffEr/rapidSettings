# Rapid Settings #

* Author: Alberto buffolino.
* Download [development version][1]

This add-on provides quick access to most NVDA settings, grouping all settings categories in a tree structure, and lets you search among them when you forget where a specific option is.

Furthermore, the window title gives you information about the current active configuration profiles, and specific combobox and context menu let you simply manage all profiles.

## Usage ##

Simply press NVDA+O and navigate in the tree, expanding your desired section of settings. When you want to change a setting value, press tab and modify the value in the combobox, editbox, and so on, or press space directly on the tree item if you want to cycle through possible values or to increment the current value (if numeric).

By default you modify settings for the current active profile, but you can also choose your desired profile from the specific combobox. Note: you choose a profile to edit rather than  choosing the current active profile.  For this, use "manual activate" in the context menu of the combobox, menu where you can also rename, delete or create a new profile. In addition, this menu lets you enable/disable all triggers.

You can also search  all settings using the search field before the tree; to restore the original tree after a search, simply press the enter key in the search field.

## Key commands ##

* NVDA+O (all layouts): open main window.
* Enter (in search field): restore original settings tree.
* Space (on a tree item): cycle through possible values of the setting, or increment the current value (if numeric).
* Applications key (on profile combobox): view all possible actions for selected profile.

## Changes for 2.0 ##

* Profile management implementation.
* Various bug fixes.

## Changes for 1.0 ##

* First release.

### Bugs or problems still present ###

* Braille remains on a blank line when search field is cleaned automatically.
* It's not possible to use return on a tree item to simulate click on ok button (see code for details).
* Enable or disable triggers from context menu requires to close dialog for coherence reasons (see code for details).
* When you select a Braille display that requires port selection, the port combobox is not shown immediately.

[1]: http://addons.nvda-project.org/files/get.php?file=rs-dev