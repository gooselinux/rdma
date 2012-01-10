#  Copyright (c) 2008 Red Hat, Inc.

#  There is no URL or upstream source entry as this package constitutes
#  upstream for itself.

Summary: Infiniband/iWARP Kernel Module Initializer
Name: rdma
Version: 1.0
Release: 9%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: rdma.conf
Source1: rdma.init
Source2: rdma.fixup-mtrr.awk
Source3: rdma.90-rdma.rules
Source4: rdma.ifup-ib
Source5: rdma.nfs-rdma.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires(post): chkconfig
Requires(preun): chkconfig
Requires: udev >= 145
%description 
User space initialization scripts for the kernel InfiniBand/iWARP drivers

%prep

%build

%install
rm -rf ${RPM_BUILD_ROOT}
install -d ${RPM_BUILD_ROOT}%{_initrddir}
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/network-scripts

install -m 0644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
install -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/fixup-mtrr.awk
install -m 0644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d/90-%{name}.rules
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -m 0755 %{SOURCE5} %{buildroot}%{_initrddir}/nfs-rdma

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add %{name} 
fi

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/%{name}/fixup-mtrr.awk
%{_initrddir}/%{name}
%{_initrddir}/nfs-rdma
%{_sysconfdir}/udev/rules.d/90-%{name}.rules
%{_sysconfdir}/sysconfig/network-scripts/ifup-ib

%changelog
* Tue Aug 17 2010 Doug Ledford <dledford@redhat.com> - 1.0-9
- Minor tweak to rdma init script to do the udevadm trigger command in two
  seperate calls since we can no longer match on the same item twice and
  have the command succeed for both match types.
- Resolves: bz612234

* Wed Aug 04 2010 Doug Ledford <dledford@redhat.com> - 1.0-8
- Update udev rules syntax to eliminate warnings emitted via syslog (bz603264)
- Add new init script for starting/stopping nfs over rdma support
- Require that the nfs-rdma service be down before stopping the rdma
  service (bz613437)
- Change ifup-ib to properly account for the fact that the [ test program
  does not process tests in order and fail immediately on first failing
  test, resulting in error messages due to unquoted environment variables
  that don't need quoting in the second test due to the fact that the
  first test guarantees they exist.  Or that's how things should be, but
  they aren't, so rewrite tests to accommodate this fact. (bz612284)
- Use ip instead of ifconfig as ifconfig knows it doesn't handle infinband
  hardware addresses properly (even though we don't care, we aren't using
  it for that) and prints out copious warning messages (bz613086)
- Related: bz612284, bz613086

* Wed May 26 2010 Doug Ledford <dledford@redhat.com> - 1.0-7
- Require a version of udev that's known to contain udevadm and support
  usage of udevadm trigger and udevadm settle
- Update rdma.init to use the proper udev commands
- Resolves: bz586594

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0-6
- Tweak init script for LSB compliance
- Tweak ifup-ib script to work properly with bonded slaves that need their
  MTU set
- Tweak ifup-ib script to properly change connected mode either on or off
  instead of only setting it on but not turning it off if the setting changes

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-3
- Add the ifup-ib script so we support connected mode on ib interfaces

* Mon Jun 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-2
- Attempt to use --subsystem-match=infiniband in the rdma init script use
  of udevtrigger so we don't trigger the whole system
- Add a requirement to stop opensm to the init script

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.0-1
- Create an initial package for Fedora review

