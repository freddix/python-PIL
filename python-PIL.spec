%define		module	PIL

Summary:	Python's own image processing library
Name:		python-%{module}
Version:	1.1.7
Release:	4
License:	distributable
Group:		Libraries/Python
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Source0-md5:	fc14a54e1ce02a0225be8854bfba478e
URL:		http://www.pythonware.com/products/pil/index.htm
BuildRequires:	freetype-devel
BuildRequires:	lcms-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	sane-backends-devel
BuildRequires:	zlib-devel
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python Imaging Library (PIL) adds image processing capabilities to
your Python interpreter. This library provides extensive file format
support, an efficient internal representation, and powerful image
processing capabilities.

%description -l pl.UTF-8
Python Imaging Library (PIL) dodaje możliwość przetwarzania obrazu do
interpretera Pythona. Biblioteka daje wsparcie dla wielu formatów
plików, wydajną reprezentację wewnętrzną i duże możliwości obróbki

%package devel
Summary:	Python's own image processing library header files
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Python's own image processing library header files.

%prep
%setup -qn Imaging-%{version}

sed -i -e "s|/usr/local/bin/python|%{_bindir}/python|" Scripts/*.py

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build_ext -i
%{__python} selftest.py

cd Sane
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install 	\
	--root=$RPM_BUILD_ROOT	\
	--optimize=2

cd Sane
%{__python} setup.py install 	\
	--root=$RPM_BUILD_ROOT	\
	--optimize=2
cd ..

install -d $RPM_BUILD_ROOT%{py_incdir}
install libImaging/Im{Platform,aging}.h $RPM_BUILD_ROOT%{py_incdir}

%py_comp $RPM_BUILD_ROOT%{py_sitedir}/%{module}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/%{module}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES*
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%attr(755,root,root) %{py_sitedir}/*.so
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py?
%{py_sitedir}/*.py[co]
%{py_sitedir}/PIL.pth

%files devel
%defattr(644,root,root,755)
%{py_incdir}/*.h

