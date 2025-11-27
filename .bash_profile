# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

/etc/profile.d/mashup_user.sh

if [[ -n "SSH_CONNECTION" ]]; then
    python3 /usr/bin/client.py &
fi

