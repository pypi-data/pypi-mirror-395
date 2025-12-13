import os
import platform
import subprocess
import sys
from typing import Optional, Tuple


def is_linux() -> bool:
    """
    Check if the current system is Linux.

    Returns:
        bool: True if the system is Linux, False otherwise
    """
    return platform.system() == "Linux"


def is_mac() -> bool:
    """
    Check if the current system is macOS.

    Returns:
        bool: True if the system is macOS, False otherwise
    """
    return platform.system() == "Darwin"


def py_higher_than_314() -> bool:
    """
    Check if Python version is higher than 3.14.

    Returns:
        bool: True if Python version is higher than 3.14, False otherwise
    """
    return sys.version_info >= (3, 14)


def readline_enable() -> bool:
    """
    Check if readline module is available.

    Returns:
        bool: True if readline is available, False otherwise
    """
    try:
        import readline
        return readline is not None
    except ImportError:
        return False


def get_architecture() -> str:
    """
    Get the system architecture.

    Returns:
        str: Architecture string (e.g., 'x86_64', 'aarch64', etc.)
    """
    return platform.machine()


def _get_process_uids_impl(pid: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Internal method to get the UIDs of a process: real, effective, saved, and filesystem UIDs.

    Args:
        pid (str): Process ID as string

    Returns:
        Optional[Tuple[int, int, int, int]]: Tuple of (real_uid, effective_uid, saved_uid, filesystem_uid) or None if failed
    """
    if is_linux():
        try:
            with open(f"/proc/{pid}/status", "r") as f:
                for line in f:
                    if line.startswith("Uid:"):
                        # Format: Uid: real effective saved filesystem
                        uids = line.split()[1:5]
                        return tuple(int(uid) for uid in uids)
        except (FileNotFoundError, PermissionError, ValueError):
            pass
    elif is_mac():
        # On macOS, use ps command to get process UIDs
        try:
            # Get real and saved UIDs using ps command
            result = subprocess.run(
                ["ps", "-o", "ruid,uid,svuid", "-p", str(pid)],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse the output
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                # Skip header line and get the values
                values = lines[1].split()
                if len(values) >= 3:
                    real_uid = int(values[0])
                    effective_uid = int(values[1])  # uid column is effective uid
                    saved_uid = int(values[2])
                    # For macOS, we'll use effective_uid as filesystem_uid as well
                    filesystem_uid = effective_uid
                    return (real_uid, effective_uid, saved_uid, filesystem_uid)
        except (subprocess.CalledProcessError, ValueError, IndexError):
            pass

    return None


def get_process_uids(pid: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Get the UIDs of a process: real, effective, saved, and filesystem UIDs.

    Args:
        pid (str): Process ID as string

    Returns:
        Optional[Tuple[int, int, int, int]]: Tuple of (real_uid, effective_uid, saved_uid, filesystem_uid) or None if failed
    """
    return _get_process_uids_impl(pid)


def get_current_process_uids() -> Tuple[int, int, int, int]:
    """
    Get the UIDs of the current process: real, effective, saved, and filesystem UIDs.

    Returns:
        Tuple[int, int, int, int]: Tuple of (real_uid, effective_uid, saved_uid, filesystem_uid)
    """
    # Try to get UIDs using the internal implementation with current process ID
    uids = _get_process_uids_impl(str(os.getpid()))
    if uids is not None:
        return uids

    # Fallback to os functions
    return (os.getuid(), os.geteuid(), os.geteuid(), os.geteuid())
