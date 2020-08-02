rc=""
case "$SHELL" in
"/bin/bash") rc="$HOME/.bashrc" ;;
"/bin/zsh") rc="$HOME/.zshrc" ;;
esac

if [ -z "$rc" ]; then
    echo "E: Could not identify run-command file to add aliases." 1>&2
    exit 1
fi

if ! [ -f "$rc" ]; then
    echo "E: The expected run-command file ($rc) does not exist." 1>&2
    exit 1
fi

# x=$(tail -c 1 "$shell")
# if [ tail -c 1 ./bashrc ]; then
#     echo >>aFile.txt
# fi
# echo "some line of text" >>aFile.txt
