"""Check the end of the JSON"""
with open('mcp_response.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print("Last 500 chars:")
print(content[-500:])
print("\n" + "=" * 70)
print(f"Total length: {len(content)}")
print(f"Last char: {repr(content[-1])}")
print(f"Last 10 chars: {repr(content[-10:])}")

# Find JSON start
json_start = content.find('{"chart":')
print(f"\nJSON starts at position: {json_start}")

if json_start != -1:
    json_str = content[json_start:]
    print(f"JSON length: {len(json_str)}")
    print(f"JSON last 100 chars: {json_str[-100:]}")
