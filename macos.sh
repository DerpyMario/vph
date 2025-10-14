#!/bin/bash

# Move to a safe directory to avoid permission errors
cd /tmp

# Parameters
MAC_USER_PASSWORD="$1"
VNC_PASSWORD="$2"
NGROK_AUTH_TOKEN="$3"
MAC_REALNAME="$4"

# Disable Spotlight indexing
sudo mdutil -i off -a

# Create new account
sudo dscl . -create /Users/tcv
sudo dscl . -create /Users/tcv UserShell /bin/bash
sudo dscl . -create /Users/tcv RealName "$MAC_REALNAME"
sudo dscl . -create /Users/tcv UniqueID 1001
sudo dscl . -create /Users/tcv PrimaryGroupID 80
sudo dscl . -create /Users/tcv NFSHomeDirectory /Users/tcv
sudo dscl . -passwd /Users/tcv "$MAC_USER_PASSWORD"
sudo createhomedir -c -u tcv > /dev/null
sudo dscl . -append /Groups/admin GroupMembership tcv

# Enable Remote Management for the user
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
    -activate -configure -access -on -users tcv -privs -all \
    -restart -agent -menu

# Enable VNC with password
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
    -configure -clientopts -setvnclegacy -vnclegacy yes

echo "$VNC_PASSWORD" | perl -we 'BEGIN { @k = unpack "C*", pack "H*", "1734516E8BA8C5E2FF1C39567390ADCA"}; $_ = <>; chomp; s/^(.{8}).*/$1/; @p = unpack "C*", $_; foreach (@k) { printf "%02X", $_ ^ (shift @p || 0) }; print "\n"' | \
    sudo tee /Library/Preferences/com.apple.VNCSettings.txt

# Install ngrok
brew install --cask ngrok

# Configure ngrok and start it
ngrok authtoken "$NGROK_AUTH_TOKEN"
ngrok tcp 5900 --region=ap &

echo "Setup complete. If you see a black screen in VNC, log into the GUI as 'tcv' first, or grant Screen Recording permissions in System Preferences."
