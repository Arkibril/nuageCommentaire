
html_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur de Mockup Billboard</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --primary-hover: #1d4ed8;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-secondary: #64748b;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
            max-width: 800px;
        }

        h1 {
            font-size: 2.25rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.025em;
        }

        p.subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            line-height: 1.6;
        }

        .main-container {
            background-color: var(--card-bg);
            border-radius: 1rem;
            box-shadow: var(--shadow-lg);
            padding: 2rem;
            width: 100%;
            max-width: 1200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2rem;
        }

        .controls {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e2e8f0;
        }

        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            font-size: 1rem;
            box-shadow: var(--shadow-sm);
            text-decoration: none;
        }

        .btn:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background-color: #e2e8f0;
            color: #475569;
        }

        .btn-secondary:hover {
            background-color: #cbd5e1;
            color: #1e293b;
        }

        /* Hide the actual file input */
        input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }

        .canvas-container {
            position: relative;
            width: 100%;
            border-radius: 0.5rem;
            overflow: hidden;
            background-color: #f1f5f9;
            box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 200px;
        }

        canvas {
            max-width: 100%;
            height: auto;
            display: block;
            box-shadow: var(--shadow-md);
        }

        .loading-text {
            color: var(--text-secondary);
            font-size: 0.9rem;
            position: absolute;
        }

        /* Utility for hidden elements */
        .hidden {
            display: none !important;
        }

        @media (min-width: 768px) {
            .controls {
                flex-direction: row;
                justify-content: center;
            }

            body {
                padding: 3rem 1.5rem;
            }
        }
    </style>
</head>

<body>

    <header>
        <h1>Billboard Mockup Generator</h1>
        <p class="subtitle">Créez des mises en situation réalistes instantanément. Importez votre visuel, nous faisons le reste.</p>
    </header>

    <main class="main-container">

        <div class="controls">
            <div class="file-input-wrapper btn">
                <span>Télécharger votre image</span>
                <input type="file" id="uploadInput" accept="image/png, image/jpeg, image/jpg">
            </div>

            <button id="downloadBtn" class="btn btn-secondary hidden">
                ⬇Télécharger le résultat
            </button>
        </div>

        <div class="canvas-container">
            <canvas id="billboardCanvas"></canvas>
            <div id="loadingMessage" class="loading-text">Chargement du studio...</div>
        </div>

    </main>

    <script>
        // CONFIGURATION - ZONE D'EDITION
        const CONFIG = {
            // Placeholder for base64 injection
            backgroundImagePath: '{BASE64_IMAGE}',
            dropZone: {
                x: 22,
                y: 737,
                width: 1033,
                height: 514
            }
        };

        const canvas = document.getElementById('billboardCanvas');
        const ctx = canvas.getContext('2d');
        const uploadInput = document.getElementById('uploadInput');
        const downloadBtn = document.getElementById('downloadBtn');
        const loadingMessage = document.getElementById('loadingMessage');

        let bgImage = new Image();
        let userImage = null;

        // Init
        bgImage.onload = () => {
            canvas.width = bgImage.width;
            canvas.height = bgImage.height;
            drawCanvas();
            loadingMessage.classList.add('hidden');
        };
        bgImage.src = CONFIG.backgroundImagePath;

        // Draw function
        function drawCanvas() {
            // 1. Draw Background
            ctx.drawImage(bgImage, 0, 0);

            // 2. Draw User Image (if exists)
            if (userImage) {
                ctx.drawImage(
                    userImage, 
                    CONFIG.dropZone.x, 
                    CONFIG.dropZone.y, 
                    CONFIG.dropZone.width, 
                    CONFIG.dropZone.height
                );
                downloadBtn.classList.remove('hidden');
            }
        }

        // Handle File Upload
        uploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                userImage = new Image();
                userImage.onload = () => {
                    drawCanvas();
                };
                userImage.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });

        // Handle Download
        downloadBtn.addEventListener('click', () => {
            const link = document.createElement('a');
            link.download = 'billboard-mockup.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        });
    </script>
</body>
</html>"""

def restore():
    try:
        with open('bg_base64.txt', 'r') as f:
            base64_str = f.read().strip()
            # Ensure proper base64 prefix if missing
            if not base64_str.startswith('data:image'):
                if 'base64,' in base64_str:
                     pass # Assume it might be 'data:image/jpeg;base64,...' or similar
                else:
                     base64_str = 'data:image/png;base64,' + base64_str

        # Replace the placeholder in the template
        final_html = html_template.replace('{BASE64_IMAGE}', base64_str)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print("Successfully restored index.html with clean CSS and correct CONFIG.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore()
