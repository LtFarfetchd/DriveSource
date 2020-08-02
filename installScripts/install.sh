rc=""
case "$SHELL" in
"/bin/bash") rc=$("~/.bashrc") ;;
"/bin/zsh") rc=$("~/.zshrc") ;;
esac

if [ -z "$rc" ]; then
    echo "Error: Could not identify run-command file to add aliases." 1>&2
    exit 1
fi

if ! [ -f "$rc" ]; then
    printf "Error: The expected run-command file (%s) does not exist." "$rc" 1>&2
    exit 1
fi

# x=$(tail -c 1 "$shell")
# if [ tail -c 1 ./bashrc ]; then
#     echo >>aFile.txt
# fi
# echo "some line of text" >>aFile.txt
