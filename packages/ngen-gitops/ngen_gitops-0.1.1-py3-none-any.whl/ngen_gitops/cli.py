#!/usr/bin/env python3
"""CLI entry point for ngen-gitops."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from . import __version__
from .bitbucket import (
    create_branch,
    set_image_in_yaml,
    create_pull_request,
    merge_pull_request,
    GitOpsError
)
from .config import (
    load_config,
    get_config_file_path,
    config_exists,
    get_bitbucket_credentials
)


def cmd_create_branch(args):
    """Handle create-branch command."""
    try:
        result = create_branch(
            repo=args.repo,
            src_branch=args.src_branch,
            dest_branch=args.dest_branch
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✅ {result['message']}")
            if result.get('branch_url'):
                print(f"   Branch URL: {result['branch_url']}")
        
        sys.exit(0 if result['success'] else 1)
        
    except GitOpsError as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_set_image_yaml(args):
    """Handle set-image-yaml command."""
    try:
        result = set_image_in_yaml(
            repo=args.repo,
            refs=args.refs,
            yaml_path=args.yaml_path,
            image=args.image,
            dry_run=args.dry_run
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✅ {result['message']}")
            if result.get('commit'):
                print(f"   {result['commit']}")
        
        sys.exit(0 if result['success'] else 1)
        
    except GitOpsError as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_pull_request(args):
    """Handle pull-request command."""
    try:
        result = create_pull_request(
            repo=args.repo,
            src_branch=args.src_branch,
            dest_branch=args.dest_branch,
            delete_after_merge=args.delete_after_merge
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✅ {result['message']}")
            if result.get('pr_url'):
                print(f"   Pull Request URL: {result['pr_url']}")
        
        sys.exit(0 if result['success'] else 1)
        
    except GitOpsError as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_merge(args):
    """Handle merge command."""
    try:
        result = merge_pull_request(
            pr_url=args.pr_url,
            delete_after_merge=args.delete_after_merge
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✅ {result['message']}")
            if result.get('merge_commit'):
                print(f"   Merge commit: {result['merge_commit']}")
        
        sys.exit(0 if result['success'] else 1)
        
    except GitOpsError as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_server(args):
    """Handle server command."""
    try:
        from .server import start_server
        
        host = args.host
        port = args.port
        
        print(f"🚀 Starting ngen-gitops server...")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Endpoints:")
        print(f"     - POST /v1/gitops/create-branch")
        print(f"     - POST /v1/gitops/set-image-yaml")
        print(f"     - POST /v1/gitops/pull-request")
        print(f"     - POST /v1/gitops/merge")
        print()
        
        start_server(host=host, port=port)
        
    except Exception as e:
        print(f"❌ Server error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_config(args):
    """Handle config command."""
    try:
        config = load_config()
        
        if args.json:
            # Mask sensitive data in JSON output
            safe_config = config.copy()
            if 'bitbucket' in safe_config and 'app_password' in safe_config['bitbucket']:
                safe_config['bitbucket']['app_password'] = '***MASKED***'
            print(json.dumps(safe_config, indent=2))
        else:
            print(f"📋 ngen-gitops Configuration")
            print(f"   Config file: {get_config_file_path()}")
            print()
            print(f"Bitbucket:")
            print(f"   Username: {config.get('bitbucket', {}).get('username', '(not set)')}")
            print(f"   App Password: {'***SET***' if config.get('bitbucket', {}).get('app_password') else '(not set)'}")
            print(f"   Organization: {config.get('bitbucket', {}).get('organization', 'loyaltoid')}")
            print()
            print(f"Server:")
            print(f"   Host: {config.get('server', {}).get('host', '0.0.0.0')}")
            print(f"   Port: {config.get('server', {}).get('port', 8080)}")
            
            # Check if credentials are valid
            try:
                creds = get_bitbucket_credentials()
                print()
                print("✅ Credentials configured")
            except ValueError as e:
                print()
                print(f"⚠️  {e}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='ngen-gitops',
        description='GitOps CLI and web server for Bitbucket operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new branch
  ngen-gitops create-branch myrepo main feature/new-feature
  
  # Update image in YAML file
  ngen-gitops set-image-yaml myrepo develop k8s/deployment.yaml myapp:v1.0.0
  
  # Create pull request
  ngen-gitops pull-request myrepo feature/new-feature develop --delete-after-merge
  
  # Merge pull request
  ngen-gitops merge https://bitbucket.org/org/repo/pull-requests/123
  
  # Start web server
  ngen-gitops server --port 8080
  
  # Show configuration
  ngen-gitops config

For more information, visit: https://github.com/mamatnurahmat/ngen-gitops
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # create-branch command
    parser_create_branch = subparsers.add_parser(
        'create-branch',
        help='Create a new branch from source branch'
    )
    parser_create_branch.add_argument('repo', help='Repository name')
    parser_create_branch.add_argument('src_branch', help='Source branch name')
    parser_create_branch.add_argument('dest_branch', help='Destination branch name')
    parser_create_branch.add_argument('--json', action='store_true', help='Output as JSON')
    parser_create_branch.set_defaults(func=cmd_create_branch)
    
    # set-image-yaml command
    parser_set_image = subparsers.add_parser(
        'set-image-yaml',
        help='Update image reference in YAML file'
    )
    parser_set_image.add_argument('repo', help='Repository name')
    parser_set_image.add_argument('refs', help='Branch/tag reference')
    parser_set_image.add_argument('yaml_path', help='Path to YAML file in repository')
    parser_set_image.add_argument('image', help='New image to set (e.g., myapp:v1.0.0)')
    parser_set_image.add_argument('--dry-run', action='store_true', help='Prepare changes without pushing')
    parser_set_image.add_argument('--json', action='store_true', help='Output as JSON')
    parser_set_image.set_defaults(func=cmd_set_image_yaml)
    
    # pull-request command
    parser_pr = subparsers.add_parser(
        'pull-request',
        help='Create a pull request'
    )
    parser_pr.add_argument('repo', help='Repository name')
    parser_pr.add_argument('src_branch', help='Source branch name')
    parser_pr.add_argument('dest_branch', help='Destination branch name')
    parser_pr.add_argument('--delete-after-merge', action='store_true', 
                          help='Delete source branch after merge')
    parser_pr.add_argument('--json', action='store_true', help='Output as JSON')
    parser_pr.set_defaults(func=cmd_pull_request)
    
    # merge command
    parser_merge = subparsers.add_parser(
        'merge',
        help='Merge a pull request'
    )
    parser_merge.add_argument('pr_url', help='Pull request URL')
    parser_merge.add_argument('--delete-after-merge', action='store_true',
                             help='Delete source branch after merge')
    parser_merge.add_argument('--json', action='store_true', help='Output as JSON')
    parser_merge.set_defaults(func=cmd_merge)
    
    # server command
    parser_server = subparsers.add_parser(
        'server',
        help='Start web server'
    )
    parser_server.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    parser_server.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    parser_server.set_defaults(func=cmd_server)
    
    # config command
    parser_config = subparsers.add_parser(
        'config',
        help='Show configuration'
    )
    parser_config.add_argument('--json', action='store_true', help='Output as JSON')
    parser_config.set_defaults(func=cmd_config)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == '__main__':
    main()
