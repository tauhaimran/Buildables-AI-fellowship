import tempfile
import soundfile as sf

def save_uploaded_audio(uploaded_file):
    """Save an uploaded audio file to a temp file and return the path"""
    # ✅ Use .name instead of .filename
    suffix = "." + uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    return tmp_path