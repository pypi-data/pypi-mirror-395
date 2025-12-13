SCRIPT_MANAGEMENT_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>脚本管理系统</title>
    <style>
        :root {
            --primary-color: #00d4ff;
            --primary-hover: #00a8cc;
            --primary-glow: rgba(0, 212, 255, 0.5);
            --success-color: #10f981;
            --success-glow: rgba(16, 249, 129, 0.5);
            --danger-color: #ff4757;
            --danger-glow: rgba(255, 71, 87, 0.5);
            --warning-color: #ffa502;
            --warning-glow: rgba(255, 165, 2, 0.5);
            --bg-primary: #0a0e1a;
            --bg-secondary: #1a1f2e;
            --bg-card: rgba(26, 31, 46, 0.8);
            --bg-card-hover: rgba(26, 31, 46, 0.95);
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --text-muted: #718096;
            --border-color: rgba(255, 255, 255, 0.1);
            --border-radius: 12px;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
            --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
            min-height: 100vh;
            color: var(--text-primary);
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(16, 249, 129, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255, 165, 2, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }

        .container {
            // max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            text-align: center;
            animation: float 6s ease-in-out infinite;
        }

        .header h1 {
            color: var(--text-primary);
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 0 20px var(--primary-glow);
            background: linear-gradient(135deg, var(--primary-color), var(--success-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 20px;
        }

        .back-button {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-primary);
            text-decoration: none;
            border-radius: var(--border-radius);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .back-button:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: var(--primary-color);
            box-shadow: 0 0 10px var(--primary-glow);
            transform: translateY(-2px);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            box-shadow: var(--shadow), var(--shadow-glow);
            text-align: center;
            transition: all 0.3s ease;
            animation: float 6s ease-in-out infinite;
            animation-delay: calc(var(--index) * 0.5s);
        }

        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            border-color: var(--primary-color);
        }

        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 5px;
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }

        .scripts-panel, .actions-panel {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            animation: float 8s ease-in-out infinite;
        }

        .panel-header {
            background: rgba(0, 212, 255, 0.1);
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .panel-header h2 {
            color: var(--text-primary);
            font-size: 1.3rem;
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .panel-content {
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
        }

        .script-item {
            background: var(--bg-card);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid var(--primary-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .script-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }

        .script-item:hover::before {
            left: 100%;
        }

        .script-item:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            border-color: var(--primary-color);
        }

        .script-item.valid {
            border-left-color: var(--success-color);
            box-shadow: var(--shadow), var(--success-glow);
        }

        .script-item.invalid {
            border-left-color: var(--danger-color);
            box-shadow: var(--shadow), var(--danger-glow);
        }

        .script-item.warning {
            border-left-color: var(--warning-color);
            box-shadow: var(--shadow), var(--warning-glow);
        }

        .script-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .script-name {
            font-weight: 600;
            color: var(--text-primary);
            text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
        }

        .script-status {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            box-shadow: 0 0 5px currentColor;
        }

        .status-indicator.valid {
            background: var(--success-color);
        }

        .status-indicator.invalid {
            background: var(--danger-color);
        }

        .status-indicator.warning {
            background: var(--warning-color);
        }

        .script-details {
            font-size: 0.85rem;
            color: var(--text-secondary);
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .script-info {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .task-classes {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            margin-top: 5px;
        }

        .task-class-badge {
            background: var(--primary-color);
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
        }

        .script-actions {
            display: flex;
            gap: 8px;
            margin-top: 15px;
            flex-wrap: wrap;
            justify-content: space-between;
            position: relative;
            z-index: 1;
        }

        .btn {
            padding: 8px 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            min-width: 80px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
            color: white;
            border-color: var(--primary-color);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .btn-primary:hover {
            box-shadow: 0 5px 20px var(--primary-glow);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success-color), #0ea5e9);
            color: white;
            border-color: var(--success-color);
            box-shadow: 0 0 10px var(--success-glow);
        }

        .btn-success:hover {
            box-shadow: 0 5px 20px var(--success-glow);
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger-color), #dc2626);
            color: white;
            border-color: var(--danger-color);
            box-shadow: 0 0 10px var(--danger-glow);
        }

        .btn-danger:hover {
            box-shadow: 0 5px 20px var(--danger-glow);
        }

        .btn-warning {
            background: linear-gradient(135deg, var(--warning-color), #f97316);
            color: white;
            border-color: var(--warning-color);
            box-shadow: 0 0 10px var(--warning-glow);
        }

        .btn-warning:hover {
            box-shadow: 0 5px 20px var(--warning-glow);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-primary);
            border-color: var(--border-color);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: var(--primary-color);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .btn-full {
            width: 100%;
            margin-bottom: 15px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: var(--text-primary);
            text-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
        }

        .form-control {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: 1rem;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 15px var(--primary-glow);
            background: rgba(255, 255, 255, 0.1);
        }

        .form-control::placeholder {
            color: var(--text-muted);
        }

        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }

        .file-input-wrapper input[type=file] {
            position: absolute;
            left: -9999px;
        }

        .file-input-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 20px;
            border: 2px dashed var(--border-color);
            border-radius: var(--border-radius);
            background: rgba(255, 255, 255, 0.05);
            cursor: pointer;
            transition: all 0.3s ease;
            color: var(--text-secondary);
        }

        .file-input-label:hover {
            border-color: var(--primary-color);
            background: rgba(0, 212, 255, 0.1);
            color: var(--text-primary);
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 1000;
        }

        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 30px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            animation: modalSlideIn 0.3s ease-out;
        }

        .modal-header {
            margin-bottom: 20px;
        }

        .modal-header h3 {
            color: var(--text-primary);
            font-size: 1.5rem;
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 20px;
        }

        .validation-results {
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-top: 20px;
        }

        .validation-section {
            margin-bottom: 20px;
        }

        .validation-section h4 {
            color: var(--text-primary);
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .validation-item {
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 6px;
            font-size: 0.9rem;
        }

        .validation-item.error {
            background: rgba(255, 71, 87, 0.2);
            border-left: 3px solid var(--danger-color);
            color: #ff8a95;
        }

        .validation-item.warning {
            background: rgba(255, 165, 2, 0.2);
            border-left: 3px solid var(--warning-color);
            color: #ffcc70;
        }

        .validation-item.success {
            background: rgba(16, 249, 129, 0.2);
            border-left: 3px solid var(--success-color);
            color: #70ffaa;
        }

        .close {
            float: right;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-secondary);
            transition: all 0.3s ease;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            border: 1px solid var(--border-color);
        }

        .close:hover {
            color: var(--danger-color);
            background: rgba(255, 71, 87, 0.1);
            border-color: var(--danger-color);
            transform: scale(1.1);
            box-shadow: 0 0 10px var(--danger-glow);
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            opacity: 0.5;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        @keyframes modalSlideIn {
            from {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .main-content {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }

            .header {
                padding: 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .script-actions {
                flex-wrap: wrap;
                gap: 5px;
            }

            .btn {
                min-width: 70px;
                padding: 6px 10px;
                font-size: 0.8rem;
            }

            .modal-content {
                padding: 20px;
                max-width: 95%;
            }
        }

        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .script-details {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.5rem;
            }

            .panel-content {
                padding: 15px;
            }

            .script-item {
                padding: 12px;
            }
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid var(--border-color);
            border-radius: 50%;
            border-top-color: var(--primary-color);
            animation: spin 1s ease-in-out infinite;
            box-shadow: 0 0 10px var(--primary-glow);
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📜 脚本管理系统</h1>
            <p>管理和监控自定义Task脚本的Web界面</p>
            <a href="/" class="back-button">
                ← 返回任务管理
            </a>
        </div>

        <div class="stats-grid">
            <div class="stat-card" style="--index: 0;">
                <div class="stat-value" id="total-scripts">0</div>
                <div class="stat-label">总脚本数</div>
            </div>
            <div class="stat-card" style="--index: 1;">
                <div class="stat-value" id="valid-scripts">0</div>
                <div class="stat-label">有效脚本</div>
            </div>
            <div class="stat-card" style="--index: 2;">
                <div class="stat-value" id="task-classes">0</div>
                <div class="stat-label">Task类数量</div>
            </div>
            <div class="stat-card" style="--index: 3;">
                <div class="stat-value" id="security-issues">0</div>
                <div class="stat-label">安全问题</div>
            </div>
        </div>

        <div class="main-content">
            <div class="scripts-panel">
                <div class="panel-header">
                    <h2>📋 脚本列表</h2>
                </div>
                <div class="panel-content">
                    <div id="scripts-list">
                        <!-- 脚本列表将通过JavaScript动态加载 -->
                    </div>
                </div>
            </div>

            <div class="actions-panel">
                <div class="panel-header">
                    <h2>🛠️ 操作面板</h2>
                </div>
                <div class="panel-content">
                    <button class="btn btn-primary btn-full" onclick="showCreateScriptModal()">
                        ➕ 创建新脚本
                    </button>
                    <button class="btn btn-success btn-full" onclick="showUploadScriptModal()">
                        📁 上传脚本文件
                    </button>
                    <button class="btn btn-warning btn-full" onclick="reloadScripts()">
                        🔄 重新加载所有脚本
                    </button>
                    <button class="btn btn-secondary btn-full" onclick="refreshScriptsList()">
                        🔄 刷新列表
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- 创建脚本模态框 -->
    <div id="create-script-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('create-script-modal')">&times;</span>
                <h3>创建新脚本</h3>
            </div>
            <form id="create-script-form">
                <div class="form-group">
                    <label for="script-name">脚本名称:</label>
                    <input type="text" id="script-name" name="script_name" class="form-control" required placeholder="请输入脚本名称">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('create-script-modal')">取消</button>
                    <button type="submit" class="btn btn-primary">创建脚本</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 上传脚本模态框 -->
    <div id="upload-script-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('upload-script-modal')">&times;</span>
                <h3>上传脚本文件</h3>
            </div>
            <form id="upload-script-form">
                <div class="form-group">
                    <div class="file-input-wrapper">
                        <input type="file" id="script-file" name="script_file" accept=".py" required>
                        <label for="script-file" class="file-input-label">
                            <span>📁</span>
                            <span id="file-name">点击选择Python脚本文件 (.py)</span>
                        </label>
                    </div>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="force-install" name="force_install">
                        强制安装（覆盖已存在的文件）
                    </label>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('upload-script-modal')">取消</button>
                    <button type="submit" class="btn btn-primary">上传并安装</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 验证结果模态框 -->
    <div id="validation-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('validation-modal')">&times;</span>
                <h3>脚本验证结果</h3>
            </div>
            <div id="validation-content">
                <!-- 验证结果将在这里显示 -->
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal('validation-modal')">关闭</button>
            </div>
        </div>
    </div>

    <!-- 脚本预览模态框 -->
    <div id="script-preview-modal" class="modal">
        <div class="modal-content" style="max-width: 800px;">
            <div class="modal-header">
                <span class="close" onclick="closeModal('script-preview-modal')">&times;</span>
                <h3>📄 脚本预览 - <span id="preview-script-name"></span></h3>
            </div>
            <div class="modal-body">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="color: var(--text-primary); margin: 0;">脚本内容</h4>
                    <div style="display: flex; gap: 10px;">
                        <button id="preview-download-btn" class="btn btn-primary" style="padding: 6px 12px; font-size: 0.8rem;">
                            📥 下载脚本
                        </button>
                        <button class="btn btn-secondary" onclick="copyScriptContent()" style="padding: 6px 12px; font-size: 0.8rem;">
                            📋 复制内容
                        </button>
                    </div>
                </div>
                <div class="validation-results" style="background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--border-radius); padding: 15px; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.85rem; line-height: 1.5; max-height: 500px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;">
                    <div id="script-content-preview">加载脚本内容中...</div>
                </div>
                <div style="margin-top: 15px; padding: 15px; background: rgba(16, 249, 129, 0.1); border: 1px solid var(--success-color); border-radius: var(--border-radius);">
                    <h4 style="color: var(--success-color); margin-bottom: 10px;">💡 使用说明</h4>
                    <ol style="color: var(--text-secondary); margin-left: 20px;">
                        <li>脚本文件已自动下载到您的本地下载文件夹</li>
                        <li>请编辑脚本文件，实现您的自定义任务逻辑</li>
                        <li>编辑完成后，使用"上传脚本文件"功能安装脚本</li>
                        <li>安装成功后，可在任务管理页面创建基于此脚本的任务</li>
                    </ol>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal('script-preview-modal')">关闭</button>
            </div>
        </div>
    </div>

    <script>
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadScriptsList();

            // 绑定表单提交事件
            document.getElementById('create-script-form').addEventListener('submit', handleCreateScript);
            document.getElementById('upload-script-form').addEventListener('submit', handleUploadScript);

            // 绑定文件选择事件
            document.getElementById('script-file').addEventListener('change', function(e) {
                const fileName = e.target.files[0]?.name || '点击选择Python脚本文件 (.py)';
                document.getElementById('file-name').textContent = fileName;
            });
        });

        // 加载脚本列表
        async function loadScriptsList() {
            try {
                const response = await fetch('/scripts');
                const data = await response.json();

                updateStats(data);
                displayScripts(data.scripts || []);

            } catch (error) {
                console.error('加载脚本列表失败:', error);
                showNotification('加载脚本列表失败', 'error');
            }
        }

        // 更新统计信息
        function updateStats(data) {
            document.getElementById('total-scripts').textContent = data.total_count || 0;
            document.getElementById('valid-scripts').textContent = data.scripts?.filter(s => s.valid).length || 0;
            document.getElementById('task-classes').textContent = data.task_classes_count || 0;

            const totalSecurityIssues = data.scripts?.reduce((sum, script) => sum + (script.security_issues || 0), 0) || 0;
            document.getElementById('security-issues').textContent = totalSecurityIssues;
        }

        // 显示脚本列表
        function displayScripts(scripts) {
            const scriptsList = document.getElementById('scripts-list');

            if (!scripts || scripts.length === 0) {
                scriptsList.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <h3>暂无脚本</h3>
                        <p>点击"创建新脚本"或"上传脚本文件"开始使用</p>
                    </div>
                `;
                return;
            }

            scriptsList.innerHTML = '';
            scripts.forEach((script, index) => {
                const scriptElement = createScriptElement(script, index);
                scriptsList.appendChild(scriptElement);
            });
        }

        // 创建脚本元素
        function createScriptElement(script, index) {
            const div = document.createElement('div');

            // 确定脚本状态
            let statusClass = 'valid';
            let statusText = '有效';
            if (!script.valid) {
                statusClass = 'invalid';
                statusText = '无效';
            } else if (script.warnings.length > 0 || script.security_issues > 0) {
                statusClass = 'warning';
                statusText = '警告';
            }

            div.className = `script-item ${statusClass}`;
            div.style.cssText = `--index: ${index % 4}`;

            const taskClassesHtml = script.task_classes.length > 0
                ? `
                    <div class="task-classes">
                        ${script.task_classes.map(cls => `<span class="task-class-badge">${cls}</span>`).join('')}
                    </div>
                `
                : '';

            div.innerHTML = `
                <div class="script-header">
                    <span class="script-name">${script.name}</span>
                    <div class="script-status">
                        <span class="status-indicator ${statusClass}"></span>
                        <span>${statusText}</span>
                    </div>
                </div>
                <div class="script-details">
                    <span>大小: ${script.size} bytes</span>
                    <span>Task类: ${script.task_classes.length} 个</span>
                </div>
                <div class="script-info">
                    路径: ${script.path}
                </div>
                ${taskClassesHtml}
                ${script.errors.length > 0 ? `
                    <div class="script-info" style="color: var(--danger-color);">
                        错误: ${script.errors.join('; ')}
                    </div>
                ` : ''}
                ${script.warnings.length > 0 ? `
                    <div class="script-info" style="color: var(--warning-color);">
                        警告: ${script.warnings.join('; ')}
                    </div>
                ` : ''}
                ${script.security_issues > 0 ? `
                    <div class="script-info" style="color: var(--warning-color);">
                        安全问题: ${script.security_issues} 个
                    </div>
                ` : ''}
                <div class="script-actions">
                    <button class="btn btn-primary" onclick="validateScript('${script.name}')">验证</button>
                    <button class="btn btn-danger" onclick="deleteScript('${script.name}')">删除</button>
                </div>
            `;
            return div;
        }

        // 显示创建脚本模态框
        function showCreateScriptModal() {
            document.getElementById('create-script-modal').style.display = 'block';
        }

        // 显示上传脚本模态框
        function showUploadScriptModal() {
            document.getElementById('upload-script-modal').style.display = 'block';
        }

        // 关闭模态框
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // 处理创建脚本
        async function handleCreateScript(event) {
            event.preventDefault();

            const formData = new FormData(event.target);
            const scriptName = formData.get('script_name');

            try {
                const response = await fetch('/scripts/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ script_name: scriptName })
                });

                const result = await response.json();

                if (response.ok) {
                    showNotification(`脚本创建成功: ${result.script_name}`, 'success');
                    closeModal('create-script-modal');
                    event.target.reset();

                    // 自动下载脚本文件
                    if (result.download_ready && result.download_url) {
                        try {
                            // 创建下载链接
                            const downloadLink = document.createElement('a');
                            downloadLink.href = result.download_url;
                            downloadLink.download = result.script_name;
                            downloadLink.style.display = 'none';
                            document.body.appendChild(downloadLink);
                            downloadLink.click();
                            document.body.removeChild(downloadLink);

                            showNotification(`脚本已自动下载: ${result.script_name}`, 'info');
                        } catch (downloadError) {
                            console.warn('自动下载失败:', downloadError);
                            showNotification('脚本创建成功，但自动下载失败', 'warning');
                        }
                    }

                    // 显示脚本内容预览
                    if (result.content) {
                        showScriptPreview(result.script_name, result.content, result.download_url);
                    }

                    loadScriptsList();
                } else {
                    showNotification(`创建失败: ${result.detail}`, 'error');
                }
            } catch (error) {
                console.error('创建脚本失败:', error);
                showNotification('创建脚本失败', 'error');
            }
        }

        // 处理上传脚本
        async function handleUploadScript(event) {
            event.preventDefault();

            const formData = new FormData(event.target);
            const fileInput = document.getElementById('script-file');

            if (!fileInput.files[0]) {
                showNotification('请选择要上传的文件', 'error');
                return;
            }

            const uploadFormData = new FormData();
            uploadFormData.append('script_file', fileInput.files[0]);
            uploadFormData.append('force_install', formData.get('force_install') === 'on');

            try {
                const response = await fetch('/scripts/install', {
                    method: 'POST',
                    body: uploadFormData
                });

                const result = await response.json();

                if (response.ok) {
                    showNotification(`脚本上传成功: ${result.message}`, 'success');

                    // 显示验证结果
                    if (result.validation_result) {
                        showValidationResult(result.validation_result);
                    }

                    closeModal('upload-script-modal');
                    event.target.reset();
                    loadScriptsList();
                } else {
                    showNotification(`上传失败: ${result.detail}`, 'error');
                }
            } catch (error) {
                console.error('上传脚本失败:', error);
                showNotification('上传脚本失败', 'error');
            }
        }

        // 验证脚本
        async function validateScript(scriptName) {
            try {
                const response = await fetch('/scripts/validate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ script_name: scriptName })
                });

                const result = await response.json();

                if (response.ok) {
                    showValidationResult(result.validation_result);
                } else {
                    showNotification(`验证失败: ${result.detail}`, 'error');
                }
            } catch (error) {
                console.error('验证脚本失败:', error);
                showNotification('验证脚本失败', 'error');
            }
        }

        // 显示验证结果
        function showValidationResult(validationResult) {
            const validationContent = document.getElementById('validation-content');

            let html = `
                <div class="validation-results">
                    <div class="validation-section">
                        <h4>总体状态: ${validationResult.valid ? '✅ 有效' : '❌ 无效'}</h4>
                    </div>
            `;

            if (validationResult.task_classes.length > 0) {
                html += `
                    <div class="validation-section">
                        <h4>发现的Task类:</h4>
                        ${validationResult.task_classes.map(cls => `<div class="validation-item success">${cls}</div>`).join('')}
                    </div>
                `;
            }

            if (validationResult.errors.length > 0) {
                html += `
                    <div class="validation-section">
                        <h4>错误:</h4>
                        ${validationResult.errors.map(error => `<div class="validation-item error">${error}</div>`).join('')}
                    </div>
                `;
            }

            if (validationResult.warnings.length > 0) {
                html += `
                    <div class="validation-section">
                        <h4>警告:</h4>
                        ${validationResult.warnings.map(warning => `<div class="validation-item warning">${warning}</div>`).join('')}
                    </div>
                `;
            }

            if (validationResult.security_issues.length > 0) {
                html += `
                    <div class="validation-section">
                        <h4>安全问题:</h4>
                        ${validationResult.security_issues.map(issue =>
                            `<div class="validation-item ${issue.severity === 'critical' ? 'error' : 'warning'}">${issue.message}</div>`
                        ).join('')}
                    </div>
                `;
            }

            html += '</div>';
            validationContent.innerHTML = html;
            document.getElementById('validation-modal').style.display = 'block';
        }

        // 删除脚本
        async function deleteScript(scriptName) {
            if (!confirm(`确定要删除脚本 "${scriptName}" 吗？此操作不可撤销。`)) {
                return;
            }

            try {
                const response = await fetch(`/scripts/${scriptName}`, {
                    method: 'DELETE'
                });

                const result = await response.json();

                if (response.ok) {
                    showNotification(`脚本删除成功: ${result.message}`, 'success');
                    loadScriptsList();
                } else {
                    showNotification(`删除失败: ${result.detail}`, 'error');
                }
            } catch (error) {
                console.error('删除脚本失败:', error);
                showNotification('删除脚本失败', 'error');
            }
        }

        // 重新加载脚本
        async function reloadScripts() {
            try {
                const response = await fetch('/scripts/reload', {
                    method: 'POST'
                });

                const result = await response.json();

                if (response.ok) {
                    showNotification(`脚本重新加载成功: ${result.message}`, 'success');
                    loadScriptsList();
                } else {
                    showNotification(`重新加载失败: ${result.detail}`, 'error');
                }
            } catch (error) {
                console.error('重新加载脚本失败:', error);
                showNotification('重新加载脚本失败', 'error');
            }
        }

        // 刷新脚本列表
        function refreshScriptsList() {
            loadScriptsList();
        }

        // 显示脚本预览
        function showScriptPreview(scriptName, scriptContent, downloadUrl) {
            document.getElementById('preview-script-name').textContent = scriptName;
            document.getElementById('script-content-preview').textContent = scriptContent;

            // 设置下载按钮
            const downloadBtn = document.getElementById('preview-download-btn');
            downloadBtn.onclick = function() {
                const downloadLink = document.createElement('a');
                downloadLink.href = downloadUrl;
                downloadLink.download = scriptName;
                downloadLink.style.display = 'none';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);

                showNotification(`脚本已下载: ${scriptName}`, 'info');
            };

            // 显示模态框
            document.getElementById('script-preview-modal').style.display = 'block';
        }

        // 复制脚本内容
        function copyScriptContent() {
            const content = document.getElementById('script-content-preview').textContent;

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(content).then(() => {
                    showNotification('脚本内容已复制到剪贴板', 'success');
                }).catch(err => {
                    console.error('复制失败:', err);
                    fallbackCopyText(content);
                });
            } else {
                fallbackCopyText(content);
            }
        }

        // 备用复制方法
        function fallbackCopyText(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand('copy');
                showNotification('脚本内容已复制到剪贴板', 'success');
            } catch (err) {
                console.error('复制失败:', err);
                showNotification('复制失败，请手动复制', 'error');
            }

            document.body.removeChild(textArea);
        }

        // 显示通知
        function showNotification(message, type) {
            // 创建通知元素
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: var(--border-radius);
                color: white;
                font-weight: 500;
                z-index: 9999;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: var(--shadow-lg);
            `;

            // 根据类型设置背景色
            const colors = {
                success: 'linear-gradient(135deg, var(--success-color), #0ea5e9)',
                error: 'linear-gradient(135deg, var(--danger-color), #dc2626)',
                warning: 'linear-gradient(135deg, var(--warning-color), #f97316)',
                info: 'linear-gradient(135deg, var(--primary-color), var(--primary-hover))'
            };

            const glowColors = {
                success: 'var(--success-glow)',
                error: 'var(--danger-glow)',
                warning: 'var(--warning-glow)',
                info: 'var(--primary-glow)'
            };

            notification.style.background = colors[type] || colors.info;
            notification.style.boxShadow = `var(--shadow-lg), 0 0 15px ${glowColors[type] || glowColors.info}`;
            notification.textContent = message;

            document.body.appendChild(notification);

            // 显示动画
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 100);

            // 3秒后自动消失
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (document.body.contains(notification)) {
                        document.body.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }

        // 点击模态框外部关闭
        window.onclick = function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""