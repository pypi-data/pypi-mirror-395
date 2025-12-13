"""cx_Freeze config for the agent as a Win32Service."""

import procustodibus_agent as agent

NAME = f"{agent.SERVICE_NAME}%s"
DISPLAY_NAME = f"{agent.DISPLAY_NAME} %s"
MODULE_NAME = "procustodibus_agent.windows.service"
CLASS_NAME = "Service"
DESCRIPTION = agent.DESCRIPTION
AUTO_START = False
SESSION_CHANGES = False
