# identify the shell
rc=""
case "$SHELL" in
"/bin/bash") rc="$HOME/.bashrc" ;;
"/bin/zsh") rc="$HOME/.zshrc" ;;
esac

# verify the shell's rc setup file
if [ -z "$rc" ]; then
    echo "E: Could not identify run-command file to add aliases to." 1>&2
    exit 1
fi

if ! [ -f "$rc" ]; then
    echo "E: The expected run-command file ($rc) does not exist." 1>&2
    exit 1
fi

# clone the master branch to the specified directory

# attempt to use the python3 alias to be explicit
pyAlias="python"
if [ -x $(command -v python3 &>/dev/null) ]; then
    pyAlias="python3"
fi

# add the alias to the rc file
x=$(tail -c 1 "$rc")
if [ -n "$x" ]; then
    echo >>$rc
fi
echo "alias sdr = $pyAlias EXEPATH" >>$rc
