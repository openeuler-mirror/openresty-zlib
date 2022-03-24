Name:               openresty-zlib
Version:            1.2.11
Release:            4
Summary:            The zlib compression library for OpenResty

Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                http://www.zlib.net/
Source0:            http://www.zlib.net/zlib-%{version}.tar.xz
Patch99:            0099-copy-dir.sh.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

AutoReqProv:        no

%define zlib_prefix		/usr/local/openresty/zlib
%define zlib_prefix_asan	/usr/local/openresty-asan/zlib

%description
The zlib compression library for use by Openresty ONLY


%package devel

Summary:            Development files for OpenResty's zlib library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's zlib library.


%package asan
Release:            14
Summary:            Clang AddressSanitizer version for the zlib compression library for OpenResty
Group:              System Environment/Libraries
BuildRequires:      libtool, clang, compiler-rt

AutoReqProv:        no
%description asan
The zlib compression library for use by Openresty ONLY. This is the clang AddressSanitizer build.


%package asan-devel
Release:            14
Summary:            Development files for OpenResty's zlib library
Group:              Development/Libraries
Requires:           openresty-zlib-asan = %{version}-%{release}

%description asan-devel
Provides C header and static library for OpenResty's clang AddressSanitizer version of zlib library.

%prep
%setup -q -n zlib-%{version}

%patch99 -p1

%build
bash ./copy-dir.sh
./configure --prefix=%{zlib_prefix}
make %{?_smp_mflags} CFLAGS='-O3 -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O3 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3'

cd asan 
export ASAN_OPTIONS=detect_leaks=0

CC="clang -fsanitize=address" ./configure --prefix=%{zlib_prefix_asan}

make %{?_smp_mflags} CC="clang -fsanitize=address" \
    CFLAGS='-O1 -fno-omit-frame-pointer -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O1 -fno-omit-frame-pointer -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    LDSHARED='clang -fsanitize=address -shared -Wl,-soname,libz.so.1,--version-script,zlib.map'

cd -

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig

cd asan
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix_asan}/share
rm -f  %{buildroot}/%{zlib_prefix_asan}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix_asan}/lib/pkgconfig
cd -

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{zlib_prefix}/lib/libz.so*


%files devel
%defattr(-,root,root,-)

%{zlib_prefix}/lib/*.a
%{zlib_prefix}/include/zlib.h
%{zlib_prefix}/include/zconf.h

%files asan
%defattr(-,root,root,-)

%attr(0755,root,root) %{zlib_prefix_asan}/lib/libz.so*


%files asan-devel
%defattr(-,root,root,-)

%{zlib_prefix_asan}/lib/*.a
%{zlib_prefix_asan}/include/zlib.h
%{zlib_prefix_asan}/include/zconf.h

%changelog
* Thu Mar 24 2022 wulei <wulei80@huawei.com> - 1.2.11-4
- Delete {?dist}

* Wed Jul 21 2021 imjoey <majunjie@apache.org> - 1.2.11-3
- Package init
