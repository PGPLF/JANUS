#!/usr/bin/env python3
"""
Weekly arXiv monitoring for new JWST high-z datasets
Execute every Monday morning

Usage:
    python3 weekly_arxiv_monitor.py
    python3 weekly_arxiv_monitor.py --days 14  # Look back 14 days
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import argparse
from pathlib import Path
import json
import re
import ssl

# SSL context for macOS
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Configuration
ARXIV_API = "http://export.arxiv.org/api/query"
DATA_DIR = Path(__file__).parent.parent / "data" / "monitoring"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Keywords for filtering
KEYWORDS_PRIMARY = [
    "JWST", "James Webb",
    "high redshift", "high-z", "z>8", "z>10", "z>12",
    "early galaxies", "primordial galaxies",
    "UV luminosity function", "stellar mass function",
    "cosmic dawn", "reionization"
]

KEYWORDS_SURVEY = [
    "JADES", "CEERS", "GLASS", "UNCOVER", "COSMOS-Web",
    "EXCELS", "A3COSMOS", "FRESCO", "PRIMER"
]

KEYWORDS_DATA = [
    "catalog", "catalogue", "data release", "photometry",
    "spectroscopy", "redshift", "luminosity function"
]

def search_arxiv(query, max_results=100, days_back=7):
    """Search arXiv API"""

    # Build query
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30, context=ssl_context) as response:
            data = response.read()
        return ET.fromstring(data)
    except Exception as e:
        print(f"Error fetching arXiv: {e}")
        return None

def parse_entries(root, days_back=7):
    """Parse arXiv entries"""

    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []

    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_back)

    for entry in root.findall('atom:entry', ns):
        try:
            # Extract fields
            arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text

            # Parse date
            pub_date = datetime.datetime.fromisoformat(published.replace('Z', '+00:00'))

            # Skip if too old
            if pub_date.replace(tzinfo=None) < cutoff_date:
                continue

            # Authors (first 3)
            authors = []
            for author in entry.findall('atom:author', ns)[:3]:
                name = author.find('atom:name', ns).text
                authors.append(name)

            # Categories
            categories = []
            for cat in entry.findall('atom:category', ns):
                categories.append(cat.get('term'))

            entries.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'summary': summary[:500],
                'published': pub_date.strftime('%Y-%m-%d'),
                'categories': categories
            })

        except Exception as e:
            continue

    return entries

def classify_relevance(entry):
    """Classify paper relevance"""

    text = (entry['title'] + ' ' + entry['summary']).lower()

    # Check for data releases (highest priority)
    data_score = sum(1 for kw in KEYWORDS_DATA if kw.lower() in text)

    # Check for surveys
    survey_score = sum(1 for kw in KEYWORDS_SURVEY if kw.lower() in text)

    # Check for high-z keywords
    highz_score = sum(1 for kw in KEYWORDS_PRIMARY if kw.lower() in text)

    # Check for specific redshift mentions
    z_mentions = re.findall(r'z\s*[>=~]\s*(\d+)', text)
    has_highz = any(float(z) >= 8 for z in z_mentions if z.isdigit())

    # Classify
    if data_score >= 2 or (data_score >= 1 and survey_score >= 1):
        return 'HIGH', data_score + survey_score + highz_score
    elif survey_score >= 1 and highz_score >= 2:
        return 'MEDIUM', survey_score + highz_score
    elif highz_score >= 2 or has_highz:
        return 'LOW', highz_score
    else:
        return None, 0

def generate_report(entries, week_num, year):
    """Generate markdown report"""

    # Classify entries
    classified = []
    for entry in entries:
        priority, score = classify_relevance(entry)
        if priority:
            entry['priority'] = priority
            entry['score'] = score
            classified.append(entry)

    # Sort by priority and score
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    classified.sort(key=lambda x: (priority_order[x['priority']], -x['score']))

    # Create report
    report_dir = DATA_DIR / f"{year}_W{week_num:02d}"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "weekly_report.md"

    with open(report_file, 'w') as f:
        f.write(f"# Veille Hebdomadaire - Semaine {week_num}/{year}\n\n")
        f.write(f"**Date**: {datetime.date.today()}\n")
        f.write(f"**Articles analysés**: {len(entries)}\n")
        f.write(f"**Articles pertinents**: {len(classified)}\n\n")

        f.write("---\n\n")

        # By priority
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            papers = [e for e in classified if e['priority'] == priority]
            if papers:
                f.write(f"## {priority} Priority ({len(papers)})\n\n")

                for p in papers:
                    f.write(f"### [{p['arxiv_id']}] {p['title']}\n")
                    f.write(f"- **Authors**: {', '.join(p['authors'])}\n")
                    f.write(f"- **Date**: {p['published']}\n")
                    f.write(f"- **arXiv**: https://arxiv.org/abs/{p['arxiv_id']}\n")
                    f.write(f"- **Categories**: {', '.join(p['categories'][:3])}\n")
                    f.write(f"\n> {p['summary'][:300]}...\n\n")

        if not classified:
            f.write("*Aucun article pertinent cette semaine.*\n")

        f.write("---\n\n")
        f.write("*Généré automatiquement par weekly_arxiv_monitor.py*\n")

    # Also save JSON
    json_file = report_dir / "papers.json"
    with open(json_file, 'w') as f:
        json.dump(classified, f, indent=2)

    return report_file, classified

def main():
    parser = argparse.ArgumentParser(description='Weekly arXiv monitor for JWST high-z')
    parser.add_argument('--days', type=int, default=7, help='Days to look back')
    args = parser.parse_args()

    print("="*60)
    print("WEEKLY ARXIV MONITOR - JWST High-z Galaxies")
    print("="*60)
    print(f"Date: {datetime.date.today()}")
    print(f"Looking back: {args.days} days")

    # Build search query
    query = 'cat:astro-ph.GA AND (JWST OR "high redshift" OR "z>8")'

    print(f"\nSearching arXiv...")
    root = search_arxiv(query, max_results=200, days_back=args.days)

    if root is None:
        print("Failed to fetch arXiv data")
        return

    # Parse entries
    entries = parse_entries(root, days_back=args.days)
    print(f"Found {len(entries)} papers in last {args.days} days")

    # Generate report
    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    year = today.year

    report_file, classified = generate_report(entries, week_num, year)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("="*60)

    high = len([e for e in classified if e['priority'] == 'HIGH'])
    medium = len([e for e in classified if e['priority'] == 'MEDIUM'])
    low = len([e for e in classified if e['priority'] == 'LOW'])

    print(f"HIGH priority:   {high}")
    print(f"MEDIUM priority: {medium}")
    print(f"LOW priority:    {low}")

    if high > 0:
        print(f"\n⚠️  {high} HIGH PRIORITY papers found!")
        for e in [x for x in classified if x['priority'] == 'HIGH']:
            print(f"   - {e['arxiv_id']}: {e['title'][:60]}...")

    print(f"\nReport saved to: {report_file}")

    return classified

if __name__ == "__main__":
    main()
