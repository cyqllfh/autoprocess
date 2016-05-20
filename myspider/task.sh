#!/bin/bash
cd /home/chu/workspace/git/myspider
pwd
echo "crawling begin"
/usr/local/bin/scrapy crawl nuomi
filename=`ls |grep json`
expect << EOF
set timeout 10
spawn scp -o StrictHostKeyChecking=no ${filename} root@192.168.1.13:/opt/nuomi
expect {
 "refused"       {exit 1}
 "unreachable"   {exit 1}
 "No route"      {exit 1}
 "*assword*"     {send "123456\n"}
 timeout         {exit 1}
 eof             {exit 1}
}
expect eof
EOF
echo "crawling end"
echo " rm ${filename}"
rm ${filename}
cd ../python-kafka/dataproducer
echo "send message"
python HDFSProducer.py ${filename}
