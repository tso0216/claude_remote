#!/usr/bin/env bash
# 把 repo 根目錄的 "Chapter X-Y.ppt(x)" 轉成 materials/md/ChX-Y.md 與 materials/pdf/ChX-Y.pdf，並重建 INDEX.md。
# 用法：bash materials/tools/convert.sh            （轉全部）
#       bash materials/tools/convert.sh "Chapter 5-1.ppt"   （只轉指定檔）
# 需要：Java 17+、Maven、LibreOffice、Python 3 + Pillow。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOOLS="$ROOT/materials/tools"; MD="$ROOT/materials/md"; PDF="$ROOT/materials/pdf"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
mkdir -p "$MD" "$PDF"

if [ ! -d "$TOOLS/lib" ]; then (cd "$TOOLS" && mvn -q dependency:copy-dependencies -DoutputDirectory=lib); fi
javac -proc:none -cp "$TOOLS/lib/*" -d "$WORK/cls" "$TOOLS/Extract.java"

if [ "$#" -gt 0 ]; then files=("$@"); else mapfile -t files < <(cd "$ROOT" && ls Chapter*.ppt Chapter*.pptx 2>/dev/null); fi
OPTS='pdf:impress_pdf_Export:{"ExportHiddenSlides":{"type":"boolean","value":"true"},"ReduceImageResolution":{"type":"boolean","value":"true"},"MaxImageResolution":{"type":"long","value":"150"},"Quality":{"type":"long","value":"80"}}'

for f in "${files[@]}"; do
  src="$ROOT/$f"; base="$(basename "$f")"; base="${base%.*}"; id="Ch${base#Chapter }"
  echo "== $f -> $id"
  java -Djava.awt.headless=true -cp "$WORK/cls:$TOOLS/lib/*" Extract "$src" "$MD/$id.md" "pdf/$id.pdf" 2>/dev/null
  rm -f "$WORK/$base.pdf"
  soffice --headless --convert-to "$OPTS" --outdir "$WORK" "$src" >/dev/null 2>&1 || true
  if [ -s "$WORK/$base.pdf" ]; then
    mv "$WORK/$base.pdf" "$PDF/$id.pdf"
  else
    echo "   LibreOffice 無法開啟，改用 Apache POI 轉圖片"
    mkdir -p "$WORK/png"
    java -Djava.awt.headless=true -cp "$TOOLS/lib/*" org.apache.poi.xslf.util.PPTX2PNG -quiet -format png -scale 1.4 \
      -outdir "$WORK/png" -outpat '${basename}-${slideno}.${format}' "$src" 2>/dev/null
    python3 "$TOOLS/to_pdf.py" "$WORK/png" "$base" "$PDF/$id.pdf"
  fi
done

python3 "$TOOLS/fill_titles.py" "$MD"
python3 "$TOOLS/build_index.py" "$MD" "$ROOT/materials/INDEX.md"
echo "完成。新章節的主題摘要要手動補進 materials/tools/build_index.py 的 TOPICS。"
