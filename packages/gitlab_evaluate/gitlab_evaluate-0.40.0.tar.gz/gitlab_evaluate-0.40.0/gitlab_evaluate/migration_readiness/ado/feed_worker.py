"""
Standalone worker functions for multiprocessing feed processing.
This module is kept minimal to avoid circular import issues when spawning worker processes.
"""
import json
from dateutil import parser

from gitlab_evaluate.migration_readiness.ado.evaluate import AdoEvaluateClient


def process_feed_packages(host, token, api_version, verify, feed):
    """Top-level function for multiprocessing to process feed packages.
    Creates its own ADO client to avoid pickling issues.
    Returns a list of package data dictionaries for aggregation."""
    ado_client = AdoEvaluateClient(host, token, api_version=api_version, verify=verify)
    project_id = feed.get('project', {}).get('id') if feed.get('project') else None
    
    if feed.get('project'):
        print(f"Processing feed {feed['name']} in project {feed['project']['name']}...")
    else:
        print(f"Processing feed {feed['name']} in organization scope...")
    
    packages_params = {}
    
    packages_response = ado_client.retry_request(
        ado_client.get_packages, packages_params, feed['id'], project_id
    )
    if not packages_response or packages_response.status_code != 200:
        print(f"Failed to fetch packages for feed {feed['name']}: {packages_response.text if packages_response else 'No response'}")
        return []
        
    packages = packages_response.json()
    package_data_list = []
    
    for package in packages.get("value", []):
        print(f"Processing package {package.get('name', 'Unknown')} in feed {feed['name']}...")
        
        # Get package versions using the versions endpoint
        versions = _get_package_versions(ado_client, feed['id'], package, project_id)
        
        # Get version-specific metrics
        version_metrics = _get_version_metrics(ado_client, feed['id'], package, versions, project_id)
        
        # Build comprehensive package data (without updating shared state)
        # Returns a list of entries, one per version
        package_entries = _build_package_data(feed, package, versions, version_metrics)
        package_data_list.extend(package_entries)

    # check if rate limit has been hit
    ado_client.wait_timer(packages_response.headers, "Packages List")
    
    return package_data_list


def _get_package_versions(ado_client, feed_id, package, project_id):
    """Get available versions for a package using the versions endpoint.
    GET https://feeds.dev.azure.com/{organization}/{project}/_apis/packaging/Feeds/{feedId}/Packages/{packageId}/versions
    """
    try:
        versions_response = ado_client.retry_request(
            ado_client.get_package_versions, {},
            feed_id, package.get('id'), project_id
        )
        
        if versions_response and versions_response.status_code == 200:
            versions_data = versions_response.json()
            print(f"Retrieved {len(versions_data.get('value', []))} versions for package {package.get('name', 'Unknown')}")
            return versions_data.get('value', [])
        else:
            print(f"Failed to get versions for package {package.get('name', 'Unknown')}: {versions_response.text if versions_response else 'No response'}")
            # Fall back to versions from the package object
            return package.get('versions', [])
            
    except Exception as e:
        print(f"Error getting package versions: {e}")
        # Fall back to versions from the package object
        return package.get('versions', [])


def _get_version_metrics(ado_client, feed_id, package, versions, project_id):
    """Get version metrics using versionmetricsbatch endpoint.
    POST https://feeds.dev.azure.com/{organization}/{project}/_apis/packaging/Feeds/{feedId}/Packages/{packageId}/versionmetricsbatch
    Returns a dict mapping version_id to metrics (downloadCount, lastDownloaded).
    """
    if not versions:
        return {}
    
    try:
        # Extract version IDs from versions list
        version_ids = [v.get('id') for v in versions if v.get('id')]
        
        if not version_ids:
            print(f"No version IDs found for package {package.get('name', 'Unknown')}")
            return {}
        
        metrics_payload = json.dumps({
            "packageVersionIds": version_ids
        })
        
        metrics_response = ado_client.get_package_version_metrics_batch(
            payload=metrics_payload,
            feed_id=feed_id,
            package_id=package.get('id'),
            project_id=project_id
        )
        
        if metrics_response and metrics_response.status_code == 200:
            metrics_data = metrics_response.json()
            print(f"Retrieved version metrics for package {package.get('name', 'Unknown')}")
            
            # Build a dict mapping version_id to metrics
            version_metrics = {}
            for metric in metrics_data.get('value', []):
                version_id = metric.get('packageVersionId')
                if version_id:
                    version_metrics[version_id] = {
                        'downloadCount': metric.get('downloadCount', 0),
                        'lastDownloaded': metric.get('lastDownloaded', 'N/A')
                    }
            return version_metrics
        else:
            status = metrics_response.status_code if metrics_response else 'None'
            text = metrics_response.text if metrics_response else 'No response'
            print(f"Failed to get version metrics for package {package.get('name', 'Unknown')} (status={status}): {text}")
            return {}
            
    except Exception as e:
        import traceback
        print(f"Error getting version metrics for {package.get('name', 'Unknown')}: {e}")
        traceback.print_exc()
        return {}


def convert_utc_to_local(utc_time):
    """Convert UTC time to local time."""
    if utc_time == 'N/A' or utc_time is None:
        return 'N/A'
    try:
        return parser.parse(utc_time).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return utc_time


def _build_package_data(feed, package, versions, version_metrics):
    """Build comprehensive package data for multiprocessing.
    Returns a list of package data dicts, one per version, with metadata for later aggregation.
    
    Args:
        feed: Feed data dictionary
        package: Package data dictionary
        versions: List of version objects from the versions endpoint
        version_metrics: Dict mapping version_id to metrics (downloadCount, lastDownloaded)
    """
    package_type = package.get('protocolType', 'Unknown')
    
    package_entries = []
    
    # If no versions, create a single entry with N/A version info
    if not versions:
        return [{
            'Scope': 'Project' if feed.get('project') else 'Organization',
            'Project ID': feed.get('project', {}).get('id', 'N/A') if feed.get('project') else 'N/A',
            'Project Name': feed.get('project', {}).get('name', 'N/A') if feed.get('project') else 'N/A',
            'Feed ID': feed.get('id', 'N/A'),
            'Feed Name': feed.get('name', 'N/A'),
            'Package ID': package.get('id', 'N/A'),
            'Package Name': package.get('name', 'N/A'),
            'Package Type': package_type,
            'Version': 'N/A',
            'isLatest': False,
            'isListed': False,
            'Total Downloads': 'N/A',
            'Publish date': 'N/A',
            'Last downloaded': 'N/A',
            'Upstream Source ID': 'N/A',
            'Upstream Source URL': 'N/A',
            'Upstream Source Type': 'N/A',
            '_is_from_upstream': False
        }]
    
    # Create an entry for each version
    for version in versions:
        version_id = version.get('id')
        version_name = version.get('version', 'N/A')
        is_latest = version.get('isLatest', False)
        is_listed = version.get('isListed', False)
        publish_date = convert_utc_to_local(version.get('publishDate'))
        upstream_source_id = version.get('directUpstreamSourceId', 'N/A')
        
        # Get version-specific metrics
        metrics = version_metrics.get(version_id, {})
        total_downloads = metrics.get('downloadCount', 'N/A')
        last_download_date = convert_utc_to_local(metrics.get('lastDownloaded', 'N/A'))
        
        upstream_source_url = "N/A"
        upstream_source_type = "N/A"
        
        if upstream_source_id != "N/A" and feed.get('upstreamSources'):
            for upstream_source in feed['upstreamSources']:
                if upstream_source.get('id') == upstream_source_id:
                    upstream_source_url = upstream_source.get('location', 'N/A')
                    upstream_source_type = upstream_source.get('upstreamSourceType', 'N/A')
                    break
        
        # Include metadata for aggregation (is_from_upstream)
        is_from_upstream = upstream_source_url != "N/A"
        
        package_entries.append({
            'Scope': 'Project' if feed.get('project') else 'Organization',
            'Project ID': feed.get('project', {}).get('id', 'N/A') if feed.get('project') else 'N/A',
            'Project Name': feed.get('project', {}).get('name', 'N/A') if feed.get('project') else 'N/A',
            'Feed ID': feed.get('id', 'N/A'),
            'Feed Name': feed.get('name', 'N/A'),
            'Package ID': package.get('id', 'N/A'),
            'Package Name': package.get('name', 'N/A'),
            'Package Type': package_type,
            'Version': version_name,
            'isLatest': is_latest,
            'isListed': is_listed,
            'Total Downloads': total_downloads,
            'Publish date': publish_date,
            'Last downloaded': last_download_date,
            'Upstream Source ID': upstream_source_id,
            'Upstream Source URL': upstream_source_url,
            'Upstream Source Type': upstream_source_type,
            '_is_from_upstream': is_from_upstream  # Metadata for aggregation
        })
    
    return package_entries
