"""Package parsers for different package managers."""

from .base import PackageParser
from .factory import PackageParserFactory, get_parser_factory, register_parser, get_parser

# Import and register all parsers
from .javascript import (
    PackageJsonParser,
    PackageLockParser, 
    YarnLockParser,
    PnpmLockParser,
    BunLockParser
)
from .python import (
    RequirementsTxtParser,
    PipfileLockParser,
    PoetryLockParser,
    PyprojectTomlParser
)
from .ruby import GemfileLockParser
from .php import ComposerLockParser
from .go import GoModParser, GoSumParser
from .rust import CargoLockParser
from .maven import MavenParser

# Register JavaScript parsers
register_parser(r'package\.json$', PackageJsonParser)
register_parser(r'package-lock\.json$', PackageLockParser)
register_parser(r'yarn\.lock$', YarnLockParser)
register_parser(r'pnpm-lock\.yaml$', PnpmLockParser)
register_parser(r'bun\.lockb$', BunLockParser)

# Register Python parsers
register_parser(r'requirements\.txt$', RequirementsTxtParser)
register_parser(r'requirements\.in$', RequirementsTxtParser)
register_parser(r'Pipfile\.lock$', PipfileLockParser)
register_parser(r'poetry\.lock$', PoetryLockParser)
register_parser(r'pyproject\.toml$', PyprojectTomlParser)

# Register Ruby parsers
register_parser(r'Gemfile\.lock$', GemfileLockParser)

# Register PHP parsers
register_parser(r'composer\.lock$', ComposerLockParser)

# Register Go parsers
register_parser(r'go\.mod$', GoModParser)
register_parser(r'go\.sum$', GoSumParser)

# Register Rust parsers
register_parser(r'Cargo\.lock$', CargoLockParser)

# Register Maven parsers
register_parser(r'pom\.xml$', MavenParser)

__all__ = [
    'PackageParser',
    'PackageParserFactory', 
    'get_parser_factory',
    'register_parser',
    'get_parser',
    # JavaScript parsers
    'PackageJsonParser',
    'PackageLockParser',
    'YarnLockParser', 
    'PnpmLockParser',
    'BunLockParser',
    # Python parsers
    'RequirementsTxtParser',
    'PipfileLockParser',
    'PoetryLockParser',
    'PyprojectTomlParser',
    # Ruby parsers
    'GemfileLockParser',
    # PHP parsers
    'ComposerLockParser',
    # Go parsers
    'GoModParser',
    'GoSumParser',
    # Rust parsers
    'CargoLockParser',
    # Maven parsers
    'MavenParser',
]
