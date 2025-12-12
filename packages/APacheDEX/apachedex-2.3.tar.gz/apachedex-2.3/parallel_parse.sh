#!/bin/bash
set -eu
usage() {
  echo "Usage:"
  echo "  find [...] -print0 | $0 \\"
  echo "    parallelism state_dir out_file command [arg1 [...]]"
  echo "Reads filenames to process from stdin, null-delimited."
  echo
  echo "Example: parsing any number of log files with up to 4"
  echo "processes in parallel with locally built pypy:"
  echo "  $ mkdir state"
  echo "  $ $0 4 state out.html /usr/local/bin/pypy \\"
  echo "    bin/apachedex --period week"
}

if [ $# -lt 4 ]; then
  usage
  exit 1
fi

if [ "$1" = "-h" -o "$1" = "--help" ]; then
  usage
  exit 0
fi

parallelism="$1"
state_dir="$2"
out_file="$3"
shift 3
mkdir -p "$state_dir"

# XXX: any simpler way ?
xargs \
  -0 \
  --no-run-if-empty \
  --max-args=1 \
  --max-procs="$parallelism" \
  -I "@FILE@" \
  -- \
  "$SHELL" \
    -c 'infile="$1";stte_dir="$2";shift 2;echo -n .;exec "$@" -Q --format json --out "$state_dir/$(sed s:/:@:g <<< "$infile").json" "$infile"' \
    "$0" \
    "@FILE@" \
    "$state_dir" \
    "$@"
echo
# XXX: what if there are too many state files for a single execution ?
find "$state_dir" -type f -print0 | xargs -0 --exit --no-run-if-empty "$@" --out "$out_file" --state-file
