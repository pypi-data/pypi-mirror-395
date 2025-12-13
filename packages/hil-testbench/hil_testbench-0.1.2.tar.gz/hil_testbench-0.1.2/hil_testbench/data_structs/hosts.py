"""Data structures for host connection configurations."""

from dataclasses import dataclass
from typing import Any, Literal

SSH_PORT = 22

RemoteOS = Literal["unix", "windows"]


@dataclass
class HostDefinition:
    """Host connection configuration matching Paramiko SSH client requirements.

    Provides all parameters needed to establish an SSH connection via paramiko.SSHClient.connect().
    """

    # Required
    host: str  # hostname or IP address

    # Authentication
    user: str | None = None  # username (defaults to current user if None)
    password: str = ""  # password for password-based auth
    key_filename: str | None = None  # path to private key file
    passphrase: str | None = None  # passphrase for encrypted private key

    # Connection
    port: int = 22  # SSH port
    timeout: float | None = None  # connection timeout in seconds
    local: bool = False  # if True, run locally without SSH (host still used for IP/hostname)

    # Remote OS type for shell wrapper selection
    remote_os: RemoteOS = "unix"  # "unix" for sh-based, "windows" for PowerShell

    # Advanced options
    allow_agent: bool = False  # allow SSH agent for authentication (default off for stability)
    look_for_keys: bool = True  # search for discoverable private keys
    compress: bool = False  # enable compression

    # Connection behavior
    banner_timeout: float | None = None  # timeout for SSH banner
    auth_timeout: float | None = None  # timeout for authentication

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HostDefinition":
        """Create HostConfig from YAML/dict.

        Auto-detects localhost as local execution (no SSH) unless explicitly overridden.
        """
        # Auto-detect: host=localhost implies local=true unless explicitly set
        auto_local = data["host"] == "localhost"

        return cls(
            host=data["host"],
            user=data.get("user"),
            password=data.get("password", ""),
            key_filename=data.get("key_filename"),
            passphrase=data.get("passphrase"),
            port=data.get("port", 22),
            timeout=data.get("timeout"),
            local=data.get("local", auto_local),
            remote_os=data.get("remote_os", "unix"),
            allow_agent=data.get("allow_agent", False),
            look_for_keys=data.get("look_for_keys", True),
            compress=data.get("compress", False),
            banner_timeout=data.get("banner_timeout"),
            auth_timeout=data.get("auth_timeout"),
        )

    def as_string(self) -> str:
        """Convert to string format for TaskRunner: user@host:port."""
        result = self.host
        if self.user:
            result = f"{self.user}@{result}"
        if self.port != SSH_PORT:
            result = f"{result}:{self.port}"
        return result

    def __str__(self) -> str:  # pragma: no cover - trivial
        """Return connection string when coerced to str (for runner plumbing)."""
        return self.as_string()

    def to_paramiko_kwargs(self) -> dict[str, Any]:
        """Get keyword arguments for paramiko.SSHClient.connect().

        Returns dict ready to unpack: client.connect(**host.to_paramiko_kwargs())
        """
        kwargs = {
            "hostname": self.host,
            "port": self.port,
            "allow_agent": self.allow_agent,
            "look_for_keys": self.look_for_keys,
            "compress": self.compress,
        }

        if self.user:
            kwargs["username"] = self.user
        if self.password:
            kwargs["password"] = self.password
        if self.key_filename:
            kwargs["key_filename"] = self.key_filename
        if self.passphrase:
            kwargs["passphrase"] = self.passphrase
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout
        if self.banner_timeout is not None:
            kwargs["banner_timeout"] = self.banner_timeout
        if self.auth_timeout is not None:
            kwargs["auth_timeout"] = self.auth_timeout

        return kwargs
