#!/usr/bin/env python3
"""
Package a skill into a .skill file for distribution
"""

import os
import sys
import json
import re
import zipfile
from pathlib import Path

def validate_skill(skill_dir: Path) -> tuple[bool, list]:
    """Validate skill structure and content"""
    errors = []
    
    # Check SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
        return False, errors
    
    # Parse frontmatter
    content = skill_md.read_text(encoding='utf-8')
    
    # Check for YAML frontmatter
    if not content.startswith('---'):
        errors.append("SKILL.md must start with YAML frontmatter")
    else:
        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            errors.append("Invalid frontmatter format")
        else:
            frontmatter = parts[1].strip()
            
            # Check required fields
            if 'name:' not in frontmatter:
                errors.append("Missing 'name' in frontmatter")
            if 'description:' not in frontmatter:
                errors.append("Missing 'description' in frontmatter")
            
            # Validate name format
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                name = name_match.group(1).strip()
                if not re.match(r'^[a-z0-9-]+$', name):
                    errors.append(f"Invalid skill name '{name}' - use lowercase letters, digits, and hyphens only")
    
    # Check directory name matches skill name
    if name_match:
        expected_dir = name_match.group(1).strip()
        if skill_dir.name != expected_dir:
            errors.append(f"Directory name '{skill_dir.name}' doesn't match skill name '{expected_dir}'")
    
    return len(errors) == 0, errors

def package_skill(skill_dir: str, output_dir: str = None) -> str:
    """Package a skill directory into a .skill file"""
    skill_path = Path(skill_dir)
    
    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)
    
    # Validate
    print(f"[SCAN] Validating skill: {skill_path.name}")
    is_valid, errors = validate_skill(skill_path)
    
    if not is_valid:
        print("[FAIL] Validation failed:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)
    
    print("[PASS] Validation passed")
    
    # Determine output path
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding='utf-8')
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    skill_name = name_match.group(1).strip() if name_match else skill_path.name
    
    if output_dir:
        output_path = Path(output_dir) / f"{skill_name}.skill"
    else:
        output_path = skill_path.parent / f"{skill_name}.skill"
    
    # Create zip file
    print(f"[PACK] Packaging to: {output_path}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Skip unwanted files - check relative parts only
                try:
                    rel_parts = file_path.relative_to(skill_path).parts
                except ValueError:
                    continue
                    
                # Skip hidden files/dirs and cache
                skip = False
                for part in rel_parts:
                    if part.startswith('.') or part == '__pycache__':
                        skip = True
                        break
                if skip:
                    continue
                    
                # Skip compiled Python
                if file_path.suffix in ['.pyc', '.pyo']:
                    continue
                
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"   + {arcname}")
    
    # Get file size
    size = output_path.stat().st_size
    print(f"[DONE] Package created: {size / 1024:.1f} KB")
    
    return str(output_path)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Package an OpenClaw skill')
    parser.add_argument('skill_dir', help='Path to skill directory')
    parser.add_argument('-o', '--output', help='Output directory (default: same as skill)')
    parser.add_argument('--install', action='store_true', help='Install after packaging')
    
    args = parser.parse_args()
    
    package_path = package_skill(args.skill_dir, args.output)
    
    print(f"\n[DONE] Skill packaged successfully!")
    print(f"   Path: {package_path}")
    
    if args.install:
        print("\n[INFO] To install this skill:")
        print(f"   openclaw skill install {package_path}")

if __name__ == '__main__':
    main()
