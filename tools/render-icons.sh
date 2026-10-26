#!/bin/sh
# Renders the PNG and ICO icons from the SVGs with headless Firefox (macOS path by default;
# set FIREFOX). Each image is drawn over black and over white, and tools/pngtool.py recovers
# the transparency from the pair.
set -eu
cd "$(dirname "$0")/.."
FIREFOX=${FIREFOX:-/Applications/Firefox.app/Contents/MacOS/firefox}
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/profile"

# render <svg> <size> <out.png>
render() {
    for bg in black white; do
        printf '<!doctype html><body style="margin:0;background:%s"><img src="file://%s" width="%s" height="%s" style="display:block">' \
            "$bg" "$PWD/$1" "$2" "$2" > "$tmp/$bg.html"
        "$FIREFOX" --headless --profile "$tmp/profile" --window-size "$2,$2" \
            --screenshot "$tmp/$bg.png" "file://$tmp/$bg.html" > /dev/null 2>&1
    done
    python3 tools/pngtool.py alpha "$tmp/black.png" "$tmp/white.png" "$3"
    echo "$3"
}

render app-icon.svg 512 app-icon-512.png
render favicon.svg 32 favicon-32.png
render assets/apple-touch-icon.svg 180 apple-touch-icon.png
render favicon.svg 16 "$tmp/16.png"
render favicon.svg 48 "$tmp/48.png"
python3 tools/pngtool.py ico favicon.ico "$tmp/16.png" favicon-32.png "$tmp/48.png"
echo favicon.ico
