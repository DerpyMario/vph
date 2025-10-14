#!/bin/bash
# Usage: ./macos.sh MAC_USER_PASSWORD VNC_PASSWORD NGROK_AUTH_TOKEN MAC_REALNAME

set -e  # Exit on error

# Validate arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 MAC_USER_PASSWORD VNC_PASSWORD NGROK_AUTH_TOKEN MAC_REALNAME"
    exit 1
fi

MAC_USER_PASSWORD="$1"
VNC_PASSWORD="$2"
NGROK_AUTH_TOKEN="$3"
MAC_REALNAME="$4"
USERNAME="tcv"

echo "Starting macOS VNC setup..."

# Disable Spotlight indexing (helps with performance)
echo "Disabling Spotlight indexing..."
mdutil -i off -a

# Create new user account
echo "Creating user account: $USERNAME"
dscl . -create /Users/$USERNAME
dscl . -create /Users/$USERNAME UserShell /bin/bash
dscl . -create /Users/$USERNAME RealName "$MAC_REALNAME"
dscl . -create /Users/$USERNAME UniqueID 1001
dscl . -create /Users/$USERNAME PrimaryGroupID 80
dscl . -create /Users/$USERNAME NFSHomeDirectory /Users/$USERNAME
dscl . -passwd /Users/$USERNAME "$MAC_USER_PASSWORD"

# Create home directory
echo "Creating home directory..."
createhomedir -c -u $USERNAME > /dev/null 2>&1 || true

# Add user to admin group
echo "Adding user to admin group..."
dscl . -append /Groups/admin GroupMembership $USERNAME

# Enable Screen Sharing (VNC)
echo "Enabling Screen Sharing/VNC..."
/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate
/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -allowAccessFor -allUsers -privs -all
/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -clientopts -setvnclegacy -vnclegacy yes

# Set VNC password
echo "Setting VNC password..."
echo "$VNC_PASSWORD" | perl -we 'BEGIN { @k = unpack "C*", pack "H*", "1734516E8BA8C5E2FF1C39567390ADCA"}; $_ = <>; chomp; s/^(.{8}).*/$1/; @p = unpack "C*", $_; foreach (@k) { printf "%02X", $_ ^ (shift @p || 0) }; print "\n"' | tee /Library/Preferences/com.apple.VNCSettings.txt > /dev/null

# Restart Screen Sharing
echo "Restarting Screen Sharing service..."
/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -restart -agent -console

# Wait for services to start
sleep 5

# Install ngrok if not present
if ! command -v ngrok &> /dev/null; then
    echo "Installing ngrok..."
    brew install --cask ngrok
else
    echo "ngrok already installed"
fi

# Configure ngrok
echo "Configuring ngrok..."
ngrok config add-authtoken "$NGROK_AUTH_TOKEN"

# Start ngrok tunnel for VNC (port 5900)
echo "Starting ngrok tunnel on port 5900..."
ngrok tcp 5900 --log=stdout > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

echo "VNC Setup complete!"
echo "Username: $USERNAME"
echo "VNC is running on port 5900"
echo "Ngrok PID: $NGROK_PID"
echo "Ngrok will be available at http://127.0.0.1:4040"
echo ""
echo "Setup completed successfully!"
