if (Test-Path dist) {
    rm -r dist
}

python -m build
python -m twine upload dist/* # 上传，需要 token
