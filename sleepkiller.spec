# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.\\'],
             binaries=None,
             datas=None,
             hiddenimports=['pystray._win32'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Sleepkiller',
          debug=False,
          strip=False,
          upx=True,
          upx_exclude = ['vcruntime140.dll'],
          console=False,
          icon='icon.ico',
          #version='version_file.txt',
      )
