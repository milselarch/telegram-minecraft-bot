Telegram chatbot running serverlessly off google cloud functions to turn on / off a minecraft server, and a script to auto-shutdown the server when theres no players online; so as to save on server operating costs.

Deploy telegram bot cloud function using:
```
gcloud beta functions deploy webhook --runtime python38 \
--trigger-http --env-vars-file .env.yaml
```