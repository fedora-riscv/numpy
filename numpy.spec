%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# eval to 2.3 if python isn't yet present, workaround for no python in fc4 minimal buildroot
%{!?python_version: %define python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]' || echo "2.3")}

Name:           numpy
Version:        1.0.4
Release:        1%{?dist}
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
License:        BSD
URL:            http://numeric.scipy.org/
Source0:        http://dl.sourceforge.net/numpy/%{name}-%{version}.tar.gz
Patch0:         numpy-1.0.1-f2py.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel python-setuptools gcc-gfortran
BuildRequires:  blas-devel lapack-devel

Provides:       f2py
Obsoletes:      f2py <= 2.45.241_1927

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%prep
%setup -q
%patch0 -p1 -b .f2py

%build
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="$RPM_OPT_FLAGS" \
    %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="$RPM_OPT_FLAGS" \
    %{__python} setup.py install --root $RPM_BUILD_ROOT
rm -rf docs-f2py ; mv $RPM_BUILD_ROOT%{python_sitearch}/%{name}/f2py/docs docs-f2py
mv -f $RPM_BUILD_ROOT%{python_sitearch}/%{name}/f2py/f2py.1 f2py.1
rm -rf doc ; mv -f $RPM_BUILD_ROOT%{python_sitearch}/%{name}/doc .
install -D -p -m 0644 f2py.1 $RPM_BUILD_ROOT%{_mandir}/man1/f2py.1
pushd $RPM_BUILD_ROOT%{_bindir} &> /dev/null
# symlink for anyone who was using f2py.numpy
ln -s f2py f2py.numpy
popd &> /dev/null

%check ||:
pushd doc &> /dev/null
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} -c "import pkg_resources, numpy ; numpy.test(1, 1)"
popd &> /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc docs-f2py doc/* LICENSE.txt
%{_bindir}/*
%{_mandir}/man*/*
%{python_sitearch}/%{name}

%changelog
* Tue May 06 2008 Jarod Wilson <jwilson@redhat.com> 1.0.4-1
- New upstream release

* Wed Aug 22 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-1
- New upstream release

* Wed Jun 06 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3-1
- New upstream release

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Drop BR: atlas-devel, since it just provides binary-compat
  blas and lapack libs. Atlas can still be optionally used
  at runtime. (Note: this is all per the atlas maintainer).

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-1
- New upstream release

* Fri May 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2.3
- Bump and rebuild against RHEL5 final

* Mon Mar 26 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2.2
- Fix BR: on gcc-gfortran

* Sat Mar 24 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2.1
- Build for EL5 w/o atlas

* Thu Jan 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2
- Per discussion w/Jose Matos, Obsolete/Provide f2py, as the
  stand-alone one is no longer supported/maintained upstream

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.0.1-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.0-2
- Rebuild for python 2.5

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.0-1
- New upstream release

* Tue Sep 06 2006 Jarod Wilson <jwilson@redhat.com> 0.9.8-1
- New upstream release

* Wed Apr 26 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.6-1
- Upstream update

* Thu Feb 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.5-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-2
- Rebuild for Fedora Extras 5

* Thu Feb  2 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-1
- Initial RPM release
- Added gfortran patch from Neal Becker
