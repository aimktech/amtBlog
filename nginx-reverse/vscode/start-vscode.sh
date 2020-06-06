#!/bin/bash
# script to launch the VSCode server

VSCODE_DIR=${HOME}/vscode

# change this password
export PASSWORD="Changem3"

# launch VSCode
nohup ${VSCODE_DIR}/bin/code-server \
	--auth password \
	--disable-telemetry \
	--bind-addr 10.195.25.166:8080 \
	--user-data-dir ${VSCODE_DIR}/data-dir \
	--cert ${VSCODE_DIR}/certs/vscode.cert \
	--cert-key ${VSCODE_DIR}/certs/vscode.key \
	${HOME}/sources >${VSCODE_DIR}/logs/vscode.log 2>&1 &
