#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import subprocess

current_dir = pathlib.Path(__file__).resolve().parent

ps_script = r'''
# Define paths
$fontPath = Join-Path -Path $pwd.Path -ChildPath "assets/font/PocketCalculator.ttf"
$fontsDirectory = [System.IO.Path]::Combine($env:WINDIR, "Fonts")

# Register font command
$definition = @"
using System;
using System.Runtime.InteropServices;

public class FontInstaller {
    [DllImport("gdi32.dll", CharSet = CharSet.Auto)]
    public static extern int AddFontResource(string lpFileName);
}
"@

# Check if the font file exists
if (Test-Path -Path $fontPath) {

    Write-Host "Font file exists, proceeding with copy..."

    try {
        # Take ownership of the Fonts folder using icacls
        icacls "C:\Windows\Fonts" /setowner "$env:USERDOMAIN\$env:USERNAME" /t > $null 2>&1
        Write-Host "Successfully took ownership of Fonts folder."

        # Grant full control to the current user on the Fonts directory
        $user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        icacls "C:\Windows\Fonts" /grant "${$user}:(F)" /t > $null 2>&1
        Write-Host "Full control granted on Fonts folder."

        # Copy the font file into the Fonts directory
        #Copy-Item -Path $fontPath -Destination $fontsDirectory -Force -ErrorAction SilentlyContinue
        #Write-Host "Font file copied successfully."

        # Register the font with the system
        Add-Type -TypeDefinition $definition

        [FontInstaller]::AddFontResource($fontPath) > $null 2>&1
        Write-Host "Font registered successfully."

        # Restore default permissions on the Fonts directory
        icacls "C:\Windows\Fonts" /reset /t > $null 2>&1
        Write-Host "Permissions restored to default."

    } catch {
        Write-Host "Failed to install font. Error: $_"
        exit
    }

} else {
    Write-Host "Font file does not exist. Please check the path."
    exit
}
'''

# |-----------------------------------------------|
# | Shortcut    |	Button  | Description         |
# |-------------|-----------|---------------------|
# | Insert      |     C     | Clear All           |
# | Delete      |	  CE    | Clear Entry         |
# | Home        |	 MRC	| Memory Recall       |
# | End         |	 MRC    | Memory Clear        |
# | Ctrl +      |	  M+    | Memory Add          |
# | Ctrl -      |	  M- 	| Memory Subtract     |
# | Page Up     |	  %	    | Percentage          |
# | Page Down   |     √	    | Square Root         |
# | Pause Break |    +/-    | Plus-Minus (Negate) |
# | Enter       |	  =	    | Equals (Get Result) |
# |-----------------------------------------------|


def check_application_files() -> bool:
    icons = current_dir.parent / 'assets' / 'icons'
    font = current_dir.parent / 'assets' / 'font' / 'PocketCalculator.ttf'
    images = [i for i in icons.iterdir()] if icons.is_dir() else []
    return all([font.is_file(), len(images)])

def get_image_path(filename: str) -> str:
    path = current_dir.parent / 'assets' / 'icons' / filename
    return str(path) if path.is_file() else filename

def install_calculator_font() -> bool:
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,    # Capture stdout and stderr
            text=True,  # Capture output as text (not bytes)
        )

        # Check if the PowerShell command executed
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False