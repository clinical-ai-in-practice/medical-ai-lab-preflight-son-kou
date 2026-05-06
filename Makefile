.PHONY: bootstrap fetch-sample inspect-data visualize smoke-train error-analysis model-swap \
        pack-report challenge-plan adapt-pipeline translation-memo \
        run-day1 run-day2 app dashboard test check preflight help

help:
	@echo "Medical AI + Agentic Coding Lab — available commands"
	@echo ""
	@echo "Day 1 stages:"
	@echo "  make bootstrap          Stage 00 — set up environment and output folders"
	@echo "  make fetch-sample       Stage 01 — fetch the imaging teaching pack"
	@echo "  make inspect-data       Stage 01 — inspect the fetched teaching pack"
	@echo "  make visualize          Stage 02 — load data and produce overlay figures"
	@echo "  make smoke-train        Stage 03 — run baseline model, write metrics"
	@echo "  make error-analysis     Stage 04 — identify best and worst predictions"
	@echo "  make model-swap         Stage 05 — make one controlled change, compare"
	@echo "  make pack-report        Stage 06 — assemble Day 1 summary report"
	@echo ""
	@echo "Day 2 stages:"
	@echo "  make challenge-plan     Stage 07 — write plan for the harder challenge"
	@echo "  make adapt-pipeline     Stage 08 — implement the planned changes"
	@echo "  make translation-memo   Stage 09 — write clinical translation memo"
	@echo ""
	@echo "Sequences:"
	@echo "  make run-day1           Stages 00–06 in order"
	@echo "  make run-day2           Stages 07–09 in order"
	@echo ""
	@echo "Other:"
	@echo "  make dashboard          Open mission dashboard (primary student interface)"
	@echo "  make app                Alias for make dashboard"
	@echo "  make preflight          Structural checks — no data required (run first)"
	@echo "  make test               Run full autograding tests (same as CI)"
	@echo "  make check              Alias for make test"

bootstrap:
	python scripts/bootstrap.py

fetch-sample:
	python scripts/fetch_data.py

inspect-data:
	python scripts/inspect_data.py

visualize:
	python scripts/visualize_sample.py

smoke-train:
	python scripts/run_train.py

error-analysis:
	python scripts/error_analysis.py

model-swap:
	python scripts/model_swap.py

pack-report:
	python scripts/pack_report.py

challenge-plan:
	python scripts/challenge_plan.py

adapt-pipeline:
	python scripts/adapt_pipeline.py

translation-memo:
	python scripts/translation_memo.py

run-day1: bootstrap fetch-sample visualize smoke-train error-analysis model-swap pack-report

run-day2: challenge-plan adapt-pipeline translation-memo

app:
	python -m streamlit run app/streamlit_app.py

# Alias — identical to make app
dashboard:
	python -m streamlit run app/streamlit_app.py

# Run the full visible autograding test suite (same command CI uses)
test:
	pytest -q tests/

# Alias — identical to make test
check:
	pytest -q tests/

# Structural preflight checks — no data required
# Runs bootstrap and checks that all scaffolding is intact
preflight:
	python scripts/bootstrap.py
	pytest -q tests/test_preflight.py tests/test_scripts_exist.py
