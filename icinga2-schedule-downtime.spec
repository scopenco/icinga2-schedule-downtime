#
Name:          icinga2-schedule-downtime
Version:       0.1
Release:       1%{?dist}
Summary:       Script for running Host/Services schedule downtime in command line for Icinga2
AutoReqProv:   no
BuildArch:     noarch

Group:         Applications/System
License:       GPL
Source0:        icinga2-schedule-downtime.py
Source1:        icinga2-schedule-downtime.conf.example

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: python

%description
Script for running Host/Services schedule downtime in command line for Icinga2

%prep
cp %{SOURCE0} %{SOURCE1} .

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -pm 750 %{SOURCE0} \
                $RPM_BUILD_ROOT/%{_bindir}/icinga2-schedule-downtime.py

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
install -pm 750 %{SOURCE1} \
                $RPM_BUILD_ROOT/%{_sysconfdir}/icinga2-schedule-downtime.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755, root, root, -)
%{_bindir}/icinga2-schedule-downtime.py
%config(noreplace) %{_sysconfdir}/icinga2-schedule-downtime.conf

%changelog
