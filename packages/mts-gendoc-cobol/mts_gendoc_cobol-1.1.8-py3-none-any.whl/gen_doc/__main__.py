import argparse as ap
import os
import sys
import time
import subprocess
import shutil
import logging
from datetime import datetime
from subprocess import PIPE
from tqdm import tqdm

# Optional color support on Windows (colorama). If not installed, script continues without it.
try:
    import colorama
    _COLORAMA_AVAILABLE = True
except Exception:
    colorama = None
    _COLORAMA_AVAILABLE = False

# Global logger
logger = logging.getLogger("gendoc")

# Main function
def main():
    # Styling tokens (ANSI). These emulate a GitHub-like palette in terminals that support ANSI.
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    GH_TITLE = "\033[97m"   # bright white
    GH_ACCENT = "\033[96m"  # cyan / accent
    GH_SUCCESS = "\033[92m" # green
    GH_MUTED = "\033[90m"   # muted gray
    GH_ERROR = "\033[91m"   # bright red
    GH_WARN = "\033[93m"    # yellow

    # Parse command line arguments with consistent, styled help text
    parser = ap.ArgumentParser(description=(f"{BOLD}{GH_TITLE}Automate COBOL documentation generation using Copilot.{RESET}"))

    parser.add_argument(
        "-p", "--Prompt", type=str, required=True,
        help=(f"{GH_ACCENT}{BOLD}Prompt directory{RESET} — {ITALIC}Directory containing .txt prompt templates used to instruct Copilot.{RESET}")
    )

    parser.add_argument(
        "-c", "--Cobol", type=str, required=True,
        help=(f"{GH_ACCENT}{BOLD}COBOL source{RESET} — {ITALIC}COBOL file or directory to document (supports .cbl/.cob).{RESET}")
    )

    parser.add_argument(
        "-sf","--Start-From", type=int, default=1,
        help=(f"{GH_ACCENT}{BOLD}Start From{RESET} — {ITALIC}Optional file index to start from (default: 1).{RESET}")

    )

    parser.add_argument(
        "-o", "--Output", type=str,
        help=(f"{GH_ACCENT}{BOLD}Output directory{RESET} — {ITALIC}Where generated documentation files will be written (default: ./Cobol_Documentation_Output).{RESET}")
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help=(f"{GH_SUCCESS}{BOLD}Verbose{RESET} — {ITALIC}Enable INFO-level logging to console.{RESET}")
    )

    parser.add_argument(
        "-d", "--debug", action="store_true",
        help=(f"{GH_SUCCESS}{BOLD}Debug{RESET} — {ITALIC}Enable DEBUG-level logging (overrides --verbose).{RESET}")
    )

    parser.add_argument(
        "--log-file", type=str,
        help=(f"{GH_ACCENT}{BOLD}Log file{RESET} — {ITALIC}Optional path for a log file. If omitted, a timestamped log is created in the output directory.{RESET}")
    )

    args = parser.parse_args()

    # Initialize colorama on Windows if available so ANSI escapes render correctly.
    if _COLORAMA_AVAILABLE:
        try:
            colorama.init(autoreset=True)
            logger.debug("Colorama initialized for ANSI support")
        except Exception:
            logger.debug("Colorama import succeeded but initialization failed")

    # Determine output path early (may be None)
    output_path = args.Output if args.Output else os.path.join(os.getcwd(), "Cobol_Documentation_Output")
    # Prepare log file path (use provided or default timestamped inside output path)
    log_file = args.log_file  # attribute name from argparse will be log_file
    if log_file is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(output_path, f"gendoc_{ts}.log")

    # Configure logging
    console_level = logging.WARNING
    if args.verbose:
        console_level = logging.INFO
    if args.debug:
        console_level = logging.DEBUG
    logger.setLevel(logging.DEBUG)  # master logger always at DEBUG
    logger.handlers.clear() # remove any existing handlers
    # Create a colored console formatter for better readability; keep the file formatter plain.
    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level = record.levelno
            name = record.levelname
            if level >= logging.ERROR:
                color = GH_ERROR
            elif level >= logging.WARNING:
                color = GH_WARN
            elif level >= logging.INFO:
                color = GH_SUCCESS
            else:
                color = GH_ACCENT
            # Wrap levelname with color
            record.levelname = f"{color}{BOLD}{name}{RESET}"
            return super().format(record)

    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    console_formatter = ColoredFormatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(console_level)
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    # File handler (always debug level) - plain formatting
    try:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)
    except OSError as e:
        # Fall back to console only if file cannot be created
        logger.error(f"Failed to create log file '{log_file}': {e}")

    logger.debug("Logger initialized")
    logger.info(f"Log file: {log_file}")
    logger.debug(f"Arguments parsed: {args}")

    try:
        prompt_path = args.Prompt
        cobol_path = args.Cobol
        logger.debug(f"Prompt path: {prompt_path}")
        logger.debug(f"Cobol path: {cobol_path}")
        logger.debug(f"Output path (pre-validation): {output_path}")

        if not os.path.exists(prompt_path):
            logger.error(f"Prompt path '{prompt_path}' does not exist.")
            sys.exit(1)
        logger.debug("Prompt path exists.")

        if not os.path.exists(cobol_path):
            logger.error(f"COBOL path '{cobol_path}' does not exist.")
            sys.exit(1)
        logger.debug("COBOL path exists.")

        if args.Output is None:
            logger.info(f"No output path provided. Using default: '{output_path}'")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info(f"Created output directory at '{output_path}'.")
        else:
            logger.debug("Output directory already exists.")

        copilot_cmd = shutil.which("copilot")
        if copilot_cmd is None:
            logger.error("'copilot' command not found. Please ensure Copilot is installed and in your PATH.")
            sys.exit(1)
        logger.info(f"Copilot command resolved to: {copilot_cmd}")
        logger.debug(f"Environment PATH: {os.environ.get('PATH','<unset>')}")

        logger.info("Validation steps completed successfully. Moving to documentation generation...")
        start_overall = time.time()

        if os.path.isfile(cobol_path):
            logger.info("Processing single COBOL file...")
            process_cobol_file(cobol_path, prompt_path, output_path)
        else:
            logger.debug("Collecting files from directory.")
            cobol_files = []
            for root, _, files in os.walk(cobol_path):
                logger.debug(f"Scanning directory: {root}")
                for file in files:
                    lower = file.lower()
                    extensions = [".c",".mak",".cbl",".cob",".h",".mx3",".exp",".mx1"]
                    if any(lower.endswith(ext) for ext in extensions):
                        cobol_file_path = os.path.join(root, file)
                        cobol_files.append(cobol_file_path)
                        logger.debug(f"Added file: {cobol_file_path}")

            if not cobol_files:
                logger.warning(f"No COBOL files found in '{cobol_path}'.")
                return

            logger.info(f"Found {len(cobol_files)} COBOL file(s) to process...")
            for f in cobol_files:
                logger.debug(f"File queued: {f}")

            # Honor the Start-From argument (argparse converts option name 'Start-From' to attribute 'Start_From')
            try:
                start_from = int(getattr(args, 'Start_From', 1))
            except Exception:
                start_from = 1
            if start_from < 1:
                logger.warning(f"Invalid Start-From value {start_from}; using 1.")
                start_from = 1

            start_index = start_from - 1  # convert 1-based to 0-based index
            if start_index >= len(cobol_files):
                logger.warning(f"Start-From index {start_from} is beyond the number of files ({len(cobol_files)}). No files will be processed.")
                cobol_files_to_process = []
            else:
                cobol_files_to_process = cobol_files[start_index:]
                logger.info(f"Processing files starting from index {start_from} (file: {os.path.basename(cobol_files[start_index])}). {len(cobol_files_to_process)} file(s) will be processed.")

            for cobol_file_path in tqdm(cobol_files_to_process, desc="Processing COBOL files", unit="file"):
                process_cobol_file(cobol_file_path, prompt_path, output_path)

        elapsed = time.time() - start_overall
        logger.info(f"Documentation generation completed in {elapsed:.2f}s.")
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        sys.exit(1)
    except SystemExit:
        raise
    except Exception:
        logger.exception("Unexpected error encountered.")
        sys.exit(1)


def process_cobol_file(cobol_file_path, prompt_path, output_path):
    file_name = os.path.basename(cobol_file_path)
    logger.debug(f"Begin processing file: {file_name}")
    start_file = time.time()
    try:
        prompt_files = [file for file in os.listdir(prompt_path) if file.endswith(".txt")]
        logger.debug(f"Prompt files discovered: {prompt_files}")
    except OSError as e:
        logger.error(f"Error accessing prompt directory '{prompt_path}': {e}")
        return

    if not prompt_files:
        logger.warning(f"No prompt files found in '{prompt_path}'. Skipping file '{file_name}'.")
        return

    for idx, prompt_file in enumerate(tqdm(prompt_files, desc=f"Processing {file_name}", unit="prompt", leave=False), start=1):
        logger.debug(f"Processing prompt {idx}/{len(prompt_files)}: {prompt_file}")
        prompt_file_path = os.path.join(prompt_path, prompt_file)
        try:
            with open(prompt_file_path, 'r', encoding='utf-8', errors='replace') as pf:
                prompt_content = pf.read()
            logger.debug(f"Loaded prompt file '{prompt_file}' size={len(prompt_content)} bytes")
        except OSError as e:
            msg = f"Failed to read prompt file '{prompt_file}': {e}"
            tqdm.write(msg)
            logger.error(msg)
            continue

        final_prompt = f"{prompt_content}. Please generate documentation for the following COBOL code:{cobol_file_path}"
        command = shutil.which("copilot")
        if command is None:
            msg = "'copilot' command became unavailable. Aborting further processing."
            tqdm.write(msg)
            logger.error(msg)
            return
        logger.debug(f"Copilot command for this prompt: {command}")
        cmd = [command, "-p", final_prompt, "--allow-all-tools","--model", "gpt-5"]
        logger.debug(f"Subprocess command list: {cmd}")
        start_time = time.time()
        try:
            process = subprocess.run(cmd, stdout=PIPE, stderr=PIPE, check=True)
            stdout, stderr = process.stdout, process.stderr
        except OSError as e:
            msg = f"Subprocess launch failed for '{file_name}' with prompt '{prompt_file}': {e}"
            tqdm.write(msg)
            logger.error(msg)
            continue
        duration = time.time() - start_time
        logger.debug(f"Subprocess finished in {duration:.2f}s returncode={process.returncode} stdout_size={len(stdout)} stderr_size={len(stderr)}")

        output_file_name = f"{os.path.basename(cobol_file_path)}_{os.path.splitext(prompt_file)[0]}_documentation.txt"
        output_file_path = os.path.join(output_path, output_file_name)
        try:
            with open(output_file_path, 'wb') as out_file:
                out_file.write(stdout)
            logger.debug(f"Wrote output file '{output_file_name}' size={len(stdout)} bytes")
        except OSError as e:
            msg = f"Failed writing output file '{output_file_name}': {e}"
            tqdm.write(msg)
            logger.error(msg)
            continue

        if process.returncode != 0:
            err_text = stderr.decode(errors='replace')
            tqdm.write(f"Error generating documentation for '{cobol_file_path}' with prompt '{prompt_file}': {err_text}")
            logger.error(f"Copilot returned non-zero exit code for '{file_name}' prompt '{prompt_file}': {err_text}")
        else:
            tqdm.write(f"Successfully generated documentation for '{file_name}' with prompt '{prompt_file}'.")
            logger.info(f"Documentation generated for '{file_name}' prompt '{prompt_file}'")
    elapsed_file = time.time() - start_file
    logger.debug(f"Finished processing file: {file_name} in {elapsed_file:.2f}s")

if __name__ == "__main__":
    main()