#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 vendor:model (e.g. 1bcf:2284)"
  exit 1
fi

vendor_model=$1
vendor=${vendor_model%%:*}
model=${vendor_model##*:}
dir="${vendor_model}"

mkdir -p "$dir"

# Find /dev/video device matching vendor:model
video_dev=$(udevadm info -q path -n /dev/video* | while read -r path; do
  if udevadm info -a -p "$path" | grep -q "ATTRS{idVendor}==\"$vendor\"" && \
     udevadm info -a -p "$path" | grep -q "ATTRS{idProduct}==\"$model\""; then
    basename "$(udevadm info -q name -p "$path")"
    break
  fi
done)

if [ -z "$video_dev" ]; then
  echo "No /dev/video device found for $vendor_model"
  exit 2
fi

video_path="/dev/$video_dev"

# Save udev info
udevadm info -a -n "$video_path" > "$dir/udevinfo.txt"

# Save v4l2 info: formats, controls, and all info
{
  echo "=== List Formats Extended ==="
  v4l2-ctl -d "$video_path" --list-formats-ext
  echo
  echo "=== Controls ==="
  v4l2-ctl -d "$video_path" -l
  echo
  echo "=== All Info ==="
  v4l2-ctl -d "$video_path" --all
} > "$dir/v4l2info.txt"

echo "Info saved to $dir/udevinfo.txt and $dir/v4l2info.txt"



