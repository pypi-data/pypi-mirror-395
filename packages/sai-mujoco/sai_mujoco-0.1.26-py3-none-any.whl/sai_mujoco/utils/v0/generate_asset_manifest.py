"""
Generic script to generate manifest.json for environment assets.
This should be run before deploying assets to Cloud (GCP).

Usage:
    # For kitchen environment
    python -m sai_mujoco.utils.v0.generate_asset_manifest \\
        --env kitchen \\
        --env-version v0 \\
        --version 1.0.0 \\
        --directories fixtures objects textures

    # For custom environment
    python -m sai_mujoco.utils.v0.generate_asset_manifest \\
        --env myenv \\
        --env-version v0 \\
        --version 1.0.0 \\
        --directories models textures configs

    # With custom assets path
    python -m sai_mujoco.utils.v0.generate_asset_manifest \\
        --env myenv \\
        --env-version v0 \\
        --version 1.0.0 \\
        --assets-path /path/to/assets \\
        --directories fixtures objects textures
"""

import sys
import os
from pathlib import Path
from sai_mujoco.utils.v0.download_assets import generate_manifest


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate manifest.json for environment assets"
    )
    parser.add_argument(
        "--env",
        required=True,
        help="Environment name (e.g., kitchen, football, pick_place)",
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Asset version number (e.g., 1.0.0, 1.2.3)",
    )
    parser.add_argument(
        "--env-version",
        required=True,
        help="Environment version (e.g., v0)",
    )
    parser.add_argument(
        "--directories",
        nargs="+",
        required=True,
        help="Space-separated list of directories to include (e.g., fixtures objects textures)",
    )
    parser.add_argument(
        "--assets-path",
        help="Path to assets directory (default: auto-detect from env name)",
        default=None,
    )
    parser.add_argument(
        "--output",
        help="Output path for manifest.json (default: assets-path/manifest.json)",
        default=None,
    )

    args = parser.parse_args()

    args.env = args.env.lower()

    if args.assets_path:
        assets_path = Path(args.assets_path)
    else:
        import sai_mujoco

        assets_path = (
            Path(os.path.dirname(sai_mujoco.__file__))
            / "assets"
            / "envs"
            / args.env
            / args.env_version
        )

    if not assets_path.exists():
        print(f"Error: Assets path does not exist: {assets_path}")
        print("\nCreate the directory or use --assets-path to specify custom location")
        sys.exit(1)

    output_path = args.output if args.output else str(assets_path / "manifest.json")

    print("\n" + "=" * 80)
    print(f"🔧 Generating Manifest for {args.env.upper()} Assets")
    print("=" * 80)
    print(f"📁 Assets Path:    {assets_path}")
    print(f"🏷️  Version:        {args.version}")
    print(f"📂 Directories:    {', '.join(args.directories)}")
    print(f"💾 Output:         {output_path}")
    print("=" * 80 + "\n")

    manifest = generate_manifest(
        base_path=str(assets_path),
        version=args.version,
        directories=args.directories,
        output_path=output_path,
    )

    print("\n" + "┌" + "─" * 78 + "┐")
    print("│" + " " * 25 + "✅ MANIFEST GENERATED" + " " * 32 + "│")
    print("└" + "─" * 78 + "┘\n")

    print("📊 Manifest Details:")
    print(f"   • Version:     {manifest['version']}")
    print(f"   • Updated at:  {manifest['updated_at']}\n")

    print("📦 Asset Statistics:")
    for dir_name, info in manifest["files"].items():
        print(f"   ├─ {dir_name}:")
        print(f"   │  ├─ Files:    {info['count']}")
        print(f"   │  └─ Checksum: {info['checksum'][:16]}...")

    print("\n" + "┌" + "─" * 78 + "┐")
    print("│" + " " * 30 + "🚀 NEXT STEPS" + " " * 35 + "│")
    print("└" + "─" * 78 + "┘\n")

    print("1️⃣  Review the manifest:")
    print(f"    {output_path}\n")

    print("2️⃣  Create assets zip:")
    print(f"    cd {assets_path}")
    print(f"    zip -r {args.env}_assets.zip {' '.join(args.directories)}\n")

    print("3️⃣  Upload to GCP:")
    print(f"    gsutil cp {output_path} \\")
    print(f"      gs://sai-assets/envs/{args.env}/{args.env_version}/manifest.json")
    print(f"    gsutil cp {args.env}_assets.zip \\")
    print(
        f"      gs://sai-assets/envs/{args.env}/{args.env_version}/{args.env}_assets.zip\n"
    )

    print("=" * 50)
    print("✨ Done!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
