from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, re
from typing import Dict, List, Tuple

# Models
class RunRequest(BaseModel):
    tool: str
    input: Dict = {}

# Color utils
HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    if not HEX_RE.match(hex_code):
        raise ValueError("HEX inválido")
    h = hex_code.lstrip("#")
    if len(h) == 3:
        h = "".join([c*2 for c in h])
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return r, g, b

def _rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(round(r))))
    g = max(0, min(255, int(round(g))))
    b = max(0, min(255, int(round(b))))
    return f"#{r:02X}{g:02X}{b:02X}"

def _rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    rf, gf, bf = r/255.0, g/255.0, b/255.0
    mx, mn = max(rf, gf, bf), min(rf, gf, bf)
    d = mx - mn
    l = (mx + mn) / 2.0
    if d == 0:
        h = 0.0
        s = 0.0
    else:
        s = d / (1 - abs(2*l - 1))
        if mx == rf:
            hprime = ((gf - bf) / d) % 6
        elif mx == gf:
            hprime = (bf - rf) / d + 2
        else:
            hprime = (rf - gf) / d + 4
        h = 60.0 * hprime
    return h % 360.0, s, l

def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h = h % 360.0
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h/60.0) % 2 - 1))
    m = l - c/2.0
    if   0 <= h < 60:   rp, gp, bp = c, x, 0
    elif 60 <= h < 120: rp, gp, bp = x, c, 0
    elif 120 <= h < 180:rp, gp, bp = 0, c, x
    elif 180 <= h < 240:rp, gp, bp = 0, x, c
    elif 240 <= h < 300:rp, gp, bp = x, 0, c
    else:               rp, gp, bp = c, 0, x
    r = (rp + m) * 255
    g = (gp + m) * 255
    b = (bp + m) * 255
    return int(round(r)), int(round(g)), int(round(b))

def _hex_to_hsl(hex_code: str) -> Tuple[float, float, float]:
    r, g, b = _hex_to_rgb(hex_code)
    return _rgb_to_hsl(r, g, b)

def _hsl_to_hex(h: float, s: float, l: float) -> str:
    r, g, b = _hsl_to_rgb(h, s, l)
    return _rgb_to_hex(r, g, b)

def _shift_hue(h: float, delta: float) -> float:
    return (h + delta) % 360.0

def _generate_palette(base_hex: str, mode: str) -> List[str]:
    h, s, l = _hex_to_hsl(base_hex)
    mode = mode.lower().strip()
    if mode == "complementary":
        hues = [h, _shift_hue(h, 180)]
    elif mode == "analogous":
        hues = [ _shift_hue(h, -30), h, _shift_hue(h, 30) ]
    elif mode == "triadic":
        hues = [ h, _shift_hue(h, 120), _shift_hue(h, 240) ]
    elif mode == "split_complementary":
        # 180 ± 30 => h+150 y h+210
        hues = [ h, _shift_hue(h, 150), _shift_hue(h, 210) ]
    elif mode == "tetradic":
        hues = [ h, _shift_hue(h, 90), _shift_hue(h, 180), _shift_hue(h, 270) ]
    else:
        raise ValueError("mode no soportado")
    return [_hsl_to_hex(H, s, l) for H in hues]

# ---------- FastAPI ----------
app = FastAPI(title="remote-hello/palette")

@app.get("/")
def root():
    return {"service": "remote-hello", "status": "ok"}

@app.get("/tools")
def list_tools():
    return {"tools": ["remote_hello", "palette_generator"]}

@app.post("/mcp/run")
def mcp_run(req: RunRequest):
    tool = req.tool
    data = req.input or {}

    if tool == "remote_hello":
        name = data.get("name") or data.get("user") or "mundo"
        return {"result": f"Hola {name} desde Remote Hello"}

    if tool == "palette_generator":
        base = data.get("base_color")
        mode = data.get("mode")
        if not isinstance(base, str) or not HEX_RE.match(base):
            raise HTTPException(status_code=400, detail="base_color inválido (usa #RRGGBB o #RGB)")
        if not isinstance(mode, str):
            raise HTTPException(status_code=400, detail="mode requerido")
        try:
            palette = _generate_palette(base, mode)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"palette": palette}

    raise HTTPException(status_code=404, detail="tool not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
