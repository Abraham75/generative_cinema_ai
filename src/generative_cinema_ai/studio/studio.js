"use strict";
const $ = id => document.getElementById(id);
const fields = {description: "Shot description", frame: "Framing", lens: "Lens", movement: "Camera movement", lighting_color: "Lighting & color", texture: "Texture"};
const trace = {tenant_id: crypto.randomUUID(), project_id: crypto.randomUUID()};
let analysis, selected, dirty = false;
let plans = new Map();
const node = (tag, text, className) => {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
};
function button(label, fn) {
  const b = node("button", label);
  b.type = "button";
  b.onclick = fn;
  return b;
}
function status(message) { $("status").textContent = message; }
function showWorkspace(show) {
  $("intake").hidden = show;
  $("workspace").hidden = !show;
  status("");
}
$("sample").onclick = () => {
  if ($("script").value.trim() && !confirm("Replace the text in the editor with the sample?")) return;
  $("script").value = "INT. PROJECTION ROOM - NIGHT\n\nMara listens in the dark. A reel clicks to a stop.\n\nEXT. THEATER ROOF - DAWN\n\nMara opens the door. The city reveals itself below.";
  $("script").focus();
};
$("file").onchange = async event => {
  const file = event.target.files[0];
  event.target.value = "";
  if (!file) return;
  if (file.size > 2000000 || !/\.(txt|fountain)$/i.test(file.name)) {
    status("Choose a .txt or .fountain text file under 2 MB."); return;
  }
  try {
    const value = await file.text();
    if (value.length > 500000) { status("Choose a smaller excerpt (up to 500,000 characters)."); return; }
    if ($("script").value.trim() && !confirm("Replace the text in the editor with this file?")) return;
    $("script").value = value;
    status("Imported " + file.name);
  } catch { status("The file could not be read. Try pasting its text."); }
};
const back = button("Return to shot planner", () => showWorkspace(true));
back.hidden = true;
$("script-form").after(back);
$("revise").onclick = () => { showWorkspace(false); $("script").focus(); };
$("script-form").onsubmit = async event => {
  event.preventDefault();
  if (!$("script").value.trim()) { status("Enter a scene to analyze."); return; }
  if (dirty && !confirm("A new analysis will replace your current shot list. Continue?")) return;
  const form = event.currentTarget;
  const controls = [...form.querySelectorAll("input,select,textarea,button")];
  controls.forEach(control => { control.disabled = true; });
  back.disabled = true;
  status("Analyzing screenplay…");
  try {
    const response = await fetch("/v1/analysis", {method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({...trace, screenplay_text: $("script").value, input_format: $("format").value})});
    if (!response.ok) throw new Error(response.status === 413 ? "This script exceeds the server byte limit. Try a shorter excerpt." : "Analysis failed. Check the script and try again.");
    const next = await response.json();
    analysis = next;
    plans = new Map(analysis.scenes.map(({scene}) => [scene.id, []]));
    dirty = false;
    selected = analysis.scenes.findIndex(({scene}) => scene.id !== "scene-000");
    $("warning").textContent = analysis.warnings.join(" ");
    $("warning").hidden = !analysis.warnings.length;
    back.hidden = false;
    showWorkspace(true);
    render();
    $("scene").querySelector("h2").focus();
  } catch (error) { status(error instanceof TypeError ? "Could not reach the local server. Check that it is running and retry." : error.message); }
  finally { controls.forEach(control => { control.disabled = false; }); back.disabled = false; }
};
function counts() {
  const shots = [...plans.values()].flat();
  const approved = shots.filter(shot => shot.approved).length;
  $("summary").textContent = shots.length + " planned · " + approved + " approved";
  $("export").disabled = approved === 0;
}
function sourcePanel(entry) {
  const panel = node("details");
  panel.open = true;
  panel.append(node("summary", "Screenplay evidence"));
  const pre = node("pre", undefined, "source");
  const chars = Array.from(entry.scene.text);
  const spans = entry.recommendations.flatMap(r => r.evidence).sort((a,b) => a.start-b.start);
  let cursor = 0;
  for (const span of spans) {
    const start = span.start-entry.scene.source_span.start, end = span.end-entry.scene.source_span.start;
    if (start < cursor) continue;
    pre.append(chars.slice(cursor,start).join(""), node("mark", chars.slice(start,end).join("")));
    cursor = end;
  }
  pre.append(chars.slice(cursor).join(""));
  panel.append(pre);
  return panel;
}
function render() {
  counts();
  $("index").replaceChildren(...analysis.scenes.map(({scene}, index) => {
    const label = scene.id === "scene-000" ? "Preamble" : scene.heading;
    const b = button(label, () => { selected = index; render(); $("scene").querySelector("h2").focus(); });
    b.setAttribute("aria-current", String(selected === index));
    return b;
  }));
  const entry = analysis.scenes[selected], scene = entry.scene;
  const title = node("h2", scene.heading);
  title.tabIndex = -1;
  const article = $("scene");
  article.replaceChildren(title, sourcePanel(entry));
  if (scene.id === "scene-000") return;
  const info = node("details", undefined, "treatment");
  info.append(node("summary", "Suggested visual treatment · " + entry.signals.join(", ")));
  info.append(node("p", entry.recommendations[0].rationale, "reference"));
  for (const rec of entry.recommendations) {
    info.append(node("p", fields[rec.category] + " — " + rec.value));
  }
  article.append(info);
  const head = node("div", undefined, "bar");
  head.append(node("h2", "Coverage"), button("Add shot", () => {
    const values = Object.fromEntries(entry.recommendations.map(r => [r.category, r.value]));
    plans.get(scene.id).push({...values, description:"", approved:false});
    dirty = true;
    render();
    article.querySelector(".shot:last-child input").focus();
  }));
  article.append(head);
  const shots = plans.get(scene.id);
  if (!shots.length) article.append(node("p", "Add a shot to start with this treatment. Describe the beat you want to capture, then approve it for export.", "reference"));
  shots.forEach((shot,index) => {
    const row = node("section", undefined, "shot");
    row.append(node("h3", "Shot " + (index+1)));
    const approve = node("input");
    approve.type = "checkbox"; approve.checked = shot.approved; approve.disabled = !shot.description.trim();
    for (const [key, name] of Object.entries(fields)) {
      const label = node("label", name);
      const input = node("input");
      input.type = "text"; input.value = shot[key];
      input.oninput = () => {
        shot[key] = input.value; shot.approved = false; approve.checked = false;
        approve.disabled = !shot.description.trim(); dirty = true; counts();
      };
      label.append(input); row.append(label);
    }
    const bar = node("div", undefined, "bar"), label = node("label");
    approve.onchange = () => { shot.approved = approve.checked; dirty = true; counts(); };
    label.append(approve, " Approved for export");
    bar.append(label, button("Remove shot", () => {
      if (!confirm("Remove this shot from the plan?")) return;
      shots.splice(index,1); dirty = true; render();
    }));
    row.append(bar); article.append(row);
  });
}
function csvCell(value) {
  // Spreadsheet programs may evaluate formula-looking text even in quoted cells.
  const text = /^\s*[=+@-]|^[\t\r\n]/.test(value) ? "'" + value : String(value);
  return '"' + text.replaceAll('"','""') + '"';
}
$("export").onclick = () => {
  const rows = [["Scene ID","Scene heading","Shot",...Object.values(fields)]];
  for (const {scene} of analysis.scenes) {
    plans.get(scene.id).forEach((shot,i) => {
      if (shot.approved) rows.push([scene.id,scene.heading,i+1,...Object.keys(fields).map(key => shot[key])]);
    });
  }
  const data = rows.map(row => row.map(csvCell).join(",")).join("\r\n");
  const url = URL.createObjectURL(new Blob(["\uFEFF",data], {type:"text/csv;charset=utf-8"}));
  const link = node("a"); link.href = url; link.download = "approved-shot-list.csv"; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status("Exported " + (rows.length-1) + " approved shot(s).");
};
