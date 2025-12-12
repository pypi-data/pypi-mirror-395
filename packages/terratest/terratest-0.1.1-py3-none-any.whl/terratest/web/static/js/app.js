let currentView = 'jobs'; // 'jobs' or 'folder'
let currentJobId = null;

// Configuración global (se carga desde localStorage si existe)
let jobConfig = {
    enableSSH: false,
    sshKeyPath: '',
    tfCloudToken: '',
    tfCloudOrg: '',
    tfCloudWorkspace: '',
    awsAccessKeyId: '',
    awsSecretAccessKey: '',
    awsSessionToken: ''
};

// Cargar configuración guardada
try {
    const savedConfig = localStorage.getItem('terratest_config');
    if (savedConfig) {
        jobConfig = { ...jobConfig, ...JSON.parse(savedConfig) };
    }
} catch (error) {
    console.error('Error al cargar configuración:', error);
}

async function runJob() {
    const out = document.getElementById("output");
    const section = document.getElementById("outputSection");
    const summary = document.getElementById("jobSummary");
    const modulePathInput = document.getElementById("modulePath");
    
    const modulePath = modulePathInput.value.trim();
    if (!modulePath) {
        showAlert({
            type: 'warning',
            title: 'Ruta Requerida',
            message: 'Debes especificar la ruta del módulo de Terraform'
        });
        return;
    }
    
    section.style.display = "block";
    summary.innerHTML = '<div style="padding: 40px; text-align: center; color: #6b7280;"><i class="fas fa-spinner fa-pulse"></i><br/><br/>Ejecutando...</div>';
    out.textContent = `⏳ Ejecutando job...\n\nMódulo: ${modulePath}\n\nPor favor espere...`;

    try {
        // Construir URL con todos los parámetros
        const params = new URLSearchParams({
            module_path: modulePath,
            enable_ssh: jobConfig.enableSSH.toString()
        });
        
        if (jobConfig.sshKeyPath) {
            params.append('ssh_key_path', jobConfig.sshKeyPath);
        }
        if (jobConfig.tfCloudToken) {
            params.append('tf_cloud_token', jobConfig.tfCloudToken);
        }
        if (jobConfig.tfCloudOrg) {
            params.append('tf_cloud_org', jobConfig.tfCloudOrg);
        }
        if (jobConfig.tfCloudWorkspace) {
            params.append('tf_cloud_workspace', jobConfig.tfCloudWorkspace);
        }
        if (jobConfig.awsAccessKeyId) {
            params.append('aws_access_key_id', jobConfig.awsAccessKeyId);
        }
        if (jobConfig.awsSecretAccessKey) {
            params.append('aws_secret_access_key', jobConfig.awsSecretAccessKey);
        }
        if (jobConfig.awsSessionToken) {
            params.append('aws_session_token', jobConfig.awsSessionToken);
        }
        
        const res = await fetch(`/api/jobs?${params.toString()}`, {
            method: "POST"
        });

        const data = await res.json();
        console.log('Job data received:', data);
        
        // Siempre mostrar el JSON raw en la izquierda
        out.textContent = JSON.stringify(data, null, 2);
        
        // Si el job terminó exitosamente, también mostrar el resumen visual en la derecha
        if (data.status === "terraform_complete") {
            console.log('Building summary...');
            summary.innerHTML = buildJobSummary(data);
        } else {
            summary.innerHTML = '<div style="padding: 40px; text-align: center; color: #6b7280;">Job en progreso...</div>';
        }

        // Recargar lista de jobs cuando termine
        setTimeout(() => {
            loadJobs();
        }, 500);
    } catch (error) {
        console.error('Error running job:', error);
        out.textContent = `❌ Error al ejecutar job:\n${error.message}`;
        summary.innerHTML = '<div style="padding: 40px; text-align: center; color: #ef4444;"><i class="fas fa-exclamation-circle"></i><br/><br/>Error</div>';
    }
}

function buildJobSummary(data) {
    const duration = data.duration_seconds ? data.duration_seconds.toFixed(2) : '0';
    const plan = data.plan_summary || {};
    
    return `
        <div class="summary-grid">
            <!-- Header -->
            <div class="summary-header">
                <div class="summary-title">
                    <i class="fas fa-check-circle"></i>
                    <span>Job completado exitosamente</span>
                </div>
                <div class="summary-meta">
                    <span class="job-id">${data.job_id}</span>
                    <span class="duration">${duration}s</span>
                </div>
            </div>

            <!-- Plan Summary -->
            <div class="summary-section">
                <h3><i class="fas fa-chart-bar"></i> Plan Summary</h3>
                <div class="plan-stats">
                    <div class="stat-item stat-add">
                        <span class="stat-value">${plan.add || 0}</span>
                        <span class="stat-label">Add</span>
                    </div>
                    <div class="stat-item stat-change">
                        <span class="stat-value">${plan.change || 0}</span>
                        <span class="stat-label">Change</span>
                    </div>
                    <div class="stat-item stat-destroy">
                        <span class="stat-value">${plan.destroy || 0}</span>
                        <span class="stat-label">Destroy</span>
                    </div>
                </div>
            </div>

            <!-- Resources -->
            ${data.resources && data.resources.length > 0 ? `
            <div class="summary-section">
                <h3><i class="fas fa-cubes"></i> Resources (${data.resources.length})</h3>
                <div class="resources-list">
                    ${data.resources.map(r => `
                        <div class="resource-item">
                            <i class="fas fa-cube"></i>
                            <span class="resource-type">${r.type}</span>
                            <span class="resource-name">${r.name}</span>
                            <span class="resource-actions">${r.actions.join(', ')}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            <!-- Outputs -->
            ${data.outputs && Object.keys(data.outputs).length > 0 ? `
            <div class="summary-section">
                <h3><i class="fas fa-external-link-alt"></i> Outputs</h3>
                <div class="outputs-list">
                    ${Object.entries(data.outputs).map(([key, value]) => `
                        <div class="output-item">
                            <span class="output-key">${key}</span>
                            <span class="output-value">${value !== null ? value : 'null'}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            <!-- Timestamps -->
            <div class="summary-section summary-footer">
                <div class="timestamp-item">
                    <i class="fas fa-clock"></i>
                    <span>Inicio: ${new Date(data.started_at).toLocaleString('es-ES')}</span>
                </div>
                <div class="timestamp-item">
                    <i class="fas fa-flag-checkered"></i>
                    <span>Fin: ${new Date(data.finished_at).toLocaleString('es-ES')}</span>
                </div>
            </div>
        </div>
    `;
}

function closeOutput() {
    document.getElementById("outputSection").style.display = "none";
}

// ========================
//  LISTA DE JOBS
// ========================
async function loadJobs() {
    currentView = 'jobs';
    currentJobId = null;
    
    const container = document.getElementById("jobs");
    const section = document.querySelector(".jobs-section");
    
    // Actualizar título
    section.querySelector("h2").innerHTML = '<i class="fas fa-folder-open"></i> Jobs Ejecutados';
    
    container.innerHTML = '<div style="text-align: center; padding: 20px; color: #6b7280; background: #1a1a1a;"><i class="fas fa-spinner fa-spin"></i> Cargando...</div>';

    try {
        const res = await fetch("/api/jobs/");
        const jobs = await res.json();

        container.innerHTML = "";

        if (jobs.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 60px; color: #6b7280; background: #1a1a1a; border: 1px solid #2a2a2a;">
                    <i class="fas fa-folder-open" style="font-size: 2.5rem; margin-bottom: 15px; opacity: 0.3;"></i>
                    <p>No hay jobs ejecutados</p>
                </div>
            `;
            return;
        }

        jobs.forEach(job => {
            const div = document.createElement("div");
            div.className = "job-folder";
            div.onclick = () => openFolder(job.job_id, job.files);

            const fileCount = job.files.length;

            div.innerHTML = `
                <div class="folder-header">
                    <i class="fas fa-folder folder-icon"></i>
                    <div class="folder-title">
                        <h3>${job.job_id}</h3>
                        <div class="folder-meta">${fileCount} archivo${fileCount !== 1 ? 's' : ''}</div>
                    </div>
                    <div class="folder-actions">
                        <button class="btn-delete-folder" onclick="deleteJob('${job.job_id}'); event.stopPropagation();" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;

            container.appendChild(div);
        });
    } catch (error) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #ef4444; background: #1a1a1a; border: 1px solid #2a2a2a;">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>Error al cargar jobs</p>
                <p style="font-size: 0.85rem; margin-top: 8px; color: #9ca3af;">${error.message}</p>
            </div>
        `;
    }
}

// ========================
//  ELIMINAR JOB
// ========================
async function deleteJob(jobId) {
    console.log('deleteJob llamado con:', jobId);
    
    const confirmed = await showConfirm({
        type: 'warning',
        title: 'Eliminar Job',
        message: `¿Eliminar el job "${jobId}"?`,
        confirmText: 'Eliminar',
        cancelText: 'Cancelar'
    });
    
    if (!confirmed) {
        return;
    }

    try {
        const url = `/api/jobs/${jobId}`;
        console.log('DELETE request a:', url);
        
        const res = await fetch(url, {
            method: "DELETE"
        });

        console.log('Response status:', res.status);

        if (res.ok) {
            const data = await res.json();
            console.log('Job eliminado:', data);
            loadJobs();
        } else {
            const error = await res.json();
            console.error('Error del servidor:', error);
            showAlert({
                type: 'error',
                title: 'Error',
                message: error.detail
            });
        }
    } catch (error) {
        console.error('Error al eliminar:', error);
        showAlert({
            type: 'error',
            title: 'Error',
            message: `Error al eliminar: ${error.message}`
        });
    }
}

// ========================
//  ELIMINAR TODOS
// ========================
async function deleteAllJobs() {
    console.log('deleteAllJobs llamado');
    
    const confirmed = await showConfirm({
        type: 'danger',
        title: 'Eliminar Todos los Jobs',
        message: '¿Eliminar TODOS los jobs? Esta acción no se puede deshacer.',
        confirmText: 'Eliminar Todos',
        cancelText: 'Cancelar'
    });
    
    if (!confirmed) {
        return;
    }

    try {
        const res = await fetch("/api/jobs/all", {
            method: "DELETE"
        });

        console.log('Response status:', res.status);
        const data = await res.json();
        console.log('Respuesta:', data);
        showAlert({
            type: 'success',
            title: 'Jobs Eliminados',
            message: data.message
        });
        loadJobs();
    } catch (error) {
        console.error('Error:', error);
        showAlert({
            type: 'error',
            title: 'Error',
            message: `Error al eliminar: ${error.message}`
        });
    }
}

// ========================
//  ABRIR CARPETA
// ========================
function openFolder(jobId, files) {
    currentView = 'folder';
    currentJobId = jobId;
    
    const container = document.getElementById("jobs");
    const section = document.querySelector(".jobs-section");
    const header = section.querySelector(".section-header");
    
    // Actualizar título con breadcrumb y botón de eliminar
    header.innerHTML = `
        <h2>
            <i class="fas fa-folder-open"></i>
            <span class="breadcrumb">
                <span class="breadcrumb-item" onclick="loadJobs(); event.stopPropagation();">Jobs</span>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-current">${jobId}</span>
            </span>
        </h2>
        <div class="header-actions">
            <button class="btn-delete" onclick="deleteCurrentJob()" title="Eliminar este job">
                <i class="fas fa-trash-alt"></i>
            </button>
            <button class="btn-close" onclick="loadJobs()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    container.innerHTML = "";
    
    const fileList = document.createElement("div");
    fileList.className = "file-list";
    
    files.forEach(filename => {
        const fileItem = document.createElement("div");
        fileItem.className = "file-item";
        fileItem.onclick = () => loadFile(jobId, filename);
        
        fileItem.innerHTML = `
            <i class="fas fa-file-code"></i>
            <span>${filename}</span>
        `;
        
        fileList.appendChild(fileItem);
    });
    
    container.appendChild(fileList);
}

// ========================
//  ELIMINAR JOB ACTUAL
// ========================
async function deleteCurrentJob() {
    if (!currentJobId) return;
    
    const confirmed = await showConfirm({
        type: 'warning',
        title: 'Eliminar Job',
        message: `¿Eliminar el job "${currentJobId}"?`,
        confirmText: 'Eliminar',
        cancelText: 'Cancelar'
    });
    
    if (!confirmed) {
        return;
    }

    try {
        const res = await fetch(`/api/jobs/${currentJobId}`, {
            method: "DELETE"
        });

        if (res.ok) {
            loadJobs();
        } else {
            const error = await res.json();
            showAlert({
                type: 'error',
                title: 'Error',
                message: error.detail
            });
        }
    } catch (error) {
        showAlert({
            type: 'error',
            title: 'Error',
            message: `Error al eliminar: ${error.message}`
        });
    }
}

// ========================
//  LEER ARCHIVO
// ========================
async function loadFile(jobId, filename) {
    const out = document.getElementById("fileContent");
    const viewer = document.getElementById("fileViewer");
    const fileNameEl = document.getElementById("fileName");
    
    viewer.style.display = "block";
    fileNameEl.textContent = filename;
    out.innerHTML = '<div style="color: #6b7280;">Cargando...</div>';

    viewer.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const res = await fetch(`/api/jobs/${jobId}/files/${filename}`);
        const data = await res.json();
        
        // Procesar el contenido y aplicar colores
        const content = data.content;
        const formattedContent = formatFileContent(content, filename);
        out.innerHTML = formattedContent;
    } catch (error) {
        out.innerHTML = `<div style="color: #ef4444;"><i class="fas fa-exclamation-circle"></i> Error al cargar archivo:<br/>${escapeHtml(error.message)}</div>`;
    }
}

function formatFileContent(content, filename) {
    // Limpiar códigos ANSI de todo el contenido primero
    const cleanContent = stripAnsiCodes(content);
    
    // Detectar el tipo de archivo
    const isLog = filename.toLowerCase().includes('log') || filename.toLowerCase().includes('stderr') || filename.toLowerCase().includes('stdout');
    const isJson = filename.toLowerCase().endsWith('.json');
    const isTerraform = filename.toLowerCase().endsWith('.tf') || filename.toLowerCase().endsWith('.tfvars');
    
    if (isLog) {
        // Formatear logs con colores (ya está limpio)
        return formatLogContent(content);
    } else if (isJson) {
        // Intentar formatear JSON
        try {
            const parsed = JSON.parse(cleanContent);
            return `<pre style="margin: 0;">${escapeHtml(JSON.stringify(parsed, null, 2))}</pre>`;
        } catch (e) {
            return `<pre style="margin: 0;">${escapeHtml(cleanContent)}</pre>`;
        }
    } else {
        // Contenido normal
        return `<pre style="margin: 0;">${escapeHtml(cleanContent)}</pre>`;
    }
}

function stripAnsiCodes(text) {
    return text
        .replace(/\x1B\[[0-9;]*[A-Za-z]/g, '')
        .replace(/\x1B\][0-9];[^\x07]*\x07/g, '')
        .replace(/\x1B\[[\?]?[0-9;]*[A-Za-z]/g, '')
        .replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F]/g, '')
        .replace(/\u001b/g, '');
}

function formatLogContent(content) {
    // Limpiar códigos ANSI primero
    const cleanContent = stripAnsiCodes(content);
    const lines = cleanContent.split('\n');
    
    const formattedLines = lines.map(line => {
        const lowerLine = line.toLowerCase();
        
        // Detectar errores
        if (lowerLine.includes('error') || lowerLine.includes('failed') || lowerLine.includes('fatal')) {
            return `<div style="color: #ef4444; margin: 2px 0;">${escapeHtml(line)}</div>`;
        }
        // Detectar advertencias
        else if (lowerLine.includes('warning') || lowerLine.includes('warn')) {
            return `<div style="color: #f59e0b; margin: 2px 0;">${escapeHtml(line)}</div>`;
        }
        // Detectar éxito
        else if (lowerLine.includes('success') || lowerLine.includes('complete') || lowerLine.includes('done')) {
            return `<div style="color: #10b981; margin: 2px 0;">${escapeHtml(line)}</div>`;
        }
        // Detectar información importante
        else if (lowerLine.includes('info') || lowerLine.includes('note')) {
            return `<div style="color: #60a5fa; margin: 2px 0;">${escapeHtml(line)}</div>`;
        }
        // Línea normal
        else {
            return `<div style="color: #e0e0e0; margin: 2px 0;">${escapeHtml(line)}</div>`;
        }
    });
    
    return formattedLines.join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function closeFileViewer() {
    document.getElementById("fileViewer").style.display = "none";
}

// ========================
//  CONFIGURACIÓN
// ========================
function openConfig() {
    const modal = document.getElementById('configModal');
    
    // Cargar valores actuales
    document.getElementById('enableSSH').checked = jobConfig.enableSSH;
    document.getElementById('sshKeyPath').value = jobConfig.sshKeyPath;
    document.getElementById('tfCloudToken').value = jobConfig.tfCloudToken;
    document.getElementById('tfCloudOrg').value = jobConfig.tfCloudOrg;
    document.getElementById('tfCloudWorkspace').value = jobConfig.tfCloudWorkspace;
    document.getElementById('awsAccessKeyId').value = jobConfig.awsAccessKeyId;
    document.getElementById('awsSecretAccessKey').value = jobConfig.awsSecretAccessKey;
    document.getElementById('awsSessionToken').value = jobConfig.awsSessionToken;
    
    // Mostrar/ocultar opciones SSH
    toggleSSHOptions();
    
    modal.style.display = 'flex';
}

function closeConfig() {
    document.getElementById('configModal').style.display = 'none';
}

function toggleSSHOptions() {
    const enableSSH = document.getElementById('enableSSH').checked;
    const sshOptions = document.getElementById('sshOptions');
    sshOptions.style.display = enableSSH ? 'block' : 'none';
}

function saveConfig() {
    jobConfig.enableSSH = document.getElementById('enableSSH').checked;
    jobConfig.sshKeyPath = document.getElementById('sshKeyPath').value.trim();
    jobConfig.tfCloudToken = document.getElementById('tfCloudToken').value.trim();
    jobConfig.tfCloudOrg = document.getElementById('tfCloudOrg').value.trim();
    jobConfig.tfCloudWorkspace = document.getElementById('tfCloudWorkspace').value.trim();
    jobConfig.awsAccessKeyId = document.getElementById('awsAccessKeyId').value.trim();
    jobConfig.awsSecretAccessKey = document.getElementById('awsSecretAccessKey').value.trim();
    jobConfig.awsSessionToken = document.getElementById('awsSessionToken').value.trim();
    
    // Guardar en localStorage
    localStorage.setItem('terratest_config', JSON.stringify(jobConfig));
    
    closeConfig();
    updateConfigIndicator();
    
    // Mostrar confirmación visual
    let configSummary = [];
    if (jobConfig.enableSSH) configSummary.push('SSH');
    if (jobConfig.tfCloudToken) configSummary.push('TF Cloud');
    if (jobConfig.awsAccessKeyId) configSummary.push('AWS');
    
    if (configSummary.length > 0) {
        console.log('Configuración guardada:', configSummary.join(', '));
    }
}

function updateConfigIndicator() {
    const configBtn = document.getElementById('configBtn');
    if (!configBtn) return;
    
    const hasConfig = jobConfig.enableSSH || jobConfig.tfCloudToken || jobConfig.awsAccessKeyId;
    
    if (hasConfig) {
        let title = 'Configuración activa: ';
        let items = [];
        if (jobConfig.enableSSH) items.push('SSH');
        if (jobConfig.tfCloudToken) items.push('TF Cloud');
        if (jobConfig.awsAccessKeyId) items.push('AWS');
        configBtn.title = title + items.join(', ');
        configBtn.style.color = '#4ade80'; // Verde si hay configuración
    } else {
        configBtn.title = 'Configurar SSH, Terraform Cloud y AWS';
        configBtn.style.color = '#a3a3a3'; // Gris por defecto
    }
}

// ========================
//  CONFIRM DIALOG
// ========================
function showConfirm(options) {
    return new Promise((resolve) => {
        const modal = document.getElementById('confirmModal');
        const icon = document.getElementById('confirmIcon');
        const title = document.getElementById('confirmTitle');
        const message = document.getElementById('confirmMessage');
        const okBtn = document.getElementById('confirmOkBtn');
        const cancelBtn = document.getElementById('confirmCancelBtn');
        
        // Configurar tipo de alerta
        const types = {
            warning: {
                icon: '<i class="fas fa-exclamation-triangle" style="color: #f59e0b;"></i>',
                btnClass: 'btn-delete',
                btnText: options.confirmText || 'Eliminar'
            },
            danger: {
                icon: '<i class="fas fa-exclamation-circle" style="color: #ef4444;"></i>',
                btnClass: 'btn-delete',
                btnText: options.confirmText || 'Confirmar'
            },
            info: {
                icon: '<i class="fas fa-info-circle" style="color: #60a5fa;"></i>',
                btnClass: 'btn-primary',
                btnText: options.confirmText || 'Aceptar'
            },
            success: {
                icon: '<i class="fas fa-check-circle" style="color: #10b981;"></i>',
                btnClass: 'btn-primary',
                btnText: options.confirmText || 'OK'
            }
        };
        
        const type = types[options.type || 'warning'];
        
        // Aplicar contenido
        icon.innerHTML = type.icon;
        title.textContent = options.title || '¿Estás seguro?';
        message.textContent = options.message || '';
        
        // Configurar botón de confirmación
        okBtn.className = type.btnClass;
        okBtn.innerHTML = `<i class="fas fa-check"></i> ${type.btnText}`;
        
        // Configurar botón de cancelar
        cancelBtn.innerHTML = `<i class="fas fa-times"></i> ${options.cancelText || 'Cancelar'}`;
        
        // Mostrar modal
        modal.style.display = 'flex';
        
        // Manejadores de teclado
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                e.preventDefault();
                handleCancel();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                handleOk();
            }
        };
        
        const handleModalClick = (e) => {
            if (e.target === modal) {
                handleCancel();
            }
        };
        
        // Función de limpieza
        const cleanup = () => {
            okBtn.removeEventListener('click', handleOk);
            cancelBtn.removeEventListener('click', handleCancel);
            modal.removeEventListener('click', handleModalClick);
            document.removeEventListener('keydown', handleKeyDown);
        };
        
        // Manejadores
        const handleOk = () => {
            modal.style.display = 'none';
            cleanup();
            resolve(true);
        };
        
        const handleCancel = () => {
            modal.style.display = 'none';
            cleanup();
            resolve(false);
        };
        
        // Agregar event listeners
        okBtn.addEventListener('click', handleOk);
        cancelBtn.addEventListener('click', handleCancel);
        modal.addEventListener('click', handleModalClick);
        document.addEventListener('keydown', handleKeyDown);
    });
}

// Función helper para mostrar alertas simples (sin cancelar)
function showAlert(options) {
    const modal = document.getElementById('confirmModal');
    const icon = document.getElementById('confirmIcon');
    const title = document.getElementById('confirmTitle');
    const message = document.getElementById('confirmMessage');
    const okBtn = document.getElementById('confirmOkBtn');
    const cancelBtn = document.getElementById('confirmCancelBtn');
    
    // Tipos de alerta
    const icons = {
        success: '<i class="fas fa-check-circle" style="color: #10b981;"></i>',
        error: '<i class="fas fa-times-circle" style="color: #ef4444;"></i>',
        info: '<i class="fas fa-info-circle" style="color: #60a5fa;"></i>',
        warning: '<i class="fas fa-exclamation-triangle" style="color: #f59e0b;"></i>'
    };
    
    icon.innerHTML = icons[options.type || 'info'];
    title.textContent = options.title || 'Información';
    message.textContent = options.message || '';
    
    okBtn.className = 'btn-primary';
    okBtn.innerHTML = '<i class="fas fa-check"></i> OK';
    okBtn.style.display = 'flex';
    cancelBtn.style.display = 'none';
    
    modal.style.display = 'flex';
    
    const handleOk = () => {
        modal.style.display = 'none';
        okBtn.removeEventListener('click', handleOk);
        cancelBtn.style.display = 'flex';
    };
    
    okBtn.addEventListener('click', handleOk);
}

// ========================
//  DOCKER IMAGE
// ========================
async function checkDockerImageStatus() {
    try {
        const res = await fetch('/api/docker-image/status');
        const data = await res.json();
        
        const statusBadge = document.getElementById('dockerImageStatus');
        const statusText = document.getElementById('dockerImageText');
        
        if (data.exists) {
            statusText.textContent = 'Imagen OK';
            statusBadge.style.borderColor = '#10b981';
            statusBadge.querySelector('i').style.color = '#10b981';
        } else {
            statusText.textContent = 'Sin imagen';
            statusBadge.style.borderColor = '#f59e0b';
            statusBadge.querySelector('i').style.color = '#f59e0b';
        }
    } catch (error) {
        console.error('Error al verificar imagen Docker:', error);
        document.getElementById('dockerImageText').textContent = 'Error';
    }
}

async function openDockerImageModal() {
    const modal = document.getElementById('dockerImageModal');
    const body = document.getElementById('dockerImageModalBody');
    const footer = document.getElementById('dockerImageModalFooter');
    
    modal.style.display = 'flex';
    
    body.innerHTML = '<div style="text-align: center; padding: 40px; color: #6b7280;"><i class="fas fa-spinner fa-pulse"></i><br/><br/>Verificando...</div>';
    footer.innerHTML = '';
    
    try {
        const res = await fetch('/api/docker-image/status');
        const data = await res.json();
        
        if (data.exists) {
            const info = data.info;
            body.innerHTML = `
                <div style="padding: 20px;">
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #10b981; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                            <i class="fas fa-check-circle"></i>
                            Imagen disponible
                        </h4>
                        <p style="color: #9ca3af; font-size: 0.9rem;">La imagen Docker de Terraform está lista para usar</p>
                    </div>
                    
                    <div style="background: #1a1a1a; border: 1px solid #2a2a2a; padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 0.85rem;">
                        <div style="margin-bottom: 8px; color: #9ca3af;">
                            <span style="color: #6b7280;">Nombre:</span> 
                            <span style="color: #f5f5f5;">${data.image_name}</span>
                        </div>
                        <div style="margin-bottom: 8px; color: #9ca3af;">
                            <span style="color: #6b7280;">ID:</span> 
                            <span style="color: #f5f5f5;">${info.short_id}</span>
                        </div>
                        <div style="margin-bottom: 8px; color: #9ca3af;">
                            <span style="color: #6b7280;">Tamaño:</span> 
                            <span style="color: #f5f5f5;">${info.size_mb} MB</span>
                        </div>
                        <div style="color: #9ca3af;">
                            <span style="color: #6b7280;">Creada:</span> 
                            <span style="color: #f5f5f5;">${new Date(info.created).toLocaleString('es-ES')}</span>
                        </div>
                    </div>
                </div>
            `;
            
            footer.innerHTML = `
                <button class="btn-primary" onclick="showAvailableImages()" style="margin-right: auto;">
                    <i class="fas fa-list"></i> Ver Imágenes
                </button>
                <button class="btn-delete" onclick="rebuildDockerImage()">
                    <i class="fas fa-sync"></i> Reconstruir
                </button>
                <button class="btn-delete" onclick="deleteDockerImage()">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            `;
        } else {
            body.innerHTML = `
                <div style="padding: 20px;">
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #f59e0b; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                            <i class="fas fa-exclamation-triangle"></i>
                            Imagen no encontrada
                        </h4>
                        <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 15px;">
                            La imagen Docker de Terraform no está disponible. Es necesaria para ejecutar jobs.
                        </p>
                        ${data.dockerfile_found ? `
                            <p style="color: #9ca3af; font-size: 0.85rem;">
                                <i class="fas fa-file-code"></i> Dockerfile encontrado en:<br/>
                                <code style="color: #f5f5f5; font-size: 0.8rem;">${data.dockerfile_path}</code>
                            </p>
                        ` : `
                            <p style="color: #ef4444; font-size: 0.85rem;">
                                <i class="fas fa-times-circle"></i> No se encontró el Dockerfile
                            </p>
                        `}
                    </div>
                </div>
            `;
            
            footer.innerHTML = `
                <button class="btn-primary" onclick="showAvailableImages()" style="margin-right: auto;">
                    <i class="fas fa-list"></i> Usar Imagen Existente
                </button>
                <button class="btn-primary" onclick="buildDockerImage()">
                    <i class="fas fa-hammer"></i> Construir Imagen
                </button>
                <button class="btn-secondary" onclick="buildDockerImageCustom()">
                    <i class="fas fa-code"></i> Con Dockerfile Custom
                </button>
            `;
        }
    } catch (error) {
        body.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #ef4444;">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>Error al verificar imagen</p>
                <p style="font-size: 0.85rem; margin-top: 8px; color: #9ca3af;">${error.message}</p>
            </div>
        `;
    }
}

function closeDockerImageModal() {
    document.getElementById('dockerImageModal').style.display = 'none';
}

async function buildDockerImage(dockerfileContent = null) {
    const body = document.getElementById('dockerImageModalBody');
    const footer = document.getElementById('dockerImageModalFooter');
    
    body.innerHTML = `
        <div style="padding: 20px;">
            <div style="text-align: center; margin-bottom: 20px; color: #60a5fa;">
                <i class="fas fa-hammer fa-2x" style="margin-bottom: 10px;"></i>
                <h4 style="margin-bottom: 5px;">Construyendo imagen...</h4>
                <p style="font-size: 0.85rem; color: #9ca3af;">Esto puede tomar algunos minutos</p>
            </div>
            <div id="buildLogs" style="background: #0d0d0d; border: 1px solid #2a2a2a; padding: 15px; border-radius: 4px; max-height: 300px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 0.8rem; color: #e0e0e0;">
                <div style="color: #6b7280;"><i class="fas fa-spinner fa-pulse"></i> Iniciando construcción...</div>
            </div>
        </div>
    `;
    footer.innerHTML = '';
    
    try {
        const requestBody = dockerfileContent ? { dockerfile_content: dockerfileContent } : {};
        const res = await fetch('/api/docker-image/build', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        const data = await res.json();
        
        if (data.status === 'success' || data.status === 'already_exists') {
            body.innerHTML = `
                <div style="padding: 40px; text-align: center; color: #10b981;">
                    <i class="fas fa-check-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                    <h4 style="margin-bottom: 10px;">¡Imagen construida exitosamente!</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af;">${data.message}</p>
                </div>
            `;
            
            footer.innerHTML = `
                <button class="btn-primary" onclick="closeDockerImageModal(); checkDockerImageStatus();" style="width: 100%;">
                    <i class="fas fa-check"></i> Cerrar
                </button>
            `;
            
            // Actualizar estado en el header
            setTimeout(() => checkDockerImageStatus(), 500);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        body.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #ef4444;">
                <i class="fas fa-times-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                <h4 style="margin-bottom: 10px;">Error al construir imagen</h4>
                <p style="font-size: 0.9rem; color: #9ca3af;">${error.message}</p>
            </div>
        `;
        
        footer.innerHTML = `
            <button class="btn-primary" onclick="closeDockerImageModal();" style="width: 100%;">
                Cerrar
            </button>
        `;
    }
}

async function buildDockerImageCustom() {
    const body = document.getElementById('dockerImageModalBody');
    const footer = document.getElementById('dockerImageModalFooter');
    
    const defaultDockerfile = `FROM hashicorp/terraform:latest

# Instalar herramientas adicionales
RUN apk add --no-cache git openssh-client

# Configurar SSH
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

WORKDIR /workspace
`;
    
    body.innerHTML = `
        <div style="padding: 20px;">
            <h4 style="color: #f5f5f5; margin-bottom: 15px;">
                <i class="fas fa-code"></i> Dockerfile Personalizado
            </h4>
            <p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 15px;">
                Define tu propio Dockerfile para construir la imagen de Terraform:
            </p>
            <textarea 
                id="customDockerfileContent" 
                style="width: 100%; height: 300px; background: #0d0d0d; color: #f5f5f5; border: 1px solid #2a2a2a; padding: 15px; font-family: 'Courier New', monospace; font-size: 0.85rem; resize: vertical;"
                placeholder="Escribe tu Dockerfile aquí..."
            >${defaultDockerfile}</textarea>
        </div>
    `;
    
    footer.innerHTML = `
        <button class="btn-secondary" onclick="openDockerImageModal()">
            <i class="fas fa-arrow-left"></i> Volver
        </button>
        <button class="btn-primary" onclick="buildFromCustomDockerfile()">
            <i class="fas fa-hammer"></i> Construir
        </button>
    `;
}

async function buildFromCustomDockerfile() {
    const dockerfileContent = document.getElementById('customDockerfileContent')?.value.trim();
    
    if (!dockerfileContent) {
        showAlert({
            type: 'warning',
            title: 'Contenido Vacío',
            message: 'Debes proporcionar el contenido del Dockerfile'
        });
        return;
    }
    
    await buildDockerImage(dockerfileContent);
}

async function rebuildDockerImage() {
    const confirmed = await showConfirm({
        type: 'warning',
        title: 'Reconstruir Imagen',
        message: '¿Reconstruir la imagen? Se eliminará la actual y se creará una nueva.',
        confirmText: 'Reconstruir',
        cancelText: 'Cancelar'
    });
    
    if (!confirmed) {
        return;
    }
    
    const body = document.getElementById('dockerImageModalBody');
    const footer = document.getElementById('dockerImageModalFooter');
    
    body.innerHTML = `
        <div style="padding: 20px;">
            <div style="text-align: center; margin-bottom: 20px; color: #60a5fa;">
                <i class="fas fa-sync fa-spin fa-2x" style="margin-bottom: 10px;"></i>
                <h4 style="margin-bottom: 5px;">Reconstruyendo imagen...</h4>
                <p style="font-size: 0.85rem; color: #9ca3af;">Esto puede tomar algunos minutos</p>
            </div>
        </div>
    `;
    footer.innerHTML = '';
    
    try {
        const res = await fetch('/api/docker-image/rebuild?force=true', { method: 'POST' });
        const data = await res.json();
        
        if (data.status === 'success') {
            body.innerHTML = `
                <div style="padding: 40px; text-align: center; color: #10b981;">
                    <i class="fas fa-check-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                    <h4 style="margin-bottom: 10px;">¡Imagen reconstruida!</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af;">${data.message}</p>
                </div>
            `;
            
            footer.innerHTML = `
                <button class="btn-primary" onclick="closeDockerImageModal(); checkDockerImageStatus();" style="width: 100%;">
                    <i class="fas fa-check"></i> Cerrar
                </button>
            `;
            
            setTimeout(() => checkDockerImageStatus(), 500);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        body.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #ef4444;">
                <i class="fas fa-times-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                <h4 style="margin-bottom: 10px;">Error</h4>
                <p style="font-size: 0.9rem; color: #9ca3af;">${error.message}</p>
            </div>
        `;
        
        footer.innerHTML = `
            <button class="btn-primary" onclick="closeDockerImageModal();" style="width: 100%;">
                Cerrar
            </button>
        `;
    }
}

async function deleteDockerImage() {
    const confirmed = await showConfirm({
        type: 'warning',
        title: 'Eliminar Imagen',
        message: '¿Eliminar la imagen Docker? Deberás reconstruirla para ejecutar jobs.',
        confirmText: 'Eliminar',
        cancelText: 'Cancelar'
    });
    
    if (!confirmed) {
        return;
    }
    
    try {
        const res = await fetch('/api/docker-image/', { method: 'DELETE' });
        const data = await res.json();
        
        if (data.status === 'success') {
            showAlert({
                type: 'success',
                title: 'Imagen Eliminada',
                message: 'Imagen eliminada exitosamente'
            });
            closeDockerImageModal();
            checkDockerImageStatus();
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        showAlert({
            type: 'error',
            title: 'Error',
            message: error.message
        });
    }
}

async function showAvailableImages() {
    const body = document.getElementById('dockerImageModalBody');
    const footer = document.getElementById('dockerImageModalFooter');
    
    body.innerHTML = '<div style="text-align: center; padding: 40px; color: #6b7280;"><i class="fas fa-spinner fa-pulse"></i><br/><br/>Cargando imágenes...</div>';
    footer.innerHTML = '';
    
    try {
        const res = await fetch('/api/docker-image/list');
        const data = await res.json();
        
        if (data.images.length === 0) {
            body.innerHTML = `
                <div style="padding: 40px; text-align: center; color: #6b7280;">
                    <i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 10px; opacity: 0.3;"></i>
                    <p>No hay imágenes Docker disponibles</p>
                </div>
            `;
            
            footer.innerHTML = `
                <button class="btn-primary" onclick="openDockerImageModal()" style="width: 100%;">
                    <i class="fas fa-arrow-left"></i> Volver
                </button>
            `;
            return;
        }
        
        const imagesList = data.images.map(img => {
            const isSelected = img.tag === data.selected_image;
            const isDefault = img.tag === data.default_image;
            
            return `
                <div class="path-item ${isSelected ? 'folder' : ''}" 
                     style="display: flex; align-items: center; padding: 12px 15px; border: 1px solid ${isSelected ? '#4ade80' : '#2a2a2a'}; margin-bottom: 8px; cursor: pointer; background: ${isSelected ? 'rgba(74, 222, 128, 0.05)' : 'transparent'};"
                     onclick="selectDockerImage('${img.tag}')">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                            <i class="fab fa-docker" style="color: ${isSelected ? '#4ade80' : '#60a5fa'};"></i>
                            <span style="font-family: 'Courier New', monospace; color: #f5f5f5; font-size: 0.9rem;">${img.tag}</span>
                            ${isSelected ? '<span style="color: #4ade80; font-size: 0.75rem; padding: 2px 8px; background: rgba(74, 222, 128, 0.1); border-radius: 3px;">SELECCIONADA</span>' : ''}
                            ${isDefault && !isSelected ? '<span style="color: #60a5fa; font-size: 0.75rem; padding: 2px 8px; background: rgba(96, 165, 250, 0.1); border-radius: 3px;">DEFAULT</span>' : ''}
                        </div>
                        <div style="display: flex; gap: 20px; font-size: 0.8rem; color: #9ca3af;">
                            <span><i class="fas fa-fingerprint"></i> ${img.id}</span>
                            <span><i class="fas fa-hdd"></i> ${img.size_mb} MB</span>
                            <span><i class="fas fa-calendar"></i> ${new Date(img.created).toLocaleDateString('es-ES')}</span>
                        </div>
                    </div>
                    ${isSelected ? '<i class="fas fa-check-circle" style="color: #4ade80; font-size: 1.2rem;"></i>' : '<i class="fas fa-arrow-right" style="color: #6b7280;"></i>'}
                </div>
            `;
        }).join('');
        
        body.innerHTML = `
            <div style="padding: 20px;">
                <h4 style="color: #f5f5f5; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-images"></i>
                    Imágenes Docker Disponibles (${data.images.length})
                </h4>
                <p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 20px;">
                    Selecciona una imagen existente para usar en tus jobs de Terraform
                </p>
                <div style="max-height: 400px; overflow-y: auto;">
                    ${imagesList}
                </div>
            </div>
        `;
        
        footer.innerHTML = `
            <button class="btn-primary" onclick="openDockerImageModal()" style="width: 100%;">
                <i class="fas fa-arrow-left"></i> Volver
            </button>
        `;
    } catch (error) {
        body.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #ef4444;">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>Error al cargar imágenes</p>
                <p style="font-size: 0.85rem; margin-top: 8px; color: #9ca3af;">${error.message}</p>
            </div>
        `;
        
        footer.innerHTML = `
            <button class="btn-primary" onclick="openDockerImageModal()" style="width: 100%;">
                <i class="fas fa-arrow-left"></i> Volver
            </button>
        `;
    }
}

async function selectDockerImage(imageName) {
    try {
        const res = await fetch('/api/docker-image/select', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_name: imageName })
        });
        
        const data = await res.json();
        
        if (data.status === 'success') {
            // Mostrar confirmación y recargar
            const body = document.getElementById('dockerImageModalBody');
            body.innerHTML = `
                <div style="padding: 40px; text-align: center; color: #10b981;">
                    <i class="fas fa-check-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                    <h4 style="margin-bottom: 10px;">¡Imagen seleccionada!</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af;">${data.message}</p>
                    <p style="font-family: 'Courier New', monospace; color: #f5f5f5; margin-top: 10px; font-size: 0.85rem;">${imageName}</p>
                </div>
            `;
            
            const footer = document.getElementById('dockerImageModalFooter');
            footer.innerHTML = `
                <button class="btn-primary" onclick="closeDockerImageModal(); checkDockerImageStatus();" style="width: 100%;">
                    <i class="fas fa-check"></i> Cerrar
                </button>
            `;
            
            // Actualizar estado en el header
            setTimeout(() => checkDockerImageStatus(), 500);
        } else {
            throw new Error(data.message || 'Error al seleccionar imagen');
        }
    } catch (error) {
        showAlert({
            type: 'error',
            title: 'Error',
            message: error.message
        });
    }
}

// ========================
//  PATH BROWSER
// ========================
let currentBrowsePath = '.';

async function openPathBrowser() {
    console.log('openPathBrowser llamado');
    const modal = document.getElementById('pathBrowserModal');
    const manualInput = document.getElementById('manualPathInput');
    
    // Si hay un path en el input, usarlo; si no, obtener el directorio del proyecto
    let currentPath = document.getElementById('modulePath').value.trim();
    if (!currentPath) {
        // Obtener el directorio del proyecto desde el servidor
        try {
            const res = await fetch('/api/filesystem/project-dir');
            if (res.ok) {
                const data = await res.json();
                currentPath = data.project_dir;
            } else {
                currentPath = '.';
            }
        } catch (error) {
            console.error('Error al obtener directorio del proyecto:', error);
            currentPath = '.';
        }
    }
    
    console.log('Modal element:', modal);
    console.log('Current path:', currentPath);
    
    if (!modal) {
        console.error('No se encontró el modal pathBrowserModal');
        showAlert({
            type: 'error',
            title: 'Error',
            message: 'No se pudo abrir el explorador de archivos'
        });
        return;
    }
    
    currentBrowsePath = currentPath;
    manualInput.value = currentPath;
    
    modal.style.display = 'flex';
    console.log('Modal display set to flex');
    
    await loadPathList(currentBrowsePath);
}

function closePathBrowser() {
    document.getElementById('pathBrowserModal').style.display = 'none';
}

async function loadPathList(path) {
    const pathList = document.getElementById('pathList');
    const breadcrumb = document.getElementById('pathBreadcrumb');
    
    pathList.innerHTML = '<div style="text-align: center; padding: 40px; color: #6b7280;"><i class="fas fa-spinner fa-spin"></i> Cargando...</div>';
    
    try {
        const res = await fetch(`/api/filesystem/list?path=${encodeURIComponent(path)}`);
        
        if (!res.ok) {
            throw new Error('No se pudo listar el directorio');
        }
        
        const data = await res.json();
        
        // Actualizar breadcrumb - normalizar el path para Windows
        const normalizedPath = path.replace(/\\/g, '/');
        const isAbsolutePath = /^[a-zA-Z]:/.test(normalizedPath) || normalizedPath.startsWith('/');
        
        if (isAbsolutePath) {
            // Path absoluto (ej: C:/Users/... o d:/proyecto)
            const pathParts = normalizedPath.split('/').filter(p => p);
            breadcrumb.innerHTML = pathParts.map((part, idx) => {
                const partPath = pathParts.slice(0, idx + 1).join('/');
                const isFirst = idx === 0;
                return `${isFirst ? '' : '<span style="color: #4a4a4a;">/</span>'}<span onclick="navigateTo('${partPath}')" style="cursor: pointer;">${part}</span>`;
            }).join('');
        } else {
            // Path relativo
            const pathParts = normalizedPath.split('/').filter(p => p && p !== '.');
            breadcrumb.innerHTML = `
                <span onclick="navigateTo('.')" style="color: #6b7280; cursor: pointer;"><i class="fas fa-folder"></i> Proyecto</span>
                ${pathParts.map((part, idx) => {
                    const partPath = './' + pathParts.slice(0, idx + 1).join('/');
                    return `<span style="color: #4a4a4a;">/</span><span onclick="navigateTo('${partPath}')" style="cursor: pointer;">${part}</span>`;
                }).join('')}
            `;
        }
        
        // Limpiar lista
        pathList.innerHTML = '';
        
        // Botón para volver atrás (usar el parent del servidor)
        if (data.parent) {
            const parentItem = document.createElement('div');
            parentItem.className = 'path-item parent';
            parentItem.onclick = () => navigateTo(data.parent);
            parentItem.innerHTML = `
                <i class="fas fa-level-up-alt"></i>
                <span>..</span>
            `;
            pathList.appendChild(parentItem);
        }
        
        // Listar directorios
        if (data.directories && data.directories.length > 0) {
            data.directories.forEach(dir => {
                const item = document.createElement('div');
                item.className = 'path-item folder';
                // Usar el path normalizado del servidor para construir la nueva ruta
                const basePath = data.normalized_path || data.path;
                const newPath = `${basePath}/${dir}`;
                item.onclick = () => navigateTo(newPath);
                item.innerHTML = `
                    <i class="fas fa-folder"></i>
                    <span>${dir}</span>
                `;
                pathList.appendChild(item);
            });
        }
        
        // Mensaje si está vacío
        if (pathList.children.length === 0 || (pathList.children.length === 1 && pathList.children[0].classList.contains('parent'))) {
            const emptyMsg = document.createElement('div');
            emptyMsg.style.cssText = 'text-align: center; padding: 40px; color: #6b7280;';
            emptyMsg.innerHTML = '<i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 10px; opacity: 0.3;"></i><p>No hay subdirectorios</p>';
            pathList.appendChild(emptyMsg);
        }
        
        // Actualizar input manual
        document.getElementById('manualPathInput').value = path;
        
    } catch (error) {
        pathList.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #ef4444;">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>Error al listar directorio</p>
                <p style="font-size: 0.85rem; margin-top: 8px; color: #9ca3af;">${error.message}</p>
            </div>
        `;
    }
}

async function navigateTo(path) {
    currentBrowsePath = path;
    await loadPathList(path);
}

function selectPath() {
    const manualInput = document.getElementById('manualPathInput');
    const selectedPath = manualInput.value.trim() || currentBrowsePath;
    
    document.getElementById('modulePath').value = selectedPath;
    closePathBrowser();
}

// Inicializar eventos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Loaded');
    
    // Verificar que los elementos del path browser existen
    const browseBtn = document.getElementById('browsePathBtn');
    const pathModal = document.getElementById('pathBrowserModal');
    console.log('Browse button:', browseBtn);
    console.log('Path modal:', pathModal);
    
    // Botones principales
    document.getElementById('runJobBtn')?.addEventListener('click', runJob);
    document.getElementById('closeOutputBtn')?.addEventListener('click', closeOutput);
    document.getElementById('deleteAllBtn')?.addEventListener('click', deleteAllJobs);
    document.getElementById('refreshJobsBtn')?.addEventListener('click', loadJobs);
    document.getElementById('closeFileViewerBtn')?.addEventListener('click', closeFileViewer);
    
    // Path browser
    if (browseBtn) {
        browseBtn.addEventListener('click', function() {
            console.log('Browse button clicked!');
            openPathBrowser();
        });
    } else {
        console.error('No se encontró el botón browsePathBtn');
    }
    
    document.getElementById('closePathBrowserBtn')?.addEventListener('click', closePathBrowser);
    document.getElementById('selectPathBtn')?.addEventListener('click', selectPath);
    
    // Configuración modal
    document.getElementById('configBtn')?.addEventListener('click', openConfig);
    document.getElementById('closeConfigBtn')?.addEventListener('click', closeConfig);
    document.getElementById('saveConfigBtn')?.addEventListener('click', saveConfig);
    document.getElementById('enableSSH')?.addEventListener('change', toggleSSHOptions);
    
    // Cerrar modales al hacer click fuera
    document.getElementById('pathBrowserModal')?.addEventListener('click', function(e) {
        if (e.target === this) {
            closePathBrowser();
        }
    });
    
    document.getElementById('configModal')?.addEventListener('click', function(e) {
        if (e.target === this) {
            closeConfig();
        }
    });
    
    // Docker image modal
    document.getElementById('dockerImageStatus')?.addEventListener('click', openDockerImageModal);
    document.getElementById('closeDockerImageModalBtn')?.addEventListener('click', closeDockerImageModal);
    
    document.getElementById('dockerImageModal')?.addEventListener('click', function(e) {
        if (e.target === this) {
            closeDockerImageModal();
        }
    });
    
    // Actualizar indicador de configuración
    updateConfigIndicator();
    
    // Verificar estado de imagen Docker
    checkDockerImageStatus();
    
    // Cargar jobs automáticamente al entrar
    loadJobs();
});

// Exponer funciones al ámbito global para los handlers dinámicos
window.deleteJob = deleteJob;
window.deleteCurrentJob = deleteCurrentJob;
window.loadJobs = loadJobs;
window.openFolder = openFolder;
window.loadFile = loadFile;
window.navigateTo = navigateTo;
window.buildDockerImage = buildDockerImage;
window.buildDockerImageCustom = buildDockerImageCustom;
window.buildFromCustomDockerfile = buildFromCustomDockerfile;
window.rebuildDockerImage = rebuildDockerImage;
window.deleteDockerImage = deleteDockerImage;
window.showAvailableImages = showAvailableImages;
window.selectDockerImage = selectDockerImage;
