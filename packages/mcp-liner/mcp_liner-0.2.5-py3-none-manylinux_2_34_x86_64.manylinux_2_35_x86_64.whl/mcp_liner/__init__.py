"""
mcp-liner: MCP Server for Liner configuration generation.
"""

import ctypes
import os
import sys
import threading


def main():
    # Locate the shared library
    package_dir = os.path.dirname(os.path.abspath(__file__))

    if sys.platform.startswith("win"):
        lib_name = "_mcp_liner.dll"
    elif sys.platform.startswith("darwin"):
        lib_name = "_mcp_liner.so"
    else:
        lib_name = "_mcp_liner.so"

    lib_path = os.path.join(package_dir, lib_name)

    # Fallback search
    if not os.path.exists(lib_path):
        patterns = [
            os.path.join(package_dir, lib_name),
            os.path.join(os.getcwd(), lib_name),
            os.path.join(os.getcwd(), "mcp_liner", lib_name),
        ]
        found = False
        for p in patterns:
            if os.path.exists(p):
                lib_path = p
                found = True
                break

        if not found:
            print(f"Error: Could not find shared library {lib_name}")
            print(f"Searched in: {package_dir}, {os.getcwd()}")
            sys.exit(1)

    try:
        # Load the shared library
        lib = ctypes.CDLL(lib_path)

        # Config RunShared signature
        lib.RunShared.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]

        # Prepare arguments
        argv_list = [arg.encode("utf-8") for arg in sys.argv]
        argv_c = (ctypes.c_char_p * len(argv_list))(*argv_list)
        argc = len(argv_list)

        # Run RunShared in a separate thread because it blocks
        t = threading.Thread(target=lib.RunShared, args=(argc, argv_c))
        t.start()

        # Main thread waits and handles signals
        while t.is_alive():
            try:
                # Sleep briefly to allow signal handling
                t.join(timeout=0.1)
            except KeyboardInterrupt:
                # Call exported Stop function from Go
                if hasattr(lib, "Stop"):
                    lib.Stop()
                else:
                    print("Warning: Stop function not found in library")

                # Wait for thread to finish
                t.join()
                sys.exit(0)

    except Exception as e:
        print(f"Error running mcp-liner: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
