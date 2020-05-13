#!/usr/bin/env sh

NAME="Krita Batch Exporter"

desktop_file="krita_batch_exporter.desktop"
addon_directory="krita_batch_exporter"
addon_path=""

WHEEL_LINUX_x86_64="https://files.pythonhosted.org/packages/c6/42/fdaf9b53942b103462db3d843c5bc3eb660f9b2e58419ebc99ed87d93dd2/Pillow-7.0.0-cp35-cp35m-manylinux1_x86_64.whl"
WHEEL_LINUX_i686="https://files.pythonhosted.org/packages/51/72/b442f78f3d0003885aaf7144b7f26e103a21f29b1c574df68fd1e4ff543e/Pillow-7.0.0-cp35-cp35m-manylinux1_i686.whl"
WHEEL_MACOS="https://files.pythonhosted.org/packages/75/0d/4d112761a257fd15729d09f71153674cc9202f454fba4f29850d919af1ad/Pillow-7.0.0-cp35-cp35m-macosx_10_6_intel.whl"
WHEEL_WINDOWS_x86_64="https://files.pythonhosted.org/packages/24/ab/0fcfd4690d15eb8039a278b173fac2ede5d4139998195a6de3dd370399f4/Pillow-7.0.0-cp35-cp35m-win_amd64.whl"
WHEEL_WINDOWS_i686="https://files.pythonhosted.org/packages/6c/4d/24927160d3e144c2e932ec1d1b39ebbb7396c2741c75691493f474cd0618/Pillow-7.0.0-cp35-cp35m-win32.whl"

# Tests and finds the correct command to run python3
# As on Windows, 'python3' might be 'python'
#
# Outputs the python command to run Python 3 or exits with an error code.
find_python_command() {
	version="$(python -c 'import sys; print(sys.version_info[0])')"
	test $? -ne 0 && exit 1
	test "$version" = "3" && echo "python" && return

	version="$(python3 -c 'import sys; print(sys.version_info[0])')"
	test $? -ne 0 && exit 1
	test "$version" = "3" && echo "python3" && return
}

# Installs the add-on to the krita resources folder
#
# Arguments:
# $1 -- pykrita directory path
# $2 -- url of the wheel file to download
install() {
	python_command="$(find_python_command)"
	test $? -ne 0 && echo "You need to have Python 3 installed to install $NAME. Exiting" && exit 1

	pykrita_dir="$1"
	pillow_wheel="$2"

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

	echo "Copying 'krita_batch_exporter/' to '$pykrita_dir'..."
	cp -r "$addon_directory" "$desktop_file" "$pykrita_dir"
	echo "Done."
	cd "$pykrita_dir" || exit 1
	eval "$python_command -m pip install --upgrade --target $addon_directory/Dependencies/ -- $pillow_wheel"
	test $? -ne 0 && exit 1

	cd "$folder_start" || exit 1
}

# Deletes the add-on files in the krita resources folder
#
# Arguments:
# $1 -- pykrita directory path
clean() {
	pykrita_dir="$1"

	echo "hello"

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
		pillow_wheel=$WHEEL_LINUX_x86_64
		uname -a | grep --quiet x86_64 || pillow_wheel=$WHEEL_LINUX_i686
		;;
	"darwin")
		pykrita_dir="/Users/$USER/Library/Application Support/krita/pykrita"
		pillow_wheel=$WHEEL_MACOS
		;;
	"windowsnt" | "msys" | "mingw64_nt")
		pykrita_dir="$APPDATA/krita/pykrita"
		pillow_wheel=$WHEEL_WINDOWS_x86_64
		uname -a | grep --quiet x86_64 || pillow_wheel=$WHEEL_WINDOWS_i686
		;;
	*)
		echo "Your platform, '$platform', is not supported. Exiting the program."
		exit 1
		;;
	esac

	install "$pykrita_dir" "$pillow_wheel" || exit 1
}

# SCRIPT
main

case $? in
0) echo "Successfully installed $NAME in $addon_path" ;;
128) echo "The addon directory already exists in $pykrita_dir, canceling the installation." ;;
*) echo "There was an error installing the Pillow image library. Canceling the install." ;;
esac

exit $?
