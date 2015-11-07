# TODO:
#	Add docs
#	Fix service file
# - check_postgres.cfg - add working sample!
%define		plugin	check_postgres
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin to check postgresql
Summary(pl.UTF-8):	Wtyczka Nagiosa sprawdzająca Postgresql
Name:		nagios-plugin-%{plugin}
Version:	2.22.0
Release:	1
License:	BSD
Group:		Networking
Source0:	http://bucardo.org/downloads/check_postgres-%{version}.tar.gz
# Source0-md5:	0ac4a8bae7b633fbfacdf58be5a1975f
Source1:	%{plugin}.cfg
URL:		https://bucardo.org/wiki/Check_postgres
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.654
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check Postgresql

%description -l pl.UTF-8
Wtyczka Nagiosa sprawdzająca Postgresql

%prep
%setup -q -n %{plugin}-%{version}
cp %{plugin}.pl %{plugin}

%{__sed} -i -e 's,/usr/local/nagios/perl/lib,%{plugindir},' %{plugin}
%{__sed} -i -e '1s,^#!.*perl,#!%{__perl},' %{plugin}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
