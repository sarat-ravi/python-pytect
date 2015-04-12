# Targets
# -------------------------------
.PHONY: default
default: install

.PHONY: clean
clean: uninstall

.PHONY: test
test: test_yalefaces
# -------------------------------

.PHONY: install
install:
	sudo pip install -e .

.PHONY: uninstall
uninstall:
	sudo pip uninstall pytect

.PHONY: test_yalefaces
test_yalefaces:
	cd tests; ./test.py

