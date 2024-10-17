#!make
-include .env
VAL := $(shell date +"%Y-%m-%d")

run:
	@echo "run script"
	chmod +x ./shell/run_scripts.sh
	./shell/run_scripts.sh > "${STDOUT_LOG_PATH}_$(VAL).log" 2>&1