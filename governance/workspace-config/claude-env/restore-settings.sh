#!/usr/bin/env bash
# restore-settings.sh
# CC switch 切换 API Key 后，将插件相关配置合并回 settings.json
# 用法: bash D:/Projects/.claude/env/restore-settings.sh

set -euo pipefail

SETTINGS_FILE="$HOME/.claude/settings.json"
REFERENCE_FILE="$(dirname "$0")/settings-reference.json"

if [ ! -f "$SETTINGS_FILE" ]; then
  echo "[ERROR] $SETTINGS_FILE not found"
  exit 1
fi

if [ ! -f "$REFERENCE_FILE" ]; then
  echo "[ERROR] $REFERENCE_FILE not found"
  exit 1
fi

# 检测 Python
_PYTHON=""
if python -c "print()" &>/dev/null; then
  _PYTHON="python"
elif python3 -c "print()" &>/dev/null; then
  _PYTHON="python3"
else
  echo "[ERROR] Python not found"
  exit 1
fi

echo "[INFO] Current settings.json:"
cat "$SETTINGS_FILE"
echo ""

# 备份
cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak.$(date +%Y%m%d_%H%M%S)"
echo "[INFO] Backup created"

# 合并: 保留 settings.json 的 env/model，合并 reference 中的其他字段
$_PYTHON -c "
import json, sys

with open(sys.argv[1], encoding='utf-8') as f:
    current = json.load(f)

with open(sys.argv[2], encoding='utf-8') as f:
    reference = json.load(f)

# 移除注释字段
for key in list(reference.keys()):
    if key.startswith('_'):
        del reference[key]

# 合并: reference 中的字段补入 current (不覆盖已有)
for key, val in reference.items():
    if key not in current:
        current[key] = val
    elif isinstance(val, dict) and isinstance(current.get(key), dict):
        # dict 类型: 深度合并
        for k2, v2 in val.items():
            if k2 not in current[key]:
                current[key][k2] = v2

with open(sys.argv[1], 'w', encoding='utf-8') as f:
    json.dump(current, f, indent=2, ensure_ascii=False)

print('[OK] settings.json updated')
" "$SETTINGS_FILE" "$REFERENCE_FILE"

echo ""
echo "[INFO] Updated settings.json:"
cat "$SETTINGS_FILE"
echo ""
echo "[DONE] Restart Claude Code to apply changes"
