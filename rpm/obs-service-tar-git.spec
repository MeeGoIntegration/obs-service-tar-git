Name:       obs-service-tar-git

Summary:    tar_git service designed for packing up git trees
Version:    0.6.0
Release:    1
Group:      Development/Tools
BuildArch:  noarch
License:    GPLv2
URL:        https://github.com/MeeGoIntegration/obs-service-tar-git
Source0:    %{name}-%{version}.tar.xz
Requires:   obs-source_service
# git is the primary tool used
Requires:   git-core
# use the repo source service if it is needed
Requires:   obs-service-repo
# the script is written in bash
Requires:   bash
# for tar, compress sources
Requires:   tar
# in case .bz2 is used in .spec
Requires:   pbzip2
# in case .gz is used in .spec
Requires:   pigz
# in case .xz is used in .spec
Requires:   xz
# for find and xargs
Requires:   findutils
# for all standard utils
Requires:   coreutils
# gawk and awk is used in the script as well as sed
Requires:   gawk
Requires:   sed
# for flock
Requires:   util-linux
# rsync and curl is used in download_files section
Requires:   rsync
Requires:   curl
# git-lfs is used to cache and clone LFS git objects
Requires:   git-lfs


%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib/obs/service/
cp tar_git %{buildroot}/usr/lib/obs/service/
cp tar_git.service %{buildroot}/usr/lib/obs/service/

%files
%defattr(-,root,root,-)
/usr/lib/obs/
%defattr(755,root,root,-)
/usr/lib/obs/service/tar_git
