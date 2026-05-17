const fs = require('fs')
const path = require('path')
const { marked } = require('marked')
const { chromium } = require('playwright')

const [input, output, title] = process.argv.slice(2)

if (!input || !output) {
  console.error('Usage: node md-to-pdf.js <input.md> <output.pdf> [title]')
  process.exit(1)
}

const markdown = fs.readFileSync(input, 'utf8')
const body = marked.parse(markdown)

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>${title || path.basename(input)}</title>
  <style>
    @page { size: A4; margin: 18mm 16mm; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: #172326;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      font-size: 11.5px;
      line-height: 1.68;
      background: #fff;
    }
    h1 {
      margin: 0 0 16px;
      color: #07999B;
      font-size: 28px;
      line-height: 1.2;
      letter-spacing: 0;
    }
    h2 {
      margin: 24px 0 9px;
      padding-top: 2px;
      color: #07999B;
      font-size: 18px;
      line-height: 1.35;
      border-top: 1px solid rgba(20, 200, 200, 0.18);
    }
    h3 {
      margin: 16px 0 7px;
      color: #172326;
      font-size: 14px;
    }
    p { margin: 0 0 8px; }
    ul, ol { margin: 6px 0 10px 18px; padding: 0; }
    li { margin: 2px 0; }
    table {
      width: 100%;
      margin: 10px 0 14px;
      border-collapse: collapse;
      page-break-inside: avoid;
      font-size: 10px;
    }
    th {
      background: rgba(20, 200, 200, 0.10);
      color: #07999B;
      font-weight: 700;
    }
    th, td {
      border: 1px solid rgba(23, 35, 38, 0.10);
      padding: 6px 7px;
      vertical-align: top;
    }
    code {
      padding: 1px 4px;
      border-radius: 5px;
      background: rgba(20, 200, 200, 0.08);
      color: #07999B;
      font-family: Menlo, Consolas, monospace;
      font-size: 10px;
    }
    pre {
      margin: 10px 0 14px;
      padding: 10px 12px;
      border: 1px solid rgba(20, 200, 200, 0.18);
      border-radius: 10px;
      background: #F7FBFB;
      white-space: pre-wrap;
      word-break: break-word;
      page-break-inside: avoid;
    }
    pre code {
      padding: 0;
      background: transparent;
      color: #172326;
      font-size: 9.5px;
      line-height: 1.55;
    }
    blockquote {
      margin: 10px 0;
      padding: 8px 12px;
      border-left: 3px solid #14C8C8;
      background: rgba(20, 200, 200, 0.08);
    }
  </style>
</head>
<body>${body}</body>
</html>`

async function main() {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage()
  await page.setContent(html, { waitUntil: 'networkidle' })
  await page.pdf({
    path: output,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true
  })
  await browser.close()
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
