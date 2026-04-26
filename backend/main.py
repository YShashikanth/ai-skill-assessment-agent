from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import fitz
from io import BytesIO
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file):
    text = ""

    try:
        file_bytes = file.file.read()

        try:
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
        except:
            pass

        if len(text.strip()) < 50:
            print("Using PyMuPDF fallback...")
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()

        print("FINAL TEXT LENGTH:", len(text))

    except Exception as e:
        print("PDF ERROR:", e)

    return text.strip()


def read_file(file: UploadFile):
    if not file:
        return ""

    try:
        if file.filename.endswith(".pdf"):
            return extract_text_from_pdf(file)

        return file.file.read().decode(errors="ignore").strip()

    except Exception as e:
        print("READ ERROR:", e)
        return ""


@app.post("/analyze")
async def analyze(
    resume_text: str = Form(None),
    jd_text: str = Form(None),
    resume_file: UploadFile = File(None),
    jd_file: UploadFile = File(None),
):
    try:
        resume = resume_text or read_file(resume_file)
        jd = jd_text or read_file(jd_file)

        # 🔥 Allow partial success
        if not resume and not jd:
            return {
                "success": False,
                "error": "Could not extract text from both files."
            }

        if not resume:
            print("WARNING: Resume extraction failed")

        if not jd:
            print("WARNING: JD extraction failed")

        result = run_agent(resume, jd)

        return {
            "success": True,
            "data": result,
            "resume_text": resume,
            "jd_text": jd
        }

    except Exception as e:
        return {"success": False, "error": str(e)}