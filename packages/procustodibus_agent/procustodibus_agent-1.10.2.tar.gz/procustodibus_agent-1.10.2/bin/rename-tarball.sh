#!/bin/sh -eu
# renames tarball (and root dir in tarball) to use preferred name
# eg ./rename-tarball.sh dist/procustodibus_agent-1.2.3.tar.gz
# renames to dist/procustodibus-agent-1.2.3.tar.gz (converting underbar to dash)
tar_path=$1
dir_path=$(dirname $tar_path)
tar_file=$(basename $tar_path)
old_name=$(basename $tar_path .tar.gz)
new_name=$(echo $old_name | sed 's/_/-/')
tmp_dir=$(mktemp -d)

mkdir -p $tmp_dir
tar xf $tar_path -C $tmp_dir
mv $tmp_dir/$old_name $tmp_dir/$new_name
tar caf $dir_path/$new_name.tar.gz -C $tmp_dir $new_name
rm -rf $tmp_dir
