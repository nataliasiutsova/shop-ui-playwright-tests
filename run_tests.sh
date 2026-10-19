#!/bin/bash
set -e

echo "▶ Cleaning old results..."
rm -rf allure-results
mkdir -p allure-results

# Restore history for Trend (from previous report)
if [ -d "allure-report/history" ]; then
    echo "▶ Restoring history from previous report..."
    cp -r allure-report/history allure-results/history
else
    echo "▶ No previous report — starting fresh history"
fi

echo "▶ Stage 1: Smoke tests (sequential)"
pytest -m smoke -v --alluredir=allure-results

echo "▶ Stage 2: Regression + E2E (4 workers)"
pytest -m "(regression or e2e) and not smoke" -v -n 4 --dist loadfile --alluredir=allure-results

echo "▶ Generating Allure report..."
allure generate allure-results -o allure-report --clean

echo "▶ Opening report..."
allure open allure-report