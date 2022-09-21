from dotenv import dotenv_values
Credentials = dotenv_values(".env")

JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
CORS_HEADERS = 'Content-Type'
MONGODB_SETTINGS = {
    'host': 'mongodb+srv://{}:{}@cluster0.nvhyrvk.mongodb.net/?retryWrites=true&w=majority' .format(Credentials["user"], Credentials["password"])   
}
PROPAGATE_EXCEPTIONS = True