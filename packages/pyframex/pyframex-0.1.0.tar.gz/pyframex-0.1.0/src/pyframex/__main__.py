"""
PyFrameX CLI - Command Line Interface
=====================================

Usage:
    pyframex <command> [options]

Commands:
    info <file>         Show DataFrame info
    head <file> [n]     Show first n rows
    query <file> <sql>  Execute SQL query
    clean <file> <output>  Auto-clean data
"""

import sys
import argparse
from pathlib import Path

from .frame import Frame


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="PyFrameX - Next-Generation DataFrame CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # info command
    info_parser = subparsers.add_parser('info', help='Show DataFrame information')
    info_parser.add_argument('file', help='Input file path')
    
    # head command
    head_parser = subparsers.add_parser('head', help='Show first n rows')
    head_parser.add_argument('file', help='Input file path')
    head_parser.add_argument('-n', '--rows', type=int, default=5, help='Number of rows')
    
    # query command
    query_parser = subparsers.add_parser('query', help='Execute SQL query')
    query_parser.add_argument('file', help='Input file path')
    query_parser.add_argument('sql', help='SQL query string')
    
    # clean command
    clean_parser = subparsers.add_parser('clean', help='Auto-clean data')
    clean_parser.add_argument('file', help='Input file path')
    clean_parser.add_argument('output', help='Output file path')
    
    # version command
    version_parser = subparsers.add_parser('version', help='Show version')
    
    args = parser.parse_args()
    
    if args.command == 'info':
        cmd_info(args.file)
    elif args.command == 'head':
        cmd_head(args.file, args.rows)
    elif args.command == 'query':
        cmd_query(args.file, args.sql)
    elif args.command == 'clean':
        cmd_clean(args.file, args.output)
    elif args.command == 'version':
        cmd_version()
    else:
        parser.print_help()


def cmd_info(filepath: str):
    """Show DataFrame information"""
    try:
        df = Frame(filepath)
        print(df.summary())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_head(filepath: str, n: int):
    """Show first n rows"""
    try:
        df = Frame(filepath)
        print(df.head(n))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_query(filepath: str, sql: str):
    """Execute SQL query"""
    try:
        df = Frame(filepath)
        result = df.sql(sql)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_clean(filepath: str, output: str):
    """Auto-clean data"""
    try:
        df = Frame(filepath)
        cleaned = df.auto_clean()
        
        # Save to output
        if output.endswith('.csv'):
            cleaned.to_csv(output)
        elif output.endswith('.json'):
            cleaned.to_json(output)
        else:
            raise ValueError(f"Unsupported output format: {output}")
        
        print(f"✓ Cleaned data saved to {output}")
        print(f"  Original rows: {len(df)}")
        print(f"  Cleaned rows:  {len(cleaned)}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_version():
    """Show version"""
    from . import __version__
    print(f"PyFrameX v{__version__}")


if __name__ == "__main__":
    main()
