#!/bin/bash

for arg in "$@"; do
  shift
  case "$arg" in
  '--flaky') set -- "$@" '-f' ;;
  '--fixed') set -- "$@" '-x' ;;
  '--module') set -- "$@" '-m' ;;
  '--test') set -- "$@" '-t' ;;
  *) set -- "$@" "$arg" ;;
  esac
done

OPTIND=1
while getopts "f:x:m:t:" opt; do
  case "$opt" in
  'f') flaky_commit=$OPTARG ;;
  'x') fixed_commit=$OPTARG ;;
  'm') test_module=$OPTARG ;;
  't') test_case=$OPTARG ;;
  esac
done
shift $(expr $OPTIND - 1)

git checkout $fixed_commit

git bisect start

git bisect bad

git checkout $flaky_commit

git bisect good

git bisect run ./git-bisect-script.sh $test_module $test_case
