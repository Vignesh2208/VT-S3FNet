%define version 4.7
%define lib_version @GENERIC_RELEASE@

%if 0%{?fedora} >= 17
%define with_kernel_modules_extra 1
%else
%define with_kernel_modules_extra 0
%endif

Name:		core
Summary:	Common Open Research Emulator for use with network namespaces
License:	BSD
Prefix:		/usr
Release:	1
Source:		core-%{version}.tar.gz
URL:		http://www.nrl.navy.mil/itd/ncs/products/core
Version:	%{version}
%description 
The Common Open Research Emulator provides Python modules and a GUI for
building virtual networks using Linux network namespace containers and bridging.

%package daemon
Summary:	Common Open Research Emulator daemon back-end
Group:		System Tools
Requires:	bash bridge-utils ebtables iproute libev python net-tools
%if %{with_kernel_modules_extra}
Requires: kernel-modules-extra procps-ng
%endif
BuildRequires:  make automake autoconf libev-devel python-devel bridge-utils ebtables iproute net-tools ImageMagick help2man 
%if %{with_kernel_modules_extra}
BuildRequires: procps-ng
%endif
Provides:	core-daemon
# python-sphinx
%description daemon
The Common Open Research Emulator provides Python modules for building virtual
networks using Linux network namespace containers and bridging. 

%package gui
Summary:	Common Open Research Emulator GUI front-end
Group:		System Tools
Requires:	tcl tk tkimg
BuildArch:	noarch
BuildRequires:  make automake autoconf
Provides:	core-gui
%description gui
The Common Open Research Emulator canvas-based Tcl/Tk GUI for easily drawing
virtual network topologies. 

%prep

%setup -q

%build

./bootstrap.sh
# not using --disable-gui/--disable-daemon, because RPM expects both to be
# installed by this build process
# assume Fedora, using systemd startup script
CFLAGS="-fno-strict-aliasing $CFLAGS" %configure --with-startup=systemd
make -j4

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post

%post daemon
# don't run EMANE with realtime option under Fedora
sed -i 's/emane_realtime = True/emane_realtime = False/' /etc/core/core.conf

%preun
#if [ "$1" = 0 ]; then
    #find %{_libdir}/python2.7/site-packages/core -name '*.pyc' -exec rm -f '{}' ';' 2> /dev/null
#fi

%postun

%files gui
%{_bindir}/core-gui
/usr/local/lib/core/addons/ipsecservice.tcl
/usr/local/lib/core/annotations.tcl
/usr/local/lib/core/api.tcl
/usr/local/lib/core/canvas.tcl
/usr/local/lib/core/cfgparse.tcl
/usr/local/lib/core/core-bsd-cleanup.sh
/usr/local/lib/core/core.tcl
/usr/local/lib/core/debug.tcl
/usr/local/lib/core/editor.tcl
/usr/local/lib/core/exceptions.tcl
/usr/local/lib/core/exec.tcl
/usr/local/lib/core/filemgmt.tcl
/usr/local/lib/core/gpgui.tcl
/usr/local/lib/core/graph_partitioning.tcl
/usr/local/lib/core/help.tcl
%{_datadir}/applications/core-gui.desktop
%{_datadir}/pixmaps/core-gui.xpm
%{_datadir}/%{name}/icons/normal/antenna.gif
%{_datadir}/%{name}/icons/normal/ap.gif
%{_datadir}/%{name}/icons/normal/core-icon.png
%{_datadir}/%{name}/icons/normal/core-icon.xbm
%{_datadir}/%{name}/icons/normal/core-logo-275x75.gif
%{_datadir}/%{name}/icons/normal/document-properties.gif
%{_datadir}/%{name}/icons/normal/gps-diagram.xbm
%{_datadir}/%{name}/icons/normal/host.gif
%{_datadir}/%{name}/icons/normal/hub.gif
%{_datadir}/%{name}/icons/normal/lanswitch.gif
%{_datadir}/%{name}/icons/normal/mdr.gif
%{_datadir}/%{name}/icons/normal/oval.gif
%{_datadir}/%{name}/icons/normal/pc.gif
%{_datadir}/%{name}/icons/normal/rj45.gif
%{_datadir}/%{name}/icons/normal/router_black.gif
%{_datadir}/%{name}/icons/normal/router.gif
%{_datadir}/%{name}/icons/normal/router_green.gif
%{_datadir}/%{name}/icons/normal/router_purple.gif
%{_datadir}/%{name}/icons/normal/router_red.gif
%{_datadir}/%{name}/icons/normal/router_yellow.gif
%{_datadir}/%{name}/icons/normal/simple.xbm
%{_datadir}/%{name}/icons/normal/text.gif
%{_datadir}/%{name}/icons/normal/thumb-unknown.gif
%{_datadir}/%{name}/icons/normal/tunnel.gif
%{_datadir}/%{name}/icons/normal/wlan.gif
%{_datadir}/%{name}/icons/normal/xen.gif
%{_datadir}/%{name}/icons/svg/ap.svg
%{_datadir}/%{name}/icons/svg/cel.svg
%{_datadir}/%{name}/icons/svg/hub.svg
%{_datadir}/%{name}/icons/svg/lanswitch.svg
%{_datadir}/%{name}/icons/svg/mdr.svg
%{_datadir}/%{name}/icons/svg/otr.svg
%{_datadir}/%{name}/icons/svg/rj45.svg
%{_datadir}/%{name}/icons/svg/router_black.svg
%{_datadir}/%{name}/icons/svg/router_green.svg
%{_datadir}/%{name}/icons/svg/router_purple.svg
%{_datadir}/%{name}/icons/svg/router_red.svg
%{_datadir}/%{name}/icons/svg/router.svg
%{_datadir}/%{name}/icons/svg/router_yellow.svg
%{_datadir}/%{name}/icons/svg/start.svg
%{_datadir}/%{name}/icons/svg/tunnel.svg
%{_datadir}/%{name}/icons/svg/vlan.svg
%{_datadir}/%{name}/icons/svg/xen.svg
%{_datadir}/%{name}/icons/tiny/ap.gif
%{_datadir}/%{name}/icons/tiny/arrow.down.gif
%{_datadir}/%{name}/icons/tiny/arrow.gif
%{_datadir}/%{name}/icons/tiny/arrow.up.gif
%{_datadir}/%{name}/icons/tiny/blank.gif
%{_datadir}/%{name}/icons/tiny/button.play.gif
%{_datadir}/%{name}/icons/tiny/button.stop.gif
%{_datadir}/%{name}/icons/tiny/cel.gif
%{_datadir}/%{name}/icons/tiny/delete.gif
%{_datadir}/%{name}/icons/tiny/document-new.gif
%{_datadir}/%{name}/icons/tiny/document-properties.gif
%{_datadir}/%{name}/icons/tiny/document-save.gif
%{_datadir}/%{name}/icons/tiny/edit-delete.gif
%{_datadir}/%{name}/icons/tiny/eraser.gif
%{_datadir}/%{name}/icons/tiny/fileopen.gif
%{_datadir}/%{name}/icons/tiny/folder.gif
%{_datadir}/%{name}/icons/tiny/host.gif
%{_datadir}/%{name}/icons/tiny/hub.gif
%{_datadir}/%{name}/icons/tiny/lanswitch.gif
%{_datadir}/%{name}/icons/tiny/link.gif
%{_datadir}/%{name}/icons/tiny/marker.gif
%{_datadir}/%{name}/icons/tiny/mdr.gif
%{_datadir}/%{name}/icons/tiny/mobility.gif
%{_datadir}/%{name}/icons/tiny/moboff.gif
%{_datadir}/%{name}/icons/tiny/observe.gif
%{_datadir}/%{name}/icons/tiny/oval.gif
%{_datadir}/%{name}/icons/tiny/pc.gif
%{_datadir}/%{name}/icons/tiny/ping.gif
%{_datadir}/%{name}/icons/tiny/plot.gif
%{_datadir}/%{name}/icons/tiny/rectangle.gif
%{_datadir}/%{name}/icons/tiny/rj45.gif
%{_datadir}/%{name}/icons/tiny/router_black.gif
%{_datadir}/%{name}/icons/tiny/router.gif
%{_datadir}/%{name}/icons/tiny/router_green.gif
%{_datadir}/%{name}/icons/tiny/router_purple.gif
%{_datadir}/%{name}/icons/tiny/router_red.gif
%{_datadir}/%{name}/icons/tiny/router_yellow.gif
%{_datadir}/%{name}/icons/tiny/run.gif
%{_datadir}/%{name}/icons/tiny/script_pause.gif
%{_datadir}/%{name}/icons/tiny/script_play.gif
%{_datadir}/%{name}/icons/tiny/script_stop.gif
%{_datadir}/%{name}/icons/tiny/select.gif
%{_datadir}/%{name}/icons/tiny/start.gif
%{_datadir}/%{name}/icons/tiny/stock_connect.gif
%{_datadir}/%{name}/icons/tiny/stock_disconnect.gif
%{_datadir}/%{name}/icons/tiny/stop.gif
%{_datadir}/%{name}/icons/tiny/text.gif
%{_datadir}/%{name}/icons/tiny/trace.gif
%{_datadir}/%{name}/icons/tiny/tunnel.gif
%{_datadir}/%{name}/icons/tiny/twonode.gif
%{_datadir}/%{name}/icons/tiny/view-refresh.gif
%{_datadir}/%{name}/icons/tiny/wlan.gif
%{_datadir}/%{name}/icons/tiny/xen.gif
/usr/local/lib/core/initgui.tcl
/usr/local/lib/core/ipv4.tcl
/usr/local/lib/core/ipv6.tcl
/usr/local/lib/core/linkcfg.tcl
/usr/local/lib/core/mobility.tcl
/usr/local/lib/core/nodecfg.tcl
/usr/local/lib/core/nodes.tcl
/usr/local/lib/core/ns2imunes.tcl
/usr/local/lib/core/plugins.tcl
/usr/local/lib/core/services.tcl
/usr/local/lib/core/tooltips.tcl
/usr/local/lib/core/topogen.tcl
/usr/local/lib/core/traffic.tcl
/usr/local/lib/core/util.tcl
/usr/local/lib/core/version.tcl
/usr/local/lib/core/widget.tcl
/usr/local/lib/core/wlanscript.tcl
/usr/local/lib/core/wlan.tcl
%{_datadir}/%{name}/examples/configs/sample10-kitchen-sink.imn
%{_datadir}/%{name}/examples/configs/sample1-bg.gif
%{_datadir}/%{name}/examples/configs/sample1.imn
%{_datadir}/%{name}/examples/configs/sample1.scen
%{_datadir}/%{name}/examples/configs/sample2-ssh.imn
%{_datadir}/%{name}/examples/configs/sample3-bgp.imn
%{_datadir}/%{name}/examples/configs/sample4-bg.jpg
%{_datadir}/%{name}/examples/configs/sample4-nrlsmf.imn
%{_datadir}/%{name}/examples/configs/sample4.scen
%{_datadir}/%{name}/examples/configs/sample5-mgen.imn
%{_datadir}/%{name}/examples/configs/sample6-emane-rfpipe.imn
%{_datadir}/%{name}/examples/configs/sample7-emane-ieee80211abg.imn
%{_datadir}/%{name}/examples/configs/sample8-ipsec-service.imn
%{_datadir}/%{name}/examples/configs/sample9-vpn.imn
%doc  %{_mandir}/man1/core-gui.1.gz

%files daemon
%config /etc/core/core.conf
%config /etc/core/perflogserver.conf
%config /etc/core/xen.conf
%{_datadir}/%{name}/examples/controlnet_updown
%{_datadir}/%{name}/examples/corens3/ns3lte.py*
%{_datadir}/%{name}/examples/corens3/ns3wifi.py*
%{_datadir}/%{name}/examples/corens3/ns3wifirandomwalk.py*
%{_datadir}/%{name}/examples/corens3/ns3wimax.py*
%{_datadir}/%{name}/examples/emanemodel2core.py*
%{_datadir}/%{name}/examples/findcore.py*
%{_datadir}/%{name}/examples/hooks/configuration_hook.sh
%{_datadir}/%{name}/examples/hooks/datacollect_hook.sh
%{_datadir}/%{name}/examples/hooks/perflogserver.py*
%{_datadir}/%{name}/examples/hooks/perflogstart.sh
%{_datadir}/%{name}/examples/hooks/perflogstop.sh
%{_datadir}/%{name}/examples/hooks/sessiondatacollect.sh
%{_datadir}/%{name}/examples/hooks/timesyncstart.sh
%{_datadir}/%{name}/examples/hooks/timesyncstop.sh
%{_datadir}/%{name}/examples/myservices/__init__.py*
%{_datadir}/%{name}/examples/myservices/README.txt
%{_datadir}/%{name}/examples/myservices/sample.py*
%{_datadir}/%{name}/examples/netns/basicrange.py*
%{_datadir}/%{name}/examples/netns/distributed.py*
%{_datadir}/%{name}/examples/netns/emane80211.py*
%{_datadir}/%{name}/examples/netns/howmanynodes.py*
%{_datadir}/%{name}/examples/netns/iperf-performance-chain.py*
%{_datadir}/%{name}/examples/netns/iperf-performance.sh
%{_datadir}/%{name}/examples/netns/ospfmanetmdrtest.py*
%{_datadir}/%{name}/examples/netns/switch.py*
%{_datadir}/%{name}/examples/netns/switchtest.py*
%{_datadir}/%{name}/examples/netns/twonodes.sh
%{_datadir}/%{name}/examples/netns/wlanemanetests.py*
%{_datadir}/%{name}/examples/netns/wlantest.py*
%{_datadir}/%{name}/examples/services/sampleFirewall
%{_datadir}/%{name}/examples/services/sampleIPsec
%{_datadir}/%{name}/examples/services/sampleVPNClient
%{_datadir}/%{name}/examples/services/sampleVPNServer
%{_datadir}/%{name}/examples/stopsession.py*
%doc  %{_mandir}/man1/core-cleanup.1.gz
%doc  %{_mandir}/man1/core-daemon.1.gz
%doc  %{_mandir}/man1/core-manage.1.gz
%doc  %{_mandir}/man1/coresendmsg.1.gz
%doc  %{_mandir}/man1/core-xen-cleanup.1.gz
%doc  %{_mandir}/man1/netns.1.gz
%doc  %{_mandir}/man1/vcmd.1.gz
%doc  %{_mandir}/man1/vnoded.1.gz
/etc/systemd/system/core-daemon.service
%{python_sitearch}/core_python_netns-1.0-py2.7.egg-info
%{python_sitearch}/netns.so
%{python_sitearch}/vcmd.so
%{python_sitelib}/core/addons/__init__.py*
%{python_sitelib}/core/api/coreapi.py*
%{python_sitelib}/core/api/data.py*
%{python_sitelib}/core/api/__init__.py*
%{python_sitelib}/core/broker.py*
%{python_sitelib}/core/bsd/__init__.py*
%{python_sitelib}/core/bsd/netgraph.py*
%{python_sitelib}/core/bsd/nodes.py*
%{python_sitelib}/core/bsd/vnet.py*
%{python_sitelib}/core/bsd/vnode.py*
%{python_sitelib}/core/conf.py*
%{python_sitelib}/core/constants.py*
%{python_sitelib}/core/coreobj.py*
%{python_sitelib}/core/emane/bypass.py*
%{python_sitelib}/core/emane/commeffect.py*
%{python_sitelib}/core/emane/emane.py*
%{python_sitelib}/core/emane/ieee80211abg.py*
%{python_sitelib}/core/emane/__init__.py*
%{python_sitelib}/core/emane/nodes.py*
%{python_sitelib}/core/emane/rfpipe.py*
%{python_sitelib}/core/emane/universal.py*
%{python_sitelib}/core/__init__.py*
%{python_sitelib}/core/location.py*
%{python_sitelib}/core/misc/event.py*
%{python_sitelib}/core/misc/__init__.py*
%{python_sitelib}/core/misc/ipaddr.py*
%{python_sitelib}/core/misc/LatLongUTMconversion.py*
%{python_sitelib}/core/misc/quagga.py*
%{python_sitelib}/core/misc/utils.py*
%{python_sitelib}/core/misc/utm.py*
%{python_sitelib}/core/misc/xmlutils.py*
%{python_sitelib}/core/mobility.py*
%{python_sitelib}/core/netns/__init__.py*
%{python_sitelib}/core/netns/nodes.py*
%{python_sitelib}/core/netns/vif.py*
%{python_sitelib}/core/netns/vnet.py*
%{python_sitelib}/core/netns/vnodeclient.py*
%{python_sitelib}/core/netns/vnode.py*
%{python_sitelib}/corens3/constants.py*
%{python_sitelib}/corens3/__init__.py*
%{python_sitelib}/corens3/obj.py*
%{python_sitelib}/corens3_python-4.7-py2.7.egg-info
%{python_sitelib}/core/phys/__init__.py*
%{python_sitelib}/core/phys/pnodes.py*
%{python_sitelib}/core/pycore.py*
%{python_sitelib}/core_python-4.7-py2.7.egg-info
%{python_sitelib}/core/sdt.py*
%{python_sitelib}/core/service.py*
%{python_sitelib}/core/services/bird.py*
%{python_sitelib}/core/services/__init__.py*
%{python_sitelib}/core/services/nrl.py*
%{python_sitelib}/core/services/quagga.py*
%{python_sitelib}/core/services/security.py*
%{python_sitelib}/core/services/ucarp.py*
%{python_sitelib}/core/services/utility.py*
%{python_sitelib}/core/services/xorp.py*
%{python_sitelib}/core/session.py*
%{python_sitelib}/core/xen/__init__.py*
%{python_sitelib}/core/xen/xenconfig.py*
%{python_sitelib}/core/xen/xen.py*
%{_sbindir}/core-cleanup
%{_sbindir}/core-daemon
%{_sbindir}/core-manage
%{_sbindir}/coresendmsg
%{_sbindir}/core-xen-cleanup
%{_sbindir}/netns
%{_sbindir}/vcmd
%{_sbindir}/vnoded

%changelog
* Wed Aug 6 2014 Jeff Ahrenholz <core-dev@pf.itd.nrl.navy.mil> - 4.7
- EMANE 0.9.1, asymmetric links, bugfixes
* Thu Aug 22 2013 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.6
- cored now core-daemon, core now core-gui for CORE 4.6 release
* Wed Apr 3 2013 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.5
- split into gui and daemon RPMs for CORE 4.5 release
* Tue Sep 4 2012 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.4
- update files list for CORE 4.4 release, removed info file
* Tue Feb 7 2012 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.3
- update files list for CORE 4.3 release, freshen dependencies
* Tue Aug 16 2011 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.2
- update for CORE 4.2 release; use dir variables, more arch independent
* Mon Dec 13 2010 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.1
- update for CORE 4.1 release; added calls to ldconfig and removal of pyc files
* Wed Aug 4 2010 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 4.0
- update for CORE 4.0 release for Python and network namespaces
* Thu Sep 10 2009 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 3.5
- update for CORE 3.5 release to include init script
* Fri May 29 2009 Jeff Ahrenholz <jeffrey.m.ahrenholz@boeing.com> - 3.4
- initial spec file for CORE 3.4 release

