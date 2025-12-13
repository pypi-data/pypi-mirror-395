"""cx_Freeze setup script."""

from re import sub

from cx_Freeze import Executable, setup

from procustodibus_agent import DESCRIPTION, DISPLAY_NAME, SERVICE_NAME
from procustodibus_agent import __version__ as version

SERVICE_DEFAULT = "Service"

SERVICE_WIN32_OWN_PROCESS = 0x10
SERVICE_AUTO_START = 0x2
SERVICE_ERROR_NORMAL = 0x1

MSIDB_SERVICE_CONTROL_EVENT_START = 0x1
MSIDB_SERVICE_CONTROL_EVENT_STOP = 0x2
MSIDB_SERVICE_CONTROL_EVENT_UNINSTALL_STOP = 0x20
MSIDB_SERVICE_CONTROL_EVENT_UNINSTALL_DELETE = 0x80

EXECUTABLES = [
    Executable(
        script="procustodibus_agent/windows/service_config.py",
        base="Win32Service",
        target_name="ProCustodibusAgentService",
        icon="installer/favicon.ico",
    ),
    Executable(
        script="procustodibus_agent/cli.py",
        base="console",
        target_name="procustodibus-agent",
        icon="installer/favicon.ico",
    ),
    Executable(
        script="procustodibus_agent/credentials.py",
        base="console",
        target_name="procustodibus-credentials",
        icon="installer/favicon.ico",
    ),
    Executable(
        script="procustodibus_agent/mfa/cli.py",
        base="console",
        target_name="procustodibus-mfa",
        icon="installer/favicon.ico",
    ),
]


def _make_component_id(executables, index):
    executable = executables[index]
    component = f"_cx_executable{index}_{executable}"
    return sub(r"[^\w.]", "_", component)


setup(
    name="procustodibus_agent",
    version=version,
    description=DESCRIPTION,
    options={
        "build_exe": {
            "excludes": [
                "test",
                "tkinter",
                "unittest",
            ],
            "includes": [
                "_cffi_backend",
                "cx_Logging",
            ],
            "include_files": [
                ("LICENSE", "LICENSE.txt"),
                ("installer/help.url", "help.url"),
                ("installer/troubleshooting.url", "troubleshooting.url"),
                ("scripts/windows/", "scripts/"),
                ("installer/cnf.txt", "cnf/README.txt"),
                ("installer/log.txt", "log/README.txt"),
            ],
            "include_msvcr": True,
            "packages": [
                "dns",
                "procustodibus_agent",
            ],
        },
        "bdist_msi": {
            "all_users": True,
            "initial_target_dir": f"[ProgramFiles64Folder]{DISPLAY_NAME}",
            "install_icon": "installer/favicon.ico",
            "upgrade_code": "{EBA087D2-BA25-4E0B-A5FB-3DDC676D0D50}",
            "data": {
                "Directory": [
                    (
                        "ProgramMenuFolder",  # ID
                        "TARGETDIR",  # DirectoryParent
                        ".",  # DefaultDir
                    ),
                    (
                        f"{SERVICE_NAME}Folder",  # ID
                        "ProgramMenuFolder",  # DirectoryParent
                        DISPLAY_NAME,  # DefaultDir
                    ),
                ],
                "Property": [
                    ("cmd", "cmd"),
                    ("explorer", "explorer"),
                ],
                "ServiceInstall": [
                    (
                        f"{SERVICE_NAME}{SERVICE_DEFAULT}Install",  # ID
                        f"{SERVICE_NAME}{SERVICE_DEFAULT}",  # Name
                        DISPLAY_NAME,  # DisplayName
                        SERVICE_WIN32_OWN_PROCESS,  # ServiceType
                        SERVICE_AUTO_START,  # StartType
                        SERVICE_ERROR_NORMAL,  # ErrorControl
                        None,  # LoadOrderGroup
                        None,  # Dependencies
                        None,  # StartName
                        None,  # Password
                        None,  # Arguments
                        _make_component_id(EXECUTABLES, 0),  # Component
                        DESCRIPTION,  # Description
                    ),
                ],
                "ServiceControl": [
                    (
                        f"{SERVICE_NAME}{SERVICE_DEFAULT}Control",  # ID
                        f"{SERVICE_NAME}{SERVICE_DEFAULT}",  # Name
                        (
                            MSIDB_SERVICE_CONTROL_EVENT_START
                            + MSIDB_SERVICE_CONTROL_EVENT_STOP
                            + MSIDB_SERVICE_CONTROL_EVENT_UNINSTALL_STOP
                            + MSIDB_SERVICE_CONTROL_EVENT_UNINSTALL_DELETE
                        ),  # Event
                        None,  # Arguments
                        0,  # Wait
                        _make_component_id(EXECUTABLES, 0),  # Component
                    ),
                ],
                "Shortcut": [
                    (
                        f"{SERVICE_NAME}TestMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} Test",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        "/k procustodibus-agent.exe --test",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}VersionMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} Version",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        "/k procustodibus-agent.exe --version",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}MfaMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} MFA Status",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        "/k procustodibus-mfa.exe",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}ServiceStatusMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} Service Status",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        f"/k sc query {SERVICE_NAME}{SERVICE_DEFAULT}",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}ServiceStartMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} Service Start",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        f"/k sc start {SERVICE_NAME}{SERVICE_DEFAULT}",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}ServiceStopMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        f"{DISPLAY_NAME} Service Stop",  # Name
                        "TARGETDIR",  # Component
                        "[cmd]",  # Target
                        f"/k sc stop {SERVICE_NAME}{SERVICE_DEFAULT}",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}HelpMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        "Help",  # Name
                        "TARGETDIR",  # Component
                        "[TARGETDIR]help.url",  # Target
                        None,  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}TroubleshootingMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        "Troubleshooting",  # Name
                        "TARGETDIR",  # Component
                        "[TARGETDIR]troubleshooting.url",  # Target
                        None,  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}ConfigurationMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        "Configuration",  # Name
                        "TARGETDIR",  # Component
                        "[explorer]",  # Target
                        "cnf",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                    (
                        f"{SERVICE_NAME}LogsMenuItem",  # ID
                        f"{SERVICE_NAME}Folder",  # Directory
                        "Logs",  # Name
                        "TARGETDIR",  # Component
                        "[explorer]",  # Target
                        "log",  # Arguments
                        None,  # Description
                        None,  # Hotkey
                        None,  # Icon
                        None,  # IconIndex
                        None,  # ShowCmd
                        "TARGETDIR",  # WkDir
                    ),
                ],
            },
        },
    },
    executables=EXECUTABLES,
)
