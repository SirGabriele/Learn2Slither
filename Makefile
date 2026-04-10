# Paths names
REQUIREMENTS_FILE = requirements.txt
VENV_DIR = venv

# Executable
PYTHON_VERSION = python3.13
VENV_EXEC = $(VENV_DIR)/bin/$(PYTHON_VERSION)

# Rules
all: venv

venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		$(PYTHON_VERSION) -m venv $(VENV_DIR); \
		$(VENV_EXEC) -m pip install --upgrade pip; \
		$(VENV_EXEC) -m pip install -r $(REQUIREMENTS_FILE); \
	fi

fclean:
	rm -rf __pycache__ $(VENV_DIR)

re: fclean all

.PHONY: all venv fclean re
