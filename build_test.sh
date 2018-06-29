#!/usr/bin/env bash

sleep 5

vectorization_works = curl -s vectorization_container:8081 | grep "This is a vectorization service for Data Science"
prediction_works  = curl -s prediction_container:8082 | grep "This is a prediction service for Data Science"
if [[ -z $vectorization_works ]] && [[ -z $prediction_works ]]
then
    echo "The build seems to be correct."
    exit 0
else
    echo "Test didn't pass. There is something wrong."
    exit 1
fi