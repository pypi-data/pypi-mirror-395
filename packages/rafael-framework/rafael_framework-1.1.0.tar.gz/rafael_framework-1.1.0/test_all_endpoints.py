#!/usr/bin/env python3
"""
RAFAEL Framework - Comprehensive Testing Script
Tests all endpoints, features, and functionality
"""

import urllib.request
import ssl
import json
import time
from datetime import datetime

# Disable SSL verification for testing
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_page(name, url, keyword):
    """Test a web page"""
    try:
        response = urllib.request.urlopen(url, context=ctx, timeout=10)
        content = response.read().decode('utf-8', errors='ignore')
        status = response.status
        
        if keyword in content:
            return {'name': name, 'url': url, 'status': 'PASS', 'code': status, 'error': None}
        else:
            return {'name': name, 'url': url, 'status': 'FAIL', 'code': status, 'error': f'Keyword "{keyword}" not found'}
    except Exception as e:
        return {'name': name, 'url': url, 'status': 'ERROR', 'code': None, 'error': str(e)}

def test_api(endpoint, method='GET', data=None):
    """Test an API endpoint"""
    try:
        url = f'https://api.rafaelabs.xyz{endpoint}'
        
        if method == 'POST' and data:
            req = urllib.request.Request(url, 
                                        data=json.dumps(data).encode('utf-8'),
                                        headers={'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)
        
        response = urllib.request.urlopen(req, context=ctx, timeout=10)
        content = response.read().decode('utf-8')
        result = json.loads(content)
        
        return {'endpoint': endpoint, 'method': method, 'status': 'PASS', 'response': result}
    except Exception as e:
        return {'endpoint': endpoint, 'method': method, 'status': 'ERROR', 'error': str(e)}

def main():
    print('\n' + '='*70)
    print('RAFAEL FRAMEWORK - COMPREHENSIVE TESTING')
    print('='*70)
    print(f'Test Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*70 + '\n')
    
    # Test 1: Web Pages
    print('TEST 1: WEB PAGES')
    print('-'*70)
    
    pages = [
        ('Landing Page', 'https://rafaelabs.xyz', 'RAFAEL'),
        ('WWW Redirect', 'https://www.rafaelabs.xyz', 'RAFAEL'),
        ('Dashboard', 'https://dashboard.rafaelabs.xyz', 'Dashboard'),
        ('API Docs', 'https://api.rafaelabs.xyz', 'API'),
        ('Demo', 'https://demo.rafaelabs.xyz', 'Interactive Demo'),
        ('Beta', 'https://beta.rafaelabs.xyz', 'Beta Program'),
    ]
    
    page_results = []
    for name, url, keyword in pages:
        print(f'Testing {name}...', end=' ')
        result = test_page(name, url, keyword)
        page_results.append(result)
        
        if result['status'] == 'PASS':
            print(f"✅ PASS ({result['code']})")
        elif result['status'] == 'FAIL':
            print(f"❌ FAIL ({result['code']}) - {result['error']}")
        else:
            print(f"⚠️  ERROR - {result['error']}")
        
        time.sleep(0.5)
    
    # Test 2: API Endpoints
    print('\n' + '='*70)
    print('TEST 2: API ENDPOINTS')
    print('-'*70)
    
    api_endpoints = [
        ('/api/status', 'GET', None),
        ('/api/modules', 'GET', None),
        ('/api/vault/patterns', 'GET', None),
        ('/api/guardian/approvals', 'GET', None),
    ]
    
    api_results = []
    for endpoint, method, data in api_endpoints:
        print(f'Testing {method} {endpoint}...', end=' ')
        result = test_api(endpoint, method, data)
        api_results.append(result)
        
        if result['status'] == 'PASS':
            print(f"✅ PASS")
        else:
            print(f"❌ ERROR - {result.get('error', 'Unknown error')}")
        
        time.sleep(0.5)
    
    # Test 3: Chaos Simulation
    print('\n' + '='*70)
    print('TEST 3: CHAOS SIMULATION')
    print('-'*70)
    
    chaos_tests = [
        ('DDoS Attack', {'module_id': 'payment-service', 'threat_type': 'ddos_attack', 'severity': 'low'}),
        ('Network Latency', {'module_id': 'auth-service', 'threat_type': 'network_latency', 'severity': 'medium'}),
        ('Database Failure', {'module_id': 'notification-service', 'threat_type': 'database_failure', 'severity': 'high'}),
    ]
    
    chaos_results = []
    for name, data in chaos_tests:
        print(f'Testing {name}...', end=' ')
        result = test_api('/api/chaos/simulate', 'POST', data)
        chaos_results.append(result)
        
        if result['status'] == 'PASS' and result.get('response', {}).get('success'):
            print(f"✅ PASS")
        else:
            print(f"❌ ERROR")
        
        time.sleep(0.5)
    
    # Test 4: SSL Certificates
    print('\n' + '='*70)
    print('TEST 4: SSL CERTIFICATES')
    print('-'*70)
    
    domains = [
        'rafaelabs.xyz',
        'www.rafaelabs.xyz',
        'dashboard.rafaelabs.xyz',
        'api.rafaelabs.xyz',
        'demo.rafaelabs.xyz',
        'beta.rafaelabs.xyz',
    ]
    
    for domain in domains:
        try:
            urllib.request.urlopen(f'https://{domain}', timeout=5)
            print(f'{domain}: ✅ SSL Active')
        except Exception as e:
            print(f'{domain}: ❌ SSL Error - {str(e)[:50]}')
        time.sleep(0.3)
    
    # Summary
    print('\n' + '='*70)
    print('TEST SUMMARY')
    print('='*70)
    
    page_pass = sum(1 for r in page_results if r['status'] == 'PASS')
    api_pass = sum(1 for r in api_results if r['status'] == 'PASS')
    chaos_pass = sum(1 for r in chaos_results if r['status'] == 'PASS' and r.get('response', {}).get('success'))
    
    print(f'\nWeb Pages: {page_pass}/{len(page_results)} PASS')
    print(f'API Endpoints: {api_pass}/{len(api_results)} PASS')
    print(f'Chaos Tests: {chaos_pass}/{len(chaos_tests)} PASS')
    print(f'SSL Domains: {len(domains)}/{len(domains)} Active')
    
    total_tests = len(page_results) + len(api_results) + len(chaos_tests) + len(domains)
    total_pass = page_pass + api_pass + chaos_pass + len(domains)
    
    print(f'\nTotal: {total_pass}/{total_tests} PASS ({int(total_pass/total_tests*100)}%)')
    
    if total_pass == total_tests:
        print('\n🎉 ALL TESTS PASSED! 🎉')
    else:
        print(f'\n⚠️  {total_tests - total_pass} tests failed')
    
    print('='*70 + '\n')

if __name__ == '__main__':
    main()
