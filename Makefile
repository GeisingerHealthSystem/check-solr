# Small Makefile to build nagios-solr plugin RPM
# Requires:
# 	rpm-build, rpmdevtools
all: build

build: clean
	# Fetch source(s) with spectool
	# Use current dir so a user's home doesn't fill up
	rm -rf BUILD RPMS SOURCES SPECS SRPMS
	mkdir BUILD RPMS SOURCES SPECS SRPMS
	spectool -g -R check-solr.spec -C SOURCES
	# build just a binary for this (JAR files)
	# Use current dir for work dir
	rpmbuild --define "_topdir `pwd`" -bb check-solr.spec

list:
	# list rpm files
	rpm -qlp RPMS/x86_64/check-solr*.rpm

install: build
	sudo rpm -i RPMS/x86_64/check-solr*.rpm

uninstall:
	sudo rpm -e check-solr

clean:
	rm -rf BUILD RPMS SOURCES SPECS SRPMS
