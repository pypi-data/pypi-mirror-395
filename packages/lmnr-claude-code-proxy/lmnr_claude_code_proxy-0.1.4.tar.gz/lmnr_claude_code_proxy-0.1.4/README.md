# Laminar Claude Code proxy

This library contains a tiny Rust proxy for Claude Code that can accept
requests from claude-agent-sdk with trace id and span id in order
to associate spans from the proxy with the parent context.
