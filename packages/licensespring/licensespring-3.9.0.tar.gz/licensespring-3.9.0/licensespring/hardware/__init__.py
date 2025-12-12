import logging
import platform
import socket
import subprocess
import sys
import uuid

from licensespring_hardware_id_generator import (
    HardwareIdAlgorithm,
    get_hardware_id,
    get_logs,
    get_version,
)


class HardwareIdProvider:
    def get_id(self):
        return str(uuid.getnode())

    def get_os_ver(self):
        return platform.platform()

    def get_hostname(self):
        return platform.node()

    def get_ip(self):
        return socket.gethostbyname(self.get_hostname())

    def get_is_vm(self):
        return False

    def get_vm_info(self):
        return None

    def get_mac_address(self):
        return ":".join(("%012X" % uuid.getnode())[i : i + 2] for i in range(0, 12, 2))

    def get_request_id(self):
        return str(uuid.uuid4())


class HardwareIdProviderSource(HardwareIdProvider):
    def get_id(self):
        hardware_id = get_hardware_id(HardwareIdAlgorithm.Default)

        logs = get_logs()
        version = get_version()
        logging.info("Version: ", version)
        logging.info("Hardware ID:", hardware_id)
        for log_line in logs:
            logging.info(log_line)

        return hardware_id


class PlatformIdProvider(HardwareIdProvider):

    def _read_from_win_registry(self, registry, key):
        try:
            from winregistry import WinRegistry

            with WinRegistry() as reg:
                return reg.read_entry(registry, key).value.strip()
        except Exception:
            return None

    def _execute_command(self, cmd):
        try:
            return subprocess.run(
                cmd, shell=True, capture_output=True, check=True, encoding="utf-8"
            ).stdout.strip()
        except Exception:
            return None

    def _read_from_file(self, path):
        try:
            with open(path) as f:
                return f.read().strip()
        except Exception:
            return None

    def _get_mac_id(self):
        return self._execute_command(
            "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'"
        )

    def _get_windows_id(self):
        id = self._read_from_win_registry(
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography", "MachineGuid"
        )
        if not id:
            result = self._execute_command("wmic csproduct get uuid")
            if result:
                lines = result.splitlines()
                if len(lines) >= 3:
                    id = lines[2].strip()
        return id

    def _get_linux_id(self):
        return self._read_from_file("/var/lib/dbus/machine-id") or self._read_from_file(
            "/etc/machine-id"
        )

    def _get_bsd_id(self):
        return self._read_from_file("/etc/hostid") or self._execute_command(
            "kenv -q smbios.system.uuid"
        )

    def get_id(self):
        platform = sys.platform
        id = None

        if platform == "darwin":
            id = self._get_mac_id()
        elif platform in ("win32", "cygwin", "msys"):
            id = self._get_windows_id()
        elif platform.startswith("linux"):
            id = self._get_linux_id()
        elif platform.startswith("openbsd") or platform.startswith("freebsd"):
            id = self._get_bsd_id()

        return id or super().get_id()
