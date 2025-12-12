#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Helper tool for the generation of versioned documentation files.

Build Sphinx docs for every stable tag (excluding rc/alpha/beta),
label highest tag as "stable", optionally label current branch as "dev" if it's ahead.
Generates a versions.json and creates redirect index pages for stable/dev.
Now with optional PDF generation!

Requirements:
 - Git with worktree support
 - sphinx-build available on PATH (install Sphinx in the env)
 - For PDF: latexmk and pdflatex (TeX Live or similar)

.. click:: mafw.scripts.doc_versioning:cli
    :prog: multiversion-doc
    :nested: full
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, List, Tuple

import click
from packaging.version import InvalidVersion, Version

# ---------------------------
# Configurable defaults
# ---------------------------
DEFAULT_MIN_TAG_REGEX = r'^v([1-9][0-9]*)\.[0-9]+\.[0-9]+(\.[0-9]+)?$'
# The files/directories under each worktree where docs live
DOCS_SUBPATH = Path('docs') / 'source'
SPHINX_BUILD_CMD = 'sphinx-build'  # ensure on PATH
OLD_VERSION_TO_BE_PATCHED = ['v1.0.0', 'v1.1.0', 'v1.2.0', 'v1.3.0', 'v1.4.0']

# ---------------------------


def run(cmd: List[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Helper to run commands with consistent behavior.

    :param cmd: Command to execute as a list of strings
    :type cmd: List[str]
    :param cwd: Working directory for command execution, defaults to None
    :type cwd: Path | None
    :return: Completed process result
    :rtype: subprocess.CompletedProcess[str]
    """
    print(f'🧩 Running: {" ".join(cmd)}')
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)


def get_git_tags(min_version: str | None = None) -> List[Tuple[Version, Any]]:
    """Return list of (Version, tag) tuples sorted ascending.

    :param min_version: Minimum version to consider, defaults to None
    :type min_version: str | None
    :return: List of (Version, tag) tuples
    :rtype: List[Tuple[Version, Any]]
    """
    out = run(['git', 'tag'])
    tags = out.stdout.split()
    versions = []
    for t in tags:
        try:
            v = Version(t)
            if v.is_prerelease or v.is_devrelease:
                continue
            if min_version and v < Version(min_version):
                continue
            versions.append((v, t))
        except InvalidVersion:
            continue
    versions.sort()
    return versions


def filter_latest_micro(versions: List[Tuple[Version, Any]]) -> List[Tuple[Version, Any]]:
    """Keep only the latest micro version per minor (major.minor).

    :param versions: List of (Version, tag) tuples
    :type versions: List[Tuple[Version, Any]]
    :return: Filtered list of (Version, tag) tuples
    :rtype: List[Tuple[Version, Any]]
    """
    latest_per_minor: dict[Tuple[int, int], Tuple[Version, Any]] = {}
    for v, tag in versions:
        key = (v.major, v.minor)
        if key not in latest_per_minor or v > latest_per_minor[key][0]:
            latest_per_minor[key] = (v, tag)
    return sorted(latest_per_minor.values())


def filter_stable_tags(tags: List[str], regex: str) -> List[str]:
    """Filter tags based on a regular expression pattern.

    :param tags: List of tag strings to filter
    :type tags: List[str]
    :param regex: Regular expression pattern to match against
    :type regex: str
    :return: Filtered list of matching tags
    :rtype: List[str]
    """
    pattern = re.compile(regex)
    return [t for t in tags if pattern.match(t)]


def parse_version_tuple(tag: str) -> Tuple[int, ...]:
    """Parse vX.Y.Z(.W) into tuple of ints for sorting.

    :param tag: Version tag string
    :type tag: str
    :return: Tuple of integers representing the version
    :rtype: Tuple[int, ...]
    """
    if tag.startswith('v'):
        tag = tag[1:]
    parts = tag.split('.')
    # only take numeric parts
    nums = []
    for p in parts:
        if p.isdigit():
            nums.append(int(p))
        else:
            # stop on strange parts; but ideally regex filters those out
            break
    return tuple(nums)


def get_current_branch() -> str:
    """Get the name of the currently checked out branch.

    :return: Name of the current branch
    :rtype: str
    """
    out = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    return out.stdout.strip()


def sort_tags_semver(tags: List[str]) -> List[str]:
    """Sort tags using semantic versioning comparison.

    :param tags: List of tag strings to sort
    :type tags: List[str]
    :return: Sorted list of tag strings
    :rtype: List[str]
    """
    return sorted(tags, key=lambda t: parse_version_tuple(t))


def git_rev_of(ref: str) -> str:
    """Get the git revision hash for a given reference.

    :param ref: Git reference (tag, branch, commit hash)
    :type ref: str
    :return: Git revision hash
    :rtype: str
    :raises RuntimeError: If git rev-list fails
    """
    proc = run(['git', 'rev-list', '-n', '1', ref])
    if proc.returncode != 0:
        raise RuntimeError(f'git rev-list failed for {ref}:\n{proc.stdout}')
    return proc.stdout.strip()


def is_ancestor(a: str, b: str) -> bool:
    """Return True if commit a is ancestor of commit b (git merge-base --is-ancestor).

    :param a: First commit reference
    :type a: str
    :param b: Second commit reference
    :type b: str
    :return: True if a is ancestor of b
    :rtype: bool
    """
    proc = run(['git', 'merge-base', '--is-ancestor', a, b])
    return proc.returncode == 0


def copy_patch_files(docs_src: Path) -> None:
    """Copy patch files needed for older versions.

    :param docs_src: Path to documentation source directory
    :type docs_src: Path
    """
    # Define the patch files to copy
    patch_files = [
        ('docs/source/conf.py', docs_src / 'conf.py'),
        ('docs/source/_static/js/version-switcher.js', docs_src / '_static/js/version-switcher.js'),
        ('docs/source/_templates/versions.html', docs_src / '_templates/versions.html'),
        ('docs/source/_ext/procparams.py', docs_src / '_ext/procparams.py'),
    ]

    # Create directories and copy files
    for src_path, dst_path in patch_files:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path.cwd() / src_path, dst_path)


def parse_sphinx_log(log_content: str) -> Tuple[int, int, List[str]]:
    """
    Parse Sphinx build log to extract warning and error counts, and warning messages.

    Only three warnings are reported

    :param log_content: Sphinx build log
    :type log_content: str
    :return: Tuple of warning, error count, warning messages
    :rtype: Tuple[int, int, List[str]]
    """
    warnings = 0
    warning_messages = []

    # Look for patterns like "build succeeded, X warning(s)."
    success_pattern = re.compile(r'build succeeded(?:,\s+(\d+)\s+warning)?', re.IGNORECASE)
    match = success_pattern.search(log_content)

    if match:
        if match.group(1):
            warnings = int(match.group(1))

    # Look for explicit warning lines and extract messages
    warning_pattern = re.compile(r'^.*WARNING:.*$', re.MULTILINE | re.IGNORECASE)
    warning_lines = warning_pattern.findall(log_content)
    warnings = max(warnings, len(warning_lines))

    # Extract just the relevant part of warning messages (limit to first 3)
    # for line in warning_lines[:3]:
    #     clean_line = ' '.join(line.split())
    #     warning_messages.append(clean_line)
    warning_messages = warning_lines[:3]

    if len(warning_lines) > 3:
        warning_messages.append(f'... and {len(warning_lines) - 3} more warning(s)')

    # Look for error patterns
    error_pattern = re.compile(r'ERROR:|CRITICAL:', re.IGNORECASE)
    errors = len(error_pattern.findall(log_content))

    return warnings, errors, warning_messages


def report_build_status(tag: str, success: bool, log: str, build_type: str = 'HTML') -> None:
    """
    Report build status with warning/error summary.

    :param tag: Version tag being built
    :type tag: str
    :param success: Whether build succeeded
    :type success: bool
    :param log: Build log content
    :type log: str
    :param build_type: Type of build (HTML or PDF)
    :type build_type: str
    """
    warnings, errors, warning_messages = parse_sphinx_log(log)

    status_icon = '✅' if success else '❌'
    status_text = 'OK' if success else 'FAILED'

    print(f'{status_icon} {tag} {build_type} build {status_text}', end='')

    if warnings > 0 or errors > 0:
        details = []
        if warnings > 0:
            details.append(f'⚠️  {warnings} warning(s)')
        if errors > 0:
            details.append(f'❌ {errors} error(s)')
        print(f' ({", ".join(details)})')

        # Display warning messages if present
        if warning_messages:
            for msg in warning_messages:
                print(f'     ⚠️  {msg}')
    else:
        print(' (no warnings)')


def build_for_tag(
    tag: str, outdir: Path, tmproot: Path, use_latest_conf: bool = False, keep_tmp: bool = False
) -> Tuple[bool, str]:
    """
    Create worktree for tag, run sphinx-build, save log.
    Returns (success, log_contents).

    :param tag: Git tag to build documentation for
    :type tag: str
    :param outdir: Output directory for built documentation
    :type outdir: Path
    :param tmproot: Root temporary directory
    :type tmproot: Path
    :param use_latest_conf: Whether to use latest conf.py, defaults to False
    :type use_latest_conf: bool
    :param keep_tmp: Whether to keep temporary files, defaults to False
    :type keep_tmp: bool
    :return: Tuple of (success, log_contents)
    :rtype: Tuple[bool, str]
    """
    worktree_path = tmproot / tag
    try:
        proc = run(['git', 'worktree', 'add', '-q', str(worktree_path), tag])
        if proc.returncode != 0:
            return False, f'git worktree add failed:\n{proc.stdout}'
        docs_src = worktree_path / DOCS_SUBPATH
        if not docs_src.exists():
            return False, f'docs source {docs_src} does not exist for tag {tag}'

        if use_latest_conf or tag in OLD_VERSION_TO_BE_PATCHED:
            copy_patch_files(docs_src)

        out_for_tag = outdir / tag
        out_for_tag.mkdir(parents=True, exist_ok=True)

        # run sphinx-build and capture output
        sp = run([SPHINX_BUILD_CMD, '-b', 'html', str(docs_src), str(out_for_tag)], cwd=worktree_path)
        log = sp.stdout
        # write log
        with open(out_for_tag / 'sphinx-build.log', 'w', encoding='utf-8') as f:
            f.write(log)
        success = sp.returncode == 0
        return success, log
    finally:
        # cleanup worktree
        if not keep_tmp:
            # use -f in case the worktree wasn't properly created
            run(['git', 'worktree', 'remove', '-f', str(worktree_path)])


def build_pdf_for_tag(
    tag: str, html_tag_dir: Path, tmproot: Path, use_latest_conf: bool = False, keep_tmp: bool = False
) -> Tuple[bool, str, Path | None]:
    """
    Create worktree for tag, run sphinx-build with latex builder, then make PDF.
    Places PDF in the same directory as the HTML output for that tag.
    Returns (success, log_contents, pdf_path).

    :param tag: Git tag to build PDF for
    :type tag: str
    :param html_tag_dir: Directory containing HTML output for the tag
    :type html_tag_dir: Path
    :param tmproot: Root temporary directory
    :type tmproot: Path
    :param use_latest_conf: Whether to use latest conf.py, defaults to False
    :type use_latest_conf: bool
    :param keep_tmp: Whether to keep temporary files, defaults to False
    :type keep_tmp: bool
    :return: Tuple of (success, log_contents, pdf_path)
    :rtype: Tuple[bool, str, Path | None]
    """
    worktree_path = tmproot / f'{tag}_pdf'
    pdf_path = None
    try:
        proc = run(['git', 'worktree', 'add', '-q', str(worktree_path), tag])
        if proc.returncode != 0:
            return False, f'git worktree add failed:\n{proc.stdout}', None

        docs_src = worktree_path / DOCS_SUBPATH
        if not docs_src.exists():
            return False, f'docs source {docs_src} does not exist for tag {tag}', None

        if use_latest_conf or tag in OLD_VERSION_TO_BE_PATCHED:
            copy_patch_files(docs_src)

        # Build latex
        latex_out = tmproot / f'{tag}_latex'
        latex_out.mkdir(parents=True, exist_ok=True)

        sp = run([SPHINX_BUILD_CMD, '-b', 'latex', str(docs_src), str(latex_out)], cwd=worktree_path)
        log = sp.stdout

        if sp.returncode != 0:
            return False, f'Sphinx latex build failed:\n{log}', None

        # Run pdflatex (via make if Makefile exists, otherwise directly)
        makefile = latex_out / 'Makefile'
        if makefile.exists():
            sp_pdf = run(['make'], cwd=latex_out)
        else:
            # Find .tex file and run pdflatex
            tex_files = list(latex_out.glob('*.tex'))
            if not tex_files:
                return False, 'No .tex file found in latex output', None
            sp_pdf = run(['pdflatex', '-interaction=nonstopmode', tex_files[0].name], cwd=latex_out)

        log += '\n' + sp_pdf.stdout

        # Find generated PDF
        pdf_files = list(latex_out.glob('*.pdf'))
        if not pdf_files:
            return False, f'PDF generation failed:\n{log}', None

        # Copy PDF to the HTML tag directory
        html_tag_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = html_tag_dir / f'{tag}.pdf'
        pdf_file = latex_out / 'mafw.pdf'
        shutil.copy(pdf_file, pdf_path)

        success = sp_pdf.returncode == 0
        return success, log, pdf_path

    finally:
        if not keep_tmp:
            run(['git', 'worktree', 'remove', '-f', str(worktree_path)])


def generate_pdf_index_page(
    html_outdir: Path, pdf_info: List[dict[str, str]], project_name: str = 'Documentation'
) -> None:
    """
    Generate an HTML page listing all available PDFs.
    This page will be placed in the root html_versions directory.
    Order: stable first, then latest, then other releases sorted by version (newest first).

    :param html_outdir: Output directory for HTML files
    :type html_outdir: Path
    :param pdf_info: List of dictionaries containing PDF information
    :type pdf_info: List[dict[str, str]]
    :param project_name: Name of the project for the page title, defaults to 'Documentation'
    :type project_name: str
    """
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PDF Downloads - {project_name}</title>
    <link rel="shortcut icon" href="stable/_static/mafw-logo.svg"/>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .pdf-list {{
            list-style: none;
            padding: 0;
        }}
        .pdf-item {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px 20px;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }}
        .pdf-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
        }}
        .pdf-version {{
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
        }}
        .pdf-label {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            margin-left: 10px;
        }}
        .label-stable {{
            background: #28a745;
            color: white;
        }}
        .label-latest {{
            background: #ffc107;
            color: #000;
        }}
        .label-release {{
            background: #6c757d;
            color: white;
        }}
        .download-btn {{
            background: #3498db;
            color: white;
            padding: 8px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }}
        .download-btn:hover {{
            background: #2980b9;
        }}
        .failed {{
            opacity: 0.5;
        }}
        .failed .download-btn {{
            background: #95a5a6;
            pointer-events: none;
        }}
    </style>
</head>
<body>
    <h1>📄 PDF Documentation Downloads</h1>
    <p>Download the complete documentation in PDF format for any version:</p>
    <ul class="pdf-list">
"""

    # Sort: stable first, then latest, then releases by version (newest first)
    sorted_info = []
    stable_item = None
    latest_item = None
    release_items = []

    for info in pdf_info:
        if info['label'] == 'alias':
            continue
        if info['label'] == 'stable':
            stable_item = info
        elif info['label'] == 'latest':
            latest_item = info
        else:  # release
            release_items.append(info)

    # Sort releases by version (newest first)
    release_items.sort(key=lambda x: parse_version_tuple(x['version']), reverse=True)

    # Build final order
    if stable_item:
        sorted_info.append(stable_item)
    if latest_item:
        sorted_info.append(latest_item)
    sorted_info.extend(release_items)

    for info in sorted_info:
        label_class = f'label-{info["label"]}'
        label_text = info['label'].upper()
        item_class = '' if info['built'] else 'failed'

        if info['built']:
            # PDF is in the same directory as HTML for each version
            pdf_link = f'{info["version"]}/{info["version"]}.pdf'
            html_content += f"""
        <li class="pdf-item {item_class}">
            <div>
                <span class="pdf-version">{info['version']}</span>
                <span class="pdf-label {label_class}">{label_text}</span>
            </div>
            <a href="{pdf_link}" class="download-btn" download>Download PDF</a>
        </li>
"""
        else:
            html_content += f"""
        <li class="pdf-item {item_class}">
            <div>
                <span class="pdf-version">{info['version']}</span>
                <span class="pdf-label {label_class}">{label_text}</span>
                <span style="color: #e74c3c; margin-left: 10px;">(Build failed)</span>
            </div>
            <span class="download-btn">Unavailable</span>
        </li>
"""

    html_content += """
    </ul>
    <p style="margin-top: 40px; color: #6c757d; font-size: 0.9em;">
        💡 Tip: The PDF version contains the complete documentation for offline reading.
    </p>
</body>
</html>
"""

    # Write to root of html_versions
    pdf_page = html_outdir / 'pdf_downloads.html'
    with open(pdf_page, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'📝 Generated PDF index page: {pdf_page}')


def write_versions_json(outdir: Path, versions: List[dict[str, str]]) -> None:
    """
    Write versions information to a JSON file.

    :param outdir: Output directory for the JSON file
    :type outdir: Path
    :param versions: List of version information dictionaries
    :type versions: List[dict[str, str]]
    """
    p = outdir / 'versions.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(versions, f, indent=2)
    print(f'🧾 Wrote versions.json to {p}')
    for v in versions:
        if v['label'] == 'alias':
            sub = v['version']
        else:
            sub = v['path']
        shutil.copy(p, outdir / sub)
        shutil.copy(p, outdir / sub / 'generated')


def mirror_version(outdir: Path, src_tag: str, target_tag: str, use_symlink: bool = True) -> None:
    """
    Mirror a version directory from one tag to another.
    Can use symlinks for efficiency or copy for compatibility.

    :param outdir: Output directory containing version directories
    :type outdir: Path
    :param src_tag: Source tag directory name
    :type src_tag: str
    :param target_tag: Target tag directory name
    :type target_tag: str
    :param use_symlink: Whether to use symlink instead of copying, defaults to True
    :type use_symlink: bool
    """
    src = outdir / src_tag
    dst = outdir / target_tag

    # Remove existing destination if it exists
    if dst.exists() or dst.is_symlink():
        if dst.is_symlink():
            dst.unlink()
        else:
            shutil.rmtree(dst)

    if use_symlink:
        print(f'🔗 Symlinking {target_tag} -> {src_tag}')
        # Create relative symlink
        dst.symlink_to(src_tag, target_is_directory=True)
    else:
        print(f'🪞 Mirroring {src_tag} to {target_tag}')
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)


def write_redirect_page(outdir: Path, name: str, target_tag: str) -> None:
    """
    Create a redirect page for a version alias.

    :param outdir: Output directory for the redirect page
    :type outdir: Path
    :param name: Name of the redirect alias (e.g., 'stable', 'dev')
    :type name: str
    :param target_tag: Tag that the redirect should point to
    :type target_tag: str
    """
    d = outdir / name
    d.mkdir(parents=True, exist_ok=True)
    target = f'../{target_tag}/index.html'  # relative path from stable/index.html to tag/index
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={target}">
    <link rel="canonical" href="{target}">
    <title>Redirecting to {target_tag}</title>
  </head>
  <body>
    <p>Redirecting to <a href="{target}">{target}</a></p>
  </body>
</html>
"""
    with open(d / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'🧾 Wrote redirect page {d / "index.html"} -> {target}')


def write_legacy_redirect_page(outdir: Path) -> None:
    """
    Create a legacy redirect page at the root of the output directory.

    :param outdir: Output directory for the redirect page
    :type outdir: Path
    """
    html = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <script>
      // Detect if we're in /doc/ subdirectory and redirect accordingly
      const path = window.location.pathname;
      const targetUrl = path.startsWith('/doc/') 
        ? '/doc/stable/index.html' 
        : 'stable/index.html';
      window.location.replace(targetUrl);
    </script>
    <meta http-equiv="refresh" content="0; url=stable/index.html">
    <link rel="canonical" href="stable/index.html">
    <title>Redirecting to stable documentation</title>
  </head>
  <body>
    <p>Redirecting to <a href="stable/index.html">Documentation of the last stable release</a></p>
  </body>
</html>
"""
    d = outdir / Path('index.html')
    with open(d, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'🧾 Wrote legacy redirect page {d}')


def write_redirects_file(outdir: Path) -> None:
    """
    Create a _redirects file for GitLab Pages.

    :param outdir: Output directory for the redirects file
    :type outdir: Path
    """
    redirects_content = """# Redirects for GitLab Pages
# See: https://docs.gitlab.com/ee/user/project/pages/redirects.html

# Redirect old PDF URL to new PDF downloads page
/doc/mafw.pdf /doc/pdf_downloads.html 301

# Redirect /doc root to stable documentation
# Note: These are specific patterns to avoid redirecting /doc/pdf_downloads.html
/doc/ /doc/stable/ 301
/doc/index.html /doc/stable/index.html 301
/doc/doc_tutorial.html /doc/stable/doc_tutorial.html 301
"""

    redirects_file = outdir / '_redirects'
    with open(redirects_file, 'w', encoding='utf-8') as f:
        f.write(redirects_content)
    print(f'🔀 Wrote _redirects file: {redirects_file}')
    print('   Note: Copy this file to the public/ directory root for GitLab Pages')


def write_root_landing_page(build_root: Path, project_name: str = 'MAFw') -> None:
    """
    Create a landing page for the project root with links to documentation and coverage.

    :param build_root: Root build directory (should contain 'doc' subdirectory)
    :type build_root: Path
    :param project_name: Project name for the page title
    :type project_name: str
    """
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{project_name} - Documentation Hub</title>
    <link rel="shortcut icon" href="doc/stable/_static/mafw-logo.svg"/>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-top: 0;
        }}
        .section {{
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .section h2 {{
            color: #2c3e50;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 15px;
        }}
        .link-btn {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s;
            font-weight: 500;
        }}
        .link-btn:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
        }}
        .link-btn.secondary {{
            background: #95a5a6;
        }}
        .link-btn.secondary:hover {{
            background: #7f8c8d;
        }}
        .description {{
            color: #555;
            margin: 10px 0;
        }}
        .icon {{
            font-size: 1.5em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 {project_name} Documentation Hub</h1>
        <p class="description">
            Welcome to the {project_name} project documentation portal. 
            Access the latest documentation, download PDFs, or view test coverage reports.
        </p>

        <div class="section">
            <h2><span class="icon">📖</span> Documentation</h2>
            <p class="description">
                Browse the complete documentation with tutorials, API reference, and guides.
            </p>
            <div class="links">
                <a href="doc/stable/index.html" class="link-btn">
                    📘 Latest Stable Documentation
                </a>
                <a href="doc/latest/index.html" class="link-btn secondary">
                    🔬 Development Version
                </a>
                <a href="doc/pdf_downloads.html" class="link-btn secondary">
                    📄 Download PDFs
                </a>
            </div>
        </div>

        <div class="section">
            <h2><span class="icon">🧪</span> Test Coverage</h2>
            <p class="description">
                View detailed test coverage reports showing which parts of the codebase are tested.
            </p>
            <div class="links">
                <a href="coverage/index.html" class="link-btn">
                    📊 View Coverage Report
                </a>
            </div>
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 0.9em;">
            <p>
                💡 <strong>Tip:</strong> Bookmark the stable documentation link for quick access to the latest version.
            </p>
        </div>
    </div>
</body>
</html>
"""

    landing_page = build_root / 'index.html'
    with open(landing_page, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'🏠 Generated root landing page: {landing_page}')
    print('   Note: This should be copied to public/index.html in GitLab CI')


@click.group()
def cli() -> None:
    """Build and manage versioned documentation."""
    pass


def get_directory_size(path: Path) -> int:
    """
    Calculate total size of a directory in bytes.

    :param path: Directory path
    :type path: Path
    :return: Total size in bytes
    :rtype: int
    """
    total = 0
    for item in path.rglob('*'):
        if item.is_file():
            total += item.stat().st_size
    return total


def format_size(bytes_size: float) -> str:
    """
    Format bytes to human-readable size.

    :param bytes_size: Size in bytes
    :type bytes_size: int
    :return: Formatted size string
    :rtype: str
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f'{bytes_size:.2f} {unit}'
        bytes_size /= 1024.0
    return f'{bytes_size:.2f} TB'


def prune_old_versions(outdir: Path, max_size_mb: int = 100, dry_run: bool = False) -> Tuple[List[str], int]:
    """
    Remove oldest version directories until total size is below threshold.
    Always keeps 'stable', 'latest', and 'dev' (if present).

    :param outdir: Output directory containing version directories
    :type outdir: Path
    :param max_size_mb: Maximum size in megabytes
    :type max_size_mb: int
    :param dry_run: If True, only report what would be deleted
    :type dry_run: bool
    :return: Tuple of (list of removed versions, final size in bytes)
    :rtype: Tuple[List[str], int]
    """
    outdir = Path(outdir).resolve()
    max_size_bytes = max_size_mb * 1024 * 1024

    # Get current total size
    current_size = get_directory_size(outdir)
    print(f'📊 Current total size: {format_size(current_size)}')
    print(f'🎯 Target maximum: {format_size(max_size_bytes)}')

    if current_size <= max_size_bytes:
        print('✅ Size is within limit. No pruning needed.')
        return [], current_size

    # Find all version directories
    protected_versions = {'stable', 'latest', 'dev'}
    version_dirs = []

    for item in outdir.iterdir():
        if item.is_dir() and item.name not in protected_versions:
            # Skip if it's a symlink (it's an alias)
            if item.is_symlink():
                continue
            size = get_directory_size(item)
            version_dirs.append((item.name, size, item))

    # Sort by version (oldest first) using semantic versioning
    version_dirs.sort(key=lambda x: parse_version_tuple(x[0]))

    print(f'\n📦 Found {len(version_dirs)} version directories (excluding protected):')
    for name, size, _ in version_dirs:
        print(f'   • {name}: {format_size(size)}')

    print(f'\n🛡️  Protected versions (will never be removed): {", ".join(protected_versions)}')

    # Remove oldest versions until we're under the limit
    removed = []
    for name, size, path in version_dirs:
        if current_size <= max_size_bytes:
            break

        print(f'\n🗑️  {"[DRY RUN] Would remove" if dry_run else "Removing"} {name} ({format_size(size)})...')

        if not dry_run:
            shutil.rmtree(path)

        removed.append(name)
        current_size -= size
        print(f'   New total size: {format_size(current_size)}')

    if not removed:
        print(f'\n⚠️  Warning: Cannot reduce size below {format_size(max_size_bytes)}')
        print('   All remaining versions are protected or size target is too aggressive.')

    return removed, current_size


def regenerate_versions_json_after_pruning(outdir: Path, removed_versions: List[str]) -> None:
    """
    Regenerate versions.json after pruning, excluding removed versions.

    :param outdir: Output directory containing version directories
    :type outdir: Path
    :param removed_versions: List of version names that were removed
    :type removed_versions: List[str]
    """
    versions_file = outdir / 'versions.json'

    if not versions_file.exists():
        print('⚠️  versions.json not found, skipping regeneration')
        return

    # Read existing versions.json
    with open(versions_file, 'r', encoding='utf-8') as f:
        versions = json.load(f)

    # Filter out removed versions
    original_count = len(versions)
    versions = [v for v in versions if v['version'] not in removed_versions and v.get('path') not in removed_versions]
    removed_count = original_count - len(versions)

    if removed_count == 0:
        print('ℹ️  No versions removed from versions.json')
        return

    print('\n🔄 Regenerating versions.json...')
    print(f'   Removed {removed_count} entries')

    # Write updated versions.json
    write_versions_json(outdir, versions)


def check_multiversion_structure(outdir: Path) -> bool:
    """
    Check if multiversion structure exists (other version directories).

    :param outdir: Output directory to check
    :type outdir: Path
    :return: True if other versions exist
    :rtype: bool
    """
    if not outdir.exists():
        return False

    # Count non-latest version directories
    version_dirs = []
    for item in outdir.iterdir():
        if item.is_dir() and item.name != 'latest':
            # Check if it's not a symlink or if it is, count it
            version_dirs.append(item.name)

    return len(version_dirs) > 0


@cli.command()
@click.option('--outdir', '-o', default='docs/build/doc', help='Output directory to check')
@click.option('--max-size', '-s', default=100, help='Maximum size in MB (default: 100)')
@click.option('--dry-run/--no-dry-run', default=False, help='Show what would be removed without actually removing')
@click.option('--auto-prune/--no-auto-prune', default=False, help='Automatically prune without confirmation')
def prune(outdir: Path, max_size: int, dry_run: bool, auto_prune: bool) -> None:
    """Prune old documentation versions to stay within size limit.

    This command removes the oldest version directories (keeping stable, latest, dev)
    until the total size is below the specified threshold.

    :param outdir: Output directory to prune
    :type outdir: Path
    :param max_size: Maximum size in megabytes
    :type max_size: int
    :param dry_run: Whether to do a dry run
    :type dry_run: bool
    :param auto_prune: Whether to prune automatically without confirmation
    :type auto_prune: bool
    """
    outdir = Path(outdir).resolve()

    if not outdir.exists():
        print(f'❌ Directory does not exist: {outdir}')
        return

    print(f'🔍 Analyzing {outdir}...\n')

    # First do a dry run to see what would be removed
    removed_versions, final_size = prune_old_versions(outdir, max_size, dry_run=True)

    if not removed_versions:
        return

    # If it's already a dry run, we're done
    if dry_run:
        print('\n📋 Summary:')
        print(f'   Versions to remove: {", ".join(removed_versions)}')
        print(f'   Final size: {format_size(final_size)}')
        print('\n💡 Run without --dry-run to actually remove these versions')
        return

    # Ask for confirmation unless auto-prune is enabled
    if not auto_prune:
        print(f'\n⚠️  This will permanently delete {len(removed_versions)} version(s): {", ".join(removed_versions)}')
        response = input('Continue? [y/N]: ')
        if response.lower() not in ('y', 'yes'):
            print('❌ Aborted')
            return

    # Actually prune
    print('\n🔨 Pruning versions...')
    removed_versions, final_size = prune_old_versions(outdir, max_size, dry_run=False)

    # Regenerate versions.json
    regenerate_versions_json_after_pruning(outdir, removed_versions)

    print('\n✅ Pruning complete!')
    print(f'   Removed: {", ".join(removed_versions)}')
    print(f'   Final size: {format_size(final_size)} (target: {max_size} MB)')


@cli.command()
@click.option('--outdir', '-o', default='docs/build/doc', help='Output directory (docs/build/doc)')
@click.option(
    '--include-dev/--no-include-dev',
    is_flag=True,
    help='If true and current branch is ahead of stable, create dev redirect. (True)',
)
@click.option('--min-vers', default='v1.0.0', help='Minimum version to consider (default: v1.0.0).')
@click.option('--keep-temp/--no-keep-temp', default=False, help='Do not remove temp dir (for debugging).')
@click.option(
    '--use-latest-conf/--no-use-latest-conf',
    is_flag=True,
    default=True,
    help='Use the latest conf.py for all builds. (True)',
)
@click.option('--build-pdf/--no-build-pdf', is_flag=True, default=False, help='Also build PDF versions. (False)')
@click.option('--project-name', default='MAFw documentation', help='Project name for PDF index page.')
@click.option(
    '--use-symlinks/--no-use-symlinks',
    is_flag=True,
    default=True,
    help='Use symlinks for stable/dev aliases instead of copying. (True)',
)
@click.option(
    '--max-size', '-s', default=0, help='Maximum artifact size in MB. If exceeded, prune old versions (0 = no limit)'
)
def build(
    outdir: Path,
    include_dev: bool,
    min_vers: str,
    keep_temp: bool,
    use_latest_conf: bool,
    build_pdf: bool,
    project_name: str,
    use_symlinks: bool,
    max_size: int,
) -> None:
    """Build multiversion documentation.

    \f

    :param outdir: Output directory for built documentation
    :type outdir: Path
    :param include_dev: Whether to include dev alias if current branch is ahead
    :type include_dev: bool
    :param min_vers: Minimum version to consider
    :type min_vers: str
    :param keep_temp: Whether to keep temporary files
    :type keep_temp: bool
    :param use_latest_conf: Whether to use latest conf.py for all builds
    :type use_latest_conf: bool
    :param build_pdf: Whether to also build PDF versions
    :type build_pdf: bool
    :param project_name: Project name for PDF index page
    :type project_name: str
    :param use_symlinks: Whether to use symlinks instead of copying
    :type use_symlinks: bool
    :param max_size: Maximum artifact size in MB (0 = no limit)
    :type max_size: int
    """
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    print('🔍 Fetching remote tags...')
    p = run(['git', 'fetch', '--tags', '--quiet'])
    if p.returncode != 0:
        print('⚠️ Warning: git fetch --tags failed. Continuing with local tags.')
        print(f'   Error output: {p.stdout[:200]}...' if p.stdout else '   (no output)')
        print('   This is normal in CI if tags are already present or fetch is restricted.')

    # Collect and filter tags
    print('🔍 Collecting git tags...')
    versions = get_git_tags(min_vers)
    versions = filter_latest_micro(versions)
    if not versions:
        print('No valid tags found. Aborting.')
        sys.exit(1)

    stable_tags = [r[1] for r in versions]
    print('🌿 Candidate stable tags (sorted):', stable_tags)

    # highest version = last element after semver sort
    highest = stable_tags[-1]
    print('🏷️ Highest stable tag:', highest)

    tmproot = Path(tempfile.mkdtemp(prefix='mafw-docs-'))
    print('🔧 Temporary root:', tmproot)

    versions_list = []
    pdf_info_list = []

    # build each tag
    for tag in stable_tags:
        print(f'📘 Building HTML for tag {tag} ...')
        success, log = build_for_tag(tag, outdir, tmproot, use_latest_conf=use_latest_conf, keep_tmp=keep_temp)
        versions_list.append(
            {
                'version': tag,
                'label': 'stable' if tag == highest else 'release',
                'built': success,
            }
        )
        report_build_status(tag, success, log, 'HTML')

        # Build PDF if requested
        pdf_built = False
        if build_pdf:
            print(f'📕 Building PDF for tag {tag} ...')
            html_tag_dir = outdir / tag
            pdf_success, pdf_log, pdf_path = build_pdf_for_tag(
                tag, html_tag_dir, tmproot, use_latest_conf=use_latest_conf, keep_tmp=keep_temp
            )
            pdf_built = pdf_success
            report_build_status(tag, pdf_success, pdf_log, 'PDF')

            # Write PDF log in the same directory
            if html_tag_dir.exists():
                with open(html_tag_dir / f'{tag}_pdf_build.log', 'w', encoding='utf-8') as f:
                    f.write(pdf_log)

        pdf_info_list.append(
            {
                'version': tag,
                'label': 'stable' if tag == highest else 'release',
                'built': pdf_built,
            }
        )

    # create stable redirect (directory stable -> tag)
    mirror_version(outdir, highest, 'stable', use_symlink=use_symlinks)

    # add a 'latest' build from current branch as useful
    print("📘 Building latest (current branch) into 'latest' ...")
    curr_docs = Path('docs') / 'source'
    if curr_docs.exists():
        latest_out = outdir / 'latest'
        latest_out.mkdir(parents=True, exist_ok=True)
        sp = run([SPHINX_BUILD_CMD, '-b', 'html', str(curr_docs), str(latest_out)])
        with open(latest_out / 'sphinx-build.log', 'w', encoding='utf-8') as f:
            f.write(sp.stdout)
        latest_ok = sp.returncode == 0
        versions_list.append({'version': 'latest', 'label': 'latest', 'built': latest_ok})
        report_build_status('latest', latest_ok, sp.stdout, 'HTML')

        # Build PDF for latest if requested
        latest_pdf_built = False
        if build_pdf and curr_docs.exists():
            print('📕 Building PDF for latest ...')
            latex_out = tmproot / 'latest_latex'
            latex_out.mkdir(parents=True, exist_ok=True)

            sp = run([SPHINX_BUILD_CMD, '-b', 'latex', str(curr_docs), str(latex_out)])
            pdf_log = sp.stdout
            if sp.returncode == 0:
                makefile = latex_out / 'Makefile'
                if makefile.exists():
                    sp_pdf = run(['make'], cwd=latex_out)
                else:
                    tex_files = list(latex_out.glob('*.tex'))
                    if tex_files:
                        sp_pdf = run(['pdflatex', '-interaction=nonstopmode', tex_files[0].name], cwd=latex_out)

                pdf_log += '\n' + sp_pdf.stdout
                pdf_files = list(latex_out.glob('*.pdf'))
                if pdf_files:
                    pdf_file = latex_out / 'mafw.pdf'
                    shutil.copy(pdf_file, latest_out / 'latest.pdf')
                    latest_pdf_built = True
                    report_build_status('latest', True, pdf_log, 'PDF')

            # Write PDF log
            with open(latest_out / 'latest_pdf_build.log', 'w', encoding='utf-8') as f:
                f.write(pdf_log)

        pdf_info_list.append({'version': 'latest', 'label': 'latest', 'built': latest_pdf_built})
    else:
        print('❌ No local docs/source for latest. Skipping latest build.')

    # detect dev (is current HEAD a descendant of highest tag?)
    head_rev = git_rev_of('HEAD')
    highest_rev = git_rev_of(highest)
    dev_label = None
    if is_ancestor(highest_rev, head_rev) and head_rev != highest_rev:
        # HEAD is descendant (ahead) of highest -> label dev
        dev_label = 'dev'
        print('🔍 Current branch is ahead of stable -> creating dev alias')
        if include_dev:
            mirror_version(outdir, 'latest', dev_label, use_symlink=use_symlinks)
    else:
        print('🔍 Current branch is not ahead of stable (or identical) -> no dev alias created')

    # add stable and dev labels in JSON with nice mapping
    versions_json = []
    for v in versions_list:
        versions_json.append({'version': v['version'], 'label': v['label'], 'built': v['built'], 'path': v['version']})

    # add convenience entries: stable -> highest, dev -> 'dev' if created
    versions_json.append({'version': 'stable', 'label': 'alias', 'path': highest})
    if dev_label and include_dev:
        versions_json.append({'version': 'dev', 'label': 'alias', 'path': 'latest'})

    write_versions_json(outdir, versions_json)
    write_legacy_redirect_page(outdir)

    # Generate root landing page (goes to parent of outdir)
    build_root = outdir.parent
    write_root_landing_page(build_root, project_name.replace(' documentation', ''))

    # Generate redirect (goes to parent of outdir)
    write_redirects_file(build_root)

    # Generate PDF index page if PDFs were built
    if build_pdf:
        generate_pdf_index_page(outdir, pdf_info_list, project_name)

    # Prune if size limit is specified
    if max_size > 0:
        print(f'\n📏 Checking artifact size (limit: {max_size} MB)...')
        removed_versions, final_size = prune_old_versions(outdir, max_size, dry_run=False)
        if removed_versions:
            regenerate_versions_json_after_pruning(outdir, removed_versions)
            # Regenerate PDF index if PDFs were built
            if build_pdf:
                # Update pdf_info_list to exclude removed versions
                pdf_info_list = [p for p in pdf_info_list if p['version'] not in removed_versions]
                generate_pdf_index_page(outdir, pdf_info_list, project_name)

    if not keep_temp:
        try:
            shutil.rmtree(tmproot)
        except Exception:
            pass

    print('🎉 All done. Built versions placed under:', outdir)


@cli.command()
@click.argument('target', type=click.Choice(['all', 'latest'], case_sensitive=False), default='all')
@click.option('--outdir', '-o', default='docs/build/doc', help='Output directory to clean')
def clean(target: str, outdir: Path) -> None:
    """Clean the output directory.
    TARGET can be 'all' (remove everything) or 'latest' (remove only latest folder).

    \f
    :param target: What to clean - 'all' or 'latest'
    :type target: str
    :param outdir: Output directory to clean
    :type outdir: Path
    """
    outdir = Path(outdir).resolve()

    if not outdir.exists():
        print(f'ℹ️  Output directory does not exist: {outdir}')
        return

    if target == 'latest':
        latest_dir = outdir / 'latest'
        if latest_dir.exists():
            try:
                if latest_dir.is_symlink():
                    latest_dir.unlink()
                else:
                    shutil.rmtree(latest_dir)
                print(f'🧹 Cleaned latest directory: {latest_dir}')
            except Exception as e:
                print(f'❌ Failed to clean directory {latest_dir}: {e}')
        else:
            print(f'ℹ️  Latest directory does not exist: {latest_dir}')
    else:  # all
        try:
            shutil.rmtree(outdir)
            print(f'🧹 Cleaned all output: {outdir}')
        except Exception as e:
            print(f'❌ Failed to clean directory {outdir}: {e}')


@cli.command()
@click.option('--outdir', '-o', default='docs/build/doc', help='Output directory for _redirects file')
@click.option('--old-pdf-path', default='/doc/mafw.pdf', help='Old PDF URL path to redirect from')
@click.option('--new-pdf-path', default='/doc/pdf_downloads.html', help='New PDF downloads page to redirect to')
@click.option('--redirect-root/--no-redirect-root', default=True, help='Redirect /doc/ root to stable')
def redirects(outdir: Path, old_pdf_path: Path, new_pdf_path: Path, redirect_root: bool) -> None:
    """Generate _redirects file for GitLab Pages.

    \f
    :param outdir: Output directory for _redirects file
    :type outdir: Path
    :param old_pdf_path: Old PDF URL path to redirect from
    :type old_pdf_path: Path
    :param new_pdf_path: New PDF downloads page to redirect to
    :type new_pdf_path: Path
    :param redirect_root: Whether to redirect /doc/ root to stable
    :type redirect_root: bool
    """
    outdir = Path(outdir).resolve()

    redirects_content = f"""# Redirects for GitLab Pages
# See: https://docs.gitlab.com/ee/user/project/pages/redirects.html

# Redirect old PDF URL to new PDF downloads page
{old_pdf_path} {new_pdf_path} 301
"""

    if redirect_root:
        redirects_content += """
# Redirect /doc root to stable documentation
# Note: These are specific patterns to avoid redirecting /doc/pdf_downloads.html
/doc/ /doc/stable/ 301
/doc/index.html /doc/stable/index.html 301
"""

    redirects_file = outdir / '_redirects'
    outdir.mkdir(parents=True, exist_ok=True)

    with open(redirects_file, 'w', encoding='utf-8') as f:
        f.write(redirects_content)

    print(f'🔀 Generated _redirects file: {redirects_file}')
    print(f'   Redirects {old_pdf_path} → {new_pdf_path} (301)')
    if redirect_root:
        print('   Redirects /doc/ → /doc/stable/ (301)')
        print('   Redirects /doc/index.html → /doc/stable/index.html (301)')
    print('\n📋 GitLab CI/CD setup:')
    print('   Make sure your .gitlab-ci.yml copies this file to public/ root:')
    print('   ')
    print('   pages:')
    print('     script:')
    print('       - mkdir -p public')
    print(f'       - cp -r {outdir}/* public/doc/')
    print(f'       - cp {redirects_file} public/_redirects')
    print('     artifacts:')
    print('       paths:')
    print('         - public')


@cli.command()
@click.option('--build-root', '-b', default='docs/build', help='Build root directory containing doc/ subdirectory')
@click.option('--project-name', default='MAFw', help='Project name for the landing page')
def landing(build_root: Path, project_name: str) -> None:
    """Generate root landing page for project.

    \f
    :param build_root: Build root directory
    :type build_root: Path
    :param project_name: Project name
    :type project_name: str
    """
    build_root = Path(build_root).resolve()
    write_root_landing_page(build_root, project_name)
    print('\n📋 GitLab CI/CD: Copy this to public/index.html:')
    print(f'   cp {build_root}/index.html public/index.html')


def ensure_versions_json_exists(outdir: Path) -> bool:
    """
    Ensure versions.json exists in outdir. If not, try to copy from another version.

    :param outdir: Output directory that should contain versions.json
    :type outdir: Path
    :return: True if versions.json exists or was successfully copied
    :rtype: bool
    """
    versions_file = outdir / 'versions.json'

    if versions_file.exists():
        return True

    print('⚠️  versions.json not found in output directory')

    # Look for versions.json in other version directories
    for item in outdir.iterdir():
        if item.is_dir() and not item.is_symlink():
            candidate = item / 'versions.json'
            if candidate.exists():
                print(f'📋 Copying versions.json from {item.name}/')
                shutil.copy(candidate, versions_file)
                shutil.copy(candidate, outdir / 'generated/versions.json')
                return True

    print('❌ Could not find versions.json in any version directory')
    return False


@cli.command(name='current')
@click.option('--outdir', '-o', default='docs/build/doc', help='Output directory (docs/build/doc)')
@click.option('--build-pdf/--no-build-pdf', is_flag=True, default=False, help='Also build PDF versions. (False)')
def build_current_only(outdir: Path, build_pdf: bool = False, project_name: str = 'Documentation') -> None:
    """
    Build documentation only for the current working tree (no git worktrees).
    Places output in the 'latest' folder.

    :param outdir: Output directory for built documentation
    :type outdir: Path
    :param build_pdf: Whether to also build PDF version
    :type build_pdf: bool
    :param project_name: Project name for PDF
    :type project_name: str
    """
    outdir = Path(outdir).resolve()

    print('📘 Building documentation for current working tree...')

    # Check if multiversion structure exists
    has_other_versions = check_multiversion_structure(outdir)

    if not has_other_versions:
        print('\n⚠️  Warning: No other version directories found!')
        print('   The version switcher and navigation may not work correctly.')
        print('   Consider running the full build at least once:')
        print('   $ multiversion-doc build')
        response = input('\nContinue anyway? [y/N]: ')
        if response.lower() not in ('y', 'yes'):
            print('❌ Aborted')
            sys.exit(0)

    curr_docs = Path('docs') / 'source'
    if not curr_docs.exists():
        print(f'❌ Documentation source not found: {curr_docs}')
        sys.exit(1)

    # Build HTML
    latest_out = outdir / 'latest'
    latest_out.mkdir(parents=True, exist_ok=True)

    print('\n🔨 Building HTML...')
    sp = run([SPHINX_BUILD_CMD, '-b', 'html', str(curr_docs), str(latest_out)])

    # Write log
    log_file = latest_out / 'sphinx-build.log'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(sp.stdout)

    html_success = sp.returncode == 0
    report_build_status('latest', html_success, sp.stdout, 'HTML')

    if not html_success:
        print(f'❌ HTML build failed. Check log: {log_file}')
        sys.exit(1)

    # Ensure versions.json exists
    print('\n🔍 Checking for versions.json...')
    if not ensure_versions_json_exists(outdir):
        print('⚠️  Version switcher may not work without versions.json')
        print('   Run the full build to generate it:')
        print('   $ python doc_versioning.py build')
    else:
        # Copy versions.json to latest folder
        shutil.copy(outdir / 'versions.json', latest_out / 'versions.json')
        shutil.copy(outdir / 'versions.json', latest_out / 'generated/versions.json')
        print('✅ versions.json is available')

    # Build PDF if requested
    if build_pdf:
        print('\n🔨 Building PDF...')
        tmproot = Path(tempfile.mkdtemp(prefix='mafw-docs-current-'))

        try:
            latex_out = tmproot / 'latex'
            latex_out.mkdir(parents=True, exist_ok=True)

            sp = run([SPHINX_BUILD_CMD, '-b', 'latex', str(curr_docs), str(latex_out)])
            pdf_log = sp.stdout

            if sp.returncode == 0:
                makefile = latex_out / 'Makefile'
                if makefile.exists():
                    sp_pdf = run(['make'], cwd=latex_out)
                else:
                    tex_files = list(latex_out.glob('*.tex'))
                    if tex_files:
                        sp_pdf = run(['pdflatex', '-interaction=nonstopmode', tex_files[0].name], cwd=latex_out)
                    else:
                        print('❌ No .tex file found')
                        sp_pdf = None

                if sp_pdf:
                    pdf_log += '\n' + sp_pdf.stdout
                    pdf_files = list(latex_out.glob('*.pdf'))

                    if pdf_files:
                        pdf_path = latest_out / 'latest.pdf'
                        shutil.copy(pdf_files[0], pdf_path)
                        pdf_success = sp_pdf.returncode == 0
                        report_build_status('latest', pdf_success, pdf_log, 'PDF')

                        if pdf_success:
                            print(f'📄 PDF saved to: {pdf_path}')
                    else:
                        print('❌ PDF generation failed: no PDF file produced')
            else:
                print('❌ LaTeX build failed')

            # Write PDF log
            with open(latest_out / 'latest_pdf_build.log', 'w', encoding='utf-8') as f:
                f.write(pdf_log)

        finally:
            shutil.rmtree(tmproot)

    print('\n✅ Documentation built successfully!')
    print(f'📂 Output: {latest_out}')


if __name__ == '__main__':
    cli.main()
