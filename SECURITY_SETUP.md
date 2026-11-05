# Security setup
Set GENERATOR_ACCESS_TOKEN to a randomly generated secret of at least 32 characters using the hosting secret store. Never commit it. Send Authorization: Bearer <token> over HTTPS. Without this secret generation is disabled.
Limits: 5 generation attempts per rolling minute and 100 per rolling 24 hours, including failed upstream requests. max_tokens is limited to 1600 and topic to 500 characters.
QUOTA_DB_PATH must point to a writable persistent volume. SQLite is shared by processes on one host; multiple replicas require a shared external quota service. Redeployment with ephemeral storage resets the quota: do not deploy this configuration with ephemeral storage or multiple replicas.
GET /generate is retained for Zapier compatibility. Configure the Authorization header in Zapier's secret fields before enabling the automation.
Before exposing the service, set provider spending limits and run the full integration tests. This PR does not configure hosting or provider limits.
