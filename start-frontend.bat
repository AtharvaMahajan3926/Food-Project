@echo off
echo ==============================================
echo  Launching FoodShare Mumbai Frontend Runtime
echo ==============================================

cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

echo Starting Frontend Server...
npm start
