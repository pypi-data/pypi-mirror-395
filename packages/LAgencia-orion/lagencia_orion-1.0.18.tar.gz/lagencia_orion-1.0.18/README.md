publicar  el modulo en pypi
instalar el modulo
https://chatgpt.com/c/68e3e04f-be3c-8328-86a5-db6c221772474
https://chatgpt.com/c/68e3e04f-be3c-8328-86a5-db6c22177247


crear ejecutables con invoke para /scripts
https://chatgpt.com/c/68e3e37c-f180-832f-9ccb-1542f3c6aa1d



notas sqlalchemy
https://chatgpt.com/c/68dc236f-6b28-832e-943c-7d041e3c91c9



# =====================
https://chatgpt.com/c/68e55ff6-72c4-8332-b31a-16557791346a

# Contruir el paquete
uv build

uv pip install .

Si quieres editable (desarrollo):
uv pip install -e .


uv pip install ..\pr_install_pack\dist\pr_install_pack-0.1.0-py3-none-any.whl
uv pip install ..\pr_install_pack\dist\*.whl --force-reinstall


# con uv pip
Si lo instalaste desde wheel (.whl)
uv build
uv pip install -e ..\pr_install_pack
uv pip install ..\pr_install_pack\dist\pr_install_pack-0.1.0-py3-none-any.whl
uv pip uninstall ..\pr_install_pack\dist\pr_install_pack-0.1.0-py3-none-any.whl


# solo con uv
uv add ..\pr_install_pack\dist\pr_install_pack-0.1.0-py3-none-any.whl
uv add --editable ..\pr_install_pack
uv remove pr_install_pack


uv add C:\Users\Pc\Desktop\proyectos\orion\dist\orion-0.1.0-py3-none-any.whl

Remove-Item -Recurse -Force dist, build
uv build
uv publish --token TOKEN_PYPI
