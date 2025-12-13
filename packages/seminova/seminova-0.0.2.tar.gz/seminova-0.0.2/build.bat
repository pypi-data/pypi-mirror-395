@echo off
maturin build --release --features python && pip install target/wheels/seminova-0.1.0-cp312-cp312-win_amd64.whl --force-reinstall
