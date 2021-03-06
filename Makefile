INSTALL_DIR := ./build

install: $(INSTALL_DIR)/bin/activate

pypi: install
	@. $(INSTALL_DIR)/bin/activate; python setup.py sdist bdist_wheel; twine upload dist/*

$(INSTALL_DIR)/bin/activate: requirements.txt requirements.txt.dev setup.py
	@test -d $(INSTALL_DIR) || virtualenv $(INSTALL_DIR)
	@. $(INSTALL_DIR)/bin/activate; pip install -U pip setuptools
	@. $(INSTALL_DIR)/bin/activate; pip install -U -r requirements.txt
	@. $(INSTALL_DIR)/bin/activate; pip install -U -r requirements.txt.dev
	@. $(INSTALL_DIR)/bin/activate; python setup.py develop
	@touch $(INSTALL_DIR)/bin/activate

shell: install
	@. $(INSTALL_DIR)/bin/activate; python

test: install
	@. $(INSTALL_DIR)/bin/activate; py.test tests --capture=no

clean:
	rm -rf dist/ build/

clean-all: clean
	rm -rf $(INSTALL_DIR)
