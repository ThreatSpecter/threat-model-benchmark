# cryptocurrency-wallet

Electrum Wallet + Exchange + Blockchain Integration — All components shown in the diagram, including wallet, exchange backend & API, mobile app, and blockchain integration. Out of scope: user’s OS, hardware device, third-party dependencies not shown. A data flow diagram of a cryptocurrency wallet submitted by Jonathan Marcil to the OWASP Threat Model Cookbook.

## Components
- Electrum Wallet GUI
- Electrum Wallet Daemon
- ElectrumX Server
- Web Browser
- Mobile App
- Exchange Website (Front-end)
- Exchange Backend
- Exchange API (Node.js)
- Trading Bot
- Blockchain Integration Module
- Wallet File
- MySQL (User & Config)
- MongoDB (Exchange Data)

## Data flows
- actor-user → comp-browser
- actor-user → comp-wallet-gui
- comp-wallet-gui → comp-wallet-daemon
- comp-wallet-daemon → comp-electrumx
- comp-browser → comp-exchange-website
- comp-exchange-website → comp-exchange-backend
- comp-trading-bot → comp-exchange-api
- comp-exchange-backend → store-mongodb
- comp-exchange-backend → store-mysql-config
- comp-exchange-backend → comp-blockchain-integration
- comp-wallet-daemon → comp-blockchain-integration

## Trust zones
- User Device
- Internet
- Exchange Internal