all: test

uninstall:
		pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
		rm -rf build dist
		find . -name '*.pyc' -exec rm \{\} \;

deps:
		pip install --upgrade pip twine wheel

install: deps
		@# Install OpenFisca-Mali for development.
		@# `make install` installs the editable version of OpenFisca-Mali.
		@# This allows contributors to test as they code.
		pip install --editable .[dev] --upgrade
		pip install openfisca-core

build: clean deps
		@# Install OpenFisca-Mali for deployment and publishing.
		@# `make build` allows us to be be sure tests are run against the packaged version
		@# of OpenFisca-Mali, the same we put in the hands of users and reusers.
		python setup.py bdist_wheel
		find dist -name "*.whl" -exec pip install --upgrade {}[dev] \;
		pip install openfisca-core

check-syntax-errors:
		python -m compileall -q .

format-style:
		@# Do not analyse .gitignored files.
		@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
		autopep8 `git ls-files | grep "\.py$$"`

check-style:
		@# Do not analyse .gitignored files.
		@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
		flake8 `git ls-files | grep "\.py$$"`

test: clean check-syntax-errors check-style
		@# Launch tests from openfisca_mali/tests directory (and not .) because TaxBenefitSystem must be initialized
		@# before parsing source files containing formulas.
		pytest
		openfisca test --country-package openfisca_mali openfisca_mali/tests
