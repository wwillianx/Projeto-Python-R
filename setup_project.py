import subprocess
import sys
import os

def install_python_packages():
    print("📦 Instalando pacotes Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_r_packages():
    print("📦 Instalando pacotes R...")
    r_command = 'Rscript r_requirements.R'
    subprocess.check_call(r_command, shell=True)

def main():
    print("🚀 Iniciando setup do projeto...\n")
    install_python_packages()
    install_r_packages()
    print("\n✅ Tudo pronto! Agora você pode rodar: python3 main.py")

if __name__ == "__main__":
    main()
