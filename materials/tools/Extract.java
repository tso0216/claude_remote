import org.apache.poi.sl.usermodel.*;

import java.awt.geom.Rectangle2D;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

/** Dump every slide of a .ppt/.pptx as Markdown, in slide order. Usage: Extract <in> <out.md> <pdfName> */
public class Extract {
    static final Set<Placeholder> SKIP = EnumSet.of(Placeholder.FOOTER, Placeholder.SLIDE_NUMBER,
            Placeholder.DATETIME, Placeholder.HEADER, Placeholder.TITLE, Placeholder.CENTERED_TITLE);

    public static void main(String[] a) throws Exception {
        File in = new File(a[0]);
        try (SlideShow<?, ?> ss = SlideShowFactory.create(in, null, true)) {
            StringBuilder sb = new StringBuilder();
            List<? extends Slide<?, ?>> slides = ss.getSlides();
            sb.append("# ").append(in.getName().replaceAll("\\.pptx?$", "")).append("\n\n");
            sb.append("> 來源：`").append(in.getName()).append("`，共 ").append(slides.size())
              .append(" 張投影片。圖表只標示位置，請看 `").append(a[2]).append("` 的同一頁。\n");
            int n = 0;
            for (Slide<?, ?> s : slides) {
                n++;
                String title = clean(s.getTitle());
                sb.append("\n## Slide ").append(n);
                if (!title.isEmpty()) sb.append(" — ").append(title.replace("\n", " "));
                if (s.isHidden()) sb.append("（隱藏投影片）");
                sb.append("\n\n");
                StringBuilder body = new StringBuilder();
                int[] pics = {0};
                for (Shape<?, ?> sh : ordered(s.getShapes())) walk(sh, body, pics, 0);
                if (pics[0] > 0) body.append("［圖 ×").append(pics[0]).append("：見 PDF 第 ").append(n).append(" 頁］\n");
                sb.append(body.length() == 0 ? "（無文字）\n" : body);
                Notes<?, ?> notes = s.getNotes();
                if (notes != null) {
                    StringBuilder nb = new StringBuilder();
                    for (Shape<?, ?> sh : notes.getShapes()) {
                        if (sh instanceof TextShape && !(isPlaceholder(sh, EnumSet.of(Placeholder.SLIDE_IMAGE, Placeholder.SLIDE_NUMBER, Placeholder.HEADER, Placeholder.FOOTER, Placeholder.DATETIME)))) {
                            String t = clean(((TextShape<?, ?>) sh).getText());
                            if (!t.isEmpty()) nb.append(t).append("\n");
                        }
                    }
                    String t = nb.toString().trim();
                    if (!t.isEmpty() && !t.matches("^\\d+$")) sb.append("\n> 備忘稿：").append(t.replace("\n", "\n> ")).append("\n");
                }
            }
            Files.writeString(Path.of(a[1]), sb.toString(), StandardCharsets.UTF_8);
            System.out.println(in.getName() + ": " + slides.size() + " slides");
        }
    }

    static boolean isPlaceholder(Shape<?, ?> sh, Set<Placeholder> kinds) {
        if (sh instanceof SimpleShape) {
            Placeholder p = ((SimpleShape<?, ?>) sh).getPlaceholder();
            return p != null && kinds.contains(p);
        }
        return false;
    }

    static List<Shape<?, ?>> ordered(Iterable<? extends Shape<?, ?>> shapes) {
        List<Shape<?, ?>> list = new ArrayList<>();
        for (Shape<?, ?> s : shapes) list.add(s);
        list.sort((x, y) -> {
            Rectangle2D ax = anchor(x), ay = anchor(y);
            if (Math.abs(ax.getY() - ay.getY()) > 12) return Double.compare(ax.getY(), ay.getY());
            return Double.compare(ax.getX(), ay.getX());
        });
        return list;
    }

    static Rectangle2D anchor(Shape<?, ?> s) {
        try { Rectangle2D r = s.getAnchor(); return r == null ? new Rectangle2D.Double() : r; }
        catch (Exception e) { return new Rectangle2D.Double(); }
    }

    static void walk(Shape<?, ?> sh, StringBuilder out, int[] pics, int depth) {
        if (isPlaceholder(sh, SKIP)) return;
        if (sh instanceof GroupShape) {
            for (Shape<?, ?> c : ordered((GroupShape<?, ?>) sh)) walk(c, out, pics, depth + 1);
        } else if (sh instanceof TableShape) {
            TableShape<?, ?> t = (TableShape<?, ?>) sh;
            int rows = t.getNumberOfRows(), cols = t.getNumberOfColumns();
            for (int r = 0; r < rows; r++) {
                out.append("|");
                for (int c = 0; c < cols; c++) {
                    TableCell<?, ?> cell = t.getCell(r, c);
                    String v = cell == null ? "" : clean(cell.getText()).replace("\n", "<br>").replace("|", "\\|");
                    out.append(" ").append(v).append(" |");
                }
                out.append("\n");
                if (r == 0) out.append("|").append(" --- |".repeat(cols)).append("\n");
            }
            out.append("\n");
        } else if (sh instanceof TextShape) {
            for (TextParagraph<?, ?, ?> p : ((TextShape<?, ?>) sh)) {
                StringBuilder line = new StringBuilder();
                for (TextRun r : p) { String raw = r.getRawText(); if (raw != null) line.append(raw); }
                String t = clean(line.toString());
                if (t.isEmpty()) continue;
                int lvl = Math.max(0, p.getIndentLevel());
                boolean bullet = p.getBulletStyle() != null;
                out.append("  ".repeat(lvl)).append(bullet ? "- " : "").append(t.replace("\n", "\n" + "  ".repeat(lvl) + (bullet ? "  " : ""))).append(bullet ? "\n" : "\n\n");
            }
            if (sh instanceof PictureShape) pics[0]++;
        } else if (sh instanceof PictureShape) {
            pics[0]++;
        } else if (sh.getClass().getSimpleName().contains("Graphic") || sh.getClass().getSimpleName().contains("Object")) {
            pics[0]++;
        }
    }

    static String clean(String s) {
        if (s == null) return "";
        return s.replace('\u000b', '\n').replace("\r", "\n").replace("_x000b_", "\n")
                .replace('\u00a0', ' ').replaceAll("[ \\t]+\n", "\n").replaceAll("\n{3,}", "\n\n").trim();
    }
}
