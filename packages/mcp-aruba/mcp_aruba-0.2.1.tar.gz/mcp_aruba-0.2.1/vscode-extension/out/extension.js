"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const keytar = __importStar(require("keytar"));
const SERVICE_NAME = 'mcp-aruba-email';
const ACCOUNT_NAME = 'email-password';
async function activate(context) {
    console.log('MCP Aruba Email extension is activating...');
    const didChangeEmitter = new vscode.EventEmitter();
    // Register the configure command
    context.subscriptions.push(vscode.commands.registerCommand('mcp-aruba-email.configure', async () => {
        await configureCredentials(context);
        didChangeEmitter.fire();
    }));
    // Register the test connection command
    context.subscriptions.push(vscode.commands.registerCommand('mcp-aruba-email.testConnection', async () => {
        await testConnection(context);
    }));
    // Register MCP Server Definition Provider
    context.subscriptions.push(vscode.lm.registerMcpServerDefinitionProvider('aruba-email', {
        onDidChangeMcpServerDefinitions: didChangeEmitter.event,
        provideMcpServerDefinitions: async () => {
            return await getMcpServerDefinitions(context);
        }
    }));
    // Check if credentials are configured
    const config = vscode.workspace.getConfiguration('mcpArubaEmail');
    const emailAddress = config.get('emailAddress');
    if (!emailAddress) {
        const action = await vscode.window.showInformationMessage('Aruba Email MCP Server: Credentials not configured. Configure now?', 'Configure', 'Later');
        if (action === 'Configure') {
            await configureCredentials(context);
            didChangeEmitter.fire();
        }
    }
    console.log('MCP Aruba Email extension activated successfully!');
}
async function configureCredentials(context) {
    const config = vscode.workspace.getConfiguration('mcpArubaEmail');
    // Get email address
    const currentEmail = config.get('emailAddress') || '';
    const emailAddress = await vscode.window.showInputBox({
        prompt: 'Enter your Aruba email address',
        value: currentEmail,
        placeHolder: 'user@aruba.it',
        validateInput: (value) => {
            if (!value || !value.includes('@')) {
                return 'Please enter a valid email address';
            }
            return null;
        }
    });
    if (!emailAddress) {
        return;
    }
    // Get password
    const password = await vscode.window.showInputBox({
        prompt: 'Enter your Aruba email password',
        password: true,
        placeHolder: 'Your password (stored securely)',
        validateInput: (value) => {
            if (!value || value.length < 1) {
                return 'Password is required';
            }
            return null;
        }
    });
    if (!password) {
        return;
    }
    // Optional: Imgur Client ID for signature photos
    const imgurClientId = await vscode.window.showInputBox({
        prompt: 'Enter Imgur Client ID (optional, for signature photos)',
        placeHolder: 'Leave empty to skip',
        ignoreFocusOut: true
    });
    // Save settings
    await config.update('emailAddress', emailAddress, vscode.ConfigurationTarget.Global);
    // Auto-generate CalDAV URL
    const caldavUrl = `https://syncdav.aruba.it/calendars/${emailAddress}/`;
    await config.update('caldavUrl', caldavUrl, vscode.ConfigurationTarget.Global);
    // Store password securely using keytar
    try {
        await keytar.setPassword(SERVICE_NAME, ACCOUNT_NAME, password);
        if (imgurClientId) {
            await keytar.setPassword(SERVICE_NAME, 'imgur-client-id', imgurClientId);
        }
        vscode.window.showInformationMessage('Aruba Email credentials saved successfully!');
    }
    catch (error) {
        vscode.window.showErrorMessage(`Failed to save password: ${error}`);
    }
}
async function testConnection(context) {
    const config = vscode.workspace.getConfiguration('mcpArubaEmail');
    const emailAddress = config.get('emailAddress');
    if (!emailAddress) {
        vscode.window.showWarningMessage('Please configure credentials first.');
        return;
    }
    const password = await keytar.getPassword(SERVICE_NAME, ACCOUNT_NAME);
    if (!password) {
        vscode.window.showWarningMessage('Password not found. Please configure credentials.');
        return;
    }
    vscode.window.showInformationMessage(`Testing connection for ${emailAddress}...`);
    // The actual test would be done by the Python server
    // Here we just verify the credentials exist
    vscode.window.showInformationMessage('Credentials configured. Use MCP tools to test the connection.');
}
async function getMcpServerDefinitions(context) {
    const config = vscode.workspace.getConfiguration('mcpArubaEmail');
    const emailAddress = config.get('emailAddress');
    if (!emailAddress) {
        console.log('Aruba Email: No email configured, skipping MCP server');
        return [];
    }
    const password = await keytar.getPassword(SERVICE_NAME, ACCOUNT_NAME);
    if (!password) {
        console.log('Aruba Email: No password stored, skipping MCP server');
        return [];
    }
    const imapHost = config.get('imapHost') || 'imaps.aruba.it';
    const imapPort = config.get('imapPort') || 993;
    const smtpHost = config.get('smtpHost') || 'smtps.aruba.it';
    const smtpPort = config.get('smtpPort') || 465;
    const caldavUrl = config.get('caldavUrl') || `https://syncdav.aruba.it/calendars/${emailAddress}/`;
    const calendarEnabled = config.get('calendarEnabled') ?? true;
    // Get optional Imgur client ID
    const imgurClientId = await keytar.getPassword(SERVICE_NAME, 'imgur-client-id') || '';
    // Environment variables for the Python server
    const env = {
        'IMAP_HOST': imapHost,
        'IMAP_PORT': String(imapPort),
        'IMAP_USER': emailAddress,
        'IMAP_PASSWORD': password,
        'SMTP_HOST': smtpHost,
        'SMTP_PORT': String(smtpPort),
        'SMTP_USER': emailAddress,
        'SMTP_PASSWORD': password,
        'CALDAV_URL': calendarEnabled ? caldavUrl : '',
        'CALDAV_USER': calendarEnabled ? emailAddress : '',
        'CALDAV_PASSWORD': calendarEnabled ? password : '',
    };
    if (imgurClientId) {
        env['IMGUR_CLIENT_ID'] = imgurClientId;
    }
    // Use uvx to run the Python MCP server from PyPI
    const serverDefinition = new vscode.McpStdioServerDefinition('Aruba Email', 'uvx', ['mcp-aruba'], env);
    return [serverDefinition];
}
function deactivate() {
    console.log('MCP Aruba Email extension deactivated');
}
//# sourceMappingURL=extension.js.map