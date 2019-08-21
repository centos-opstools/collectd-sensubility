
%global golang_namespace github.com/paramite

Name:           collectd-sensubility
Version:        0.1.4
Release:        1%{?dist}
Summary:        collectd-exec extension enabling collectd to bahave like sensu-client
License:        ASL 2.0
URL:            https://%{golang_namespace}/%{name}
Source0:        https://%{golang_namespace}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        example-config.conf

BuildRequires:  gcc
BuildRequires:  golang >= 1.2-7

BuildRequires:  golang(github.com/go-ini/ini)
BuildRequires:  golang(github.com/streadway/amqp)
BuildRequires:  golang(github.com/stretchr/testify)

%description
This project aims provide possibility to switch from Sensu based availability monitoring solution to monitoring solution based on collectd with AMQP-1.0 messaging bus.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p src/github.com/paramite
ln -s ../../../ src/github.com/paramite/collectd-sensubility
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
* Wed Jul 21 2019 Martin Mágr <mmagr@redhat.com> - 0.1.4-1
- Unbundled dependencies

* Fri Jul 19 2019 Martin Mágr <mmagr@redhat.com> - 0.1.1-1
- Initial build
