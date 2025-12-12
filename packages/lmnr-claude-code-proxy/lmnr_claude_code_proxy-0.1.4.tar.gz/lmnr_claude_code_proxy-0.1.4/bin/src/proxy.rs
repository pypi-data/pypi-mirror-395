use crate::spans::create_span_request;
use crate::state::{CurrentTraceAndLaminarContext, SharedState};

use futures_util::stream::{Stream, StreamExt};
use http_body_util::{BodyExt, Full, StreamBody, combinators::BoxBody};
use hyper::{
    Method, Request, Response, StatusCode,
    body::{Bytes, Frame, Incoming},
};
use hyper_rustls::HttpsConnector;
use hyper_util::client::legacy::{Client, connect::HttpConnector};
use prost::Message;
use std::sync::Mutex;
use std::{
    pin::Pin,
    sync::Arc,
    task::{Context, Poll},
    time::{SystemTime, UNIX_EPOCH},
};
use tokio::task::JoinSet;

fn get_unix_nano() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards")
        .as_nanos() as u64
}

async fn send_trace_to_lmnr(
    trace_request: crate::proto::opentelemetry_collector_trace_v1::ExportTraceServiceRequest,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    project_api_key: String,
    laminar_url: String,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let endpoint = format!("{laminar_url}/v1/traces");

    // Encode the protobuf message
    let mut buf = Vec::new();
    if let Err(e) = trace_request.encode(&mut buf) {
        eprintln!("Failed to encode trace request: {}", e);
        return Err(e.into());
    }

    // Build the request body
    let body = Full::new(Bytes::from(buf))
        .map_err(|never| match never {})
        .boxed();

    // Build the request with Authorization header
    let auth_header = format!("Bearer {}", project_api_key);
    let req = match Request::builder()
        .method(Method::POST)
        .uri(&endpoint)
        .header("content-type", "application/x-protobuf")
        .header("authorization", auth_header)
        .body(body)
    {
        Ok(req) => req,
        Err(e) => {
            eprintln!("Failed to build request: {}", e);
            return Err(e.into());
        }
    };

    // Send the request
    match client.request(req).await {
        Ok(response) => {
            let status = response.status();
            if !status.is_success() {
                eprintln!("Failed to send trace to LMNR: status {}", status);
            }
        }
        Err(e) => {
            eprintln!("Failed to send trace to LMNR: {}", e);
            return Err(e.into());
        }
    };

    Ok(())
}

struct SpanCapturingStream<S> {
    inner: S,
    accumulated: Arc<Mutex<Vec<Bytes>>>,
    request_body: String,
    trace: Option<CurrentTraceAndLaminarContext>,
    start_time_unix_nano: u64,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
}

impl<S> Stream for SpanCapturingStream<S>
where
    S: Stream<Item = Result<Bytes, hyper::Error>> + Unpin,
{
    type Item = Result<Bytes, hyper::Error>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        match Pin::new(&mut self.inner).poll_next(cx) {
            Poll::Ready(Some(Ok(bytes))) => {
                // Push directly to accumulated using synchronous mutex
                // This ensures all bytes are captured before stream ends
                if let Ok(mut accumulated) = self.accumulated.lock() {
                    accumulated.push(bytes.clone());
                }
                Poll::Ready(Some(Ok(bytes)))
            }
            Poll::Ready(None) => {
                // Stream ended successfully - create span
                self.create_span_in_background();
                Poll::Ready(None)
            }
            Poll::Ready(Some(Err(e))) => {
                // Stream ended with error - still try to create span with partial data
                self.create_span_in_background();
                Poll::Ready(Some(Err(e)))
            }
            Poll::Pending => Poll::Pending,
        }
    }
}

impl<S> SpanCapturingStream<S>
where
    S: Stream<Item = Result<Bytes, hyper::Error>> + Unpin,
{
    fn create_span_in_background(&self) {
        // Capture end time right when stream ends
        let end_time_unix_nano = get_unix_nano();
        let accumulated = self.accumulated.clone();
        let request_body = self.request_body.clone();
        let trace = self.trace.clone();
        let start_time_unix_nano = self.start_time_unix_nano;
        let client = self.client.clone();
        let background_tasks = self.background_tasks.clone();

        // Extract response body from accumulated chunks synchronously
        // This must be done before spawning to avoid holding MutexGuard across await
        let response_body = {
            match accumulated.lock() {
                Ok(chunks) => {
                    let total_size: usize = chunks.iter().map(|b| b.len()).sum();
                    let mut response_bytes = Vec::with_capacity(total_size);
                    for chunk in chunks.iter() {
                        response_bytes.extend_from_slice(chunk);
                    }
                    String::from_utf8_lossy(&response_bytes).to_string()
                }
                Err(e) => {
                    eprintln!("Failed to lock accumulated chunks: {}", e);
                    return;
                }
            }
            // MutexGuard is automatically dropped here
        };

        // Spawn background task on the JoinSet for graceful shutdown tracking
        background_tasks.lock().unwrap().spawn(async move {
            if let Some(trace) = trace {
                match create_span_request(
                    request_body,
                    response_body,
                    trace.trace_id,
                    trace.span_id,
                    trace.span_ids_path,
                    start_time_unix_nano,
                    end_time_unix_nano,
                    trace.span_path,
                ) {
                    Ok(span_request) => {
                        if let Err(e) = send_trace_to_lmnr(
                            span_request,
                            client,
                            trace.project_api_key,
                            trace.laminar_url,
                        )
                        .await
                        {
                            eprintln!("Failed to send trace to LMNR: {}", e);
                        }
                    }
                    Err(e) => {
                        eprintln!("Failed to create span request: {}", e);
                    }
                }
            }
        });
    }
}

pub async fn handle(
    req: Request<Incoming>,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    target_url: String,
    state: SharedState,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let method = req.method().clone();
    let uri = req.uri();
    let path = uri.path();

    // Handle internal span context endpoint
    if path == "/lmnr-internal/span-context" && method == Method::POST {
        return handle_span_context(req, state).await;
    }

    if path == "/lmnr-internal/health" && method == Method::GET {
        return handle_health().await;
    }

    forward_request(req, client, target_url, state, background_tasks).await
}

async fn handle_health()
-> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    Ok(Response::builder()
        .status(StatusCode::OK)
        .body(
            Full::new(Bytes::from("{\"status\":\"ok\"}"))
                .map_err(|never| match never {})
                .boxed(),
        )
        .unwrap())
}
async fn handle_span_context(
    req: Request<Incoming>,
    state: SharedState,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let body_bytes = req.collect().await?.to_bytes();

    match serde_json::from_slice::<CurrentTraceAndLaminarContext>(&body_bytes) {
        Ok(trace) => {
            let mut state_guard = state.lock().unwrap();
            *state_guard = Some(trace.clone());
            drop(state_guard);

            let response = Response::builder()
                .status(StatusCode::OK)
                .body(
                    Full::new(Bytes::from("{\"status\":\"ok\"}"))
                        .map_err(|never| match never {})
                        .boxed(),
                )
                .unwrap();
            Ok(response)
        }
        Err(e) => {
            let error_msg = format!("{{\"error\":\"Invalid JSON: {}\"}}", e);
            let response = Response::builder()
                .status(StatusCode::BAD_REQUEST)
                .body(
                    Full::new(Bytes::from(error_msg))
                        .map_err(|never| match never {})
                        .boxed(),
                )
                .unwrap();
            Ok(response)
        }
    }
}

async fn forward_request(
    req: Request<Incoming>,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    target_url: String,
    state: SharedState,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let uri = req.uri();
    let path_and_query = uri.path_and_query().map(|x| x.as_str()).unwrap_or("/");
    let target_uri = format!("{}{}", target_url, path_and_query).parse().unwrap();

    let (mut parts, body) = req.into_parts();
    parts.uri = target_uri;

    // Collect request body
    let req_body_bytes = body.collect().await?.to_bytes();
    let req_body_str = String::from_utf8_lossy(&req_body_bytes).to_string();
    let new_body = Full::new(req_body_bytes.clone())
        .map_err(|never| match never {})
        .boxed();
    let proxy_req = Request::from_parts(parts, new_body);

    // Capture start time right before sending request
    let start_time_unix_nano = get_unix_nano();

    // Send request
    let resp = client.request(proxy_req).await?;
    let (parts, body) = resp.into_parts();

    // Get trace context
    let trace = state.lock().unwrap().clone();

    // Wrap the response body in a stream that captures chunks while forwarding them
    let body_stream = body.into_data_stream();
    let capturing_stream = SpanCapturingStream {
        inner: body_stream,
        accumulated: Arc::new(Mutex::new(Vec::new())),
        request_body: req_body_str,
        trace,
        start_time_unix_nano,
        client: client.clone(),
        background_tasks,
    };

    let streaming_body =
        StreamBody::new(capturing_stream.map(|result| result.map(|bytes| Frame::data(bytes))));

    Ok(Response::from_parts(parts, BodyExt::boxed(streaming_body)))
}
