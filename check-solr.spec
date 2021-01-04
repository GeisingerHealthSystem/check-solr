# List of vars/macros:
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html
%define name check-solr
%define version 0.0.1
%define unmangled_version 0.0.1
%define release 1

Summary: Nagios/Icinga check for Solr.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: None
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: None
Url: https://github.com/GeisingerHealthSystem/nagios-solr

%description
Nagios/Icinga check for Solr.

%pre

%prep
%setup -n %{name}-%{version}

%install
mkdir -p %{buildroot}/usr/lib64/nagios/plugins
install -p -m 755 check_solr %{buildroot}/usr/lib64/nagios/plugins

%files
/usr/lib64/nagios/plugins/check_solr

%changelog

