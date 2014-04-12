%global		_disable_ld_no_undefined	1
%global		module		Vol

Name:		coin-or-%{module}

Summary:	Vol (Volume Algorithm)
Version:	1.4.4
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel


# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

%description
Vol (Volume Algorithm) is an open-source implementation of a subgradient
method that produces primal as well as dual solutions. The primal solution
comes from estimating the volumes below the faces of the dual problem. This
is an approximate method so the primal vector might have small infeasiblities
that are negligible in many practical settings. The original subgradient
algorithm produces only dual solutions.

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

# silence doxygen deprecation warnings
sed -i 's/^\(SYMBOL_CACHE_SIZE\|SHOW_DIRECTORIES\|HTML_ALIGN_MEMBERS\|USE_INLINE_TREES\|DOT_FONTNAME\)/#\1/g' doxydoc/doxygen.conf.in

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
make %{?_smp_mflags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
make test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/vol_addlibs.txt
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Fri Mar 28 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.4-1
- Update to latest upstream release.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.1-2
- Use proper _smp_flags macro (#894586#c6).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.1-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.3-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.3-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.3-1
- Rename package to coin-or-Vol.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.3-1
- Initial coinor-Vol spec.
