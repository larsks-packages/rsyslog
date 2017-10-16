%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/rsyslog

%global want_hiredis 0
%global want_mongodb 0

#due to multiple failures of extensive testbench on various archs
#and module requirements of certain tests need to have it disabled,
#tests execution possible locally on properly set up workstation
%global want_testbench 0

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.29.0
Release: 4%{?dist}
License: (GPLv3+ and ASL 2.0)
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: http://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{version}.tar.gz
Source2: rsyslog.conf

Patch0001: 0001-do-not-require-syslog.socket.patch
Patch0002: 0002-do-not-call-fjson_object_put-from-jsonMerge.patch

Source3: rsyslog.logrotate

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: libgcrypt-devel
BuildRequires: libfastjson-devel
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: liblogging-stdlog-devel
BuildRequires: libtool
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
# make sure systemd is in a version that isn't affected by rhbz#974132
BuildRequires: systemd-devel >= 204-8
BuildRequires: zlib-devel
BuildRequires: qpid-proton-c-devel

Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: syslog
Obsoletes: sysklogd < 1.5-11

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package doc
Summary: HTML documentation for rsyslog
Group: Documentation

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libestr-devel libee-devel liblognorm-devel >= 1.0.2

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mariadb-connector-c-devel

%if %{want_mongodb}
%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librelp-devel >= 1.0.3

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel

%package omamqp1
Summary: Provides the omamqp1 module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: qpid-proton-c-devel

%package kafka
Summary: Provides the omkafka module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librdkafka-devel

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%description doc
This subpackage contains documentation for rsyslog.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%if %{want_mongodb}
%description mongodb
The rsyslog-mongodb package contains a dynamic shared object that will add
MongoDB database support to rsyslog.
%endif

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%description omamqp1
The omamqp1 output module can be used to send log messages via an AMQP 
1.0-compatible messaging bus.

%description kafka
The rsyslog-kafka package provides module for Apache Kafka output. 

%prep
%autosetup -p1
%setup -q -DT -a1
mv build doc

%build
autoreconf -iv

%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS="-L%{_libdir} -lhiredis"
%endif
%configure \
	--prefix=/usr \
	--disable-static \
%if %{want_testbench}
	--enable-testbench \
%endif
	--enable-elasticsearch \
	--enable-generate-man-pages \
	--enable-gnutls \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp \
	--enable-libdbi \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mysql \
	--enable-omamqp1 \
%if %{want_hiredis}
	--enable-omhiredis \
%endif
	--enable-omjournal \
%if %{want_mongodb}
	--enable-ommongodb \
%endif
	--enable-omprog \
	--enable-omrabbitmq \
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \
	--enable-omkafka

make V=1

%check
make V=1 check

%install
make V=1 DESTDIR=%{buildroot} install

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -d -m 700 %{buildroot}%{rsyslog_statedir}
install -d -m 700 %{buildroot}%{rsyslog_pkidir}
install -d -m 755 %{buildroot}%{rsyslog_docdir}/html

install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
install -p -m 644 plugins/ommysql/createDB.sql %{buildroot}%{rsyslog_docdir}/mysql-createDB.sql
install -p -m 644 plugins/ompgsql/createDB.sql %{buildroot}%{rsyslog_docdir}/pgsql-createDB.sql
install -p -m 644 tools/recover_qi.pl %{buildroot}%{rsyslog_docdir}/recover_qi.pl
# extract documentation
cp -r doc/* %{buildroot}%{rsyslog_docdir}/html
# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la

# imdiag and liboverride is only used for testing
rm -f %{buildroot}%{_libdir}/rsyslog/imdiag.so
rm -f %{buildroot}%{_libdir}/rsyslog/liboverride_gethostname.so

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING*
%doc AUTHORS ChangeLog README.md
%{rsyslog_docdir}
%exclude %{rsyslog_docdir}/html
%exclude %{rsyslog_docdir}/mysql-createDB.sql
%exclude %{rsyslog_docdir}/pgsql-createDB.sql
%dir %{_libdir}/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_sbindir}/rsyslogd
%{_mandir}/man5/rsyslog.conf.5.gz
%{_mandir}/man8/rsyslogd.8.gz
%{_unitdir}/rsyslog.service
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
# plugins
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmcisconames.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/pmsnare.so

%files crypto
%defattr(-,root,root)
%{_bindir}/rscryutil
%{_mandir}/man1/rscryutil.1.gz
%{_libdir}/rsyslog/lmcry_gcry.so

%files doc
%defattr(-,root,root)
%doc %{rsyslog_docdir}/html

%files elasticsearch
%defattr(-,root,root)
%{_libdir}/rsyslog/omelasticsearch.so

%if %{want_hiredis}
%files hiredis
%defattr(-,root,root)
%{_libdir}/rsyslog/omhiredis.so
%endif

%files libdbi
%defattr(-,root,root)
%{_libdir}/rsyslog/omlibdbi.so

%files mmaudit
%defattr(-,root,root)
%{_libdir}/rsyslog/mmaudit.so

%files mmjsonparse
%defattr(-,root,root)
%{_libdir}/rsyslog/mmjsonparse.so

%files mmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/mmnormalize.so

%files mmsnmptrapd
%defattr(-,root,root)
%{_libdir}/rsyslog/mmsnmptrapd.so

%files mysql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/mysql-createDB.sql
%{_libdir}/rsyslog/ommysql.so

%if %{want_mongodb}
%files mongodb
%defattr(-,root,root)
%{_bindir}/logctl
%{_libdir}/rsyslog/ommongodb.so
%endif

%files pgsql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/pgsql-createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%files rabbitmq
%defattr(-,root,root)
%{_libdir}/rsyslog/omrabbitmq.so

%files gssapi
%defattr(-,root,root)
%{_libdir}/rsyslog/lmgssutil.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/omgssapi.so

%files relp
%defattr(-,root,root)
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files gnutls
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_gtls.so

%files snmp
%defattr(-,root,root)
%{_libdir}/rsyslog/omsnmp.so

%files udpspoof
%defattr(-,root,root)
%{_libdir}/rsyslog/omudpspoof.so

%files omamqp1
%defattr(-,root,root)
%{_libdir}/rsyslog/omamqp1.so

%files kafka
%defattr(-,root,root)
%{_libdir}/rsyslog/omkafka.so

%changelog
* Mon Oct 16 2017 Lars Kellogg-Stedman <lars@redhat.com> 8.29.0-2
- do not call fjson_object_put from jsonMerge
- do not require syslog.socket

