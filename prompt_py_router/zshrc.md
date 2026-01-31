# 将以下内容添加到 ~/.zshrc
ag-plan() {
    # 1. 路由增强并写入临时变量
    local raw_input="$1"
    local enhanced_prompt=$(echo "$raw_input" | python3 ~/Users/a58/work/skills/prompt_py_router/ag_router.py)

    # 2. 注入剪贴板
    echo "$enhanced_prompt" | pbcopy

    # 3. macOS 窗口劫持注入
    osascript <<EOF
        tell application "System Events"
            # 这里的 "Antigravity" 需对应你 IDE 的实际 Process Name
            set frontmost of process "Antigravity" to true
            delay 0.3
            keystroke "a" using {command down} -- 全选旧内容
            keystroke "v" using {command down} -- 粘贴增强内容
        end tell
EOF
    echo "🚀 匹配完成。内容已注入 Antigravity，请审计后回车。"
}