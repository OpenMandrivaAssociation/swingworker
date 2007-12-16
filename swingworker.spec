%define section		free

Name:		swingworker
Version:	1.2.1
Release:	%mkrel 2
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
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{__rm} -fr %{buildroot}
%setup -q -c -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant bundles

%install
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 dist/bundles/swing-worker.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -pr dist/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%clean
%{__rm} -rf %{buildroot}

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
