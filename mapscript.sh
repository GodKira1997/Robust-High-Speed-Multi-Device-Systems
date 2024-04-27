nameserver=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}')   # find nameserver
[ -n "$nameserver" ] || "unable to find nameserver" || exit 1            # exit immediately if nameserver was not found
echo "##### nameserver found: '$nameserver'"
localhost_entry=$(grep -v "127.0.0.1" /etc/hosts | grep "\slocalhost$")  # find localhost entry excluding 127.0.0.1
if [ -n "$localhost_entry" ]; then                                       # if localhost entry was found
    echo "##### localhost entry found: '$localhost_entry'"
    sed -i "s/$localhost_entry/$nameserver localhost/g" /etc/hosts       # then update localhost entry with the new $nameserver
else                                                                     # else if entry was not found
    echo "##### localhost entry not found"
    echo "$nameserver localhost" >> /etc/hosts                           # then append $nameserver mapping to localhost
fi
cat /etc/hosts                                                           # display to confirm
