#!/bin/bash

echo 'Waiting for nomad...'
while true
do
  START=`nomad node-status | grep "ready"`
  if [ -n "$START" ]; then
    break
  else
    sleep 2
  fi
done
echo 'Deploying openfaas components...'
nomad job run /vagrant/contrib/nomad/faas.hcl