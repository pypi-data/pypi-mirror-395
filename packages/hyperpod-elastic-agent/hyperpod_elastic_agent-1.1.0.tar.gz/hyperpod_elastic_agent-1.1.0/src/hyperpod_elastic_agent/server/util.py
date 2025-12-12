import json

from ..ipc.util import IPCWorkerGroup
from ..logagent.log_agent import LogState
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentState(str, Enum):
    """
    INIT -  The Agent is initialized but the API, socketserver
            (and training processing in case of In-process restart) are not initialized yet
    READY - Agent is ready to receive commands from control plane
    RUNNING - Agent received a START job command
    COMPLETED - Training script succeeded
    FAULTED - Training script failed
    STOPPING - Agent received a `/stop` request from a RUNNING or FAULTED state.
               Once workers are stopped this will auto-transition to READY
    SHUTDOWN - Agent received a command to shut down
    """
    INIT = "INIT"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAULTED = "FAULTED"
    STOPPING = "STOPPING"
    SHUTDOWN = "SHUTDOWN"


PLR_VALID_TRANSITIONS = {
    AgentState.INIT: [
        AgentState.READY,
        AgentState.SHUTDOWN,
    ],
    AgentState.READY: [
        AgentState.RUNNING,
        AgentState.SHUTDOWN,
    ],
    AgentState.RUNNING: [
        AgentState.COMPLETED,
        AgentState.FAULTED,
        AgentState.STOPPING,
        AgentState.SHUTDOWN,  # For testing only
    ],
    AgentState.FAULTED: [
        AgentState.STOPPING,
        AgentState.SHUTDOWN,
    ],
    AgentState.STOPPING: [
        AgentState.READY,  # Automated
    ],
    AgentState.COMPLETED: [
        AgentState.SHUTDOWN,
        AgentState.STOPPING,
    ],
    AgentState.SHUTDOWN: [],
}

IPR_VALID_TRANSITIONS = {
    AgentState.INIT: [
        AgentState.READY,
        AgentState.SHUTDOWN,
        AgentState.FAULTED,
    ],
    AgentState.READY: [
        AgentState.INIT,
        AgentState.RUNNING,
        AgentState.SHUTDOWN,
        AgentState.FAULTED,
    ],
    AgentState.RUNNING: [
        AgentState.INIT,
        AgentState.COMPLETED,
        AgentState.FAULTED,
        AgentState.STOPPING,
        AgentState.SHUTDOWN,  # For testing only
    ],
    AgentState.FAULTED: [
        AgentState.INIT,
        AgentState.STOPPING,
        AgentState.SHUTDOWN,
    ],
    AgentState.STOPPING: [
        AgentState.READY,  # Automated
        AgentState.INIT,
    ],
    AgentState.COMPLETED: [
        AgentState.SHUTDOWN,
        AgentState.STOPPING,
    ],
    AgentState.SHUTDOWN: [],
}

AGENT_STATE_EXPLANATIONS = {
    AgentState.INIT: "The agent is initializing. It will transition to READY once the initialization is finished",
    AgentState.READY: "The agent is ready to begin training, and is waiting for the rest of the training agents to be ready. It will begin running when it receives a start signal from the HyperPodTrainingOperator",
    AgentState.RUNNING: "The agent is now running the training script",
    AgentState.FAULTED: "The agent has detected a fault and stopped training. It is waiting for the HyperPodTrainingOperator to acknowledge the fault",
    AgentState.STOPPING: "The agent has been stopped and is now cleaning up resources to restart. It will automatically transition to READY once done",
    AgentState.COMPLETED: "The agent is finished after the training script has exited successfully",
    AgentState.SHUTDOWN: "The agent has received the shutdown signal and is not exiting",
}


@dataclass
class AgentInfo:
    state: AgentState
    transitions: dict[AgentState, str]
    reason: Optional[str] = None
    message: Optional[str] = None
    ip_version: Optional[str] = None
    ipc_worker_group: Optional[IPCWorkerGroup] = None


@dataclass
class StatusResponse:
    status: str
    transitions: Dict[AgentState, str]
    agent_version: str
    reason: Optional[str] = None
    message: Optional[str] = None
    progress: Optional[dict[str, Any]] = None
    ip_version: Optional[str] = None
    assigned_rank: Optional[str] = None
    ipc_worker_group: Optional[IPCWorkerGroup] = None
    spare: Optional[str] = None
    priority: Optional[str] = None
    restart_mode: Optional[str] = None


class StatusResponseJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, StatusResponse):
            response = {
                "status": o.status.lower(),
                "transitions": o.transitions,
            }
            if o.reason:
                response["reason"] = o.reason
            if o.message:
                response["message"] = o.message
            if o.restart_mode:
                response["restartMode"] = o.restart_mode
            if o.ipc_worker_group:
                worker_data = o.ipc_worker_group.get_worker_data()
                if worker_data:
                    response["worker_data"] = worker_data
                response["rank_labels"] = o.ipc_worker_group.get_rank_labels()
                restart_mode = o.ipc_worker_group.get_operator_restart_mode()
                if restart_mode:
                    response["restartMode"] = restart_mode
            if o.ip_version:
                response["ipversion"] = o.ip_version
            if o.progress:
                response["progress"] = o.progress
            if o.agent_version:
                response["agent_version"] = o.agent_version
            if o.assigned_rank:
                response["assigned_rank"] = o.assigned_rank
            if o.spare:
                response["spare"] = o.spare
            if o.priority:
                response["priority"] = o.priority
            return response
        return super().default(o)
