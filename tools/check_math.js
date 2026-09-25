// Render every $...$ / $$...$$ formula in the worked solutions with KaTeX and
// report any that fail, plus any stray control characters (a sign that a
// backslash sequence like \f or \n was eaten while the file was written).
//
// Usage: node tools/check_math.js
const fs = require("fs");
const path = require("path");
const katex = require("../app/static/vendor/katex/katex.min.js");

const root = path.join(__dirname, "..", "amc_questions");
let files = 0, formulas = 0, problems = 0;

function strings(value, where, out) {
  if (typeof value === "string") out.push([where, value]);
  else if (Array.isArray(value)) value.forEach((v, i) => strings(v, `${where}[${i}]`, out));
  else if (value && typeof value === "object") {
    for (const [k, v] of Object.entries(value)) strings(v, where ? `${where}.${k}` : k, out);
  }
  return out;
}

// Every worked/ folder: amc_questions/<year>/worked and amc_questions/ace-amc-book/<topic>/worked.
function workedDirs(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!e.isDirectory()) continue;
    const sub = path.join(dir, e.name);
    if (e.name === "worked") out.push(sub);
    else workedDirs(sub, out);
  }
  return out;
}

for (const dir of workedDirs(root)) {
  for (const name of fs.readdirSync(dir).filter((n) => n.endsWith(".json"))) {
    files++;
    const data = JSON.parse(fs.readFileSync(path.join(dir, name), "utf8"));
    for (const [where, text] of strings(data, "", [])) {
      if (/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(text)) {
        problems++;
        console.log(`${name} ${where}: control character in text`);
      }
      const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
      let m;
      while ((m = re.exec(text))) {
        formulas++;
        try {
          katex.renderToString(m[1] ?? m[2], { displayMode: !!m[1], throwOnError: true });
        } catch (e) {
          problems++;
          console.log(`${name} ${where}: ${e.message.split("\n")[0]}`);
        }
      }
    }
  }
}
console.log(`${files} files, ${formulas} formulas, ${problems} problems`);
process.exit(problems ? 1 : 0);
