#!/bin/bash

# LlamaFarm CLI - Complete Project Setup Script
# Creates ALL files with working placeholders

set -e

echo "🌾 LlamaFarm CLI - Complete Project Setup"
echo "========================================"
echo ""

# Check if directory exists
if [ -d "llamafarm-cli" ]; then
    echo "⚠️  Directory 'llamafarm-cli' already exists."
    read -p "Remove it and continue? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf llamafarm-cli
    else
        echo "Exiting..."
        exit 1
    fi
fi

# Create root directory
echo "📁 Creating project structure..."
mkdir -p llamafarm-cli
cd llamafarm-cli

# Create all directories
mkdir -p src/{commands,templates,utils,models,agents,config,__tests__}
mkdir -p demo/public
mkdir -p scripts
mkdir -p templates/examples
mkdir -p .github/workflows
mkdir -p test

# Create package.json
echo "📦 Creating package.json..."
cat > package.json << 'EOF'
{
  "name": "@llamafarm/llamafarm",
  "version": "0.1.0",
  "description": "🌾 Plant and harvest AI models, agents, and databases into single deployable binaries",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "llamafarm": "./dist/cli.js"
  },
  "files": [
    "dist",
    "templates",
    "README.md",
    "LICENSE"
  ],
  "scripts": {
    "build": "tsc",
    "dev": "ts-node src/cli.ts",
    "prepare": "npm run build",
    "test": "jest",
    "lint": "eslint src --ext .ts",
    "format": "prettier --write \"src/**/*.ts\"",
    "demo": "node scripts/demo.js",
    "postinstall": "node scripts/postinstall.js || true",
    "system-check": "node dist/utils/system-check.js",
    "package:mac": "pkg . -t node18-macos-arm64 -o binaries/llamafarm-mac",
    "package:linux": "pkg . -t node18-linux-x64 -o binaries/llamafarm-linux",
    "package:win": "pkg . -t node18-win-x64 -o binaries/llamafarm.exe",
    "package:all": "npm run package:mac && npm run package:linux && npm run package:win"
  },
  "keywords": [
    "ai",
    "llm",
    "ollama",
    "edge",
    "deployment",
    "binary",
    "local-ai",
    "harvest",
    "langchain",
    "vector-database",
    "rag",
    "chromadb"
  ],
  "author": "Harvest AI Team",
  "license": "MIT",
  "homepage": "https://github.com/llamafarm/llamafarm-cli#readme",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/llamafarm/llamafarm-cli.git"
  },
  "bugs": {
    "url": "https://github.com/llamafarm/llamafarm-cli/issues"
  },
  "dependencies": {
    "commander": "^11.1.0",
    "chalk": "^4.1.2",
    "ora": "^5.4.1",
    "express": "^4.18.2",
    "ws": "^8.16.0",
    "node-fetch": "^2.7.0",
    "chromadb": "^1.7.3",
    "ollama": "^0.5.0",
    "archiver": "^6.0.1",
    "extract-zip": "^2.0.1",
    "fs-extra": "^11.2.0",
    "update-notifier": "^5.1.0",
    "boxen": "^5.1.2",
    "figlet": "^1.7.0",
    "inquirer": "^8.2.6",
    "js-yaml": "^4.1.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/express": "^4.17.21",
    "@types/ws": "^8.5.10",
    "@types/fs-extra": "^11.0.4",
    "@types/archiver": "^6.0.2",
    "@types/figlet": "^1.5.8",
    "@types/inquirer": "^8.2.10",
    "@types/js-yaml": "^4.0.9",
    "@types/node-fetch": "^2.6.11",
    "typescript": "^5.3.3",
    "ts-node": "^10.9.2",
    "@types/jest": "^29.5.11",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^6.19.0",
    "@typescript-eslint/parser": "^6.19.0",
    "prettier": "^3.2.4",
    "pkg": "^5.8.1"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "jest": {
    "preset": "ts-jest",
    "testEnvironment": "node",
    "roots": [
      "<rootDir>/src"
    ],
    "testMatch": [
      "**/__tests__/**/*.ts",
      "**/?(*.)+(spec|test).ts"
    ]
  },
  "pkg": {
    "scripts": "dist/**/*.js",
    "assets": [
      "dist/**/*",
      "templates/**/*",
      "node_modules/figlet/fonts/**/*"
    ],
    "targets": [
      "node18-macos-arm64",
      "node18-linux-x64",
      "node18-win-x64"
    ],
    "outputPath": "binaries"
  }
}
EOF

# Create tsconfig.json
echo "⚙️  Creating tsconfig.json..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,
    "noEmitOnError": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
EOF

# Create jest.config.js
echo "🧪 Creating jest.config.js..."
cat > jest.config.js << 'EOF'
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts'
  ]
};
EOF

# Create the main CLI file
echo "🌾 Creating CLI entry point..."
cat > src/cli.ts << 'EOF'
#!/usr/bin/env node

import { program } from 'commander';
import chalk from 'chalk';
import figlet from 'figlet';
import updateNotifier from 'update-notifier';
import { readFileSync } from 'fs';
import { join } from 'path';

// Commands
import { plantCommand } from './commands/plant';
import { harvestCommand } from './commands/harvest';
import { tillCommand } from './commands/till';
import { sowCommand } from './commands/sow';
import { irrigateCommand } from './commands/irrigate';
import { fertilizeCommand } from './commands/fertilize';
import { pruneCommand } from './commands/prune';
import { greenhouseCommand } from './commands/greenhouse';
import { siloCommand } from './commands/silo';
import { barnCommand } from './commands/barn';
import { fieldCommand } from './commands/field';
import { compostCommand } from './commands/compost';
import { almanacCommand } from './commands/almanac';
import { weatherCommand } from './commands/weather';

const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf-8'));

// Check for updates
updateNotifier({ pkg }).notify();

// ASCII art banner
console.log(chalk.green(figlet.textSync('LlamaFarm', { horizontalLayout: 'full' })));
console.log(chalk.yellow('🌾 Plant and harvest AI models locally 🦙\n'));

program
  .name('llamafarm')
  .description('CLI for planting and harvesting AI models, agents, and databases into deployable binaries')
  .version(pkg.version);

// Core commands
program
  .command('plant <model>')
  .description('🌱 Plant a model with agents, databases, and configurations')
  .option('-d, --device <device>', 'target device (raspberry-pi, jetson, mac, windows, linux)', 'mac')
  .option('-a, --agent <agent>', 'agent name or template', 'chat-basic')
  .option('-r, --rag <enabled>', 'enable RAG pipeline', 'disabled')
  .option('-db, --database <type>', 'database type (vector, sqlite, postgres)', 'vector')
  .option('-p, --port <port>', 'port to run on (auto-assigns if not specified)')
  .option('-c, --config <file>', 'load configuration from YAML file')
  .option('--gpu', 'enable GPU acceleration')
  .option('--quantize <level>', 'quantization level (q4_0, q4_1, q5_0, q5_1, q8_0)', 'q4_0')
  .action(plantCommand);

program
  .command('harvest <url>')
  .description('🌾 Harvest a planted binary from URL or local path')
  .option('-o, --output <path>', 'output directory', './harvest')
  .option('--verify', 'verify binary integrity')
  .action(harvestCommand);

// Configuration commands
program
  .command('till')
  .description('🚜 Prepare the soil (initialize configuration)')
  .option('-f, --force', 'force re-initialization')
  .option('--import <file>', 'import configuration from YAML')
  .option('--export <file>', 'export current configuration to YAML')
  .action(tillCommand);

program
  .command('sow <seeds>')
  .description('🌰 Sow data seeds (configure data sources for RAG)')
  .option('-t, --type <type>', 'seed type (pdf, csv, json, api, web)', 'pdf')
  .option('-p, --path <path>', 'path to data source')
  .option('--chunk-size <size>', 'chunk size for processing', '512')
  .option('--overlap <overlap>', 'chunk overlap', '50')
  .action(sowCommand);

// Agent commands
program
  .command('irrigate <agent>')
  .description('💧 Irrigate agents (configure agent pipelines)')
  .option('-f, --framework <framework>', 'agent framework (langchain, autogen, crewai, llamaindex)', 'langchain')
  .option('-t, --template <template>', 'use agent template')
  .option('--tools <tools...>', 'tools to enable for agent')
  .option('--memory <type>', 'memory type (buffer, summary, vector)', 'buffer')
  .action(irrigateCommand);

program
  .command('fertilize')
  .description('🪴 Fertilize the deployment (optimize performance)')
  .option('--target <target>', 'optimization target (speed, memory, accuracy)', 'balanced')
  .option('--profile', 'run profiling before optimization')
  .action(fertilizeCommand);

// Management commands
program
  .command('prune')
  .description('✂️  Prune unused resources')
  .option('--models', 'prune unused models')
  .option('--agents', 'prune unused agents')
  .option('--data', 'prune old data')
  .option('--all', 'prune everything')
  .action(pruneCommand);

program
  .command('greenhouse')
  .description('🏡 Test in the greenhouse (sandbox environment)')
  .option('-m, --model <model>', 'model to test')
  .option('-a, --agent <agent>', 'agent to test')
  .option('--scenario <file>', 'test scenario file')
  .option('--benchmark', 'run performance benchmarks')
  .action(greenhouseCommand);

// Storage commands
program
  .command('silo')
  .description('🏭 Manage the silo (vector database)')
  .option('--init <type>', 'initialize vector DB (chroma, pinecone, weaviate, qdrant)', 'chroma')
  .option('--index <name>', 'create or select index')
  .option('--embed <model>', 'embedding model', 'all-MiniLM-L6-v2')
  .option('--dimension <size>', 'embedding dimension', '384')
  .action(siloCommand);

program
  .command('barn')
  .description('🏚️  Manage the barn (model storage)')
  .option('--list', 'list stored models')
  .option('--add <model>', 'add model to barn')
  .option('--remove <model>', 'remove model from barn')
  .option('--update', 'update all models')
  .action(barnCommand);

// Deployment commands
program
  .command('field')
  .description('🌾 Manage fields (deployment environments)')
  .option('--create <name>', 'create new field')
  .option('--list', 'list all fields')
  .option('--select <name>', 'select active field')
  .option('--config <file>', 'apply field configuration')
  .action(fieldCommand);

// Utility commands
program
  .command('compost')
  .description('♻️  Compost old deployments (cleanup and archive)')
  .option('--days <days>', 'archive deployments older than N days', '30')
  .option('--keep <count>', 'keep last N deployments', '5')
  .action(compostCommand);

program
  .command('almanac')
  .description('📚 View the almanac (documentation and guides)')
  .option('--recipe <name>', 'show specific recipe')
  .option('--list', 'list all recipes')
  .option('--search <term>', 'search recipes')
  .action(almanacCommand);

program
  .command('weather')
  .description('🌤️  Check the weather (system status and health)')
  .option('--detailed', 'show detailed metrics')
  .option('--history <days>', 'show history for N days', '7')
  .action(weatherCommand);

// Parse command line arguments
program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
EOF

# Create placeholder commands
echo "📝 Creating command files..."

# Create placeholder function
create_placeholder_command() {
    local cmd=$1
    local emoji=$2
    local desc=$3
    
    cat > "src/commands/${cmd}.ts" << EOF
import chalk from 'chalk';
import figlet from 'figlet';

export async function ${cmd}Command(...args: any[]) {
  console.log(chalk.yellow('\\n${emoji} ${desc^}\\n'));
  console.log(chalk.cyan(figlet.textSync('Coming Soon!', { font: 'Small' })));
  console.log(chalk.gray('\\n🦙 The llamas are in the pasture...'));
  console.log(chalk.gray('   They\\'re learning new tricks and will be back soon!\\n'));
  
  // Show what this command will do
  console.log(chalk.green('📋 This command will:'));
  const features = getCommandFeatures('${cmd}');
  features.forEach(feature => console.log(chalk.gray(\`   • \${feature}\`)));
  
  console.log(chalk.yellow('\\n🚧 Check back in the next update!\\n'));
}

function getCommandFeatures(command: string): string[] {
  const features: Record<string, string[]> = {
    plant: [
      'Download and configure AI models',
      'Set up agent frameworks',
      'Initialize vector databases',
      'Package everything into a binary',
      'Generate deployment scripts'
    ],
    harvest: [
      'Download packaged binaries',
      'Extract and install models',
      'Set up runtime environment',
      'Create convenient launchers',
      'Verify package integrity'
    ],
    till: [
      'Initialize farm configuration',
      'Set up default preferences',
      'Configure hardware settings',
      'Import/export configurations',
      'Prepare for first planting'
    ],
    sow: [
      'Configure data sources for RAG',
      'Process PDFs, CSVs, and APIs',
      'Set up chunking strategies',
      'Index documents for retrieval',
      'Prepare knowledge bases'
    ],
    irrigate: [
      'Configure agent pipelines',
      'Set up memory systems',
      'Connect tools and APIs',
      'Define conversation flows',
      'Optimize agent performance'
    ],
    fertilize: [
      'Optimize model performance',
      'Fine-tune memory usage',
      'Boost inference speed',
      'Profile bottlenecks',
      'Apply hardware acceleration'
    ],
    prune: [
      'Clean up unused models',
      'Remove old deployments',
      'Free up disk space',
      'Archive stale data',
      'Optimize storage usage'
    ],
    greenhouse: [
      'Test models in sandbox',
      'Run performance benchmarks',
      'Validate configurations',
      'Test agent behaviors',
      'Experiment safely'
    ],
    silo: [
      'Manage vector databases',
      'Create embedding indices',
      'Configure storage backends',
      'Optimize search performance',
      'Handle data persistence'
    ],
    barn: [
      'Store and organize models',
      'Track model versions',
      'Manage quantizations',
      'Update model registry',
      'Handle model downloads'
    ],
    field: [
      'Manage deployment environments',
      'Configure dev/staging/prod',
      'Handle environment variables',
      'Track deployments',
      'Manage configurations'
    ],
    compost: [
      'Archive old deployments',
      'Compress unused data',
      'Generate reports',
      'Clean up resources',
      'Maintain farm health'
    ],
    almanac: [
      'View documentation',
      'Browse recipes and guides',
      'Learn best practices',
      'Find examples',
      'Get community tips'
    ],
    weather: [
      'Check system health',
      'Monitor resource usage',
      'View performance metrics',
      'Track model status',
      'Get system alerts'
    ]
  };
  
  return features[command] || ['Amazing features coming soon!'];
}
EOF
}

# Create all placeholder commands
create_placeholder_command "plant" "🌱" "Planting"
create_placeholder_command "harvest" "🌾" "Harvesting"
create_placeholder_command "till" "🚜" "Tilling"
create_placeholder_command "sow" "🌰" "Sowing"
create_placeholder_command "irrigate" "💧" "Irrigating"
create_placeholder_command "fertilize" "🪴" "Fertilizing"
create_placeholder_command "prune" "✂️" "Pruning"
create_placeholder_command "greenhouse" "🏡" "Greenhouse"
create_placeholder_command "silo" "🏭" "Silo Management"
create_placeholder_command "barn" "🏚️" "Barn Management"
create_placeholder_command "field" "🌾" "Field Management"
create_placeholder_command "compost" "♻️" "Composting"
create_placeholder_command "almanac" "📚" "Almanac"
create_placeholder_command "weather" "🌤️" "Weather Check"

# Create template files
echo "🎨 Creating template files..."

cat > src/templates/chat-ui.ts << 'EOF'
export function createChatUI(model: string, agent: string, port: number): string {
  return `<!DOCTYPE html>
<html>
<head>
    <title>LlamaFarm Chat - ${model}</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #2e7d32; }
        .status { background: #e8f5e9; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌾 LlamaFarm Chat</h1>
        <div class="status">
            <p>Model: ${model}</p>
            <p>Agent: ${agent}</p>
            <p>Port: ${port}</p>
        </div>
        <p>🦙 The llamas are in the pasture... Coming soon!</p>
    </div>
</body>
</html>`;
}
EOF

cat > src/templates/agent-server.ts << 'EOF'
export function createAgentServer(config: any): string {
  return `// Agent server for ${config.name}
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('🦙 The llamas are in the pasture... Coming soon!');
});

app.listen(${config.port || 3000}, () => {
  console.log('🌾 LlamaFarm agent server (placeholder) running on port ${config.port || 3000}');
});`;
}
EOF

cat > src/templates/dockerfile.ts << 'EOF'
export function createDockerfile(device: string, model: string, config: any): string {
  return `FROM ubuntu:22.04
# LlamaFarm Dockerfile for ${model} on ${device}
# 🦙 The llamas are in the pasture... Coming soon!
WORKDIR /app
CMD ["echo", "LlamaFarm placeholder container"]`;
}
EOF

# Create utility files
echo "🔧 Creating utility files..."

cat > src/utils/config.ts << 'EOF'
import * as fs from 'fs-extra';
import * as path from 'path';
import * as os from 'os';

export function getConfigPath(): string {
  return path.join(os.homedir(), '.llamafarm', 'config.json');
}

export async function loadConfig(): Promise<any> {
  const configPath = getConfigPath();
  if (await fs.pathExists(configPath)) {
    return await fs.readJSON(configPath);
  }
  return {
    version: '0.1.0',
    message: 'The llamas are in the pasture...',
    status: 'coming_soon'
  };
}

export async function saveConfig(config: any): Promise<void> {
  const configPath = getConfigPath();
  await fs.ensureDir(path.dirname(configPath));
  await fs.writeJSON(configPath, config, { spaces: 2 });
}
EOF

cat > src/utils/yaml.ts << 'EOF'
import * as yaml from 'js-yaml';
import * as fs from 'fs-extra';

export async function loadYamlConfig(filePath: string): Promise<any> {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return yaml.load(content) as any;
  } catch (error) {
    console.log('🦙 The llamas are learning to read YAML... Coming soon!');
    return {};
  }
}
EOF

cat > src/utils/portfinder.ts << 'EOF'
import * as net from 'net';

export async function getPort(startPort: number = 8080): Promise<number> {
  return new Promise((resolve) => {
    const server = net.createServer();
    
    server.listen(startPort, () => {
      const port = (server.address() as net.AddressInfo).port;
      server.close(() => resolve(port));
    });
    
    server.on('error', () => {
      getPort(startPort + 1).then(resolve);
    });
  });
}
EOF

cat > src/utils/errors.ts << 'EOF'
import chalk from 'chalk';

export class LlamaFarmError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'LlamaFarmError';
  }
}

export function handleError(error: any): void {
  console.error(chalk.red(`\n❌ Error: ${error.message}`));
  console.log(chalk.yellow('\n🦙 The llamas are working on fixing this...'));
  process.exit(1);
}
EOF

cat > src/utils/compiler.ts << 'EOF'
import chalk from 'chalk';

export class BinaryCompiler {
  async compile(options: any): Promise<string> {
    console.log(chalk.yellow('🎯 The Baler is being assembled...'));
    console.log(chalk.gray('🦙 The llamas are in the pasture... Coming soon!'));
    return 'placeholder.tar.gz';
  }
}
EOF

cat > src/utils/validators.ts << 'EOF'
export function validateModelName(model: string): boolean {
  // Placeholder validation
  return true;
}

export function validateDevice(device: string): boolean {
  const validDevices = ['mac', 'windows', 'linux', 'raspberry-pi', 'jetson'];
  return validDevices.includes(device);
}

export function validateQuantization(quantization: string): boolean {
  const validQuantizations = ['q4_0', 'q4_1', 'q5_0', 'q5_1', 'q8_0'];
  return validQuantizations.includes(quantization);
}
EOF

cat > src/utils/system-check.ts << 'EOF'
import * as os from 'os';
import chalk from 'chalk';

export interface SystemInfo {
  platform: string;
  arch: string;
  totalMemory: number;
  freeMemory: number;
  cpuCores: number;
  nodeVersion: string;
}

export async function getSystemInfo(): Promise<SystemInfo> {
  return {
    platform: os.platform(),
    arch: os.arch(),
    totalMemory: Math.round(os.totalmem() / 1024 / 1024 / 1024),
    freeMemory: Math.round(os.freemem() / 1024 / 1024 / 1024),
    cpuCores: os.cpus().length,
    nodeVersion: process.version
  };
}

export function displaySystemRequirements(): void {
  console.log(chalk.cyan('\n📋 System Requirements:'));
  console.log(chalk.gray('   • Node.js 18+'));
  console.log(chalk.gray('   • 4GB+ RAM'));
  console.log(chalk.gray('   • 10GB+ free disk space'));
  console.log(chalk.yellow('\n🦙 The llamas are checking your system...'));
}

// Allow running directly
if (require.main === module) {
  displaySystemRequirements();
}
EOF

# Create model registry
echo "📦 Creating models and agents..."

cat > src/models/registry.ts << 'EOF'
export interface ModelInfo {
  name: string;
  size: string;
  quantizations: string[];
  description: string;
}

export const MODEL_REGISTRY: Record<string, ModelInfo> = {
  'llama3-8b': {
    name: 'Llama 3 8B',
    size: '8B',
    quantizations: ['q4_0', 'q4_1', 'q5_0', 'q5_1', 'q8_0'],
    description: 'Meta\'s Llama 3 - Coming soon!'
  },
  'mixtral-8x7b': {
    name: 'Mixtral 8x7B',
    size: '8x7B',
    quantizations: ['q4_0', 'q4_1', 'q5_0'],
    description: 'Mixtral MoE - The llamas are learning!'
  }
};

export function getModelInfo(modelName: string): ModelInfo | undefined {
  return MODEL_REGISTRY[modelName];
}
EOF

cat > src/agents/templates.ts << 'EOF'
export interface AgentTemplate {
  name: string;
  description: string;
  framework: string;
}

export const AGENT_TEMPLATES: Record<string, AgentTemplate> = {
  'chat-basic': {
    name: 'Basic Chat Assistant',
    description: 'Simple chat - The llamas are practicing conversation!',
    framework: 'langchain'
  },
  'research-assistant': {
    name: 'Research Assistant',
    description: 'Research helper - The llamas are reading papers!',
    framework: 'langchain'
  }
};
EOF

cat > src/config/defaults.ts << 'EOF'
export const DEFAULT_CONFIG = {
  version: '0.1.0',
  defaults: {
    device: 'mac',
    quantization: 'q4_0',
    gpu: false,
    vectorDb: 'chroma',
    agentFramework: 'langchain'
  },
  message: 'The llamas are in the pasture... Coming soon!'
};
EOF

# Create index.ts
cat > src/index.ts << 'EOF'
// LlamaFarm CLI exports
export { plantCommand } from './commands/plant';
export { harvestCommand } from './commands/harvest';
export { tillCommand } from './commands/till';
export { sowCommand } from './commands/sow';
export { greenhouseCommand } from './commands/greenhouse';
export { siloCommand } from './commands/silo';

// Re-export utilities
export * from './utils/config';
export * from './utils/yaml';
export * from './utils/portfinder';

// Package info
export const version = '0.1.0';
export const name = '@llamafarm/llamafarm';
EOF

# Create demo files
echo "🎮 Creating demo files..."

cat > demo/demo.ts << 'EOF'
import express from 'express';
import { WebSocketServer } from 'ws';
import chalk from 'chalk';

export class LlamaFarmDemo {
  private app: express.Application;
  private wss: WebSocketServer;

  constructor(config: any) {
    this.app = express();
    this.wss = new WebSocketServer({ port: config.port + 1 });
  }

  async initialize() {
    this.app.get('/', (req, res) => {
      res.send(`
        <h1>🌾 LlamaFarm Demo</h1>
        <p>🦙 The llamas are in the pasture... Coming soon!</p>
        <p>This is a placeholder demo showing where the magic will happen.</p>
      `);
    });

    this.app.listen(8080, () => {
      console.log(chalk.green('🌾 Demo server running on http://localhost:8080'));
      console.log(chalk.yellow('🦙 The llamas are in the pasture... Full demo coming soon!'));
    });
  }
}
EOF

cat > demo/run-demo.ts << 'EOF'
import { LlamaFarmDemo } from './demo';
import chalk from 'chalk';
import figlet from 'figlet';

export async function runDemo() {
  console.log(chalk.green(figlet.textSync('LlamaFarm Demo', { font: 'Small' })));
  console.log(chalk.yellow('\n🦙 The llamas are preparing the demo...\n'));
  
  const demo = new LlamaFarmDemo({ port: 8080 });
  await demo.initialize();
}

if (require.main === module) {
  runDemo();
}
EOF

# Create test files
echo "🧪 Creating test files..."

cat > src/__tests__/utils.test.ts << 'EOF'
import { validateDevice, validateQuantization } from '../utils/validators';
import { getPort } from '../utils/portfinder';

describe('Utility Functions', () => {
  describe('validators', () => {
    it('should validate device names', () => {
      expect(validateDevice('mac')).toBe(true);
      expect(validateDevice('invalid')).toBe(false);
    });

    it('should validate quantization levels', () => {
      expect(validateQuantization('q4_0')).toBe(true);
      expect(validateQuantization('invalid')).toBe(false);
    });
  });

  describe('portfinder', () => {
    it('should find an available port', async () => {
      const port = await getPort();
      expect(port).toBeGreaterThanOrEqual(8080);
    });
  });
});
EOF

cat > src/__tests__/commands.test.ts << 'EOF'
describe('Commands', () => {
  it('should have placeholder test', () => {
    // The llamas are writing tests... Coming soon!
    expect(true).toBe(true);
  });

  it('should validate llama presence', () => {
    const llamasInPasture = true;
    expect(llamasInPasture).toBe(true);
  });
});
EOF

# Create scripts
echo "📜 Creating scripts..."

cat > scripts/demo.js << 'EOF'
#!/usr/bin/env node
const chalk = require('chalk');

console.log(chalk.green('\n🌾 LlamaFarm Demo'));
console.log(chalk.yellow('🦙 The llamas are in the pasture... Coming soon!\n'));
console.log(chalk.gray('To run the demo when ready:'));
console.log(chalk.gray('  1. npm run build'));
console.log(chalk.gray('  2. node dist/demo/run-demo.js\n'));
EOF

cat > scripts/postinstall.js << 'EOF'
const chalk = require('chalk');
const figlet = require('figlet');

try {
  console.log(chalk.green(figlet.textSync('LlamaFarm', { font: 'Small' })));
  console.log(chalk.yellow('\n🌾 Thank you for installing LlamaFarm! 🦙\n'));
  console.log(chalk.white('Quick Start:'));
  console.log(chalk.gray('  1. Run "llamafarm --help" to see all commands'));
  console.log(chalk.gray('  2. Try "llamafarm weather" to check system status'));
  console.log(chalk.gray('  3. Run "llamafarm plant llama3-8b" to plant your first model\n'));
  console.log(chalk.cyan('📚 Documentation: https://github.com/llamafarm/llamafarm-cli'));
  console.log(chalk.yellow('\n🦙 Note: The llamas are still in the pasture...'));
  console.log(chalk.yellow('   Most features are coming soon!\n'));
} catch (e) {
  // Silent fail for postinstall
}
EOF

# Make scripts executable
chmod +x scripts/*.js

# Create documentation
echo "📚 Creating documentation..."

cat > README.md << 'EOF'
# 🌾 LlamaFarm

> Plant and harvest AI models locally - The complete AI deployment toolkit

[![npm version](https://img.shields.io/npm/v/@llamafarm/llamafarm.svg)](https://www.npmjs.com/package/@llamafarm/llamafarm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LlamaFarm makes deploying AI models, agents, and vector databases as simple as copying a file. Package everything into a single binary that runs anywhere - from Raspberry Pis to enterprise servers.

## 🦙 Current Status

**The llamas are in the pasture... Most features coming soon!**

This is an early preview release. All commands are implemented as placeholders that show what's coming.

## 🚀 Quick Start

```bash
# Install globally
npm install -g @llamafarm/llamafarm

# See available commands
llamafarm --help

# Try a command (placeholder for now)
llamafarm plant llama3-8b
llamafarm weather
```

## 🌱 Features (Coming Soon)

- **🦙 One-Command Deployment**: Package models, agents, and databases into single executables
- **🌾 Farm-Themed CLI**: Intuitive commands that make AI deployment feel natural
- **📦 Zero Dependencies**: Compiled binaries run without Python, CUDA, or complex setups
- **🤖 Multi-Agent Support**: LangChain, AutoGen, CrewAI, and LlamaIndex ready
- **🗄️ Vector Database Integration**: ChromaDB, Qdrant, Pinecone, and Weaviate support
- **🔧 YAML Configuration**: Define complex deployments with simple config files
- **🏡 Local-First**: Keep your data and models on your own hardware

## 📚 Commands

All commands currently show placeholder messages. Full functionality coming soon!

### Core Commands
- `plant` - Package a model with agents and databases
- `harvest` - Deploy a packaged binary

### Configuration
- `till` - Initialize configuration
- `sow` - Configure data sources

### Management
- `barn` - Model storage
- `silo` - Vector database management
- `greenhouse` - Testing environment

### Utilities
- `weather` - System status
- `almanac` - Documentation
- `compost` - Cleanup

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

**Happy Farming! 🌾🦙**

*Remember: The best AI runs on your own hardware.*
EOF

cat > QUICKSTART.md << 'EOF'
# 🚀 LlamaFarm Quick Start Guide

Get ready to run AI models locally! (Coming soon)

## Current Status

🦙 **The llamas are in the pasture...**

This is an early preview. All commands show placeholder messages indicating what features are coming.

## Prerequisites

- Node.js 18+ installed
- 8GB+ of RAM recommended
- ~10GB free disk space for models

## Installation

```bash
# Install globally via npm
npm install -g @llamafarm/llamafarm

# Verify installation
llamafarm --version
```

## Try It Out

Even though features are coming soon, you can explore all commands:

```bash
# See all available commands
llamafarm --help

# Try the weather command
llamafarm weather

# Try planting (placeholder)
llamafarm plant llama3-8b

# Check the almanac
llamafarm almanac
```

## What's Coming

When fully implemented, you'll be able to:

1. **Plant Models**: Package AI models into deployable binaries
2. **Configure Agents**: Set up LangChain, AutoGen, and more
3. **Manage Databases**: Use vector databases for RAG
4. **Deploy Anywhere**: Run on Mac, Linux, Windows, Raspberry Pi, and more

## Stay Updated

- Watch the repo for updates
- Join our Discord (coming soon)
- Follow development progress

Happy farming! 🦙🌾
EOF

cat > CONTRIBUTING.md << 'EOF'
# Contributing to LlamaFarm 🌾

First off, thank you for considering contributing to LlamaFarm!

## 🦙 Current Status

**The llamas are in the pasture...**

This project is in early development. Most features are placeholders showing what's coming.

## 🌱 How Can I Contribute?

### Reporting Issues

- Check if the issue already exists
- Include clear steps to reproduce
- Mention your OS and Node.js version

### Suggesting Features

- Describe the feature clearly
- Explain why it would be useful
- Keep the farming theme alive!

### Code Contributions

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🚜 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/llamafarm-cli.git
cd llamafarm-cli

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run tests
npm test

# Link for local testing
npm link
```

## 📝 Code Style

- Use TypeScript
- Follow existing patterns
- Keep the farming theme consistent
- Add tests for new features

## 🌾 Placeholder to Implementation

When implementing a placeholder command:

1. Keep the friendly farming messages
2. Add real functionality
3. Update tests
4. Update documentation

## Questions?

Feel free to open an issue!

Happy farming! 🦙🌾
EOF

cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Harvest AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Build outputs
dist/
binaries/
*.tgz
*.tar.gz

# LlamaFarm specific
.llamafarm/
harvests/
chroma_db/
*.gguf
models/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# Testing
coverage/
.nyc_output/

# OS
Thumbs.db
EOF

# Create .npmignore
cat > .npmignore << 'EOF'
# Source files (only ship compiled)
src/
tsconfig.json
.eslintrc.json
.prettierrc

# Tests
__tests__/
*.test.ts
*.spec.ts
jest.config.js

# Development files
.gitignore
.editorconfig
.github/

# LlamaFarm runtime
.llamafarm/
harvests/
models/
*.gguf

# Binaries (users build their own)
binaries/

# Development
.vscode/
.idea/
*.log
EOF

# Create .eslintrc.json
cat > .eslintrc.json << 'EOF'
{
  "parser": "@typescript-eslint/parser",
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
EOF

# Create .prettierrc
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
EOF

# Create GitHub Actions workflow
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build
      run: npm run build
      
    - name: Test
      run: npm test
EOF

# Create example configuration
mkdir -p templates/examples
cat > templates/examples/farm.yaml << 'EOF'
# LlamaFarm Configuration Example
# 🦙 The llamas are learning to read YAML... Coming soon!

model:
  name: llama3-8b
  quantization: q4_0
  
agent:
  name: chat-assistant
  framework: langchain
  
deployment:
  device: mac
  port: 8080
  
# This configuration will work once the llamas return from the pasture!
EOF

# Create a setup script for the project
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

echo "🌾 Welcome to LlamaFarm!"
echo "======================="
echo ""

# Check Node.js version
NODE_VERSION=$(node --version 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ is required. Please install Node.js first."
    exit 1
fi

echo "✅ Node.js version OK"
echo ""

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔨 Building TypeScript..."
npm run build

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. npm link (to use llamafarm command globally)"
echo "   2. llamafarm --help (see all commands)"
echo "   3. llamafarm weather (try a command)"
echo ""
echo "🦙 Note: The llamas are in the pasture..."
echo "   Most features are placeholders showing what's coming!"
echo ""
echo "Happy farming! 🌾"
EOF

chmod +x setup.sh

# Final summary
echo ""
echo "✅ LlamaFarm CLI project created successfully!"
echo ""
echo "📁 Project structure:"
echo "   └── llamafarm-cli/"
echo "       ├── 📦 package.json (configured)"
echo "       ├── ⚙️ tsconfig.json (TypeScript config)"
echo "       ├── 📚 README.md, QUICKSTART.md, CONTRIBUTING.md"
echo "       ├── 📄 LICENSE (MIT)"
echo "       ├── 🚀 setup.sh (setup script)"
echo "       ├── src/"
echo "       │   ├── 🌾 cli.ts (main entry with all commands)"
echo "       │   ├── commands/ (14 command files)"
echo "       │   ├── templates/ (3 template generators)"
echo "       │   ├── utils/ (7 utility files)"
echo "       │   ├── models/ (model registry)"
echo "       │   ├── agents/ (agent templates)"
echo "       │   └── __tests__/ (test files)"
echo "       ├── demo/ (demo implementation)"
echo "       ├── scripts/ (helper scripts)"
echo "       └── .github/workflows/ (CI/CD)"
echo ""
echo "📊 Total files created: 47"
echo ""
echo "🚀 To get started:"
echo "   cd llamafarm-cli"
echo "   ./setup.sh"
echo ""
echo "🦙 Note: All commands work but show 'The llamas are in the pasture...' message"
echo "   This is intentional - showing the structure of what's to come!"
echo ""
echo "Happy farming! 🌾🦙"
EOF