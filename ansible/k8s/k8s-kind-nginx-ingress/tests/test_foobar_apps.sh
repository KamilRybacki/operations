#!/bin/bash

MANIFEST_URL="https://kind.sigs.k8s.io/examples/ingress/usage.yaml"

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

echo "Testing the foo app"
FOO_STATUS_CODE=$(curl \
  -s \
  -k \
  -o /dev/null \
  -w "%{http_code}" \
  0.0.0.0/foo/hostname
)
echo "Foo app status code: $FOO_STATUS_CODE"
if [ "$FOO_STATUS_CODE" -ne 200 ]; then
  echo "Foo app failed"
  STATUS=1
fi

echo "Testing the bar app"
BAR_STATUS_CODE=$(curl \
  -s \
  -k \
  -o /dev/null \
  -w "%{http_code}" \
  0.0.0.0/bar/hostname
)
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
