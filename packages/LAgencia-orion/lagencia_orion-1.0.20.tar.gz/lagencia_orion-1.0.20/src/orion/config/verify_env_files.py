#!/usr/bin/env python3
"""
Script para verificar la configuración de archivos .env
Ejecutar desde: /workspaces/airflow/dags/orion/config/
"""

import os
from pathlib import Path


def verify_env_files():
    print("=" * 60)
    print("VERIFICACIÓN DE ARCHIVOS DE CONFIGURACIÓN")
    print("=" * 60)

    # Directorio del script
    config_dir = Path(__file__).resolve().parent
    print(f"\n📁 Directorio de config: {config_dir}")
    print(f"📁 Directorio de trabajo actual: {Path.cwd()}")

    # Variable de entorno
    env = os.getenv("PYTHON_ENV_ORION", "dev")
    print(f"\n🔧 PYTHON_ENV_ORION = {env}")

    # Buscar archivos .env
    print("\n🔍 Archivos .env encontrados:")
    env_files = sorted(config_dir.glob(".env*"))

    if env_files:
        for f in env_files:
            size = f.stat().st_size
            print(f"  ✓ {f.name} ({size} bytes)")
    else:
        print("  ✗ No se encontraron archivos .env")

    # Verificar archivo específico
    target_file = config_dir / f".env.{env}"
    print(f"\n🎯 Archivo objetivo: {target_file}")

    if target_file.exists():
        print("  ✓ Archivo existe")
        print("  📄 Contenido (sin valores sensibles):")
        with open(target_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key = line.split("=")[0]
                    print(f"     {key}=***")
    else:
        print("  ✗ Archivo NO existe")
        print("\n💡 Crear archivo con:")
        print(f"     touch {target_file}")
        print("\n💡 Ejemplo de contenido:")
        print("""     URL_DB_EMPATIA=postgresql://user:pass@host:5432/empatia
     URL_DB_BELLATRIX=postgresql://user:pass@host:5432/bellatrix
     LOG_LEVEL=INFO""")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    verify_env_files()
