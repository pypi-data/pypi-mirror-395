"""
CAILculator MCP Server
High-dimensional data analysis for MCP clients
"""

__version__ = "1.3.0"
__author__ = "Paul Chavez"
__email__ = "paul@chavezailabs.com"

# Lazy imports to speed up module loading
# These will only be imported when accessed
def __getattr__(name):
    if name == 'MCPServer' or name == 'main':
        from .server import MCPServer, main
        globals()['MCPServer'] = MCPServer
        globals()['main'] = main
        return globals()[name]
    elif name == 'TOOLS_DEFINITIONS' or name == 'call_tool':
        from .tools import TOOLS_DEFINITIONS, call_tool
        globals()['TOOLS_DEFINITIONS'] = TOOLS_DEFINITIONS
        globals()['call_tool'] = call_tool
        return globals()[name]
    elif name == 'PatternDetector' or name == 'Pattern':
        from .patterns import PatternDetector, Pattern
        globals()['PatternDetector'] = PatternDetector
        globals()['Pattern'] = Pattern
        return globals()[name]
    elif name == 'create_hypercomplex' or name == 'Pathion' or name == 'Sedenion':
        from .hypercomplex import create_hypercomplex, Pathion, Sedenion
        globals()['create_hypercomplex'] = create_hypercomplex
        globals()['Pathion'] = Pathion
        globals()['Sedenion'] = Sedenion
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    'MCPServer',
    'main',
    'TOOLS_DEFINITIONS',
    'call_tool',
    'PatternDetector',
    'Pattern',
    'create_hypercomplex',
    'Pathion',
    'Sedenion',
]
