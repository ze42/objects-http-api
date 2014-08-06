#! /bin/sh

basedir=/home/ze/work/is/schema
yml2json="$basedir"/bin/yml2json.py
validate="$basedir"/bin/validate.py

schemabase='example/schema.json'

die()
{
  echo "ERROR: $@"
  exit 1
}

cd "$basedir" || die "failed to cd basedir"

# Update all json files - for inter-schema links
"$yml2json" *.yml example/*.yml || die "Failed to update json files"

for schema in *.json ; do
  out=$("$validate" "$schemabase" "$schema" 2>&1) || {
	echo "$out"
	die "Failed to validate $schema"
  }
  echo "Schema ${schema%.json} ok"
done

for example in example/*.example.*json ; do
  schema="${example#*/}"
  schema="${schema%%.*}"
  out=$( "$validate" "$schema".json "$example" 2>&1 ) ; ret=$?
  case "$example" in
	*.fail*)
		case "$ret" in
			0) die "$example: should have failed" ;;
			1) echo "${example#*/}: ok: failed as expected" ;;
			2) echo "$out" >&2 ;
			   die "$schema schema validation failed" ;;
			*) echo "$out" >&2 ;
			   die "$example: Unexpected return code ($ret)"
		esac
        ;;
	*)
		case "$ret" in
			0) echo "${example#*/}: ok" ;;
			1) echo "$out" >&2 ;
			   die "$schema validation failed" ;;
			2) echo "$out" >&2 ;
			   die "$schema schema validation failed" ;;
			*) echo "$out" >&2 ;
			   die "$example: Unexpected return code ($ret)"
		esac
        ;;
  esac
done
