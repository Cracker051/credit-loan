import os
import secrets


def get_secret_key():
  env_var_name = 'SECRET_KEY'
  env_secret_key = os.environ.get(env_var_name)
  if env_secret_key:
    return env_secret_key
  
  print(f"WARN: the environment variable '{env_var_name}' is not set")
  # Generates a random key of 50 characters
  random_key = secrets.token_urlsafe(50)
  print("Using a randomly generated key:", random_key)
  return random_key  
