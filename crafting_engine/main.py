from core.database import engine, Base
from core.models import __all__

def run_application():
    # STEP 1: The settings are loaded via 'settings = Settings(...)'
    # which reads from your .env files and validates required variables (like database_url).
    print("Application Configuration Loaded.")

    # STEP 2: Now that the config is stable, we initialize the schema.
    Base.metadata.create_all(engine)



if __name__ == "__main__":
    run_application()