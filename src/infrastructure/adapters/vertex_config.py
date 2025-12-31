def setup_vertex_env():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.getenv("VERTEX_AI_PROJECT_ID"))
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

    yield
