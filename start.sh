#!/usr/bin/env bash
set -e
if [ -f /etc/secrets/secrets.toml ]; then
	cp /etc/secrets/secrets.toml .streamlit/secrets.toml
fi
exec streamlit run AppC.py --server.port "$PORT" --server.address 0.0.0.0