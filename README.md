pdfXBlock
=========

### Description ###

This XBlock provides an easy way to embed a PDF.

- Download button available
- (Optional) Source document download button, for example to provide your PPT file

### Customize the XBlock ###

- By default, PDF Download Allowed is set on True. The default value can  be changed in `pdfXBlock / pdf / pdf.py`

### Install / Update the XBlock ###

    # Move to the folder where you want to download the XBlock
    cd /edx/app/edxapp
    # Download the XBlock
    sudo -u edxapp git clone https://github.com/MarCnu/pdfXBlock.git
    # Install the XBlock
    sudo -u edxapp /edx/bin/pip.edxapp install pdfXBlock/
    # Upgrade the XBlock if it is already installed, using --upgrade
    sudo -u edxapp /edx/bin/pip.edxapp install pdfXBlock/ --upgrade
    # Remove the installation files
    sudo rm -r pdfXBlock

### Reboot if something isn't right ###

    sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:

### Activate the XBlock in your course ###
Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["pdf"]`.

### Use the XBlock in a unit ###
Select `Advanced -> PDF` in your unit.
