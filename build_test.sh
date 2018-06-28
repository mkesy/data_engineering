#!/usr/bin/env bash

sleep 5

if curl -s decontainer:80 | grep "This is a service for Data Science"

then
    echo "The build seems to be correct."
    exit 0
else
    echo "Test didn't pass. There is something wrong."
    exit 1
fi