###############################################################################
# Copyright (c) 2021 Gennady Trafimenkov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

default:
	false

prep:
	$(MAKE) format
	$(MAKE) unittests-coverage

format:
	python -m black .
	terraform fmt extras/terraform/ro-iam-policy

lint:
	python -m pylint awsrev revizor.py

unittests:
	python -m unittest

unittests-coverage:
	-coverage run -m unittest
	coverage report -m --include=awsrev/*,revizor.py
	coverage html --include=awsrev/*,revizor.py
	@echo
	@echo "------------------------------------------------------------------------------"
	@echo "html report: file://$$(pwd)/htmlcov/index.html"
	@echo "------------------------------------------------------------------------------"

check:
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) unittests
