"""Network interface discovery utilities for local and remote hosts."""

from __future__ import annotations

import json
import socket
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol

import psutil

from hil_testbench.run.exceptions import ConfigurationError


class RemoteExecutionContext(Protocol):
    """Minimal interface required to query remote network information."""

    is_remote: bool
    streamer: Any

    def run(self, command: str, capture: bool = True, **_unused: Any) -> int: ...


@dataclass(slots=True)
class InterfaceRecord:
    """Structured representation of a network interface."""

    name: str
    address: str
    is_loopback: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "address": self.address,
            "is_loopback": self.is_loopback,
        }


class _LocalInterfaceCollector:
    def __init__(self, ipv4_only: bool):
        self._ipv4_only = ipv4_only

    def collect(self) -> list[InterfaceRecord]:
        try:
            net_interfaces = psutil.net_if_addrs()
        except Exception:  # pragma: no cover - psutil missing/unavailable
            return []

        records: list[InterfaceRecord] = []
        for iface_name, addrs in net_interfaces.items():
            record = self._first_ipv4_record(iface_name, addrs)
            if record:
                records.append(record)
        return records

    def _first_ipv4_record(
        self,
        iface_name: str,
        addrs: Iterable[Any],
    ) -> InterfaceRecord | None:
        for addr in addrs:
            if self._ipv4_only and addr.family != socket.AF_INET:
                continue
            address = getattr(addr, "address", "")
            if not address:
                continue
            return InterfaceRecord(
                name=iface_name,
                address=address,
                is_loopback=address.startswith("127."),
            )
        return None


class _RemoteCommandRunner:
    def __init__(self, context: RemoteExecutionContext) -> None:
        self._context = context

    def run_python_snippet(self, snippet: str) -> str | None:
        command = f"python3 -c {json.dumps(snippet)}"
        return self._execute(command)

    def run_command(self, command: str) -> str | None:
        return self._execute(command)

    def _execute(self, command: str) -> str | None:
        try:
            exit_code = self._context.run(command, capture=True)
        except Exception:
            return None
        streamer = getattr(self._context, "streamer", None)
        if exit_code != 0 or streamer is None:
            return None
        try:
            return streamer.get_stdout()
        except Exception:  # pragma: no cover - defensive
            return None


class _RemoteInterfaceCollector:
    def __init__(self, context: RemoteExecutionContext, ipv4_only: bool):
        if not context.is_remote:
            raise ConfigurationError(
                "get_remote_interfaces requires remote ExecutionContext",
                context={"context_type": type(context).__name__},
            )
        self._runner = _RemoteCommandRunner(context)
        self._ipv4_only = ipv4_only

    def collect(self) -> list[InterfaceRecord]:
        for strategy in (
            self._collect_via_python,
            self._collect_via_ip_json,
            self._collect_via_ifconfig,
            self._collect_via_ipconfig,
        ):
            records = strategy()
            if records:
                return records
        return []

    def _collect_via_python(self) -> list[InterfaceRecord]:
        snippet = _build_python_interface_script(self._ipv4_only)
        output = self._runner.run_python_snippet(snippet)
        if not output:
            return []
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return []
        return _records_from_mappings(data)

    def _collect_via_ip_json(self) -> list[InterfaceRecord]:
        output = self._runner.run_command("ip -j addr show")
        if not output:
            return []
        return _parse_ip_addr_output(output, self._ipv4_only)

    def _collect_via_ifconfig(self) -> list[InterfaceRecord]:
        output = self._runner.run_command("ifconfig -a")
        if not output:
            return []
        return _parse_ifconfig_output(output)

    def _collect_via_ipconfig(self) -> list[InterfaceRecord]:
        output = self._runner.run_command("ipconfig")
        if not output:
            return []
        return _parse_ipconfig_output(output)


def get_local_interfaces(ipv4_only: bool = True) -> list[dict[str, Any]]:
    """Return interface metadata for the local host."""

    collector = _LocalInterfaceCollector(ipv4_only)
    return _records_to_dicts(collector.collect())


def get_remote_interfaces(
    context: RemoteExecutionContext, ipv4_only: bool = True
) -> list[dict[str, Any]]:
    """Return interface metadata for a remote execution context."""

    collector = _RemoteInterfaceCollector(context, ipv4_only)
    return _records_to_dicts(collector.collect())


def get_non_loopback_ipv4_interfaces(
    context: RemoteExecutionContext | None = None,
) -> list[dict[str, Any]]:
    """Prefer non-loopback IPv4 interfaces, falling back to loopback when needed."""

    if context is None or not context.is_remote:
        records = _LocalInterfaceCollector(ipv4_only=True).collect()
    else:
        records = _RemoteInterfaceCollector(context, ipv4_only=True).collect()
    return _records_to_dicts(_prefer_non_loopback(records))


def _records_to_dicts(records: list[InterfaceRecord]) -> list[dict[str, Any]]:
    return [record.as_dict() for record in records]


def _records_from_mappings(data: Iterable[dict[str, Any]]) -> list[InterfaceRecord]:
    records: list[InterfaceRecord] = []
    for item in data:
        name = item.get("name")
        address = item.get("address")
        if not name or not address:
            continue
        records.append(
            InterfaceRecord(
                name=name,
                address=address,
                is_loopback=bool(item.get("is_loopback", address.startswith("127."))),
            )
        )
    return records


def _build_python_interface_script(ipv4_only: bool) -> str:
    ipv4_filter = "if addr.family == 2:" if ipv4_only else "if True:"
    return (
        "import json, socket\n"
        "try:\n"
        "    import psutil\n"
        "    ifaces = []\n"
        "    for name, addrs in psutil.net_if_addrs().items():\n"
        "        for addr in addrs:\n"
        f"            {ipv4_filter}\n"
        "                is_loopback = addr.address.startswith('127.')\n"
        "                ifaces.append({'name': name, 'address': addr.address, 'is_loopback': is_loopback})\n"
        "                break\n"
        "    print(json.dumps(ifaces))\n"
        "except ImportError:\n"
        "    print('[]')\n"
    )


def _parse_ip_addr_output(output: str, ipv4_only: bool) -> list[InterfaceRecord]:
    try:
        ip_data = json.loads(output)
    except json.JSONDecodeError:
        return []

    records: list[InterfaceRecord] = []
    for iface in ip_data:
        name = iface.get("ifname", "")
        for addr_info in iface.get("addr_info", []):
            if ipv4_only and addr_info.get("family") != "inet":
                continue
            address = addr_info.get("local")
            if not address:
                continue
            records.append(
                InterfaceRecord(
                    name=name,
                    address=address,
                    is_loopback=address.startswith("127."),
                )
            )
            break
    return records


def _parse_ifconfig_output(output: str) -> list[InterfaceRecord]:
    records: list[InterfaceRecord] = []
    current_iface: str | None = None
    for line in output.splitlines():
        if line and not line[0].isspace():
            current_iface = line.split(":")[0].strip()
            continue
        if "inet " not in line or not current_iface:
            continue
        address = _extract_ifconfig_address(line)
        if address:
            records.append(_build_record(current_iface, address))
    return records


def _extract_ifconfig_address(line: str) -> str | None:
    parts = line.split()
    for idx, value in enumerate(parts):
        if value == "inet" and idx + 1 < len(parts):
            return parts[idx + 1].split("/")[0]
    return None


def _parse_ipconfig_output(output: str) -> list[InterfaceRecord]:
    records: list[InterfaceRecord] = []
    current_iface: str | None = None
    for raw_line in output.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if lowered.endswith(":") and "adapter" in lowered:
            current_iface = line.rstrip(":").split("adapter", 1)[-1].strip()
            continue
        if "IPv4 Address" not in line or not current_iface:
            continue
        parts = line.split(":", 1)
        if len(parts) < 2:
            continue
        address = parts[1].split("(")[0].strip()
        records.append(_build_record(current_iface, address))
    return records


def _build_record(name: str, address: str) -> InterfaceRecord:
    return InterfaceRecord(name=name, address=address, is_loopback=address.startswith("127."))


def _prefer_non_loopback(records: list[InterfaceRecord]) -> list[InterfaceRecord]:
    non_loopback = [record for record in records if not record.is_loopback]
    return non_loopback or records


__all__ = [
    "get_local_interfaces",
    "get_remote_interfaces",
    "get_non_loopback_ipv4_interfaces",
]
