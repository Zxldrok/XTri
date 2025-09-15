@echo off
echo ========================================
echo    Suite d'Optimisation PC - XTri
echo ========================================
echo.
echo Lancement de l'application...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier si psutil est installé
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo Installation de la dépendance psutil...
    pip install psutil
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer psutil
        pause
        exit /b 1
    )
)

REM Lancer l'application
echo Démarrage de la Suite d'Optimisation PC...
python pc_optimizer_suite.py

REM Si l'application se ferme avec une erreur
if errorlevel 1 (
    echo.
    echo L'application s'est fermée avec une erreur.
    echo Vérifiez les messages ci-dessus pour plus d'informations.
    pause
)

echo.
echo Application fermée.
pause