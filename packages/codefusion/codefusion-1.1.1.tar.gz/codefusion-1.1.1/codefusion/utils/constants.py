# codefusion/utils/constants.py
import typing as t

HEADER_SEPARATOR = "=" * 80
FILE_SEPARATOR = "-" * 80

BINARY_EXTENSIONS: t.Set[str] = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', '.tiff',
    '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar', '.xz',
    '.exe', '.dll', '.so', '.dylib', '.jar', '.class', '.pyc', '.pyo',
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac', '.mkv', '.webm',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.db', '.sqlite', '.sqlite3',
    '.bin', '.dat', '.o', '.obj', '.pdb', '.lib', '.a',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.pkl', '.pickle', '.npy', '.npz', '.h5', '.hdf5', '.pth', '.onnx',
}

EXTENSIONLESS_TEXT_FILES: t.Set[str] = {
    'dockerfile', 'makefile', 'rakefile', 'procfile', 
    'gemfile', 'guardfile', 'podfile', 'berksfile',
    'vagrantfile', 'jenkinsfile', 'fastfile', 'appfile',
    'changelog', 'authors', 'contributors', 'copying', 
    'install', 'news', 'thanks', 'history', 'notice', 'manifest'
}

LICENSE_PATTERNS: t.List[str] = [
    "LICENSE", "LICENSE.*", "LICENCE", "LICENCE.*",
    "license", "license.*", "licence", "licence.*",
    "*/LICENSE", "*/LICENSE.*", "*/LICENCE", "*/LICENCE.*",
    "COPYING", "COPYRIGHT", "*/COPYING", "*/COPYRIGHT",
    "NOTICE", "*/NOTICE"
]

README_PATTERNS: t.List[str] = [
    "README", "README.*", "readme", "readme.*",
    "*/README", "*/README.*"
]

WRAPPER_PATTERNS: t.List[str] = [
    "mvnw", "mvnw.cmd", "*/mvnw", "*/mvnw.cmd",
    "gradlew", "gradlew.bat", "*/gradlew", "*/gradlew.bat",
    "*/.mvn/wrapper/*", "*/gradle/wrapper/*",
    "*/.mvn/*", ".mvn"
]

LOCKFILE_PATTERNS: t.List[str] = [
    "package-lock.json", "*/package-lock.json",
    "yarn.lock", "*/yarn.lock", 
    "pnpm-lock.yaml", "*/pnpm-lock.yaml",
    "composer.lock", "*/composer.lock",
    "Gemfile.lock", "*/Gemfile.lock",
    "Pipfile.lock", "*/Pipfile.lock",
    "poetry.lock", "*/poetry.lock",
    "cargo.lock", "*/cargo.lock",
    "*.terraform.lock.hcl", "*/.terraform.lock.hcl",
    "*.lock"
]

PACKAGE_PATTERNS: t.List[str] = [
    "package.json", "*/package.json",
    "composer.json", "*/composer.json",
    "Gemfile", "*/Gemfile",
    "Pipfile", "*/Pipfile",
    "requirements*.txt", "*/requirements*.txt",
    "setup.py", "*/setup.py",
    "setup.cfg", "*/setup.cfg",
    "cargo.toml", "*/cargo.toml",
    "go.mod", "*/go.mod",
    "go.sum", "*/go.sum",
    "pom.xml", "*/pom.xml",
    "build.gradle", "*/build.gradle",
    "gradle.properties", "*/gradle.properties"
]

# CodeFusion output and cache patterns
CODEFUSION_OUTPUT_PATTERNS: t.List[str] = [
    "code_compilation.*", "*/code_compilation.*",
    "code-compilation.*", "*/code-compilation.*",
    "project_compilation.*", "*/project_compilation.*",
    "project-compilation.*", "*/project-compilation.*",
    "*_compilation.txt", "*_compilation.md", "*_compilation.html", "*_compilation.json",
    "compiled_code.*", "*/compiled_code.*",
    "codebase.*", "*/codebase.*",
    "full_code.*", "*/full_code.*",
    "merged_code.*", "*/merged_code.*",
    "unified_code.*", "*/unified_code.*",
    "combined_code.*", "*/combined_code.*",
    "*.codefusion", "*/*.codefusion"
]

DEFAULT_EXCLUDE_PATTERNS: t.List[str] = [
    # Version control
    "*/.git/*", ".git", "*/.svn/*", ".svn", "*/.hg/*", ".hg",
    
    # Python
    "*/__pycache__/*", "__pycache__", "*/.pytest_cache/*", ".pytest_cache",
    ".coverage", "*/.coverage.*", "*/.mypy_cache/*", ".mypy_cache",
    "*/.tox/*", ".tox", "*/venv/*", "venv", "*/.venv/*", ".venv",
    "*/env/*", "env", "*/.env/*", ".env", "*/virtualenv/*", "virtualenv",
    "*/dist/*", "dist", "*/build/*", "build", "*.egg-info", "*/.eggs/*",
    "*.pyc", "*.pyo", "*.pyd",
    
    # Node.js
    "*/node_modules/*", "node_modules", "**/node_modules/**",
    "*/bower_components/*", "bower_components",
    "*/coverage/*", "*/.nyc_output/*", ".nyc_output",
    "*.log", "*/logs/*", "*/log/*",
    
    # Java/Maven/Gradle  
    "*/target/*", "target", "*/.gradle/*", ".gradle",
    "*/out/*", "out", "*.class", "*.jar", "*.war", "*.ear",
    
    # Build outputs
    "*/bin/*", "bin", "*/obj/*", "obj",
    "*/Debug/*", "Debug", "*/Release/*", "Release",
    "*/CMakeFiles/*", "CMakeFiles", "CMakeCache.txt",
    "*.o", "*.obj", "*.so", "*.dll", "*.dylib",
    
    # IDE files
    "*/.idea/*", ".idea", "*/.vscode/*", ".vscode",
    "*/.vs/*", ".vs", "*.iml", "*.swp", "*.swo", "*~",
    
    # Documentation builds
    "*/docs/_build/*", "docs/_build", "*/site/*", "site",
    "*/public/*", "public", "*/_site/*", "_site",
    
    # OS files
    ".DS_Store", "*/.DS_Store", "Thumbs.db", "*/Thumbs.db",
    
    # Binary files
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.ico", "*.svg",
    "*.pdf", "*.zip", "*.tar", "*.gz", "*.rar",
    "*.exe", "*.dll", "*.so", "*.dylib",
    "*.mp3", "*.mp4", "*.avi", "*.mov",
    
    # Cache and temp
    "*/.cache/*", ".cache", "*/tmp/*", "tmp", "*/temp/*", "temp",
    
    # CI/CD
    "*/.github/workflows/.git/*", "*/.circleci/*", ".circleci",
    
    # Terraform
    "*/.terraform/*", ".terraform", "*.tfstate", "*.tfstate.*",

    # Config & Secrets
    ".gitignore", "*/.gitignore",
    "*.env", "*/.env", "*.env.*", "*/.env.*",
    "*.pem", "*/.pem", "*.key", "*/.key",
    "secrets.*", "*/secrets.*",
    "*.secret", "*/.secret",
]

def get_exclude_patterns(exclude_licenses: bool = True, 
                         exclude_readmes: bool = False,
                         exclude_wrappers: bool = True,
                         exclude_lockfiles: bool = True,
                         exclude_packages: bool = True) -> t.List[str]:
    patterns = DEFAULT_EXCLUDE_PATTERNS.copy()
    
    # Always exclude codefusion output files
    patterns.extend(CODEFUSION_OUTPUT_PATTERNS)
    
    if exclude_licenses:
        patterns.extend(LICENSE_PATTERNS)
    
    if exclude_readmes:
        patterns.extend(README_PATTERNS)
    
    if exclude_wrappers:
        patterns.extend(WRAPPER_PATTERNS)
        
    if exclude_lockfiles:
        patterns.extend(LOCKFILE_PATTERNS)
    
    if exclude_packages:
        patterns.extend(PACKAGE_PATTERNS)
    
    return patterns
