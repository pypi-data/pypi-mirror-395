"""
HTML templates for the upserver web interface.
"""

from datetime import datetime


def get_upload_page_html():
    """
    Get the HTML content for the upload page.

    Returns:
        str: Complete HTML content for the upload interface
    """
    current_time = datetime.now().strftime("%H:%M:%S")

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Upload Resumable - Server with Listing</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📁</text></svg>">\
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
<div class="container">
    <h1>📤 Resumable Upload + List & Download</h1>
    <div class="server-status">
        🟢 SERVER ONLINE AND READY
    </div>
    <div class="console-log" id="consoleLog">
        <div>✅ Page loaded successfully</div>
        <div>⏰ {current_time}</div>
        <div>🔄 Waiting for file selection...</div>
    </div>
    <div class="features">
        <ul>
            <li>Accepts ANY type of file</li>
            <li>Supports ultra large files</li>
            <li>Automatically resumes if dropped</li>
            <li>Real-time speed</li>
            <li>Can pause and continue</li>
        </ul>
    </div>
    <div class="upload-box">
        <div class="emoji">☁️</div>
        <p style="margin-bottom: 10px; color:#666;font-size:16px;">Select any file</p>
        <input type="file" id="fileInput">
        <div id="fileInfo"></div>
    </div>
    <div class="list-controls">
        <button onclick="showFileList()">📂 Show files on server</button>
    </div>
    <div id="fileListBox" style="display:none;margin:20px 0;">
        <h3>Files on server</h3>
        <table id="fileTable" style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:#F0F1FF;">
                <th>Name</th><th>Size</th><th>Modified</th><th>Download</th>
            </tr></thead>
            <tbody></tbody>
        </table>
    </div>
    <div class="controls">
        <button id="uploadBtn" onclick="startUpload()" disabled>🚀 Start Upload</button>
        <button id="pauseBtn" class="btn-pause" onclick="pauseUpload()" style="display:none;">⏸️ Pause</button>
        <button id="resumeBtn" class="btn-resume" onclick="resumeUpload()" style="display:none;">▶️ Resume</button>
    </div>
    <div class="progress-container" id="progressContainer">
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill">0%</div>
        </div>
        <div class="progress-info" id="progressInfo">
            <div><span class="progress-label">📤 Uploaded:</span><span class="progress-value" id="uploadedSize">0 MB / 0 MB</span></div>
            <div><span class="progress-label">⚡ Speed:</span><span class="speed" id="uploadSpeed">0 MB/s</span></div>
            <div><span class="progress-label">⏱️ Time remaining:</span><span class="progress-value" id="timeLeft">Calculating...</span></div>
            <div><span class="progress-label">📊 Chunks:</span><span class="progress-value" id="chunkProgress">0 / 0</span></div>
        </div>
    </div>
    <div style="margin-top: 20px;">
        <h3 style="color: #333; margin-bottom: 10px; font-size: 18px;">📋 Activity Log</h3>
        <div id="status"></div>
    </div>
</div>
<script>
{get_javascript_code()}
</script>
</body>
</html>
"""


def get_css_styles():
    """
    Get CSS styles for the upload page.

    Returns:
        str: CSS styles
    """
    return """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 28px;
        }
        .server-status {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid #28a745;
            color: #155724;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
            animation: pulse 2s infinite;
            font-size: 16px;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .console-log {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
        }
        .console-log div {
            margin: 2px 0;
        }
        .features {
            background: #f0f1ff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .features ul {
            list-style: none;
            padding-left: 0;
        }
        .features li {
            padding: 5px 0;
        }
        .features li:before {
            content: "✅ ";
        }
        .upload-box {
            border: 3px dashed #667eea;
            border-radius: 10px;
            padding: 40px 20px;
            text-align: center;
            background: #f8f9ff;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        .upload-box:hover {
            border-color: #764ba2;
            background: #f0f1ff;
        }
        input[type="file"] {
            margin: 20px 0;
            padding: 10px;
            width: 100%;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s;
            font-weight: bold;
            margin: 5px;
        }
        button:active {
            transform: scale(0.95);
        }
        button:hover {
            transform: scale(1.05);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .btn-pause {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .btn-resume {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .list-controls {
            text-align: center;
            margin: 20px 0;
        }
        .emoji {
            font-size: 48px;
            margin-bottom: 20px;
        }
        #status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            font-size: 14px;
            min-height: 100px;
            max-height: 300px;
            overflow-y: auto;
            display: block;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        .loading {
            background: #d1ecf1;
            color: #0c5460;
            border: 2px solid #bee5eb;
        }
        .warning {
            background: #fff3cd;
            color: #856404;
            border: 2px solid #ffeaa7;
        }
        .progress-container {
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .progress-bar {
            width: 100%;
            height: 40px;
            background: #e0e0e0;
            border-radius: 20px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .progress-info {
            margin-top: 15px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .progress-info div {
            padding: 8px 0;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #dee2e6;
        }
        .progress-info div:last-child {
            border-bottom: none;
        }
        .progress-label {
            color: #666;
        }
        .progress-value {
            font-weight: bold;
            color: #333;
        }
        .speed {
            font-weight: bold;
            color: #667eea;
            font-size: 18px;
        }
        #fileInfo {
            margin: 15px 0;
            padding: 15px;
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-radius: 10px;
            display: none;
            line-height: 1.6;
        }
        .controls {
            text-align: center;
            margin-top: 15px;
        }
        #fileTable td, #fileTable th {
            padding: 6px 5px;
            border-bottom: 1px solid #eee;
        }
        #fileTable th {
            background: #F0F1FF;
        }
    """


def get_javascript_code():
    """
    Get JavaScript code for the upload page.

    Returns:
        str: JavaScript code
    """
    return """
        let currentFile = null;
        let isPaused = false;
        let uploadStartTime = null;
        let totalUploaded = 0;
        let uploadSpeed = 0;
        let chunkSize = 5 * 1024 * 1024; // 5MB

        function addLog(message, color='#333') {
            console.log('AddLog called:', message);
            const status = document.getElementById('status');
            if (!status) {
                console.error('Status element not found!');
                return;
            }

            status.style.display = 'block';

            const div = document.createElement('div');
            div.style.color = color;
            div.style.margin = '3px 0';
            div.style.fontSize = '13px';
            div.style.fontFamily = 'Courier New, monospace';
            div.style.padding = '4px 8px';
            div.style.backgroundColor = 'rgba(255,255,255,0.8)';
            div.style.borderLeft = '3px solid ' + color;
            div.style.borderRadius = '3px';
            div.innerHTML = `[${new Date().toLocaleTimeString()}] ${message}`;
            status.appendChild(div);
            status.scrollTop = status.scrollHeight;

            while (status.children.length > 50) {
                status.removeChild(status.firstChild);
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            addLog('🚀 Upload system initialized', '#28a745');
            addLog('ℹ️ Select a file to enable upload', '#17a2b8');
        });

        document.getElementById('fileInput').addEventListener('change', function(e) {
            currentFile = e.target.files[0];
            if (currentFile) {
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileInfo').innerHTML = `
                    <p><strong>📁 File:</strong> ${currentFile.name}</p>
                    <p><strong>📏 Size:</strong> ${(currentFile.size / 1024 / 1024).toFixed(2)} MB</p>
                    <p><strong>📅 Type:</strong> ${currentFile.type || 'Unknown'}</p>
                `;
                addLog(`✅ File selected: ${currentFile.name} (${(currentFile.size / 1024 / 1024).toFixed(2)} MB)`, '#28a745');
            } else {
                addLog('⚠️ No file selected', '#ffc107');
            }
        });

        function showFileList() {
            addLog('🔄 Requesting file list from server...', '#007bff');
            const fileListBox = document.getElementById('fileListBox');

            fetch('/files')
                .then(response => {
                    addLog(`📡 Response received: Status ${response.status}`, '#6c757d');
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(files => {
                    addLog(`📋 Processing ${files.length} files...`, '#28a745');
                    let tbody = document.querySelector("#fileTable tbody");

                    if (files.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#666;padding:20px;">No files found on server</td></tr>';
                        addLog('📭 Empty directory - no files found', '#ffc107');
                    } else {
                        tbody.innerHTML = files.map(file => {
                            let sizeMB = (file.size/1024/1024).toFixed(2) + " MB";
                            let downBtn = `<a href="/download/${encodeURIComponent(file.name)}" style="color:#fff;background:#764ba2;padding:5px 15px;border-radius:10px;text-decoration:none;font-weight:bold;">⬇️ Download</a>`;
                            return `<tr>
                                <td>${file.name}</td>
                                <td>${sizeMB}</td>
                                <td>${file.modified}</td>
                                <td>${downBtn}</td>
                            </tr>`;
                        }).join('');
                        addLog(`✅ ${files.length} files listed successfully`, '#28a745');
                    }

                    fileListBox.style.display = "block";
                })
                .catch(error => {
                    addLog(`❌ Error listing files: ${error.message}`, '#dc3545');
                    console.error('Detailed error:', error);
                });
        }

        async function startUpload() {
            if (!currentFile) {
                addLog('❌ No file selected!', '#ff0000');
                return;
            }

            isPaused = false;
            uploadStartTime = Date.now();
            totalUploaded = 0;

            document.getElementById('uploadBtn').style.display = 'none';
            document.getElementById('pauseBtn').style.display = 'inline-block';
            document.getElementById('progressContainer').style.display = 'block';

            addLog(`🚀 Starting upload of ${currentFile.name}...`);

            const totalChunks = Math.ceil(currentFile.size / chunkSize);
            let uploadedChunks = 0;

            try {
                for (let i = 0; i < totalChunks; i++) {
                    if (isPaused) {
                        addLog('⏸️ Upload paused by user');
                        return;
                    }

                    const start = i * chunkSize;
                    const end = Math.min(start + chunkSize, currentFile.size);
                    const chunk = currentFile.slice(start, end);

                    const chunkStartTime = Date.now();

                    const formData = new FormData();
                    formData.append('chunk', chunk);
                    formData.append('filename', currentFile.name);
                    formData.append('chunkIndex', i);
                    formData.append('totalChunks', totalChunks);
                    formData.append('fileSize', currentFile.size);

                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }

                    uploadedChunks++;
                    totalUploaded += chunk.size;

                    const progress = (totalUploaded / currentFile.size) * 100;
                    document.getElementById('progressFill').style.width = progress + '%';
                    document.getElementById('progressFill').textContent = progress.toFixed(1) + '%';

                    const chunkTime = Date.now() - chunkStartTime;
                    const chunkSpeed = (chunk.size / 1024 / 1024) / (chunkTime / 1000);
                    uploadSpeed = chunkSpeed;

                    document.getElementById('uploadedSize').textContent = `${(totalUploaded / 1024 / 1024).toFixed(2)} MB / ${(currentFile.size / 1024 / 1024).toFixed(2)} MB`;
                    document.getElementById('uploadSpeed').textContent = `${uploadSpeed.toFixed(2)} MB/s`;
                    document.getElementById('chunkProgress').textContent = `${uploadedChunks} / ${totalChunks}`;

                    const remainingBytes = currentFile.size - totalUploaded;
                    const timeLeft = remainingBytes / (uploadSpeed * 1024 * 1024);
                    document.getElementById('timeLeft').textContent = timeLeft > 0 ? `${timeLeft.toFixed(0)}s` : 'Almost done!';

                    addLog(`📦 Chunk ${uploadedChunks}/${totalChunks} sent (${(chunk.size / 1024).toFixed(1)} KB) | ⚡ Processing: ${(chunkTime/1000).toFixed(3)}s`, '#17a2b8');
                }

                const totalTime = (Date.now() - uploadStartTime) / 1000;
                const minutes = Math.floor(totalTime / 60);
                const seconds = Math.floor(totalTime % 60);
                const timeDisplay = minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`;
                const avgSpeed = (currentFile.size / 1024 / 1024 / totalTime).toFixed(2);

                document.getElementById('timeLeft').textContent = `Completed in ${timeDisplay}`;
                document.getElementById('progressFill').textContent = '100% Complete!';
                document.getElementById('uploadSpeed').textContent = `${avgSpeed} MB/s (avg)`;

                addLog(`🎉 Upload completed successfully! File: ${currentFile.name}`, '#008000');
                addLog(`⏱️ Total time: ${timeDisplay} | Average speed: ${avgSpeed} MB/s`, '#28a745');
                addLog(`📊 Statistics: ${totalChunks} chunks sent | Size: ${(currentFile.size / 1024 / 1024).toFixed(2)} MB`, '#6f42c1');

                setTimeout(() => {
                    resetUploadUI();
                }, 3000);

            } catch (error) {
                addLog(`❌ Upload error: ${error.message}`, '#ff0000');
                resetUploadUI();
            }
        }

        function pauseUpload() {
            isPaused = true;
            document.getElementById('pauseBtn').style.display = 'none';
            document.getElementById('resumeBtn').style.display = 'inline-block';
            addLog('⏸️ Upload paused');
        }

        function resumeUpload() {
            document.getElementById('pauseBtn').style.display = 'inline-block';
            document.getElementById('resumeBtn').style.display = 'none';
            addLog('▶️ Resuming upload...');
            startUpload();
        }

        function resetUploadUI() {
            document.getElementById('uploadBtn').style.display = 'inline-block';
            document.getElementById('pauseBtn').style.display = 'none';
            document.getElementById('resumeBtn').style.display = 'none';
            document.getElementById('uploadBtn').disabled = currentFile ? false : true;
        }
    """
