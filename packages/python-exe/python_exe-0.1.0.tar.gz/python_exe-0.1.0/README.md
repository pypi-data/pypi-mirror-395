pyexe (v0.1.0)
=================

快速说明
- 命令：`pyexe build <file.py>`
- 目的：生成一个可运行的打包结果（Windows 平台优先实现）。

实现细节与限制（0.1.0）
- 首选在 Windows 上使用系统自带的 `IExpress` 生成自解压 `.exe`。该 `.exe` 会将你的脚本解压到临时目录并运行一个 `run.bat`（默认使用系统 `py -3` 运行，或在 `--embed-interpreter` 指定时尝试运行捆绑的 `python.exe`）。
- 如果 `IExpress` 不可用或构建失败，构建器会回退到生成一个 `dist/<name>.pyz`（zipapp）和一个 `dist/<name>.cmd` 启动器。目标机器需要安装 Python（可用 `py` 启动器）。
- 当前版本不会像 PyInstaller 那样把 Python 解释器和所有扩展完整地打包成单个本地二进制，若需要完全独立的二进制文件，请考虑后续版本或使用专门工具。

如何使用
1. 安装（可选）
   - 本地可用：`python -m pip install -e .`（在项目目录运行）
   - 或直接通过 `python -m pyexe build script.py`

2. 示例：
```
pyexe build hello.py
```

3. 构建结果见 `dist/`：
   - 在 Windows 且 IExpress 可用：`dist/hello.exe`
   - 否则：`dist/hello.pyz` + `dist/hello.cmd`

注意事项
- `--embed-interpreter` 会尝试复制当前 Python 可执行文件到打包目录，体积可能很大，且不保证包含所有运行时依赖。
- 若你需要更完整的独立 exe（无需目标机器安装 Python），推荐使用专门工具或在后续版本中实现更复杂的打包流程。

下一步（我可以帮忙）
- 添加更多资源收集（复制依赖包、DLL、扩展模块）以实现真正独立的 exe。
- 集成可选的压缩与数字签名。
