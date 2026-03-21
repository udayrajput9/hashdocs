"""
Pre-designed certificate templates with placeholders.
These are injected via the template gallery.
"""

# Common text styles
TITLE_STYLE = {"type":"i-text", "fontSize":48, "fontWeight":"bold", "fill":"#1a1a2e", "textAlign":"center", "originX":"center", "top":120, "left":500, "fontFamily":"Inter, Arial"}
SUBTITLE_STYLE = {"type":"i-text", "fontSize":24, "fill":"#4b5563", "textAlign":"center", "originX":"center", "top":220, "left":500, "fontFamily":"Inter, Arial"}
NAME_STYLE = {"type":"i-text", "fontSize":64, "fontWeight":"bold", "fill":"#2563eb", "textAlign":"center", "originX":"center", "top":280, "left":500, "fontFamily":"Inter, Arial"}
COURSE_STYLE = {"type":"i-text", "fontSize":32, "fill":"#1a1a2e", "textAlign":"center", "originX":"center", "top":400, "left":500, "fontFamily":"Inter, Arial"}

# Base shape templates
def _rect(left, top, w, h, fill, opacity=1.0):
    return {"type":"rect", "left":left, "top":top, "width":w, "height":h, "fill":fill, "opacity":opacity}

def _line(x1, y1, x2, y2, stroke="#000", w=2):
    return {"type":"line", "left":x1, "top":y1, "x1":0, "y1":0, "x2":x2-x1, "y2":y2-y1, "stroke":stroke, "strokeWidth":w}


TEMPLATE_PRESETS = [
    {
        "id": "academic_classic",
        "name": "Academic Classic Blue",
        "category": "academic",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#f8fafc",
            "objects": [
                # Borders
                _rect(40, 40, 920, 620, "transparent"),
                {"type":"rect", "left":35, "top":35, "width":930, "height":630, "fill":"transparent", "stroke":"#1e3a8a", "strokeWidth":8},
                {"type":"rect", "left":45, "top":45, "width":910, "height":610, "fill":"transparent", "stroke":"#d1d5db", "strokeWidth":2},
                
                # Accents
                _rect(0, 0, 1000, 20, "#1e3a8a"),
                _rect(0, 680, 1000, 20, "#1e3a8a"),

                # Text
                {**TITLE_STYLE, "text": "CERTIFICATE OF ACHIEVEMENT"},
                {**SUBTITLE_STYLE, "text": "This proudly confirms that"},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#1e3a8a"},
                {**SUBTITLE_STYLE, "text": "has successfully completed the requirements for", "top":360, "fontSize":20},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#111827", "fontWeight":"bold"},
                
                # Signatures
                _line(200, 580, 400, 580, "#94a3b8"),
                {"type":"i-text", "text":"Issue Date: {{date}}", "left":300, "top":590, "fontSize":16, "originX":"center", "fill":"#64748b"},
                
                _line(600, 580, 800, 580, "#94a3b8"),
                {"type":"i-text", "text":"{{organization}}", "left":700, "top":590, "fontSize":16, "originX":"center", "fill":"#64748b", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "modern_minimal",
        "name": "Modern Minimalist",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                # Left accent
                _rect(0, 0, 80, 700, "#2563eb"),
                _rect(80, 0, 10, 700, "#60a5fa", 1.0),
                
                # Text
                {**TITLE_STYLE, "text": "CERTIFICATE", "left":540, "top":120, "fontSize":56, "textAlign":"left", "originX":"center"},
                {**TITLE_STYLE, "text": "OF COMPLETION", "left":540, "top":180, "fontSize":24, "fontWeight":"normal", "fill":"#64748b"},
                
                {"type":"i-text", "text":"Presented to", "left":160, "top":280, "fontSize":18, "fill":"#94a3b8"},
                {**NAME_STYLE, "text": "{{name}}", "left":160, "top":310, "textAlign":"left", "originX":"left", "fill":"#111827", "fontSize":48},
                
                {"type":"i-text", "text":"For outstanding performance in:", "left":160, "top":420, "fontSize":18, "fill":"#94a3b8"},
                {**COURSE_STYLE, "text": "{{course}}", "left":160, "top":450, "textAlign":"left", "originX":"left", "fontWeight":"bold", "fontSize":28},
                
                # Footer
                {"type":"i-text", "text":"Authorized by: {{organization}}", "left":160, "top":620, "fontSize":14, "fill":"#64748b"},
                {"type":"i-text", "text":"Date: {{date}}", "left":850, "top":620, "fontSize":14, "originX":"right", "fill":"#64748b"},
            ]
        }
    },
    {
        "id": "gold_prestige",
        "name": "Gold Prestige",
        "category": "achievement",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#0f172a",
            "objects": [
                {"type":"rect", "left":20, "top":20, "width":960, "height":660, "fill":"transparent", "stroke":"#fbbf24", "strokeWidth":4},
                {"type":"rect", "left":30, "top":30, "width":940, "height":640, "fill":"transparent", "stroke":"#fcd34d", "strokeWidth":1, "opacity":0.5},
                
                {**TITLE_STYLE, "text": "AWARD OF EXCELLENCE", "fill":"#fbbf24", "top":100, "fontSize":42},
                
                {"type":"line", "left":300, "top":160, "x1":0, "y1":0, "x2":400, "y2":0, "stroke":"#fbbf24", "strokeWidth":2, "originX":"left"},
                
                {**SUBTITLE_STYLE, "text": "Is hereby granted to", "fill":"#94a3b8", "top":200},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#ffffff", "top":260, "fontSize":56},
                
                {**SUBTITLE_STYLE, "text": "in recognition of their dedication to", "fill":"#94a3b8", "top":360, "fontSize":18},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#fbbf24", "top":400},
                
                {"type":"i-text", "text":"Date: {{date}}", "left":500, "top":500, "fontSize":16, "originX":"center", "fill":"#64748b"},
                
                {"type":"line", "left":400, "top":600, "x1":0, "y1":0, "x2":200, "y2":0, "stroke":"#fbbf24", "strokeWidth":1},
                {"type":"i-text", "text":"{{organization}}", "left":500, "top":615, "fontSize":18, "originX":"center", "fill":"#f8fafc"},
            ]
        }
    },
    {
        "id": "corporate_modern",
        "name": "Corporate Modern",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                _rect(0, 600, 1000, 100, "#0f172a"),
                {"type":"rect", "left":850, "top":0, "width":150, "height":700, "fill":"#f1f5f9"},
                
                {**TITLE_STYLE, "text": "Attestation of Completion", "left":100, "textAlign":"left", "originX":"left", "top":80, "fontSize":40, "fill":"#1e293b"},
                
                {"type":"i-text", "text":"This certifies that", "left":100, "top":200, "fontSize":18, "fill":"#64748b"},
                {**NAME_STYLE, "text": "{{name}}", "left":100, "top":240, "textAlign":"left", "originX":"left", "fill":"#0284c7"},
                
                {"type":"i-text", "text":"completed the training module:", "left":100, "top":340, "fontSize":18, "fill":"#64748b"},
                {**COURSE_STYLE, "text": "{{course}}", "left":100, "top":380, "textAlign":"left", "originX":"left", "fill":"#0f172a"},
                
                {"type":"i-text", "text":"Issued on {{date}}", "left":100, "top":640, "fontSize":16, "fill":"#e2e8f0"},
                {"type":"i-text", "text":"{{organization}}", "left":800, "top":640, "fontSize":16, "fill":"#e2e8f0", "originX":"right", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "participation_stamp",
        "name": "Participation Badge",
        "category": "participation",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#fdfbf7",
            "objects": [
                {"type":"circle", "radius":300, "left":500, "top":350, "originX":"center", "originY":"center", "fill":"transparent", "stroke":"#d1d5db", "strokeWidth":2},
                {"type":"circle", "radius":280, "left":500, "top":350, "originX":"center", "originY":"center", "fill":"transparent", "stroke":"#10b981", "strokeWidth":10, "opacity":0.1},
                
                {**TITLE_STYLE, "text": "CERTIFICATE OF PARTICIPATION", "fill":"#065f46", "fontSize":36, "top":120},
                
                {"type":"i-text", "text":"Awarded to", "left":500, "originX":"center", "top":220, "fontSize":20, "fill":"#6b7280"},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#111827", "top":260, "fontSize":52},
                
                {"type":"i-text", "text":"For active participation in the", "left":500, "originX":"center", "top":370, "fontSize":20, "fill":"#6b7280"},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#065f46", "top":410, "fontWeight":"bold", "fontSize":36},
                
                {"type":"i-text", "text":"Date: {{date}}", "left":500, "originX":"center", "top":550, "fontSize":16, "fill":"#4b5563"},
                {"type":"i-text", "text":"{{organization}}", "left":500, "originX":"center", "top":580, "fontSize":18, "fill":"#111827", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "creative_waves",
        "name": "Creative Waves",
        "category": "custom",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#f4f4f5",
            "objects": [
                {"type":"circle", "radius":250, "left":0, "top":0, "originX":"center", "originY":"center", "fill":"#8b5cf6", "opacity":0.1},
                {"type":"circle", "radius":350, "left":1000, "top":700, "originX":"center", "originY":"center", "fill":"#ec4899", "opacity":0.1},
                
                {**TITLE_STYLE, "text": "Achievement Unlocked", "fill":"#6d28d9", "fontSize":48, "top":140},
                
                {**NAME_STYLE, "text": "{{name}}", "fill":"#111827", "top":260},
                
                {"type":"i-text", "text":"Has successfully mastered", "left":500, "originX":"center", "top":380, "fontSize":20, "fill":"#71717a"},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#be185d", "top":420, "fontWeight":"bold"},
                
                _line(250, 560, 750, 560, "#d4d4d8", 1),
                {"type":"i-text", "text":"{{date}}  •  {{organization}}", "left":500, "originX":"center", "top":580, "fontSize":16, "fill":"#52525b"},
            ]
        }
    },
    {
        "id": "tech_bootcamp",
        "name": "Tech Bootcamp",
        "category": "completion",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#000000",
            "objects": [
                _rect(20, 20, 960, 660, "transparent"),
                {"type":"rect", "left":20, "top":20, "width":960, "height":660, "fill":"transparent", "stroke":"#22c55e", "strokeWidth":2},
                
                {"type":"i-text", "text":"// CERTIFICATE_OF_COMPLETION", "left":60, "originX":"left", "top":80, "fontSize":24, "fill":"#22c55e", "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text":"{", "left":60, "originX":"left", "top":160, "fontSize":32, "fill":"#4b5563", "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text":"\"student\":", "left":100, "originX":"left", "top":220, "fontSize":24, "fill":"#93c5fd", "fontFamily":"Courier New, monospace"},
                {"type":"i-text", "text":"\"{{name}}\",", "left":260, "originX":"left", "top":220, "fontSize":32, "fill":"#f8fafc", "fontWeight":"bold", "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text":"\"program\":", "left":100, "originX":"left", "top":320, "fontSize":24, "fill":"#93c5fd", "fontFamily":"Courier New, monospace"},
                {"type":"i-text", "text":"\"{{course}}\",", "left":260, "originX":"left", "top":320, "fontSize":28, "fill":"#fcd34d", "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text":"\"date\":    \"{{date}}\",", "left":100, "originX":"left", "top":420, "fontSize":24, "fill":"#93c5fd", "fontFamily":"Courier New, monospace"},
                {"type":"i-text", "text":"\"issuer\":  \"{{organization}}\"", "left":100, "originX":"left", "top":480, "fontSize":24, "fill":"#93c5fd", "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text":"}", "left":60, "originX":"left", "top":560, "fontSize":32, "fill":"#4b5563", "fontFamily":"Courier New, monospace"},
            ]
        }
    },
    {
        "id": "classic_green",
        "name": "Classic Green",
        "category": "academic",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                {"type":"rect", "left":0, "top":0, "width":1000, "height":700, "fill":"transparent", "stroke":"#14532d", "strokeWidth":30},
                {"type":"rect", "left":40, "top":40, "width":920, "height":620, "fill":"transparent", "stroke":"#86efac", "strokeWidth":2},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":500, "originX":"center", "top":100, "fontSize":60, "fill":"#14532d", "fontWeight":"bold"},
                {"type":"i-text", "text": "OF ACHIEVEMENT", "left":500, "originX":"center", "top":170, "fontSize":20, "fill":"#166534", "letterSpacing": 200},
                
                {"type":"i-text", "text":"PROUDLY PRESENTED TO", "left":500, "originX":"center", "top":280, "fontSize":14, "fill":"#4b5563", "letterSpacing": 100},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#000000", "top":320, "fontSize":52},
                
                {"type":"i-text", "text":"For excellent performance and completion of", "left":500, "originX":"center", "top":420, "fontSize":16, "fill":"#4b5563"},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#14532d", "top":460, "fontSize":28, "fontWeight":"bold"},
                
                _line(200, 600, 450, 600, "#14532d", 2),
                {"type":"i-text", "text":"{{date}}", "left":325, "originX":"center", "top":610, "fontSize":14, "fill":"#14532d"},
                
                _line(550, 600, 800, 600, "#14532d", 2),
                {"type":"i-text", "text":"{{organization}}", "left":675, "originX":"center", "top":610, "fontSize":14, "fill":"#14532d"},
            ]
        }
    },
    {
        "id": "dark_elegant",
        "name": "Dark Elegant",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#1e1e1e",
            "objects": [
                _rect(50, 50, 900, 600, "transparent"),
                {"type":"rect", "left":50, "top":50, "width":900, "height":600, "fill":"transparent", "stroke":"#ffffff", "strokeWidth":1, "opacity":0.2},
                
                {"type":"i-text", "text": "{{organization}}", "left":500, "originX":"center", "top":100, "fontSize":20, "fill":"#a1a1aa", "letterSpacing": 200},
                
                {"type":"i-text", "text": "CERTIFICATE OF COMPLETION", "left":500, "originX":"center", "top":160, "fontSize":40, "fill":"#ffffff", "fontWeight":"bold"},
                
                {"type":"i-text", "text":"THIS ACKNOWLEDGES THAT", "left":500, "originX":"center", "top":260, "fontSize":14, "fill":"#a1a1aa", "letterSpacing": 150},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#ffffff", "top":300, "fontSize":48},
                
                {"type":"i-text", "text":"HAS COMPLETED", "left":500, "originX":"center", "top":400, "fontSize":14, "fill":"#a1a1aa", "letterSpacing": 150},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#e4e4e7", "top":440, "fontSize":32},
                
                {"type":"i-text", "text":"DATE: {{date}}", "left":500, "originX":"center", "top":550, "fontSize":14, "fill":"#a1a1aa", "letterSpacing": 100},
            ]
        }
    },
    {
        "id": "bold_statement",
        "name": "Bold Statement",
        "category": "achievement",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#be123c",
            "objects": [
                _rect(0, 0, 300, 700, "#9f1239"),
                
                {"type":"i-text", "text": "AWARD", "left":150, "originX":"center", "top":300, "fontSize":60, "fill":"#ffffff", "fontWeight":"900", "angle": -90},
                
                {"type":"i-text", "text": "PRESENTED TO", "left":350, "originX":"left", "top":100, "fontSize":24, "fill":"#fecdd3", "fontWeight":"bold"},
                {**NAME_STYLE, "text": "{{name}}", "left":350, "originX":"left", "top":150, "fill":"#ffffff", "fontSize":64},
                
                {"type":"i-text", "text": "FOR OUTSTANDING ACHIEVEMENT IN", "left":350, "originX":"left", "top":350, "fontSize":18, "fill":"#fecdd3", "fontWeight":"bold"},
                {**COURSE_STYLE, "text": "{{course}}", "left":350, "originX":"left", "top":400, "fill":"#ffffff", "fontSize":40, "fontWeight":"bold"},
                
                {"type":"i-text", "text": "DATE: {{date}}", "left":350, "originX":"left", "top":600, "fontSize":18, "fill":"#fecdd3", "fontWeight":"bold"},
                {"type":"i-text", "text": "{{organization}}", "left":900, "originX":"right", "top":600, "fontSize":18, "fill":"#fecdd3", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "pro_emerald_gold",
        "name": "Emerald & Gold Prestige",
        "category": "achievement",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#f8fafc",
            "objects": [
                _rect(0, 0, 1000, 700, "#064e3b"), # Deep emerald background
                {"type":"rect", "left":40, "top":40, "width":920, "height":620, "fill":"transparent", "stroke":"#fbbf24", "strokeWidth":4},
                {"type":"rect", "left":50, "top":50, "width":900, "height":600, "fill":"transparent", "stroke":"#fcd34d", "strokeWidth":1, "opacity":0.5},
                
                # Corner geometry (gold triangles via rotated rects hidden mostly out of bounds)
                {"type":"rect", "left":0, "top":0, "width":150, "height":150, "fill":"#fbbf24", "angle":45, "originX":"center", "originY":"center"},
                {"type":"rect", "left":1000, "top":700, "width":150, "height":150, "fill":"#fbbf24", "angle":45, "originX":"center", "originY":"center"},

                {"type":"i-text", "text": "CERTIFICATE", "left":500, "originX":"center", "top":120, "fontSize":48, "fill":"#fbbf24", "fontWeight":"bold", "letterSpacing": 200},
                {"type":"i-text", "text": "OF EXCELLENCE", "left":500, "originX":"center", "top":180, "fontSize":24, "fill":"#fef3c7", "letterSpacing": 400},
                
                _line(400, 240, 600, 240, "#fbbf24", 2),
                
                {"type":"i-text", "text": "PROUDLY PRESENTED TO", "left":500, "originX":"center", "top":280, "fontSize":14, "fill":"#94a3b8", "letterSpacing": 150},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#ffffff", "top":320, "fontSize":64, "fontFamily":"Georgia, serif"},
                
                {"type":"i-text", "text": "IN RECOGNITION OF EXCEPTIONAL PERFORMANCE IN", "left":500, "originX":"center", "top":420, "fontSize":12, "fill":"#94a3b8", "letterSpacing": 100},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#fbbf24", "top":460, "fontSize":32, "fontFamily":"Georgia, serif"},
                
                _line(250, 600, 450, 600, "#fbbf24", 1),
                {"type":"i-text", "text": "DATE: {{date}}", "left":350, "originX":"center", "top":615, "fontSize":12, "fill":"#fef3c7", "letterSpacing": 100},
                
                _line(550, 600, 750, 600, "#fbbf24", 1),
                {"type":"i-text", "text": "{{organization}}", "left":650, "originX":"center", "top":615, "fontSize":14, "fill":"#ffffff", "fontWeight":"bold", "letterSpacing": 100},
            ]
        }
    },
    {
        "id": "pro_cyber_neon",
        "name": "Cyber Neon Tech",
        "category": "completion",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#09090b",
            "objects": [
                # Abstract grid / background elements
                {"type":"rect", "left":100, "top":0, "width":2, "height":700, "fill":"#27272a"},
                {"type":"rect", "left":300, "top":0, "width":2, "height":700, "fill":"#27272a"},
                {"type":"rect", "left":500, "top":0, "width":2, "height":700, "fill":"#27272a"},
                {"type":"rect", "left":700, "top":0, "width":2, "height":700, "fill":"#27272a"},
                {"type":"rect", "left":900, "top":0, "width":2, "height":700, "fill":"#27272a"},
                
                # Neon accents
                {"type":"circle", "radius":300, "left":0, "top":700, "originX":"center", "originY":"center", "fill":"#8b5cf6", "opacity":0.15},
                {"type":"circle", "radius":400, "left":1000, "top":0, "originX":"center", "originY":"center", "fill":"#06b6d4", "opacity":0.15},
                
                {"type":"rect", "left":50, "top":50, "width":900, "height":600, "fill":"transparent", "stroke":"#06b6d4", "strokeWidth":2, "opacity":0.5},
                
                {"type":"i-text", "text": "// CERTIFICATE_ACQUIRED", "left":100, "originX":"left", "top":100, "fontSize":24, "fill":"#06b6d4", "fontFamily":"Courier New, monospace", "fontWeight":"bold"},
                
                {"type":"i-text", "text": "USER:", "left":100, "originX":"left", "top":200, "fontSize":18, "fill":"#a1a1aa", "fontFamily":"Courier New, monospace"},
                {**NAME_STYLE, "text": "{{name}}", "left":100, "originX":"left", "top":230, "fill":"#ffffff", "fontSize":56, "fontFamily":"Courier New, monospace"},
                
                {"type":"i-text", "text": "MODULE_DECRYPTED:", "left":100, "originX":"left", "top":350, "fontSize":18, "fill":"#8b5cf6", "fontFamily":"Courier New, monospace"},
                {**COURSE_STYLE, "text": "{{course}}", "left":100, "originX":"left", "top":390, "fill":"#e4e4e7", "fontSize":36, "fontFamily":"Courier New, monospace"},
                
                {"type":"rect", "left":100, "top":580, "width":200, "height":40, "fill":"#06b6d4", "opacity":0.2},
                {"type":"i-text", "text": "TS: {{date}}", "left":110, "originX":"left", "top":590, "fontSize":16, "fill":"#06b6d4", "fontFamily":"Courier New, monospace"},
                
                {"type":"rect", "left":650, "top":580, "width":250, "height":40, "fill":"#8b5cf6", "opacity":0.2},
                {"type":"i-text", "text": "SYS: {{organization}}", "left":660, "originX":"left", "top":590, "fontSize":16, "fill":"#c4b5fd", "fontFamily":"Courier New, monospace", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "pro_rose_gold",
        "name": "Luxury Rose Gold",
        "category": "custom",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#fafaf9",
            "objects": [
                # Big soft background geometry
                {"type":"circle", "radius":400, "left":0, "top":0, "originX":"center", "originY":"center", "fill":"#fda4af", "opacity":0.05},
                {"type":"circle", "radius":250, "left":1000, "top":700, "originX":"center", "originY":"center", "fill":"#be123c", "opacity":0.05},
                
                {"type":"rect", "left":40, "top":40, "width":920, "height":620, "fill":"transparent", "stroke":"#e11d48", "strokeWidth":1, "opacity":0.3},
                {"type":"rect", "left":50, "top":50, "width":900, "height":600, "fill":"transparent", "stroke":"#fda4af", "strokeWidth":3, "opacity":0.8},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":500, "originX":"center", "top":130, "fontSize":52, "fill":"#881337", "fontFamily":"Georgia, serif", "letterSpacing": 100},
                {"type":"i-text", "text": "OF APPRECIATION", "left":500, "originX":"center", "top":190, "fontSize":20, "fill":"#be123c", "letterSpacing": 300},
                
                {"type":"i-text", "text": "PROUDLY GRANTED TO", "left":500, "originX":"center", "top":280, "fontSize":12, "fill":"#a8a29e", "letterSpacing": 200},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#4c0519", "top":320, "fontSize":56, "fontFamily":"Georgia, serif"},
                
                {"type":"i-text", "text": "FOR DEDICATED INVOLVEMENT IN", "left":500, "originX":"center", "top":420, "fontSize":12, "fill":"#a8a29e", "letterSpacing": 150},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#881337", "top":460, "fontSize":32, "fontFamily":"Georgia, serif", "fontWeight":"normal"},
                
                _line(250, 600, 400, 600, "#e11d48", 1),
                {"type":"i-text", "text": "{{date}}", "left":325, "originX":"center", "top":620, "fontSize":14, "fill":"#78716c"},
                {"type":"i-text", "text": "Date", "left":325, "originX":"center", "top":640, "fontSize":10, "fill":"#a8a29e", "letterSpacing": 100},
                
                _line(600, 600, 750, 600, "#e11d48", 1),
                {"type":"i-text", "text": "{{organization}}", "left":675, "originX":"center", "top":620, "fontSize":14, "fill":"#4c0519", "fontWeight":"bold"},
                {"type":"i-text", "text": "Organization", "left":675, "originX":"center", "top":640, "fontSize":10, "fill":"#a8a29e", "letterSpacing": 100},
            ]
        }
    },
    {
        "id": "pro_modern_swiss",
        "name": "Swiss Typography",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                {"type":"rect", "left":50, "top":50, "width":900, "height":600, "fill":"#f4f4f5"},
                
                {"type":"rect", "left":50, "top":50, "width":20, "height":200, "fill":"#ef4444"},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":120, "originX":"left", "top":120, "fontSize":72, "fill":"#18181b", "fontWeight":"900", "fontFamily":"Helvetica, Arial"},
                {"type":"i-text", "text": "THIS DOCUMENT CERTIFIES THAT", "left":120, "originX":"left", "top":280, "fontSize":14, "fill":"#71717a", "fontWeight":"bold", "letterSpacing": 150},
                
                {**NAME_STYLE, "text": "{{name}}", "left":120, "originX":"left", "top":320, "fill":"#18181b", "fontSize":64, "fontWeight":"900", "fontFamily":"Helvetica, Arial"},
                
                {"type":"i-text", "text": "HAS SUCCESSFULLY COMPLETED", "left":120, "originX":"left", "top":430, "fontSize":14, "fill":"#71717a", "fontWeight":"bold", "letterSpacing": 150},
                {**COURSE_STYLE, "text": "{{course}}", "left":120, "originX":"left", "top":470, "fill":"#ef4444", "fontSize":36, "fontWeight":"900", "fontFamily":"Helvetica, Arial"},
                
                {"type":"i-text", "text": "DATE: {{date}}", "left":120, "originX":"left", "top":580, "fontSize":14, "fill":"#18181b", "fontWeight":"bold", "letterSpacing": 50},
                {"type":"i-text", "text": "ISSUED BY: {{organization}}", "left":910, "originX":"right", "top":580, "fontSize":14, "fill":"#18181b", "fontWeight":"bold", "letterSpacing": 50},
            ]
        }
    },
    {
        "id": "pro_abstract_geo",
        "name": "Abstract Geometric",
        "category": "participation",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                # Creative overlapped geometry
                {"type":"circle", "radius":200, "left":100, "top":-100, "fill":"#fde047", "opacity":0.8},
                {"type":"rect", "left":150, "top":100, "width":150, "height":150, "fill":"#3b82f6", "angle":45, "opacity":0.9},
                {"type":"circle", "radius":150, "left":850, "top":550, "fill":"#ef4444", "opacity":0.8},
                {"type":"rect", "left":800, "top":400, "width":100, "height":100, "fill":"#10b981", "angle":45, "opacity":0.9},
                
                {"type":"rect", "left":40, "top":40, "width":920, "height":620, "fill":"transparent", "stroke":"#111827", "strokeWidth":4},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":500, "originX":"center", "top":150, "fontSize":64, "fill":"#111827", "fontWeight":"900"},
                {"type":"i-text", "text": "OF PARTICIPATION", "left":500, "originX":"center", "top":230, "fontSize":24, "fill":"#6b7280", "letterSpacing": 300},
                
                {**NAME_STYLE, "text": "{{name}}", "fill":"#111827", "top":330, "fontSize":56},
                
                _line(350, 420, 650, 420, "#e5e7eb", 2),
                
                {"type":"i-text", "text": "For contributing to", "left":500, "originX":"center", "top":450, "fontSize":18, "fill":"#6b7280"},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#3b82f6", "top":490, "fontSize":32, "fontWeight":"bold"},
                
                {"type":"i-text", "text": "{{date}}", "left":200, "originX":"center", "top":600, "fontSize":18, "fill":"#111827", "fontWeight":"bold"},
                {"type":"i-text", "text": "{{organization}}", "left":800, "originX":"center", "top":600, "fontSize":18, "fill":"#111827", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "pro_navy_gold_ribbon",
        "name": "Navy Gold Ribbon",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#ffffff",
            "objects": [
                {"type":"rect", "left":0, "top":0, "width":300, "height":700, "fill":"#1e3a8a"},
                {"type":"rect", "left":280, "top":0, "width":20, "height":700, "fill":"#fbbf24"}, # Gold ribbon
                
                # Vertical text on the ribbon
                {"type":"i-text", "text": "CERTIFICATE OF EXCELLENCE", "left":150, "originX":"center", "top":350, "fontSize":24, "fill":"#ffffff", "fontWeight":"bold", "angle":-90, "letterSpacing": 200},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":400, "originX":"left", "top":100, "fontSize":64, "fill":"#1e3a8a", "fontWeight":"bold"},
                {"type":"i-text", "text": "OF COMPLETION", "left":400, "originX":"left", "top":180, "fontSize":24, "fill":"#94a3b8", "letterSpacing": 200},
                
                {"type":"i-text", "text": "AWARDED TO", "left":400, "originX":"left", "top":300, "fontSize":14, "fill":"#fbbf24", "fontWeight":"bold", "letterSpacing": 100},
                {**NAME_STYLE, "text": "{{name}}", "left":400, "originX":"left", "top":340, "fill":"#1e3a8a", "fontSize":52},
                
                {"type":"i-text", "text": "FOR OUTSTANDING MASTERY OF", "left":400, "originX":"left", "top":440, "fontSize":14, "fill":"#94a3b8", "fontWeight":"bold", "letterSpacing": 100},
                {**COURSE_STYLE, "text": "{{course}}", "left":400, "originX":"left", "top":480, "fill":"#1e3a8a", "fontSize":28, "fontWeight":"bold"},
                
                _line(400, 600, 600, 600, "#cbd5e1", 1),
                {"type":"i-text", "text": "{{date}}", "left":400, "originX":"left", "top":620, "fontSize":14, "fill":"#64748b"},
                
                _line(700, 600, 900, 600, "#cbd5e1", 1),
                {"type":"i-text", "text": "{{organization}}", "left":700, "originX":"left", "top":620, "fontSize":14, "fill":"#1e3a8a", "fontWeight":"bold"},
            ]
        }
    },
    {
        "id": "pro_black_platinum",
        "name": "Black & Platinum",
        "category": "professional",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#000000",
            "objects": [
                {"type":"rect", "left":20, "top":20, "width":960, "height":660, "fill":"transparent", "stroke":"#e5e7eb", "strokeWidth":1, "opacity":0.3},
                {"type":"rect", "left":25, "top":25, "width":950, "height":650, "fill":"transparent", "stroke":"#9ca3af", "strokeWidth":3},
                
                {"type":"i-text", "text": "C E R T I F I C A T E", "left":500, "originX":"center", "top":120, "fontSize":48, "fill":"#f3f4f6", "fontWeight":"300", "letterSpacing": 400},
                {"type":"i-text", "text": "O F   R E C O G N I T I O N", "left":500, "originX":"center", "top":180, "fontSize":16, "fill":"#9ca3af", "fontWeight":"bold", "letterSpacing": 600},
                
                {"type":"i-text", "text": "HONORABLY PRESENTED TO", "left":500, "originX":"center", "top":280, "fontSize":12, "fill":"#6b7280", "letterSpacing": 200},
                {**NAME_STYLE, "text": "{{name}}", "fill":"#ffffff", "top":320, "fontSize":56, "fontFamily":"Georgia, serif", "fontWeight":"normal"},
                
                {"type":"i-text", "text": "IN APPRECIATION OF", "left":500, "originX":"center", "top":420, "fontSize":12, "fill":"#6b7280", "letterSpacing": 200},
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#d1d5db", "top":460, "fontSize":28, "fontWeight":"300"},
                
                _line(300, 600, 700, 600, "#4b5563", 1),
                {"type":"i-text", "text": "{{date}}   //   {{organization}}", "left":500, "originX":"center", "top":620, "fontSize":14, "fill":"#9ca3af", "letterSpacing": 100},
            ]
        }
    },
    {
        "id": "pro_startup_vibrant",
        "name": "Startup Vibrant Gradient",
        "category": "completion",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#fdf8f6",
            "objects": [
                {"type":"circle", "radius":400, "left":0, "top":700, "originX":"center", "originY":"center", "fill":"#f97316", "opacity":0.1},
                {"type":"circle", "radius":300, "left":1000, "top":0, "originX":"center", "originY":"center", "fill":"#ec4899", "opacity":0.1},
                {"type":"rect", "left":0, "top":0, "width":15, "height":700, "fill":"#f97316"},
                
                {"type":"i-text", "text": "CERTIFICATE", "left":100, "originX":"left", "top":120, "fontSize":72, "fill":"#431407", "fontWeight":"900"},
                {"type":"i-text", "text": "OF ACHIEVEMENT", "left":100, "originX":"left", "top":200, "fontSize":24, "fill":"#ea580c", "fontWeight":"bold", "letterSpacing": 200},
                
                {**NAME_STYLE, "text": "{{name}}", "left":100, "originX":"left", "top":300, "fill":"#111827", "fontSize":60},
                
                {"type":"i-text", "text": "Killed it at:", "left":100, "originX":"left", "top":420, "fontSize":20, "fill":"#9a3412"},
                {**COURSE_STYLE, "text": "{{course}}", "left":100, "originX":"left", "top":460, "fill":"#ea580c", "fontSize":36, "fontWeight":"bold"},
                
                {"type":"i-text", "text": "{{date}}", "left":100, "originX":"left", "top":600, "fontSize":18, "fill":"#431407", "fontWeight":"bold"},
                {"type":"i-text", "text": "{{organization}}", "left":300, "originX":"left", "top":600, "fontSize":18, "fill":"#431407"},
            ]
        }
    },
    {
        "id": "pro_classic_diploma",
        "name": "Traditional Diploma",
        "category": "academic",
        "canvas_json": {
            "version": "5.3.0",
            "background": "#fefce8",
            "objects": [
                {"type":"rect", "left":20, "top":20, "width":960, "height":660, "fill":"transparent", "stroke":"#1e3a8a", "strokeWidth":10},
                {"type":"rect", "left":32, "top":32, "width":936, "height":636, "fill":"transparent", "stroke":"#3b82f6", "strokeWidth":2, "opacity":0.5},
                {"type":"rect", "left":40, "top":40, "width":920, "height":620, "fill":"transparent", "stroke":"#1e3a8a", "strokeWidth":1},
                
                {"type":"i-text", "text": "{{organization}}", "left":500, "originX":"center", "top":100, "fontSize":32, "fill":"#1e3a8a", "fontFamily":"Georgia, serif", "fontWeight":"bold"},
                {"type":"i-text", "text": "Upon the recommendation of the Faculty, has conferred upon", "left":500, "originX":"center", "top":180, "fontSize":16, "fill":"#334155", "fontFamily":"Georgia, serif", "fontStyle":"italic"},
                
                {**NAME_STYLE, "text": "{{name}}", "fill":"#1e40af", "top":260, "fontSize":64, "fontFamily":"Times New Roman, serif"},
                
                {"type":"i-text", "text": "the degree or certification of", "left":500, "originX":"center", "top":380, "fontSize":16, "fill":"#334155", "fontFamily":"Georgia, serif", "fontStyle":"italic"},
                
                {**COURSE_STYLE, "text": "{{course}}", "fill":"#1e3a8a", "top":440, "fontSize":40, "fontFamily":"Georgia, serif", "fontWeight":"bold"},
                
                {"type":"i-text", "text": "Given on this day, {{date}}", "left":500, "originX":"center", "top":520, "fontSize":18, "fill":"#1e3a8a", "fontFamily":"Georgia, serif"},
                
                _line(150, 620, 400, 620, "#1e3a8a", 2),
                {"type":"i-text", "text": "President", "left":275, "originX":"center", "top":630, "fontSize":14, "fill":"#1e3a8a", "fontFamily":"Georgia, serif", "fontStyle":"italic"},
                
                _line(600, 620, 850, 620, "#1e3a8a", 2),
                {"type":"i-text", "text": "Dean of Faculty", "left":725, "originX":"center", "top":630, "fontSize":14, "fill":"#1e3a8a", "fontFamily":"Georgia, serif", "fontStyle":"italic"},
            ]
        }
    }
]
