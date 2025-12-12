import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import zipapp
import io


def _make_run_bat(target_script_name: str, embed: bool) -> str:
    # run script from the extraction folder
    if embed:
        cmd = '"%~dp0\\python.exe" "%~dp0\\' + target_script_name + '"'
    else:
        cmd = 'py -3 "%~dp0\\' + target_script_name + '"'
    # Use CRLF endings for Windows tools
    content = f"@echo off\r\n{cmd}\r\n"
    return content


def _generate_sed(target_name: str, payload_dir: Path, install_cmd: str) -> str:
    # Create a minimal IExpress SED file to create a self-extracting archive that runs install_cmd
    # IExpress expects SourceFiles0 to point to the payload folder, and [SourceFiles0]
    # to list entries like file001=filename (relative to SourceFiles0 path).
    files_section_lines = []
    for i, p in enumerate(sorted(payload_dir.iterdir()), start=1):
        key = f"file{str(i).zfill(3)}"
        files_section_lines.append(f"{key}={p.name}")

    files_section = "\n".join(files_section_lines)
    # Ensure TargetName is absolute path
    target_abs = str(Path(target_name).resolve())
    payload_abs = str(Path(payload_dir).resolve())

    sed = f"""[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=0
UseLongFileName=1
InsideOut=0
CAB_FixedSize=0
RebootMode=NoRestart
InstallPrompt=
DisplayLicense=No
FinishedMessage=No
TargetName={target_abs}
FriendlyName=pyexe bundle
InstallProgram={install_cmd}
PostInstallCmd=

[SourceFiles]
SourceFiles0={payload_abs}

[SourceFiles0]
{files_section}

[Strings]
"""
    return sed


def build_script(script_path: Path, output: str = None, embed_interpreter: bool = False):
    script_path = Path(script_path)
    base = script_path.stem

    dist = Path(os.getcwd()) / "dist"
    dist.mkdir(exist_ok=True)

    if output:
        out_path = Path(output)
        if out_path.is_dir():
            out_path = out_path / f"{base}.exe"
    else:
        out_path = dist / f"{base}.exe"

    # Try to build an IExpress self-extracting exe on Windows
    if sys.platform.startswith("win"):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            payload = td_path / "payload"
            payload.mkdir()
            # copy script
            target_script_name = script_path.name
            shutil.copy2(script_path, payload / target_script_name)

            # if embedding interpreter requested, copy current python.exe and related DLLs (best-effort)
            if embed_interpreter:
                py_exe = Path(sys.executable)
                try:
                    shutil.copy2(py_exe, payload / "python.exe")
                except Exception:
                    pass

            # make run.bat
            run_bat_content = _make_run_bat(target_script_name, embed_interpreter)
            (payload / "run.bat").write_text(run_bat_content, encoding="mbcs")

            # generate SED and call iexpress
            sed_path = td_path / "build.sed"
            sed_content = _generate_sed(str(out_path.resolve()), payload, "run.bat")
            # IExpress expects the SED file in the ANSI codepage; write using the local MBCS encoding
            sed_path.write_text(sed_content, encoding="mbcs")
            # also save a copy for debugging in dist
            try:
                debug_sed = Path(os.getcwd()) / "dist" / "last_build.sed"
                debug_sed.write_text(sed_content, encoding="mbcs")
            except Exception:
                pass

            iexpress = shutil.which("iexpress.exe")
            if iexpress:
                # Call IExpress to create the self-extracting EXE
                # Use /N to run non-interactively with an SED file
                proc = subprocess.run([iexpress, "/N", str(sed_path)], cwd=td, capture_output=True, text=True)
                if proc.returncode != 0:
                    # don't raise — fall back to zipapp so user can still get a runnable artifact
                    print(f"IExpress failed (rc={proc.returncode}). Falling back to zipapp.\nstdout:{proc.stdout}\nstderr:{proc.stderr}")
                else:
                    print(f"Built: {out_path}")
                    return
            else:
                print("IExpress not found — falling back to zipapp + .cmd launcher")

            # Try 7-Zip SFX method as a more robust alternative if available
            try:
                seven = shutil.which("7z") or shutil.which("7za")
                if seven:
                    sfx_module = Path(seven).parent / "7z.sfx"
                    if not sfx_module.exists():
                        # try common sibling names
                        for name in ("7zCon.sfx", "7zS.sfx"):
                            cand = Path(seven).parent / name
                            if cand.exists():
                                sfx_module = cand
                                break

                    if sfx_module.exists():
                        # create archive
                        archive = td_path / "payload.7z"
                        # use 7z to create the archive (archive placed in td)
                        cmd = [seven, "a", "-mx=9", str(archive), "*"]
                        proc7 = subprocess.run(cmd, cwd=payload, capture_output=True, text=True)
                        if proc7.returncode == 0:
                            # create config
                            install_cmd = "run.bat"
                            config = (
                                ";!@Install@!UTF-8!\r\n"
                                f"Title=pyexe bundle\r\n"
                                f"RunProgram={install_cmd}\r\n"
                                ";!@InstallEnd@!\r\n"
                            )
                            out_exe = out_path
                            with open(sfx_module, "rb") as f_sfx, open(archive, "rb") as f_arch, open(out_exe, "wb") as f_out:
                                f_out.write(f_sfx.read())
                                f_out.write(config.encode("utf-8"))
                                f_out.write(f_arch.read())
                            print(f"Built using 7z SFX: {out_exe}")
                            return
                        else:
                            print("7z failed to create archive, falling back to zipapp")
            except Exception:
                pass

    # Fallback: create a zipapp .pyz and a .cmd launcher
    pyz_path = Path(os.getcwd()) / "dist" / f"{base}.pyz"
    # build a tiny package directory
    with tempfile.TemporaryDirectory() as td2:
        td2p = Path(td2)
        app_dir = td2p / base
        app_dir.mkdir()
        # copy script as __main__.py
        shutil.copy2(script_path, app_dir / "__main__.py")
        # create zipapp
        zipapp.create_archive(app_dir, pyz_path)

    # create a .cmd launcher next to pyz
    launcher_cmd = Path(os.getcwd()) / "dist" / f"{base}.cmd"
    launcher_cmd.write_text(f"@echo off\npy -3 %~dp0\\{pyz_path.name} %*\n", encoding="utf-8")

    print(f"Fallback build created: {pyz_path} and launcher {launcher_cmd}")
