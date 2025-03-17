 # What is it?

reload_addon is an add-on for Blender to speed up the update of the addon you are creating without having to close and reopen Blender.

# How this add-on works?

This add-on searches for all modules and updates them one by one. Just follow these steps to get it working:

1. The add-on you are working on must be installed in Blender.
2. Select the add-on you're working on from the drop-down menu, in the Panel space, or in the Preferences options.
3. Once you've edited your add-on and saved the changes, use the keyboard shortcut Shift + Alt + R and the add-on will update.


![alt text](https://github.com/cgclouds/images/blob/main/01%20-%20Choose%20an%20add-on.png)


# Limitations

1. This add-on works with simple projects and also with menu options with images. For more complex projects, there's no guarantee that it will work correctly.
2. Modules that call functions from other modules that haven't been updated will retain their pre-update functions. You can edit the update order in List of Modules. Or you could use the keyboard shortcut twice.

# Installation

1. Download the addon from the releases page.
2. Open Blender and go to Edit -> Preferences -> Add-ons.
3. Press the arrow button in the top-right corner and hit "Install from Disk".
4. Locate where you saved the addon, select it and hit "Install from Disk".

Enjoy!

# Help & Support

To report any bugs or request a feature, you can either use the [issues page](https://github.com/cgclouds/reload_addon/issues).
