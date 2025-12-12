## Changelog

### 6.1.2 - 2025-12-04

*   [fedfind-6.1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.1.2.tar.gz)

1.  Add an Accept header to HTTP requests (to make bot checkers happy)

### 6.1.1 - 2025-09-26

*   [fedfind-6.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.1.1.tar.gz)

1.  Update `expected_images` definition for `ElnNightly`

ELN has subvariants now!

### 6.1.0 - 2025-06-06

*   [fedfind-6.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.1.0.tar.gz)

1.  Remove `ODCSCompose` and `ElnCompose` release types
2.  Add an `expected_images` definition for `ElnNightly`

The ODCS ELN composes have not been run for some months now, and the URL where they lived is
empty. Removing these compose types is technically an interface change, but they cannot have
done anything useful for anyone for quite some time, so it shouldn't cause any problems.

### 6.0.6 - 2025-03-11

*   [fedfind-6.0.6.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.6.tar.gz)

1.  Tweak `Compose.exists` to not be `True` too early (before sync is done)

### 6.0.5 - 2025-01-22

*   [fedfind-6.0.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.5.tar.gz)

1.  Don't use 'container' image type when synthesizing metadata (yet)

### 6.0.4 - 2024-10-21

*   [fedfind-6.0.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.4.tar.gz)

1.  Add several new subvariants to the constants (improves metadata synthesis)

### 6.0.3 - 2024-09-18

*   [fedfind-6.0.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.3.tar.gz)

1.  Extend EPEL filtering to cover EPEL 10 nightlies

### 6.0.2 - 2024-09-13

*   [fedfind-6.0.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.2.tar.gz)

1.  Fix paths and respin handling for ELN

### 6.0.1 - 2024-09-04

*   [fedfind-6.0.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.1.tar.gz)

1.  Change ELN compose release value from "ELN" to "eln"

### 6.0.0 - 2024-08-30

*   [fedfind-6.0.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-6.0.0.tar.gz)

1.  **API**: Remove `helpers.pdc_query`
2.  **API**: Remove `Pungi4Release.get_package_nevras_pdc`
3.  **NEW**: Add `ElnNightly` class to support new-style ELN composes
4.  Port all uses of PDC to use the new "metadata archive" instead
5.  Fix errors in `ElnCompose` initialization
6.  Handle "ELN" as a version in `helpers.parse_cid`

This release adapts to the retirement of PDC and the moving of ELN composes from ODCS
to a more typical script-driven build on kojipkgs. The removed functions mean this must
be a major-versioned release, but since PDC has been retired they were not working anyway.
Use of the "metadata archive" instead of PDC should be transparent in practical use.

### 5.3.0 - 2024-05-30

*   [fedfind-5.3.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.3.0.tar.gz)

1.  **NEW**: honor `FEDFIND_NO_CACHE` environment variable to disable persistent caching

Setting this variable disables the caching of PDC query responses and dl.fp.o file lists. This
can interfere with test suites that use something like pyvcr to "record" and "replay" remote
transactions, if a required PDC response or file list is cached on the system of the user
generating the "recording".

### 5.2.0 - 2024-05-16

*   [fedfind-5.2.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.2.0.tar.gz)

1.  **NEW**: add `relnum` property to `Release` instances, representing the release number
2.  **NEW**: add `eol` property to `Release` instances, indicating EOL date
3.  **NEW**: re-introduce ``Updates`` and ``UpdatesTesting`` classes and support

The updates and updates-testing composes have images again now, so we need to bring back support
for them. The eol property is useful for fedora-cloud-image-uploader, so it seems reasonable to
implement it here rather than making that project do the work. relnum is similarly useful there
but also in various other places, it gives you a guaranteed integer which will be the "most
correct-ish" one for Rawhide and ELN - the number of the next release that will branch.

### 5.1.4 - 2024-04-29

*   [fedfind-5.1.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.1.4.tar.gz)

1.  Handle a few new subvariants
2.  Update test data etc. for Fedora 40 release

### 5.1.3 - 2023-10-29

*   [fedfind-5.1.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.1.3.tar.gz)

1.  Adjust to deprecation of `datetime.datetime.utcnow()` in Python 3.12

### 5.1.2 - 2023-08-31

*   [fedfind-5.1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.1.2.tar.gz)

1.  Handle composes with no images.json metadata file

### 5.1.1 - 2023-06-19

*   [fedfind-5.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.1.1.tar.gz)

1.  Specifically refuse to try and find ELN composes by compose ID

### 5.1.0 - 2023-06-19

*   [fedfind-5.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.1.0.tar.gz)

1.  Handle Fedora ELN composes as new `ElnCompose` class
2.  Update test data etc. for Fedora 38 release

### 5.0.1 - 2022-12-02

*   [fedfind-5.0.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.0.1.tar.gz)

1.  Fix `fedfindlocal.py` with recent fedora_nightlies
2.  Make local path win over system paths in `fedfindlocal.py`
3.  Fix bogus images showing up in RespinRelease due to new live-respins-archive

### 5.0.0 - 2021-12-10

*   [fedfind-5.0.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-5.0.0.tar.gz)

1.  Drop several obsolete `Release` types (Modular, Atomic, Docker)
2.  Drop updates and updates-testing releases: still exist, but don't produce images any more
3.  Make `https_url_generic` None for releases without a generic tree
4.  Add some more flavors to helpers.get_weight

This is a major release due to the removal of several `Release` subclasses and related CLI
commands and so on. In practical terms it shouldn't actually require most or any users to
make changes, because the removed classes relate to compose types that haven't been produced
for years.

### 4.4.5 - 2021-12-09

*   [fedfind-4.4.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.5.tar.gz)

1.  Add several new subvariants to the constants
2.  Correct project name in setup.py
3.  Modernize build/release scripts in line with PEP 517 / PEP 518
4.  Update and enhance tox configuration
5.  Use stdlib cached_property and mock where possible
6.  Lint code with black
7.  Work correctly with old productmd versions that don't have 'vmdk' image type

### 4.4.4 - 2020-10-24

*   [fedfind-4.4.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.4.tar.gz)

1.  Use our own bespoke release metadata instead of Bodhi

### 4.4.3 - 2020-07-22

*   [fedfind-4.4.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.3.tar.gz)

1.  Don't delete _pdccid property, just unset it

### 4.4.2 - 2020-05-01

*   [fedfind-4.4.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.2.tar.gz)

1.  Fix `get_current_release` for new 'ELN' release
2.  Update tests and fixtures for Fedora 32 release

### 4.4.1 - 2020-02-21

*   [fedfind-4.4.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.1.tar.gz)

1.  Mark pytest yield fixtures as yield_fixture in conftest.py

### 4.4.0 - 2020-02-21

*   [fedfind-4.4.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.4.0.tar.gz)

1.  Drop Python 2.6 support, update test config and environments
2.  Use Bodhi not (orphaned) pkgdb for current release info (#17)
3.  Update tests, data and code for F28, F29, F30 and F31 stable releases

This *shouldn't* be backwards incompatible on Python 2.7 or later, unless I messed something up.
It will no longer run on Python 2.6 (some code is changed to syntax that only works on 2.7 and
later). aarch64 is now a recognized arch, and 'Scientific' and 'Comp_Neuro' are recognized as
subvariants. The pkgdb -> Bodhi swap should be transparent, as long as I didn't mess anything up.

### 4.3.0 - 2020-01-07

*   [fedfind-4.3.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.3.0.tar.gz)

1.  Get non-existent Pungi4Release metadata from PDC if we can
2.  Read image sizes from imagelist files for non-Pungi 4 composes

### 4.2.8 - 2019-10-01

*   [fedfind-4.2.8.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.8.tar.gz)

1.  Expire internal collections (release info) cache after one day
2.  Add setuptools_git to setup_requires in `setup.py`

### 4.2.7 - 2019-07-10

*   [fedfind-4.2.7.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.7.tar.gz)

1.  Tweak `version` implementation (fixes it for updates and updates-testing composes)

### 4.2.6 - 2019-07-09

*   [fedfind-4.2.6.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.6.tar.gz)

1.  Update the `RESPINRE` regex used to identify respin release images, again

### 4.2.5 - 2019-06-25

*   [fedfind-4.2.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.5.tar.gz)

1.  Resurrect old `previous_release()` implementation to work around PDC import failures

### 4.2.4 - 2019-06-25

*   [fedfind-4.2.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.4.tar.gz)

1.  Don't expect Atomic Host images for >29 Branched or recent Rawhide either

### 4.2.3 - 2019-06-24

*   [fedfind-4.2.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.3.tar.gz)

1.  Don't expect Atomic Host images for >29 update composes

### 4.2.2 - 2019-03-08

*   [fedfind-4.2.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.2.tar.gz)

1.  Fix image dict synthesis for pre-Pungi 4 composes with productmd 1.20

### 4.2.1 - 2018-11-22

*   [fedfind-4.2.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.1.tar.gz)

1.  Handle running test suite HTTP server fixture with Python 2 or 3

### 4.2.0 - 2018-06-05

*   [fedfind-4.2.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.2.0.tar.gz)

1.  Handle updates and updates-testing composes (#16)
2.  Handle 'Fedora-Container' nightly composes
3.  Handle 'Fedora-IoT' nightly composes

This release adds support for several new(ish) compose types. updates and updates-testing composes
are handled via milestones, as their dist is 'Fedora': we add two new milestones, 'Updates' and
'Updates-testing'. The others are handled just like all the other post-release nightly composes.

### 4.1.3 - 2018-05-28

*   [fedfind-4.1.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.1.3.tar.gz)

1.  Handle sudden new location for Fedora-Cloud and Fedora-Docker nightlies

### 4.1.2 - 2018-05-21

*   [fedfind-4.1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.1.2.tar.gz)

1.  Couple of fixes for handling the special live-respins releases

### 4.1.1 - 2018-03-06

*   [fedfind-4.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.1.1.tar.gz)

1.  Update `expected_images` and `const.SUBVARIANTS` for Atomic variant renames

### 4.1.0 - 2018-02-20

*   [fedfind-4.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.1.0.tar.gz)

1.  **NEW**: restore PDC-based NEVRA check as `get_package_nevras_pdc`
2.  Make tests smarter about waiting for the test HTTP server to come up

This release restores the PDC-based implementation of `get_package_nvras` for Pungi4Release
classes as a **separate** method called `get_package_nevras_pdc`. `get_package_nvras` is still
available for Pungi4Release classes and works just as it does for other classes. The PDC version
is available *only* for Pungi4Release classes (as other releases are not in PDC).

### 4.0.0 - 2018-01-19

*   [fedfind-4.0.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-4.0.0.tar.gz)

1.  **API** Remove `get_release_url` and `get_release_cid`
2.  `get_release`: check discovered compose matches requested URL or compose ID
3.  `get_release`, CLI: allow and prefer Atomic, Docker, Cloud, Respin discovery by dist, not milestone
4.  Milestone attribute of Atomic, Docker, Cloud composes is now 'Nightly'
5.  `get_release`: really raise `UnsupportedComposeError` for unsupported composes
6.  `get_release`: rejig current. vs archive release detection to handle both existing at once
7.  Make `exists` False not True for`CurrentRelease`s that have been archived
8.  Fix `expected_images` for Fedora 26+ (i686 no longer primary arch)
9.  Update `previous_release` for `Milestone` instances for Fedora 26+ not having Alpha releases
10. Update `const` with new subvariants
11. Various fixes, updates and enhancements to test suite
12.  Miscellaneous clean-ups and code refactoring

This is a major release, with the main goals being to sort out the mess that had developed around
composes with 'dist' / shortname other than 'Fedora'. Early in fedfind's life, when it started
handling two-week Atomic composes, we chose to use the `milestone` value to represent these, and
over time added more and more `milestones` that represented non-mainline composes. But with the
shift to Pungi 4 and the proliferation of compose types during the Fedora 25 and 26 cycles, it
became clear that releng's approach was to identify these by the productmd 'short name', and the
'Fedora-Modular' composes could not be handled via the `milestone` value, as we actually needed
to identify different milestones for 'Fedora-Modular' composes. So we retrofitted the 'dist'
concept to fedfind, but continued to handle all dists other than 'Fedora-Modular' as 'milestones'.
This was entirely inconsistent and messy. With this release, we clearly prefer using the 'dist'
concept to handle all these composes. We remain backwards-compatible with the `milestone` approach
for now, but print a warning when it's used.

We take advantage of the major release to do some refactoring and cleanup. There should actually
be very little flat out backwards incompatibility in this release, but it's possible some unusual
cases don't behave quite as they did before in ways that aren't clearly explained above.

### 3.8.3 - 2017-11-21

*   [fedfind-3.8.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.8.3.tar.gz)

1.  Fix `get_package_nvras` for Modular composes a bit harder

### 3.8.2 - 2017-11-15

*   [fedfind-3.8.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.8.2.tar.gz)

1.  Fix `get_package_nvras` for Modular composes
2.  Fix `https_url_generic` for Modular composes
3.  Fix `get_package_nvras` on Python 3

### 3.8.1 - 2017-11-14

*   [fedfind-3.8.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.8.1.tar.gz)

1.  Restore `get_current_release` to using the pkgdb collections API, it is being updated again

### 3.8.0 - 2017-11-07

*   [fedfind-3.8.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.8.0.tar.gz)

1.  **NEW** Add `ModularProduction` and `ModularCompose` to support modular candidate composes

### 3.7.1 - 2017-10-27

*   [fedfind-3.7.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.7.1.tar.gz)

1.  Handle missing 'updates-testing' release type with productmd before 1.9

### 3.7.0 - 2017-10-27

*   [fedfind-3.7.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.7.0.tar.gz)

1.  **NEW** Add `BikeshedModularNightly` class for 'Bikeshed' nightly modular composes
    (these are the same as `RawhideModularNightly` previously)
2.  Completely rewrite `helpers.parse_cid` to be much more capable of handling complex CIDs
3.  Explicitly do not support 'updates' and 'updates-testing' composes (no images)

### 3.6.4 - 2017-10-16

*   [fedfind-3.6.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.6.4.tar.gz)

1.  Update CHANGELOG for 3.6.3 changes (missed when releasing 3.6.3)

### 3.6.3 - 2017-10-13

*   [fedfind-3.6.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.6.3.tar.gz)

1.  Fix `expected_images` property for modular composes (trying to use it crashed before)

### 3.6.2 - 2017-09-11

*   [fedfind-3.6.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.6.2.tar.gz)

1.  Fix `pdc_query` to include a trailing `/` in URLs (PDC no longer accepts queries without)
2.  Update `const.SUBVARIANTS` to include Python_Classroom and LXQt

### 3.6.1 - 2017-08-18

*   [fedfind-3.6.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.6.1.tar.gz)

1.  Temporarily hard code 'current' release info as pkgdb has gone and PDC isn't ready

### 3.6.0 - 2017-08-16

*   [fedfind-3.6.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.6.0.tar.gz)

1.  **NEW**: Support Rawhide and Branched modular nightly composes with new classes

### 3.5.4 - 2017-04-18

*   [fedfind-3.5.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.5.4.tar.gz)

1.  Handle cache directory suddenly disappearing

### 3.5.3 - 2017-04-06

*   [fedfind-3.5.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.5.3.tar.gz)

1.  Allow 'FACD' as a compose shortname

### 3.5.2 - 2017-03-26

*   [fedfind-3.5.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.5.2.tar.gz)

1.  Add other secondary arch compose URLs to known URL list too

### 3.5.1 - 2017-03-26

*   [fedfind-3.5.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.5.1.tar.gz)

1.  Add PPC compose URL to known URL list (RHBZ #1435953)

### 3.5.0 - 2017-02-17

*   [fedfind-3.5.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.5.0.tar.gz)

1.  **NEW** Add support for Cloud nightly composes
2.  Revise docstrings and expected image lists for Docker and Atomic nightlies

### 3.4.3 - 2017-02-10

*   [fedfind-3.4.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.4.3.tar.gz)

1.  Fix tests for `disc_number` change from 3.4.2

### 3.4.2 - 2017-02-10

*   [fedfind-3.4.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.4.2.tar.gz)

1.  Include `disc_number` in synthesized image dicts

### 3.4.1 - 2017-02-10

*   [fedfind-3.4.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.4.1.tar.gz)

1.  **SECURITY** Don't return Pungi4Release for unknown URLs
2.  Include `composeinfo` dict in synthesized metadata

### 3.4.0 - 2017-01-26

*   [fedfind-3.4.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.4.0.tar.gz)

1.  **API**: Remove `Release.release_number` property again, it really wasn't a great idea
2.  Fix getting `RespinRelease` by URL (broke with the CID pass through stuff in 3.2.4)

### 3.3.0 - 2017-01-18

*   [fedfind-3.3.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.3.0.tar.gz)

1.  **NEW**: Add `helpers.get_current_stables()`, returns a list of non-EOL stable release numbers
2.  **NEW**: Add `Release.release_number` property, useful mainly for Rawhide nightlies
3.  **NEW**: Add `url` and `direct_url` URL entries to `all_images` image dicts
4.  Pylint cleanups

### 3.2.5 - 2017-01-13

*   [fedfind-3.2.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.5.tar.gz)

1.  Add missing changelog entry for 3.2.4 (forgot to update it in 3.2.4 release)

### 3.2.4 - 2017-01-13

*   [fedfind-3.2.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.4.tar.gz)

1.  **NEW**: Support Docker nightly stable composes
2.  Pass compose ID through from `get_release` to `Release` instance when available
3.  Use `Pungi4Release.get_previous_release` for Docker and Atomic
4.  Fix `Pungi4Release.version` property

### 3.2.3 - 2016-12-14

*   [fedfind-3.2.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.3.tar.gz)

1.  Fix tests for a change from 3.2.1

### 3.2.2 - 2016-12-14

*   [fedfind-3.2.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.2.tar.gz)

1.  Get rid of an `image.py` which snuck into the 3.2.1 release and kinda broke it

### 3.2.1 - 2016-12-08

*   [fedfind-3.2.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.1.tar.gz)

1.  Improve fake compose IDs and release discovery from them
2.  Extend test coverage for recent changes
3.  Small tweaks to `RespinRelease` and `get_release` behaviour

### 3.2.0 - 2016-12-07

*   [fedfind-3.2.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.2.0.tar.gz)

1.  **NEW**: Add `RespinRelease` class, `Respin` milestone to support semi-official live-respins
2.  Remove a stray debug print statement (broke `get_package_nvras` for old releases with Python 3)

### 3.1.3 - 2016-11-30

*   [fedfind-3.1.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.1.3.tar.gz)

1.  Fix some release number check problems (inc. `get_package_nvras` crashing for Rawhide)

### 3.1.2 - 2016-11-30

*   [fedfind-3.1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.1.2.tar.gz)

1.  Improve caching implementation to work (in degraded mode) if user home dir is not writable

### 3.1.1 - 2016-11-29

*   [fedfind-3.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.1.1.tar.gz)

1.  CLI: replace `netinst` with `boot` when used as a type query, and warn about it
2.  `pdc_query`: cache certain results locally to avoid repeated round trips

### 3.1.0 - 2016-11-29

*   [fedfind-3.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.1.0.tar.gz)

1.  Use original image metadata from PDC for stripped/split composes when possible
    * `boot.iso` images no longer returned for Fedora 9 and later
    * `type` for netinst images is now always `boot`, never `netinst`
    * `subvariant` for Mate images is now always `Mate`, not `MATE` when synthesized
    * Much more metadata available for Fedora 24 and later stable and milestone releases

### 3.0.4 - 2016-11-23

*   [fedfind-3.0.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.0.4.tar.gz)

1.  Tweak pytest invocation again, jeez
2.  Add missing test data file
3.  Adjust tests to run on EL 6, remove caplog requirement

### 3.0.3 - 2016-11-23

*   [fedfind-3.0.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.0.3.tar.gz)

1.  Tests don't hard require caplog any more

### 3.0.2 - 2016-11-23

*   [fedfind-3.0.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.0.2.tar.gz)

1.  Adjust pytest invocation from `setup.py` a little to avoid warnings

### 3.0.1 - 2016-11-23

*   [fedfind-3.0.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.0.1.tar.gz)

1.  Tests: allow skipping tests that use caplog (EPEL 6 doesn't have it)

### 3.0.0 - 2016-11-23

*   [fedfind-3.0.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-3.0.0.tar.gz)

1.  Use `imagelist` files, not rsync scraping, to find images in non-metadata composes
    * **API**: `helpers.rsync_helper` is removed
    * **API**: `helpers.urlopen_retries` no longer handles rsync URLs
    * Image discovery is now much faster and produces less load on both ends
    * Image discovery will work offline as long as it's worked online at least once

### 2.7.2 - 2016-11-20

*   [fedfind-2.7.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.7.2.tar.gz)

1.  `helpers.parse_cid` can optionally provide distro too, with `dist=True`

### 2.7.1 - 2016-11-09

*   [fedfind-2.7.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.7.1.tar.gz)

1.  Fix handling of 'RC' milestone composes (they're not called 'Final' any more)

### 2.7.0 - 2016-10-10

*   [fedfind-2.7.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.7.0.tar.gz)

1.  More ostree handling in `helpers.create_image_dict`
2.  Find images from 'alt' location as well, for releases split when synced to public mirrors
    * **API**: `MirrorRelease.all_paths` now returns list of tuples not list of path strings
    * **API**: `MirrorRelease.all_paths` may now raise new `fedfind.exceptions.RsyncError`
    * **NEW**: synthesized image dicts in `MirrorRelease.metadata` now have `alt` key
    * **NEW**: `MirrorRelease` subclasses now have `alt_location` property

### 2.6.3 - 2016-10-10

*   [fedfind-2.6.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.6.3.tar.gz)

1.  Update `helpers.correct_image` to handle -ostree- in filename as well as -dvd-

### 2.6.2 - 2016-10-06

*   [fedfind-2.6.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.6.2.tar.gz)

1.  Fix tests for `create_image_dict` change

### 2.6.1 - 2016-10-06

*   [fedfind-2.6.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.6.1.tar.gz)

1.  `helpers.create_image_dict`: use `dvd-ostree` type for ostree installer images

### 2.6.0 - 2016-10-06

*   [fedfind-2.6.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.6.0.tar.gz)

1.  **API** `Release.PostRelease` class removed: old-style two-week Atomic composes no longer exist
2.  Don't use `identify_image` for `Release.check_expected` as it's not actually the same tuple
3.  Some fixes and updates to the `expected_images` for each release class

### 2.5.0 - 2016-10-05

*   [fedfind-2.5.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.5.0.tar.gz)

1.  **NEW** `helpers.correct_image`: 'correct' an image dict for issues in upstream-generated metadata
2.  **NEW** `helpers.identify_image`: construct an image identifier from the image dict
3.  `Release.all_images`: run image dicts through `helpers.correct_image`
    * This means `all_images` will be **DIFFERENT** for the same compose than 2.4.11 or earlier

### 2.4.11 - 2016-08-26

*   [fedfind-2.4.11.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.11.tar.gz)

1.  `cli`: exit cleanly if there is no finished compose for specified or guessed date

### 2.4.10 - 2016-06-28

*   [fedfind-2.4.10.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.10.tar.gz)

1.  `helpers.parse_cid`: handle Pungi 4 2 Week Atomic compose IDs starting 'Fedora-Atomic'
2.  **NEW** `release.AtomicNightly`: new Release subclass for Pungi 4 2 Week Atomic composes
3.  `release.get_release`: handle Pungi 4 2 Week Atomic compose IDs, add 'Atomic' milestone returning AtomicNightly
4.  `cli`: add 'Atomic' milestone
5.  `release.get_release`: don't use Pungi4Mirror (due to stripping of metadata from mirrored composes)

### 2.4.9 - 2016-05-30

*   [fedfind-2.4.9.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.9.tar.gz)

1.  `helpers.parse_cid`: check if cid is valid and raise `ValueError` if not

### 2.4.8 - 2016-05-30

*   [fedfind-2.4.8.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.8.tar.gz)

1.  `release.Release`: set `label` to empty string (avoids a problem in wikitcms)

### 2.4.7 - 2016-05-04

*   [fedfind-2.4.7.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.7.tar.gz)

1.  `get_release`: clean up a stray debug `print()`

### 2.4.6 - 2016-04-28

*   [fedfind-2.4.6.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.6.tar.gz)

1.  `get_release`: handle 2 Week Atomic 'compose IDs' as `cid`
2.  `PostRelease`: make `respin` a str, not an int (technically an API change but...meh)

### 2.4.5 - 2016-04-14

*   [fedfind-2.4.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.5.tar.gz)

1.  `helpers.get_weight`: allow ignoring arch

### 2.4.4 - 2016-04-10

*   [fedfind-2.4.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.4.tar.gz)

1.  `helpers.pdc_query`: handle non-paged queries
2.  **NEW** `helpers.get_weight`: indicate how important an image is (for sorting download tables etc.)

### 2.4.3 - 2016-03-30

*   [fedfind-2.4.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.3.tar.gz)

1.  Re-add `Milestone` class for milestone releases, now we have F24 Alpha

### 2.4.2 - 2016-03-30

*   [fedfind-2.4.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.2.tar.gz)

1.  Don't use PDC for `get_package_nvras` for Pungi 4 composes temporarily (pdc-updater GitHub issue #10)

### 2.4.1 - 2016-03-21

*   [fedfind-2.4.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.1.tar.gz)

1.  Tests require mock as well as pytest (in setup.py)
2.  Fix the tests to run in Koji (hopefully)

### 2.4.0 - 2016-03-21

*   [fedfind-2.4.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.4.0.tar.gz)

1.  **API** `Release.get_package_nvras` replaces `get_package_versions`, outputs N(E)VRAs now
2.  CLI: allow specifying release by compose ID or label as well as release/milestone/compose/respin
3.  `helpers.pdc_query` now handles query params as a tuple list as well as as a dict
4.  `setup.py` test integration: now you can run `python setup.py test`

### 2.3.0 - 2016-03-17

*   [fedfind-2.3.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.3.0.tar.gz)

1.  **API** Drop `payload` image property in favour of productmd `subvariant`
2.  Synthesize `subvariant` for non-Pungi 4 composes
3.  **NEW** Reintroduce `Compose` release class for mirrored candidate composes
4.  Extend test coverage
5.  Fix `Postrelease` instances with respin 0 (they weren't locating properly before)
6.  Fix `exists` for all pre-Pungi 4 release types (it was recursing infinitely...oops)
7.  `helpers.label_from_cid` now bails without wasting a remote trip if type is not 'production'
8.  Fix some issues with `version` property for Pungi 4 production composes

### 2.2.3 - 2016-03-17

*   [fedfind-2.2.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.2.3.tar.gz)

1.  Fix `get_release` when passing a Rawhide compose ID

### 2.2.2 - 2016-03-16

*   [fedfind-2.2.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.2.2.tar.gz)

1.  Fix `helpers.get_size()` with Python 3

### 2.2.1 - 2016-03-16

*   [fedfind-2.2.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.2.1.tar.gz)

1.  Add missing CHANGELOG entry for 2.2.0

### 2.2.0 - 2016-03-16

*   [fedfind-2.2.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.2.0.tar.gz)

1.  **NEW** `cid_from_label` and `label_from_cid` helpers (they do what they say on the tin)
2.  **NEW** `Production` release class representing 'production' composes on kojipkgs
3.  **NEW** `Release.get_package_versions` method moved here from python-wikitcms
4.  `Release.previous_release` for all Pungi 4 releases now goes through PDC
5.  `get_release` can now handle URL, compose ID, and compose label
6.  Major updates to tests (better coverage of helpers and release, all tests run offline)
7.  A few miscellaneous bug fixes

### 2.1.1 - 2016-03-03

*   [fedfind-2.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.1.1.tar.gz)

1. Fix `check_expected()` for mixed-case payloads

### 2.1.0 - 2016-03-02

*   [fedfind-2.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.1.0.tar.gz)

1. Mixed-case payloads (to match productmd variants more closely)
2. Fix Atomic identification (Atomic images were incorrectly assigned payload 'cloud' in 2.0.0)
3. Fix type for Atomic installer images with final names in old releases
4. Restore some special case handling from 1.x for tricky old release image filenames
5. Use 'Everything' not 'generic' as the payload for old release 'generic' images
6. Move compose ID parsing into `helpers` (so wikitcms can share it)
7. Don't crash in `all_images` for `Pungi4Release` instances that don't exist
8. Make the fake compose IDs for non-Pungi 4 releases a bit better
9. Fix `find_cid()` when there is no compose ID (should return '', not crash)
10. **NEW** add `branched` boolean arg for `get_current_release()` (will return Branched if it exists)

### 2.0.0 - 2016-02-29

*   [fedfind-2.0.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-2.0.0.tar.gz)

fedfind 2.0 is a **really major** release which pretty much rewrites fedfind for a world where Fedora composes are done with Pungi 4. It is more incompatible than not with fedfind 1.x, existing users are almost certain to need changes. Only the CLI interface is mostly unchanged (the `--respin / -i` argument is added, but is optional and all previous invocations should still work and return as close as possible to the same results).

If you have code which uses fedfind you may *seriously consider* stopping using it entirely; it is possible you can achieve your requirements now with Pungi 4 compose metadata and information from [PDC](https://pdc.fedoraproject.org). The primary use cases for fedfind now are only locating composes (if fedmsg messages are not sufficient for you; the locations of new composes are sent out via fedmsg now), synthesizing the `payload` concept which is still missing from productmd, and (to an extent) making it possible to interact with non-Pungi 4 composes in the same way as Pungi 4 composes, if you need to do that (i.e. if you need to deal with old stable releases or the two-week Atomic nightly composes). If you do not need to do any of those things you likely no longer need fedfind.

1. **API** `Image` and `Query` classes dropped entirely
2. **API** `kojiclient.py` (and the `ClientSession` class) removed
3. **API** Many now-unneeded constants from `fedfind.const` removed
4. **API** `respin` concept added to versioning to account for Pungi 4 composes using it
5. **API** `Compose` and `Milestone` classes temporarily dropped as we don't yet know how to do them with Pungi 4
6. **API** `Release.all_images` is now a list of productmd-style image dicts, not of fedfind `Image` instances
7. **API** `Release.koji_done` and `Release.pungi_done` replaced by a single `Release.done` property
8. **API** `Release.check_expected` and `Release.difference` now return `(payload, type, arch)` 3-tuples
9. **API** `Release.find_images` is removed
10. **API** `Release.image_from_url_or_path` is removed
11. **API** `Nightly.all_boot_images` and `Nightly.all_koji_images` are removed
12. **API** `Nightly.get_koji_tasks` and `Nightly.get_koji_images` are removed
13. **API** `MirrorRelease.get_mirror_images()` is removed
14. **API** use unicode literals and print function on Python 2
15. **NEW** `Release.metadata` dict of productmd-style metadata is added
16. **NEW** `Release.location` top-level release location property is added (faked up for non-Pungi 4 releases)
17. **NEW** `Release.cid` 'compose ID' property is added (sloppily faked for non-Pungi 4 releases)
18. **NEW** `Release.all_paths` added (though you're most likely to want `all_images`)
19. Synthesis of `payload` property adapted from old `Image` code
20. Synthesis of partly productmd-compatible metadata for non-Pungi 4 composes
21. Some embryonic support for querying stuff in PDC

### 1.6.2 - 2015-10-02

*   [fedfind-1.6.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.6.2.tar.gz)

1.  Updated location of PostRelease releases (they got moved)

### 1.6.1 - 2015-09-29

*   [fedfind-1.6.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.6.1.tar.gz)

1.  Rewrite `get_release()` and add tests for it (API and expected results do not change)
2.  Fix `get_current_release()` for Python 3
3.  Revise documentation somewhat

### 1.6 - 2015-09-19

*   [fedfind-1.6.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.6.tar.gz)

1.  **API** Treat 'docker' as an `imagetype` (replacing 'filesystem') not a `loadout`
2.  **NEW** Add `shortdesc` attribute for images (shorter description)
3.  **NEW** Add `helpers.get_current_release()` using pkgdb API (better than rsync scrape)
4.  **NEW** Add `PostRelease` class for post-release stable nightly composes
5.  **API** Change `expected_images()`, `difference()` and `check_expected()` to use a 4-tuple with `imagesubtype` included
6.  **API** Catch more 'cloud atomic' image variants properly
7.  **NEW** Add `canned` imagetype, use it for the Cloud Atomic installer image
8.  **API** For images with `subflavor`, `payload` is now `(flavor)_(subflavor)`, not `(flavor) (subflavor)`

### 1.5.1 - 2015-09-02

*   [fedfind-1.5.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.5.1.tar.gz)

1.  **NEW** Add `size` attribute for images
2.  Treat images with 'SRPMS' in their names as `source` imagetype (really old releases)
3.  **NEW** Add `imagesubtype` attribute for images (Vagrant and disk images have various subtypes)

### 1.5 - 2015-08-27

*   [fedfind-1.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.5.tar.gz)

1.  Return rsync retcodes properly in `rsync_helper()`
2.  Have `url_exists()` only return `False` for rsync when 'not found' return code hit
3.  Retry rsync commands when server is full
4.  **NEW** Add `wait()` method for Releases to wait for the compose to exist
5.  Sanity check URLs passes to `url_exists()`
6.  Add pytext/tox test framework and tests
7.  Make `expected_images` more accurate, add Cloud images

### 1.4.2 - 2015-08-21

*   [fedfind-1.4.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.4.2.tar.gz)

1.  Python 3 fix (broke non-nightly image searching and a few other things on Py3...)

### 1.4.1 - 2015-08-21

*   [fedfind-1.4.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.4.1.tar.gz)

1.  Fix a bug in `koji_done` caused by the query opt fixes in 1.4
2.  Add Branched release guessing (so you can pass `-m Branched` and it will guess the release number). Will also guess today's date if you don't pass `-c`
3.  Fix a bug in rsync calls which meant we were getting more data than we meant to

### 1.4 - 2015-08-20

*   [fedfind-1.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.4.tar.gz)

1.  Drop the `multiprocessing` stuff from 1.3, use xmlrpclib `multicall` to batch Koji requests instead
2.  Improve the Koji caching mechanism for partial matches
3.  Fix wrong opt names in Koji query opts (some queries weren't actually doing what they meant to do at all)

### 1.3 - 2015-08-20

*   [fedfind-1.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.3.tar.gz)

1.  Fix `-r NN` in the CLI (broken in 1.2)
2.  Add `previous_release` property for Releases
3.  Various improvements to image parsing (find more images and identify them more accurately)
4.  Add `difference()` method for Releases (show images that are in this release but not the other)
5.  Add `check_expected()` method for Releases (check if all 'important' images are present)
6.  **API**: rename `find_task_url()` to `find_task_images()` and make it return all images (not just one)
7.  Add `find_task_urls()` which actually returns URLs
8.  Add a Koji query cache mechanism for `Nightly` instances
9.  Add `koji_done()` and `pungi_done()` properties (for all Releases, but mostly useful for `Nightly`)
10. Parallelize Koji queries using `multiprocessing`

### 1.2 - 2015-07-23

*   [fedfind-1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.2.tar.gz)

1.  Add a proper logging mechanism
2.  Allow 'Rawhide' as a release value (but, unfortunately, broke `-r NN` in the CLI)

### 1.1.5 - 2015-04-30

*   [fedfind-1.1.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.5.tar.gz)

1.  Add a `-g` parameter that prints the 'generic' URL for the given release
2.  Allow `--milestone Branched` and `--milestone Rawhide` (they are never really necessary, but it's not unusual to pass them instinctively, and as we can handle them, better to do so than fail)

### 1.1.4 - 2015-04-23

*   [fedfind-1.1.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.4.tar.gz)

1.  Drop shebangs from files that can't be executed, use 'env' in shebangs in files that can be executed, don't specify a python version in shebangs (as fedfind is python version-agnostic)

### 1.1.3 - 2015-04-16

*   [fedfind-1.1.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.3.tar.gz)

1.  Drop bundled copy of cached-property, as it's now packaged for Fedora and EPEL (and available from pypi on other platforms)

### 1.1.2 - 2015-03-10

*   [fedfind-1.1.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.2.tar.gz)

1.  Update milestone release mirror path: now uses _ not - as separator

### 1.1.1 - 2015-02-26

*   [fedfind-1.1.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.1.tar.gz)

1.  Handle an argparse bug upstream which causes a crash instead of a nice usage message when invoked with no subcommand

### 1.1.0 - 2015-02-26

*   [fedfind-1.1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.1.0.tar.gz)

1.  Python 3 support
2.  Cleaner approach to using dl.fedoraproject.org instead of download.fedoraproject.org URLs for some images (see 1.0.8)

### 1.0.8 - 2015-02-25

*   [fedfind-1.0.8.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.8.tar.gz)

1.  Use dl.fedoraproject.org URLs, not download.fedoraproject.org, for TC/RC images

### 1.0.7 - 2015-02-25

*   [fedfind-1.0.7.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.7.tar.gz)

1.  Fix a bug which broke finding nightly Koji images by type

### 1.0.6 - 2015-02-18

*   [fedfind-1.0.6.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.6.tar.gz)

1.  Adjustments for the attempt to consolidate versioning across fedfind, python-wikitcms and relval using `release`, `milestone`, `compose` attributes to identify all images/events
2.  Misc. bug fixes and doc cleanups
3.  Add `version` attribute for `Image` objects

### 1.0.5 - 2015-02-12

*   [fedfind-1.0.5.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.5.tar.gz)

1.  Some refinements and bug fixes in image detection
2.  Provide a sort weight property for images
3.  Use xmlrpclib instead of koji to improve portability

### 1.0.4 - 2015-02-09

*   [fedfind-1.0.4.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.4.tar.gz)

1.  Bugfix to the EL 6 compatibility

### 1.0.3 - 2015-02-09

*   [fedfind-1.0.3.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.3.tar.gz)

1.  A lot of pylint cleanups, including various bugfixes found along the way
2.  Python 2.6 compatibility + subprocess32 usage made optional == EL 6 compatibility! Repo now has EL6 and EL7 builds. Note, requires EPEL (for koji package)

### 1.0.2 - 2015-02-06

*   [fedfind-1.0.2.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.2.tar.gz)

1.  Multiple small bugfixes and cleanups (mainly to Koji querying)
2.  Rejigged how the CLI command is implemented (doesn't change usage from the RPM, lets you run `./fedfind.py` directly from a git checkout if you like)

### 1.0.1 - 2015-02-06

*   [fedfind-1.0.1.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.1.tar.gz)

1.  Add ppc to arch list

### 1.0 - 2015-02-05

*   [fedfind-1.0.tar.gz](https://files.pythonhosted.org/packages/source/f/fedfind/fedfind-1.0.tar.gz)

1.  Initial release of fedfind
