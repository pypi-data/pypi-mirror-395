mod error;
mod utils;

use std::collections::HashMap;

pub use error::SpanError;
use serde_json::Value;

use crate::{
    anthropic::{
        request::{ContentBlock, PostMessagesRequest, ToolResultContent},
        response::MessageResponse,
    },
    proto::{
        opentelemetry_collector_trace_v1::ExportTraceServiceRequest,
        opentelemetry_proto_common_v1::KeyValue as KeyValueInner,
        opentelemetry_proto_trace_v1::{
            ResourceSpans, ScopeSpans, Span as ProtoSpan, Status, span::SpanKind,
            status::StatusCode,
        },
    },
    spans::utils::convert_attributes_to_proto_key_value,
};

use utils::{
    bytes_to_uuid_like_string, extract_attributes, generate_span_id, parse_span_id,
    parse_sse_events, parse_trace_id,
};

const MILLIS_IN_NANO: u64 = 1_000_000;

pub fn create_span_request(
    request_body: String,
    response_body: String,
    trace_id: String,
    parent_span_id: String,
    span_ids_path: Vec<String>,
    start_time_unix_nano: u64,
    end_time_unix_nano: u64,
    span_path: Vec<String>,
) -> Result<ExportTraceServiceRequest, SpanError> {
    let input: PostMessagesRequest =
        serde_json::from_str(&request_body).map_err(|e| SpanError::JsonParseError {
            context: format!("request body: {}", request_body),
            error: e.to_string(),
        })?;

    let output = if input.stream {
        let events = parse_sse_events(&response_body);
        MessageResponse::from_stream_events(events)
    } else {
        let message_response: MessageResponse =
            serde_json::from_str(&response_body).map_err(|e| SpanError::JsonParseError {
                context: "response body".to_string(),
                error: e.to_string(),
            })?;
        message_response
    };

    // Parse trace_id and span_id from UUID format to bytes
    let trace_id_bytes = parse_trace_id(&trace_id)?;
    let parent_span_id_bytes = parse_span_id(&parent_span_id)?;
    let span_id_bytes = generate_span_id();

    // Validate lengths (trace_id: 16 bytes, span_id: 8 bytes)
    if trace_id_bytes.len() != 16 {
        return Err(SpanError::InvalidBytesLength {
            expected: 16,
            got: trace_id_bytes.len(),
        });
    }
    if parent_span_id_bytes.len() != 8 {
        return Err(SpanError::InvalidBytesLength {
            expected: 8,
            got: parent_span_id_bytes.len(),
        });
    }

    let span_id_string = bytes_to_uuid_like_string(&span_id_bytes)?;
    let ids_path = span_ids_path
        .clone()
        .into_iter()
        .chain(vec![span_id_string])
        .collect::<Vec<_>>();

    let mut tool_result_spans = Vec::new();
    if input.messages.len() > 1 {
        let last_message = input.messages.last().unwrap();
        let second_last_message = input.messages.get(input.messages.len() - 2).unwrap();
        if last_message.is_tool_result() && second_last_message.is_tool_use() {
            let tool_results = last_message.content.tool_results();
            let tool_uses = second_last_message.content.tool_uses();
            for (tool_use_id, tool_result) in tool_results.iter() {
                if let Some(tool_use) = tool_uses.get(tool_use_id) {
                    match create_tool_result_span(
                        &trace_id_bytes,
                        &parent_span_id_bytes,
                        &ids_path,
                        &span_path,
                        start_time_unix_nano,
                        tool_use,
                        tool_result,
                    ) {
                        Ok(tool_result_span) => tool_result_spans.push(tool_result_span),
                        Err(_) => {
                            // eprintln!("Failed to create tool result span");
                        }
                    }
                }
            }
        }
    }

    let mut attributes = extract_attributes(input, output);
    attributes.insert(
        "lmnr.span.ids_path".to_string(),
        Value::Array(ids_path.into_iter().map(|s| Value::String(s)).collect()),
    );
    attributes.insert(
        "lmnr.span.path".to_string(),
        Value::Array(span_path.into_iter().map(|s| Value::String(s)).collect()),
    );

    // Convert attributes HashMap to proto KeyValue format
    let proto_attributes: Vec<KeyValueInner> = convert_attributes_to_proto_key_value(attributes)?;

    // Create the proto Span
    let proto_span = ProtoSpan {
        trace_id: trace_id_bytes,
        span_id: span_id_bytes,
        name: "anthropic.messages".to_string(),
        attributes: proto_attributes,
        // Leave other fields as default/empty for now
        trace_state: String::new(),
        parent_span_id: parent_span_id_bytes,
        flags: 1,                      // TraceFlags::SAMPLED
        kind: SpanKind::Client as i32, // Client
        start_time_unix_nano,
        end_time_unix_nano,
        events: Vec::new(),
        dropped_attributes_count: 0,
        dropped_events_count: 0,
        links: Vec::new(),
        dropped_links_count: 0,
        status: Some(Status {
            code: StatusCode::Ok as i32,
            message: String::new(),
        }),
    };

    // Wrap in ScopeSpans
    let scope_spans = ScopeSpans {
        scope: None,
        spans: vec![proto_span]
            .into_iter()
            .chain(tool_result_spans.into_iter())
            .collect(),
        schema_url: String::new(),
    };

    // Wrap in ResourceSpans
    let resource_spans = ResourceSpans {
        resource: None,
        scope_spans: vec![scope_spans],
        schema_url: String::new(),
    };

    // Create the ExportTraceServiceRequest
    let export_request = ExportTraceServiceRequest {
        resource_spans: vec![resource_spans],
    };

    Ok(export_request)
}

fn create_tool_result_span(
    trace_id_bytes: &Vec<u8>,
    parent_span_id_bytes: &Vec<u8>,
    span_ids_path: &Vec<String>,
    span_path: &Vec<String>,
    start_time_unix_nano: u64,
    tool_use: &ContentBlock,
    tool_result: &ContentBlock,
) -> Result<ProtoSpan, SpanError> {
    let span_id_bytes = generate_span_id();
    if !matches!(tool_use, ContentBlock::ToolUse { .. }) {
        return Err(SpanError::InvalidContentBlock {
            context: "tool use".to_string(),
            error: "tool use is not a tool use content block".to_string(),
        });
    }
    if !matches!(tool_result, ContentBlock::ToolResult { .. }) {
        return Err(SpanError::InvalidContentBlock {
            context: "tool result".to_string(),
            error: "tool result is not a tool result content block".to_string(),
        });
    }

    let mut attributes = HashMap::new();
    attributes.insert(
        "lmnr.span.ids_path".to_string(),
        Value::Array(
            span_ids_path
                .into_iter()
                .map(|s| Value::String(s.clone()))
                .collect(),
        ),
    );
    attributes.insert(
        "lmnr.span.path".to_string(),
        Value::Array(
            span_path
                .into_iter()
                .map(|s| Value::String(s.clone()))
                .collect(),
        ),
    );
    attributes.insert(
        "lmnr.span.type".to_string(),
        Value::String("TOOL".to_string()),
    );

    let span_name;
    match tool_use {
        ContentBlock::ToolUse { name, input, .. } => {
            span_name = name.as_str();
            attributes.insert(
                "lmnr.span.input".to_string(),
                Value::String(input.to_string()),
            );
        }
        _ => unreachable!(),
    }
    match tool_result {
        ContentBlock::ToolResult { content, .. } => {
            if let Some(content) = content {
                let output_string = match content {
                    ToolResultContent::String(s) => s.to_string(),
                    ToolResultContent::Blocks(blocks) => serde_json::to_string(&blocks).unwrap(),
                };
                attributes.insert("lmnr.span.output".to_string(), Value::String(output_string));
            }
        }
        _ => unreachable!(),
    }

    Ok(ProtoSpan {
        trace_id: trace_id_bytes.clone(),
        span_id: span_id_bytes,
        name: span_name.to_string(),
        attributes: convert_attributes_to_proto_key_value(attributes)?,
        // Leave other fields as default/empty for now
        trace_state: String::new(),
        parent_span_id: parent_span_id_bytes.clone(),
        flags: 1,                      // TraceFlags::SAMPLED
        kind: SpanKind::Client as i32, // Client
        // Span of duration 0, 1 millisecond before the span that reports the tool result
        start_time_unix_nano: start_time_unix_nano - MILLIS_IN_NANO,
        end_time_unix_nano: start_time_unix_nano - MILLIS_IN_NANO,
        events: Vec::new(),
        dropped_attributes_count: 0,
        dropped_events_count: 0,
        links: Vec::new(),
        dropped_links_count: 0,
        status: Some(Status {
            code: StatusCode::Ok as i32,
            message: String::new(),
        }),
    })
}
