#!/bin/bash

# Source wheel
WHEEL="dist/gabriel_server-4.1-py3-none-any.whl"

# Target directories
TARGETS=(
    "/home/achanana/lab-work/steeleagle/backend/server/engines/telemetry"
    "/home/achanana/lab-work/steeleagle/backend/server/engines/avoidance"
    "/home/achanana/lab-work/steeleagle/backend/server/engines/detection"
    "/home/achanana/lab-work/steeleagle/backend/server/engines/gabriel-server"
)

# Copy wheel to each target
for DIR in "${TARGETS[@]}"; do
    cp "$WHEEL" "$DIR/"
    echo "Copied $WHEEL to $DIR/"
done

