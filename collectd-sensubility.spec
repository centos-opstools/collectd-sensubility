
%global golang_namespace github.com/infrawatch
%undefine _debugsource_packages

Name:           collectd-sensubility
Version:        0.1.8
Release:        2%{?dist}
Summary:        collectd-exec extension enabling collectd to bahave like sensu-client
License:        ASL 2.0
URL:            https://%{golang_namespace}/%{name}
Source0:        https://%{golang_namespace}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        example-config.conf

BuildRequires:  gcc
BuildRequires:  golang >= 1.2-7
BuildRequires:  golang(github.com/infrawatch/apputils) >= 0.1

Requires:       util-linux

%description
This project aims provide possibility to switch from Sensu based availability monitoring solution to monitoring solution based on collectd with AMQP-1.0 messaging bus.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p src/github.com/infrawatch
ln -s ../../../ src/github.com/infrawatch/collectd-sensubility
export GOPATH=$(pwd):%{gopath}
go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x -o collectd-sensubility main/main.go

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 ./collectd-sensubility %{buildroot}%{_bindir}/collectd-sensubility
chmod a+x %{buildroot}%{_bindir}/collectd-sensubility
install -d %{buildroot}%{_sysconfdir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/collectd-sensubility.conf

%files
%doc README.md
%license LICENSE
%{_bindir}/collectd-sensubility
%{_sysconfdir}/collectd-sensubility.conf

%changelog
* Tue Oct 13 2020 Martin Magr <mmagr@redhat.com> - 0.1.8-2
- Rebuild with fixed apputils

* Tue Sep 02 2020 Martin Mágr <mmagr@redhat.com> - 0.1.8-1
- Updated to latest upstream release

* Tue May 12 2020 Martin Mágr <mmagr@redhat.com> - 0.1.5-1
- Fix config issue (rhbz#1827023)

* Wed Aug 21 2019 Martin Mágr <mmagr@redhat.com> - 0.1.4-1
- Unbundled dependencies

* Fri Jul 19 2019 Martin Mágr <mmagr@redhat.com> - 0.1.1-1
- Initial build
