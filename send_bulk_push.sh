#!/bin/bash

# Config
FASTAPI_URL="http://148.253.86.63:8001/bulk-push"
REGISTER_NAME="Temperature_value"
REGISTER_TYPE="T"
REGISTER_DID="0"
VALUE1="100"
VALUE2="105"
DELTA=60
OFFSET=70  # décalage en secondes

# 1. Récupérer le timestamp de VictoriaMetrics et ajouter le décalage
TS=$(($(curl -s 'http://148.253.86.63:8428/api/v1/query?query=time()' \
  | grep -o '[0-9]\{10\}' | head -1) + OFFSET))

# 2. Construire le payload JSON avec tous les champs requis
PAYLOAD=$(cat <<EOF
{
  "registers": [
    { "name": "$REGISTER_NAME", "type": "$REGISTER_TYPE", "did": "$REGISTER_DID" }
  ],
  "ranges": [
    {
      "ts": $TS,
      "delta": $DELTA,
      "rows": [
        ["$VALUE1"],
        ["$VALUE2"]
      ]
    }
  ]
}
EOF
)

# 3. Afficher le payload pour debug
echo "Payload envoyé :"
echo "$PAYLOAD"

# 4. Envoyer la requête
curl -XPOST "$FASTAPI_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

