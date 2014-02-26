# Rapid Settings #

* Author: Alberto buffolino.

This add-on provides a quick access to all NVDA settings, grouping all settings categories in a tree structure, and lets you to search among them when you forget where is a specific option.

Furthermore, the window title gives you information about the current active configuration profile (normal configuration, or other, if you created it).

## Usage ##

Simply press NVDA+O and navigate in the tree, expanding your desired section of settings. When you want to change a setting value, press tab and modify the value in the combobox, editbox, and so on.

You can also search in all settings, using the specific field before the tree; to restore the original tree after a research, simply press enter key in search field.

## Key commands ##

* NVDA+o (all layouts): open main window.
* Enter (in search field): restore original settings tree.

## Changes for 1.0 ##

* First release.

### Bugs still present ###

* Search field content is not updated on Braille when it cleaned automatically.
* If you press escape on a combobox, editbox, radio button or slider, the event is not processed by main dialog, generating errors.
* When you select a Braille display that requires port selection, the port combobox is not shown immediately.
* If you get an error in Braille display selection (display not found), after pressing ok the original dialog appears.
