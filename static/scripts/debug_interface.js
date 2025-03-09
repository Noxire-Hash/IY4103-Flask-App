class DebugInterface {
    constructor() {
        this.gameState = {
            currentBiome: null,
            currentAction: null,
            isHarvesting: false,
            gameData: null,
            stamps: []
        };

        // Available console commands
        this.consoleCommands = {
            help: () => this.showHelp(),
            'material.add': (id, amount = 1) => this.addMaterial(id, amount),
            'material.remove': (id, amount = 1) => this.removeMaterial(id, amount),
            'stamp.create': (name, rarity = 'common') => this.createCustomStamp(name, rarity),
            'stamp.progress': (id, progress) => this.updateStampProgress(id, progress),
            'player.addExp': (amount) => this.addPlayerExp(amount),
            'player.addCoins': (amount) => this.addPlayerCoins(amount),
            'clear': () => this.clearConsole()
        };

        this.loadGameData()
            .then(() => {
                this.initializeElements();
                this.setupEventListeners();
                this.loadInitialData();
            });
    }

    async loadGameData() {
        try {
            this.setLoadingState(true);
            const response = await fetch('/api/game_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.gameState.gameData = await response.json();
            console.log('Game data loaded:', this.gameState.gameData);
        } catch (error) {
            console.error('Failed to load game data:', error);
            this.logMessage(`Error loading game data: ${error.message}`);
        } finally {
            this.setLoadingState(false);
        }
    }

    setLoadingState(isLoading) {
        const container = document.getElementById('stampsContainer');
        if (container) {
            if (isLoading) {
                container.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
            }
        }

        // Disable buttons during loading
        const buttons = ['addStamp', 'clearStamps', 'createStamp'];
        buttons.forEach(id => {
            const button = document.getElementById(id);
            if (button) {
                button.disabled = isLoading;
            }
        });
    }

    initializeElements() {
        // UI Elements
        this.elements = {
            console: document.getElementById('debugConsole'),
            biomeSelect: document.getElementById('biomeSelect'),
            entitySelect: document.getElementById('entitySelect'),
            playerStats: {
                level: document.getElementById('playerLevel'),
                exp: document.getElementById('playerExp'),
                coins: document.getElementById('playerCoins')
            },
            currentAction: {
                type: document.getElementById('currentActionType'),
                target: document.getElementById('currentActionTarget'),
                progress: document.getElementById('actionProgressText'),
                timeRemaining: document.getElementById('actionTimeRemaining'),
                progressBar: document.querySelector('.action-progress .progress-bar')
            }
        };
    }

    setupEventListeners() {
        // Biome Control
        this.elements.biomeSelect.addEventListener('change', () => this.updateBiomeInfo());
        document.getElementById('travelToBiome').addEventListener('click', () => this.travelToBiome());

        // Entity Actions
        document.getElementById('harvestEntity').addEventListener('click', () => this.startHarvesting());
        document.getElementById('spawnEntity').addEventListener('click', () => this.spawnEntity());

        // Debug Actions
        document.getElementById('createStamp').addEventListener('click', () => this.createStamp());
        document.getElementById('toggleLogger').addEventListener('click', () => this.toggleLogger());

        // Equipment Management
        document.querySelectorAll('.remove-item').forEach(btn => {
            btn.addEventListener('click', (e) => this.removeItem(e));
        });

        // Stamps functionality
        document.getElementById('addStamp').addEventListener('click', () => this.addStamp());
        document.getElementById('clearStamps').addEventListener('click', () => this.clearStamps());

        // Console input handling
        const consoleInput = document.getElementById('consoleInput');
        const executeBtn = document.getElementById('executeCommand');

        consoleInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand(consoleInput.value);
                consoleInput.value = '';
            }
        });

        executeBtn.addEventListener('click', () => {
            this.executeCommand(consoleInput.value);
            consoleInput.value = '';
        });
    }

    loadInitialData() {
        // Load biomes
        this.populateBiomeSelect();
        this.updateBiomeInfo();

        // Load initial player stats
        this.updatePlayerStats({
            level: 1,
            exp: 0,
            coins: 1000
        });

        // Load initial stamps
        this.loadStamps();
    }

    // UI Update Methods
    populateBiomeSelect() {
        if (!this.gameState.gameData?.biomes) {
            this.logMessage('Error: No biome data available');
            return;
        }

        this.elements.biomeSelect.innerHTML = this.gameState.gameData.biomes.map(biome =>
            `<option value="${biome.id}">${biome.name} (Level ${biome.req_level})</option>`
        ).join('');
    }

    updateBiomeInfo() {
        if (!this.gameState.gameData?.biomes) {
            this.logMessage('Error: No biome data available');
            return;
        }

        const selectedBiome = this.gameState.gameData.biomes.find(b => b.id === this.elements.biomeSelect.value);
        if (selectedBiome) {
            this.gameState.currentBiome = selectedBiome;
            this.updateEntitySelect();
            this.logMessage(`Selected biome: ${selectedBiome.name}`);
        }
    }

    loadStamps() {
        if (!this.gameState.gameData?.stamps) {
            this.logMessage('Error: No stamp data available');
            return;
        }

        this.gameState.stamps = this.gameState.gameData.stamps;
        this.renderStamps();
    }

    renderStamps() {
        const container = document.getElementById('stampsContainer');
        if (!container) {
            this.logMessage('Error: Stamps container not found');
            return;
        }

        container.innerHTML = '';

        if (!this.gameState.stamps || this.gameState.stamps.length === 0) {
            container.innerHTML = '<div class="text-muted">No stamps available</div>';
            return;
        }

        this.gameState.stamps.forEach(stamp => {
            const stampElement = document.createElement('div');
            stampElement.className = 'stamp-item';
            stampElement.innerHTML = `
                <div class="stamp-header">
                    <span class="stamp-name">${stamp.name}</span>
                    <span class="stamp-rarity ${stamp.rarity}">${stamp.rarity.charAt(0).toUpperCase() + stamp.rarity.slice(1)}</span>
                </div>
                <div class="stamp-progress">
                    <div class="progress">
                        <div class="progress-bar" role="progressbar"
                             style="width: ${(stamp.progress / stamp.max_progress) * 100}%"
                             aria-valuenow="${stamp.progress}"
                             aria-valuemin="0"
                             aria-valuemax="${stamp.max_progress}">
                        </div>
                    </div>
                    <span class="progress-text">${stamp.progress}/${stamp.max_progress}</span>
                </div>
            `;
            container.appendChild(stampElement);
        });
    }

    addStamp() {
        // Example of adding a new stamp
        const newStamp = {
            id: `stamp_${Date.now()}`,
            name: "New Achievement",
            rarity: "common",
            progress: 0,
            max_progress: 100
        };
        this.gameState.stamps.push(newStamp);
        this.renderStamps();
        this.logMessage('New stamp added');
    }

    clearStamps() {
        this.gameState.stamps = [];
        this.renderStamps();
        this.logMessage('All stamps cleared');
    }

    createStamp() {
        // This method is called when clicking the "Create Stamp" button in debug actions
        const stamp = {
            id: `stamp_${Date.now()}`,
            name: "Debug Achievement",
            rarity: "epic",
            progress: Math.floor(Math.random() * 100),
            max_progress: 100
        };
        this.gameState.stamps.push(stamp);
        this.renderStamps();
        this.logMessage('Debug stamp created');
    }

    executeCommand(input) {
        if (!input.trim()) return;

        this.logMessage(`> ${input}`, 'command');

        try {
            // Parse the command
            const matches = input.match(/^(\w+(?:\.\w+)?)\s*\((.*)\)$/);
            if (!matches) {
                if (input.toLowerCase() === 'help') {
                    this.showHelp();
                    return;
                }
                if (input.toLowerCase() === 'clear') {
                    this.clearConsole();
                    return;
                }
                throw new Error('Invalid command format. Type "help" for usage.');
            }

            const [, command, argsString] = matches;

            // Parse arguments, handling strings and numbers
            const args = argsString ? argsString.split(',').map(arg => {
                arg = arg.trim();
                if (arg.startsWith("'") || arg.startsWith('"')) {
                    return arg.slice(1, -1);
                }
                return !isNaN(arg) ? Number(arg) : arg;
            }) : [];

            if (this.consoleCommands[command]) {
                const result = this.consoleCommands[command](...args);
                if (result !== undefined) {
                    this.logMessage(`Result: ${result}`);
                }
            } else {
                throw new Error(`Unknown command: ${command}`);
            }
        } catch (error) {
            this.logMessage(`Error: ${error.message}`, 'error');
        }
    }

    showHelp() {
        const helpText = `
Available commands:
- help() : Show this help message
- clear() : Clear console
- material.add(id, amount?) : Add material to inventory
- material.remove(id, amount?) : Remove material from inventory
- stamp.create(name, rarity?) : Create a new stamp
- stamp.progress(id, progress) : Update stamp progress
- player.addExp(amount) : Add experience points
- player.addCoins(amount) : Add coins

Examples:
> material.add('wood', 5)
> stamp.create('My Achievement', 'rare')
> player.addExp(100)
        `;
        this.logMessage(helpText);
    }

    // Command implementations
    addMaterial(id, amount = 1) {
        this.logMessage(`Adding ${amount} ${id} to inventory`);
        // TODO: Implement actual material addition
    }

    removeMaterial(id, amount = 1) {
        this.logMessage(`Removing ${amount} ${id} from inventory`);
        // TODO: Implement actual material removal
    }

    createCustomStamp(name, rarity = 'common') {
        const stamp = {
            id: `stamp_${Date.now()}`,
            name: name,
            rarity: rarity,
            progress: 0,
            max_progress: 100
        };
        this.gameState.stamps.push(stamp);
        this.renderStamps();
        this.logMessage(`Created stamp: ${name} (${rarity})`);
    }

    updateStampProgress(id, progress) {
        const stamp = this.gameState.stamps.find(s => s.id === id);
        if (stamp) {
            stamp.progress = Math.min(Math.max(0, progress), stamp.max_progress);
            this.renderStamps();
            this.logMessage(`Updated stamp progress: ${stamp.name} - ${progress}/${stamp.max_progress}`);
        } else {
            throw new Error(`Stamp not found: ${id}`);
        }
    }

    addPlayerExp(amount) {
        const currentExp = parseInt(this.elements.playerStats.exp.textContent);
        this.updatePlayerStats({ exp: currentExp + amount });
        this.logMessage(`Added ${amount} experience points`);
    }

    addPlayerCoins(amount) {
        const currentCoins = parseInt(this.elements.playerStats.coins.textContent);
        this.updatePlayerStats({ coins: currentCoins + amount });
        this.logMessage(`Added ${amount} coins`);
    }

    logMessage(message, type = 'info') {
        const timestamp = new Date().toISOString().replace('T', ' ').substr(0, 19);
        const logLine = document.createElement('div');
        logLine.className = `console-line ${type}`;

        if (type === 'command') {
            logLine.innerHTML = `<span class="command-text">${message}</span>`;
        } else {
            logLine.innerHTML = `
                <span class="timestamp">[${timestamp}]</span>
                <span class="message">${message}</span>
            `;
        }

        this.elements.console.appendChild(logLine);
        this.elements.console.scrollTop = this.elements.console.scrollHeight;
    }

    clearConsole() {
        this.elements.console.innerHTML = '';
        this.logMessage('Console cleared');
    }
}

// Initialize the debug interface when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    const debugInterface = new DebugInterface();
});
