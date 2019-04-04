package=cmd5
UNAME=$(shell uname)
VERSION=`head -1 VERSION`

define banner
	@echo
	@echo "###################################"
	@echo $(1)
	@echo "###################################"
endef

source: 
	cd ../cloudmesh.common; make source
	$(call banner, "Install cloudmesh-cmd5")
	pip install -e . -U
	cms help

clean:
	$(call banner, "CLEAN")
	rm -rf dist
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
	rm -rf .tox
	rm -f *.whl

######################################################################
# PYPI
######################################################################


twine:
	pip install -U twine

dist:
	python setup.py sdist bdist_wheel
	twine check dist/*

build: clean
	$(call banner, "bbuild")
	bump2version --allow-dirty build
	python setup.py sdist bdist_wheel
	# git push origin master --tags
	twine check dist/*
	twine upload --repository testpypi  dist/*

patch: clean
	$(call banner, "patch")
	bump2version patch --allow-dirty
	@cat VERSION
	@echo

minor: clean
	$(call banner, "minor")
	bump2version minor --allow-dirty
	@cat VERSION
	@echo

release: clean
	$(call banner, "release")
	@ bump2version release --tag --allow-dirty
	@cat VERSION
	@echo
	python setup.py sdist bdist_wheel
	git push origin master --tags
	twine check dist/*
	twine upload --repository testpypi https://test.pypi.org/legacy/ dist/*
	@bump2version --new-version "$(VERSION)-dev0" part --allow-dirty
	@bump2version patch --allow-dirty
	$(call banner, "new-version")
	@cat VERSION
	@echo

dev:
	bump2version --new-version "$(VERSION)-dev0" part --allow-dirty
	bump2version patch --allow-dirty
	@cat VERSION
	@echo

reset:
	bump2version --new-version "4.0.0-dev0" part --allow-dirty

upload:
	twine check dist/*
	twine upload dist/*

pip: patch
	pip install --index-url https://test.pypi.org/simple/ \
	    --extra-index-url https://pypi.org/simple cloudmesh-$(package)

log:
	$(call banner, log)
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

######################################################################
# DOCKER
######################################################################

image:
	docker build -t cloudmesh/cmd5:1.0 . 

shell:
	docker run --rm -it cloudmesh/cmd5:1.0  /bin/bash 

cms:
	docker run --rm -it cloudmesh/cmd5:1.0

dockerclean:
	-docker kill $$(docker ps -q)
	-docker rm $$(docker ps -a -q)
	-docker rmi $$(docker images -q)

push:
	docker push cloudmesh/cmd5:1.0

run:
	docker run cloudmesh/cmd5:1.0 /bin/sh -c "cd technologies; git pull; make"
