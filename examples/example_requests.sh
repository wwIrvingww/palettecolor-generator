# Pruebas automáticas para palettecolor-generator

echo "1) remote_hello"
curl -s -X POST http://127.0.0.1:8000/mcp/run \
  -H "Content-Type: application/json" \
  -d '{"tool":"remote_hello","input":{"name":"Irving"}}' | jq

echo ""
echo "2) palette triadic"
curl -s -X POST http://127.0.0.1:8000/mcp/run \
  -H "Content-Type: application/json" \
  -d '{"tool":"palette_generator","input":{"base_color":"#3498db","mode":"triadic"}}' | jq
