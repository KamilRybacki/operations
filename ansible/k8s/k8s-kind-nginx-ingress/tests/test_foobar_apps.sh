#!/bin/bash

MANIFEST_URL=/home/kamil/Projekty/Moje/operations/ansible/k8s/k8s-kind-nginx-ingress/tests/test_services.yaml

echo "Creating the ingress"
kubectl \
  apply \
    -f \
      $MANIFEST_URL

echo "Waiting for the ingress to be ready"
kubectl \
  wait \
    --for=condition=ready \
    pod \
      --all \
      --timeout=300s

echo "Testing the ingress"

CLUSTER_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

FOO_CURL_COMMAND="curl -X GET -s -k -o /dev/null -w \"%{http_code}\" 0.0.0.0/foo/hostname"
BAR_CURL_COMMAND="curl -X GET -s -k -o /dev/null -w \"%{http_code}\" 0.0.0.0/bar/hostname"

echo "Testing the foo app"
FOO_STATUS_CODE=$(eval $FOO_CURL_COMMAND)
echo "Foo app status code: $FOO_STATUS_CODE"
if [ "$FOO_STATUS_CODE" -ne 200 ]; then
  echo "Foo app failed"
  STATUS=1
fi

echo "Testing the bar app"
BAR_STATUS_CODE=$(eval $BAR_CURL_COMMAND)
echo "Bar app status code: $BAR_STATUS_CODE"
if [ "$BAR_STATUS_CODE" -ne 200 ]; then
  echo "Bar app failed"
  STATUS=1
fi

echo "Cleaning up"
kubectl \
  delete \
    -f \
      $MANIFEST_URL

if [ "$STATUS" -eq 0 ]; then
  echo "All tests passed"
else
  echo "Some tests failed"
fi
exit "$STATUS"
