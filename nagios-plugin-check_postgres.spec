# TODO:
#	Add docs
#	Fix service file
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
URL:		https://bucardo.org/wiki/Check_postgres
BuildRequires:	perl-devel >= 1:5.8.0
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

cat > %{plugin}.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ $ARG1$
}

define service {
	use                     generic-service
	name                    template
	service_description     template
	register                0

	normal_check_interval   5
	retry_check_interval    1

	notification_interval   10

	check_command           %{plugin}
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{plugin}.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
