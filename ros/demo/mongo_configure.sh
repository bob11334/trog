IP=10.42.0.29 
iptables -A INPUT -s $IP -p tcp --destination-port 27017 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -d $IP -p tcp --source-port 27017 -m state --state ESTABLISHED -j ACCEPT
