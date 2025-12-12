Compute APDEX from Apache-style logs.

Overview
========

Parses Apache-style logs and generates several statistics intended for a
website developer audience:

- APDEX (Application Performance inDEX, see http://www.apdex.org) ratio
  (plotted)

  Because you want to know how satisfied your users are.

- hit count (plotted)

  Because achieving 100% APDEX is easy when there is nobody around.

- HTTP status codes, with optional detailed output of the most frequent URLs
  per error status code, along with their most frequent referers

  Because your forgot to update a link to that conditionally-used browser
  compatibility javascript you renamed.

- Hottest pages (pages which use rendering time the most)

  Because you want to know where to invest time to get highest user experience
  improvement.

- ERP5 sites: per-module statistics, with module and document views separated

  Because module and document types are not born equal in usage patterns.

Some parsing performance figures:

On a 2.3Ghz Corei5, apachedex achieves 97000 lines/s (
pypy-c-jit-62994-bd32583a3f11-linux64) and 43000 lines/s (CPython 2.7).
Those were measures on a 3000000-hits logfile, with 3 --skip-base, 1
--erp5-base, 3 --base and --default set. --\*base values were similar in
simplicity to the ones provided in examples below.

What APacheDEX is not
=====================

APacheDEX does not produce website audience statistics like AWStats, Google
Analytics (etc) could do.

APacheDEX does not monitor website availability & resource usage like Zabbix,
Cacti, Ganglia, Nagios (etc) could do.

Requirements
============

Dependencies
------------

As such, apachedex has no strict dependencies outside of standard python 2.7
installation.
But generated output needs a few javascript files which come from other
projects:

- jquery.js

- jquery.flot.js

- jquery.flot.time.js (official flot plugin)

- jquery.flot.axislabels.js (third-party flot plugin)

If you installed apachedex (using an egg or with a distribution's package) you
should have them already.
If you are running from repository, you need to fetch them first::

  python setup.py deps

Input
-----

All default "combined" log format fields are supported (more can easily be
added), plus %D.

Mandatory fields are (in any order) `%t`, `%r` (for request's URL), `%>s`,
`%{Referer}i`, `%D`. Just tell apachedex the value from your apache log
configuration (see `--logformat` argument documentation).

Input files may be provided uncompressed or compressed in:

- bzip

- gzip2

- xz

Input filename "-" is understood as stdin.

Output
------

The output is HTML + CSS + JS, so you need a web browser to read it.

Output filename "-" is understood as stdout.

Usage
=====

A few usage examples. See embedded help (`-h`/`--help`) for further options.

Most basic usage::

  apachedex --default website access.log

Generate stand-alone output (suitable for inclusion in a mail, for example)::

  apachedex --default website --js-embed access.log --out attachment.html

A log file with requests for 2 websites for which individual stats are
desired, and hits outside those base urls are ignored::

  apachedex --base "/site1(/|$|\?)" "/site2(/|$|\?)"

A log file with a site section to ignore. Order does not matter::

  apachedex --skip-base "/ignored(/|$|\?)" --default website

A mix of both above examples. Order matters !::

  apachedex --skip-base "/site1/ignored(/|$|\?)" \
  --base "/site1(/|$|\?)" "/site2(/|$|\?)"

Matching non-ASCII urls works by using urlencoded strings::

  apachedex --base "/%E6%96%87%E5%AD%97%E5%8C%96%E3%81%91(/|$|\\?)" access.log

Naming websites so that report looks less intimidating, by interleaving
"+"-prefixed titles with regexes (title must be just before regex)::

  apachedex --default "Public website" --base "+Back office" \
  "/backoffice(/|$|\\?)" "+User access" "/secure(/|$|\\?)" access.log

Saving the result of an analysis for faster reuse::

  apachedex --default foo --format json --out save_state.json --period day \
  access.log

Although not required, it is strongly advised to provide `--period` argument,
as mixing states saved with different periods (fixed or auto-detected from
data) give hard-to-read results and can cause problems if loaded data gets
converted to a larger period.

Continuing a saved analysis, updating collected data::

  apachedex --default foo --format json --state-file save_state.json \
  --out save_state.json --period day access.2.log

Generating HTML output from two state files, aggregating their content
without parsing more logs::

  apachedex --default foo --state-file save_state.json save_state.2.json \
  --period day --out index.html


Configuration files
===================

Providing a filename prefixed by "@" puts the content of that file in place of
that argument, recursively. Each file is loaded relative to the containing
directory of referencing file, or current working directory for command line.

- foo/dev.cfg::

    --error-detail
    @site.cfg
    --stats

- foo/site.cfg::

    --default Front-office
    # This is a comment
    --prefix "+Back office" "/back(/|$|\?)" # This is another comment
    --skip-prefix "/baz/ignored(/|$|\?)" --prefix +Something "/baz(/|$|\?)"

- command line::

    apachedex --skip-base "/ignored(/|$|\?)" @foo/dev.cfg --out index.html \
    access.log

This is equivalent to::

  apachedex --skip-base "/ignored(/|$|\?)" --error-detail \
  --default Front-office --prefix "+Back office" "/back(/|$|\?)" \
  --skip-prefix "/baz/ignored(/|$|\?)" --prefix +Something "/baz(/|$|\?)" \
  --stats --out index.html access.log

Portability note: the use of paths containing directory elements inside
configuration files is discouraged, as it's not portable. This may change
later (ex: deciding that import paths are URLs and applying their rules).

Periods
=======

When providing the `--period` argument, two related settings are affected:

- the period represented by each point in a graph (most important for the
  hit graph, as it represents the number of hits per such period)

- the period represented by each column in per-period tables (status codes
  per date, hits per day...)

Also, when `--period` is not provided, apachedex uses a threshold to tell
when to switch to the larger period. That period was chosen to correspond
to 200 graph points, which represents a varying number of table columns.

.. table :: Details of `--period` argument

  =========== ========== ========== ============== =========================
  --period    graph      table      to next period columns until next period
  =========== ========== ========== ============== =========================
  quarterhour minute     15 minutes 200 minutes    8 (3.3 hours)
  halfday     30 minutes 12 hours   100 hours      9 (4.1 days)
  day         hour       day        200 hours      9 (8.3 days)
  week        6 hours    week       1200 hours     8 (7.1 weeks)
  month       day        month      5000 hours     7 (~6.7 months)
  quarter     7 days     quarter    1400 days      16 (15.3 weeks)
  year        month      year       (n/a)          (infinity)
  =========== ========== ========== ============== =========================

"7 days" period used in `--period quarter` are not weeks strictly
speaking: a week starts a monday/sunday, pendending on the locale.
"7 days" start on the first day of the year, for simplicity - and
performance. "week" used for `--period week` are really weeks, although
starting on monday independently from locale.

When there are no hits for more than a graph period, placeholders are
generated at 0 hit value (which is the reality) and 100% apdex (this is
arbitrary). Those placeholders only affect graphs, and do not affect
averages nor table content.

Because not all graph periods are actually equal in length (because of
leap seconds, DST, leap years, year containing a non-integer number of
weeks), some hit graph points are artificially corrected against these
effects. Here also, the correction only affects graphs, neither averages
nor table content. For example, on non-leap years, the last year's
"7 days" period lasts a single day. Ploted hit count is then multiplied
by 7 (and 3.5 on leap years).

Performance
===========

For better performance...

- pipe decompressed files to apachedex instead of having apachedex decompress
  files itself::

    bzcat access.log.bz2 | apachedex [...] -

- when letting apachedex decide statistic granularity with multiple log files,
  provide earliest and latest log files first (whatever order) so apachedex can
  adapt its data structure to analysed time range before there is too much
  data::

    apachedex [...] access.log.1.gz access.log.99.gz access.log.2.gz \
    access.log.3.gz [...] access.98.gz

- parse log files in parallel processes, saving analysis output and aggregating
  them in the end::

    for LOG in access*.log; do
      apachedex "$@" --format json --out "$LOG.json" "$LOG" &
    done
    wait
    apachedex "$@" --out access.html --state-file access.*.json

  If you have bash and have an xargs implementation supporting `-P`, you may
  want to use `parallel_parse.sh` available in source distribution or from
  repository.

Notes
=====

Loading saved states generated with different sets of parameters is not
prevented, but can produce nonsense/unreadable results. Or it can save the day
if you do want to mix different parameters (ex: you have some logs generated
with %T, others with %D).

It is unclear how saved state format will evolve. Be prepared to have
to regenerate saved states when you upgrade APacheDEX.
