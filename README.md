# Analyse de sentiments avec Flask
API d'analyse de sentiments avec Flask. 
API accessible via un système de pseudo/mot de passe, disposant de deux modèles d'analyse de sentiment avec des restrictions d'accès aux versions d'api selon l'utilisateur

# Code de l'API
# Tests / Utilisation

	Pour les pages ou route inexistantes 
http://localhost:5000/testapi


curl -X GET -i http://localhost:5000/testapi

	Route /status
http://localhost:5000/status


curl -X GET -i http://localhost:5000/status

	Route /welcome
http://localhost:5000/welcome?username=Anika&password=8944


# Utilisateur existant :
curl -X GET -i 'http://localhost:5000/welcome?username=Anika&password=8944'

# Utilisateur non existant :
curl -X GET -i 'http://localhost:5000/welcome?username=Anika1&password=8944'

# Utilisateur avec mauvais mot de passe :
curl -X GET -i 'http://localhost:5000/welcome?username=Anika&password=89441'

# Utilisateur avec mot de passe format non valide (string au lieu integer) :
curl -X GET -i 'http://localhost:5000/welcome?username=Anika&password=8944a'


# Route /permissions
# Cas 1 (v1=0 et v2=1)
curl -X 'POST' -i \
  'http://127.0.0.1:5000/permissions' \
  -H 'Content-Type: application/json' \
  -d '{
    "username":"Anika",
    "password":8944
}'

# Cas 2 (v1=1 et v2=0)
curl -X 'POST' -i \
  'http://127.0.0.1:5000/permissions' \
  -H 'Content-Type: application/json' \
  -d '{
    "username":"Mara",
    "password":9820
}'

# Cas 3 (v1=1 et v2=1)
curl -X 'POST' -i \
  'http://127.0.0.1:5000/permissions' \
  -H 'Content-Type: application/json' \
  -d '{
    "username":"Amber",
    "password":9274
}'

# Route /v1/permissions
# Cas 1 sans le header Authorization :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -d '{
    "sentence":"This is bad news"
}'

# Cas 2 utilisateur qui n’existe pas :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Georges=8944'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 3 utilisateur qui avec mauvais mot de passe :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Anika=89441'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 4 utilisateur qui n’a pas droit à la v1 :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Anika=8944'\
  -d '{
    "sentence":"This is bad news"
}'


# Cas 5 utilisateur qui a droit à la v1 avec score négatif :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Piper=2914'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 6 utilisateur qui a droit à la v1 avec score positif :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v1/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Piper=2914'\
  -d '{
    "sentence":"This is good news"
}'


# Route /v2/permissions
# Cas 1 sans le header Authorization :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -d '{
    "sentence":"This is bad news"
}'

# Cas 2 utilisateur qui n’existe pas :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Georges=8944'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 3 utilisateur qui avec mauvais mot de passe :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Anika=89441'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 4 utilisateur qui n’a pas droit à la v2 :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Rhiannon=3545'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 5 utilisateur qui a droit à la v2 avec score négatif :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Lionel=4527'\
  -d '{
    "sentence":"This is bad news"
}'

# Cas 6 utilisateur qui a droit à la v1 avec score positif :
curl -X 'POST' -i \
  'http://127.0.0.1:5000/v2/sentiment' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Lionel=4527'\
  -d '{
    "sentence":"This is good news"
}'
