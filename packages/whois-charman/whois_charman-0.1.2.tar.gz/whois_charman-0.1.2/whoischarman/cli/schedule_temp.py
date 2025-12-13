HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>调度管理系统</title>
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
            grid-template-columns: 1fr;
            gap: 30px;
        }

        .tasks-table-panel {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            animation: float 8s ease-in-out infinite;
        }

        .table-container {
            overflow-x: auto;
            border-radius: var(--border-radius);
        }

        .tasks-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            overflow: hidden;
        }

        .tasks-table thead {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 168, 204, 0.1));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .tasks-table thead th {
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.9rem;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
            text-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
        }

        .tasks-table tbody tr {
            transition: all 0.3s ease;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .tasks-table tbody tr:hover {
            background: rgba(0, 212, 255, 0.1);
            transform: scale(1.01);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .tasks-table tbody tr.running {
            background: rgba(16, 249, 129, 0.05);
        }

        .tasks-table tbody tr.running:hover {
            background: rgba(16, 249, 129, 0.15);
        }

        .tasks-table tbody tr.error {
            background: rgba(255, 71, 87, 0.05);
        }

        .tasks-table tbody tr.error:hover {
            background: rgba(255, 71, 87, 0.15);
        }

        .tasks-table tbody td {
            padding: 12px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        .tasks-table tbody td:last-child {
            border-right: none;
        }

        .status-cell {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .status-indicator.running {
            background: var(--success-color);
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 0 10px var(--success-glow);
        }

        .status-indicator.stopped {
            background: var(--text-muted);
        }

        .status-indicator.error {
            background: var(--danger-color);
            animation: pulse 1s ease-in-out infinite;
            box-shadow: 0 0 10px var(--danger-glow);
        }

        .task-name-cell {
            color: var(--text-primary);
            font-weight: 600;
            text-shadow: 0 0 3px rgba(0, 212, 255, 0.3);
        }

        .execution-count {
            font-weight: 500;
            color: var(--primary-color);
        }

        .error-count {
            font-weight: 500;
            color: var(--danger-color);
        }

        .interval-cell {
            color: var(--text-secondary);
        }

        .enabled-cell {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .enabled-cell.enabled {
            background: rgba(16, 249, 129, 0.2);
            color: var(--success-color);
            border: 1px solid var(--success-color);
        }

        .enabled-cell.disabled {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
        }

        .time-cell {
            color: var(--text-secondary);
            font-size: 0.85rem;
            white-space: nowrap;
        }

        .error-cell {
            color: var(--danger-color);
            font-size: 0.8rem;
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .actions-cell {
            display: flex;
            gap: 6px;
            justify-content: flex-start;
            flex-wrap: nowrap;
        }

        .btn-sm {
            padding: 4px 8px;
            font-size: 0.7rem;
            min-width: auto;
            border-radius: 4px;
            flex-shrink: 0;
            font-weight: 500;
        }

        .empty-state {
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            border: 2px dashed var(--border-color);
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

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            box-shadow: 0 0 5px currentColor;
            display: inline-block;
        }

        .status-indicator.running {
            background: var(--success-color);
            animation: pulse 2s ease-in-out infinite;
        }

        .status-indicator.stopped {
            background: var(--text-muted);
        }

        .status-indicator.error {
            background: var(--danger-color);
            animation: pulse 1s ease-in-out infinite;
        }

        /* 表格样式 */
        .tasks-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow), var(--shadow-glow);
        }

        .tasks-table th {
            background: rgba(0, 212, 255, 0.1);
            color: var(--text-primary);
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
            font-size: 0.85rem;
            text-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
        }

        .tasks-table td {
            padding: 8px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.8rem;
            vertical-align: middle;
        }

        .tasks-table tr {
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .tasks-table tbody tr:hover {
            background: rgba(0, 212, 255, 0.05);
            transform: scale(1.01);
        }

        .tasks-table tbody tr:last-child td {
            border-bottom: none;
        }

        /* 表格列宽设置 */
        .status-cell {
            width: 60px;
            text-align: center;
        }

        .task-name-cell {
            font-weight: 600;
            color: var(--text-primary);
            min-width: 120px;
        }

        .status-text-cell {
            min-width: 80px;
        }

        .execution-cell {
            text-align: center;
            min-width: 60px;
        }

        .error-cell {
            text-align: center;
            min-width: 60px;
        }

        .time-cell {
            min-width: 120px;
        }

        .log-file-cell {
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .actions-cell {
            width: 160px;
            text-align: right;
        }

        /* 任务状态样式 */
        .task-running {
            color: var(--success-color);
            font-weight: 500;
        }

        .task-stopped {
            color: var(--text-muted);
        }

        .task-error {
            color: var(--danger-color);
            font-weight: 500;
        }

        /* 表格内按钮样式 */
        .table-actions {
            display: flex;
            gap: 3px;
            justify-content: flex-end;
            align-items: center;
            flex-wrap: nowrap;
        }

        .btn-table {
            padding: 3px 6px;
            font-size: 0.7rem;
            min-width: 40px;
            white-space: nowrap;
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

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .btn:disabled:hover {
            transform: none;
            box-shadow: none;
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

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
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
            max-width: 500px;
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

        .logs-viewer {
            background: #1f2937;
            color: #f3f4f6;
            border-radius: var(--border-radius);
            padding: 20px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
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

        /* 响应式表格样式 */
        .table-responsive {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .main-content {
                gap: 20px;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }

            .form-row {
                grid-template-columns: 1fr;
            }

            .header {
                padding: 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .panel-header {
                flex-direction: column;
                gap: 15px;
                align-items: stretch !important;
            }

            .panel-header h2 {
                text-align: center;
            }

            /* 移动端表格处理 */
            .tasks-table {
                font-size: 0.8rem;
            }

            .tasks-table thead th {
                padding: 10px 6px;
                font-size: 0.75rem;
            }

            .tasks-table tbody td {
                padding: 8px 6px;
                font-size: 0.75rem;
            }

            .btn-sm {
                padding: 3px 6px;
                font-size: 0.65rem;
            }

            .actions-cell {
                flex-direction: column;
                gap: 3px;
            }

            .error-cell {
                max-width: 100px;
            }

            .time-cell {
                font-size: 0.7rem;
            }

            .enabled-cell {
                font-size: 0.7rem;
                padding: 2px 6px;
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

            .header h1 {
                font-size: 1.5rem;
            }

            .panel-content {
                padding: 15px;
            }

            /* 超小屏幕表格处理 */
            .table-container {
                overflow-x: scroll;
                -webkit-overflow-scrolling: touch;
            }

            .tasks-table {
                min-width: 600px;
            }

            .tasks-table thead th:nth-child(7),
            .tasks-table tbody td:nth-child(7),
            .tasks-table thead th:nth-child(8),
            .tasks-table tbody td:nth-child(8) {
                display: none;
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

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
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

        @keyframes glow {
            0%, 100% { box-shadow: var(--shadow), var(--shadow-glow); }
            50% { box-shadow: var(--shadow-lg), var(--shadow-glow); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 调度管理系统</h1>
            <p>管理和监控定时任务的Web界面</p>
            <div style="margin-top: 20px;">
                <a href="/scripts-management" class="btn btn-primary" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px;">
                    📜 脚本管理
                </a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="total-tasks">0</div>
                <div class="stat-label">总任务数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="running-tasks">0</div>
                <div class="stat-label">运行中</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="enabled-tasks">0</div>
                <div class="stat-label">已启用</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="available-tasks">0</div>
                <div class="stat-label">可用任务类型</div>
            </div>
        </div>

        <div class="main-content">
            <div class="tasks-table-panel">
                <div class="panel-header">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <h2>🚀 任务管理</h2>
                        <button class="btn btn-primary" onclick="showCreateTaskModal()">
                            ➕ 创建新任务
                        </button>
                    </div>
                </div>
                <div class="panel-content">
                    <div class="table-container">
                        <table class="tasks-table">
                            <thead>
                                <tr>
                                    <th style="width: 80px;">状态</th>
                                    <th style="width: 180px;">任务名称</th>
                                    <th style="width: 90px;">执行次数</th>
                                    <th style="width: 90px;">错误次数</th>
                                    <th style="width: 120px;">执行间隔</th>
                                    <th style="width: 100px;">启用状态</th>
                                    <th style="width: 140px;">开始时间</th>
                                    <th style="width: 160px;">最后错误</th>
                                    <th style="width: 220px;">控制操作</th>
                                </tr>
                            </thead>
                            <tbody id="tasks-table-body">
                                <!-- 任务行将通过JavaScript动态加载 -->
                            </tbody>
                        </table>
                        <div id="empty-state" class="empty-state" style="display: none;">
                            <div style="text-align: center; padding: 60px 20px;">
                                <div style="font-size: 3rem; margin-bottom: 20px;">📋</div>
                                <h3 style="color: var(--text-primary); margin-bottom: 10px;">暂无任务</h3>
                                <p style="color: var(--text-secondary); margin-bottom: 20px;">点击上方按钮创建第一个任务</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 创建任务模态框 -->
    <div id="create-task-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('create-task-modal')">&times;</span>
                <h3>创建新任务</h3>
            </div>
            <form id="create-task-form">
                <div class="form-group">
                    <label for="task-name">任务名称:</label>
                    <input type="text" id="task-name" name="name" class="form-control" required>
                </div>

                <div class="form-group">
                    <label for="task-type">任务类型:</label>
                    <select id="task-type" name="task_type" class="form-control" required>
                        <option value="">请选择任务类型</option>
                    </select>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="interval-seconds">执行间隔(秒):</label>
                        <input type="number" id="interval-seconds" name="interval_seconds" class="form-control" value="60" min="1">
                    </div>
                    <div class="form-group">
                        <label for="max-executions">最大执行次数(-1为无限):</label>
                        <input type="number" id="max-executions" name="max_executions" class="form-control" value="-1">
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="enabled">启用任务:</label>
                        <select id="enabled" name="enabled" class="form-control">
                            <option value="true">是</option>
                            <option value="false">否</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="log-level">日志级别:</label>
                        <select id="log-level" name="log_level" class="form-control">
                            <option value="DEBUG">DEBUG</option>
                            <option value="INFO" selected>INFO</option>
                            <option value="WARNING">WARNING</option>
                            <option value="ERROR">ERROR</option>
                        </select>
                    </div>
                </div>

                <!-- 任务参数配置区域 -->
                <div id="task-parameters-section" style="display: none;">
                    <hr style="margin: 30px 0; border: 1px solid var(--border-color);">
                    <h4 style="margin-bottom: 20px; color: var(--text-primary); text-shadow: 0 0 5px rgba(0, 212, 255, 0.3);">🔧 任务参数配置</h4>
                    <div id="task-parameters-container">
                        <!-- 动态生成的参数表单 -->
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('create-task-modal')">取消</button>
                    <button type="submit" class="btn btn-primary">创建任务</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 日志查看模态框 -->
    <div id="logs-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>📄 任务日志 - <span id="logs-task-name"></span></h3>
                <span class="close" onclick="closeModal('logs-modal')">&times;</span>
            </div>
            <div class="modal-body">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="color: var(--text-primary); margin: 0;">日志内容</h4>
                    <button class="btn btn-secondary" onclick="refreshTaskLogs()" style="padding: 6px 12px; font-size: 0.8rem;">
                        🔄 刷新日志
                    </button>
                </div>
                <div class="logs-viewer" id="logs-content" style="background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--border-radius); padding: 15px; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.85rem; line-height: 1.5; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;">
                    加载日志中...
                </div>
            </div>
        </div>
    </div>


    <script>
        let currentTaskName = null;
        let currentLogsTaskName = null;
        let eventSource = null;

        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadSchedulerInfo();
            loadTasksList();
            startRealTimeUpdates();

            // 绑定表单提交事件
            document.getElementById('create-task-form').addEventListener('submit', handleCreateTask);
        });

        // 启动实时更新
        function startRealTimeUpdates() {
            if (eventSource) {
                eventSource.close();
            }

            eventSource = new EventSource('/events');
            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateSchedulerStats(data);
            };

            eventSource.onerror = function() {
                console.log('SSE connection lost, retrying in 5 seconds...');
                setTimeout(startRealTimeUpdates, 5000);
            };
        }

        // 加载调度器信息
        async function loadSchedulerInfo() {
            try {
                const response = await fetch('/scheduler/info');
                const data = await response.json();
                updateSchedulerStats(data);

                // 更新任务类型下拉框
                const taskTypeSelect = document.getElementById('task-type');
                taskTypeSelect.innerHTML = '<option value="">请选择任务类型</option>';

                if (data.available_task_classes) {
                    data.available_task_classes.forEach(taskType => {
                        const option = document.createElement('option');
                        option.value = taskType;
                        option.textContent = taskType;
                        taskTypeSelect.appendChild(option);
                    });
                }

                // 存储任务参数信息
                window.taskParameters = data.task_parameters || {};

                // 监听任务类型变化
                taskTypeSelect.addEventListener('change', function() {
                    const selectedTaskType = this.value;
                    showTaskParameters(selectedTaskType);
                });

            } catch (error) {
                console.error('加载调度器信息失败:', error);
            }
        }

        // 显示任务参数配置
        function showTaskParameters(taskType) {
            const parametersSection = document.getElementById('task-parameters-section');
            const parametersContainer = document.getElementById('task-parameters-container');

            if (!taskType || !window.taskParameters || !window.taskParameters[taskType]) {
                parametersSection.style.display = 'none';
                parametersContainer.innerHTML = '';
                return;
            }

            const parameters = window.taskParameters[taskType];

            // 过滤掉 kwargs 参数，因为它在自动处理中已经包含了
            const filteredParams = Object.entries(parameters).filter(([name, info]) => name !== 'kwargs');

            if (filteredParams.length === 0) {
                parametersSection.style.display = 'none';
                return;
            }

            parametersSection.style.display = 'block';
            parametersContainer.innerHTML = '';

            filteredParams.forEach(([paramName, paramInfo]) => {
                const formGroup = document.createElement('div');
                formGroup.className = 'form-group';

                const label = document.createElement('label');
                const labelText = paramInfo.required ? `${paramName} *` : paramName;
                label.textContent = labelText;

                const input = createParameterInput(paramName, paramInfo);

                formGroup.appendChild(label);
                formGroup.appendChild(input);
                parametersContainer.appendChild(formGroup);
            });
        }

        // 根据参数类型创建输入控件
        function createParameterInput(paramName, paramInfo) {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = `param_${paramName}`;
            input.className = 'form-control';
            input.id = `param-${paramName}`;

            // 根据类型设置输入类型
            const paramType = paramInfo.type.toLowerCase();
            if (paramType.includes('int')) {
                input.type = 'number';
            } else if (paramType.includes('bool')) {
                // 布尔类型使用下拉框
                const select = document.createElement('select');
                select.name = input.name;
                select.className = input.className;
                select.id = input.id;

                const trueOption = document.createElement('option');
                trueOption.value = 'true';
                trueOption.textContent = 'True';

                const falseOption = document.createElement('option');
                falseOption.value = 'false';
                falseOption.textContent = 'False';

                select.appendChild(trueOption);
                select.appendChild(falseOption);

                // 设置默认值
                if (paramInfo.default !== null && paramInfo.default !== undefined) {
                    select.value = paramInfo.default.toString();
                }

                return select;
            } else if (paramType.includes('dict') || paramType.includes('list')) {
                // 复杂类型使用文本域
                const textarea = document.createElement('textarea');
                textarea.name = input.name;
                textarea.className = input.className;
                textarea.id = input.id;
                textarea.rows = 3;
                textarea.placeholder = '请输入JSON格式的数据，例如: {"key": "value"} 或 ["item1", "item2"]';
                return textarea;
            }

            // 设置默认值
            if (paramInfo.default !== null && paramInfo.default !== undefined) {
                input.value = paramInfo.default;
            }

            // 设置占位符
            if (paramInfo.required) {
                input.placeholder = `请输入 ${paramName}`;
                input.required = true;
            } else {
                input.placeholder = `可选，默认值: ${paramInfo.default}`;
            }

            return input;
        }

        // 更新调度器统计信息
        function updateSchedulerStats(data) {
            document.getElementById('total-tasks').textContent = data.total_tasks || 0;
            document.getElementById('running-tasks').textContent = data.running_tasks || 0;
            document.getElementById('enabled-tasks').textContent = data.enabled_tasks || 0;
            document.getElementById('available-tasks').textContent = (data.available_task_classes || []).length;
        }

        // 加载任务列表
        async function loadTasksList() {
            try {
                const response = await fetch('/tasks');
                const tasks = await response.json();

                const tableBody = document.getElementById('tasks-table-body');
                const emptyState = document.getElementById('empty-state');
                const table = document.querySelector('.tasks-table');

                tableBody.innerHTML = '';

                if (Object.keys(tasks).length === 0) {
                    table.style.display = 'none';
                    emptyState.style.display = 'block';
                    return;
                }

                table.style.display = 'table';
                emptyState.style.display = 'none';

                Object.values(tasks).forEach(task => {
                    const taskRow = createTaskTableRow(task);
                    tableBody.appendChild(taskRow);
                });
            } catch (error) {
                console.error('加载任务列表失败:', error);
            }
        }

        // 创建任务表格行
        function createTaskTableRow(task) {
            const tr = document.createElement('tr');
            tr.className = `${task.running ? 'running' : ''} ${task.status === 'error' ? 'error' : ''}`;

            // 格式化时间
            const formatTime = (timeStr) => {
                if (!timeStr || timeStr === '未启动' || timeStr === '运行中') return timeStr;
                try {
                    const date = new Date(timeStr);
                    return date.toLocaleString('zh-CN', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                } catch (e) {
                    return timeStr;
                }
            };

            // 格式化错误信息
            const formatError = (error) => {
                if (!error || error === '无') return '无';
                return error.length > 30 ? error.substring(0, 27) + '...' : error;
            };

            tr.innerHTML = `
                <td>
                    <div class="status-cell">
                        <span class="status-indicator ${task.running ? 'running' : task.status === 'error' ? 'error' : 'stopped'}"></span>
                        <span>${task.status}</span>
                    </div>
                </td>
                <td>
                    <div class="task-name-cell" title="${task.name}">${task.name}</div>
                </td>
                <td>
                    <span class="execution-count">${task.execution_count}</span>
                </td>
                <td>
                    <span class="error-count">${task.error_count}</span>
                </td>
                <td>
                    <div class="interval-cell">${task.config.interval_seconds}秒</div>
                </td>
                <td>
                    <span class="enabled-cell ${task.config.enabled ? 'enabled' : 'disabled'}">
                        ${task.config.enabled ? '已启用' : '已禁用'}
                    </span>
                </td>
                <td>
                    <div class="time-cell" title="${task.start_time || '未启动'}">
                        ${formatTime(task.start_time)}
                    </div>
                </td>
                <td>
                    <div class="error-cell" title="${task.last_error || '无'}">
                        ${formatError(task.last_error)}
                    </div>
                </td>
                <td>
                    <div class="actions-cell">
                        ${task.running ?
                            `<button class="btn btn-warning btn-sm" onclick="stopTask('${task.name}')" title="停止任务">停止</button>` :
                            `<button class="btn btn-success btn-sm" onclick="startTask('${task.name}')" title="启动任务">启动</button>`
                        }
                        <button class="btn btn-secondary btn-sm" onclick="showTaskLogs('${task.name}')" title="查看日志">日志</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteTask('${task.name}')" title="删除任务">删除</button>
                    </div>
                </td>
            `;
            return tr;
        }

        // 显示任务详情
        async function showTaskDetails(taskName) {
            try {
                const response = await fetch(`/tasks/${taskName}/status`);
                const task = await response.json();

                const detailsDiv = document.getElementById('task-details');
                detailsDiv.innerHTML = `
                    <div style="display: flex; align-items: center; margin-bottom: 20px;">
                        <h3 style="margin: 0; color: var(--text-primary); text-shadow: 0 0 10px var(--primary-glow);">任务详情: ${task.name}</h3>
                        <div style="margin-left: auto; display: flex; gap: 10px;">
                            <button class="tab-btn ${currentTab === 'details' ? 'active' : ''}" onclick="switchTab('details', '${taskName}')" style="padding: 8px 16px; border: 1px solid var(--border-color); background: ${currentTab === 'details' ? 'var(--primary-color)' : 'rgba(255, 255, 255, 0.1)'}; color: var(--text-primary); border-radius: 6px; cursor: pointer; transition: all 0.3s ease;">
                                📊 详情
                            </button>
                            <button class="tab-btn ${currentTab === 'logs' ? 'active' : ''}" onclick="switchTab('logs', '${taskName}')" style="padding: 8px 16px; border: 1px solid var(--border-color); background: ${currentTab === 'logs' ? 'var(--primary-color)' : 'rgba(255, 255, 255, 0.1)'}; color: var(--text-primary); border-radius: 6px; cursor: pointer; transition: all 0.3s ease;">
                                📄 日志
                            </button>
                        </div>
                    </div>
                    <div id="task-details-content">
                        ${currentTab === 'details' ? getDetailsContent(task) : getLogsContent(taskName)}
                    </div>
                `;

                tasksList.innerHTML = tableHTML;
            } catch (error) {
                console.error('加载任务列表失败:', error);
                const tasksList = document.getElementById('tasks-list');
                tasksList.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--danger-color);">
                        <p>加载任务列表失败: ${error.message}</p>
                    </div>
                `;
            }
        }

        // 创建任务表格行
        function createTaskRow(task) {
            // 格式化时间显示
            const formatTime = (timeStr) => {
                if (!timeStr || timeStr === '未启动') return '未启动';
                try {
                    const date = new Date(timeStr);
                    return date.toLocaleString('zh-CN');
                } catch {
                    return timeStr;
                }
            };

            // 状态文本样式类
            const getStatusClass = () => {
                if (task.running) return 'task-running';
                if (task.status === 'error') return 'task-error';
                return 'task-stopped';
            };

            // 状态指示器类
            const getStatusIndicatorClass = () => {
                if (task.running) return 'running';
                if (task.status === 'error') return 'error';
                return 'stopped';
            };

            return `
                <tr class="task-row">
                    <td class="status-cell">
                        <span class="status-indicator ${getStatusIndicatorClass()}" title="${task.status}"></span>
                    </td>
                    <td class="task-name-cell">${task.name}</td>
                    <td class="status-text-cell ${getStatusClass()}">${task.status}</td>
                    <td class="execution-cell">${task.running ? '是' : '否'}</td>
                    <td class="execution-cell">${task.execution_count}</td>
                    <td class="error-cell ${task.error_count > 0 ? 'task-error' : ''}">${task.error_count}</td>
                    <td class="time-cell">${formatTime(task.start_time)}</td>
                    <td class="time-cell">${formatTime(task.end_time)}</td>
                    <td style="max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${task.last_error || '无'}">
                        ${task.last_error || '无'}
                    </td>
                    <td class="log-file-cell" title="${task.log_file}">
                        ${task.log_file}
                    </td>
                    <td class="actions-cell">
                        <div class="table-actions">
                            ${task.running ?
                                `<button class="btn btn-warning btn-table" onclick="stopTask('${task.name}')" title="停止任务">停止</button>` :
                                `<button class="btn btn-success btn-table" onclick="startTask('${task.name}')" title="启动任务">启动</button>`
                            }
                            <button class="btn btn-danger btn-table" onclick="deleteTask('${task.name}')" title="删除任务">删除</button>
                            <button class="btn btn-secondary btn-table" onclick="showLogsModal('${task.name}')" title="查看日志">日志</button>
                        </div>
                    </td>
                </tr>
            `;
        }

        // 显示日志模态框
        function showLogsModal(taskName) {
            currentLogsTaskName = taskName;
            document.getElementById('logs-task-name').textContent = taskName;
            document.getElementById('logs-modal').style.display = 'block';
            document.getElementById('logs-content').textContent = '加载日志中...';
            refreshTaskLogs();
        }

        // 刷新任务日志
        async function refreshTaskLogs() {
            if (!currentLogsTaskName) return;

        // 显示任务日志模态框
        async function showTaskLogs(taskName) {
            try {
                const response = await fetch(`/tasks/${taskName}/logs?lines=200`);
                const logs = await response.json();

                // 创建或更新日志模态框
                let logsModal = document.getElementById('logs-modal');
                if (!logsModal) {
                    // 如果不存在，创建日志模态框
                    const modalHTML = `
                        <div id="logs-modal" class="modal">
                            <div class="modal-content" style="max-width: 800px;">
                                <div class="modal-header">
                                    <span class="close" onclick="closeModal('logs-modal')">&times;</span>
                                    <h3 id="logs-title">任务日志</h3>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <span style="color: var(--text-secondary); font-size: 0.9rem;">任务: <strong style="color: var(--text-primary);">${taskName}</strong></span>
                                    <button class="btn btn-secondary" onclick="refreshModalLogs('${taskName}')" style="padding: 6px 12px; font-size: 0.8rem;">
                                        🔄 刷新日志
                                    </button>
                                </div>
                                <div class="logs-viewer" id="modal-logs-content" style="background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--border-radius); padding: 15px; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.85rem; line-height: 1.5; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;">
                                    加载日志中...
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" onclick="closeModal('logs-modal')">关闭</button>
                                </div>
                            </div>
                        </div>
                    `;
                    document.body.insertAdjacentHTML('beforeend', modalHTML);
                    logsModal = document.getElementById('logs-modal');
                }

                // 更新标题和内容
                document.getElementById('logs-title').textContent = `任务日志 - ${taskName}`;
                const logsContent = document.getElementById('modal-logs-content');
                if (logsContent) {
                    logsContent.textContent = logs.length > 0 ? logs.join('\\n') : '暂无日志';
                    logsContent.scrollTop = logsContent.scrollHeight;
                }

                // 显示模态框
                logsModal.style.display = 'block';
                currentTaskName = taskName;

            } catch (error) {
                console.error('获取日志失败:', error);
                showNotification('获取日志失败', 'error');
            }
        }

        // 刷新模态框中的日志
        async function refreshModalLogs(taskName) {
            try {
                const response = await fetch(`/tasks/${taskName}/logs?lines=200`);
                const logs = await response.json();

                const logsContent = document.getElementById('modal-logs-content');
                if (logsContent) {
                    logsContent.textContent = logs.length > 0 ? logs.join('\\n') : '暂无日志';
                    logsContent.scrollTop = logsContent.scrollHeight;
                }
                showNotification('日志刷新成功', 'success');
            } catch (error) {
                console.error('刷新日志失败:', error);
                showNotification('刷新日志失败', 'error');
            }
        }

        // 加载任务日志（用于详情面板）
        async function loadTaskLogs(taskName) {
            try {
                const response = await fetch(`/tasks/${currentLogsTaskName}/logs?lines=200`);
                const logs = await response.json();

                const logsContent = document.getElementById('logs-content');
                if (logsContent) {
                    logsContent.textContent = logs.length > 0 ? logs.join('\\n') : '暂无日志';
                    logsContent.scrollTop = logsContent.scrollHeight;
                }
            } catch (error) {
                console.error('加载日志失败:', error);
                const logsContent = document.getElementById('logs-content');
                if (logsContent) {
                    logsContent.textContent = '加载日志失败: ' + error.message;
                }
            }
        }

        // 启动任务
        async function startTask(taskName) {
            try {
                const response = await fetch(`/tasks/${taskName}/start`, {
                    method: 'POST'
                });

                if (response.ok) {
                    showNotification('任务启动成功', 'success');
                    loadTasksList();
                } else {
                    const error = await response.json();
                    showNotification(`启动失败: ${error.detail}`, 'error');
                }
            } catch (error) {
                console.error('启动任务失败:', error);
                showNotification('启动任务失败', 'error');
            }
        }

        // 停止任务
        async function stopTask(taskName) {
            try {
                const response = await fetch(`/tasks/${taskName}/stop`, {
                    method: 'POST'
                });

                if (response.ok) {
                    showNotification('任务停止成功', 'success');
                    loadTasksList();
                } else {
                    const error = await response.json();
                    showNotification(`停止失败: ${error.detail}`, 'error');
                }
            } catch (error) {
                console.error('停止任务失败:', error);
                showNotification('停止任务失败', 'error');
            }
        }

        // 删除任务
        async function deleteTask(taskName) {
            if (!confirm(`确定要删除任务 "${taskName}" 吗？`)) {
                return;
            }

            try {
                const response = await fetch(`/tasks/${taskName}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    showNotification('任务删除成功', 'success');
                    loadTasksList();
                    if (currentTaskName === taskName) {
                        currentTaskName = null;
                    }
                } else {
                    const error = await response.json();
                    showNotification(`删除失败: ${error.detail}`, 'error');
                }
            } catch (error) {
                console.error('删除任务失败:', error);
                showNotification('删除任务失败', 'error');
            }
        }

        
        // 显示创建任务模态框
        function showCreateTaskModal() {
            document.getElementById('create-task-modal').style.display = 'block';
        }

        // 关闭模态框
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // 处理创建任务
        async function handleCreateTask(event) {
            event.preventDefault();

            const formData = new FormData(event.target);
            const taskData = {
                name: formData.get('name'),
                task_type: formData.get('task_type'),
                interval_seconds: parseInt(formData.get('interval_seconds')),
                enabled: formData.get('enabled') === 'true',
                max_executions: parseInt(formData.get('max_executions')),
                log_level: formData.get('log_level'),
                exchange_configs: [],
                ai_configs: [],
                params: {}
            };

            // 收集自定义参数
            const taskType = formData.get('task_type');
            if (taskType && window.taskParameters && window.taskParameters[taskType]) {
                const parameters = window.taskParameters[taskType];

                Object.entries(parameters).forEach(([paramName, paramInfo]) => {
                    if (paramName === 'kwargs') return; // 跳过 kwargs

                    const inputElement = document.getElementById(`param-${paramName}`);
                    if (inputElement) {
                        let value = inputElement.value;

                        // 处理布尔值
                        if (paramInfo.type.toLowerCase().includes('bool')) {
                            taskData.params[paramName] = value === 'true';
                        }
                        // 处理整数
                        else if (paramInfo.type.toLowerCase().includes('int')) {
                            taskData.params[paramName] = parseInt(value) || 0;
                        }
                        // 处理复杂类型（JSON）
                        else if (paramInfo.type.toLowerCase().includes('dict') ||
                                 paramInfo.type.toLowerCase().includes('list')) {
                            try {
                                taskData.params[paramName] = JSON.parse(value || '{}');
                            } catch (e) {
                                console.warn(`参数 ${paramName} JSON解析失败，使用原始字符串值`);
                                taskData.params[paramName] = value;
                            }
                        }
                        // 处理字符串
                        else {
                            taskData.params[paramName] = value;
                        }
                    }
                });
            }

            try {
                const response = await fetch('/tasks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(taskData)
                });

                if (response.ok) {
                    showNotification('任务创建成功', 'success');
                    closeModal('create-task-modal');
                    document.getElementById('create-task-form').reset();
                    loadTasksList();
                    loadSchedulerInfo();
                } else {
                    const error = await response.json();
                    showNotification(`创建失败: ${error.detail}`, 'error');
                }
            } catch (error) {
                console.error('创建任务失败:', error);
                showNotification('创建任务失败', 'error');
            }
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