import hashlib
import os
from pathlib import Path

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "01_Constitution"
OUTPUT_DIR = BASE_DIR / "03_Application"
OUTPUT_PDF = OUTPUT_DIR / "ScentID_Master_Archive_LOCKED.pdf"
ENV_FILE = BASE_DIR / ".env"


def load_env(env_path: Path) -> dict:
    values = {}
    if not env_path.exists():
        return values
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def collect_protocol_texts() -> str:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"Missing constitution directory: {SOURCE_DIR}")

    text_files = sorted(
        [p for p in SOURCE_DIR.iterdir() if p.suffix.lower() in {".md", ".txt"}]
    )
    if not text_files:
        raise FileNotFoundError("No .md or .txt protocol files found in 01_Constitution")

    chunks = []
    for file_path in text_files:
        body = file_path.read_text(encoding="utf-8", errors="replace")
        chunks.append(f"# FILE: {file_path.name}\n\n{body}\n")
    return "\n" + ("\n" + ("-" * 80) + "\n").join(chunks)


def build_pdf(content: str, owner_password: str, user_password: str = "") -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_title("Scent-ID Master Archive")
    pdf.set_author("Scent-ID Command Authority")
    pdf.set_creator("build_locked_pdf.py")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Scent-ID Master Archive", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, "Locked protocol export", ln=1)
    pdf.ln(4)
    pdf.set_font("Courier", "", 10)

    for line in content.splitlines():
        safe = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 5, safe)

    # fpdf2 supports PDF permission restrictions.
    if hasattr(pdf, "set_protection"):
        pdf.set_protection(
            perm=[],
            user_pwd=user_password,
            owner_pwd=owner_password,
        )

    pdf.output(str(OUTPUT_PDF))


def main() -> None:
    env = load_env(ENV_FILE)
    owner_pwd = env.get("MASTER_PDF_OWNER_PASSWORD", "")
    if not owner_pwd:
        owner_pwd = hashlib.sha256(os.urandom(32)).hexdigest()

    user_pwd = env.get("MASTER_PDF_USER_PASSWORD", "")
    archive_text = collect_protocol_texts()

    build_pdf(content=archive_text, owner_password=owner_pwd, user_password=user_pwd)
    print(f"Locked PDF generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
