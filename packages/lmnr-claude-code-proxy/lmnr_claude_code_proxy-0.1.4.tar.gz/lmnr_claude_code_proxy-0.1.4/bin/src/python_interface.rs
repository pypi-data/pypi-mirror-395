use crate::server;
use std::{sync::Mutex, thread};
use tokio::sync::oneshot;

// Global state to track the running server
struct ServerState {
    _thread_handle: thread::JoinHandle<()>,
    shutdown_tx: oneshot::Sender<()>,
}

impl ServerState {
    fn shutdown(self) -> thread::Result<()> {
        let _ = self.shutdown_tx.send(());
        self._thread_handle.join()?;
        Ok(())
    }
}

const DEFAULT_PORT: u16 = 45667;
static SERVER: Mutex<Option<ServerState>> = Mutex::new(None);

/// Run the proxy server in a background thread
#[pyo3::pyfunction]
#[pyo3(signature = (target_url, port=DEFAULT_PORT))]
pub fn run(target_url: String, port: u16) -> pyo3::prelude::PyResult<()> {
    let mut server_guard = SERVER.lock().unwrap();

    if server_guard.is_some() {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(
            "Server is already running. Call stop() first.",
        ));
    }

    let (shutdown_tx, shutdown_rx) = oneshot::channel();

    let thread_handle = thread::spawn(move || {
        let rt = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .expect("Failed to create Tokio runtime");

        rt.block_on(async {
            if let Err(e) = server::start_server(target_url, port, shutdown_rx).await {
                eprintln!("Server error: {}", e);
            }
        });
    });

    *server_guard = Some(ServerState {
        _thread_handle: thread_handle,
        shutdown_tx,
    });

    Ok(())
}

/// Stop the proxy server
#[pyo3::pyfunction]
#[pyo3(signature = ())]
pub fn stop() -> pyo3::prelude::PyResult<()> {
    let mut server_guard = SERVER.lock().unwrap();

    if let Some(state) = server_guard.take() {
        state.shutdown().map_err(|_| {
            pyo3::exceptions::PyRuntimeError::new_err("Failed to join server thread")
        })?;
        Ok(())
    } else {
        Err(pyo3::exceptions::PyRuntimeError::new_err(
            "No server is currently running.",
        ))
    }
}
