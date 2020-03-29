#!/usr/bin/env sh

NAME="Krita Batch Exporter"

addon_directory="krita_batch_exporter"
addon_path=""

pykrita_dir=""
pillow_wheel=""

WHEEL_LINUX_x86_64="https://files.pythonhosted.org/packages/c6/42/fdaf9b53942b103462db3d843c5bc3eb660f9b2e58419ebc99ed87d93dd2/Pillow-7.0.0-cp35-cp35m-manylinux1_x86_64.whl"
WHEEL_LINUX_i686="https://files.pythonhosted.org/packages/51/72/b442f78f3d0003885aaf7144b7f26e103a21f29b1c574df68fd1e4ff543e/Pillow-7.0.0-cp35-cp35m-manylinux1_i686.whl"
WHEEL_MACOS="https://files.pythonhosted.org/packages/75/0d/4d112761a257fd15729d09f71153674cc9202f454fba4f29850d919af1ad/Pillow-7.0.0-cp35-cp35m-macosx_10_6_intel.whl"
WHEEL_WINDOWS_x86_64="https://files.pythonhosted.org/packages/24/ab/0fcfd4690d15eb8039a278b173fac2ede5d4139998195a6de3dd370399f4/Pillow-7.0.0-cp35-cp35m-win_amd64.whl"
WHEEL_WINDOWS_i686="https://files.pythonhosted.org/packages/6c/4d/24927160d3e144c2e932ec1d1b39ebbb7396c2741c75691493f474cd0618/Pillow-7.0.0-cp35-cp35m-win32.whl"

install() {
	folder_start="$(pwd)"
	echo "Copying 'krita_batch_exporter/' to '$pykrita_dir'..."

	addon_path=$pykrita_dir/$addon_directory
	if test -d "$addon_path"; then
		echo "The directory $addon_path already exists. Overwrite?"
		input=""
		while test -z "$(echo $input | grep -E '^(y(es)?)|(no?)$')"; do
			echo "yes / no"
			read -r input
		done
		test "$(echo $input | grep -E 'y(es)')" && clean || exit 128
		test $? -ne 0 && exit 128
	fi

	cp -r "$addon_directory" "$pykrita_dir"
	echo "Done."
	cd "$pykrita_dir" || exit 1
	python3 -m pip install --target "Dependencies/" -- "$pillow_wheel"
	test $? -ne 0 && exit 1

	cd "$folder_start" || exit 1
}

clean() {
	echo "Cleaning up the existing addon directory..."
	rm -rf "$addon_path"
	test $? && echo "There was an error removing the $addon_path directory." && exit 1
	echo "Done."
	exit 0
}

main() {
	python3 --version || echo "You need to have Python 3 installed to install $NAME. Exiting" && exit 1

	platform="$(uname) | tr [:upper:] [:lower:]"
	case "$platform" in
	"linux" | "freebsd")
		pykrita_dir="$HOME/.local/share/krita/pykrita"
		pillow_wheel=$WHEEL_LINUX_x86_64
		uname -a | grep --quiet x86_64 || pillow_wheel=$WHEEL_LINUX_i686
		;;
	"darwin")
		pykrita_dir="$HOME/.local/share/krita/pykrita"
		pillow_wheel=$WHEEL_MACOS
		;;
	"windowsnt" | "msys")
		pykrita_dir="$APPDATA/krita/pykrita"
		pillow_wheel=$WHEEL_WINDOWS_x86_64
		uname -a | grep --quiet x86_64 || pillow_wheel=$WHEEL_WINDOWS_i686
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
*) echo "There was an error installing the Pillow image library. Canceling the install." ;;
esac

exit $?
