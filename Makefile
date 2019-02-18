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
	$(call banner, "Install cloudmesh.cmd5")
	pip install -e . -U
	cms help

clean:
	$(call banner, "CLEAN")
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
	rm -rf .tox
	rm -f *.whl

######################################################################
# PYPI
######################################################################

twine:
	pip install -U twine

dist: clean
	@echo "######################################"
	@echo "# $(VERSION)"
	@echo "######################################"
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist
	python setup.py bdist_wheel

upload_test: twine dist
#	python setup.py	 sdist bdist bdist_wheel upload -r https://test.pypi.org/legacy/
	twine upload --repository pypitest dist/cloudmesh.$(package)-$(VERSION)-py2.py3-none-any.whl	dist/cloudmesh.$(package)-$(VERSION).tar.gz


# python -m pip install --index-url https://test.pypi.org/simple/ cloudmesh.cmd5

log:
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

register: dist
	@echo "######################################"
	@echo "# $(VERSION)"
	@echo "######################################"
	twine register dist/cloudmesh.$(package)-$(VERSION)-py2.py3-none-any.whl
	# twine register dist/cloudmesh.$(package)-$(VERSION).tar.gz


upload: dist
	twine upload dist/*

#
# GIT
#

tag:
	touch README.md
	git tag $(VERSION)
	git commit -a -m "$(VERSION)"
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

clean:
	-docker kill $$(docker ps -q)
	-docker rm $$(docker ps -a -q)
	-docker rmi $$(docker images -q)

push:
	docker push cloudmesh/cmd5:1.0

run:
	docker run cloudmesh/cmd5:1.0 /bin/sh -c "cd technologies; git pull; make"
