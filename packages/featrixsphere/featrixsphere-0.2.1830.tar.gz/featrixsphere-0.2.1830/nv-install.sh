#!/usr/bin/env bash
set -euo pipefail

########################################
# Config – tweak if you want
########################################
TORCH_INDEX_URL="https://download.pytorch.org/whl/cu124"  # CUDA 12.4 wheels
# If you want to pin a version later:
# TORCH_PKG="torch==2.4.1"
TORCH_PKG="torch"  # latest torch for cu124

########################################
# Must be run on Ubuntu with sudo/root
########################################
if [[ "$EUID" -ne 0 ]]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

echo "=== Detecting Ubuntu version ==="
. /etc/os-release
echo "Ubuntu: $PRETTY_NAME"

if [[ "$ID" != "ubuntu" ]]; then
  echo "This script is intended for Ubuntu. Detected ID=$ID."
  exit 1
fi

########################################
# Base Python + tools (with python3-is-python)
########################################
echo "=== apt update & core packages ==="
# Set DEBIAN_FRONTEND to noninteractive to avoid debconf errors
export DEBIAN_FRONTEND=noninteractive
apt-get update -y

echo "=== Installing Python 3 + pip ==="
apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  build-essential \
  wget curl git ca-certificates gnupg lsb-release pciutils \
  nvtop \
  vim

# Ensure `python` runs python3
if ! command -v python >/dev/null 2>&1; then
  echo "Setting up python command (python3-is-python or fallback)..."
  if ! apt-get install -y python3-is-python 2>/dev/null; then
    if ! apt-get install -y python-is-python3 2>/dev/null; then
      # If neither package exists, create a symlink manually
      echo "Creating python symlink manually..."
      ln -sf /usr/bin/python3 /usr/bin/python || true
    fi
  fi
fi

echo "Python versions:"
python --version || true
python3 --version || true

########################################
# Check GPU presence
########################################
echo "=== Checking for NVIDIA GPU ==="
if lspci | grep -qi 'NVIDIA'; then
  echo "NVIDIA GPU detected:"
  lspci | grep -i 'NVIDIA' || true
else
  echo "WARNING: No NVIDIA GPU detected by lspci. Continuing anyway..."
fi

########################################
# NVIDIA driver + CUDA repo
########################################
echo "=== Installing NVIDIA CUDA repository and driver ==="

CUDA_KEYRING_PKG="cuda-keyring_1.1-1_all.deb"
CUDA_KEYRING_URL="https://developer.download.nvidia.com/compute/cuda/repos/ubuntu${VERSION_ID//./}/x86_64/${CUDA_KEYRING_PKG}"

# Add NVIDIA CUDA repo keyring if not already installed
if ! dpkg -s cuda-keyring >/dev/null 2>&1; then
  echo "Downloading CUDA keyring from: $CUDA_KEYRING_URL"
  curl -fsSL "$CUDA_KEYRING_URL" -o "/tmp/${CUDA_KEYRING_PKG}"
  dpkg -i "/tmp/${CUDA_KEYRING_PKG}"
  rm "/tmp/${CUDA_KEYRING_PKG}"
fi

apt-get update -y

# Install CUDA meta-package (includes driver + toolkit)
echo "Installing 'cuda' meta-package (driver + toolkit)..."
apt-get install -y cuda

echo "=== NVIDIA driver and CUDA toolkit installed ==="

# Overwrite profile script each time (idempotent)
CUDA_PROFILE="/etc/profile.d/cuda.sh"
echo "=== Writing ${CUDA_PROFILE} ==="
cat > "$CUDA_PROFILE" << 'EOF'
# CUDA environment
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
EOF

########################################
# Reboot notice (for driver)
########################################
echo "=================================================="
echo "Driver install done. You *should* reboot once this"
echo "script completes so the kernel picks up the driver."
echo "=================================================="

########################################
# PyTorch install via pip (system-wide)
########################################
#echo "=== Upgrading pip (with --break-system-packages) ==="
#python -m pip install --upgrade pip --break-system-packages

echo "=== Upgrading pip first ==="
# Use python3 explicitly for pip upgrade
python3 -m pip install --upgrade pip || true

echo "=== Installing PyTorch (${TORCH_PKG}) with CUDA (index: ${TORCH_INDEX_URL}) ==="
# Determine which python command to use (python or python3)
PYTHON_CMD="python3"
if command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

# Check if pip supports --break-system-packages flag using the same python command
if ${PYTHON_CMD} -m pip install --help 2>&1 | grep -q "break-system-packages"; then
  echo "Using --break-system-packages flag (pip >= 23.0)"
  ${PYTHON_CMD} -m pip install --break-system-packages \
    --index-url "${TORCH_INDEX_URL}" \
    "${TORCH_PKG}"
else
  echo "Using --user flag (older pip version)"
  ${PYTHON_CMD} -m pip install --user \
    --index-url "${TORCH_INDEX_URL}" \
    "${TORCH_PKG}"
fi

echo "=== Verifying PyTorch + CUDA ==="
${PYTHON_CMD} << 'EOF'
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("CUDA device count:", torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(f"Device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("!!! CUDA NOT AVAILABLE IN TORCH !!!")
EOF

echo "=================================================="
echo "DONE."
echo
echo "If this is the first run on this box, reboot once:"
echo "  sudo reboot"
echo
echo "Then you can do:"
echo "  python -c 'import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))'"
echo "=================================================="

