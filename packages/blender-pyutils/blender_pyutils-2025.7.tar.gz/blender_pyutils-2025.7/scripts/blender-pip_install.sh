#!/usr/bin/env bash
set -euo pipefail

# This is the original version of the code that only served to install packages
# in Blender's module directory. Use "blender-pyutils pip" instead.

# Usage examples
#
# Install the tqdm package.
# blender-pip_install.sh tqdm
#
# Install a package from source in the current directory.
# blender-pip_install.sh .
#
# Install all packages in a requirements.txt file.
# blender-pip_install.sh -r requirements.txt
~~~


tmp_dir=$(mktemp -d)
# shellcheck disable=SC2064
trap "rm -fr ${tmp_dir@Q}" EXIT
cat > "$tmp_dir/get_version.py" <<'SCRIPT'
#!/usr/bin/env python3
"""Print the Python version."""
import sys
import bpy
vinfo = sys.version_info
print(f"{vinfo.major}.{vinfo.minor}.{vinfo.micro}")
bpy.ops.wm.quit_blender()
SCRIPT

# Installed version of blender.
blender_version=$(blender -v | sed -n 's/^Blender //p')

# Blender version of Python.
blender_pyversion=$(blender --background --python "$tmp_dir/get_version.py" | \
                    grep -E '^[0-9]+\.[0-9]+\.[0-9]+$')

# Blender configuration directory.
blender_dir=${XDG_CONFIG_HOME:-$HOME/.config}/blender/${blender_version%.*}

# Module directory recognized by blender.
module_dir=${blender_dir}/scripts/modules

log_path=${0##*/}
log_path=${log_path%.*}.log

echo "Blender version: $blender_version"
echo "Python version in Blender: $blender_pyversion"
echo "Detected module directory: $module_dir"
echo "Installation log file: $log_path"

# Install uv within a virtual environment.
function install_uv()
{
  python3 -m ensurepip
  python3 -m pip install -U pip
  python3 -m pip install -U uv
}

# Create the bootstrap virtual environment with uv if necessary.
install_uv=false
if ! command -v uv >/dev/null 2>&1
then
  cat << 'UV_MSG'
It is recommended to install uv for virtual environment management:

  https://docs.astral.sh/uv/getting-started/installation/

For this operation, uv will be installed in a temporary virtual environment.
UV_MSG
  install_uv=true
  python3 -m venv "$tmp_dir/bootstrap_venv"
  # shellcheck source=/dev/null
  source "$tmp_dir/bootstrap_venv/bin/activate"
  install_uv
fi

# Create the virtual environment with Blender's version of Python.
uv venv --python "$blender_pyversion" "$tmp_dir/venv"
# shellcheck source=/dev/null
source "$tmp_dir/venv/bin/activate"
# Install UV in this environment too if necessary.
if "$install_uv"
then
  install_uv
fi

# Create the module directory if missing.
mkdir -p "$module_dir"

# Install the packages to the target directory from the virtual environment with
# the required version of Python.
uv pip install -U --target "$module_dir" "$@"
