#!/usr/bin/env python3
"""
Build verification script for AIBE extension.

Checks that content.js is up-to-date with its source files before packaging.
Fails with clear error message if rebuild is needed.
"""

import os
import sys
from pathlib import Path


def get_modification_time(file_path):
    """Get file modification time, or 0 if file doesn't exist."""
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return 0


def verify_content_js_build():
    """
    Verify that content.js is newer than all its source files.

    Returns:
        True if content.js is up to date, False otherwise
    """
    # Find the extension directory relative to this script
    script_dir = Path(__file__).parent
    extension_dir = script_dir / "aibe_server" / "extension"

    # Target file
    content_js = extension_dir / "content.js"

    # Source files
    content_entry = extension_dir / "content.entry.js"
    modules_dir = extension_dir / "modules"

    # Check if content.js exists
    if not content_js.exists():
        print("ERROR: content.js not found!")
        print(f"  Expected location: {content_js}")
        print("\nYou must build the extension before packaging:")
        print("  cd server/aibe_server/extension")
        print("  npm install")
        print("  npx esbuild content.entry.js --bundle --outfile=content.js --format=iife")
        return False

    content_js_time = get_modification_time(content_js)

    # Check entry point
    if content_entry.exists():
        if get_modification_time(content_entry) > content_js_time:
            print("ERROR: content.entry.js is newer than content.js!")
            print("  content.js must be rebuilt")
            print("\nRun the build command:")
            print("  cd server/aibe_server/extension")
            print("  npx esbuild content.entry.js --bundle --outfile=content.js --format=iife")
            return False

    # Check all module files
    if modules_dir.exists():
        stale_modules = []
        for module_file in modules_dir.glob("*.js"):
            if get_modification_time(module_file) > content_js_time:
                stale_modules.append(module_file.name)

        if stale_modules:
            print("ERROR: The following module files are newer than content.js:")
            for module in stale_modules:
                print(f"  - {module}")
            print("\ncontent.js must be rebuilt:")
            print("  cd server/aibe_server/extension")
            print("  npx esbuild content.entry.js --bundle --outfile=content.js --format=iife")
            return False

    # All checks passed
    print("✓ Build verification passed: content.js is up to date")
    return True


def main():
    """Main entry point for command-line usage."""
    if verify_content_js_build():
        sys.exit(0)
    else:
        print("\nBuild verification FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
