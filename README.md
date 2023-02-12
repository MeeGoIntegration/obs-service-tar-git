# obs-service-tar-git
**OBS tar_git source service**

Note that this README is not an exhaustive description or even a specification.  It is merely a user contributed write-up providing some guidance how `tar_git` works.  This write-up may have flaws or be fully errorneous at places; if you want to know something for sure, please read `tar_git`'s [interface definition](https://github.com/MeeGoIntegration/obs-service-tar-git/blob/master/tar_git.service) and its [shell script](https://github.com/MeeGoIntegration/obs-service-tar-git/blob/master/tar_git), which provides all its functionality.

Side note: This is *not* about the regular OBS (Open Build Service) services (plug-in modules) `tar_scm` or `git_tar`: The only publicly visible place where `tar_git` runs is [the SailfishOS-OBS](https://build.merproject.org/), where it is the only and mandatory service.

### Parameters for OBS' `_service` file
See `tar_git`'s [interface definition](https://github.com/MeeGoIntegration/obs-service-tar-git/blob/master/tar_git.service) and an [exemplary `_service`](https://build.merproject.org/package/view_file/sailfishos:chum:testing/harbour-storeman-installer/_service) file.

### Parsing of Git tags
1. A valid tag for `tar_git` may contain at most a single dash ("-").  The sub-string starting at the dash is discarded.
2. A valid tag for `tar_git` may be prefixed by either a small "v" or a "vendor string" ending in a slash ("/").  The "v" or the "vendor string" including the slash are discarded.
3. The resulting, stripped tag must conform to the extended regular expression (ERE) `^[[:digit:]]+\.[[:alnum:].~+]*$` (but is actually [written more complicated](https://github.com/MeeGoIntegration/obs-service-tar-git/blob/master/tar_git#L406)) and originate from the branch provided by the `branch` parameter, otherwise it is discarded.
4. If there is no valid tag or if a commit ID (short-hash) was provided, `tar_git` [looks for the "nearest" tag](https://github.com/MeeGoIntegration/obs-service-tar-git/blob/master/tar_git#L960) which fulfils aforementioned rules (i.e., runs through steps 1 to 3 with it), but misses to filter for the branch provided by the `branch` parameter.  It then appends a `+`, the branch name in which the "nearest" tag was found, a `.` a date string, a `.1.g` and a short-hash (¿of the last commit?), which are a clear indication that this code path was used, resulting in, e.g., `0.5.2+main.20230129011931.1.g584263a` when the "nearest" tag found was `0.5.2-3`.
5. The result of this overwrites the original `Version:` string in the RPM spec file, which can be viewed at a package's page in the SailfishOS-OBS..

Note that, when a package is built by the SailfishOS-OBS, also a new release string is constructed, comprised of `-1.`, the package revision at OBS and `.1.jolla`.  This is *not* visible in the processed RPM spec file of a package, because it is done while building a package.

For example, when using `sfos4.2/0.3.0-2` as a tag name for the `harbour-storeman` app, this results in, e.g., `harbour-storeman-0.3.0-1.13.1.jolla.armv7hl.rpm`.

#### The `token` parameter
When the `token` parameter contains a non-empty string (not a regular expression), this string is used as a sub-string an original (i.e., unprocessed) tag must match to, otherwise the tag is discarded.  Note that such a tag is then subjected to the processing describes in steps 1 to 4, above.  Hence for the aforementioned example utilising "Storeman", `sfos` would be a suitable a token.  Or when marking release versions with the string `release` in the release version (e.g., `1.2.3-release2`), the string `release` is a suitable `token` to filter for release versions.

#### Examples
Once understood how `tar_git`'s parsing of Git tags works, one can play with it: For example, by using the tags `1.2.3+git1`, `1.2.3~git1` or `1.2.3.git1` the whole string will become part of the RPM file-name, for `1.2.3-git1`, `git1/1.2.3` and `foo/1.2.3-bar` only the `1.2.3`.
