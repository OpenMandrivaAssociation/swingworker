%define section		free

Name:		swingworker
Version:	1.2.1
Release:	7
Epoch:		0
Summary:        Swing Worker API
License:        LGPL
Url:            https://swingworker.dev.java.net/
Group:		Development/Java
#
Source0:        https://swingworker.dev.java.net/files/documents/2810/51774/swing-worker-src-1.1.zip
BuildRequires:	java-rpmbuild >= 1.6
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  locales-en
BuildArch:      noarch

%description
SwingWorker is designed for situations where you need to have a long running 
task run in a background thread and provide updates to the UI either 
when done, or while processing. This project is a backport of SwingWorker 
included into Java 1.6.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;

%build
export LC_ALL=ISO-8859-1
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant bundles javadoc

%install
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 dist/bundles/swing-worker.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(-,root,root)
%{_javadir}/*


%files javadoc
%defattr(-,root,root)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %{_javadocdir}/%{name}


%changelog
* Tue Sep 08 2009 Thierry Vignaud <tvignaud@mandriva.com> 0:1.2.1-6mdv2010.0
+ Revision: 434237
- rebuild

* Sat Aug 02 2008 Thierry Vignaud <tvignaud@mandriva.com> 0:1.2.1-5mdv2009.0
+ Revision: 261305
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tvignaud@mandriva.com> 0:1.2.1-4mdv2009.0
+ Revision: 253860
- rebuild

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.2.1-2mdv2008.1
+ Revision: 121029
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Thu Dec 13 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:1.2.1-1mdv2008.1
+ Revision: 119142
- Initial package for backport of Java6's swingworker
- create swingworker

