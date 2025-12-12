"""
Laminar Claude Code Proxy - Python bindings for HTTP proxy server
"""

import httpx
import logging
import threading
import time
from .lmnr_claude_code_proxy import run, stop

logger = logging.getLogger(__name__)

__all__ = ["run_server", "stop_server", "set_current_trace"]

HEALTH_CHECK_INTERVAL = 1

# Module-level variables to track the server state
_server_port: int = 45667
_target_url: str = ""
_monitor_thread: threading.Thread | None = None
_stop_monitoring = threading.Event()


def set_current_trace(
    trace_id: str,
    span_id: str,
    project_api_key: str,
    span_ids_path: list[str] | None = None,
    span_path: list[str] | None = None,
    laminar_url: str = "https://api.lmnr.ai",
) -> None:
    """
    Set the current trace context by sending an HTTP request to the running proxy server.
    
    Args:
        trace_id: The trace ID
        span_id: The span ID
        project_api_key: The project API key
        span_ids_path: List of span IDs in the path
        port: Optional port number. If not provided, uses the port from the last run() call.
    
    Raises:
        ValueError: If no port is provided and run() hasn't been called yet.
        httpx.HTTPError: If the HTTP request fails.
    """
    global _server_port
    
    # Determine which port to use
    target_port = _server_port
    
    # Prepare the JSON payload
    payload = {
        "trace_id": trace_id,
        "span_id": span_id,
        "project_api_key": project_api_key,
        "span_ids_path": span_ids_path or [],
        "span_path": span_path or [],
        "laminar_url": laminar_url,
    }
    
    # Send POST request to the internal endpoint
    url = f"http://127.0.0.1:{target_port}/lmnr-internal/span-context"
    
    with httpx.Client() as client:
        response = client.post(url, json=payload, timeout=5.0)
        response.raise_for_status()



def _health_check_monitor() -> None:
    """
    Background thread that monitors server health and restarts if needed.
    Polls every HEALTH_CHECK_INTERVAL seconds.
    """
    global _server_port, _target_url
    
    while not _stop_monitoring.is_set():
        # Wait for HEALTH_CHECK_INTERVAL seconds, but check stop flag more frequently
        if _stop_monitoring.wait(timeout=HEALTH_CHECK_INTERVAL):
            break
            
        # Try to check server health
        try:
            url = f"http://127.0.0.1:{_server_port}/lmnr-internal/health"
            with httpx.Client() as client:
                response = client.get(url, timeout=2.0)
                if response.status_code == 200:
                    # Server is healthy
                    continue
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as e:
            # Server is not responding, try to restart
            logger.warning("Server health check failed: %s. Attempting to restart...", e)
            try:
                # Try to stop the existing server (it might be stuck)
                try:
                    stop()
                except Exception:
                    pass  # Server might already be dead
                
                # Wait a bit before restarting
                time.sleep(0.1)
                
                # Restart the server
                run(_target_url, _server_port)
                logger.info("Server restarted successfully")
            except Exception as restart_error:
                logger.error("Failed to restart server: %s", restart_error)


def run_server(target_url: str, port: int) -> None:
    """
    Run the proxy server in a background thread with health monitoring.
    
    A background monitor thread will check the server health every
    HEALTH_CHECK_INTERVAL seconds and automatically restart it if it dies.
    
    Args:
        target_url: The target URL to proxy requests to
        port: The port to listen on
    """
    global _server_port, _target_url, _monitor_thread, _stop_monitoring
    
    # Stop any existing monitoring
    if _monitor_thread is not None and _monitor_thread.is_alive():
        _stop_monitoring.set()
        _monitor_thread.join(timeout=HEALTH_CHECK_INTERVAL)
    
    # Reset the stop flag
    _stop_monitoring.clear()
    
    # Store server configuration
    _server_port = port
    _target_url = target_url
    
    # Start the server
    try:
        run(target_url, port)
    except Exception as e:
        logger.error("Error running the proxy server: %s", e)
        raise
    
    # Start the health check monitor thread
    _monitor_thread = threading.Thread(target=_health_check_monitor, daemon=True)
    _monitor_thread.start()
    logger.info("Started proxy server with health monitoring on port %d", port)


def stop_server() -> None:
    """
    Stop the proxy server and its health monitoring thread.
    """
    global _monitor_thread, _stop_monitoring
    
    # Signal the monitor thread to stop
    _stop_monitoring.set()
    
    # Stop the server
    try:
        stop()
    except Exception as e:
        logger.debug("Error stopping the proxy server: %s", e)
    
    # Wait for monitor thread to finish
    if _monitor_thread is not None:
        _monitor_thread.join(timeout=2.0)
        _monitor_thread = None
    
    logger.debug("Stopped proxy server and health monitoring")

