%define		svnrev	4645
%define		rel		0.1
Summary:	Varnish VCL rules: Security.VCL
Name:		varnish-vcl-security.vcl
Version:	0.1
Release:	0.%{svnrev}.%{rel}
License:	GPL v2
Group:		Networking/Daemons/HTTP
# revno=4645
# svn co http://varnish-cache.org/svn/trunk/varnish-tools/security.vcl${revno:+@$revno} security.vcl
# tar -cjf security.vcl-$(svnversion security.vcl).tar.bz2 --exclude=.svn security.vcl
# ../dropin security.vcl-$(svnversion security.vcl).tar.bz2
Source0:	security.vcl-%{svnrev}.tar.bz2
# Source0-md5:	a8c85b4adb9377977d70d4ac1d30086a
URL:		http://www.varnish-cache.org/browser/trunk/varnish-tools/security.vcl
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/varnish/security

%description
Security.VCL aims to provide:
- A standardized framework for security-related filters
- Several core rule-sets
- A tool to generate Security.VCL modules from mod_security rules.
- A limited set of default 'handlers', for instance CGI scripts to
  call upon when Bad Stuff happens.

This is done mainly by using clever VCL, and with as little impact on
normal operation as possible. The incident handlers are mainly
CGI-like scripts on a backend.

%prep
%setup -q -n security.vcl

# we have vcl syntax now
grep -r syntax=c . -l | xargs sed -i -e 's,syntax=c,syntax=vcl,'

%build
%{__make} -C vcl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a vcl/* $RPM_BUILD_ROOT%{_sysconfdir}

# not needed runtime
rm $RPM_BUILD_ROOT%{_sysconfdir}/{Makefile,VARIABLES}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{_sysconfdir}
%dir %{_sysconfdir}/breach
%dir %{_sysconfdir}/build
%dir %{_sysconfdir}/modules
%{_sysconfdir}/main.vcl
%{_sysconfdir}/breach/*.vcl
%{_sysconfdir}/build/*.vcl
%{_sysconfdir}/modules/*.vcl
