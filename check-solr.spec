%define name check-solr
%define version v0.1.1
%define release 1

Summary: Nagios/Icinga check for Solr.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: https://github.com/GeisingerHealthSystem/nagios-solr
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

%install
cd %{_sourcedir}
mkdir -p %{buildroot}/usr/lib64/nagios/plugins
cp check_solr %{buildroot}/usr/lib64/nagios/plugins
chmod +x %{buildroot}/usr/lib64/nagios/plugins

%files
/usr/lib64/nagios/plugins/check_solr

%changelog

