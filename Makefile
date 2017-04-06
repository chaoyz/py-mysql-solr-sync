init:
    pip install -r requirements.txt

test:
    py.test test_sample.py

.PHONY: init test