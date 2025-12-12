import json
import threading
import uvicorn
from typing import Optional, List, Dict, Any, Union

from .util import AgentState, StatusResponse, StatusResponseJSONEncoder
from .api_models import UpdateRequest, StopRequest, StartRequest
from fastapi import FastAPI, Response, Request
from fastapi.exceptions import RequestValidationError
from http import HTTPStatus
from torch.distributed.elastic.utils.logging import get_logger
from fastapi.responses import JSONResponse

logger = get_logger(__name__)

class HyperPodElasticAgentServer(threading.Thread):
    """
    Starts a new thread running a FastAPI+uvicorn based server to receive commands from Job Controller
    and updates the state machine for the JobAgent.
    The `status` API reads the `RunResult` state of the workers and returns it as a JSON response.
    """

    def __init__(self, agent, server_specs):
        super().__init__()
        
        # Initialize FastAPI with metadata for better documentation
        self._app = FastAPI(
            title="HyperPod Elastic Agent API",
            description="API for controlling and monitoring the HyperPod Elastic Agent",
            version="1.1.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json"
        )
        
        # Add exception handler for validation errors
        self._app.add_exception_handler(RequestValidationError, self._validation_exception_handler)
        
        self._register_routes()
        self._agent = agent
        config = uvicorn.Config(self._app, **server_specs)
        self._server = uvicorn.Server(config)

    @property
    def started(self):
        return self._server.started
        
    def _register_routes(self):
        """
        Register API routes with FastAPI.
        
        Uses Pydantic models for request validation on /start and /update endpoints.
        Includes tags and summaries for better API documentation.
        """
        self._app.add_api_route(
            "/start", 
            self._api_start, 
            methods=["POST"], 
            response_model=None,
            summary="Start the agent",
            description="Starts the agent with the provided configuration and sets its state to RUNNING",
            tags=["Agent Control"]
        )
        self._app.add_api_route(
            "/stop", 
            self._api_stop, 
            methods=["POST"],
            response_model=None,
            summary="Stop the agent",
            description="Stops the agent and sets its state to STOPPING",
            tags=["Agent Control"]
        )
        self._app.add_api_route(
            "/status", 
            self._api_status, 
            methods=["GET"],
            summary="Get agent status",
            description="Returns the current status of the agent",
            tags=["Agent Status"]
        )
        self._app.add_api_route(
            "/update", 
            self._api_update, 
            methods=["POST"],
            response_model=None,
            summary="Update agent configuration",
            description="Updates the agent configuration with new values",
            tags=["Agent Control"]
        )
        self._app.add_api_route(
            "/shutdown",
            self._api_shutdown,
            methods=["POST"],
            summary="Shutdown the agent",
            description="Shuts down the agent completely",
            tags=["Agent Control"]
        )

    async def _api_start(self, request: StartRequest) -> Response:
        # Bit of a hack to update the agent state immediately
        # so that the operator doesn't run into race conditions
        self._agent.set_agent_state_running()
        
        # Update agent info with validated request data
        self._update_agent_info(request)            
        self._agent.set_assigned_rank(request.rank)            
        self._agent.update_progress(request.progress)
        self._agent.can_start = True
        
        return Response(status_code=HTTPStatus.OK)

    async def _api_stop(self, request: Optional[StopRequest] = None) -> Response:
        # Use default values if request is None
        restart_mode = "ipr"
        is_graceful = None
        timeout = None
        
        if request is not None:
            restart_mode = request.restart_mode if request.restart_mode is not None else "ipr"
            is_graceful = request.is_graceful
            timeout = request.timeout
            
        logger.info(f"API /stop called with restart_mode={restart_mode}, is_graceful={is_graceful}, timeout={timeout}")
        
        self._agent.set_restart_mode(restart_mode)
        # Store parameters for _stop_workers to use
        self._agent.set_graceful_shutdown_params(is_graceful, timeout)
        logger.info(f"Set shutdown parameters in agent: is_graceful={is_graceful}, timeout={timeout}")
        self._agent.set_agent_state(AgentState.STOPPING)
        self._agent.can_start = False
        logger.info(f"Agent state set to STOPPING")
        return Response(status_code=HTTPStatus.OK)

    def _api_status(self) -> Response:
        progress = self._agent.get_agent_progress()
        agent_version = self._agent.version
        assigned_rank = self._agent.get_assigned_rank()
        agent_info = self._agent.get_agent_state_info()
        spare = str(self._agent.spare)
        restart_mode = self._agent.get_restart_mode()
        status_resp = StatusResponse(
            status=agent_info.state,
            reason=agent_info.reason,
            message=agent_info.message,
            transitions=agent_info.transitions,
            agent_version=agent_version,
            progress=progress,
            ip_version=agent_info.ip_version,
            ipc_worker_group=agent_info.ipc_worker_group,
            spare=spare,
            restart_mode=restart_mode,
        )
        if self._agent.priority:
            status_resp.priority = "True"
        if assigned_rank >= 0:
            status_resp.assigned_rank = str(assigned_rank)
        resp_txt = json.dumps(status_resp,
                              ensure_ascii=False,
                              allow_nan=False,
                              indent=None,
                              separators=(",", ":"),
                              cls=StatusResponseJSONEncoder).encode("utf-8")
        return Response(resp_txt)

    async def _api_update(self, request: UpdateRequest) -> Response:
        # Update agent info with validated request data
        self._update_agent_info(request)
        
        # Incremental ranking - for IPR this will send rank info to all local ranks
        # No op for PLR
        self._agent.send_rank_info(request.rank)
        
        # Return response (same as /status)
        return self._api_status()

    def _api_shutdown(self) -> Response:
        self._agent.set_agent_state(AgentState.SHUTDOWN)
        return Response(status_code=HTTPStatus.OK)
    
    def _update_agent_info(self, request):
        """
        Helper method that updates the agent state
        with the values from the request_dict.
        """        
        self._agent.update_rendezvous_info(
            request.rank,
            request.nnodes,
            request.faultCount,
            request.master_addr,
            request.master_port,
            request.ipVersion,
            request.rankIps,
            request.worker_data,
        )
        self._agent.set_log_monitoring_configuration(
            request.log_monitoring_configuration)
        self._agent.handle_spare_update(request.spare, request.faultCount)

    def run(self):
        """
        Sets up the server config and starts the uvicorn server on a new event loop
        """
        logger.debug(f"Server thread id: {threading.get_ident()}")
        self._server.run()

    def shutdown(self):
        """
        Shuts down the server by updating server properties.
        See `uvicorn.server.Server.main_loop` for more details
        """
        self._server.should_exit = True
        self._server.force_exit = True

    async def _validation_exception_handler(
            self, request: Request, exc: RequestValidationError
        ) -> JSONResponse:
        """
        Custom exception handler for validation errors.
        Logs detailed error information and returns a 422 response.
        """
        error_detail = exc.errors()
        
        # Clean up the error details to ensure they're JSON serializable
        # Remove any non-serializable objects like exceptions
        for err in error_detail:
            if 'ctx' in err and 'error' in err['ctx'] and isinstance(err['ctx']['error'], Exception):
                # Convert exception to string representation
                err['ctx']['error'] = str(err['ctx']['error'])
        
        error_locations = [f"{' -> '.join(str(loc) for loc in err['loc'])}" for err in error_detail]
        error_messages = [err['msg'] for err in error_detail]
        
        # Get the request body for logging
        body = None
        try:
            if hasattr(exc, "body"):
                if isinstance(exc.body, bytes):
                    body = exc.body.decode("utf-8")
                else:
                    body = str(exc.body)
            else:
                # If body is not available in the exception, try to get it from the request
                body_bytes = await request.body()
                if body_bytes:
                    body = body_bytes.decode("utf-8")
        except Exception as e:
            body = f"<Error retrieving request body: {str(e)}>"
        
        # Create a more detailed log message
        log_message = f"Validation error for {request.method} {request.url.path}: "
        for loc, msg in zip(error_locations, error_messages):
            log_message += f"\n  - {loc}: {msg}"
        
        if body:
            log_message += f"\nRequest body: {body}"
        
        logger.error(log_message)
        
        # Return the standard FastAPI validation error response
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={"detail": error_detail},
        )
