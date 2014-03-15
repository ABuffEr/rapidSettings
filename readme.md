# Rapid Settings #

* Author: Alberto buffolino.
* Download [development version][1]

This add-on provides a quick access to all NVDA settings, grouping all settings categories in a tree structure, and lets you to search among them when you forget where is a specific option.

Furthermore, the window title gives you information about the current active configuration profiles, and a apposite combobox and context menu let you to simply manage all profiles.

## Usage ##

Simply press NVDA+O and navigate in the tree, expanding your desired section of settings. When you want to change a setting value, press tab and modify the value in the combobox, editbox, and so on, or press space directly on the tree item if you want to cycle through possible values or to increment the current value (if numeric).

To default you modify settings of current active profile, but you can also choose your desired profile from apposite combobox. Note: you choose a profile to editing, you don't set the current active profile; for this, use "manual activate" in context menu of combobox, menu where you can also rename, delete or create a new profile, in addition to enable/disable all triggers.

You can also search in all settings, using the specific field before the tree; to restore the original tree after a research, simply press enter key in search field.

## Key commands ##

* NVDA+O (all layouts): open main window.
* Enter (in search field): restore original settings tree.
* Space (on a tree item): cycle through possible values of the setting, or increment the current value (if numeric).
* Applications key (on profile combobox): view all possible actions for selected profile.

## Changes for 2.0 ##

* Profile management implementation.

## Changes for 1.0 ##

* First release.

### Bugs or problems still present ###

* Braille remains on a blank line when search field it cleaned automatically.
* If you press escape on a combobox, editbox, radio button or slider, the event is not processed by main dialog, generating errors.
* If you press escape on context menu, dialog is closed (not context menu).
* It's not possible to use return on a tree item to simulate click on ok button (see code for details).
* Enable or disable triggers from context menu requires to close dialog for coherence reasons (see code for details).
* When you select a Braille display that requires port selection, the port combobox is not shown immediately.
* If you get an error in Braille display selection (display not found), after pressing ok the original dialog appears.

[1]: http://addons.nvda-project.org/files/get.php?rs-dev