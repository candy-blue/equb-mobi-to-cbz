# equb-mobi-to-cbz

一个 Windows 小工具：把 `.equb/.epub` 与 `.mobi`（非 DRM）转换为 `.cbz`。

## 当前功能

- 支持批量选择文件（`.equb` / `.epub` / `.mobi`）
- 输出为同名 `.cbz`，并对图片按页序重命名为 `0001.jpg`、`0002.png`…
- `.equb/.epub`：直接从压缩包中提取图片并打包为 CBZ
- `.mobi`：先解包提取图片再打包为 CBZ（仅支持未加密文件）

## 使用方式

### 方式一：直接运行（GUI）

双击运行程序，选择文件与输出目录，点击“开始转换”。

### 方式二：命令行（CLI）

```bash
python main.py --cli --out 输出目录 输入1.equb 输入2.mobi
```

## 打包成 Windows 可执行文件（exe）

```bash
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name equb-mobi-to-cbz main.py
```

输出位置：

- `dist/equb-mobi-to-cbz.exe`

## 常见问题

- 转换失败提示“加密/No images found”：通常是文件带 DRM 或内容不是图片型书籍
