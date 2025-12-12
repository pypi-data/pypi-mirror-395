# Benchmark commands
BASE_URL ?= https://benchmark-dr-s-2799835ad04b501a95044223ae72ced7.staging.langgraph.app 
RAMP_START ?= 40
RAMP_END ?= 1000
RAMP_MULTIPLIER ?= 2
WAIT_SECONDS ?= 60
CLEAR_BETWEEN_STEPS ?= true
CLEAR_DELAY_SECONDS ?= 5
DATA_SIZE ?= 1000
DELAY ?= 0
EXPAND ?= 1
STEPS ?= 100

benchmark-burst:
	make benchmark-reset
	k6 run burst.js

benchmark-ramp:
	make benchmark-reset
	k6 run --out json=raw_data_$(shell date +%Y-%m-%dT%H-%M-%S).json --system-tags=[] ramp.js

benchmark-capacity:
	rm -f capacity_summary_t*.json capacity_raw_t*.json capacity_histogram_*.json
	npm install
	BASE_URL=$(BASE_URL) \
	RAMP_START=$(RAMP_START) \
	RAMP_END=$(RAMP_END) \
	RAMP_MULTIPLIER=$(RAMP_MULTIPLIER) \
	WAIT_SECONDS=$(WAIT_SECONDS) \
	CLEAR_BETWEEN_STEPS=$(CLEAR_BETWEEN_STEPS) \
	CLEAR_DELAY_SECONDS=$(CLEAR_DELAY_SECONDS) \
	DATA_SIZE=$(DATA_SIZE) \
	DELAY=$(DELAY) \
	EXPAND=$(EXPAND) \
	STEPS=$(STEPS) \
	node capacity_runner.mjs

benchmark-charts:
	npm install
	node graphs.js $(shell ls -t raw_data_*.json | head -1) true

benchmark-reset:
	node clean.js

benchmark-new-revision:
	node update-revision.js

benchmark-clean:
	rm -f results_*.json summary_*.json raw_data_*.json *_chart_*.png

benchmark-clean-charts:
	rm -f *_chart_*.png
