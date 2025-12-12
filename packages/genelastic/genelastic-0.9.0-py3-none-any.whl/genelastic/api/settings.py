from environs import Env

env = Env()
env.read_env()

# Load required environment variables.
GENAPI_ES_URL = env.url("GENAPI_ES_URL").geturl()
GENAPI_ES_ENCODED_API_KEY = env.str("GENAPI_ES_ENCODED_API_KEY")
GENAPI_ES_INDEX_PREFIX = env.str("GENAPI_ES_INDEX_PREFIX")
GENAPI_ES_CERT_FP = env.str("GENAPI_ES_CERT_FP")
