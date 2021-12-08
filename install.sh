#!/usr/bin/env sh

NAME="Batch Exporter"

desktop_file="kritapykrita_batch_exporter.desktop"
addon_directory="batch_exporter"
addon_path=""

# Installs the add-on to the krita resources folder.
#
# Arguments:
# $1 -- pykrita directory path
install() {
	pykrita_dir="$1"

	folder_start="$(pwd)"

	addon_path="$pykrita_dir/$addon_directory"
	if test -d "$addon_path"; then
		echo "The directory $addon_path already exists. Overwrite?"
		input=""
		while test -z "$(echo $input | grep -E '^(y(es)?)|(no?)$')"; do
			echo "yes / no"
			read -r input
		done
		test "$(echo "$input" | grep -E 'y(es)?')" && clean "$pykrita_dir" || exit 128
		test $? -ne 0 && exit 128
	fi

	echo "Copying $addon_directory to '$pykrita_dir'..."
	cp -r "$addon_directory" "$desktop_file" "$pykrita_dir"
	echo "Done."
	cd "$pykrita_dir" || exit 1
	test $? -ne 0 && exit 1

	cd "$folder_start" || exit 1
}

# Deletes the add-on files in the krita resources folder
#
# Arguments:
# $1 -- pykrita directory path
clean() {
	pykrita_dir="$1"

	echo "Cleaning up the existing addon directory..."
	echo "$pykrita_dir/$addon_directory"
	rm -rf "${pykrita_dir:?}/$addon_directory" "${pykrita_dir:?}/$desktop_file"
	test $? -ne 0 && echo "There was an error removing the $addon_path directory." && exit 1
	echo "Done."
}

main() {
	platform="$(uname | tr '[:upper:]' '[:lower:]' | cut -d- -f 1)"

	case "$platform" in
	"linux" | "freebsd")
		pykrita_dir="$HOME/.local/share/krita/pykrita"
		;;
	"darwin")
		pykrita_dir="/Users/$USER/Library/Application Support/krita/pykrita"
		;;
	"windowsnt" | "msys" | "mingw64_nt")
		pykrita_dir="$APPDATA/krita/pykrita"
		;;
	*)
		echo "Your platform, '$platform', is not supported. Exiting the program."
		exit 1
		;;
	esac

	install "$pykrita_dir" || exit 1
}

# SCRIPT
main

case $? in
0) echo "Successfully installed $NAME in $addon_path" ;;
128) echo "The addon directory already exists in $pykrita_dir, canceling the installation." ;;
*) echo "There was an error installing installing the add-on. Canceling the install." ;;
esac

exit $?
