import logging
from prepare_pdfs import sanitize_fences
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

src = Path(r"..\OUTPUT\testout1.0.7\mpa_auto_rls.cbl\mpa_auto_rls.cbl_prompt2_documentation.md").resolve()
dst = Path("out_sanitized.md").resolve()

logger.info('Reading %s', src)
content = src.read_text(encoding='utf-8')
san = sanitize_fences(content, logger)
dst.write_text(san, encoding='utf-8')
logger.info('Wrote sanitized output to %s', dst)

print('---SANITIZED START---')
print(san[:2000])
print('---SANITIZED END---')
