"""Run on DB-S01: register lecture entry points without exposing the registry key."""
import json
import subprocess
import urllib.request

container = json.loads(subprocess.check_output(['docker', 'inspect', 'pm-web']))[0]
env = dict(item.split('=', 1) for item in container['Config']['Env'] if '=' in item)
key = env.get('PM_REGISTRY_KEY')
if not key:
    raise SystemExit('Registry key is not configured; service registration was not changed.')
base = 'http://192.168.1.64:3110'
for name, title, category, link in [
    ('kifu-kouza-2026', '2026年度 寄付講座スライド', 'webui', '/'),
    ('kifu-kouza-2026-mgmt', '寄付講座 管理・セリフダウンロード', 'management', '/admin.html'),
]:
    payload = {
        'name': name, 'display_name': title, 'category': category,
        'badge_label': '講義' if category == 'webui' else '管理',
        'badge_type': 'app' if category == 'webui' else 'manage',
        'description': '技術者と社会 / みのる化成 / 59ページ・90分 / 2画面対応',
        'web_url': base + link, 'status': 'active', 'sort_order': 70,
        'project_key': 'kifu-kouza-2026', 'metadata_url': base + '/metadata.json',
    }
    request = urllib.request.Request(
        'http://127.0.0.1:8080/api/registry/services',
        data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={'Content-Type': 'application/json', 'X-Registry-Key': key},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        response.read()
        print(name + ': HTTP ' + str(response.status))
