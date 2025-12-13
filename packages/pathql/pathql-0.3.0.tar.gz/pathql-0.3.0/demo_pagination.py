#!/usr/bin/env python3
"""
Example demonstrating the new paginate() functionality.
"""

import tempfile
from pathlib import Path

from src.tpath import PQuery


def demo_pagination():
    """Demonstrate pagination with a realistic example."""

    print("🔍 PQuery Pagination Demo")
    print("=" * 40)

    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📁 Creating test files in: {temp_path}")

        # Create 47 files of various sizes
        for i in range(47):
            size = (i % 5 + 1) * 100  # Vary file sizes
            content = "x" * size
            (temp_path / f"document_{i:03d}.txt").write_text(content)

        # Also create some other file types
        for i in range(8):
            (temp_path / f"image_{i:02d}.jpg").write_text(f"fake image {i}")

        print(f"✅ Created {47 + 8} test files")

        # Query for text files only
        query = PQuery().from_(temp_dir).where(lambda p: p.suffix == ".txt").distinct()

        print("\n📄 Processing text files in pages of 10:")
        print("-" * 40)

        # Demonstrate pagination
        total_processed = 0
        total_size = 0

        for page_num, page in enumerate(query.paginate(10), 1):
            page_size = sum(f.size.bytes for f in page)
            total_size += page_size
            total_processed += len(page)

            print(f"Page {page_num}: {len(page)} files, {page_size:,} bytes")

            # Show first few files in each page
            for file in page[:3]:  # Show first 3 files
                print(f"  📄 {file.name} ({file.size.bytes} bytes)")

            if len(page) > 3:
                print(f"  ... and {len(page) - 3} more files")

        print("\n📊 Summary:")
        print(f"Total pages: {page_num}")
        print(f"Total files: {total_processed}")
        print(f"Total size: {total_size:,} bytes")

        # Demonstrate manual page access
        print("\n🔧 Manual page access:")
        print("-" * 40)

        paginator = query.paginate(15)

        # Get specific pages
        first_page = next(paginator, [])
        print(f"First page: {len(first_page)} files")

        second_page = next(paginator, [])
        print(f"Second page: {len(second_page)} files")

        third_page = next(paginator, [])
        print(f"Third page: {len(third_page)} files")

        fourth_page = next(paginator, [])
        print(f"Fourth page: {len(fourth_page)} files")

        # Demonstrate efficiency - single scan
        print("\n⚡ Efficiency demonstration:")
        print("-" * 40)
        print("Each file is processed exactly once - O(n) performance!")
        print("Memory usage is O(page_size), not O(total_files)")

        # Show streaming vs materialization
        print("\n🔄 Streaming vs Materialization:")
        print("-" * 40)

        # Streaming approach (recommended for large datasets)
        print("Streaming approach (memory efficient):")
        count = 0
        for page in query.paginate(5):
            count += len(page)
            print(f"  Processed page: {len(page)} files (total so far: {count})")
            # In real use, you'd process each file here

        # Materialization approach (when you need all pages)
        print("\nMaterialization approach (when you need all pages):")
        all_pages = list(query.paginate(5))
        print(
            f"  Got {len(all_pages)} pages with {sum(len(p) for p in all_pages)} total files"
        )
        print(f"  Can now access any page: page 1 has {len(all_pages[0])} files")


if __name__ == "__main__":
    demo_pagination()
