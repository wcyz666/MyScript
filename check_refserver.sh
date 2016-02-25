#!/bin/bash

url_q1="http://q1-1848733628.us-east-1.elb.amazonaws.com/q2?userid=2324314004&hashtag=LinkedIn"

content=`curl -s "$url_q1"`

sample=`cat sample`


if [ "$content" = "$sample" ]; then
	echo "Check OK on : "`date`
else
	echo "Server down on : "`date`
	echo -e "Q2 reference server gives: $content" | mail -s "[Urgent] Reference Server has trouble!!!!" cheng.wang@sv.cmu.edu
	echo -e "Q2 reference server gives: $content" | mail -s "[Urgent] Reference Server has trouble!!!!" xranthoar@gmail.com
	echo -e "Q2 reference server gives: $content" | mail -s "[Urgent] Reference Server has trouble!!!!" xiaodi.larry@gmail.com
	echo -e "Q2 reference server gives: $content" | mail -s "[Urgent] Reference Server has trouble!!!!" starking192@gmail.com
fi
